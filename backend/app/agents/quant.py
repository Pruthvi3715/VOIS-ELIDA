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
        You are the Quantitative Analysis Agent - the most rigorous numbers analyst in the financial industry.

        CRITICAL ROLE:
        You MUST provide DEEP, DATA-DRIVEN analysis with EXPLICIT CITATIONS for every claim.

        MANDATORY ANALYSIS STRUCTURE:
        For EACH metric, you MUST include:
        1. The EXACT numerical value from the context
        2. Comparison to industry benchmarks or historical norms
        3. Percentage deviation from benchmarks
        4. Impact on final score (+X points or -X points)

        METRICS TO ANALYZE (cite exact values):
        - Valuation: P/E Ratio, Forward P/E, PEG Ratio, Price-to-Book
        - Profitability: Profit Margins, Return on Equity, Return on Assets
        - Financial Health: Debt-to-Equity, Current Ratio, Free Cash Flow
        - Growth: Revenue Growth, Earnings Growth
        - Market Position: Market Capitalization, Sector, Industry

        OUTPUT FORMAT (STRICT JSON):
        {{
            "score": <0-100>,
            "confidence": <0-100 based on data completeness>,
            "metrics_used": ["Format: 'P/E: 23.5', 'ROE: 18.2%', 'Debt/Equity: 45.3'"],
            "metrics_values": {{"pe_ratio": 23.5, "roe": 0.182, "debt_to_equity": 45.3}},
            "strengths": [
                "MUST cite specific numbers. Example: 'ROE of 22.5% exceeds industry average of 15%, indicating superior capital efficiency and placing the company in the top quartile of its sector.'"
            ],
            "weaknesses": [
                "MUST cite specific numbers. Example: 'P/E ratio of 32.1 is 45% above the sector median of 22.0, suggesting potential overvaluation unless justified by exceptional growth prospects.'"
            ],
            "reasoning": '''
            WRITE 4-5 DETAILED PARAGRAPHS with this EXACT structure:
            
            Paragraph 1 - Valuation Assessment:
            - State each valuation metric with exact value
            - Compare to benchmarks (e.g., "P/E of X vs sector average of Y")
            - Calculate percentage premium/discount
            - Explain what this means for the stock
            
            Paragraph 2 - Profitability & Efficiency:
            - Cite profit margins, ROE, ROA with exact percentages
            - Compare to industry standards
            - Assess trends (improving/declining)
            - Explain competitive advantages or disadvantages
            
            Paragraph 3 - Financial Health:
            - State Debt-to-Equity ratio
            - Analyze leverage relative to industry norms
            - Assess free cash flow and liquidity
            - Discuss solvency risks or strengths
            
            Paragraph 4 - Growth & Market Position:
            - Cite revenue and earnings growth rates
            - Compare to historical averages and peer growth
            - Analyze market cap and competitive position
            - Assess scalability and market opportunities
            
            Paragraph 5 - Score Justification:
            - Explain EXACTLY why the score is X and not X+20 or X-20
            - List each factor contributing to score
            - Provide weighted breakdown (e.g., "Valuation contributes -10 points due to elevated P/E, while profitability adds +25 points due to exceptional margins")
            '''
        }}

        STRICT SCORING GUIDELINES:
        - 85-100: Exceptional fundamentals across ALL metrics (e.g., PEG<1.0, ROE>20%, D/E<30, Margins>15%)
        - 70-84: Strong fundamentals with 1-2 minor weaknesses
        - 55-69: Above average, but notable concerns (e.g., high valuation or moderate debt)
        - 40-54: Mixed signals - some good metrics offset by significant concerns
        - 25-39: More weaknesses than strengths - fundamental issues present
        - 0-24: Distress or severe fundamental deterioration

        ABSOLUTE REQUIREMENTS:
        ❌ FORBIDDEN: "Good P/E", "Strong fundamentals", "Attractive valuation" WITHOUT NUMBERS
        ✅ REQUIRED: "P/E of 12.5 is 40% below sector average of 20.8, indicating undervaluation"
        
        ❌ FORBIDDEN: "The company is profitable"
        ✅ REQUIRED: "Net profit margin of 18.2% exceeds the sector median of 12.5%, ranking in the 75th percentile"
        
        If ANY metric is missing from context, explicitly state "[Metric X] not available" and reduce confidence by 10 points per missing critical metric.

        CONTEXT (Retrieved from RAG):
        {context_str if context_str else "CRITICAL ERROR: No financial data available. Cannot perform quantitative analysis. Return score:0, confidence:0, reasoning:'No financial data provided in context.'"}
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
        
        # Build detailed reasoning
        reasoning_paragraphs = []
        
        # Para 1: Valuation
        if any(k in metrics_values for k in ["pe_ratio", "forward_pe", "peg_ratio"]):
            valuation_text = "**Valuation Analysis:** "
            if "pe_ratio" in metrics_values:
                pe = metrics_values["pe_ratio"]
                valuation_text += f"The current P/E ratio of {pe:.2f} "
                if pe < 15:
                    valuation_text += f"is below my threshold of 15, suggesting the stock trades at {((15-pe)/15*100):.1f}% discount to fair value based on earnings. "
                elif pe > 30:
                    valuation_text += f"exceeds reasonable levels (>30), indicating a {((pe-30)/30*100):.1f}% premium that may not be justified without exceptional growth. "
                else:
                    valuation_text += "falls within the fair range of 15-30, indicating market pricing is reasonable relative to earnings. "
            reasoning_paragraphs.append(valuation_text)
        
        # Para 2: Profitability
        if any(k in metrics_values for k in ["profit_margins", "return_on_equity"]):
            profit_text = "**Profitability Assessment:** "
            if "profit_margins" in metrics_values:
                margin = metrics_values["profit_margins"]
                profit_text += f"Net profit margin of {margin:.1%} "
                if margin > 0.15:
                    profit_text += f"significantly exceeds the 15% benchmark for quality companies, demonstrating pricing power and operational efficiency. "
                elif margin < 0.05:
                    profit_text += f"falls below the minimum 5% threshold for sustainable businesses, raising concerns about competitive positioning. "
            reasoning_paragraphs.append(profit_text)
        
        # Para 3: Score justification
        score_justification = f"**Final Score Rationale:** Starting from a baseline of 50, I applied the following adjustments: {'; '.join(adjustments)}. "
        score_justification += f"This yields a final quantitative score of {score}/100. "
        if weaknesses:
            score_justification += f"Key concerns preventing a higher score include: {', '.join(weaknesses[:2])}. "
        if strengths:
            score_justification += f"Primary strengths supporting this score are: {', '.join(strengths[:2])}. "
        reasoning_paragraphs.append(score_justification)
        
        detailed_reasoning = " ".join(reasoning_paragraphs)
        
        # Build response
        if not metrics_used:
            return f"""[Rule-Based Fallback] No financial metrics found in RAG context.
Score: 30
Confidence: 10
Reasoning: Unable to perform quantitative analysis due to complete absence of financial data in provided context. This represents a critical data gap. Without fundamental metrics like P/E ratio, profit margins, or debt levels, I cannot assess the investment quality. Reduced score to 30 to reflect information insufficiency risk."""
        
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
