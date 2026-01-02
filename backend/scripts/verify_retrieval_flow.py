from app.agents.scout import scout_agent
from app.services.rag_service import rag_service
from app.agents.quant import quant_agent
import time

# 1. Ingest
asset_id = "ITC.NS"
print(f"Ingesting {asset_id}...")
raw_data = scout_agent.collect_data(asset_id)
documents = [str(raw_data["financials"])]
metadatas = [{"asset_id": asset_id, "type": "financials"}]
rag_service.add_documents(documents, metadatas)

# 2. Retrieve
print("Retrieving context...")
global_context_raw = rag_service.query(
    query_text=f"Financial analysis of {asset_id}", 
    n_results=10,
    where={"asset_id": asset_id}
)
global_context = []
if global_context_raw and global_context_raw['documents']:
    for i, doc in enumerate(global_context_raw['documents'][0]):
            meta = global_context_raw['metadatas'][0][i] if global_context_raw['metadatas'] else {}
            # print(f"DEBUG: Found Doc Type: {meta.get('type')}")
            global_context.append({"content": doc, "metadata": meta})

# 3. Quant Run
print("\nRunning Quant Agent...")
result = quant_agent.run(global_context)
print(f"Quant Result: {result}")
