"""
Match Score Service
Calculates how well an asset matches the investor's DNA profile.
"""
from typing import Dict, Any, List, Optional
from app.models.investor_dna import (
    InvestorDNA, 
    MatchScoreBreakdown, 
    MatchResult,
    RiskTolerance,
    InvestmentStyle,
    HoldingPeriod,
    DEFAULT_INVESTOR_DNA
)


class MatchScoreService:
    """
    Service to calculate Match Score between an asset and investor DNA.
    """
    
    def __init__(self):
        self.excluded_sector_keywords = {
            "tobacco": ["Tobacco", "Cigarettes"],
            "alcohol": ["Alcoholic Beverages", "Brewers", "Distillers", "Wineries"],
            "gambling": ["Casinos", "Gaming", "Gambling"],
            "weapons": ["Aerospace & Defense", "Weapons", "Ammunition"],
            "fossil_fuels": ["Oil & Gas", "Coal", "Petroleum"]
        }
    
    def calculate_match_score(
        self,
        agent_results: Dict[str, Any],
        asset_data: Dict[str, Any],
        investor_dna: Optional[InvestorDNA] = None
    ) -> MatchResult:
        """
        Calculate comprehensive match score.
        
        Args:
            agent_results: Results from all agents (quant, macro, philosopher, regret)
            asset_data: Raw asset data from scout (financials, technicals)
            investor_dna: User's investor profile (uses default if None)
        
        Returns:
            MatchResult with score breakdown and recommendations
        """
        if investor_dna is None:
            investor_dna = DEFAULT_INVESTOR_DNA
        
        # Extract data
        financials = asset_data.get("financials", {})
        technicals = asset_data.get("technicals", {})
        
        # Calculate component scores
        fundamental_score = self._get_fundamental_score(agent_results.get("quant", {}))
        macro_score = self._get_macro_score(agent_results.get("macro", {}))
        philosophy_score = self._get_philosophy_score(agent_results.get("philosopher", {}))
        risk_score = self._get_risk_score(agent_results.get("regret", {}))
        dna_match_score = self._calculate_dna_match(financials, technicals, investor_dna)
        
        # Check for ethical violations
        ethical_violation = self._check_ethical_filters(financials, investor_dna)
        if ethical_violation:
            dna_match_score = max(0, dna_match_score - 50)  # Heavy penalty
        
        # Create breakdown
        breakdown = MatchScoreBreakdown(
            fundamental_score=fundamental_score,
            macro_score=macro_score,
            philosophy_score=philosophy_score,
            risk_score=risk_score,
            dna_match_score=dna_match_score
        )
        
        total_score = int(breakdown.total_score)
        
        # Generate recommendations
        fit_reasons, concern_reasons = self._generate_reasons(
            agent_results, financials, technicals, investor_dna, ethical_violation
        )
        
        recommendation, action_owned, action_not_owned = self._get_recommendations(
            total_score, ethical_violation, investor_dna
        )
        
        # Generate summary
        summary = self._generate_summary(
            total_score, recommendation, fit_reasons, concern_reasons, investor_dna
        )
        
        return MatchResult(
            asset_id=financials.get("symbol", "Unknown"),
            match_score=total_score,
            breakdown=breakdown,
            recommendation=recommendation,
            action_if_owned=action_owned,
            action_if_not_owned=action_not_owned,
            fit_reasons=fit_reasons[:5],
            concern_reasons=concern_reasons[:5],
            summary=summary
        )
    
    def _get_fundamental_score(self, quant_result: Dict) -> float:
        """Extract fundamental score from Quant Agent."""
        # Handle new structured format
        if "output" in quant_result:
            return float(quant_result.get("output", {}).get("score", 50))
        return float(quant_result.get("score", 50))
    
    def _get_macro_score(self, macro_result: Dict) -> float:
        """Convert macro trend to score."""
        if "output" in macro_result:
            trend = macro_result.get("output", {}).get("trend", "Neutral")
        else:
            trend = macro_result.get("trend", "Neutral")
        
        trend_scores = {
            "Bullish": 80,
            "Neutral": 50,
            "Bearish": 25,
            "Indeterminate": 40
        }
        return trend_scores.get(trend, 50)
    
    def _get_philosophy_score(self, phil_result: Dict) -> float:
        """Convert philosophy alignment to score."""
        if "output" in phil_result:
            alignment = phil_result.get("output", {}).get("alignment", "Medium")
        else:
            alignment = phil_result.get("alignment_score", "Medium")
        
        alignment_scores = {
            "High": 85,
            "Medium": 55,
            "Low": 25
        }
        return alignment_scores.get(alignment, 55)
    
    def _get_risk_score(self, regret_result: Dict) -> float:
        """Convert risk level to inverted score (lower risk = higher score)."""
        if "output" in regret_result:
            risk_level = regret_result.get("output", {}).get("risk_level", "Medium")
        else:
            risk_level = regret_result.get("risk_level", "Medium")
        
        # Inverted: low risk = high score
        risk_scores = {
            "Low": 85,
            "Medium": 55,
            "High": 25
        }
        return risk_scores.get(risk_level, 55)
    
    def _calculate_dna_match(
        self,
        financials: Dict,
        technicals: Dict,
        dna: InvestorDNA
    ) -> float:
        """Calculate how well asset matches investor DNA."""
        score = 70  # Start with baseline
        
        # Check P/E against preference
        pe = financials.get("pe_ratio")
        if pe and dna.max_pe_ratio:
            if pe <= dna.max_pe_ratio:
                score += 10
            else:
                score -= 15
        
        # Check dividend yield
        div_yield = financials.get("dividend_yield", 0)
        if dna.min_dividend_yield and div_yield:
            if div_yield >= dna.min_dividend_yield:
                score += 10
            else:
                score -= 5
        
        # Check profitability preference
        margins = financials.get("profit_margins")
        if dna.prefer_profitable and margins:
            if margins > 0:
                score += 10
            else:
                score -= 15
        
        # Check market cap preference
        market_cap = str(financials.get("market_cap", ""))
        if dna.min_market_cap:
            if "T" in market_cap:
                score += 10  # Trillion = large cap
            elif "B" in market_cap:
                try:
                    cap_val = float(market_cap.replace("B", "").replace(",", ""))
                    min_val = float(dna.min_market_cap.replace("B", "").replace(",", ""))
                    if cap_val >= min_val:
                        score += 5
                except:
                    pass
        
        # Check 52-week high preference
        if dna.avoid_52w_highs:
            pct_from_high = technicals.get("pct_from_52w_high", 0)
            if pct_from_high and pct_from_high < -5:
                score += 10  # Not at high
            elif pct_from_high and pct_from_high >= -2:
                score -= 10  # Near high
        
        # Check oversold preference
        if dna.prefer_oversold:
            rsi = technicals.get("rsi_14", 50)
            if rsi and rsi < 30:
                score += 15  # Oversold
            elif rsi and rsi > 70:
                score -= 10  # Overbought
        
        # Check risk tolerance alignment
        volatility = technicals.get("volatility_raw", 0.2)
        if volatility:
            if dna.risk_tolerance == RiskTolerance.CONSERVATIVE:
                if volatility > 0.25:
                    score -= 20  # Too volatile
                else:
                    score += 10
            elif dna.risk_tolerance == RiskTolerance.AGGRESSIVE:
                if volatility > 0.30:
                    score += 5  # Aggressive likes volatility
        
        # Investment style alignment
        roe = financials.get("return_on_equity", 0)
        revenue_growth = financials.get("revenue_growth", 0)
        
        if dna.investment_style == InvestmentStyle.VALUE:
            if pe and pe < 15:
                score += 10
        elif dna.investment_style == InvestmentStyle.GROWTH:
            if revenue_growth and revenue_growth > 0.15:
                score += 10
        elif dna.investment_style == InvestmentStyle.DIVIDEND:
            if div_yield and div_yield > 2:
                score += 15
        
        return max(0, min(100, score))
    
    def _check_ethical_filters(self, financials: Dict, dna: InvestorDNA) -> Optional[str]:
        """Check if asset violates any ethical filters."""
        sector = financials.get("sector", "").lower()
        industry = financials.get("industry", "").lower()
        combined = f"{sector} {industry}"
        
        if dna.exclude_tobacco:
            if "tobacco" in combined or "cigarette" in combined:
                return "Tobacco company excluded by your ethical preferences"
        
        if dna.exclude_alcohol:
            if any(x in combined for x in ["alcohol", "beer", "wine", "spirits", "distill"]):
                return "Alcohol company excluded by your ethical preferences"
        
        if dna.exclude_gambling:
            if any(x in combined for x in ["casino", "gambling", "betting"]):
                return "Gambling company excluded by your ethical preferences"
        
        if dna.exclude_weapons:
            if any(x in combined for x in ["weapon", "defense", "ammunition"]):
                return "Weapons company excluded by your ethical preferences"
        
        if dna.exclude_fossil_fuels:
            if any(x in combined for x in ["oil", "gas", "coal", "petroleum"]):
                return "Fossil fuel company excluded by your ethical preferences"
        
        return None
    
    def _generate_reasons(
        self,
        agent_results: Dict,
        financials: Dict,
        technicals: Dict,
        dna: InvestorDNA,
        ethical_violation: Optional[str]
    ) -> tuple:
        """Generate fit and concern reasons."""
        fit_reasons = []
        concern_reasons = []
        
        if ethical_violation:
            concern_reasons.append(ethical_violation)
        
        # From Quant
        quant = agent_results.get("quant", {})
        quant_score = self._get_fundamental_score(quant)
        if quant_score >= 70:
            fit_reasons.append("Strong fundamental metrics")
        elif quant_score < 40:
            concern_reasons.append("Weak fundamental metrics")
        
        # From Macro
        macro = agent_results.get("macro", {})
        macro_trend = macro.get("output", {}).get("trend") or macro.get("trend", "Neutral")
        if macro_trend == "Bullish":
            fit_reasons.append("Favorable macro environment")
        elif macro_trend == "Bearish":
            concern_reasons.append("Challenging macro environment")
        
        # From risk
        regret = agent_results.get("regret", {})
        risk_level = regret.get("output", {}).get("risk_level") or regret.get("risk_level", "Medium")
        if risk_level == "Low":
            fit_reasons.append("Low downside risk identified")
        elif risk_level == "High":
            concern_reasons.append("High downside risk scenarios identified")
        
        # Valuation
        pe = financials.get("pe_ratio")
        if pe:
            if pe < 15:
                fit_reasons.append(f"Attractive valuation (P/E: {pe:.1f})")
            elif pe > 35:
                concern_reasons.append(f"High valuation (P/E: {pe:.1f})")
        
        # Technical position
        rsi = technicals.get("rsi_14")
        if rsi:
            if rsi < 30:
                fit_reasons.append(f"Technically oversold (RSI: {rsi:.0f})")
            elif rsi > 70:
                concern_reasons.append(f"Technically overbought (RSI: {rsi:.0f})")
        
        # Trend
        trend = technicals.get("trend_signal", "")
        if "Uptrend" in trend or "Bullish" in trend:
            fit_reasons.append("Positive price trend")
        elif "Downtrend" in trend or "Bearish" in trend:
            concern_reasons.append("Negative price trend")
        
        # Profitability
        margins = financials.get("profit_margins")
        if margins:
            if margins > 0.2:
                fit_reasons.append(f"High profit margins ({margins:.1%})")
            elif margins < 0.05:
                concern_reasons.append(f"Low profit margins ({margins:.1%})")
        
        return fit_reasons, concern_reasons
    
    def _get_recommendations(
        self,
        score: int,
        ethical_violation: Optional[str],
        dna: InvestorDNA
    ) -> tuple:
        """Get action recommendations based on score."""
        
        # Ethical violation = automatic avoid
        if ethical_violation:
            return ("Avoid", "Exit", "Avoid")
        
        # Based on score and risk tolerance
        if dna.risk_tolerance == RiskTolerance.CONSERVATIVE:
            if score >= 75:
                return ("Buy", "Hold", "Buy")
            elif score >= 60:
                return ("Hold", "Hold", "Wait")
            else:
                return ("Avoid", "Reduce", "Avoid")
        
        elif dna.risk_tolerance == RiskTolerance.MODERATE:
            if score >= 70:
                return ("Buy", "Hold", "Buy")
            elif score >= 50:
                return ("Hold", "Hold", "Wait")
            elif score >= 35:
                return ("Don't Add", "Hold", "Don't Add")
            else:
                return ("Avoid", "Reduce", "Avoid")
        
        else:  # AGGRESSIVE
            if score >= 65:
                return ("Buy", "Add More", "Buy")
            elif score >= 45:
                return ("Hold", "Hold", "Consider")
            else:
                return ("Don't Add", "Hold", "Don't Add")
    
    def _generate_summary(
        self,
        score: int,
        recommendation: str,
        fit_reasons: List[str],
        concern_reasons: List[str],
        dna: InvestorDNA
    ) -> str:
        """Generate human-readable summary."""
        
        if score >= 75:
            opening = f"This asset is a strong match ({score}%) for your {dna.investment_style.value} investment style."
        elif score >= 60:
            opening = f"This asset is a decent match ({score}%) but has some considerations."
        elif score >= 45:
            opening = f"This asset has a moderate match ({score}%) with mixed signals."
        else:
            opening = f"This asset has a low match ({score}%) for your investment profile."
        
        # Add key point
        if fit_reasons:
            opening += f" Key strength: {fit_reasons[0].lower()}."
        
        if concern_reasons:
            opening += f" Key concern: {concern_reasons[0].lower()}."
        
        # Recommendation
        if recommendation == "Buy":
            opening += " Consider adding to your portfolio."
        elif recommendation == "Hold":
            opening += " Hold if you own it; don't add now."
        elif recommendation == "Don't Add":
            opening += " Don't add now; wait for better entry."
        elif recommendation == "Avoid":
            opening += " This doesn't align with your preferences."
        
        return opening


# Singleton instance
match_score_service = MatchScoreService()
