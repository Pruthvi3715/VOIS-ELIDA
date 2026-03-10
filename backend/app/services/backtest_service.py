"""
Backtest Service for ELIDA
Tests the system's predictions against historical stock performance.
Uses heuristic/rule-based agent analysis (no LLM calls) for speed and reproducibility.
"""
import json
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

from app.services.score_labels import get_score_label
from app.services.match_score_service import match_score_service
from app.models.investor_dna import DEFAULT_INVESTOR_DNA, InvestorDNA
from app.core.logging import get_logger

logger = get_logger("backtest")


@dataclass
class BacktestPrediction:
    """A single prediction made by the system."""
    ticker: str
    date: str
    match_score: int
    score_label: str
    verdict: str        # Buy / Hold / Sell / Avoid
    confidence: int
    quant_score: int
    macro_score: int
    risk_score: int
    philosophy_score: int
    
    # Actual outcomes (filled after checking)
    price_at_prediction: float = 0.0
    price_after_30d: float = 0.0
    price_after_90d: float = 0.0
    return_30d: float = 0.0
    return_90d: float = 0.0
    correct_30d: bool = False
    correct_90d: bool = False


@dataclass
class BacktestSummary:
    """Summary statistics for a backtest run."""
    total_predictions: int = 0
    tickers_tested: List[str] = field(default_factory=list)
    date_range: str = ""
    
    # Hit rates
    hit_rate_30d: float = 0.0
    hit_rate_90d: float = 0.0
    
    # Precision by verdict
    buy_precision_30d: float = 0.0
    buy_precision_90d: float = 0.0
    sell_precision_30d: float = 0.0
    sell_precision_90d: float = 0.0
    
    # Returns
    avg_return_buys_30d: float = 0.0
    avg_return_buys_90d: float = 0.0
    avg_return_sells_30d: float = 0.0
    avg_return_sells_90d: float = 0.0
    avg_return_holds_30d: float = 0.0
    avg_return_holds_90d: float = 0.0
    
    # Score correlation
    score_return_correlation_30d: float = 0.0
    score_return_correlation_90d: float = 0.0
    
    # System grade
    system_grade: str = ""
    system_verdict: str = ""
    
    predictions: List[Dict] = field(default_factory=list)


