import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, Any, List, Tuple

from app.agents.scout import scout_agent
from app.services.rag_service import rag_service
from app.services.match_score_service import match_score_service
from app.agents.quant import quant_agent
from app.agents.macro import macro_agent
from app.agents.philosopher import philosopher_agent
from app.agents.regret import regret_agent
from app.agents.coach import coach_agent
from app.models.investor_dna import InvestorDNA, DEFAULT_INVESTOR_DNA
from app.core.logging import get_logger
from app.core.exceptions import OrchestrationException, AgentException, DataFetchException

logger = get_logger("orchestrator")


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
        logger.info(f"Starting ingestion for {asset_id}")
        try:
            # 0. Clear old cache for this asset (ensure fresh analysis)
            deleted_count = rag_service.delete_by_asset(asset_id)
            if deleted_count > 0:
                logger.debug(f"Cleared {deleted_count} cached documents for {asset_id}")
            
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
            logger.info(f"Ingestion complete for {asset_id}")
            
            # Return technicals (including history) to the frontend
            return {
                "status": "success", 
                "asset_id": asset_id,
                "market_data": raw_data.get("technicals", {}),
                "data_quality": raw_data.get("data_quality", {})
            }
        except DataFetchException:
            # Re-raise explicit data errors so the API can handle them (e.g. 404)
            raise
        except Exception as e:
            logger.error(f"Ingestion failed for {asset_id}: {e}")
            raise OrchestrationException(asset_id, "ingestion", str(e))

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
            
            # 1. Centralized Retrieval - Get asset-specific AND global data
            logger.info(f"Retrieving context for {asset_id}...")
            
            # Query asset-specific data (financials, technicals, news)
            global_context_raw = rag_service.query(
                query_text=f"Financial analysis of {asset_id}", 
                n_results=15,  # Increased for better coverage
                where={"asset_id": asset_id}
            )
            
            # Also query global macro data (stored with asset_id="GLOBAL")
            macro_context_raw = rag_service.query(
                query_text="macro economic indicators interest rates GDP inflation",
                n_results=3,
                where={"asset_id": "GLOBAL"}
            )
            
            # Convert to list of dicts with context trimming
            global_context = []
            MAX_CONTENT_CHARS = 2500  # Increased for better quality
            
            # Process asset-specific data
            if global_context_raw and global_context_raw['documents']:
                for i, doc in enumerate(global_context_raw['documents'][0]):
                     meta = global_context_raw['metadatas'][0][i] if global_context_raw['metadatas'] else {}
                     trimmed_doc = doc[:MAX_CONTENT_CHARS] if len(doc) > MAX_CONTENT_CHARS else doc
                     global_context.append({"content": trimmed_doc, "metadata": meta})
            
            # Process global macro data
            if macro_context_raw and macro_context_raw['documents']:
                for i, doc in enumerate(macro_context_raw['documents'][0]):
                     meta = macro_context_raw['metadatas'][0][i] if macro_context_raw['metadatas'] else {}
                     trimmed_doc = doc[:MAX_CONTENT_CHARS] if len(doc) > MAX_CONTENT_CHARS else doc
                     global_context.append({"content": trimmed_doc, "metadata": meta})
            
            # CRITICAL: Inject cached asset data directly for reliable agent access
            cached_data = self.current_asset_data.get(asset_id, {})
            
            # HALLUCINATION PREVENTION: Always inject company name first
            company_name = cached_data.get("financials", {}).get("company_name", asset_id)
            sector = cached_data.get("financials", {}).get("sector", "Unknown")
            industry = cached_data.get("financials", {}).get("industry", "Unknown")
            
            global_context.insert(0, {
                "content": f"ANALYZING: {company_name} (Symbol: {asset_id})\nSector: {sector}\nIndustry: {industry}\n\nIMPORTANT: All analysis below is ONLY for {company_name}. Do NOT mention or analyze any other company.",
                "metadata": {"asset_id": asset_id, "type": "company_identifier", "source": "system", "priority": "HIGH"}
            })
            
            if cached_data:
                # Financials
                if cached_data.get("financials"):
                    global_context.append({
                        "content": str(cached_data["financials"]),
                        "metadata": {"asset_id": asset_id, "type": "financials", "source": "direct_cache"}
                    })
                # Technicals  
                if cached_data.get("technicals"):
                    global_context.append({
                        "content": str(cached_data["technicals"]),
                        "metadata": {"asset_id": asset_id, "type": "technicals", "source": "direct_cache"}
                    })
                # Macro
                if cached_data.get("macro"):
                    global_context.append({
                        "content": str(cached_data["macro"]),
                        "metadata": {"asset_id": "GLOBAL", "type": "macro", "source": "direct_cache"}
                    })
                
                # News (CRITICAL for Philosopher/Regret)
                if cached_data.get("news"):
                    news_items = cached_data["news"]
                    # Format news for better readability by agents
                    news_text = "RECENT NEWS:\n"
                    if isinstance(news_items, list):
                        for item in news_items[:10]: # Limit to top 10 relevant news
                           if isinstance(item, dict):
                               news_text += f"- {item.get('title', '')} ({item.get('publisher', 'Unknown')})\n"
                           else:
                               news_text += f"- {str(item)}\n"
                    
                    global_context.append({
                        "content": news_text,
                        "metadata": {"asset_id": asset_id, "type": "news", "source": "direct_cache"}
                    })

                # Company Profile/Summary (CRITICAL for alignment)
                if cached_data.get("financials", {}).get("company_profile"):
                     global_context.append({
                        "content": f"COMPANY PROFILE: {cached_data['financials']['company_profile']}",
                        "metadata": {"asset_id": asset_id, "type": "profile", "source": "direct_cache"}
                    })
                
                logger.info(f"Injected {len([k for k in cached_data if cached_data.get(k)])} cached data types for {asset_id}")

            # Inject Custom Rules into Context
            if investor_dna.custom_rules:
                rules_text = "IMPORTANT USER RULES (Must be respected):\n" + "\n".join(f"- {rule}" for rule in investor_dna.custom_rules)
                global_context.append({
                    "content": rules_text, 
                    "metadata": {"type": "user_instructions", "source": "investor_dna"}
                })
                logger.info(f"Injected {len(investor_dna.custom_rules)} custom rules")

            # 2. Invoke Analysis Agents (PARALLEL Execution for speed)
            logger.info("Invoking agents in PARALLEL...")
            import time
            
            start_time = time.time()
            
            # Agents list for parallel execution
            agents: List[Tuple] = [
                (quant_agent, "quant"),
                (macro_agent, "macro"),
                (philosopher_agent, "philosopher"),
                (regret_agent, "regret")
            ]
            
            def run_single_agent(agent_tuple):
                """Run a single agent and return result with name."""
                agent, agent_name = agent_tuple
                try:
                    logger.debug(f"Starting {agent_name.upper()} Agent...")
                    result = agent.run(global_context)
                    logger.info(f"[OK] Agent {agent_name.upper()} completed")
                    return agent_name, result
                except Exception as e:
                    logger.error(f"[ERROR] Agent {agent_name.upper()} failed: {e}")
                    return agent_name, {
                        "error": str(e), 
                        "analysis": f"Analysis failed: {str(e)}",
                        "score": 50,
                        "confidence": 0
                    }
            
            # Run all agents in parallel using ThreadPoolExecutor
            agent_results = {}
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = list(executor.map(run_single_agent, agents))
                for agent_name, result in futures:
                    agent_results[agent_name] = result

            elapsed = time.time() - start_time
            logger.info(f"Agent analysis completed in {elapsed:.2f} seconds (parallel)")
            
            # 3. Calculate Match Score
            logger.info("Calculating Match Score...")
            asset_data = self.current_asset_data.get(asset_id, {})
            
            # If we don't have cached data, reconstruct from RAG
            if not asset_data:
                asset_data = self._reconstruct_asset_data(global_context)
            
            match_result = match_score_service.calculate_match_score(
                agent_results=agent_results,
                asset_data=asset_data,
                investor_dna=investor_dna
            )
            
            logger.info(f"Match Score = {match_result.match_score}%")
            
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
            logger.debug("Retrieving Insights from RAG for Coach...")
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
            logger.info("Invoking Coach for final synthesis...")
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
