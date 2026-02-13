import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Search, Sparkles, Zap, Target, User, Clock,
    TrendingUp, TrendingDown, BarChart3, Brain,
    Shield, Gauge, ArrowRight, Activity, Star
} from 'lucide-react';
import { API_BASE_URL } from '../api';

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

    // Poll market data
    useEffect(() => {
        fetchRecentHistory();
        fetchMarketData();
        const interval = setInterval(fetchMarketData, 30000);
        return () => clearInterval(interval);
    }, [watchedTickers]);

    // Save watched
    useEffect(() => {
        localStorage.setItem('watchedTickers', JSON.stringify(watchedTickers));
    }, [watchedTickers]);

    const fetchRecentHistory = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/history?limit=4`);
            const data = await response.json();
            setRecentAnalyses(data.entries?.slice(0, 4) || []);
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
                    const data = jsonData.financials || jsonData;
                    const isIndian = ticker.endsWith('.NS') || ticker.endsWith('.BO');

                    results.push({
                        ticker,
                        price: data.current_price || data.price || 0,
                        change: data.price_change_percentage_24h || data.change_percent || 0,
                        currencySymbol: isIndian ? '\u20B9' : '$',
                        name: data.company_name || ticker.replace('.NS', '')
                    });
                }
            } catch (e) {
                results.push({
                    ticker, error: true, price: 0, change: 0,
                    currencySymbol: ticker.endsWith('.NS') ? '\u20B9' : '$',
                    name: ticker
                });
            }
        }
        setMarketData(results);
    };

    const handleAnalyze = () => {
        if (searchTicker.trim()) {
            setLoading(true);
            setTimeout(() => {
                navigate(`/analysis/${searchTicker.trim().toUpperCase()}`);
                setLoading(false);
            }, 800); // Fake load for smoothness
        }
    };

    const removeTicker = (t) => setWatchedTickers(watchedTickers.filter(x => x !== t));
    const addTicker = (e) => {
        e.preventDefault();
        if (newTicker && !watchedTickers.includes(newTicker.toUpperCase())) {
            setWatchedTickers([...watchedTickers, newTicker.toUpperCase()]);
            setNewTicker('');
        }
    };

    return (
        <div className="space-y-12 animate-float">
            {/* 1. Hero Section - Centered & Premium */}
            <div className="relative py-12 px-6 text-center">
                {/* Glow behind header */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-primary-500/20 rounded-full blur-[100px] -z-10" />

                <h1 className="text-5xl md:text-6xl font-black mb-6 tracking-tight">
                    <span className="text-white">AI-Powered </span>
                    <span className="text-gradient">Investment Intelligence</span>
                </h1>
                <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto font-light leading-relaxed">
                    Instantly analyze stocks with autonomous agents.
                    <span className="text-indigo-400 font-medium"> Quant</span>,
                    <span className="text-cyan-400 font-medium"> Macro</span>, and
                    <span className="text-amber-400 font-medium"> Fundamental</span>.
                </p>

                {/* Search Bar */}
                <div className="relative max-w-2xl mx-auto group z-20">
                    <div className="absolute inset-0 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition-opacity duration-500" />
                    <div className="relative flex items-center bg-[#0F101A] border border-white/10 rounded-2xl p-2 shadow-2xl transition-all group-hover:border-white/20">
                        <Search className="w-6 h-6 text-gray-400 ml-4 mr-2" />
                        <input
                            type="text"
                            value={searchTicker}
                            onChange={(e) => setSearchTicker(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                            placeholder="Analyze any asset (e.g. RELIANCE.NS, TSLA)..."
                            className="flex-1 bg-transparent text-lg text-white placeholder-gray-600 focus:outline-none h-12"
                        />
                        <button
                            onClick={handleAnalyze}
                            disabled={!searchTicker.trim() || loading}
                            className="bg-gradient-to-r from-violet-600 to-indigo-600 text-white px-8 py-3 rounded-xl font-bold flex items-center gap-2 hover:shadow-lg hover:shadow-violet-500/25 transition-all active:scale-95 disabled:opacity-50 disabled:scale-100"
                        >
                            {loading ? (
                                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            ) : (
                                <>Analyze <Zap className="w-4 h-4 fill-white" /></>
                            )}
                        </button>
                    </div>
                </div>

                {/* Quick Tags */}
                <div className="flex flex-wrap justify-center gap-3 mt-6">
                    {['TCS.NS', 'RELIANCE.NS', 'AAPL', 'MSFT', 'BTC-USD'].map(t => (
                        <button
                            key={t}
                            onClick={() => { setSearchTicker(t); handleAnalyze(); }}
                            className="text-xs font-medium px-3 py-1.5 rounded-full bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10 hover:text-white transition-colors"
                        >
                            {t}
                        </button>
                    ))}
                </div>
            </div>

            {/* 2. Stats Grid - Premium Glass Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-4">
                {/* Active Agents */}
                <div className="glass-card-premium p-6 relative overflow-hidden group">
                    <div className="absolute right-0 top-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <Brain className="w-24 h-24 text-indigo-500" />
                    </div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
                            <Activity className="w-5 h-5 text-indigo-400" />
                        </div>
                        <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Agents Active</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <span className="text-3xl font-bold text-white">4</span>
                        <span className="text-sm text-indigo-400">/ 4 Systems</span>
                    </div>
                    <div className="mt-3 h-1 w-full bg-white/5 rounded-full overflow-hidden">
                        <div className="h-full w-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full animate-pulse-soft" />
                    </div>
                </div>

                {/* Market Status */}
                <div className="glass-card-premium p-6 relative overflow-hidden group">
                    <div className="absolute right-0 top-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <Activity className="w-24 h-24 text-emerald-500" />
                    </div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                            <TrendingUp className="w-5 h-5 text-emerald-400" />
                        </div>
                        <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Market Data</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <span className="text-3xl font-bold text-white">Live</span>
                        <span className="flex h-2 w-2 relative">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                        </span>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">Connecting to Global Exchanges</p>
                </div>

                {/* Accuracy */}
                <div className="glass-card-premium p-6 relative overflow-hidden group">
                    <div className="absolute right-0 top-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <Target className="w-24 h-24 text-amber-500" />
                    </div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/20">
                            <Target className="w-5 h-5 text-amber-400" />
                        </div>
                        <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Precision</span>
                    </div>
                    <div className="flex items-baseline gap-2">
                        <span className="text-3xl font-bold text-white">87%</span>
                        <span className="text-sm text-amber-400 font-medium">+2.4%</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">Based on backtested signals</p>
                </div>

                {/* Profile Link */}
                <div
                    onClick={() => navigate('/profile')}
                    className="glass-card-premium p-6 relative overflow-hidden group hover:bg-white/5 transition-colors cursor-pointer border-dashed border-white/20 hover:border-violet-500/50"
                >
                    <div className="flex flex-col items-center justify-center h-full text-center">
                        <div className="p-3 rounded-full bg-white/5 mb-3 group-hover:scale-110 transition-transform">
                            <User className="w-6 h-6 text-gray-300" />
                        </div>
                        <span className="text-white font-medium">Investor Profile</span>
                        <span className="text-xs text-gray-500 mt-1">Customize your DNA</span>
                    </div>
                </div>
            </div>

            {/* 3. Bottom Section: Watchlist & Recent */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 px-4 pb-12">
                {/* Watchlist */}
                <div className="lg:col-span-2 glass-card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold flex items-center gap-2">
                            <Star className="w-5 h-5 text-amber-400 fill-amber-400" />
                            My Watchlist
                        </h3>
                        <form onSubmit={addTicker} className="flex gap-2">
                            <input
                                type="text"
                                value={newTicker}
                                onChange={(e) => setNewTicker(e.target.value)}
                                placeholder="Search stocks..."
                                className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-sm text-white focus:border-emerald-500/50 outline-none w-36"
                            />
                            <button type="submit" className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-emerald-500/30 transition-colors flex items-center gap-1">
                                + Add Stock
                            </button>
                        </form>
                    </div>

                    <div className="space-y-3">
                        {marketData.map((stock) => (
                            <div
                                key={stock.ticker}
                                onClick={() => navigate(`/analysis/${stock.ticker}`)}
                                className="group flex items-center justify-between p-4 rounded-xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.06] hover:border-white/10 transition-all cursor-pointer relative overflow-hidden"
                            >
                                {/* Hover Gradient */}
                                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.02] to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />

                                <div className="flex items-center gap-4">
                                    <Star className="w-4 h-4 text-amber-400 fill-amber-400 flex-shrink-0" />
                                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xs border ${stock.change >= 0 ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-rose-500/10 border-rose-500/20 text-rose-400'}`}>
                                        {stock.change >= 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white">{stock.ticker}</h4>
                                        <p className="text-xs text-gray-500">{stock.name}</p>
                                    </div>
                                </div>
                                <div className="text-right flex items-center gap-6">
                                    <div className="hidden sm:flex gap-0.5 items-end h-8">
                                        {[40, 60, 45, 70, 55, 65, 50].map((h, i) => (
                                            <div key={i} className={`w-1 rounded-t-sm ${stock.change >= 0 ? 'bg-emerald-500/20' : 'bg-rose-500/20'}`} style={{ height: `${h}%` }} />
                                        ))}
                                    </div>

                                    <div>
                                        <div className="text-lg font-bold text-white tabular-nums">
                                            {stock.currencySymbol}{typeof stock.price === 'number' ? stock.price.toLocaleString(undefined, { minimumFractionDigits: 2 }) : stock.price}
                                        </div>
                                        <div className={`text-xs font-medium flex items-center justify-end gap-1 ${stock.change >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                                            {stock.change >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                                            {Math.abs(stock.change).toFixed(2)}%
                                        </div>
                                    </div>

                                    <button
                                        onClick={(e) => { e.stopPropagation(); removeTicker(stock.ticker); }}
                                        className="p-2 text-gray-600 hover:text-rose-400 transition-colors opacity-0 group-hover:opacity-100"
                                    >
                                        ×
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Recent Activity */}
                <div className="glass-card p-6">
                    <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <Clock className="w-5 h-5 text-violet-400" />
                        Recent Activity
                    </h3>
                    <div className="space-y-4">
                        {recentAnalyses.length === 0 ? (
                            <div className="text-center py-10 text-gray-500">
                                <Sparkles className="w-8 h-8 mx-auto mb-2 opacity-20" />
                                <p className="text-sm">No analysis history yet.</p>
                            </div>
                        ) : (
                            recentAnalyses.map((item, i) => (
                                <div
                                    key={i}
                                    onClick={() => navigate(`/analysis/${item.query}`)}
                                    className="flex items-center gap-4 p-3 rounded-lg hover:bg-white/5 transition-colors cursor-pointer border border-transparent hover:border-white/5"
                                >
                                    <div className="w-2 h-2 rounded-full bg-violet-500" />
                                    <div className="flex-1">
                                        <h5 className="font-medium text-white">{item.query}</h5>
                                        <p className="text-xs text-gray-500">Analyzed {new Date(item.timestamp).toLocaleDateString()}</p>
                                    </div>
                                    <ArrowRight className="w-4 h-4 text-gray-600" />
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;
