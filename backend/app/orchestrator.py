from app.agents.scout import scout_agent
from app.services.rag_service import rag_service
from app.services.match_score_service import match_score_service
from app.agents.quant import quant_agent
from app.agents.macro import macro_agent
from app.agents.philosopher import philosopher_agent
from app.agents.regret import regret_agent
from app.agents.coach import coach_agent
from app.models.investor_dna import InvestorDNA, DEFAULT_INVESTOR_DNA
from typing import Optional, Dict, Any


class FinancialOrchestrator:
    """
    Orchestrates the full analysis pipeline:
    1. Data ingestion via Scout
    2. RAG storage
    3. Multi-agent analysis
    4. Match Score calculation
    5. Coach synthesis
    """
    
    def __init__(self):
        self.current_asset_data: Dict[str, Any] = {}
    
    def ingest_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        Phase 1: Ingestion & Memory Population
        """
        print(f"Orchestrator: Starting ingestion for {asset_id}")
        try:
            # 1. Scout collects data
            raw_data = scout_agent.collect_data(asset_id)
            
            # Store for later use in match score
            self.current_asset_data[asset_id] = raw_data
            
            # 2. Process and Chunk
            documents = []
            metadatas = []
            
            # Financials
            documents.append(str(raw_data["financials"]))
            metadatas.append({"asset_id": asset_id, "type": "financials"})
            
            # Macro
            documents.append(str(raw_data["macro"]))
            metadatas.append({"asset_id": "GLOBAL", "type": "macro"})

            # Technicals
            if "technicals" in raw_data:
                documents.append(str(raw_data["technicals"]))
                metadatas.append({"asset_id": asset_id, "type": "technicals"})
            
            # News
            for news_item in raw_data.get("news", []):
                if isinstance(news_item, dict):
                    news_text = f"News: {news_item.get('title', '')} - {news_item.get('publisher', '')}"
                else:
                    news_text = str(news_item)
                documents.append(news_text)
                metadatas.append({"asset_id": asset_id, "type": "news"})
                
            # 3. Store in Shared Memory (RAG)
            rag_service.add_documents(documents, metadatas)
            print(f"Orchestrator: Ingestion complete for {asset_id}")
            
            # Return technicals (including history) to the frontend
            return {
                "status": "success", 
                "asset_id": asset_id,
                "market_data": raw_data.get("technicals", {}),
                "data_quality": raw_data.get("data_quality", {})
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e

    def retrieve_context(
        self, 
        query: str, 
        asset_id: str,
        investor_dna: Optional[InvestorDNA] = None
    ) -> Dict[str, Any]:
        """
        Phase 2: Centralized Retrieval & Agent Orchestration with Match Score
        """
        try:
            # Use default DNA if not provided
            if investor_dna is None:
                investor_dna = DEFAULT_INVESTOR_DNA
            
            # 1. Centralized Retrieval (Scoped to current Asset) - OPTIMIZED for speed
            print(f"Orchestrator: Retrieving context for {asset_id}...")
            global_context_raw = rag_service.query(
                query_text=f"Financial analysis of {asset_id}", 
                n_results=5,  # Reduced from 15 for faster LLM processing
                where={"asset_id": asset_id}
            )
            
            # Convert to list of dicts with context trimming
            global_context = []
            MAX_CONTENT_CHARS = 2000  # Limit each context chunk
            if global_context_raw and global_context_raw['documents']:
                for i, doc in enumerate(global_context_raw['documents'][0]):
                     meta = global_context_raw['metadatas'][0][i] if global_context_raw['metadatas'] else {}
                     # Trim long content to reduce LLM prompt size
                     trimmed_doc = doc[:MAX_CONTENT_CHARS] if len(doc) > MAX_CONTENT_CHARS else doc
                     global_context.append({"content": trimmed_doc, "metadata": meta})

            # Inject Custom Rules into Context
            if investor_dna.custom_rules:
                rules_text = "IMPORTANT USER RULES (Must be respected):\n" + "\n".join(f"- {rule}" for rule in investor_dna.custom_rules)
                global_context.append({
                    "content": rules_text, 
                    "metadata": {"type": "user_instructions", "source": "investor_dna"}
                })
                print(f"Orchestrator: Injected {len(investor_dna.custom_rules)} custom rules.")

            # 2. Invoke Analysis Agents (Parallel Execution)
            print("Orchestrator: Invoking agents (Parallel Execution)...")
            import time
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            start_time = time.time()
            
            # Map agent instances to their names for result organization
            agent_map = {
                quant_agent: "quant",
                macro_agent: "macro",
                philosopher_agent: "philosopher",
                regret_agent: "regret"
            }
            
            agent_results = {}
            
            # Use ThreadPoolExecutor for parallel calls
            with ThreadPoolExecutor(max_workers=4) as executor:
                # Submit all tasks
                future_to_agent = {
                    executor.submit(agent.run, global_context): agent_map[agent] 
                    for agent in agent_map
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_agent):
                    agent_name = future_to_agent[future]
                    try:
                        result = future.result()
                        agent_results[agent_name] = result
                        print(f"  → Agent {agent_name.upper()} completed.")
                    except Exception as e:
                        print(f"  ❌ Agent {agent_name.upper()} failed: {e}")
                        agent_results[agent_name] = {"error": str(e), "analysis": f"Analysis failed: {str(e)}"}

            elapsed = time.time() - start_time
            print(f"Orchestrator: Agent analysis completed in {elapsed:.2f} seconds")
            
            # 3. Calculate Match Score
            print("Orchestrator: Calculating Match Score...")
            asset_data = self.current_asset_data.get(asset_id, {})
            
            # If we don't have cached data, reconstruct from RAG
            if not asset_data:
                asset_data = self._reconstruct_asset_data(global_context)
            
            match_result = match_score_service.calculate_match_score(
                agent_results=agent_results,
                asset_data=asset_data,
                investor_dna=investor_dna
            )
            
            print(f"Orchestrator: Match Score = {match_result.match_score}%")
            
            # 4. Store Agent Insights to RAG
            insight_docs = []
            insight_metas = []
            for agent_name, res in agent_results.items():
                analysis = res.get('analysis', str(res))
                score_key = res.get('score') or res.get('trend') or res.get('alignment_score') or res.get('risk_level')
                content = f"Agent: {agent_name.upper()}\nAnalysis: {analysis}\nKey Metric: {score_key}"
                insight_docs.append(content)
                insight_metas.append({
                    "asset_id": asset_id, 
                    "type": "agent_insight", 
                    "source_agent": agent_name
                })

            rag_service.add_documents(insight_docs, insight_metas)
            
            # 5. Retrieve Insights for Coach
            print("Orchestrator: Retrieving Insights from RAG for Coach...")
            coach_context_raw = rag_service.query(
                query_text=f"Analysis of {asset_id}", 
                n_results=10, 
                where={"type": "agent_insight"}
            )
            
            coach_context = []
            if coach_context_raw and coach_context_raw['documents']:
                 for doc in coach_context_raw['documents'][0]:
                     coach_context.append({"content": doc, "metadata": {"type": "agent_insight"}})

            # 6. Coach Synthesis
            print("Orchestrator: Invoking Coach (RAG Mode)...")
            coach_result = coach_agent.run(coach_context)
            
            return {
                "orchestration_id": "orch_v2_match",
                "asset_id": asset_id,
                "global_context_count": len(global_context),
                "coach_retrieval_count": len(coach_context),
                
                # Agent Results
                "results": agent_results,
                
                # Match Score (NEW!)
                "match_score": match_result.match_score,
                "match_result": {
                    "score": match_result.match_score,
                    "recommendation": match_result.recommendation,
                    "action_if_owned": match_result.action_if_owned,
                    "action_if_not_owned": match_result.action_if_not_owned,
                    "fit_reasons": match_result.fit_reasons,
                    "concern_reasons": match_result.concern_reasons,
                    "summary": match_result.summary,
                    "breakdown": {
                        "fundamental": match_result.breakdown.fundamental_score,
                        "macro": match_result.breakdown.macro_score,
                        "philosophy": match_result.breakdown.philosophy_score,
                        "risk": match_result.breakdown.risk_score,
                        "dna_match": match_result.breakdown.dna_match_score
                    }
                },
                
                # Coach Verdict
                "coach_verdict": coach_result,
                
                # Market Data for charts
                "market_data": asset_data.get("technicals", {})
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
    
    def _reconstruct_asset_data(self, context: list) -> Dict[str, Any]:
        """Reconstruct asset data from RAG context."""
        import ast
        asset_data = {"financials": {}, "technicals": {}}
        
        for item in context:
            content = item.get("content", "")
            doc_type = item.get("metadata", {}).get("type", "")
            
            try:
                if doc_type == "financials":
                    data = ast.literal_eval(content) if isinstance(content, str) else content
                    asset_data["financials"] = data
                elif doc_type == "technicals":
                    data = ast.literal_eval(content) if isinstance(content, str) else content
                    asset_data["technicals"] = data
            except:
                continue
        
        return asset_data


orchestrator = FinancialOrchestrator()
