import { useState, useEffect } from 'react';
import {
    Briefcase,
    Plus,
    Trash2,
    RefreshCw,
    Loader2,
    ChevronDown,
    ChevronUp,
    BarChart3
} from 'lucide-react';
import { API_BASE_URL, getUserId } from '../api';

function PortfolioPage() {
    const [portfolio, setPortfolio] = useState(() => {
        const saved = localStorage.getItem('elida_portfolio');
        return saved ? JSON.parse(saved) : [];
    });
    const [newTicker, setNewTicker] = useState('');
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
            status: 'pending',
            addedAt: new Date().toISOString()
        }]);
        setNewTicker('');
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
        if (!rec) return 'text-gray-500';
        const r = rec.toLowerCase();
        if (r.includes('buy') || r.includes('strong')) return 'text-green-600';
        if (r.includes('sell') || r.includes('avoid')) return 'text-red-600';
        return 'text-amber-600';
    };

    const getRecommendationBg = (rec) => {
        if (!rec) return 'bg-gray-50 border-gray-200';
        const r = rec.toLowerCase();
        if (r.includes('buy') || r.includes('strong')) return 'bg-green-50 border-green-200';
        if (r.includes('sell') || r.includes('avoid')) return 'bg-red-50 border-red-200';
        return 'bg-amber-50 border-amber-200';
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

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
                        <Briefcase className="w-7 h-7 text-gray-700" />
                        My Portfolio
                    </h1>
                    <p className="text-gray-500 mt-1">Add stocks and get AI-powered recommendations</p>
                </div>
                <button
                    onClick={analyzePortfolio}
                    disabled={analyzing || portfolio.length === 0}
                    className="flex items-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {analyzing ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <RefreshCw className="w-5 h-5" />
                            Analyze All
                        </>
                    )}
                </button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="bg-white rounded-xl border border-gray-200 p-4">
                    <p className="text-gray-500 text-sm">Total Stocks</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                </div>
                <div className="bg-white rounded-xl border border-gray-200 p-4">
                    <p className="text-gray-500 text-sm">Analyzed</p>
                    <p className="text-2xl font-bold text-blue-600">{stats.analyzed}</p>
                </div>
                <div className="bg-white rounded-xl border border-gray-200 p-4">
                    <p className="text-gray-500 text-sm">Avg Score</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.avgScore.toFixed(0)}%</p>
                </div>
                <div className="bg-green-50 rounded-xl border border-green-200 p-4">
                    <p className="text-green-600 text-sm">Buy Signals</p>
                    <p className="text-2xl font-bold text-green-600">{stats.buyCount}</p>
                </div>
                <div className="bg-red-50 rounded-xl border border-red-200 p-4">
                    <p className="text-red-600 text-sm">Sell Signals</p>
                    <p className="text-2xl font-bold text-red-600">{stats.sellCount}</p>
                </div>
            </div>

            {/* Add Stock */}
            <div className="bg-white rounded-xl border border-gray-200 p-4">
                <div className="flex gap-3">
                    <input
                        type="text"
                        value={newTicker}
                        onChange={(e) => setNewTicker(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && addStock()}
                        placeholder="Enter stock symbol (e.g. TCS.NS, AAPL, INFY.NS)"
                        className="flex-1 border border-gray-200 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-gray-300 focus:ring-2 focus:ring-gray-100 transition"
                    />
                    <button
                        onClick={addStock}
                        className="flex items-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white rounded-lg font-medium transition"
                    >
                        <Plus className="w-5 h-5" />
                        Add
                    </button>
                </div>
            </div>

            {/* Filter Tabs */}
            <div className="flex gap-2">
                {['all', 'buy', 'hold', 'sell'].map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        className={`px-4 py-2 rounded-lg font-medium capitalize transition ${filter === f
                            ? 'border-2 border-gray-800 text-gray-900 bg-white'
                            : 'bg-white border border-gray-200 text-gray-500 hover:text-gray-700'
                            }`}
                    >
                        {f}
                    </button>
                ))}
            </div>

            {/* Portfolio Table */}
            {filteredPortfolio.length === 0 ? (
                <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
                    <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">No stocks in portfolio</h3>
                    <p className="text-gray-500">Add stocks above to start building your portfolio</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {filteredPortfolio.map((stock) => (
                        <div
                            key={stock.ticker}
                            className={`bg-white rounded-xl border border-gray-200 overflow-hidden transition-all ${expandedStock === stock.ticker ? 'ring-2 ring-gray-300' : ''
                                }`}
                        >
                            {/* Main Row */}
                            <div
                                className="p-4 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition"
                                onClick={() => setExpandedStock(expandedStock === stock.ticker ? null : stock.ticker)}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">
                                        <span className="text-sm font-bold text-gray-700">
                                            {stock.ticker.replace('.NS', '').slice(0, 3)}
                                        </span>
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-gray-900">{stock.ticker}</h4>
                                        <p className="text-sm text-gray-500">
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
                                                <circle cx="28" cy="28" r="24" fill="none" stroke="#e5e7eb" strokeWidth="4" />
                                                <circle
                                                    cx="28" cy="28" r="24" fill="none"
                                                    stroke={stock.score >= 70 ? '#22c55e' : stock.score >= 50 ? '#eab308' : '#ef4444'}
                                                    strokeWidth="4"
                                                    strokeDasharray={`${stock.score * 1.51} 151`}
                                                    strokeLinecap="round"
                                                />
                                            </svg>
                                            <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-gray-900">
                                                {stock.score}
                                            </span>
                                        </div>
                                    )}

                                    <button
                                        onClick={(e) => { e.stopPropagation(); removeStock(stock.ticker); }}
                                        className="p-2 text-gray-400 hover:text-red-500 transition"
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
                                <div className="px-4 pb-4 border-t border-gray-100 pt-4">
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h5 className="text-sm text-gray-500 mb-1">Match Score</h5>
                                            <p className="text-2xl font-bold text-gray-900">{stock.score}%</p>
                                        </div>
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h5 className="text-sm text-gray-500 mb-1">Risk Level</h5>
                                            <p className="text-xl font-semibold text-gray-900">{stock.risk || 'Unknown'}</p>
                                        </div>
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h5 className="text-sm text-gray-500 mb-1">Action</h5>
                                            <p className={`text-xl font-semibold ${getRecommendationColor(stock.recommendation)}`}>
                                                {stock.recommendation}
                                            </p>
                                        </div>
                                    </div>
                                    <a
                                        href={`/analysis/${stock.ticker}`}
                                        className="mt-4 inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 transition"
                                    >
                                        <BarChart3 className="w-4 h-4" />
                                        View Full Analysis
                                    </a>
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
