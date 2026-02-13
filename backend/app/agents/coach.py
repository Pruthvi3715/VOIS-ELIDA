from typing import Any, Dict, List
from app.agents.base import BaseAgent
import re


class CoachAgent(BaseAgent):
    """
    Decision Synthesis (Coach) Agent - Combines all agent insights into final recommendation.
    Enhanced with weighted synthesis, conflict resolution, and structured output.
    """
    
    def __init__(self):
        super().__init__(name="Coach Synthesizer")
        
        # Agent weight configuration
        self.agent_weights = {
            "Quant Agent": 0.30,
            "Macro Agent": 0.20,
            "Philosopher Agent": 0.15,
            "Regret Simulation Agent": 0.20,
            "Technical": 0.15
        }

    def run(self, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synthesize insights from all agents into a final recommendation.
        """
        # Extract and organize agent insights
        insights = [str(c.get("content")) for c in context]
        context_str = "\n---\n".join(insights) if insights else "No Agent Insights found in RAG."
        
        # Extract asset identifier from context
        asset_id = "Unknown"
        for c in context:
            content_str = str(c.get("content", ""))
            if "Symbol:" in content_str or "ANALYZING:" in content_str:
                symbol_match = re.search(r'Symbol:\s*(\S+)', content_str)
                if symbol_match:
                    asset_id = symbol_match.group(1)
                    break
            # Also try extracting from agent insight format
            if "Agent:" in content_str and asset_id == "Unknown":
                ticker_match = re.search(r'\b([A-Z]{1,5}(?:\.NS|\.BO)?)\b', content_str)
                if ticker_match:
                    asset_id = ticker_match.group(1)
        
        data_quality = self.calculate_data_quality(context)
        
        prompt = f"""Synthesize agent insights for {asset_id} into final recommendation. Return JSON only.

IMPORTANT: Only reference data, indicators, and metrics that appear in the agent insights below.
Do NOT invent or reference any indicators, VIX levels, or metrics not explicitly mentioned by the agents.

AGENT INSIGHTS:
{context_str}

OUTPUT FORMAT:
{{
    "verdict": "One compelling sentence summary for {asset_id}",
    "action": "Buy|Hold|Sell",
    "confidence": 0-100,
    "position_size": "Full|Half|Quarter|None",
    "reasoning": "2-3 sentences explaining why, citing ONLY agent signals present above",
    "key_risks": ["Top 1-2 risks from agent data"],
    "catalysts": ["Top 1-2 positive triggers from agent data"]
}}

Weigh: Quant (30%), Macro (20%), Regret (20%), Philosopher (15%). Resolve any conflicts."""
        
        response = self.call_llm(
            prompt=prompt,
            system_prompt=self.get_guardrail_system_prompt("You are a wise Investment Coach. Synthesize all agent inputs into a balanced recommendation. Output valid JSON. Only reference insights that exist in the provided agent outputs."),
            fallback_func=self._heuristic_synthesis,
            fallback_args=context
        )
        
        # Parse response
        parsed = self._parse_response(response)
        
        # Determine if fallback was used
        fallback_used = "[Fallback]" in response or "[Heuristic]" in response
        
        return self.format_output(
            output_data={
                "verdict": parsed.get("verdict", ""),
                "action": parsed["action"],
                "position_size": parsed.get("position_size", "Half"),
                "agent_synthesis": parsed.get("agent_synthesis", []),
                "agreements": parsed.get("agreements", []),
                "conflicts": parsed.get("conflicts", []),
                "key_risks": parsed.get("key_risks", []),
                "catalysts": parsed.get("catalysts", [])
            },
            confidence=parsed["confidence"],
            data_quality=data_quality,
            fallback_used=fallback_used,
            analysis=parsed.get("reasoning", response)
        )

    def compare_analysis(self, stock1: str, data1: Dict[str, Any], stock2: str, data2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two stocks based on their agent analyses.
        """
        prompt = f"""
        You are the Investment Coach. Compare two stocks side-by-side based on their AI analysis data.

        STOCK A: {stock1}
        Analysis: {str(data1)[:3000]}

        STOCK B: {stock2}
        Analysis: {str(data2)[:3000]}

        TASK:
        Provide a Head-to-Head comparison. For EACH agent dimension (Quant, Macro, Philosopher, Regret), pick a winner and explain why.

        OUTPUT FORMAT (STRICT JSON):
        {{
            "overall_winner": "{stock1} or {stock2} or Tie",
            "overall_reasoning": "concise verdict summary...",
            "dimensions": {{
                "Quant": {{ "winner": "{stock1}", "reason": "Lower P/E (15 vs 25) and higher efficiency" }},
                "Macro": {{ "winner": "{stock2}", "reason": "Better defensive qualities in recession" }},
                "Philosopher": {{ "winner": "Tie", "reason": "Both have strong governance" }},
                "Regret": {{ "winner": "{stock1}", "reason": "Lower downside risk" }}
            }}
        }}
        """
        
        response = self.call_llm(
            prompt=prompt,
            system_prompt="You are a Comparative Financial Analyst. Be decisive and specific.",
        )
        
        return self.parse_json_from_response(response) or {
            "overall_winner": "Tie",
            "overall_reasoning": "Could not generate comparison.",
            "dimensions": {}
        }

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        """
        result = {
            "verdict": "",
            "action": "Hold",
            "confidence": 50,
            "position_size": "Half",
            "agent_synthesis": [],
            "agreements": [],
            "conflicts": [],
            "key_risks": [],
            "catalysts": [],
            "reasoning": response
        }
        
        # Try JSON parsing
        parsed_json = self.parse_json_from_response(response)
        if parsed_json:
            result.update(parsed_json)
            # Validate action
            valid_actions = ["Buy", "Hold", "Sell"]
            if result["action"] not in valid_actions:
                result["action"] = self.extract_level(result["action"], valid_actions, "Hold")
            result["confidence"] = max(0, min(100, result.get("confidence", 50)))
            return result
        
        # Fallback extraction
        if "Action: Buy" in response or "action\": \"Buy" in response:
            result["action"] = "Buy"
        elif "Action: Sell" in response or "action\": \"Sell" in response:
            result["action"] = "Sell"
        else:
            result["action"] = "Hold"
        
        result["confidence"] = self.extract_confidence(response, 50)
        
        # Extract verdict
        verdict_match = re.search(r'Verdict:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
        if verdict_match:
            result["verdict"] = verdict_match.group(1).strip()
        
        return result

    def _heuristic_synthesis(self, context: List[Dict[str, Any]]) -> str:
        """
        Heuristic-based synthesis when LLM unavailable.
        """
        full_text = " ".join([str(c.get("content", "")) for c in context])
        
        # Count signals
        positive_signals = 0
        negative_signals = 0
        agent_synthesis = []
        agreements = []
        conflicts = []
        
        # Analyze Quant signals
        quant_positive = full_text.count("score") and any(
            f"score\": {s}" in full_text.lower() or f"Score: {s}" in full_text 
            for s in range(60, 101)
        )
        quant_negative = "score\": 4" in full_text.lower() or "Score: 4" in full_text or "Score: 3" in full_text
        
        if "Quant" in full_text:
            if quant_positive or "attractive" in full_text.lower():
                positive_signals += 2
                agent_synthesis.append({
                    "agent": "Quant Agent",
                    "signal": "positive",
                    "weight_applied": 0.30,
                    "key_insight": "Favorable valuation metrics"
                })
            elif quant_negative or "overvalued" in full_text.lower():
                negative_signals += 2
                agent_synthesis.append({
                    "agent": "Quant Agent",
                    "signal": "negative",
                    "weight_applied": 0.30,
                    "key_insight": "Valuation concerns"
                })
            else:
                agent_synthesis.append({
                    "agent": "Quant Agent",
                    "signal": "neutral",
                    "weight_applied": 0.30,
                    "key_insight": "Mixed fundamentals"
                })
        
        # Analyze Macro signals
        if "Bullish" in full_text:
            positive_signals += 1
            agent_synthesis.append({
                "agent": "Macro Agent",
                "signal": "positive",
                "weight_applied": 0.20,
                "key_insight": "Supportive macro environment"
            })
        elif "Bearish" in full_text:
            negative_signals += 1
            agent_synthesis.append({
                "agent": "Macro Agent",
                "signal": "negative",
                "weight_applied": 0.20,
                "key_insight": "Challenging macro conditions"
            })
        else:
            agent_synthesis.append({
                "agent": "Macro Agent",
                "signal": "neutral",
                "weight_applied": 0.20,
                "key_insight": "Neutral macro backdrop"
            })
        
        # Analyze Risk signals
        if "High" in full_text and "Risk" in full_text:
            negative_signals += 1.5
            agent_synthesis.append({
                "agent": "Regret Agent",
                "signal": "negative",
                "weight_applied": 0.20,
                "key_insight": "Elevated downside risks identified"
            })
        elif "Low" in full_text and "Risk" in full_text:
            positive_signals += 1
            agent_synthesis.append({
                "agent": "Regret Agent",
                "signal": "positive",
                "weight_applied": 0.20,
                "key_insight": "Manageable risk profile"
            })
        else:
            agent_synthesis.append({
                "agent": "Regret Agent",
                "signal": "neutral",
                "weight_applied": 0.20,
                "key_insight": "Standard sector risks"
            })
        
        # Analyze Alignment
        if "High" in full_text and "Alignment" in full_text:
            positive_signals += 0.5
            agent_synthesis.append({
                "agent": "Philosopher Agent",
                "signal": "positive",
                "weight_applied": 0.15,
                "key_insight": "Strong long-term alignment"
            })
        elif "Low" in full_text and "Alignment" in full_text:
            negative_signals += 0.5
            agent_synthesis.append({
                "agent": "Philosopher Agent",
                "signal": "negative",
                "weight_applied": 0.15,
                "key_insight": "Ethical or sustainability concerns"
            })
        
        # Determine action
        net_signal = positive_signals - negative_signals
        
        if net_signal >= 2:
            action = "Buy"
            position_size = "Full" if net_signal >= 3 else "Half"
            verdict = "Positive signals dominate - investment opportunity identified"
            confidence = min(75, 50 + int(net_signal * 8))
        elif net_signal <= -1.5:
            action = "Sell"
            position_size = "None"
            verdict = "Negative signals outweigh positives - avoid or reduce exposure"
            confidence = min(70, 50 + int(abs(net_signal) * 8))
        else:
            action = "Hold"
            position_size = "Quarter" if net_signal > 0 else "None"
            verdict = "Mixed signals warrant cautious approach"
            confidence = 45
        
        # Identify agreements/conflicts
        signals = [s.get("signal") for s in agent_synthesis]
        if signals.count("positive") >= 3:
            agreements.append("Multiple agents signal positive outlook")
        if signals.count("negative") >= 3:
            agreements.append("Multiple agents signal caution")
        if "positive" in signals and "negative" in signals:
            conflicts.append("Agents disagree on overall outlook - balanced position recommended")
        
        result = {
            "verdict": verdict,
            "action": action,
            "confidence": confidence,
            "position_size": position_size,
            "agent_synthesis": agent_synthesis,
            "agreements": agreements if agreements else ["Standard market considerations apply"],
            "conflicts": conflicts if conflicts else ["No major conflicts between agents"],
            "key_risks": ["Market volatility", "Company-specific execution risk"],
            "catalysts": ["Positive earnings surprise", "Sector tailwinds"],
            "reasoning": f"[Heuristic Fallback] Analyzed {len(agent_synthesis)} agent signals. " +
                        f"Net score: {net_signal:+.1f} ({positive_signals:.1f} positive vs {negative_signals:.1f} negative). " +
                        f"Recommendation: {action} with {position_size} position."
        }
        
        import json
        return f"[Heuristic Synthesis]\n```json\n{json.dumps(result, indent=2)}\n```"


coach_agent = CoachAgent()
