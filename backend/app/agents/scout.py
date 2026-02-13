from yahooquery import Ticker
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from app.services.cache_service import cache_data
from app.core.config import settings
import datetime


class ScoutAgent:
    """
    The Scout Agent is responsible for gathering data from various sources.
    Enhanced with data validation, quality indicators, and improved error handling.
    """
    
    def __init__(self):
        self.name = "Scout Agent"
    
    def collect_data(self, asset_id: str) -> Dict[str, Any]:
        """
        Main entry point to collect data for a given asset.
        Returns data with quality indicators.
        """
        # Real data collection (mock mode disabled for production)
        result = self._fetch_cached_data(asset_id)
        
        # Add data quality assessment
        result["data_quality"] = self._assess_data_quality(result)
        result["collection_timestamp"] = datetime.datetime.now().isoformat()
        
        return result

    @staticmethod
    @cache_data(expire_seconds=3600)
    def _fetch_cached_data(asset_id: str) -> Dict[str, Any]:
        print(f"[Scout Agent] [FIND] Collecting data for {asset_id}...")
        
        # DEMO MODE - Safe mock company for presentations
        if asset_id.upper() in ("DEMO.NS", "DEMO", "ELIDA.NS"):
            print(f"[Scout Agent] [TARGET] Using DEMO company data (safe for presentation)")
            return ScoutAgent._get_demo_company_data()
        
        # Check if this is a cryptocurrency (NEW)
        from app.services.coingecko_service import coingecko_service
        if coingecko_service.is_crypto(asset_id) or asset_id.startswith("CRYPTO:"):
            print(f"[Scout Agent] [CRYPTO] Detected cryptocurrency: {asset_id}")
            crypto_data = coingecko_service.get_crypto_data(asset_id)
            
            if "error" not in crypto_data:
                # Build financials-like structure from crypto data
                financials = {
                    "source": crypto_data.get("source", "CoinGecko"),
                    "asset_type": "cryptocurrency",
                    "symbol": crypto_data.get("symbol"),
                    "company_name": crypto_data.get("company_name"),
                    "current_price": crypto_data.get("current_price"),
                    "currency": crypto_data.get("currency", "USD"),
                    "market_cap": crypto_data.get("market_cap"),
                    "52_week_high": crypto_data.get("ath"),
                    "52_week_low": crypto_data.get("atl"),
                    "price_change_24h": crypto_data.get("price_change_percentage_24h"),
                    "price_change_7d": crypto_data.get("price_change_percentage_7d"),
                    "price_change_30d": crypto_data.get("price_change_percentage_30d"),
                    "sector": "Cryptocurrency",
                    "industry": crypto_data.get("industry", "Digital Asset"),
                    "market_cap_rank": crypto_data.get("market_cap_rank"),
                    "total_volume_24h": crypto_data.get("total_volume_24h"),
                    "circulating_supply": crypto_data.get("circulating_supply"),
                    "max_supply": crypto_data.get("max_supply"),
                    "summary": crypto_data.get("summary", "")
                }
                
                # Build technicals from price history
                history = crypto_data.get("price_history", [])
                technicals = {
                    "history": history,
                    "rsi_14": ScoutAgent._calculate_rsi_from_history(history) if history else None,
                    "trend_signal": ScoutAgent._calculate_trend_from_history(history) if history else "Unknown"
                }
                
                macro = ScoutAgent._get_macro_data_static(asset_id)
                news = []  # Crypto news would need different source
                
                print(f"[Scout Agent] [OK] Crypto collection complete: {crypto_data.get('company_name')}")
                return {
                    "financials": financials,
                    "technicals": technicals,
                    "macro": macro,
                    "news": news,
                    "anomalies": [],
                    "sanity_alerts": []
                }
            else:
                print(f"[Scout Agent] [WARN] Crypto fetch failed: {crypto_data.get('error')}")
        
        # Regular stock data flow

        
        # Ticker Normalization for known issues (e.g. Asian Paints)
        if asset_id == "ASIANPAINTS.NS":
            print(f"[Scout Agent] [FIX] Normalizing ticker: ASIANPAINTS.NS -> ASIANPAINT.NS")
            asset_id = "ASIANPAINT.NS"

        # Regular stock data flow
        financials = ScoutAgent._get_financials_deep_static(asset_id)
        technicals = ScoutAgent._get_technicals_static(asset_id)
        macro = ScoutAgent._get_macro_data_static(asset_id)
        news = ScoutAgent._get_news_static(asset_id)
        
        # Enrich with Screener.in data for Indian stocks (NEW)
        if asset_id.endswith(".NS") or asset_id.endswith(".BO"):
            try:
                from app.services.screener_service import screener_service
                screener_data = screener_service.get_data(asset_id)
                
                if "error" not in screener_data:
                    print(f"[Scout Agent] [DATA] Screener.in fetch successful")
                    
                    # Check if we are currently using Mock/Fallback data from Yahoo
                    is_mock = "Mock" in str(financials.get("source", "")) or financials.get("current_price", 0) == 1000.0
                    
                    if is_mock:
                         print(f"[Scout Agent] [RECOVERY] Replacing Mock/Failed Yahoo data with Genuine Screener.in data")
                         financials = ScoutAgent._map_screener_to_financials(screener_data, financials)
                    else:
                        print(f"[Scout Agent] [DATA] Enriching Yahoo data with Screener.in metrics")
                        # Merge Screener data - prioritize Screener for these fields
                        if screener_data.get("roce"):
                            financials["roce"] = screener_data["roce"]
                        if screener_data.get("promoter_holding"):
                            financials["promoter_holding"] = screener_data["promoter_holding"]
                        if screener_data.get("fii_holding"):
                            financials["fii_holding"] = screener_data["fii_holding"]
                        if screener_data.get("dii_holding"):
                            financials["dii_holding"] = screener_data["dii_holding"]
                        if screener_data.get("screener_book_value") and not financials.get("book_value"):
                            financials["book_value"] = screener_data["screener_book_value"]
                        if screener_data.get("face_value"):
                            financials["face_value"] = screener_data["face_value"]
                        if screener_data.get("sales_growth_5yr"):
                            financials["sales_growth_5yr"] = screener_data["sales_growth_5yr"]
                        if screener_data.get("profit_growth_5yr"):
                            financials["profit_growth_5yr"] = screener_data["profit_growth_5yr"]
                else:
                    print(f"[Scout Agent] [WARN] Screener.in: {screener_data.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"[Scout Agent] [WARN] Screener.in enrichment failed: {e}")
        
        # Apply data validation and corrections (currency, price anomalies)
        from app.services.data_validator import data_validator
        
        financials, technicals, anomalies = data_validator.validate_and_enrich(
            financials, technicals, asset_id
        )
        
        # Apply sanity checks to catch hallucinations (D/E ratio, etc.)
        from app.services.sanity_checker import sanity_checker
        
        financials, sanity_alerts = sanity_checker.check_financials(financials, asset_id)
        
        # Log sanity check results
        for alert in sanity_alerts:
            severity_icon = "[ALERT]" if alert.severity == "CRITICAL" else "[WARN]" if alert.severity == "ERROR" else "[INFO]"
            print(f"[Scout Agent] {severity_icon} Sanity Check [{alert.severity}]: {alert.message}")
            if alert.suggested_action:
                print(f"              -> Action: {alert.suggested_action}")
        
        # If significant price movement detected, search for specific news
        volatility_query = data_validator.get_news_search_query(anomalies, asset_id)
        if volatility_query:
            print(f"[Scout Agent] [WARN] Abnormal price movement detected! Searching: {volatility_query}")
            volatility_news = ScoutAgent._get_volatility_news(asset_id, volatility_query)
            if volatility_news:
                news = volatility_news + news  # Prepend volatility-specific news
        
        # Log corrections and anomalies
        if financials.get("currency_corrected"):
            print(f"[Scout Agent] [FIX] Currency corrected: {financials.get('currency_original')} -> {financials.get('currency')}")
        
        if financials.get("debt_to_equity_corrected"):
            print(f"[Scout Agent] [FIX] D/E Ratio corrected: {financials.get('debt_to_equity_original')} -> {financials.get('debt_to_equity')}")
        
        for anomaly in anomalies:
            print(f"[Scout Agent] [WARN] {anomaly.get('severity', 'INFO')}: {anomaly.get('message', 'Unknown anomaly')}")
        
        # Log collection summary
        fin_source = financials.get("source", "Unknown")
        tech_valid = "history" in technicals and len(technicals.get("history", [])) > 0
        macro_valid = macro.get("volatility_index") not in [None, "N/A", "Error"]
        
        print(f"[Scout Agent] [OK] Collection complete:")
        print(f"  - Financials: {fin_source}")
        print(f"  - Technicals: {'Valid' if tech_valid else 'Mock'}")
        print(f"  - Macro: {'Valid' if macro_valid else 'Incomplete'}")
        print(f"  - News: {len(news)} items")
        print(f"  - Anomalies: {len(anomalies)} detected")
        print(f"  - Sanity Alerts: {len(sanity_alerts)} issues")
        
        return {
            "financials": financials,
            "technicals": technicals,
            "macro": macro,
            "news": news,
            "anomalies": anomalies,
            "sanity_alerts": [{"field": a.field, "severity": a.severity, "message": a.message} for a in sanity_alerts]
        }

    @staticmethod
    def _map_screener_to_financials(screener_data: Dict[str, Any], old_financials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps known Screener.in data fields to our internal financials structure.
        Used when primary data source fails.
        """
        # Start with a clean structure but keep existing useful metadata
        new_fin = old_financials.copy()
        
        # Update source to indicate recovery
        new_fin["source"] = "Screener.in (Valid)"
        new_fin["is_mock"] = False
        new_fin["currency"] = "INR"  # Screener is India-only
        
        # Map core metrics
        if "screener_market_cap" in screener_data:
            # Convert Cr to Billions or Trillions string format for consistency explanation
            mcap_cr = screener_data["screener_market_cap"]
            if mcap_cr:
                 if mcap_cr > 100000:
                     new_fin["market_cap"] = f"{mcap_cr/100000:.2f}T"
                 else:
                     new_fin["market_cap"] = f"{mcap_cr/1000:.2f}B"
        
        # Valuation
        if "screener_pe" in screener_data:
            new_fin["pe_ratio"] = screener_data["screener_pe"]
        
        if "screener_book_value" in screener_data:
            new_fin["book_value"] = screener_data["screener_book_value"]
            if "current_price" in screener_data: # If we scraped price? Screener usually has it
                 pass # Screener scraper didn't return current price explicitly?
        
        # Profitability
        if "roce" in screener_data:
            new_fin["return_on_capital_employed"] = screener_data["roce"]
        if "screener_roe" in screener_data:
            new_fin["return_on_equity"] = screener_data["screener_roe"]
        if "profit_margins" in screener_data: # If calculated
             pass
             
        # Screener specific
        if "promoter_holding" in screener_data:
            new_fin["promoter_holding"] = screener_data["promoter_holding"]
        
        # Growth
        if "sales_growth_5yr" in screener_data:
            new_fin["revenue_growth"] = screener_data["sales_growth_5yr"]
        if "profit_growth_5yr" in screener_data:
            new_fin["earnings_growth"] = screener_data["profit_growth_5yr"]

        # Note about missing keys
        new_fin["summary"] = f"Analysis based on Screener.in data. Market Cap: {new_fin.get('market_cap', 'N/A')}, P/E: {new_fin.get('pe_ratio', 'N/A')}, ROE: {new_fin.get('return_on_equity', 'N/A')}%."
        
        return new_fin

    def _assess_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess overall data quality and completeness.
        """
        quality = {
            "overall": "High",
            "components": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check financials
        financials = data.get("financials", {})
        if "Mock" in str(financials.get("source", "")):
            quality["components"]["financials"] = "Low"
            quality["issues"].append("Financial data from mock source")
        elif financials.get("pe_ratio") is None:
            quality["components"]["financials"] = "Medium"
            quality["issues"].append("Some financial metrics missing")
        else:
            quality["components"]["financials"] = "High"
        
        # Check technicals
        technicals = data.get("technicals", {})
        if "Mock" in str(technicals.get("note", "")):
            quality["components"]["technicals"] = "Low"
            quality["issues"].append("Technical data from mock source")
        elif len(technicals.get("history", [])) < 50:
            quality["components"]["technicals"] = "Medium"
            quality["issues"].append("Limited price history available")
        else:
            quality["components"]["technicals"] = "High"
        
        # Check macro
        macro = data.get("macro", {})
        if macro.get("volatility_index") in [None, "N/A", "Error"]:
            quality["components"]["macro"] = "Low"
            quality["issues"].append("Macro indicators unavailable")
        else:
            quality["components"]["macro"] = "High"
        
        # Check news
        news = data.get("news", [])
        if not news or "No recent news" in str(news):
            quality["components"]["news"] = "Low"
            quality["issues"].append("No recent news available")
        else:
            quality["components"]["news"] = "High"
        
        # Calculate overall quality
        component_scores = {"High": 3, "Medium": 2, "Low": 1}
        scores = [component_scores.get(v, 2) for v in quality["components"].values()]
        avg_score = sum(scores) / len(scores) if scores else 2
        
        if avg_score >= 2.5:
            quality["overall"] = "High"
        elif avg_score >= 1.5:
            quality["overall"] = "Medium"
            quality["recommendations"].append("Consider waiting for better data before major decisions")
        else:
            quality["overall"] = "Low"
            quality["recommendations"].append("Data quality is low - use with caution")
        
        return quality

    @staticmethod
    def _get_financials_deep_static(asset_id: str) -> Dict[str, Any]:
        """
        Fetch comprehensive financial data with validation.
        """
        try:
            ticker = Ticker(asset_id)
            
            # Request quoteType carefully as it might fail for some assets
            modules = ticker.get_modules(['summaryDetail', 'financialData', 'defaultKeyStatistics', 'summaryProfile', 'price', 'quoteType'])
            
            if asset_id not in modules or isinstance(modules[asset_id], str):
                raise ValueError(f"No data found for {asset_id}")

            data_all = modules[asset_id]
            
            summary_detail = data_all.get('summaryDetail', {})
            financial_data = data_all.get('financialData', {})
            key_stats = data_all.get('defaultKeyStatistics', {})
            summary_profile = data_all.get('summaryProfile', {})
            price_module = data_all.get('price', {})
            summary_profile = data_all.get('summaryProfile', {})
            price_module = data_all.get('price', {})
            quote_type_module = data_all.get('quoteType', {})
            
            # Check for Forex/Currency
            quote_type = quote_type_module.get('quoteType', 'EQUITY')
            is_forex = quote_type == 'CURRENCY'
            
            # Extract basic price data (works for both Eq and Forex)
            current_price = financial_data.get("currentPrice") or price_module.get("regularMarketPrice") or 0.0
            currency = financial_data.get("currency") or price_module.get("currency") or "USD"
            
            # Forex-specific extraction
            if is_forex:
                data = {
                    "source": "YahooQuery (Forex)",
                    "asset_type": "forex",
                    "symbol": asset_id,
                    "current_price": current_price,
                    "currency": currency,
                    "bid": summary_detail.get("bid"),
                    "ask": summary_detail.get("ask"),
                    "previous_close": summary_detail.get("previousClose"),
                    "open": summary_detail.get("open"),
                    "52_week_high": summary_detail.get("fiftyTwoWeekHigh"),
                    "52_week_low": summary_detail.get("fiftyTwoWeekLow"),
                    "sector": "Currency",
                    "industry": "Forex",
                    "company_name": price_module.get("shortName") or quote_type_module.get("shortName") or asset_id,
                    "summary": f"Forex pair {asset_id} ({quote_type_module.get('longName', asset_id)})"
                }
                print(f"[Scout Agent] [FOREX] Forex pair detected: {data['company_name']}")
                return data

            # Standard Equity Extraction
            market_cap_raw = summary_detail.get('marketCap', 0)
            
            # Format market cap
            if market_cap_raw:
                if market_cap_raw >= 1e12:
                    market_cap = f"{market_cap_raw / 1e12:.2f}T"
                elif market_cap_raw >= 1e9:
                    market_cap = f"{market_cap_raw / 1e9:.2f}B"
                elif market_cap_raw >= 1e6:
                    market_cap = f"{market_cap_raw / 1e6:.2f}M"
                else:
                    market_cap = str(market_cap_raw)
            else:
                market_cap = "N/A"
            
            data = {
                "source": "YahooQuery (Live)",
                "symbol": asset_id,
                "current_price": current_price,
                "currency": currency,
                
                # Valuation Metrics
                "pe_ratio": ScoutAgent._safe_round(summary_detail.get("trailingPE")),
                "forward_pe": ScoutAgent._safe_round(summary_detail.get("forwardPE")),
                "peg_ratio": ScoutAgent._safe_round(key_stats.get("pegRatio")),
                "price_to_book": ScoutAgent._safe_round(key_stats.get("priceToBook")),
                "market_cap": market_cap,
                
                # Price Data
                "previous_close": ScoutAgent._safe_round(summary_detail.get("previousClose")),
                "52_week_high": ScoutAgent._safe_round(summary_detail.get("fiftyTwoWeekHigh")),
                "52_week_low": ScoutAgent._safe_round(summary_detail.get("fiftyTwoWeekLow")),
                "beta": ScoutAgent._safe_round(summary_detail.get("beta")),
                
                # Dividend Data
                "dividend_yield": ScoutAgent._safe_round(summary_detail.get("dividendYield"), 4),
                "dividend_rate": ScoutAgent._safe_round(summary_detail.get("dividendRate")),
                
                # Book Value
                "book_value": ScoutAgent._safe_round(key_stats.get("bookValue")),
                
                # Profitability & Efficiency
                "profit_margins": ScoutAgent._safe_round(financial_data.get("profitMargins"), 4),
                "return_on_equity": ScoutAgent._safe_round(financial_data.get("returnOnEquity"), 4),
                "return_on_assets": ScoutAgent._safe_round(financial_data.get("returnOnAssets"), 4),
                
                # Financial Health
                "debt_to_equity": ScoutAgent._safe_round(financial_data.get("debtToEquity")),
                "current_ratio": ScoutAgent._safe_round(financial_data.get("currentRatio")),
                "free_cash_flow": financial_data.get("freeCashflow"),
                
                # Growth
                "revenue_growth": ScoutAgent._safe_round(financial_data.get("revenueGrowth"), 4),
                "earnings_growth": ScoutAgent._safe_round(financial_data.get("earningsGrowth"), 4),
                
                # Company Info
                "sector": summary_profile.get("sector", "Unknown"),
                "industry": summary_profile.get("industry", "Unknown"),
                "company_name": summary_profile.get("longName") or key_stats.get("shortName", asset_id),
                "summary": (summary_profile.get("longBusinessSummary", "") or "")[:500] + "...",

                # NEW: Advanced Metrics (Requested by User)
                "enterprise_value": ScoutAgent._safe_round(key_stats.get("enterpriseValue")),
                "price_to_sales": ScoutAgent._safe_round(summary_detail.get("priceToSalesTrailing12Months")),
                "enterprise_to_revenue": ScoutAgent._safe_round(key_stats.get("enterpriseToRevenue")),
                "enterprise_to_ebitda": ScoutAgent._safe_round(key_stats.get("enterpriseToEbitda")),
                
                # Share Statistics
                "shares_outstanding": ScoutAgent._safe_round(key_stats.get("sharesOutstanding"), 0),
                "float_shares": ScoutAgent._safe_round(key_stats.get("floatShares"), 0),
                "held_percent_insiders": ScoutAgent._safe_round(key_stats.get("heldPercentInsiders"), 4),
                "held_percent_institutions": ScoutAgent._safe_round(key_stats.get("heldPercentInstitutions"), 4),
                "short_ratio": ScoutAgent._safe_round(key_stats.get("shortRatio")),
                
                # Dates
                "fiscal_year_ends": key_stats.get("lastFiscalYearEnd"),
                "most_recent_quarter": key_stats.get("mostRecentQuarter"),
                
                # Balance Sheet Highlights
                "total_cash": key_stats.get("totalCash"),
                "total_debt": key_stats.get("totalDebt")
            }
            
            # Validate we got meaningful data
            if not current_price:
                 # Check if it's potentially an ETF or Index which might behave differently
                 if quote_type == 'ETF':
                      data['sector'] = 'Exchange Traded Fund'
                      return data
                 if quote_type == 'INDEX':
                      data['sector'] = 'Index'
                      return data
                 
                 raise ValueError("Empty price data from YahooQuery")
            
            # Count valid metrics for quality indicator
            valid_metrics = sum(1 for v in data.values() if v is not None and v != "N/A")
            data["metrics_available"] = valid_metrics
            data["metrics_total"] = len(data) - 3  # Exclude source, symbol, metrics counts
            
            return data
            
        except Exception as e:
            print(f"[Scout Agent] [WARN] YahooQuery financials failed: {e}")
            
            # Fallback: Try yfinance
            try:
                print(f"[Scout Agent] [RETRY] Attempting yfinance fallback for financials...")
                import yfinance as yf
                ticker = yf.Ticker(asset_id)
                info = ticker.info
                
                if not info or 'regularMarketPrice' not in info:
                    raise ValueError("yfinance returned empty data")
                
                # Construct data from yfinance info
                data = {
                    "source": "yfinance (Fallback)",
                    "symbol": asset_id,
                    "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
                    "currency": info.get("currency", "USD"),
                    
                    # Valuation
                    "pe_ratio": info.get("trailingPE"),
                    "forward_pe": info.get("forwardPE"),
                    "peg_ratio": info.get("pegRatio"),
                    "price_to_book": info.get("priceToBook"),
                    "market_cap": f"{info.get('marketCap', 0) / 1e9:.2f}B" if info.get('marketCap') else "N/A",
                    "enterprise_value": info.get("enterpriseValue"),
                    "price_to_sales": info.get("priceToSalesTrailing12Months"),
                    "enterprise_to_revenue": info.get("enterpriseToRevenue"),
                    "enterprise_to_ebitda": info.get("enterpriseToEbitda"),
                    
                    # Profitability
                    "profit_margins": info.get("profitMargins"),
                    "return_on_equity": info.get("returnOnEquity"),
                    "return_on_assets": info.get("returnOnAssets"),
                    
                    # Health
                    "debt_to_equity": info.get("debtToEquity"),
                    "current_ratio": info.get("currentRatio"),
                    "free_cash_flow": info.get("freeCashflow"),
                    "total_cash": info.get("totalCash"),
                    "total_debt": info.get("totalDebt"),
                    
                    # Growth
                    "revenue_growth": info.get("revenueGrowth"),
                    "earnings_growth": info.get("earningsGrowth"),
                    
                    # Share Stats
                    "shares_outstanding": info.get("sharesOutstanding"),
                    "float_shares": info.get("floatShares"),
                    "held_percent_insiders": info.get("heldPercentInsiders"),
                    "held_percent_institutions": info.get("heldPercentInstitutions"),
                    "short_ratio": info.get("shortRatio"),
                    
                    # Info
                    "sector": info.get("sector", "Unknown"),
                    "industry": info.get("industry", "Unknown"),
                    "company_name": info.get("longName", asset_id),
                    "summary": info.get("longBusinessSummary", "")[:500] + "..."
                }
                
                print(f"[Scout Agent] [OK] yfinance fallback successful")
                
                # Count valid metrics
                valid_metrics = sum(1 for v in data.values() if v is not None and v != "N/A")
                data["metrics_available"] = valid_metrics
                data["metrics_total"] = len(data) - 3
                return data
                
            except Exception as yf_e:
                print(f"[Scout Agent] [ERROR] yfinance fallback failed: {yf_e}")
            
            # Final Fallback: MOCK
            # Final Fallback: MOCK
            if settings.ALLOW_DEMO_DATA:
                print(f"[Scout Agent] 📦 Using synthetic mock data (ALLOW_DEMO_DATA=True)")
                return ScoutAgent._get_mock_financials(asset_id)
            else:
                from app.core.exceptions import DataFetchException
                raise DataFetchException(asset_id, "financials", "All data providers failed and demo data is disabled.")

    @staticmethod
    def _get_mock_financials(asset_id: str) -> Dict[str, Any]:
        """
        Returns generic mock financial data as fallback when API fails.
        """
        return {
            "source": "Mock Data (API Fallback)",
            "symbol": asset_id,
            "current_price": 1000.00,
            "currency": "INR",
            "pe_ratio": 20.0,
            "forward_pe": 18.0,
            "peg_ratio": 1.0,
            "price_to_book": 2.0,
            "market_cap": "100B",
            "profit_margins": 0.10,
            "return_on_equity": 0.15,
            "return_on_assets": 0.08,
            "debt_to_equity": 50.0,
            "current_ratio": 1.5,
            "free_cash_flow": 1000000000,
            "revenue_growth": 0.10,
            "earnings_growth": 0.08,
            "sector": "Unknown (API Failed)",
            "industry": "Unknown (API Failed)",
            "summary": f"Data for {asset_id} is currently unavailable due to API limits. This is placeholder data.",
            "metrics_available": 5,
            "metrics_total": 20,
            "is_mock": True
        }

    @staticmethod
    def _get_technicals_static(asset_id: str) -> Dict[str, Any]:
        """
        Calculate technical indicators with enhanced error handling.
        """
        try:
            # Primary: YahooQuery
            # Primary: yfinance (More robust standard)
            try:
                import yfinance as yf
                # print(f"[Scout Agent] [CHART] Fetching technicals via yfinance for {asset_id}...")
                ticker = yf.Ticker(asset_id)
                df = ticker.history(period="1y")
                
                if df.empty or len(df) < 50:
                    raise ValueError("yfinance returned empty technicals")
                
                close_col = 'Close'
                source = "yfinance (Live)"

            except Exception as yf_e:
                print(f"[Scout Agent] [WARN] yfinance technicals failed: {yf_e}")
                
                # Fallback: YahooQuery
                try:
                    print(f"[Scout Agent] [RETRY] Attempting YahooQuery fallback for technicals...")
                    ticker = Ticker(asset_id)
                    hist = ticker.history(period="1y")
                    
                    if isinstance(hist, dict) or hist.empty:
                        raise ValueError("No historical data")
                    
                    # Handle MultiIndex
                    if 'symbol' in hist.index.names:
                        df = hist.xs(asset_id, level='symbol')
                    else:
                        df = hist

                    if df.empty or len(df) < 50:
                        raise ValueError("Insufficient historical data")

                    # Determine close column
                    close_col = 'close' if 'close' in df.columns else 'adjclose'
                    if close_col not in df.columns:
                        if 'Close' in df.columns:
                            close_col = 'Close'
                        else:
                            raise ValueError("No Close price column found")
                            
                    source = "YahooQuery (Fallback)"
                except Exception as yq_e:
                    raise ValueError(f"Both providers failed. yfinance: {yf_e}, YahooQuery: {yq_e}")

            close = df[close_col]
            
            # Calculate indicators
            sma_50 = close.rolling(window=50).mean().iloc[-1]
            sma_200 = close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None
            current_price = close.iloc[-1]
            
            # Trend determination
            if sma_200 is not None:
                if current_price > sma_50 > sma_200:
                    trend = "Strong Uptrend (Bullish)"
                elif current_price < sma_50 < sma_200:
                    trend = "Strong Downtrend (Bearish)"
                elif sma_50 > sma_200:
                    trend = "Uptrend (Golden Cross)"
                else:
                    trend = "Downtrend (Death Cross)"
            else:
                trend = "Neutral (Insufficient history for 200-day SMA)"
            
            # RSI calculation
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = (100 - (100 / (1 + rs))).iloc[-1]
            
            # Safely handle NaN RSI (e.g. flat price)
            if pd.isna(rsi):
                rsi = 50.0
            
            rsi_status = "Neutral"
            if rsi > 70:
                rsi_status = "Overbought"
            elif rsi < 30:
                rsi_status = "Oversold"
            
            # Volatility
            daily_returns = close.pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252)
            
            # 52-week range
            high_52w = close.max()
            low_52w = close.min()
            pct_from_high = ((current_price - high_52w) / high_52w) * 100
            
            # Prepare history for charting
            history_df = pd.concat([
                close,
                close.rolling(window=50).mean().rename('sma_50')
            ], axis=1).iloc[-100:]
            
            history = []
            for idx, row in history_df.iterrows():
                # Handle both datetime and date index types
                if hasattr(idx, 'date'):
                    date_str = str(idx.date())
                else:
                    date_str = str(idx).split(" ")[0]
                    
                history.append({
                    "date": date_str,
                    "price": round(float(row[close_col]), 2),
                    "sma_50": round(float(row['sma_50']), 2) if not pd.isna(row['sma_50']) else None
                })

                        # Recent price changes (for data latency awareness)
            price_1d_ago = close.iloc[-2] if len(close) >= 2 else current_price
            price_5d_ago = close.iloc[-6] if len(close) >= 6 else current_price
            
            price_change_1d = ((current_price - price_1d_ago) / price_1d_ago) * 100 if price_1d_ago else 0
            price_change_5d = ((current_price - price_5d_ago) / price_5d_ago) * 100 if price_5d_ago else 0
            
            # Generate price alert for significant moves
            price_alert = None
            if price_change_5d <= -5:
                price_alert = f"[WARN] ALERT: Price dropped {abs(price_change_5d):.1f}% in last 5 days"
            elif price_change_5d >= 5:
                price_alert = f"[CHART] ALERT: Price surged {price_change_5d:.1f}% in last 5 days"
            elif price_change_1d <= -3:
                price_alert = f"[WARN] ALERT: Price dropped {abs(price_change_1d):.1f}% today"
            elif price_change_1d >= 3:
                price_alert = f"[CHART] ALERT: Price surged {price_change_1d:.1f}% today"

            return {
                "source": source,
                "current_price": round(float(current_price), 2),
                "sma_50": round(float(sma_50), 2),
                "sma_200": round(float(sma_200), 2) if sma_200 else None,
                "trend_signal": trend,
                "rsi_14": round(float(rsi), 2),
                "rsi_status": rsi_status,
                "volatility_annualized": f"{volatility:.2%}",
                "volatility_raw": round(float(volatility), 4),
                "high_52w": round(float(high_52w), 2),
                "low_52w": round(float(low_52w), 2),
                "pct_from_52w_high": round(float(pct_from_high), 2),
                # NEW: Recent price changes
                "price_change_1d": round(float(price_change_1d), 2),
                "price_change_5d": round(float(price_change_5d), 2),
                "price_alert": price_alert,
                "history": history,
                "data_points": len(close)
            }
            
        except Exception as e:
            print(f"[Scout Agent] [WARN] Error calculating technicals for {asset_id}: {e}")
            if settings.ALLOW_DEMO_DATA:
                 return ScoutAgent._get_mock_technicals()
            raise e  # Propagate error if no demo data allowed

    @staticmethod
    def _get_mock_technicals() -> Dict[str, Any]:
        """
        Returns generic mock technical data as fallback.
        """
        base_date = datetime.date.today()
        return {
            "source": "Mock Data (API Fallback)",
            "current_price": 1000.00,
            "sma_50": 980.00,
            "sma_200": 950.00,
            "trend_signal": "Neutral (Data Unavailable)",
            "rsi_14": 50.0,
            "rsi_status": "Neutral",
            "volatility_annualized": "15.00%",
            "volatility_raw": 0.15,
            "high_52w": 1100.00,
            "low_52w": 900.00,
            "pct_from_52w_high": -9.09,
            "history": [],
            "data_points": 0,
            "note": "Mock Data (API Failed) - Real chart data unavailable"
        }

    @staticmethod
    def _get_macro_data_static(asset_id: str = None) -> Dict[str, Any]:
        """
        Fetch macro indicators with region awareness.
        Uses India VIX for .NS/.BO stocks, US VIX for others.
        """
        # Detect region from asset_id
        is_india = asset_id and asset_id.upper().endswith((".NS", ".BO"))
        region = "INDIA" if is_india else "US"
        
        # Region-specific macro proxies
        # Region-specific macro proxies
        if is_india:
            macro_proxies = {
                "volatility_index": "^INDIAVIX",     # India VIX
                "market_change_pct": "^NSEI",        # Nifty 50
                "interest_rate_proxy": "^TNX",       # US 10Y as Proxy (hard to get India 10Y on Yahoo)
            }
        else:
            macro_proxies = {
                "interest_rate_proxy": "^TNX",        # US 10Y Treasury
                "volatility_index": "^VIX",           # US VIX
                "market_change_pct": "^GSPC",         # S&P 500
            }
        
        results = {
            "source": f"YahooQuery (Macro - {region})",
            "region": region,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        try:
            symbols = list(macro_proxies.values())
            tickers = Ticker(symbols)
            price_data = tickers.price
            
            for key, symbol in macro_proxies.items():
                if symbol in price_data and isinstance(price_data[symbol], dict):
                    price = price_data[symbol].get('regularMarketPrice')
                    change_pct = price_data[symbol].get('regularMarketChangePercent')
                    
                    results[key] = price if price else "N/A"
                    results[f"{key}_symbol"] = symbol
                    if change_pct is not None:
                        results[f"{key}_change"] = round(float(change_pct) * 100, 2)
                else:
                    results[key] = "N/A"
            
            # Add market interpretation
            vix = results.get("volatility_index")
            if isinstance(vix, (int, float)):
                if vix > 25:
                    results["vix_interpretation"] = "High Fear"
                elif vix < 15:
                    results["vix_interpretation"] = "Low Volatility / Complacency"
                else:
                    results["vix_interpretation"] = "Normal Range"
                    
        except Exception as e:
            print(f"[Scout Agent] [WARN] Error fetching macro data: {e}")
            results["error"] = str(e)
            for key in macro_proxies:
                if key not in results:
                    results[key] = "Error"
        
        # Integrate FRED Data (Economic Indicators)
        try:
            from app.services.fred_service import fred_service
            fred_data = fred_service.get_macro_summary()
            if "indicators" in fred_data:
                for ind_name, ind_data in fred_data["indicators"].items():
                    if isinstance(ind_data, dict):
                        results[f"fred_{ind_name}"] = ind_data.get("value", "N/A")
                        results[f"fred_{ind_name}_desc"] = ind_data.get("description", "")
            
            if "yield_curve" in fred_data:
                results["yield_curve_spread"] = fred_data["yield_curve"].get("spread")
                results["yield_curve_signal"] = fred_data["yield_curve"].get("status")
                
        except Exception as e:
            print(f"[Scout Agent] [WARN] FRED integration failed: {e}")

        # Integrate Real-Time RBI Data for Indian stocks
        if is_india:
            try:
                from app.services.rbi_service import rbi_service
                rbi_data = rbi_service.get_real_time_rates()
                if "repo_rate" in rbi_data:
                    results["rbi_repo_rate"] = rbi_data["repo_rate"]
                    results["rbi_repo_rate_desc"] = "Policy Repo Rate (RBI Live)"
                    print(f"[Scout Agent] [INDIA] RBI Live Rate: {rbi_data['repo_rate']}%")
                elif "error" in rbi_data:
                    print(f"[Scout Agent] [WARN] RBI Scraper Warning: {rbi_data['error']}")
            except Exception as e:
                print(f"[Scout Agent] [WARN] RBI Scraper Failed: {e}")

        return results

    @staticmethod
    def _get_news_static(asset_id: str) -> List[Dict[str, str]]:
        """
        Fetch news using multiple sources with fallback.
        Primary: yahooquery search API (returns news section)
        Fallback: yfinance
        """
        results = []
        
        # Method 1: Try yahooquery search API (more reliable for news)
        try:
            from yahooquery import search, Ticker
            
            # Try to get company name for better search
            try:
                ticker_info = Ticker(asset_id)
                quote_type = ticker_info.quote_type.get(asset_id, {})
                company_name = quote_type.get("longName", "") or quote_type.get("shortName", "")
                if company_name:
                    search_term = f"{company_name} stock news"
                else:
                    search_term = asset_id.replace(".NS", "").replace(".BO", "") + " stock news"
            except:
                search_term = asset_id.replace(".NS", "").replace(".BO", "") + " stock news"
            
            print(f"[Scout Agent] [NEWS] Searching news for: {search_term}")
            search_result = search(search_term)
            
            if search_result and "news" in search_result:
                news_items = search_result.get("news", [])
                
                for item in news_items[:5]:
                    if isinstance(item, dict):
                        title = item.get("title", "")
                        link = item.get("link", "")
                        publisher = item.get("publisher", "Unknown")
                        published = item.get("providerPublishTime", "")
                        
                        # Convert timestamp if numeric
                        if isinstance(published, (int, float)):
                            try:
                                from datetime import datetime
                                published = datetime.fromtimestamp(published).isoformat()
                            except:
                                published = str(published)
                        
                        if title:
                            results.append({
                                "title": title,
                                "link": link,
                                "publisher": publisher,
                                "timestamp": published,
                                "source": "YahooQuery Search"
                            })
                
                if results:
                    print(f"[Scout Agent] [OK] Found {len(results)} news items via search")
                    return results
                    
        except Exception as e:
            print(f"[Scout Agent] [WARN] yahooquery search news failed: {e}")
        
        # Method 2: Try yahooquery Ticker.news() (sometimes works)
        try:
            from yahooquery import Ticker
            ticker = Ticker(asset_id)
            news_response = ticker.news()
            
            if isinstance(news_response, list) and news_response and news_response[0] != "error":
                for item in news_response[:5]:
                    if isinstance(item, dict):
                        title = item.get("title", "")
                        if title:
                            results.append({
                                "title": title,
                                "link": item.get("link", ""),
                                "publisher": item.get("publisher", "Unknown"),
                                "timestamp": str(item.get("providerPublishTime", "")),
                                "source": "YahooQuery Ticker"
                            })
                
                if results:
                    print(f"[Scout Agent] [OK] Found {len(results)} news items via Ticker.news()")
                    return results
                    
        except Exception as e:
            print(f"[Scout Agent] [WARN] yahooquery Ticker.news() failed: {e}")
        
        # Method 3: Try yfinance with rate limiting
        try:
            import yfinance as yf
            import time
            
            # Rate limiting: wait a bit to avoid hitting limits
            time.sleep(0.5)
            
            ticker = yf.Ticker(asset_id)
            yf_news = ticker.news
            
            if yf_news and isinstance(yf_news, list):
                for item in yf_news[:5]:
                    if isinstance(item, dict):
                        title = item.get("title", "")
                        if title:
                            results.append({
                                "title": title,
                                "link": item.get("link", ""),
                                "publisher": item.get("publisher", "Unknown"),
                                "timestamp": str(item.get("providerPublishTime", "")),
                                "source": "yfinance"
                            })
                
                if results:
                    print(f"[Scout Agent] [OK] Found {len(results)} news items via yfinance")
                    return results
                    
        except Exception as e:
            print(f"[Scout Agent] [WARN] yfinance news failed: {e}")
        
        # Method 4: Generate fallback news based on company info
        if not results:
            results = ScoutAgent._get_fallback_news(asset_id)
        
        return results if results else [{"title": f"No recent news found for {asset_id}", "link": "", "publisher": "", "timestamp": "", "source": "None"}]

    @staticmethod
    def _get_fallback_news(asset_id: str) -> List[Dict[str, str]]:
        """
        Generate intelligent fallback news based on company profile.
        """
        try:
            from yahooquery import Ticker
            ticker = Ticker(asset_id)
            profile = ticker.summary_profile.get(asset_id, {})
            
            if isinstance(profile, dict):
                sector = profile.get("sector", "the market")
                industry = profile.get("industry", "this sector")
                
                # Generate sector-relevant news placeholders
                return [
                    {
                        "title": f"Market Update: {sector} sector stocks in focus",
                        "link": "",
                        "publisher": "Market Analysis",
                        "timestamp": datetime.datetime.now().isoformat(),
                        "source": "Generated",
                        "note": "Auto-generated based on sector"
                    },
                    {
                        "title": f"Industry Watch: Latest trends in {industry}",
                        "link": "",
                        "publisher": "Industry Analysis",
                        "timestamp": datetime.datetime.now().isoformat(),
                        "source": "Generated",
                        "note": "Auto-generated based on industry"
                    }
                ]
        except:
            pass
        
        return []

    @staticmethod
    def _get_volatility_news(asset_id: str, query: str) -> List[Dict[str, str]]:
        """
        Search for news specifically related to price volatility events.
        Uses a more targeted search query.
        """
        results = []
        
        try:
            from yahooquery import search
            
            print(f"[Scout Agent] [SEARCH] Volatility news search: {query}")
            search_result = search(query)
            
            if search_result and "news" in search_result:
                news_items = search_result.get("news", [])
                
                for item in news_items[:3]:  # Get top 3 volatility-related
                    if isinstance(item, dict):
                        title = item.get("title", "")
                        link = item.get("link", "")
                        publisher = item.get("publisher", "Unknown")
                        published = item.get("providerPublishTime", "")
                        
                        # Convert timestamp if numeric
                        if isinstance(published, (int, float)):
                            try:
                                from datetime import datetime
                                published = datetime.fromtimestamp(published).isoformat()
                            except:
                                published = str(published)
                        
                        if title:
                            results.append({
                                "title": title,
                                "link": link,
                                "publisher": publisher,
                                "timestamp": published,
                                "source": "Volatility Search",
                                "priority": "HIGH",
                                "reason": "Related to significant price movement"
                            })
                
                if results:
                    print(f"[Scout Agent] [OK] Found {len(results)} volatility-related news items")
                    
        except Exception as e:
            print(f"[Scout Agent] [WARN] Volatility news search failed: {e}")
        
        return results

    @staticmethod
    def _safe_round(value, decimals: int = 2):
        """
        Safely round a value, returning None if invalid.
        """
        if value is None:
            return None
        try:
            return round(float(value), decimals)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _calculate_rsi_from_history(history: list, period: int = 14) -> float:
        """Calculate RSI from price history list."""
        if len(history) < period + 1:
            return None
        
        try:
            prices = [h.get("Close") or h.get("close", 0) for h in history[-period-1:]]
            deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
            
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            
            avg_gain = sum(gains) / period
            avg_loss = sum(losses) / period
            
            if avg_loss == 0:
                return 100.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return round(rsi, 2)
        except:
            return None
    
    @staticmethod
    def _calculate_trend_from_history(history: list) -> str:
        """Determine trend signal from price history."""
        if len(history) < 20:
            return "Insufficient Data"
        
        try:
            recent = [h.get("Close") or h.get("close", 0) for h in history[-20:]]
            older = [h.get("Close") or h.get("close", 0) for h in history[-40:-20]] if len(history) >= 40 else recent
            
            recent_avg = sum(recent) / len(recent)
            older_avg = sum(older) / len(older)
            
            change = ((recent_avg - older_avg) / older_avg) * 100 if older_avg else 0
            
            if change > 10:
                return "Strong Uptrend (Bullish)"
            elif change > 3:
                return "Uptrend (Bullish)"
            elif change < -10:
                return "Strong Downtrend (Bearish)"
            elif change < -3:
                return "Downtrend (Bearish)"
            else:
                return "Neutral (Sideways)"
        except:
            return "Unknown"

    @staticmethod
    def _get_demo_company_data() -> Dict[str, Any]:
        """Mock data for DEMO.NS - safe company for presentations."""
        import random
        
        # Generate realistic price history
        base_price = 1250.00
        history = []
        for i in range(90):
            date = (datetime.datetime.now() - datetime.timedelta(days=90-i)).strftime("%Y-%m-%d")
            variation = random.uniform(-2, 2.5)
            price = base_price * (1 + (i * 0.002) + (variation / 100))
            history.append({"date": date, "close": round(price, 2)})
        
        current_price = history[-1]["close"] if history else 1350.00
        
        financials = {
            "source": "Demo Data",
            "symbol": "RELIANCE.NS",
            "company_name": "Reliance Industries Limited",
            "sector": "Energy",
            "industry": "Oil & Gas Refining",
            "current_price": current_price,
            "currency": "INR",
            "market_cap": 1800000000000,  # 18,00,000 Cr
            "52_week_high": current_price * 1.12,
            "52_week_low": current_price * 0.82,
            "pe_ratio": 24.8,
            "pb_ratio": 2.1,
            "roe": 9.5,
            "debt_to_equity": 0.42,
            "dividend_yield": 0.35,
            "eps": current_price / 24.8,
            "revenue_growth": 12.5,
            "profit_margin": 8.2,
            "operating_margin": 14.0,
            "summary": "Reliance Industries Limited is India's largest private sector company. It operates across energy, petrochemicals, retail, and telecommunications (Jio). Mukesh Ambani serves as Chairman. The company has a diversified business model with strong cash flows."
        }
        
        technicals = {
            "history": history,
            "current_price": current_price,
            "sma_50": current_price * 0.98,
            "sma_200": current_price * 0.92,
            "rsi_14": 58.5,
            "trend_signal": "Uptrend (Bullish)",
            "support": current_price * 0.95,
            "resistance": current_price * 1.05
        }
        
        macro = {
            "vix": 14.5,
            "nifty_trend": "Bullish",
            "interest_rate": 6.5,
            "inflation": 5.2,
            "global_sentiment": "Cautiously Optimistic"
        }
        
        news = [
            {"title": "Reliance Jio adds 5 million subscribers in December", "publisher": "Economic Times", "date": "2025-01-05"},
            {"title": "Reliance Retail expansion: 500 new stores planned", "publisher": "Moneycontrol", "date": "2025-01-03"},
            {"title": "Mukesh Ambani announces green energy investment of $10 billion", "publisher": "Business Standard", "date": "2025-01-01"}
        ]
        
        return {
            "financials": financials,
            "technicals": technicals,
            "macro": macro,
            "news": news,
            "anomalies": [],
            "sanity_alerts": []
        }


scout_agent = ScoutAgent()

