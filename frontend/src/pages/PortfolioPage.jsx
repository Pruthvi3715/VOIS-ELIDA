import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Briefcase,
    Plus,
    Trash2,
    RefreshCw,
    Loader2,
    ChevronDown,
    ChevronUp,
    BarChart3,
    FileUp,
    Zap,
    PieChart,
    TrendingUp,
    CheckCircle,
    AlertCircle,
    Shield
} from 'lucide-react';
import { API_BASE_URL, getUserId } from '../api';

function PortfolioPage() {
    const navigate = useNavigate();
    const [portfolio, setPortfolio] = useState(() => {
        const saved = localStorage.getItem('elida_portfolio');
        return saved ? JSON.parse(saved) : [];
    });
    const [newTicker, setNewTicker] = useState('');
    const [newShares, setNewShares] = useState('');
    const [newPrice, setNewPrice] = useState('');
    const [loading, setLoading] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [expandedStock, setExpandedStock] = useState(null);
    const [filter, setFilter] = useState('all');

    // Save portfolio to localStorage whenever it changes
    useEffect(() => {
        localStorage.setItem('elida_portfolio', JSON.stringify(portfolio));
    }, [portfolio]);

    const addStock = () => {
        const ticker = newTicker.trim().toUpperCase();
        if (!ticker) return;

        // Check if already exists
        if (portfolio.some(s => s.ticker === ticker)) {
            alert('Stock already in portfolio');
            return;
        }

        setPortfolio([...portfolio, {
            ticker,
            shares: parseFloat(newShares) || 0,
            buyPrice: parseFloat(newPrice) || 0,
            status: 'pending',
            addedAt: new Date().toISOString()
        }]);
        setNewTicker('');
        setNewShares('');
        setNewPrice('');
    };

    const removeStock = (ticker) => {
        setPortfolio(portfolio.filter(s => s.ticker !== ticker));
    };

    const analyzePortfolio = async () => {
        if (portfolio.length === 0) return;

        setAnalyzing(true);
        const tickers = portfolio.map(s => s.ticker);

        try {
            const response = await fetch(`${API_BASE_URL}/api/portfolio/scan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: getUserId(),
                    tickers
                })
            });

            const data = await response.json();

            // Update portfolio with results
            setPortfolio(prev => prev.map(stock => {
                const result = data.results?.find(r => r.ticker === stock.ticker);
                if (result) {
                    return {
                        ...stock,
                        status: result.error ? 'error' : 'analyzed',
                        score: result.score,
                        recommendation: result.recommendation,
                        risk: result.risk,
                        error: result.error,
                        analyzedAt: new Date().toISOString()
                    };
                }
                return stock;
            }));

        } catch (error) {
            console.error('Analysis failed:', error);
            alert('Failed to analyze portfolio. Ensure backend is running.');
        } finally {
            setAnalyzing(false);
        }
    };

    const getRecommendationColor = (rec) => {
        if (!rec) return 'text-gray-400';
        const r = rec.toLowerCase();
        if (r.includes('buy') || r.includes('strong')) return 'text-success';
        if (r.includes('sell') || r.includes('avoid')) return 'text-error';
        return 'text-warning';
    };

    const getRecommendationBg = (rec) => {
        if (!rec) return 'bg-white/5 border-white/10';
        const r = rec.toLowerCase();
        if (r.includes('buy') || r.includes('strong')) return 'bg-success/10 border-success/30';
        if (r.includes('sell') || r.includes('avoid')) return 'bg-error/10 border-error/30';
        return 'bg-warning/10 border-warning/30';
    };

    const filteredPortfolio = portfolio.filter(stock => {
        if (filter === 'all') return true;
        if (filter === 'buy') return stock.recommendation?.toLowerCase().includes('buy');
        if (filter === 'hold') return stock.recommendation?.toLowerCase().includes('hold');
        if (filter === 'sell') return stock.recommendation?.toLowerCase().includes('sell') || stock.recommendation?.toLowerCase().includes('avoid');
        return true;
    });

    const stats = {
        total: portfolio.length,
        analyzed: portfolio.filter(s => s.status === 'analyzed').length,
        avgScore: portfolio.filter(s => s.score).reduce((sum, s) => sum + s.score, 0) / (portfolio.filter(s => s.score).length || 1),
        buyCount: portfolio.filter(s => s.recommendation?.toLowerCase().includes('buy')).length,
        sellCount: portfolio.filter(s => s.recommendation?.toLowerCase().includes('sell') || s.recommendation?.toLowerCase().includes('avoid')).length,
    };

    const quickAddStocks = ['AAPL', 'MSFT', 'GOOGL', 'RELIANCE.NS', 'TCS.NS'];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div className="flex items-center gap-4">
                    <div className="p-3 rounded-xl bg-primary-500/10 border border-primary-500/20">
                        <Briefcase className="w-6 h-6 text-primary-400" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold text-white">My Portfolio</h1>
                        <p className="text-secondary text-sm">Track and analyze your investments</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        className="flex items-center gap-2 px-4 py-2.5 bg-surface-light text-gray-300 rounded-xl border border-white/10 hover:bg-white/10 hover:text-white transition-all"
                    >
                        <FileUp className="w-4 h-4" />
                        Import PDF
                    </button>
                    <button
                        onClick={analyzePortfolio}
                        disabled={analyzing || portfolio.length === 0}
                        className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-primary-600 to-accent-dark text-white rounded-xl font-medium hover:shadow-glow transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {analyzing ? (
                            <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Analyzing...
                            </>
                        ) : (
                            <>
                                <Zap className="w-4 h-4" />
                                Analyze All
                            </>
                        )}
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="glass-card p-4">
                    <p className="text-secondary text-xs uppercase tracking-wider mb-1">Total Stocks</p>
                    <p className="text-2xl font-bold text-white">{stats.total}</p>
                </div>
                <div className="glass-card p-4">
                    <p className="text-secondary text-xs uppercase tracking-wider mb-1">Analyzed</p>
                    <p className="text-2xl font-bold text-primary-400">{stats.analyzed}</p>
                </div>
                <div className="glass-card p-4">
                    <p className="text-secondary text-xs uppercase tracking-wider mb-1">Avg Score</p>
                    <p className="text-2xl font-bold text-white">{stats.analyzed > 0 ? `${stats.avgScore.toFixed(0)}` : '--'}</p>
                </div>
                <div className="glass-card p-4 border-success/20">
                    <p className="text-success text-xs uppercase tracking-wider mb-1">Buy Signals</p>
                    <p className="text-2xl font-bold text-success">{stats.buyCount}</p>
                </div>
                <div className="glass-card p-4 border-error/20">
                    <p className="text-error text-xs uppercase tracking-wider mb-1">Sell Signals</p>
                    <p className="text-2xl font-bold text-error">{stats.sellCount}</p>
                </div>
            </div>

            {/* Portfolio Analysis Section - NEW */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Portfolio Allocation Pie Chart */}
                <div className="glass-card p-6">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <PieChart className="w-5 h-5 text-primary-400" />
                        Portfolio Allocation by Sector
                    </h3>
                    <div className="flex items-center justify-center">
                        {/* SVG Pie Chart */}
                        <div className="relative w-48 h-48">
                            <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                                {/* Technology - 45% */}
                                <circle cx="50" cy="50" r="40" fill="transparent"
                                    stroke="#6366f1" strokeWidth="20"
                                    strokeDasharray="113 251" strokeDashoffset="0" />
                                {/* Banking - 25% */}
                                <circle cx="50" cy="50" r="40" fill="transparent"
                                    stroke="#10b981" strokeWidth="20"
                                    strokeDasharray="62.8 251" strokeDashoffset="-113" />
                                {/* Energy - 20% */}
                                <circle cx="50" cy="50" r="40" fill="transparent"
                                    stroke="#f59e0b" strokeWidth="20"
                                    strokeDasharray="50.2 251" strokeDashoffset="-175.8" />
                                {/* Healthcare - 10% */}
                                <circle cx="50" cy="50" r="40" fill="transparent"
                                    stroke="#a855f7" strokeWidth="20"
                                    strokeDasharray="25.1 251" strokeDashoffset="-226" />
                            </svg>
                            <div className="absolute inset-0 flex items-center justify-center flex-col">
                                <span className="text-2xl font-bold text-white">{stats.total}</span>
                                <span className="text-xs text-gray-400">Stocks</span>
                            </div>
                        </div>
                    </div>
                    {/* Legend */}
                    <div className="grid grid-cols-2 gap-3 mt-6">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-indigo-500"></div>
                            <span className="text-sm text-gray-300">Technology 45%</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                            <span className="text-sm text-gray-300">Banking 25%</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                            <span className="text-sm text-gray-300">Energy 20%</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                            <span className="text-sm text-gray-300">Healthcare 10%</span>
                        </div>
                    </div>
                </div>

                {/* Health Metrics */}
                <div className="glass-card p-6">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <Shield className="w-5 h-5 text-emerald-400" />
                        Health Metrics
                    </h3>

                    {/* Portfolio Health Score */}
                    <div className="mb-6">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-gray-400 text-sm">Portfolio Health Score</span>
                            <span className="text-2xl font-bold text-white">
                                {stats.analyzed > 0 ? Math.round(stats.avgScore) : '--'}
                                <span className="text-sm text-gray-400">/100</span>
                            </span>
                        </div>
                        <div className="h-3 bg-white/10 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-emerald-500 to-emerald-400 rounded-full transition-all duration-500"
                                style={{ width: `${stats.analyzed > 0 ? stats.avgScore : 0}%` }}
                            ></div>
                        </div>
                    </div>

                    {/* Metrics List */}
                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/10">
                            <div className="flex items-center gap-3">
                                <CheckCircle className="w-5 h-5 text-emerald-400" />
                                <span className="text-gray-300">Diversification</span>
                            </div>
                            <span className="text-emerald-400 font-medium">Good</span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/10">
                            <div className="flex items-center gap-3">
                                <AlertCircle className="w-5 h-5 text-amber-400" />
                                <span className="text-gray-300">Risk Level</span>
                            </div>
                            <span className="px-3 py-1 bg-amber-500/20 text-amber-400 rounded-lg text-sm font-medium">Moderate</span>
                        </div>

                        <div className="flex items-center justify-between p-3 bg-white/5 rounded-xl border border-white/10">
                            <div className="flex items-center gap-3">
                                <TrendingUp className="w-5 h-5 text-emerald-400" />
                                <span className="text-gray-300">Concentration Risk</span>
                            </div>
                            <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-lg text-sm font-medium">Low</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="glass-card p-5">
                <h3 className="text-white font-semibold mb-4">Add Stock</h3>
                <div className="flex flex-wrap gap-3">
                    <input
                        type="text"
                        value={newTicker}
                        onChange={(e) => setNewTicker(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && addStock()}
                        placeholder="Stock symbol (AAPL, TCS.NS)"
                        className="flex-1 min-w-[200px] bg-surface-light border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-primary-500/50 focus:ring-1 focus:ring-primary-500/50 transition-all"
                    />
                    <input
                        type="number"
                        value={newShares}
                        onChange={(e) => setNewShares(e.target.value)}
                        placeholder="Shares (optional)"
                        className="w-32 bg-surface-light border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-primary-500/50 transition-all"
                    />
                    <input
                        type="number"
                        value={newPrice}
                        onChange={(e) => setNewPrice(e.target.value)}
                        placeholder="Buy price (optional)"
                        className="w-40 bg-surface-light border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-primary-500/50 transition-all"
                    />
                    <button
                        onClick={addStock}
                        className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-accent-dark text-white rounded-xl font-medium hover:shadow-glow transition-all"
                    >
                        <Plus className="w-5 h-5" />
                        Add
                    </button>
                </div>

                {/* Quick Add */}
                <div className="flex items-center gap-2 mt-4">
                    <span className="text-secondary text-sm">Quick add:</span>
                    {quickAddStocks.map(t => (
                        <button
                            key={t}
                            onClick={() => {
                                if (!portfolio.some(s => s.ticker === t)) {
                                    setPortfolio([...portfolio, { ticker: t, status: 'pending', addedAt: new Date().toISOString() }]);
                                }
                            }}
                            className="text-xs px-3 py-1.5 rounded-lg bg-white/5 text-gray-400 border border-white/10 hover:bg-white/10 hover:text-white transition-all"
                        >
                            + {t}
                        </button>
                    ))}
                </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex gap-2">
                {['all', 'buy', 'hold', 'sell'].map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        className={`px-4 py-2 rounded-xl font-medium capitalize transition-all ${filter === f
                            ? 'bg-primary-500/20 text-primary-300 border border-primary-500/30'
                            : 'bg-surface-light text-gray-400 border border-white/10 hover:text-white hover:border-white/20'
                            }`}
                    >
                        {f}
                    </button>
                ))}
            </div>

            {/* Portfolio List */}
            {filteredPortfolio.length === 0 ? (
                <div className="glass-card p-12 text-center">
                    <Briefcase className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-white mb-2">No stocks in portfolio</h3>
                    <p className="text-secondary">Add stocks above to start tracking</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {filteredPortfolio.map((stock) => (
                        <div
                            key={stock.ticker}
                            className={`glass-card overflow-hidden transition-all ${expandedStock === stock.ticker ? 'ring-1 ring-primary-500/50' : ''
                                }`}
                        >
                            {/* Main Row */}
                            <div
                                className="p-4 flex items-center justify-between cursor-pointer hover:bg-white/[0.02] transition-all"
                                onClick={() => setExpandedStock(expandedStock === stock.ticker ? null : stock.ticker)}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-surface-light border border-white/10 flex items-center justify-center">
                                        <span className="text-sm font-bold text-gray-300">
                                            {stock.ticker.replace('.NS', '').slice(0, 3)}
                                        </span>
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-white">{stock.ticker}</h4>
                                        <p className="text-sm text-secondary">
                                            {stock.status === 'pending' && 'Not analyzed yet'}
                                            {stock.status === 'analyzed' && `Score: ${stock.score}%`}
                                            {stock.status === 'error' && 'Analysis failed'}
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4">
                                    {stock.recommendation && (
                                        <span className={`px-4 py-1.5 rounded-lg border font-medium ${getRecommendationBg(stock.recommendation)} ${getRecommendationColor(stock.recommendation)}`}>
                                            {stock.recommendation}
                                        </span>
                                    )}

                                    {stock.score && (
                                        <div className="w-14 h-14 relative">
                                            <svg className="w-full h-full -rotate-90">
                                                <circle cx="28" cy="28" r="24" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="4" />
                                                <circle
                                                    cx="28" cy="28" r="24" fill="none"
                                                    stroke={stock.score >= 70 ? '#00f5a0' : stock.score >= 50 ? '#ffc107' : '#ff4757'}
                                                    strokeWidth="4"
                                                    strokeDasharray={`${stock.score * 1.51} 151`}
                                                    strokeLinecap="round"
                                                />
                                            </svg>
                                            <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-white">
                                                {stock.score}
                                            </span>
                                        </div>
                                    )}

                                    <button
                                        onClick={(e) => { e.stopPropagation(); removeStock(stock.ticker); }}
                                        className="p-2 text-gray-500 hover:text-error transition-all"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>

                                    {expandedStock === stock.ticker ? (
                                        <ChevronUp className="w-5 h-5 text-gray-400" />
                                    ) : (
                                        <ChevronDown className="w-5 h-5 text-gray-400" />
                                    )}
                                </div>
                            </div>

                            {/* Expanded Details */}
                            {expandedStock === stock.ticker && stock.status === 'analyzed' && (
                                <div className="px-4 pb-4 border-t border-white/5 pt-4">
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        <div className="bg-surface-light rounded-xl p-4 border border-white/5">
                                            <h5 className="text-sm text-secondary mb-1">Match Score</h5>
                                            <p className="text-2xl font-bold text-white">{stock.score}%</p>
                                        </div>
                                        <div className="bg-surface-light rounded-xl p-4 border border-white/5">
                                            <h5 className="text-sm text-secondary mb-1">Risk Level</h5>
                                            <p className="text-xl font-semibold text-white">{stock.risk || 'Unknown'}</p>
                                        </div>
                                        <div className="bg-surface-light rounded-xl p-4 border border-white/5">
                                            <h5 className="text-sm text-secondary mb-1">Action</h5>
                                            <p className={`text-xl font-semibold ${getRecommendationColor(stock.recommendation)}`}>
                                                {stock.recommendation}
                                            </p>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => navigate(`/analysis/${stock.ticker}`)}
                                        className="mt-4 inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 transition-all"
                                    >
                                        <BarChart3 className="w-4 h-4" />
                                        View Full Analysis
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default PortfolioPage;
