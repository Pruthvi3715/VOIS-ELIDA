from typing import Any, Dict, List
from app.agents.base import BaseAgent


class PhilosopherAgent(BaseAgent):
    """
    Philosophical and Long-Term Alignment Agent - Evaluates ethical and sustainable investment alignment.
    Enhanced with ESG factors, sector ethics, and structured output.
    """
    
    def __init__(self):
        super().__init__(name="Philosopher Agent")
        
        # Sector default ethical ratings
        self.sector_ethics = {
            "Technology": {"base": "Medium", "factors": ["Data Privacy", "AI Ethics", "Digital Divide"]},
            "Healthcare": {"base": "High", "factors": ["Access to Medicine", "Drug Pricing", "Patient Care"]},
            "Financial Services": {"base": "Medium", "factors": ["Financial Inclusion", "Predatory Lending", "Transparency"]},
            "Consumer": {"base": "Medium", "factors": ["Labor Practices", "Product Safety", "Marketing Ethics"]},
            "Energy": {"base": "Low", "factors": ["Carbon Footprint", "Transition Plans", "Community Impact"]},
            "Industrials": {"base": "Medium", "factors": ["Worker Safety", "Environmental Impact", "Supply Chain"]},
            "Utilities": {"base": "Medium", "factors": ["Clean Energy Mix", "Affordability", "Infrastructure"]},
            "Materials": {"base": "Low", "factors": ["Mining Practices", "Waste Management", "Biodiversity"]},
            "Real Estate": {"base": "Medium", "factors": ["Affordable Housing", "Urban Development", "Sustainability"]},
        }

    def run(self, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze long-term alignment with ethical and sustainable principles.
        """
        # Calculate data quality
        data_quality = self.calculate_data_quality(context)
        
        context_str = "\n".join([str(c.get("content")) for c in context])
        
        prompt = f"""
        You are the Philosophical and Long-Term Alignment Agent.

        ROLE:
        Evaluate the investment's alignment with sustainable wealth creation and ethical principles. Move beyond generic ESG labels.

        FACTORS:
        - Moat Sustainability: Is the business model durable for 10+ years?
        - Governance: Alignment of incentives (Management ownership vs compensation).
        - Social License: Does society *want* this company to exist?
        - Negative Externalities: Pollution, addiction, etc.

        OUTPUT FORMAT (STRICT JSON):
        {{
            "alignment": "<Low|Medium|High>",
            "confidence": <0-100>,
            "factors_analyzed": [
                {{"factor": "name", "assessment": "positive/neutral/negative", "reasoning": "Specific detail"}}
            ],
            "ethical_strengths": ["Specific positive attribute"],
            "ethical_concerns": ["Specific negative attribute (e.g., 'pending lawsuit regarding X')"],
            "long_term_outlook": "10-year view assessment",
            "reasoning": "PHILOSOPHICAL TREATISE: Write 2-3 paragraphs. Discuss the tension between profit and principle for this specific asset. Is it a 'Compounder' or a 'Cigar Butt'? Justify the alignment score."
        }}

        RULES:
        1. BE NUANCED. Few companies are "Pure Good" or "Pure Evil". Explore the grey areas.
        2. FOCUS ON DURABILITY. Ethics often correlates with longevity.
        3. CITE EVIDENCE. "Governance is weak because X..."

        CONTEXT (Retrieved from RAG):
        {context_str if context_str else "No company data available in context."}
        """
        
        response = self.call_llm(
            prompt=prompt,
            system_prompt="You are a Philosopher analyzing investments for ethical alignment. Output valid JSON. Be thoughtful and balanced.",
            fallback_func=self._sector_based_analysis,
            fallback_args=context
        )
        
        # Parse response
        parsed = self._parse_response(response)
        
        # Determine if fallback was used
        fallback_used = "[Fallback]" in response or "[Sector-Based]" in response
        
        return self.format_output(
            output_data={
                "alignment": parsed["alignment"],
                "factors_analyzed": parsed.get("factors_analyzed", []),
                "ethical_strengths": parsed.get("ethical_strengths", []),
                "ethical_concerns": parsed.get("ethical_concerns", []),
                "long_term_outlook": parsed.get("long_term_outlook", "Unknown")
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
            "alignment": "Medium",
            "confidence": 50,
            "factors_analyzed": [],
            "ethical_strengths": [],
            "ethical_concerns": [],
            "long_term_outlook": "Unknown",
            "reasoning": response
        }
        
        # Try JSON parsing
        parsed_json = self.parse_json_from_response(response)
        if parsed_json:
            result.update(parsed_json)
            # Validate alignment
            valid_alignments = ["Low", "Medium", "High"]
            if result["alignment"] not in valid_alignments:
                result["alignment"] = self.extract_level(result["alignment"], valid_alignments, "Medium")
            result["confidence"] = max(0, min(100, result.get("confidence", 50)))
            return result
        
        # Fallback extraction
        result["alignment"] = self.extract_level(response, ["Low", "Medium", "High"], "Medium")
        result["confidence"] = self.extract_confidence(response, 50)
        
        return result

    def _sector_based_analysis(self, context: List[Dict[str, Any]]) -> str:
        """
        Sector-based fallback analysis when LLM unavailable.
        """
        sector = None
        company_summary = ""
        symbol = "Unknown"
        
        # Extract sector and summary from context
        for item in context:
            content = item.get("content", "")
            try:
                import ast
                data = content if isinstance(content, dict) else ast.literal_eval(str(content))
                
                if isinstance(data, dict):
                    if "sector" in data:
                        sector = data.get("sector")
                    if "summary" in data:
                        company_summary = data.get("summary", "")[:300]
                    if "symbol" in data:
                        symbol = data.get("symbol")
            except:
                # Check if it's a raw string with sector info
                if isinstance(content, str):
                    for s in self.sector_ethics.keys():
                        if s.lower() in content.lower():
                            sector = s
                            break
        
        # Get sector defaults or use generic
        if sector and sector in self.sector_ethics:
            ethics = self.sector_ethics[sector]
            base_alignment = ethics["base"]
            key_factors = ethics["factors"]
        else:
            base_alignment = "Medium"
            key_factors = ["Business Model", "Governance", "Stakeholder Impact"]
            sector = sector or "Unknown"
        
        # Build factors analyzed
        factors_analyzed = [
            {"factor": f, "assessment": "neutral", "reasoning": f"Insufficient data for detailed {f} assessment"} 
            for f in key_factors[:3]
        ]
        
        result = {
            "alignment": base_alignment,
            "confidence": 35,
            "factors_analyzed": factors_analyzed,
            "ethical_strengths": [f"Operates in {sector} sector"],
            "ethical_concerns": ["Limited ethical data available for comprehensive analysis"],
            "long_term_outlook": f"Sector-typical risks and opportunities apply to {sector}",
            "reasoning": f"[Sector-Based Fallback] Limited ethical data for {symbol}. Applied sector defaults for {sector}. Key considerations: {', '.join(key_factors)}. Recommend gathering ESG data for more accurate assessment."
        }
        
        import json
        return f"[Sector-Based Analysis]\n```json\n{json.dumps(result, indent=2)}\n```"


philosopher_agent = PhilosopherAgent()
