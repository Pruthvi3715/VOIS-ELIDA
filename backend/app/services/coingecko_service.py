"""
CoinGecko Service for Cryptocurrency Data
Fetches real-time crypto data without API key (free tier).
"""
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime


class CoinGeckoService:
    """
    Fetches cryptocurrency data from CoinGecko API (free, no key required).
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Map common crypto symbols to CoinGecko IDs
    SYMBOL_MAP = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "XRP": "ripple",
        "SOL": "solana",
        "ADA": "cardano",
        "DOGE": "dogecoin",
        "DOT": "polkadot",
        "MATIC": "matic-network",
        "LINK": "chainlink",
        "AVAX": "avalanche-2",
        "UNI": "uniswap",
        "ATOM": "cosmos",
        "LTC": "litecoin",
        "XLM": "stellar"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json"
        })
    
    def get_crypto_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch comprehensive crypto data for analysis.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH", "BTC-USD", "CRYPTO:BTC")
        
        Returns:
            Dictionary with financial-like metrics for crypto
        """
        # Normalize symbol
        clean_symbol = self._normalize_symbol(symbol)
        coin_id = self.SYMBOL_MAP.get(clean_symbol.upper())
        
        if not coin_id:
            # Try direct lookup by ID
            coin_id = clean_symbol.lower()
        
        try:
            # Get current data
            coin_data = self._get_coin_data(coin_id)
            
            if "error" in coin_data:
                return coin_data
            
            # Get price history for technicals
            history = self._get_price_history(coin_id, days=365)
            
            return {
                "source": "CoinGecko (Live)",
                "asset_type": "cryptocurrency",
                "symbol": clean_symbol.upper(),
                "coin_id": coin_id,
                "current_price": coin_data.get("current_price_usd"),
                "currency": "USD",
                
                # Market Data
                "market_cap": self._format_large_number(coin_data.get("market_cap")),
                "market_cap_raw": coin_data.get("market_cap"),
                "total_volume_24h": self._format_large_number(coin_data.get("total_volume")),
                "circulating_supply": coin_data.get("circulating_supply"),
                "max_supply": coin_data.get("max_supply"),
                
                # Price Changes
                "price_change_24h": coin_data.get("price_change_24h"),
                "price_change_percentage_24h": coin_data.get("price_change_percentage_24h"),
                "price_change_percentage_7d": coin_data.get("price_change_percentage_7d"),
                "price_change_percentage_30d": coin_data.get("price_change_percentage_30d"),
                
                # 52W / ATH
                "52_week_high": coin_data.get("ath"),
                "52_week_low": coin_data.get("atl"),
                "ath": coin_data.get("ath"),
                "ath_date": coin_data.get("ath_date"),
                "atl": coin_data.get("atl"),
                "atl_date": coin_data.get("atl_date"),
                
                # Rank
                "market_cap_rank": coin_data.get("market_cap_rank"),
                
                # Sector/Category
                "sector": "Cryptocurrency",
                "industry": coin_data.get("category", "Digital Asset"),
                "company_name": coin_data.get("name", clean_symbol.upper()),
                
                # Summary
                "summary": coin_data.get("description", "Cryptocurrency asset")[:500] + "...",
                
                # Historical data for charts
                "price_history": history
            }
            
        except Exception as e:
            return {"error": str(e), "source": "CoinGecko"}
    
    def _normalize_symbol(self, symbol: str) -> str:
        """Normalize crypto symbol input."""
        # Handle various formats: BTC, BTC-USD, CRYPTO:BTC, bitcoin
        symbol = symbol.upper()
        if symbol.startswith("CRYPTO:"):
            symbol = symbol[7:]
        if "-USD" in symbol:
            symbol = symbol.replace("-USD", "")
        if "-INR" in symbol:
            symbol = symbol.replace("-INR", "")
        return symbol
    
    def _get_coin_data(self, coin_id: str) -> Dict[str, Any]:
        """Fetch current coin data."""
        try:
            # Simple price endpoint for speed
            url = f"{self.BASE_URL}/coins/{coin_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                return {"error": f"Coin '{coin_id}' not found"}
            
            response.raise_for_status()
            data = response.json()
            
            market_data = data.get("market_data", {})
            
            return {
                "name": data.get("name"),
                "symbol": data.get("symbol", "").upper(),
                "category": data.get("categories", ["Digital Asset"])[0] if data.get("categories") else "Digital Asset",
                "description": (data.get("description", {}).get("en", "") or "")[:500],
                
                # Price
                "current_price_usd": market_data.get("current_price", {}).get("usd"),
                
                # Market
                "market_cap": market_data.get("market_cap", {}).get("usd"),
                "market_cap_rank": market_data.get("market_cap_rank"),
                "total_volume": market_data.get("total_volume", {}).get("usd"),
                
                # Supply
                "circulating_supply": market_data.get("circulating_supply"),
                "max_supply": market_data.get("max_supply"),
                
                # Price Changes
                "price_change_24h": market_data.get("price_change_24h"),
                "price_change_percentage_24h": market_data.get("price_change_percentage_24h"),
                "price_change_percentage_7d": market_data.get("price_change_percentage_7d_in_currency", {}).get("usd"),
                "price_change_percentage_30d": market_data.get("price_change_percentage_30d_in_currency", {}).get("usd"),
                
                # ATH/ATL
                "ath": market_data.get("ath", {}).get("usd"),
                "ath_date": market_data.get("ath_date", {}).get("usd"),
                "atl": market_data.get("atl", {}).get("usd"),
                "atl_date": market_data.get("atl_date", {}).get("usd")
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {e}"}
    
    def _get_price_history(self, coin_id: str, days: int = 365) -> List[Dict]:
        """Fetch historical price data for charts."""
        try:
            url = f"{self.BASE_URL}/coins/{coin_id}/market_chart"
            params = {"vs_currency": "usd", "days": days}
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            prices = data.get("prices", [])
            volumes = data.get("total_volumes", [])
            
            history = []
            for i, (timestamp, price) in enumerate(prices):
                date = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
                volume = volumes[i][1] if i < len(volumes) else 0
                history.append({
                    "Date": date,
                    "Close": price,
                    "Volume": volume
                })
            
            return history
            
        except Exception as e:
            print(f"[CoinGecko] Price history error: {e}")
            return []
    
    def _format_large_number(self, value: Optional[float]) -> str:
        """Format large numbers with B/M suffix."""
        if not value:
            return "N/A"
        if value >= 1e12:
            return f"{value / 1e12:.2f}T"
        elif value >= 1e9:
            return f"{value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"{value / 1e6:.2f}M"
        return str(int(value))
    
    def is_crypto(self, symbol: str) -> bool:
        """Check if a symbol is a cryptocurrency."""
        clean = self._normalize_symbol(symbol)
        return clean.upper() in self.SYMBOL_MAP or symbol.startswith("CRYPTO:")


# Singleton instance
coingecko_service = CoinGeckoService()
