"""
Financial Data Sanity Check Service
Detects and flags impossible or suspicious financial metrics.
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SanityAlert:
    """Represents a sanity check failure."""
    field: str
    reported_value: Any
    expected_range: str
    severity: str  # "WARNING", "ERROR", "CRITICAL"
    message: str
    suggested_action: str


class SanityChecker:
    """
    Validates financial metrics against known reasonable ranges.
    Flags hallucinations and data errors before they reach agents.
    """
    
    # Known blue-chip companies that are typically debt-free or low-debt
    KNOWN_LOW_DEBT_COMPANIES = {
        "TCS", "INFY", "WIPRO", "HCLTECH",  # Indian IT
        "GOOGL", "GOOG", "META", "AAPL",     # US Tech
        "MSFT", "NVDA", "ADBE",              # US Tech
    }
    
    # Sector-specific D/E expectations
    SECTOR_DE_EXPECTATIONS = {
        "Technology": (0, 1.0),
        "Information Technology": (0, 1.0),
        "Information Technology Services": (0, 0.5),
        "Software": (0, 0.5),
        "Consumer Defensive": (0, 2.0),
        "Financial Services": (0, 15.0),  # Banks have high leverage
        "Banking": (5, 20.0),
        "Real Estate": (1, 5.0),
        "Utilities": (1, 3.0),
    }
    
    # Market cap thresholds for sanity checks
    LARGE_CAP_THRESHOLD = 1e12  # 1 Trillion (in local currency)
    
    def __init__(self):
        self.alerts: List[SanityAlert] = []
    
    def check_financials(
        self, 
        financials: Dict[str, Any],
        asset_id: str
    ) -> Tuple[Dict[str, Any], List[SanityAlert]]:
        """
        Run sanity checks on financial data.
        Returns corrected financials and list of alerts.
        """
        self.alerts = []
        corrected = financials.copy()
        
        symbol = asset_id.split(".")[0].upper()
        sector = financials.get("sector", "")
        industry = financials.get("industry", "")
        market_cap_str = str(financials.get("market_cap", ""))
        
        # Parse market cap
        market_cap = self._parse_market_cap(market_cap_str)
        is_large_cap = market_cap and market_cap >= self.LARGE_CAP_THRESHOLD
        
        # 1. Check Debt-to-Equity Ratio
        de_ratio = financials.get("debt_to_equity")
        if de_ratio is not None:
            corrected_de = self._check_debt_to_equity(
                de_ratio, symbol, sector, industry, is_large_cap
            )
            if corrected_de != de_ratio:
                corrected["debt_to_equity"] = corrected_de
                corrected["debt_to_equity_original"] = de_ratio
                corrected["debt_to_equity_corrected"] = True
        
        # 2. Check P/E Ratio
        pe_ratio = financials.get("pe_ratio")
        if pe_ratio is not None:
            self._check_pe_ratio(pe_ratio, sector)
        
        # 3. Check Profit Margins
        margins = financials.get("profit_margins")
        if margins is not None:
            self._check_profit_margins(margins, sector)
        
        # 4. Check ROE
        roe = financials.get("return_on_equity")
        if roe is not None:
            self._check_roe(roe)
        
        # 5. Cross-validation: High D/E + High Margins = Suspicious for IT
        if de_ratio and de_ratio > 5 and margins and margins > 0.15:
            if "technology" in sector.lower() or "software" in industry.lower():
                self.alerts.append(SanityAlert(
                    field="cross_validation",
                    reported_value=f"D/E={de_ratio}, Margins={margins:.1%}",
                    expected_range="IT companies rarely have high D/E with high margins",
                    severity="CRITICAL",
                    message="Data conflict: High-margin IT company with extreme leverage is unusual",
                    suggested_action="Verify D/E ratio from multiple sources"
                ))
        
        # Add sanity check results to financials
        corrected["_sanity_alerts"] = [
            {
                "field": a.field,
                "severity": a.severity,
                "message": a.message,
                "action": a.suggested_action
            } for a in self.alerts
        ]
        corrected["_sanity_checked"] = True
        
        return corrected, self.alerts
    
    def _check_debt_to_equity(
        self,
        de_ratio: float,
        symbol: str,
        sector: str,
        industry: str,
        is_large_cap: bool
    ) -> float:
        """
        Validate and potentially correct D/E ratio.
        """
        # Check if this is a known low-debt company
        if symbol in self.KNOWN_LOW_DEBT_COMPANIES and de_ratio > 2:
            self.alerts.append(SanityAlert(
                field="debt_to_equity",
                reported_value=de_ratio,
                expected_range="0.0 - 0.5 (known low-debt company)",
                severity="CRITICAL",
                message=f"{symbol} is known to be a low-debt company but shows D/E of {de_ratio}",
                suggested_action="D/E likely misread as percentage. Dividing by 100."
            ))
            # Common error: percentage shown as decimal (10.17% read as 10.17)
            if de_ratio > 1:
                return de_ratio / 100
        
        # Check sector expectations
        expected = self.SECTOR_DE_EXPECTATIONS.get(sector) or self.SECTOR_DE_EXPECTATIONS.get(industry)
        if expected:
            min_de, max_de = expected
            if de_ratio > max_de * 2:  # More than 2x the expected max
                self.alerts.append(SanityAlert(
                    field="debt_to_equity",
                    reported_value=de_ratio,
                    expected_range=f"{min_de} - {max_de} for {sector}",
                    severity="ERROR",
                    message=f"D/E ratio {de_ratio} is unusually high for {sector} sector",
                    suggested_action="Verify from company filings"
                ))
                # Attempt correction if it looks like a percentage error
                if de_ratio > 5 and de_ratio < 100:
                    return de_ratio / 100
        
        # Large-cap non-financial companies rarely have D/E > 5
        if is_large_cap and de_ratio > 5:
            if "financial" not in sector.lower() and "bank" not in industry.lower():
                self.alerts.append(SanityAlert(
                    field="debt_to_equity",
                    reported_value=de_ratio,
                    expected_range="0 - 3 for large-cap non-financial",
                    severity="WARNING",
                    message=f"Large-cap showing D/E of {de_ratio} is unusual outside financials",
                    suggested_action="Cross-check with annual report"
                ))
        
        return de_ratio
    
    def _check_pe_ratio(self, pe_ratio: float, sector: str):
        """Validate P/E ratio."""
        if pe_ratio < 0:
            self.alerts.append(SanityAlert(
                field="pe_ratio",
                reported_value=pe_ratio,
                expected_range="Positive (company should be profitable)",
                severity="INFO",
                message="Negative P/E indicates losses",
                suggested_action="Check if company recently turned profitable"
            ))
        elif pe_ratio > 100:
            self.alerts.append(SanityAlert(
                field="pe_ratio",
                reported_value=pe_ratio,
                expected_range="5 - 50 for most sectors",
                severity="WARNING",
                message=f"P/E of {pe_ratio} is extremely high",
                suggested_action="May be due to one-time earnings dip"
            ))
    
    def _check_profit_margins(self, margins: float, sector: str):
        """Validate profit margins."""
        if margins > 0.8:  # 80%+ margins is rare
            self.alerts.append(SanityAlert(
                field="profit_margins",
                reported_value=margins,
                expected_range="0 - 50% for most industries",
                severity="WARNING",
                message=f"Profit margins of {margins:.1%} are unusually high",
                suggested_action="Verify if this includes one-time gains"
            ))
        elif margins < -0.5:  # Losing 50%+ of revenue
            self.alerts.append(SanityAlert(
                field="profit_margins",
                reported_value=margins,
                expected_range="Above -25% for going concerns",
                severity="ERROR",
                message=f"Negative margins of {margins:.1%} indicate severe losses",
                suggested_action="Check if company is in turnaround"
            ))
    
    def _check_roe(self, roe: float):
        """Validate Return on Equity."""
        if roe > 1.0:  # 100%+ ROE
            self.alerts.append(SanityAlert(
                field="return_on_equity",
                reported_value=roe,
                expected_range="5% - 40% for healthy companies",
                severity="WARNING",
                message=f"ROE of {roe:.1%} is unusually high - may indicate low equity base",
                suggested_action="Check for recent share buybacks or negative equity"
            ))
    
    def _parse_market_cap(self, cap_str: str) -> Optional[float]:
        """Parse market cap string to number."""
        try:
            if "T" in cap_str:
                return float(cap_str.replace("T", "").replace(",", "")) * 1e12
            elif "B" in cap_str:
                return float(cap_str.replace("B", "").replace(",", "")) * 1e9
            elif "M" in cap_str:
                return float(cap_str.replace("M", "").replace(",", "")) * 1e6
            return float(cap_str.replace(",", ""))
        except:
            return None


# Singleton instance
sanity_checker = SanityChecker()
