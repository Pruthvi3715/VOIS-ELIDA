"""
Data Validation and Anomaly Detection Service
Detects and corrects common data quality issues.
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class DataValidator:
    """
    Validates and enriches financial data with anomaly detection.
    """
    
    # Market to currency mapping
    MARKET_CURRENCIES = {
        ".NS": "INR",   # NSE India
        ".BO": "INR",   # BSE India
        ".L": "GBP",    # London
        ".HK": "HKD",   # Hong Kong
        ".TO": "CAD",   # Toronto
        ".AX": "AUD",   # Australia
        ".DE": "EUR",   # Germany
        ".PA": "EUR",   # Paris
        ".T": "JPY",    # Tokyo
    }
    
    # Reasonable market cap bounds by currency (in local currency)
    MARKET_CAP_BOUNDS = {
        "USD": {"max_trillion": 5.0},      # Largest US companies ~3T
        "INR": {"max_trillion": 25.0},     # In trillions INR, ~300B USD
        "GBP": {"max_trillion": 0.5},      # Largest UK ~200B GBP
        "EUR": {"max_trillion": 0.5},      # Largest EU ~400B EUR
        "JPY": {"max_trillion": 100.0},    # In trillions JPY
    }
    
    # Volatility thresholds for news triggers
    VOLATILITY_THRESHOLDS = {
        "extreme": 0.10,    # 10%+ requires urgent news hunt
        "high": 0.05,       # 5%+ should search for reasons
        "moderate": 0.03,   # 3%+ worth noting
    }
    
    def __init__(self):
        self.anomalies: List[Dict] = []
        self.corrections: List[Dict] = []
    
    def validate_and_enrich(
        self, 
        financials: Dict[str, Any],
        technicals: Dict[str, Any],
        asset_id: str
    ) -> Tuple[Dict, Dict, List[Dict]]:
        """
        Validate and enrich financial data.
        Returns: (corrected_financials, corrected_technicals, anomalies)
        """
        self.anomalies = []
        self.corrections = []
        
        # 1. Fix currency mismatch
        financials = self._fix_currency(financials, asset_id)
        
        # 2. Detect abnormal price movements
        price_anomaly = self._detect_price_anomaly(technicals, asset_id)
        if price_anomaly:
            self.anomalies.append(price_anomaly)
        
        # 3. Validate market cap sanity
        cap_anomaly = self._validate_market_cap(financials)
        if cap_anomaly:
            self.anomalies.append(cap_anomaly)
        
        # 4. Cross-validate price consistency
        price_mismatch = self._check_price_consistency(financials, technicals)
        if price_mismatch:
            self.anomalies.append(price_mismatch)
        
        # Add anomaly flags to data
        financials["_anomalies"] = [a for a in self.anomalies if a.get("category") == "financial"]
        technicals["_anomalies"] = [a for a in self.anomalies if a.get("category") == "technical"]
        technicals["_corrections"] = self.corrections
        
        return financials, technicals, self.anomalies
    
    def _fix_currency(self, financials: Dict, asset_id: str) -> Dict:
        """
        Detect and fix currency label based on market suffix.
        """
        detected_currency = None
        
        # Detect from asset suffix
        for suffix, currency in self.MARKET_CURRENCIES.items():
            if asset_id.upper().endswith(suffix):
                detected_currency = currency
                break
        
        reported_currency = financials.get("currency", "USD")
        
        # If mismatch detected
        if detected_currency and detected_currency != reported_currency:
            self.corrections.append({
                "field": "currency",
                "original": reported_currency,
                "corrected": detected_currency,
                "reason": f"Asset suffix indicates {detected_currency} market"
            })
            financials["currency"] = detected_currency
            financials["currency_corrected"] = True
            financials["currency_original"] = reported_currency
        
        return financials
    
    def _detect_price_anomaly(self, technicals: Dict, asset_id: str) -> Optional[Dict]:
        """
        Detect abnormal price movements that require explanation.
        """
        history = technicals.get("history", [])
        if len(history) < 2:
            return None
        
        # Get recent prices
        latest = history[-1].get("price", 0)
        previous = history[-2].get("price", 0)
        
        if previous == 0:
            return None
        
        daily_change = (latest - previous) / previous
        abs_change = abs(daily_change)
        
        # Determine severity
        severity = None
        requires_news = False
        
        if abs_change >= self.VOLATILITY_THRESHOLDS["extreme"]:
            severity = "EXTREME"
            requires_news = True
        elif abs_change >= self.VOLATILITY_THRESHOLDS["high"]:
            severity = "HIGH"
            requires_news = True
        elif abs_change >= self.VOLATILITY_THRESHOLDS["moderate"]:
            severity = "MODERATE"
        
        if severity:
            direction = "crash" if daily_change < 0 else "surge"
            return {
                "category": "technical",
                "type": "abnormal_price_movement",
                "severity": severity,
                "message": f"{severity} {direction}: {daily_change:.1%} in single session",
                "details": {
                    "previous_price": previous,
                    "current_price": latest,
                    "change_percent": round(daily_change * 100, 2),
                    "requires_news_search": requires_news,
                    "suggested_query": f"{asset_id} stock {direction} reason today" if requires_news else None,
                    "date": history[-1].get("date")
                }
            }
        
        return None
    
    def _validate_market_cap(self, financials: Dict) -> Optional[Dict]:
        """
        Validate market cap is reasonable for the currency.
        """
        market_cap_str = financials.get("market_cap", "")
        currency = financials.get("currency", "USD")
        
        # Parse market cap
        if "T" in market_cap_str:
            try:
                cap_value = float(market_cap_str.replace("T", "").replace(",", ""))
                
                bounds = self.MARKET_CAP_BOUNDS.get(currency, {})
                max_trillion = bounds.get("max_trillion", 10)
                
                if currency == "USD" and cap_value > 3.5:
                    # Suspicious - might be INR labeled as USD
                    return {
                        "category": "financial",
                        "type": "suspicious_market_cap",
                        "severity": "HIGH",
                        "message": f"Market cap {cap_value}T {currency} exceeds world's largest companies",
                        "details": {
                            "reported_value": market_cap_str,
                            "currency": currency,
                            "suspicion": "Likely INR mislabeled as USD"
                        }
                    }
            except:
                pass
        
        return None
    
    def _check_price_consistency(
        self, 
        financials: Dict, 
        technicals: Dict
    ) -> Optional[Dict]:
        """
        Check if financial and technical prices are consistent.
        """
        fin_price = financials.get("current_price", 0)
        tech_price = technicals.get("current_price", 0)
        
        if fin_price and tech_price:
            diff_pct = abs(fin_price - tech_price) / max(fin_price, tech_price) * 100
            
            if diff_pct > 5:  # More than 5% difference
                return {
                    "category": "data_consistency",
                    "type": "price_mismatch",
                    "severity": "MODERATE",
                    "message": f"Price mismatch: financials={fin_price}, technicals={tech_price}",
                    "details": {
                        "financial_price": fin_price,
                        "technical_price": tech_price,
                        "difference_percent": round(diff_pct, 2)
                    }
                }
        
        return None
    
    def get_news_search_query(self, anomalies: List[Dict], asset_id: str) -> Optional[str]:
        """
        Generate a specific news search query based on detected anomalies.
        """
        for anomaly in anomalies:
            if anomaly.get("details", {}).get("requires_news_search"):
                return anomaly["details"].get("suggested_query")
        
        return None


# Singleton instance
data_validator = DataValidator()
