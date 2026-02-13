import chromadb
from chromadb.config import Settings
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from typing import List, Dict, Any, Optional
import uuid
import hashlib
from datetime import datetime

# Try to import sentence_transformers, fall back to mock if missing/fails
try:
    from sentence_transformers import SentenceTransformer
    class LocalHuggingFaceEmbeddingFunction(EmbeddingFunction):
        def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
            self.model = SentenceTransformer(model_name)
        
        def __call__(self, input: Documents) -> Embeddings:
            # Convert numpy array to list for Chroma
            return self.model.encode(input).tolist()
    
    HAS_REAL_EMBEDDINGS = True
    print("RAG Service: [OK] Successfully loaded sentence-transformers.")
except ImportError:
    HAS_REAL_EMBEDDINGS = False
    print("RAG Service: [WARN] sentence-transformers not found. Using Mock embeddings.")

class MockEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Create a deterministic mock embedding based on text hash
        embeddings = []
        for text in input:
            # Simple hash to float list of size 384 (standard size)
            hash_val = int(hashlib.sha256(text.encode()).hexdigest(), 16)
            # Create a simple vector pattern
            vector = [(hash_val % (i + 1)) / (i + 1) for i in range(384)]
            embeddings.append(vector)
        return embeddings


class RAGService:
    """
    Enhanced RAG Service with deduplication, document management, and improved querying.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        if HAS_REAL_EMBEDDINGS:
            self.embedding_fn = LocalHuggingFaceEmbeddingFunction()
        else:
            self.embedding_fn = MockEmbeddingFunction()
            
        self.collection = self.client.get_or_create_collection(
            name="financial_knowledge_base",
            embedding_function=self.embedding_fn
        )
        
        # Track document hashes to prevent duplicates
        self._document_hashes = set()
        self._load_existing_hashes()
    
    def _load_existing_hashes(self):
        """Load existing document hashes to prevent duplicates on restart."""
        try:
            existing = self.collection.get(include=["documents"])
            if existing and existing.get("documents"):
                for doc in existing["documents"]:
                    self._document_hashes.add(self._hash_document(doc))
            print(f"RAG Service: Loaded {len(self._document_hashes)} existing document hashes.")
        except Exception as e:
            print(f"RAG Service: [WARN] Could not load existing hashes: {e}")
    
    def _hash_document(self, document: str) -> str:
        """Create a hash for deduplication."""
        return hashlib.md5(document.encode()).hexdigest()
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: List[Dict[str, Any]],
        deduplicate: bool = True
    ) -> List[str]:
        """
        Add documents to the collection with optional deduplication.
        """
        if not documents:
            return []
        
        # Add timestamp to metadata
        for meta in metadatas:
            if "timestamp" not in meta:
                meta["timestamp"] = datetime.now().isoformat()
        
        if deduplicate:
            new_docs = []
            new_metas = []
            
            for doc, meta in zip(documents, metadatas):
                doc_hash = self._hash_document(doc)
                if doc_hash not in self._document_hashes:
                    new_docs.append(doc)
                    new_metas.append(meta)
                    self._document_hashes.add(doc_hash)
                else:
                    print(f"RAG Service: Skipping duplicate document (type: {meta.get('type', 'unknown')})")
            
            documents = new_docs
            metadatas = new_metas
        
        if not documents:
            print("RAG Service: No new documents to add (all duplicates).")
            return []
        
        ids = [str(uuid.uuid4()) for _ in documents]
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"RAG Service: Added {len(documents)} documents.")
        return ids

    def query(
        self, 
        query_text: str, 
        n_results: int = 5, 
        where: Dict = None,
        where_document: Dict = None
    ) -> Dict[str, Any]:
        """
        Query documents with optional filtering.
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where,
                where_document=where_document
            )
            
            # Log query results
            doc_count = len(results['documents'][0]) if results and results.get('documents') else 0
            print(f"RAG Service: Query '{query_text[:30]}...' returned {doc_count} results.")
            
            return results
        except Exception as e:
            print(f"RAG Service: [ERROR] Query error: {e}")
            return {"documents": [[]], "metadatas": [[]], "ids": [[]]}

    def get_by_asset(self, asset_id: str, doc_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all documents for a specific asset.
        """
        where_filter = {"asset_id": asset_id}
        if doc_type:
            where_filter["type"] = doc_type
        
        return self.query(
            query_text=f"Information about {asset_id}",
            n_results=20,
            where=where_filter
        )

    def delete_by_asset(self, asset_id: str) -> int:
        """
        Delete all documents for a specific asset (useful for refresh).
        """
        try:
            # Get documents for this asset
            results = self.collection.get(
                where={"asset_id": asset_id},
                include=["documents"]
            )
            
            if results and results.get("ids"):
                ids_to_delete = results["ids"]
                self.collection.delete(ids=ids_to_delete)
                
                # Remove from hash set
                for doc in results.get("documents", []):
                    doc_hash = self._hash_document(doc)
                    self._document_hashes.discard(doc_hash)
                
                print(f"RAG Service: Deleted {len(ids_to_delete)} documents for {asset_id}.")
                return len(ids_to_delete)
            
            return 0
        except Exception as e:
            print(f"RAG Service: ❌ Delete error: {e}")
            return 0

    def clear_all(self):
        """Clear all documents from the collection."""
        try:
            self.client.delete_collection("financial_knowledge_base")
            self.collection = self.client.get_or_create_collection(
                name="financial_knowledge_base",
                embedding_function=self.embedding_fn
            )
            self._document_hashes.clear()
            print("RAG Service: Cleared all documents.")
        except Exception as e:
            print(f"RAG Service: ❌ Clear error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG store."""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "hash_count": len(self._document_hashes),
                "has_real_embeddings": HAS_REAL_EMBEDDINGS
            }
        except Exception as e:
            return {"error": str(e)}


rag_service = RAGService()
