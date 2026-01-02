from typing import Any, Dict, List
from app.agents.base import BaseAgent


class RegretAgent(BaseAgent):
    """
    Regret Simulation and Downside Risk Agent - Identifies tail risk scenarios.
    Enhanced with multiple scenario modeling, probability estimation, and structured output.
    """
    
    def __init__(self):
        super().__init__(name="Regret Simulation Agent")
        
        # Sector-specific risk profiles
        self.sector_risks = {
            "Technology": {
                "scenarios": ["Regulatory crackdown on big tech", "Disruption by new technology", "Cybersecurity breach"],
                "base_risk": "Medium",
                "typical_drawdown": "30-50%"
            },
            "Healthcare": {
                "scenarios": ["Drug trial failure", "Patent expiration cliff", "Regulatory rejection"],
                "base_risk": "Medium",
                "typical_drawdown": "20-40%"
            },
            "Financial Services": {
                "scenarios": ["Credit crisis", "Regulatory fines", "Interest rate shock"],
                "base_risk": "Medium",
                "typical_drawdown": "40-60%"
            },
            "Consumer": {
                "scenarios": ["Consumer spending decline", "Brand reputation crisis", "Supply chain disruption"],
                "base_risk": "Medium",
                "typical_drawdown": "25-40%"
            },
            "Energy": {
                "scenarios": ["Oil price collapse", "Climate regulation", "Stranded assets"],
                "base_risk": "High",
                "typical_drawdown": "40-70%"
            },
        }

    def run(self, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify and simulate downside risk scenarios.
        """
        # Calculate data quality
        data_quality = self.calculate_data_quality(context)
        
        context_str = "\n".join([str(c.get("content")) for c in context])
        
        prompt = f"""
        You are the Regret Simulation and Downside Risk Agent.

        ROLE:
        Identify SPECIFIC, PLAUSIBLE downside scenarios. Avoid generic "market crash" risks. Focus on idiosyncratic risks.

        RISK CATEGORIES:
        - Company-Specific: Product failure, management scandal, earnings miss.
        - Sector-Specific: Regulatory change, commodity price shock.
        - Macro: Recession, rate hike impact.

        OUTPUT FORMAT (STRICT JSON):
        {{
            "risk_level": "<Low|Medium|High>",
            "confidence": <0-100>,
            "scenarios": [
                {{
                    "name": "Detailed Scenario Name",
                    "probability": "<Low|Medium|High>",
                    "impact": "Specific consequence (e.g., 'Revenue drops 20%')",
                    "estimated_drawdown": "<e.g. 15-20%>"
                }}
            ],
            "max_drawdown_estimate": "<worst case %>",
            "risk_mitigants": ["Specific factor that protects the downside"],
            "vulnerabilities": ["Specific weakness exposed in these scenarios"],
            "reasoning": "DETAILED SIMULATION: Describe the 'Pre-Mortem'. Imagine it is 1 year later and the investment failed. Explain exactly WHAT went wrong and WHY. be narrative and specific."
        }}

        RULES:
        1. BE SPECIFIC. "Competition" is bad. "Aggressive pricing by competitor X eroding margins by 500bps" is good.
        2. ESTIMATE IMPACT. Quantify the damage where possible.
        3. NO FEAR MONGERING. scenarios must be grounded in reality/context.

        CONTEXT (Retrieved from RAG):
        {context_str if context_str else "No risk data available in context."}
        """
        
        response = self.call_llm(
            prompt=prompt,
            system_prompt="You are a Risk Analyst focused on downside scenarios. Output valid JSON. Be thorough but realistic.",
            fallback_func=self._sector_risk_analysis,
            fallback_args=context
        )
        
        # Parse response
        parsed = self._parse_response(response)
        
        # Determine if fallback was used
        fallback_used = "[Fallback]" in response or "[Sector-Risk]" in response
        
        return self.format_output(
            output_data={
                "risk_level": parsed["risk_level"],
                "scenarios": parsed.get("scenarios", []),
                "max_drawdown_estimate": parsed.get("max_drawdown_estimate", "Unknown"),
                "risk_mitigants": parsed.get("risk_mitigants", []),
                "vulnerabilities": parsed.get("vulnerabilities", [])
            },
            confidence=parsed["confidence"],
            data_quality=data_quality,
            fallback_used=fallback_used,
            analysis=parsed.get("reasoning", response)
        )

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        """
        result = {
            "risk_level": "Medium",
            "confidence": 50,
            "scenarios": [],
            "max_drawdown_estimate": "Unknown",
            "risk_mitigants": [],
            "vulnerabilities": [],
            "reasoning": response
        }
        
        # Try JSON parsing
        parsed_json = self.parse_json_from_response(response)
        if parsed_json:
            result.update(parsed_json)
            # Validate risk level
            valid_levels = ["Low", "Medium", "High"]
            if result["risk_level"] not in valid_levels:
                result["risk_level"] = self.extract_level(result["risk_level"], valid_levels, "Medium")
            result["confidence"] = max(0, min(100, result.get("confidence", 50)))
            return result
        
        # Fallback extraction
        result["risk_level"] = self.extract_level(response, ["Low", "Medium", "High"], "Medium")
        result["confidence"] = self.extract_confidence(response, 50)
        
        # Extract drawdown if mentioned
        import re
        drawdown_match = re.search(r'(\d+)[%-]?\s*(?:to|-)?\s*(\d+)?[%-]?\s*(?:drawdown|decline)', response, re.IGNORECASE)
        if drawdown_match:
            if drawdown_match.group(2):
                result["max_drawdown_estimate"] = f"{drawdown_match.group(1)}-{drawdown_match.group(2)}%"
            else:
                result["max_drawdown_estimate"] = f"{drawdown_match.group(1)}%"
        
        return result

    def _sector_risk_analysis(self, context: List[Dict[str, Any]]) -> str:
        """
        Sector-based risk analysis fallback.
        """
        sector = None
        symbol = "Unknown"
        volatility = None
        debt_ratio = None
        
        # Extract relevant data from context
        for item in context:
            content = item.get("content", "")
            try:
                import ast
                data = content if isinstance(content, dict) else ast.literal_eval(str(content))
                
                if isinstance(data, dict):
                    if "sector" in data:
                        sector = data.get("sector")
                    if "symbol" in data:
                        symbol = data.get("symbol")
                    if "volatility_annualized" in data:
                        vol_str = str(data.get("volatility_annualized", ""))
                        try:
                            volatility = float(vol_str.replace("%", ""))
                        except:
                            pass
                    if "debt_to_equity" in data:
                        debt_ratio = data.get("debt_to_equity")
            except:
                if isinstance(content, str):
                    for s in self.sector_risks.keys():
                        if s.lower() in content.lower():
                            sector = s
                            break
        
        # Get sector defaults
        if sector and sector in self.sector_risks:
            risk_profile = self.sector_risks[sector]
            base_risk = risk_profile["base_risk"]
            scenarios_list = risk_profile["scenarios"]
            drawdown = risk_profile["typical_drawdown"]
        else:
            base_risk = "Medium"
            scenarios_list = ["Market correction", "Competitive pressure", "Operational issues"]
            drawdown = "25-40%"
            sector = sector or "Unknown"
        
        # Adjust risk based on data
        risk_level = base_risk
        vulnerabilities = []
        mitigants = []
        
        if volatility:
            if volatility > 30:
                risk_level = "High"
                vulnerabilities.append(f"High volatility ({volatility:.1f}%)")
            elif volatility < 15:
                mitigants.append(f"Low historical volatility ({volatility:.1f}%)")
        
        if debt_ratio:
            if debt_ratio > 100:
                risk_level = "High"
                vulnerabilities.append(f"High leverage (D/E: {debt_ratio:.1f})")
            elif debt_ratio < 30:
                mitigants.append(f"Conservative balance sheet (D/E: {debt_ratio:.1f})")
        
        # Build scenarios
        scenarios = [
            {
                "name": s,
                "probability": "Low" if i == 0 else "Medium",
                "impact": f"Could significantly impact {sector} sector companies",
                "estimated_drawdown": f"{15 + i*10}-{30 + i*10}%"
            }
            for i, s in enumerate(scenarios_list[:3])
        ]
        
        result = {
            "risk_level": risk_level,
            "confidence": 40,
            "scenarios": scenarios,
            "max_drawdown_estimate": drawdown,
            "risk_mitigants": mitigants if mitigants else ["Standard market diversification"],
            "vulnerabilities": vulnerabilities if vulnerabilities else [f"Sector-typical {sector} risks apply"],
            "reasoning": f"[Sector-Risk Fallback] Applied sector risk profile for {sector}. Symbol: {symbol}. " +
                        f"Base risk level: {base_risk}. Adjust position sizing for identified scenarios."
        }
        
        import json
        return f"[Sector-Risk Analysis]\n```json\n{json.dumps(result, indent=2)}\n```"


regret_agent = RegretAgent()
