import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Search,
    Sparkles,
    Zap,
    Target,
    User,
    Clock,
    TrendingUp,
    TrendingDown
} from 'lucide-react';
import { API_BASE_URL, getUserId } from '../api';

function DashboardPage() {
    const navigate = useNavigate();
    const [searchTicker, setSearchTicker] = useState('');
    const [recentAnalyses, setRecentAnalyses] = useState([]);
    const [marketData, setMarketData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [watchedTickers, setWatchedTickers] = useState(() => {
        const saved = localStorage.getItem('watchedTickers');
        return saved ? JSON.parse(saved) : ['RELIANCE.NS', 'TCS.NS', 'AAPL'];
    });
    const [newTicker, setNewTicker] = useState('');
    const [agentStatus, setAgentStatus] = useState({ active: 4, total: 4 });

    // Fetch recent history on mount
    useEffect(() => {
        fetchRecentHistory();
        fetchMarketData();
        const interval = setInterval(fetchMarketData, 30000); // Poll every 30s
        return () => clearInterval(interval);
    }, [watchedTickers]);

    // Save watched tickers
    useEffect(() => {
        localStorage.setItem('watchedTickers', JSON.stringify(watchedTickers));
    }, [watchedTickers]);

    const fetchRecentHistory = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/history?limit=5`);
            const data = await response.json();
            const entries = data.entries || [];
            setRecentAnalyses(entries.slice(0, 5));
        } catch (error) {
            console.log('No recent history', error);
        }
    };

    const fetchMarketData = async () => {
        const results = [];
        for (const rawTicker of watchedTickers) {
            const ticker = rawTicker.trim().toUpperCase();
            try {
                const response = await fetch(`${API_BASE_URL}/market-data/${ticker}`);
                if (response.ok) {
                    const jsonData = await response.json();

                    // Handle multiple possible data structures:
                    // 1. Demo cache: returns flat {price, change, volume, currency, ...}
                    // 2. Scout agent: returns {financials: {...}, technicals: {...}, ...}
                    const data = jsonData.financials || jsonData;

                    // Currency detection - use ticker suffix as PRIMARY indicator (most reliable)
                    const isIndianStock = ticker.endsWith('.NS') || ticker.endsWith('.BO');
                    const currencySymbol = isIndianStock ? '\u20B9' : '$';

                    // Extract price - handle different field names
                    const price = data.current_price || data.price || 0;

                    // Extract change percentage
                    const change = data.price_change_percentage_24h || data.change_percent || data.pct_change || data.change || 0;

                    // Format volume
                    let formattedVolume = 'N/A';
                    if (data.volume && data.volume > 0) {
                        if (data.volume >= 1000000) {
                            formattedVolume = `${(data.volume / 1000000).toFixed(1)}M`;
                        } else if (data.volume >= 1000) {
                            formattedVolume = `${(data.volume / 1000).toFixed(1)}K`;
                        } else {
                            formattedVolume = data.volume.toString();
                        }
                    }

                    results.push({
                        ticker,
                        price: price,
                        change: change,
                        volume: formattedVolume,
                        currencySymbol,
                        name: data.company_name || data.name || ticker.replace('.NS', '').replace('.BO', '')
                    });
                } else {
                    throw new Error(`HTTP ${response.status}`);
                }
            } catch (e) {
                console.error(`Failed to fetch data for ${ticker}`, e);
                // Fallback for failed requests - use ticker-based currency detection
                const isIndianStock = ticker.endsWith('.NS') || ticker.endsWith('.BO');
                results.push({
                    ticker,
                    error: true,
                    price: 0,
                    change: 0,
                    volume: 'N/A',
                    currencySymbol: isIndianStock ? '\u20B9' : '$',
                    name: ticker.replace('.NS', '').replace('.BO', '')
                });
            }
        }
        setMarketData(results);
    };

    const addTicker = (e) => {
        e.preventDefault();
        if (newTicker && !watchedTickers.includes(newTicker.toUpperCase())) {
            setWatchedTickers([...watchedTickers, newTicker.toUpperCase()]);
            setNewTicker('');
        }
    };

    const removeTicker = (tickerToRemove) => {
        setWatchedTickers(watchedTickers.filter(t => t !== tickerToRemove));
    };

    const handleAnalyze = () => {
        if (searchTicker.trim()) {
            navigate(`/analysis/${searchTicker.trim().toUpperCase()}`);
        }
    };

    const currentTime = new Date().toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });

    return (
        <div className="space-y-6">
            {/* Investment Analysis Card */}
            <div className="glass-card rounded-xl border border-glass-border p-8 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-secondary-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="p-2 rounded-lg bg-surface-light border border-glass-border">
                            <Sparkles className="w-5 h-5 text-amber-400" />
                        </div>
                        <h2 className="text-xl font-bold text-white">Investment Analysis</h2>
                    </div>

                    <p className="text-secondary text-sm mb-6 max-w-2xl">
                        Get AI-powered investment recommendations using our multi-agent system.
                        Analyze stocks with Quant, Macro, and Fundamental perspectives.
                    </p>

                    <div className="flex gap-3 max-w-3xl">
                        <div className="flex-1 relative">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                type="text"
                                value={searchTicker}
                                onChange={(e) => setSearchTicker(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                                placeholder="Enter stock symbol (e.g., RELIANCE.NS, AAPL, TCS.NS)"
                                className="w-full pl-12 pr-4 py-4 bg-surface-light/50 border border-glass-border rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-primary-500/50 focus:ring-1 focus:ring-primary-500/50 transition-all font-medium"
                            />
                        </div>
                        <button
                            onClick={handleAnalyze}
                            disabled={!searchTicker.trim() || loading}
                            className="flex items-center gap-2 px-8 py-4 bg-gradient-primary text-white rounded-xl font-bold hover:shadow-glow hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                        >
                            {loading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <Zap className="w-5 h-5 fill-current" />}
                            Analyze
                        </button>
                    </div>
                </div>
            </div>

            {/* Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* AI Agents */}
                <div className="glass-card rounded-xl border border-glass-border p-5 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-3 opacity-10">
                        <Target className="w-16 h-16 text-primary-500" />
                    </div>
                    <p className="text-primary-400 text-sm font-semibold mb-1 uppercase tracking-wider">AI Agents</p>
                    <div className="flex items-end gap-2">
                        <p className="text-3xl font-bold text-white">{agentStatus.active}/{agentStatus.total}</p>
                        <span className="mb-1.5 w-2 h-2 rounded-full bg-success shadow-glow-sm animate-pulse" />
                    </div>
                    <p className="text-secondary/80 text-xs mt-1">Systems operational</p>
                </div>

                {/* Data Freshness */}
                <div className="glass-card rounded-xl border border-glass-border p-5 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-3 opacity-10">
                        <Clock className="w-16 h-16 text-success" />
                    </div>
                    <p className="text-success text-sm font-semibold mb-1 uppercase tracking-wider">Market Data</p>
                    <div className="flex items-end gap-2">
                        <p className="text-3xl font-bold text-white">Live</p>
                        <span className="mb-1.5 text-xs font-medium px-1.5 py-0.5 rounded bg-success/20 text-success border border-success/30">Real-time</span>
                    </div>
                    <p className="text-secondary/80 text-xs mt-1">Global coverage</p>
                </div>

                {/* Accuracy */}
                <div className="glass-card rounded-xl border border-glass-border p-5 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-3 opacity-10">
                        <Target className="w-16 h-16 text-amber-500" />
                    </div>
                    <p className="text-amber-500 text-sm font-semibold mb-1 uppercase tracking-wider">Accuracy</p>
                    <p className="text-3xl font-bold text-white">87%</p>
                    <p className="text-secondary/80 text-xs mt-1">Historical verification</p>
                </div>

                {/* Profile */}
                <div
                    onClick={() => navigate('/profile')}
                    className="glass-card rounded-xl border border-glass-border p-5 flex flex-col items-center justify-center cursor-pointer hover:bg-surface-light/30 transition-colors group"
                >
                    <div className="p-3 rounded-full bg-surface-light border border-glass-border mb-2 group-hover:border-primary-500/50 group-hover:scale-110 transition-all">
                        <User className="w-6 h-6 text-secondary group-hover:text-white" />
                    </div>
                    <p className="text-secondary text-sm font-medium group-hover:text-white transition-colors">Investor Profile</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Live Market Data */}
                <div className="lg:col-span-2 glass-card rounded-xl border border-glass-border p-6">
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                            <div className="relative">
                                <span className="flex h-3 w-3">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-3 w-3 bg-success"></span>
                                </span>
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-white">Live Market Watch</h3>
                                <p className="text-xs text-secondary">Track up to 3 stocks • Hover to remove</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <form onSubmit={addTicker} className="flex gap-2">
                                <input
                                    type="text"
                                    value={newTicker}
                                    onChange={(e) => setNewTicker(e.target.value)}
                                    placeholder="e.g., RELIANCE.NS, AAPL"
                                    className="w-44 px-3 py-1.5 bg-surface-light/50 border border-glass-border rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-primary-500/50 focus:ring-1 focus:ring-primary-500/30 transition-all"
                                />
                                <button
                                    type="submit"
                                    disabled={!newTicker || watchedTickers.length >= 6}
                                    className="px-4 py-1.5 bg-gradient-to-r from-primary-600 to-accent-dark text-white text-sm font-medium rounded-lg hover:shadow-glow transition disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    + Add
                                </button>
                            </form>
                            <span className="text-xs text-secondary font-mono bg-surface-light px-2 py-1 rounded border border-glass-border">{currentTime}</span>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {marketData.map((stock) => (
                            <div
                                key={stock.ticker}
                                className={`relative group p-4 rounded-xl border transition-all duration-300 ${stock.error
                                    ? 'bg-error/5 border-error/20 hover:border-error/40'
                                    : 'bg-surface-light/30 border-glass-border hover:bg-surface-light/50 hover:border-primary-500/30'
                                    }`}
                            >
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        removeTicker(stock.ticker);
                                    }}
                                    className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 p-1.5 hover:bg-error/20 rounded-lg text-gray-400 hover:text-error transition-all z-10"
                                    title="Remove from Watchlist"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18" /><path d="m6 6 12 12" /></svg>
                                </button>

                                <div
                                    onClick={() => navigate(`/analysis/${stock.ticker}`)}
                                    className="cursor-pointer"
                                >
                                    <div className="flex items-start justify-between mb-3">
                                        <div>
                                            <span className="font-bold text-white text-lg tracking-wide">{stock.ticker}</span>
                                            <p className="text-[10px] text-secondary uppercase tracking-wider">
                                                {stock.error ? 'Data unavailable' : (stock.name && stock.name !== stock.ticker ? stock.name.slice(0, 15) + (stock.name.length > 15 ? '...' : '') : 'Stock')}
                                            </p>
                                        </div>
                                        <div className={`px-2 py-1 rounded-lg text-xs font-bold ${stock.error
                                            ? 'bg-warning/10 text-warning border border-warning/20'
                                            : stock.change >= 0
                                                ? 'bg-success/10 text-success border border-success/20'
                                                : 'bg-error/10 text-error border border-error/20'
                                            }`}>
                                            {stock.error ? 'N/A' : `${stock.change >= 0 ? '+' : ''}${Number(stock.change).toFixed(2)}%`}
                                        </div>
                                    </div>

                                    <div className="flex items-end justify-between">
                                        <div>
                                            <div className="flex items-baseline gap-1">
                                                <span className="text-secondary text-sm font-medium">{stock.currencySymbol}</span>
                                                <p className="text-2xl font-bold text-white tracking-tight">
                                                    {stock.error || stock.price === 0
                                                        ? '–'
                                                        : (typeof stock.price === 'number' ? stock.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : stock.price)}
                                                </p>
                                            </div>
                                        </div>
                                        {!stock.error && (stock.change >= 0 ? <TrendingUp className="w-10 h-10 text-success/20 -mb-2 -mr-2" /> : <TrendingDown className="w-10 h-10 text-error/20 -mb-2 -mr-2" />)}
                                    </div>
                                </div>
                            </div>
                        ))}
                        {/* Placeholder for Empty States to encourage adding stocks */}
                        {marketData.length < 3 && (
                            <div
                                className="border-2 border-dashed border-glass-border/50 rounded-xl p-4 flex flex-col items-center justify-center text-center gap-2 text-secondary/50 hover:text-primary-400 hover:border-primary-500/30 transition-all cursor-pointer min-h-[120px]"
                                onClick={() => document.querySelector('input[placeholder="e.g., RELIANCE.NS, AAPL"]')?.focus()}
                            >
                                <div className="p-2 rounded-full bg-surface-light/50 border border-glass-border">
                                    <Sparkles className="w-5 h-5" />
                                </div>
                                <span className="text-sm font-medium">Add stock to watchlist</span>
                                <span className="text-xs opacity-70">Click to add</span>
                            </div>
                        )}
                    </div>
                </div>

                {/* Recent Analysis Side List */}
                <div className="glass-card rounded-xl border border-glass-border p-6 h-full">
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <Clock className="w-5 h-5 text-primary-400" />
                        Recent Activity
                    </h3>
                    {recentAnalyses.length === 0 ? (
                        <div className="text-center py-8">
                            <div className="w-12 h-12 rounded-full bg-surface-light border border-glass-border flex items-center justify-center mx-auto mb-3">
                                <Search className="w-5 h-5 text-secondary" />
                            </div>
                            <p className="text-secondary text-sm">
                                No recent analyses.<br />Start by searching a stock!
                            </p>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {recentAnalyses.map((item, index) => (
                                <div
                                    key={index}
                                    onClick={() => navigate(`/analysis/${item.query}`)}
                                    className="p-3 rounded-xl bg-surface-light/30 border border-glass-border hover:bg-surface-light/50 hover:border-primary-500/30 cursor-pointer transition-all flex items-center justify-between group"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500/20 to-secondary-500/20 flex items-center justify-center text-xs font-bold text-white border border-white/5">
                                            {item.query.slice(0, 1)}
                                        </div>
                                        <span className="font-medium text-gray-200 group-hover:text-white transition-colors">{item.query}</span>
                                    </div>
                                    <span className="text-xs text-secondary">
                                        {new Date(item.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;