class BacktestService:
    """
    Core backtesting engine.
    Analyzes stocks at historical dates and compares predictions vs actual outcomes.
    """

    def __init__(self):
        self._yahooquery_available = True
        try:
            from yahooquery import Ticker
        except ImportError:
            self._yahooquery_available = False
            logger.warning("yahooquery not installed — backtesting will not work")
    
    def run_backtest(
        self,
        tickers: List[str],
        start_date: str,
        end_date: Optional[str] = None,
        interval_months: int = 3,
        investor_dna: Optional[InvestorDNA] = None,
        forward_days: List[int] = None,
    ) -> BacktestSummary:
        """
        Run a full backtest.

        Args:
            tickers: List of stock tickers (e.g. ["TCS.NS", "RELIANCE.NS"])
            start_date: Start date for backtest (YYYY-MM-DD)
            end_date: End date (default: 90 days ago to allow forward checking)
            interval_months: Months between test points
            investor_dna: Investor profile (default used if None)
            forward_days: Days to check forward returns (default: [30, 90])
        """
        if not self._yahooquery_available:
            raise RuntimeError("yahooquery is required for backtesting. Install with: pip install yahooquery")
        
        if forward_days is None:
            forward_days = [30, 90]
        
        if investor_dna is None:
            investor_dna = DEFAULT_INVESTOR_DNA
        
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            # Default: 90 days ago to allow 90-day forward checking
            end = datetime.now() - timedelta(days=91)
        
        # Generate test dates
        test_dates = []
        current = start
        while current <= end:
            test_dates.append(current)
            current += timedelta(days=interval_months * 30)
        
        if not test_dates:
            test_dates = [start]
        
        logger.info(f"Backtesting {len(tickers)} tickers × {len(test_dates)} dates = {len(tickers) * len(test_dates)} predictions")
        
        # Run predictions
        predictions: List[BacktestPrediction] = []
        
        for ticker in tickers:
            logger.info(f"--- Backtesting {ticker} ---")
            for test_date in test_dates:
                try:
                    pred = self._analyze_at_date(ticker, test_date, investor_dna, forward_days)
                    if pred:
                        predictions.append(pred)
                        logger.info(
                            f"  {test_date.strftime('%Y-%m-%d')} | Score={pred.match_score} ({pred.score_label}) | "
                            f"Verdict={pred.verdict} | 30d={pred.return_30d:+.1f}% | 90d={pred.return_90d:+.1f}% | "
                            f"{'✅' if pred.correct_30d else '❌'}(30d) {'✅' if pred.correct_90d else '❌'}(90d)"
                        )
                except Exception as e:
                    logger.error(f"  {test_date.strftime('%Y-%m-%d')} | FAILED: {e}")
        
        # Calculate summary statistics
        summary = self._calculate_summary(predictions, tickers, start_date, end_date or end.strftime("%Y-%m-%d"))
        
        return summary
    
    def _analyze_at_date(
        self,
        ticker: str,
        analysis_date: datetime,
        investor_dna: InvestorDNA,
        forward_days: List[int]
    ) -> Optional[BacktestPrediction]:
        """
        Analyze a stock using data available at a specific historical date.
        Uses rule-based analysis (no LLM) for speed and reproducibility.
        """
        from yahooquery import Ticker as YQTicker
        
        yq = YQTicker(ticker)
        
        # 1. Get historical price data around the analysis date
        hist_start = (analysis_date - timedelta(days=365)).strftime("%Y-%m-%d")
        hist_end = (analysis_date + timedelta(days=max(forward_days) + 10)).strftime("%Y-%m-%d")
        
        history = yq.history(start=hist_start, end=hist_end)
        
        if history is None or (hasattr(history, 'empty') and history.empty):
            logger.warning(f"No history data for {ticker}")
            return None
        
        # Handle multi-index DataFrame
        if hasattr(history.index, 'names') and 'symbol' in history.index.names:
            history = history.reset_index()
            history = history[history['symbol'] == ticker]
        
        if 'date' not in history.columns:
            history = history.reset_index()
        
        # Ensure date column is datetime
        history['date'] = history['date'].apply(lambda x: x if isinstance(x, datetime) else datetime.combine(x, datetime.min.time()) if hasattr(x, 'year') else datetime.strptime(str(x)[:10], "%Y-%m-%d"))
        
        # Find price at analysis date (closest available)
        pre_date_prices = history[history['date'] <= analysis_date]
        if pre_date_prices.empty:
            logger.warning(f"No price data at {analysis_date.strftime('%Y-%m-%d')} for {ticker}")
            return None
        
        price_at_prediction = float(pre_date_prices.iloc[-1]['close'])
        
        # 2. Get financials (using yahooquery — these are point-in-time enough for backtesting)
        financials = self._get_historical_financials(yq, ticker)
        
        # 3. Calculate technical indicators from historical prices up to analysis_date
        technicals = self._calculate_technicals(pre_date_prices)
        
        # 4. Run heuristic agent analysis
        agent_results = self._run_heuristic_agents(financials, technicals)
        
        # 5. Calculate match score
        asset_data = {"financials": financials, "technicals": technicals}
        match_result = match_score_service.calculate_match_score(
            agent_results=agent_results,
            asset_data=asset_data,
            investor_dna=investor_dna
        )
        
        # 6. Determine verdict
        verdict = match_result.recommendation
        
        # 7. Calculate actual forward returns
        return_30d = 0.0
        return_90d = 0.0
        price_30d = price_at_prediction
        price_90d = price_at_prediction
        
        for days in forward_days:
            target_date = analysis_date + timedelta(days=days)
            post_prices = history[
                (history['date'] >= target_date - timedelta(days=5)) &
                (history['date'] <= target_date + timedelta(days=5))
            ]
            
            if not post_prices.empty:
                future_price = float(post_prices.iloc[0]['close'])
                pct_return = ((future_price - price_at_prediction) / price_at_prediction) * 100
                
                if days == 30:
                    return_30d = round(pct_return, 2)
                    price_30d = future_price
                elif days == 90:
                    return_90d = round(pct_return, 2)
                    price_90d = future_price
        
        # 8. Determine correctness
        correct_30d = self._is_correct(verdict, return_30d)
        correct_90d = self._is_correct(verdict, return_90d)
        
        label_info = get_score_label(match_result.match_score)
        
        return BacktestPrediction(
            ticker=ticker,
            date=analysis_date.strftime("%Y-%m-%d"),
            match_score=match_result.match_score,
            score_label=label_info["label"],
            verdict=verdict,
            confidence=agent_results.get("quant", {}).get("confidence", 50),
            quant_score=int(self._extract_agent_score(agent_results.get("quant", {}))),
            macro_score=int(self._extract_agent_score(agent_results.get("macro", {}))),
            risk_score=int(self._extract_agent_score(agent_results.get("regret", {}))),
            philosophy_score=int(self._extract_agent_score(agent_results.get("philosopher", {}))),
            price_at_prediction=round(price_at_prediction, 2),
            price_after_30d=round(price_30d, 2),
            price_after_90d=round(price_90d, 2),
            return_30d=return_30d,
            return_90d=return_90d,
            correct_30d=correct_30d,
            correct_90d=correct_90d,
        )
    
    def _extract_agent_score(self, result: Dict) -> float:
        """Extract score from agent result dict."""
        if "output" in result:
            return float(result.get("output", {}).get("score", 50))
        return float(result.get("score", 50))
    
    def _get_historical_financials(self, yq_ticker, ticker: str) -> Dict:
        """Get financial data from yahooquery."""
        try:
            summary = yq_ticker.summary_detail.get(ticker, {})
            key_stats = yq_ticker.key_stats.get(ticker, {})
            profile = yq_ticker.asset_profile.get(ticker, {})
            
            if isinstance(summary, str) or isinstance(key_stats, str):
                return {"symbol": ticker}
            
            return {
                "symbol": ticker,
                "company_name": profile.get("shortName", ticker) if isinstance(profile, dict) else ticker,
                "sector": profile.get("sector", "Unknown") if isinstance(profile, dict) else "Unknown",
                "industry": profile.get("industry", "Unknown") if isinstance(profile, dict) else "Unknown",
                "pe_ratio": summary.get("trailingPE") if isinstance(summary, dict) else None,
                "forward_pe": summary.get("forwardPE") if isinstance(summary, dict) else None,
                "peg_ratio": key_stats.get("pegRatio") if isinstance(key_stats, dict) else None,
                "profit_margins": key_stats.get("profitMargins") if isinstance(key_stats, dict) else None,
                "return_on_equity": key_stats.get("returnOnEquity") if isinstance(key_stats, dict) else None,
                "debt_to_equity": key_stats.get("debtToEquity") if isinstance(key_stats, dict) else None,
                "revenue_growth": key_stats.get("revenueGrowth") if isinstance(key_stats, dict) else None,
                "dividend_yield": summary.get("dividendYield") if isinstance(summary, dict) else None,
                "market_cap": self._format_market_cap(summary.get("marketCap")) if isinstance(summary, dict) else None,
                "current_price": summary.get("previousClose") if isinstance(summary, dict) else None,
            }
        except Exception as e:
            logger.error(f"Failed to get financials for {ticker}: {e}")
            return {"symbol": ticker}
    
    def _format_market_cap(self, mc) -> Optional[str]:
        """Format market cap to human-readable string."""
        if mc is None:
            return None
        try:
            mc = float(mc)
            if mc >= 1e12:
                return f"{mc/1e12:.2f}T"
            elif mc >= 1e9:
                return f"{mc/1e9:.2f}B"
            elif mc >= 1e6:
                return f"{mc/1e6:.2f}M"
            return str(mc)
        except (TypeError, ValueError):
            return None
    
    def _calculate_technicals(self, price_history) -> Dict:
        """Calculate basic technical indicators from price history."""
        try:
            closes = price_history['close'].values
            if len(closes) < 14:
                return {}
            
            # RSI (14-period)
            deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            
            avg_gain = sum(gains[-14:]) / 14
            avg_loss = sum(losses[-14:]) / 14
            
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            
            # Simple moving averages
            current_price = float(closes[-1])
            sma_20 = float(sum(closes[-20:])) / min(20, len(closes)) if len(closes) >= 20 else current_price
            sma_50 = float(sum(closes[-50:])) / min(50, len(closes)) if len(closes) >= 50 else current_price
            
            # 52-week high/low
            year_closes = closes[-252:] if len(closes) >= 252 else closes
            high_52w = float(max(year_closes))
            low_52w = float(min(year_closes))
            pct_from_high = ((current_price - high_52w) / high_52w) * 100 if high_52w > 0 else 0
            
            # Volatility (30-day std)
            if len(closes) >= 30:
                returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(-30, 0) if closes[i-1] > 0]
                volatility = (sum(r**2 for r in returns) / len(returns)) ** 0.5 if returns else 0.2
            else:
                volatility = 0.2
            
            # Trend signal
            if current_price > sma_20 > sma_50:
                trend = "Bullish Uptrend"
            elif current_price < sma_20 < sma_50:
                trend = "Bearish Downtrend"
            else:
                trend = "Neutral"
            
            return {
                "rsi_14": round(rsi, 2),
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2),
                "current_price": round(current_price, 2),
                "52w_high": round(high_52w, 2),
                "52w_low": round(low_52w, 2),
                "pct_from_52w_high": round(pct_from_high, 2),
                "volatility_raw": round(volatility, 4),
                "trend_signal": trend,
            }
        except Exception as e:
            logger.error(f"Technical calculation error: {e}")
            return {}
    
    def _run_heuristic_agents(self, financials: Dict, technicals: Dict) -> Dict[str, Any]:
        """
        Run lightweight heuristic analysis for each agent role.
        No LLM calls — pure rule-based for speed and reproducibility.
        v2: Wider score adjustments + momentum overlay for better differentiation.
        """
        quant_score = self._heuristic_quant(financials, technicals)
        macro_score = self._heuristic_macro(technicals)
        risk_score = self._heuristic_risk(financials, technicals)
        philosophy_score = self._heuristic_philosophy(financials)
        
        # Momentum overlay: adjust macro score more aggressively based on trend
        momentum_adj = self._momentum_overlay(technicals)
        macro_score = max(0, min(100, macro_score + momentum_adj))
        
        return {
            "quant": {"score": quant_score, "output": {"score": quant_score}},
            "macro": {"score": macro_score, "output": {"score": macro_score, "trend": technicals.get("trend_signal", "Neutral")}},
            "regret": {"score": risk_score, "output": {"score": risk_score, "risk_level": "Medium"}},
            "philosopher": {"score": philosophy_score, "output": {"score": philosophy_score, "alignment": "Medium"}},
        }
    
    def _momentum_overlay(self, technicals: Dict) -> int:
        """
        v2 NEW: Momentum adjustment based on price action.
        Returns adjustment value (-20 to +20) applied to macro score.
        """
        adj = 0
        
        rsi = technicals.get("rsi_14")
        trend = technicals.get("trend_signal", "")
        pct_from_high = technicals.get("pct_from_52w_high", 0)
        
        # Strong momentum combos
        if isinstance(rsi, (int, float)):
            if rsi > 65 and "Bullish" in trend:
                adj += 12   # Strong uptrend momentum
            elif rsi < 35 and "Bearish" in trend:
                adj -= 12   # Strong downtrend momentum
            elif rsi > 75:
                adj -= 8    # Overbought risk even in uptrend
            elif rsi < 25:
                adj += 8    # Deeply oversold = contrarian opportunity
        
        # Price distance from 52w high
        if isinstance(pct_from_high, (int, float)):
            if pct_from_high > -3:
                adj -= 10   # At highs — risky timing
            elif pct_from_high < -25:
                adj += 8    # Deep discount from highs
            elif pct_from_high < -15:
                adj += 3    # Moderate discount
        
        return max(-20, min(20, adj))
    
    def _heuristic_quant(self, data: Dict, technicals: Dict = None) -> int:
        """
        Rule-based Quant Agent scoring.
        v2: Wider adjustments, momentum-aware valuation.
        """
        score = 45  # Start below neutral — must earn score
        
        # P/E ratio — wider bands
        pe = data.get("pe_ratio")
        if isinstance(pe, (int, float)) and pe > 0:
            if pe < 12: score += 20      # Deep value
            elif pe < 18: score += 12    # Reasonable value
            elif pe < 25: score += 3     # Fair
            elif pe < 35: score -= 10    # Expensive
            elif pe < 50: score -= 18    # Very expensive
            else: score -= 25           # Bubble territory
        
        # Forward P/E — growth-adjusted signal
        fpe = data.get("forward_pe")
        if isinstance(fpe, (int, float)) and fpe > 0:
            if fpe < 15: score += 12
            elif fpe < 22: score += 5
            elif fpe > 35: score -= 12
            elif fpe > 50: score -= 20
        
        # P/E to Forward P/E trend (improving or worsening)
        if isinstance(pe, (int, float)) and isinstance(fpe, (int, float)) and pe > 0 and fpe > 0:
            if fpe < pe * 0.85: score += 8   # Earnings expected to grow (fwd PE is lower)
            elif fpe > pe * 1.2: score -= 8  # Earnings expected to shrink
        
        # Profit margins — wider bands
        margins = data.get("profit_margins")
        if isinstance(margins, (int, float)):
            if margins > 0.20: score += 15   # Excellent margins
            elif margins > 0.12: score += 8
            elif margins > 0.05: score += 2
            elif margins > 0: score -= 8
            else: score -= 18               # Loss-making
        
        # ROE — wider bands  
        roe = data.get("return_on_equity")
        if isinstance(roe, (int, float)):
            if roe > 0.25: score += 15       # Exceptional
            elif roe > 0.15: score += 10
            elif roe > 0.10: score += 3
            elif roe > 0.05: score -= 5
            else: score -= 12               # Poor capital efficiency
        
        # Debt — wider penalties
        dte = data.get("debt_to_equity")
        if isinstance(dte, (int, float)):
            if dte < 20: score += 10
            elif dte < 50: score += 5
            elif dte > 150: score -= 15
            elif dte > 100: score -= 10
            if dte > 250: score -= 20       # Danger zone
        
        # PEG ratio
        peg = data.get("peg_ratio")
        if isinstance(peg, (int, float)) and peg > 0:
            if peg < 0.8: score += 15
            elif peg < 1.0: score += 10
            elif peg < 1.5: score += 3
            elif peg > 2.5: score -= 12
            elif peg > 2: score -= 5
        
        # Revenue growth signal
        rg = data.get("revenue_growth")
        if isinstance(rg, (int, float)):
            if rg > 0.20: score += 10
            elif rg > 0.10: score += 5
            elif rg < -0.05: score -= 10
            elif rg < 0: score -= 5
        
        return max(0, min(100, score))
    
    def _heuristic_macro(self, technicals: Dict) -> int:
        """
        Rule-based Macro Agent scoring based on technicals.
        v2: Stronger trend signal, RSI extremes, SMA position.
        """
        score = 45  # Start below neutral
        
        # Trend signal — highest weight
        trend = technicals.get("trend_signal", "")
        if "Bullish" in trend: score += 20
        elif "Bearish" in trend: score -= 20
        
        # RSI signal — wider bands
        rsi = technicals.get("rsi_14")
        if isinstance(rsi, (int, float)):
            if rsi < 25: score += 15       # Deeply oversold
            elif rsi < 35: score += 8      # Oversold  
            elif rsi > 75: score -= 15     # Overbought
            elif rsi > 65: score -= 5      # Getting hot
            elif 40 <= rsi <= 60: score += 5  # Healthy middle
        
        # 52w position — critical timing signal
        pct_from_high = technicals.get("pct_from_52w_high", 0)
        if isinstance(pct_from_high, (int, float)):
            if pct_from_high < -40: score += 15    # Deeply discounted
            elif pct_from_high < -25: score += 10  # Significant discount
            elif pct_from_high < -15: score += 5   # Moderate discount
            elif pct_from_high > -3: score -= 12   # At all-time highs
            elif pct_from_high > -8: score -= 5    # Near highs
        
        # SMA position — price vs moving averages
        price = technicals.get("current_price", 0)
        sma_20 = technicals.get("sma_20", 0)
        sma_50 = technicals.get("sma_50", 0)
        if price and sma_20 and sma_50:
            # Price above both SMAs = strong
            if price > sma_20 > sma_50:
                score += 8
            # Price below both SMAs = weak
            elif price < sma_20 < sma_50:
                score -= 8
            # Golden cross potential (SMA20 > SMA50 but price dipped)
            elif sma_20 > sma_50 and price < sma_20:
                score += 3  # Potential dip-buy
        
        return max(0, min(100, score))
    
    def _heuristic_risk(self, financials: Dict, technicals: Dict) -> int:
        """
        Rule-based Risk/Regret Agent scoring. Higher = less risky.
        v2: Start at 50 (not 60), heavier volatility & drawdown penalties.
        """
        score = 50  # Neutral start — must earn safety score
        
        # Debt risk — primary financial risk
        dte = financials.get("debt_to_equity")
        if isinstance(dte, (int, float)):
            if dte < 20: score += 18       # Very low debt
            elif dte < 50: score += 10
            elif dte > 150: score -= 22    # Dangerous
            elif dte > 100: score -= 15
        
        # Profitability buffer
        margins = financials.get("profit_margins")
        if isinstance(margins, (int, float)):
            if margins > 0.15: score += 12
            elif margins > 0.08: score += 5
            elif margins < 0: score -= 25  # Loss-making is very risky
            elif margins < 0.03: score -= 10
        
        # Volatility — heavy weight in risk scoring
        volatility = technicals.get("volatility_raw", 0.02)
        if isinstance(volatility, (int, float)):
            if volatility > 0.04: score -= 22    # Very high volatility
            elif volatility > 0.03: score -= 15
            elif volatility > 0.02: score -= 5
            elif volatility < 0.012: score += 12  # Very stable
            elif volatility < 0.018: score += 5
        
        # Drawdown risk — distance from 52w high
        pct_from_high = technicals.get("pct_from_52w_high", 0)
        if isinstance(pct_from_high, (int, float)):
            if pct_from_high < -30: score -= 12    # Already in big drawdown
            elif pct_from_high < -20: score -= 5
            elif pct_from_high > -5: score -= 5    # Near highs = downside risk
        
        # Market cap = stability
        mc = str(financials.get("market_cap", ""))
        if "T" in mc: score += 12
        elif "B" in mc:
            try:
                val = float(mc.replace("B", "").replace(",", ""))
                if val > 100: score += 8
                elif val > 50: score += 5
            except:
                pass
        
        return max(0, min(100, score))
    
    def _heuristic_philosophy(self, financials: Dict) -> int:
        """
        Rule-based Philosophy Agent scoring.
        v2: Start at 45 (not 55), wider adjustments for growth/quality.
        """
        score = 45  # Start below neutral — must earn quality score
        
        # Market cap = established business quality
        mc = str(financials.get("market_cap", ""))
        if "T" in mc: score += 18
        elif "B" in mc:
            try:
                val = float(mc.replace("B", "").replace(",", ""))
                if val > 100: score += 14
                elif val > 50: score += 10
                elif val > 10: score += 5
                else: score += 2
            except:
                pass
        
        # Revenue growth — ambition signal
        rg = financials.get("revenue_growth")
        if isinstance(rg, (int, float)):
            if rg > 0.20: score += 15      # High growth
            elif rg > 0.10: score += 10
            elif rg > 0.05: score += 3
            elif rg < -0.05: score -= 15   # Shrinking business
            elif rg < 0: score -= 8
        
        # Profitability = sustainable business model
        margins = financials.get("profit_margins")
        if isinstance(margins, (int, float)):
            if margins > 0.20: score += 15
            elif margins > 0.10: score += 10
            elif margins > 0.05: score += 3
            elif margins < 0: score -= 20  # Unsustainable
            elif margins < 0.03: score -= 8
        
        # ROE — management quality 
        roe = financials.get("return_on_equity")
        if isinstance(roe, (int, float)):
            if roe > 0.20: score += 10
            elif roe > 0.12: score += 5
            elif roe < 0.05: score -= 8
        
        # Dividend — shareholder friendliness
        div_yield = financials.get("dividend_yield")
        if isinstance(div_yield, (int, float)):
            if div_yield > 0.03: score += 5
            elif div_yield > 0.01: score += 2
        
        return max(0, min(100, score))
    
    def _is_correct(self, verdict: str, actual_return: float) -> bool:
        """Check if prediction was correct based on actual return."""
        v = verdict.lower()
        if v in ("buy", "add more"):
            return actual_return > 0
        elif v in ("sell", "avoid", "reduce", "exit", "don't add"):
            return actual_return <= 0
        else:  # Hold / Wait / Consider
            return abs(actual_return) < 10  # Hold is correct if price didn't move much
    
    def _calculate_summary(
        self,
        predictions: List[BacktestPrediction],
        tickers: List[str],
        start_date: str,
        end_date: str
    ) -> BacktestSummary:
        """Calculate summary statistics from all predictions."""
        summary = BacktestSummary(
            total_predictions=len(predictions),
            tickers_tested=tickers,
            date_range=f"{start_date} to {end_date}",
            predictions=[asdict(p) for p in predictions],
        )
        
        if not predictions:
            summary.system_grade = "N/A"
            summary.system_verdict = "No predictions could be generated"
            return summary
        
        # Hit rates
        correct_30d = sum(1 for p in predictions if p.correct_30d)
        correct_90d = sum(1 for p in predictions if p.correct_90d)
        summary.hit_rate_30d = round((correct_30d / len(predictions)) * 100, 1)
        summary.hit_rate_90d = round((correct_90d / len(predictions)) * 100, 1)
        
        # Precision by verdict type
        buys = [p for p in predictions if p.verdict.lower() in ("buy", "add more")]
        sells = [p for p in predictions if p.verdict.lower() in ("sell", "avoid", "reduce", "exit", "don't add")]
        holds = [p for p in predictions if p.verdict.lower() in ("hold", "wait", "consider")]
        
        if buys:
            summary.buy_precision_30d = round(sum(1 for p in buys if p.return_30d > 0) / len(buys) * 100, 1)
            summary.buy_precision_90d = round(sum(1 for p in buys if p.return_90d > 0) / len(buys) * 100, 1)
            summary.avg_return_buys_30d = round(sum(p.return_30d for p in buys) / len(buys), 2)
            summary.avg_return_buys_90d = round(sum(p.return_90d for p in buys) / len(buys), 2)
        
        if sells:
            summary.sell_precision_30d = round(sum(1 for p in sells if p.return_30d <= 0) / len(sells) * 100, 1)
            summary.sell_precision_90d = round(sum(1 for p in sells if p.return_90d <= 0) / len(sells) * 100, 1)
            summary.avg_return_sells_30d = round(sum(p.return_30d for p in sells) / len(sells), 2)
            summary.avg_return_sells_90d = round(sum(p.return_90d for p in sells) / len(sells), 2)
        
        if holds:
            summary.avg_return_holds_30d = round(sum(p.return_30d for p in holds) / len(holds), 2)
            summary.avg_return_holds_90d = round(sum(p.return_90d for p in holds) / len(holds), 2)
        
        # Score-return correlation (Pearson simplified)
        if len(predictions) >= 3:
            scores = [p.match_score for p in predictions]
            returns_30 = [p.return_30d for p in predictions]
            returns_90 = [p.return_90d for p in predictions]
            
            summary.score_return_correlation_30d = round(self._pearson(scores, returns_30), 3)
            summary.score_return_correlation_90d = round(self._pearson(scores, returns_90), 3)
        
        # System grade
        avg_hit = (summary.hit_rate_30d + summary.hit_rate_90d) / 2
        if avg_hit >= 70:
            summary.system_grade = "A+ (Excellent)"
            summary.system_verdict = "System shows strong predictive capability"
        elif avg_hit >= 60:
            summary.system_grade = "A (Good)"
            summary.system_verdict = "System predictions are reliable above average"
        elif avg_hit >= 55:
            summary.system_grade = "B (Decent)"
            summary.system_verdict = "System is slightly better than random, useful as a signal"
        elif avg_hit >= 50:
            summary.system_grade = "C (Marginal)"
            summary.system_verdict = "System is at coin-flip level, needs improvement"
        else:
            summary.system_grade = "D (Poor)"
            summary.system_verdict = "System is worse than random, contrarian use may work"
        
        return summary
    
    def _pearson(self, x: list, y: list) -> float:
        """Simple Pearson correlation coefficient."""
        n = len(x)
        if n < 3:
            return 0.0
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = (sum((xi - mean_x) ** 2 for xi in x)) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y)) ** 0.5
        
        if std_x == 0 or std_y == 0:
            return 0.0
        
        return cov / (std_x * std_y)
    
    def format_results_table(self, summary: BacktestSummary) -> str:
        """Format backtest results as a readable table."""
        lines = []
        lines.append("=" * 90)
        lines.append("  ELIDA BACKTEST RESULTS")
        lines.append("=" * 90)
        lines.append(f"  Tickers: {', '.join(summary.tickers_tested)}")
        lines.append(f"  Date Range: {summary.date_range}")
        lines.append(f"  Total Predictions: {summary.total_predictions}")
        lines.append("")
        
        # Prediction details table
        lines.append(f"  {'Ticker':<14} {'Date':<12} {'Score':<6} {'Label':<14} {'Verdict':<8} {'30d %':<8} {'90d %':<8} {'30d':>4} {'90d':>4}")
        lines.append("  " + "-" * 86)
        
        for p in summary.predictions:
            c30 = "✅" if p["correct_30d"] else "❌"
            c90 = "✅" if p["correct_90d"] else "❌"
            lines.append(
                f"  {p['ticker']:<14} {p['date']:<12} {p['match_score']:<6} {p['score_label']:<14} "
                f"{p['verdict']:<8} {p['return_30d']:>+7.1f}% {p['return_90d']:>+7.1f}% {c30:>4} {c90:>4}"
            )
        
        lines.append("")
        lines.append("  SUMMARY STATISTICS")
        lines.append("  " + "-" * 40)
        lines.append(f"  Hit Rate (30d):      {summary.hit_rate_30d}%")
        lines.append(f"  Hit Rate (90d):      {summary.hit_rate_90d}%")
        lines.append(f"  Buy Precision (30d): {summary.buy_precision_30d}%")
        lines.append(f"  Buy Precision (90d): {summary.buy_precision_90d}%")
        lines.append(f"  Avg Return Buys 30d: {summary.avg_return_buys_30d:+.2f}%")
        lines.append(f"  Avg Return Buys 90d: {summary.avg_return_buys_90d:+.2f}%")
        lines.append(f"  Score↔Return Corr:   {summary.score_return_correlation_30d} (30d) | {summary.score_return_correlation_90d} (90d)")
        lines.append("")
        lines.append(f"  SYSTEM GRADE: {summary.system_grade}")
        lines.append(f"  VERDICT: {summary.system_verdict}")
        lines.append("=" * 90)
        
        return "\n".join(lines)
    
    def export_csv(self, summary: BacktestSummary) -> str:
        """Export predictions to CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "ticker", "date", "match_score", "score_label", "verdict", "confidence",
            "quant_score", "macro_score", "risk_score", "philosophy_score",
            "price_at_prediction", "price_after_30d", "price_after_90d",
            "return_30d", "return_90d", "correct_30d", "correct_90d"
        ])
        writer.writeheader()
        for p in summary.predictions:
            writer.writerow(p)
        return output.getvalue()


# Singleton
backtest_service = BacktestService()
