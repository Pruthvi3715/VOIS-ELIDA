from typing import Any, Dict, List
from app.agents.base import BaseAgent


class QuantAgent(BaseAgent):
    """
    Quantitative Analysis Agent - Evaluates assets using numerical and financial metrics.
    Enhanced with better fallback logic, confidence scoring, and structured output.
    """
    
    def __init__(self):
        super().__init__(name="Quant Agent")
        
        # Scoring rules configuration
        self.scoring_rules = {
            "pe_ratio": {"good": (0, 15), "fair": (15, 30), "poor": (30, float('inf'))},
            "forward_pe": {"good": (0, 20), "fair": (20, 35), "poor": (35, float('inf'))},
            "peg_ratio": {"good": (0, 1), "fair": (1, 2), "poor": (2, float('inf'))},
            "debt_to_equity": {"good": (0, 50), "fair": (50, 100), "poor": (100, float('inf'))},
            "profit_margins": {"good": (0.15, 1), "fair": (0.05, 0.15), "poor": (0, 0.05)},
            "return_on_equity": {"good": (0.15, 1), "fair": (0.08, 0.15), "poor": (0, 0.08)},
        }

    def run(self, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze financial data and return quantitative assessment.
        """
        # Filter for financial data
        financial_data = [c for c in context if c.get("metadata", {}).get("type") == "financials"]
        
        # Calculate data quality
        data_quality = self.calculate_data_quality(financial_data)
        
        # Prepare context for LLM
        context_str = "\n".join([str(item.get("content")) for item in financial_data])
        
        prompt = f"""
        You are the Quantitative Analysis Agent.

        ROLE:
        Evaluate the asset strictly using numerical and financial metrics. Provide a DEEP, DATA-DRIVEN analysis.

        METRICS TO ANALYZE:
        - Valuation: P/E, Forward P/E, PEG Ratio, Price-to-Book (Cite exact values)
        - Profitability: Profit Margins, Return on Equity (Compare to sector norms)
        - Health: Debt-to-Equity, Free Cash Flow (Assess solvency)
        - Size: Market Capitalization

        OUTPUT FORMAT (STRICT JSON):
        {{
            "score": <0-100>,
            "confidence": <0-100 based on data completeness>,
            "metrics_used": ["list of metrics with values, e.g., 'P/E (22.5)'"],
            "metrics_values": {{"metric": value}},
            "strengths": ["Detailed sentence explaining strength with data"],
            "weaknesses": ["Detailed sentence explaining weakness with data"],
            "reasoning": "COMPREHENSIVE JUSTIFICATION: Write 3-4 detailed paragraphs. Explain EXACTLY how the score was calculated. CITE EVERY NUMBER used. Compare metrics to benchmarks. Do not use generic phrases like 'good valuation' without proof."
        }}

        SCORING GUIDELINES:
        - 80-100: Exceptional fundamentals (e.g., PEG < 1, ROE > 20%)
        - 60-79: Solid but imperfect (e.g., fair valuation, stable growth)
        - 40-59: Mixed signals (e.g., cheap but low growth, or expensive but high growth)
        - 20-39: Fundamental flaws (e.g., declining margins, high debt)
        - 0-19: Distress signals

        RULES:
        1. NO GENERIC OUPUT. Bad: "Good P/E". Good: "P/E of 12.5 is 40% below sector average of 20, indicating undervaluation."
        2. JUSTIFY THE SCORE. If score is 60, explain why it's not 80 (what's missing?) and why it's not 40 (what's good?).
        3. CITE SOURCES/VALUES. Use the data provided in context.

        CONTEXT (Retrieved from RAG):
        {context_str if context_str else "No financial data available in context."}
        """
        
        # Call LLM with fallback
        response = self.call_llm(
            prompt=prompt,
            system_prompt="You are a strict Quantitative Analyst. Output valid JSON only. Justify every score with specific metrics.",
            fallback_func=self._rule_based_analysis,
            fallback_args=financial_data
        )
        
        # Parse response
        parsed = self._parse_response(response, financial_data)
        
        # Determine if fallback was used
        fallback_used = "[Fallback]" in response or "[Rule-Based]" in response
        
        # Adjust confidence based on data quality
        if data_quality == "Low":
            parsed["confidence"] = min(parsed["confidence"], 40)
        elif data_quality == "Medium":
            parsed["confidence"] = min(parsed["confidence"], 70)
        
        return self.format_output(
            output_data={
                "score": parsed["score"],
                "metrics_used": parsed.get("metrics_used", []),
                "metrics_values": parsed.get("metrics_values", {}),
                "strengths": parsed.get("strengths", []),
                "weaknesses": parsed.get("weaknesses", [])
            },
            confidence=parsed["confidence"],
            data_quality=data_quality,
            fallback_used=fallback_used,
            analysis=parsed.get("reasoning", response)
        )

    def _parse_response(self, response: str, financial_data: List[Dict]) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        """
        result = {
            "score": 50,
            "confidence": 50,
            "metrics_used": [],
            "metrics_values": {},
            "strengths": [],
            "weaknesses": [],
            "reasoning": response
        }
        
        # Try JSON parsing
        parsed_json = self.parse_json_from_response(response)
        if parsed_json:
            result.update(parsed_json)
            result["score"] = max(0, min(100, result.get("score", 50)))
            result["confidence"] = max(0, min(100, result.get("confidence", 50)))
            return result
        
        # Fallback to regex extraction
        result["score"] = self.extract_score(response, 50)
        result["confidence"] = self.extract_confidence(response, 50)
        
        # Extract reasoning
        import re
        reason_match = re.search(r'(?:Reason(?:ing)?|Explanation):\s*(.+?)(?:\n\n|$)', response, re.DOTALL | re.IGNORECASE)
        if reason_match:
            result["reasoning"] = reason_match.group(1).strip()
        
        return result

    def _rule_based_analysis(self, financial_data: List[Dict[str, Any]]) -> str:
        """
        Enhanced rule-based fallback analysis with multiple metrics.
        """
        score = 50
        confidence = 30  # Low confidence for rule-based
        metrics_used = []
        metrics_values = {}
        strengths = []
        weaknesses = []
        adjustments = []
        
        for item in financial_data:
            content = item.get("content", "")
            try:
                import ast
                data = content if isinstance(content, dict) else ast.literal_eval(str(content))
                
                # P/E Ratio Analysis
                pe = data.get("pe_ratio")
                if isinstance(pe, (int, float)) and pe > 0:
                    metrics_used.append("P/E Ratio")
                    metrics_values["pe_ratio"] = pe
                    if pe < 15:
                        score += 15
                        adjustments.append(f"P/E {pe:.1f} < 15: +15")
                        strengths.append(f"Attractive P/E ratio of {pe:.1f}")
                    elif pe > 30:
                        score -= 15
                        adjustments.append(f"P/E {pe:.1f} > 30: -15")
                        weaknesses.append(f"High P/E ratio of {pe:.1f} suggests overvaluation")
                    else:
                        score += 5
                        adjustments.append(f"P/E {pe:.1f} is fair: +5")
                
                # Forward P/E Analysis
                fpe = data.get("forward_pe")
                if isinstance(fpe, (int, float)) and fpe > 0:
                    metrics_used.append("Forward P/E")
                    metrics_values["forward_pe"] = fpe
                    if fpe < 20:
                        score += 10
                        adjustments.append(f"Fwd P/E {fpe:.1f} < 20: +10")
                        strengths.append(f"Forward P/E of {fpe:.1f} indicates growth at reasonable price")
                    elif fpe > 35:
                        score -= 10
                        adjustments.append(f"Fwd P/E {fpe:.1f} > 35: -10")
                        weaknesses.append(f"High forward P/E of {fpe:.1f}")
                
                # PEG Ratio Analysis
                peg = data.get("peg_ratio")
                if isinstance(peg, (int, float)) and peg > 0:
                    metrics_used.append("PEG Ratio")
                    metrics_values["peg_ratio"] = peg
                    if peg < 1:
                        score += 12
                        adjustments.append(f"PEG {peg:.2f} < 1: +12")
                        strengths.append(f"PEG ratio of {peg:.2f} suggests undervaluation relative to growth")
                    elif peg > 2:
                        score -= 8
                        adjustments.append(f"PEG {peg:.2f} > 2: -8")
                        weaknesses.append(f"PEG ratio of {peg:.2f} is elevated")
                
                # Profit Margins Analysis
                margins = data.get("profit_margins")
                if isinstance(margins, (int, float)):
                    metrics_used.append("Profit Margins")
                    metrics_values["profit_margins"] = margins
                    if margins > 0.15:
                        score += 10
                        adjustments.append(f"Margins {margins:.1%} > 15%: +10")
                        strengths.append(f"Strong profit margins of {margins:.1%}")
                    elif margins < 0.05:
                        score -= 10
                        adjustments.append(f"Margins {margins:.1%} < 5%: -10")
                        weaknesses.append(f"Low profit margins of {margins:.1%}")
                
                # Return on Equity Analysis
                roe = data.get("return_on_equity")
                if isinstance(roe, (int, float)):
                    metrics_used.append("Return on Equity")
                    metrics_values["return_on_equity"] = roe
                    if roe > 0.15:
                        score += 10
                        adjustments.append(f"ROE {roe:.1%} > 15%: +10")
                        strengths.append(f"Excellent ROE of {roe:.1%}")
                    elif roe < 0.08:
                        score -= 8
                        adjustments.append(f"ROE {roe:.1%} < 8%: -8")
                        weaknesses.append(f"Low ROE of {roe:.1%}")
                
                # Debt-to-Equity Analysis
                dte = data.get("debt_to_equity")
                if isinstance(dte, (int, float)):
                    metrics_used.append("Debt-to-Equity")
                    metrics_values["debt_to_equity"] = dte
                    if dte < 50:
                        score += 8
                        adjustments.append(f"D/E {dte:.1f} < 50: +8")
                        strengths.append(f"Conservative leverage with D/E of {dte:.1f}")
                    elif dte > 100:
                        score -= 10
                        adjustments.append(f"D/E {dte:.1f} > 100: -10")
                        weaknesses.append(f"High leverage with D/E of {dte:.1f}")
                
                # Market Cap Analysis
                mc = str(data.get("market_cap", ""))
                if mc:
                    metrics_used.append("Market Cap")
                    metrics_values["market_cap"] = mc
                    if "T" in mc:
                        score += 8
                        adjustments.append(f"Market Cap {mc} (Mega-cap): +8")
                        strengths.append(f"Mega-cap stability with market cap of {mc}")
                    elif "B" in mc:
                        try:
                            val = float(mc.replace("B", "").replace(",", ""))
                            if val > 50:
                                score += 5
                                adjustments.append(f"Market Cap {mc} (Large-cap): +5")
                        except:
                            pass
                
                # Increase confidence based on metrics found
                confidence = min(70, 30 + len(metrics_used) * 8)
                
            except Exception as e:
                continue
        
        # Clamp score
        score = max(0, min(100, score))
        
        # Build response
        if not metrics_used:
            return f"""[Rule-Based Fallback] No financial metrics found in RAG context.
Score: 50
Confidence: 20
Reasoning: Unable to perform quantitative analysis due to missing financial data. Defaulting to neutral score."""
        
        result = {
            "score": score,
            "confidence": confidence,
            "metrics_used": list(set(metrics_used)),
            "metrics_values": metrics_values,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "reasoning": f"[Rule-Based Fallback] Applied quantitative rules. Adjustments: {'; '.join(adjustments)}"
        }
        
        import json
        return f"[Rule-Based Analysis]\n```json\n{json.dumps(result, indent=2)}\n```"


quant_agent = QuantAgent()
