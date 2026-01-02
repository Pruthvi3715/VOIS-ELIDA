"""
FRED (Federal Reserve Economic Data) Service
Fetches US economic indicators for macro analysis.
"""
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import os


class FREDService:
    """
    Service to fetch economic data from FRED API.
    Free API with 120 requests/minute limit.
    """
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    # Key economic indicators
    INDICATORS = {
        "GDP": "GDP",                      # US GDP
        "UNEMPLOYMENT": "UNRATE",           # Unemployment Rate
        "INFLATION": "CPIAUCSL",           # Consumer Price Index
        "FED_FUNDS": "FEDFUNDS",           # Federal Funds Rate
        "TREASURY_10Y": "DGS10",           # 10-Year Treasury Yield
        "TREASURY_2Y": "DGS2",             # 2-Year Treasury Yield
        "MORTGAGE_30Y": "MORTGAGE30US",    # 30-Year Mortgage Rate
        "INDUSTRIAL_PRODUCTION": "INDPRO", # Industrial Production Index
        "RETAIL_SALES": "RSXFS",           # Retail Sales
        "CONSUMER_SENTIMENT": "UMCSENT",   # U Michigan Consumer Sentiment
    }
    
    # India Economic Indicators
    INDIA_INDICATORS = {
        "INDIA_GDP": "MKTGDPINA646NWDB",       # GDP Current Prices
        "INDIA_INFLATION": "FPCPITOTLZGIND",   # Inflation (Annual %)
        "INDIA_REPO_RATE": "IRSTCB01INM156N",  # Central Bank Policy Rate
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FRED_API_KEY")
        self._cache = {}
        self._cache_time = {}
        self._cache_duration = 3600  # 1 hour cache
    
    def get_indicator(self, indicator_name: str) -> Dict[str, Any]:
        """
        Fetch a single economic indicator.
        """
        series_id = self.INDICATORS.get(indicator_name.upper())
        if not series_id:
            return {"error": f"Unknown indicator: {indicator_name}"}
        
        # Check cache
        cache_key = f"indicator_{series_id}"
        if self._is_cached(cache_key):
            return self._cache[cache_key]
        
        try:
            data = self._fetch_series(series_id)
            self._cache[cache_key] = data
            self._cache_time[cache_key] = datetime.now()
            return data
        except Exception as e:
            return {"error": str(e), "series_id": series_id}
    
    def get_macro_summary(self) -> Dict[str, Any]:
        """
        Get a summary of key macro indicators.
        """
        cache_key = "macro_summary"
        if self._is_cached(cache_key):
            return self._cache[cache_key]
        
        summary = {
            "source": "FRED API" if self.api_key else "FRED Mock (No API Key)",
            "timestamp": datetime.now().isoformat(),
            "indicators": {}
        }
        
        # Key indicators for investment decisions
        key_indicators = ["FED_FUNDS", "TREASURY_10Y", "TREASURY_2Y", "UNEMPLOYMENT", "INFLATION"]
        
        for indicator in key_indicators:
            data = self.get_indicator(indicator)
            if "error" not in data:
                summary["indicators"][indicator.lower()] = {
                    "value": data.get("value"),
                    "date": data.get("date"),
                    "change": data.get("change"),
                    "description": data.get("description")
                }

        # Add India Indicators (FRED)
        for name, series_id in self.INDIA_INDICATORS.items():
            # Special handling: get_indicator expects key in INDICATORS, but these are in INDIA_INDICATORS
            # We can just fetch directly using series_id if we bypass get_indicator logic or update get_indicator
            # Simpler: use _fetch_series directly
            data = self._fetch_series(series_id)
            if "error" not in data:
                 summary["indicators"][name.lower()] = {
                    "value": data.get("value"),
                    "date": data.get("date"),
                    "description": data.get("title", name)
                }
        
        # Calculate yield curve (2Y-10Y spread)
        try:
            y10 = summary["indicators"].get("treasury_10y", {}).get("value")
            y2 = summary["indicators"].get("treasury_2y", {}).get("value")
            if y10 and y2:
                spread = float(y10) - float(y2)
                summary["yield_curve"] = {
                    "spread": round(spread, 2),
                    "status": "Inverted (Recession Signal)" if spread < 0 else "Normal"
                }
        except:
            pass
        
        self._cache[cache_key] = summary
        self._cache_time[cache_key] = datetime.now()
        return summary
    
    def _fetch_series(self, series_id: str) -> Dict[str, Any]:
        """
        Fetch series data from FRED API.
        """
        if not self.api_key:
            return self._get_mock_data(series_id)
        
        # Get series info
        url = f"{self.BASE_URL}/series"
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json"
        }
        
        response = requests.get(url, params=params, timeout=10)
        series_info = response.json().get("seriess", [{}])[0]
        
        # Get latest observations
        obs_url = f"{self.BASE_URL}/series/observations"
        obs_params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 2
        }
        
        obs_response = requests.get(obs_url, params=obs_params, timeout=10)
        observations = obs_response.json().get("observations", [])
        
        if not observations:
            return {"error": "No data available", "series_id": series_id}
        
        latest = observations[0]
        previous = observations[1] if len(observations) > 1 else None
        
        result = {
            "series_id": series_id,
            "title": series_info.get("title", series_id),
            "description": series_info.get("notes", ""),
            "value": float(latest["value"]) if latest["value"] != "." else None,
            "date": latest["date"],
            "units": series_info.get("units", ""),
            "frequency": series_info.get("frequency", "")
        }
        
        if previous and previous["value"] != ".":
            try:
                prev_val = float(previous["value"])
                curr_val = float(latest["value"])
                result["change"] = round(curr_val - prev_val, 3)
                result["change_pct"] = round((curr_val - prev_val) / prev_val * 100, 2) if prev_val else 0
            except:
                pass
        
        return result
    
    def _get_mock_data(self, series_id: str) -> Dict[str, Any]:
        """
        Return mock data when no API key is available.
        """
        mock_data = {
            "FEDFUNDS": {"value": 5.33, "title": "Federal Funds Rate", "units": "%"},
            "DGS10": {"value": 4.58, "title": "10-Year Treasury Yield", "units": "%"},
            "DGS2": {"value": 4.42, "title": "2-Year Treasury Yield", "units": "%"},
            "UNRATE": {"value": 4.2, "title": "Unemployment Rate", "units": "%"},
            "UNRATE": {"value": 4.2, "title": "Unemployment Rate", "units": "%"},
            "CPIAUCSL": {"value": 314.5, "title": "Consumer Price Index", "units": "Index"},
            # India Mocks
            "MKTGDPINA646NWDB": {"value": 3.4, "title": "India GDP (Trillion USD)", "units": "USD"},
            "FPCPITOTLZGIND": {"value": 5.4, "title": "India Inflation (CPI)", "units": "%"},
            "IRSTCB01INM156N": {"value": 6.5, "title": "India Repo Rate", "units": "%"},
        }
        
        data = mock_data.get(series_id, {})
        return {
            "series_id": series_id,
            "title": data.get("title", series_id),
            "value": data.get("value"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "units": data.get("units", ""),
            "source": "Mock Data (No FRED API Key)"
        }
    
    def _is_cached(self, key: str) -> bool:
        """Check if cache is valid."""
        if key not in self._cache:
            return False
        cache_time = self._cache_time.get(key)
        if not cache_time:
            return False
        return (datetime.now() - cache_time).seconds < self._cache_duration


# Singleton instance
fred_service = FREDService()
