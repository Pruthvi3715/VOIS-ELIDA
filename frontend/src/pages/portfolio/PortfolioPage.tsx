import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Briefcase, Plus, Trash2, RefreshCw, Loader2, ChevronDown, ChevronUp,
    BarChart3, PieChart, TrendingUp, AlertTriangle, Upload, Search, X
} from 'lucide-react';
import { useAnalysis } from '../../context/AnalysisContext';

// Popular ticker suggestions
const POPULAR_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA',
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ITC.NS',
    'TATAMOTORS.NS', 'WIPRO.NS', 'ICICIBANK.NS'
];

interface PortfolioStock {
    ticker: string;
    shares?: number;
    buyPrice?: number;
    status: 'pending' | 'analyzing' | 'analyzed' | 'error';
    score?: number;
    recommendation?: string;
    risk?: string;
    error?: string;
    addedAt: string;
    analyzedAt?: string;
}

const PortfolioPage: React.FC = () => {
    const navigate = useNavigate();
    const inputRef = useRef<HTMLInputElement>(null);

    const [portfolio, setPortfolio] = useState<PortfolioStock[]>(() => {
        const saved = localStorage.getItem('elida_portfolio');
        return saved ? JSON.parse(saved) : [];
    });
    const [newTicker, setNewTicker] = useState('');
    const [newShares, setNewShares] = useState('');
    const [newBuyPrice, setNewBuyPrice] = useState('');
    const [expandedStock, setExpandedStock] = useState<string | null>(null);
    const [filter, setFilter] = useState('all');
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [showUploadModal, setShowUploadModal] = useState(false);

    // Save portfolio to localStorage
    useEffect(() => {
        localStorage.setItem('elida_portfolio', JSON.stringify(portfolio));
    }, [portfolio]);

    // Filtered suggestions based on input
    const suggestions = POPULAR_TICKERS.filter(t =>
        t.toLowerCase().includes(newTicker.toLowerCase()) &&
        !portfolio.some(p => p.ticker === t)
    ).slice(0, 5);

    const addStock = (ticker?: string) => {
        const t = (ticker || newTicker).trim().toUpperCase();
        if (!t) return;

        if (portfolio.some(s => s.ticker === t)) {
            return;
        }

        setPortfolio([...portfolio, {
            ticker: t,
            shares: newShares ? parseFloat(newShares) : undefined,
            buyPrice: newBuyPrice ? parseFloat(newBuyPrice) : undefined,
            status: 'pending',
            addedAt: new Date().toISOString()
        }]);
        setNewTicker('');
        setNewShares('');
        setNewBuyPrice('');
        setShowSuggestions(false);
    };

    const removeStock = (ticker: string) => {
        setPortfolio(portfolio.filter(s => s.ticker !== ticker));
    };

    const { startPortfolioAnalysis, isAnalyzing, progress } = useAnalysis();

    // Listen for portfolio updates from AnalysisContext or other tabs
    useEffect(() => {
        const handleStorageChange = () => {
            const saved = localStorage.getItem('elida_portfolio');
            if (saved) {
                setPortfolio(JSON.parse(saved));
            }
        };

        window.addEventListener('storage', handleStorageChange);
        return () => window.removeEventListener('storage', handleStorageChange);
    }, []);

    // Also reload when analysis finishes
    useEffect(() => {
        if (!isAnalyzing) {
            const saved = localStorage.getItem('elida_portfolio');
            if (saved) {
                setPortfolio(JSON.parse(saved));
            }
        }
    }, [isAnalyzing]);


    const analyzePortfolio = async () => {
        if (portfolio.length === 0) return;

        // Mark all as pending/analyzing strictly for UI feedback before context takes over? 
        // Actually AnalysisContext handles the background check.
        // We just trigger it.

        const tickers = portfolio.map(p => p.ticker);
        await startPortfolioAnalysis(tickers);
    };

    // Portfolio insights calculations
    const insights = {
        total: portfolio.length,
        analyzed: portfolio.filter(s => s.status === 'analyzed').length,
        avgScore: Math.round(
            portfolio.filter(s => s.score).reduce((sum, s) => sum + (s.score || 0), 0) /
            (portfolio.filter(s => s.score).length || 1)
        ),
        buyCount: portfolio.filter(s => s.recommendation?.toLowerCase().includes('buy')).length,
        holdCount: portfolio.filter(s => s.recommendation?.toLowerCase().includes('hold')).length,
        sellCount: portfolio.filter(s =>
            s.recommendation?.toLowerCase().includes('sell') ||
            s.recommendation?.toLowerCase().includes('avoid')
        ).length,
    };

    const getActionColor = (rec?: string) => {
        if (!rec) return 'text-secondary';
        const r = rec.toLowerCase();
        if (r.includes('buy')) return 'text-success';
        if (r.includes('sell') || r.includes('avoid')) return 'text-error';
        return 'text-warning';
    };

    const getActionBg = (rec?: string) => {
        if (!rec) return 'bg-surface-light border-glass-border';
        const r = rec.toLowerCase();
        if (r.includes('buy')) return 'bg-success/10 border-success/30';
        if (r.includes('sell') || r.includes('avoid')) return 'bg-error/10 border-error/30';
        return 'bg-warning/10 border-warning/30';
    };

    const filteredPortfolio = portfolio.filter(stock => {
        if (filter === 'all') return true;
        if (filter === 'buy') return stock.recommendation?.toLowerCase().includes('buy');
        if (filter === 'hold') return stock.recommendation?.toLowerCase().includes('hold');
        if (filter === 'sell') return stock.recommendation?.toLowerCase().includes('sell');
        return true;
    });

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="p-3 rounded-xl bg-gradient-primary">
                        <Briefcase className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold text-white">My Portfolio</h1>
                        <p className="text-secondary text-sm">Track and analyze your investments</p>
                    </div>
                </div>

                <div className="flex gap-3">
                    <button
                        onClick={() => setShowUploadModal(true)}
                        className="btn-secondary flex items-center gap-2"
                    >
                        <Upload className="w-4 h-4" />
                        Import PDF
                    </button>
                    <button
                        onClick={analyzePortfolio}
                        disabled={isAnalyzing || portfolio.length === 0}
                        className="btn-primary flex items-center gap-2"
                    >
                        {isAnalyzing ? (
                            <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing ({Math.round(progress)}%)...</>
                        ) : (
                            <><RefreshCw className="w-4 h-4" /> Analyze All</>
                        )}
                    </button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-4"
                >
                    <p className="text-secondary text-sm">Total Stocks</p>
                    <p className="text-3xl font-bold text-white">{insights.total}</p>
                </motion.div>
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="glass-card p-4"
                >
                    <p className="text-secondary text-sm">Analyzed</p>
                    <p className="text-3xl font-bold text-primary-400">{insights.analyzed}</p>
                </motion.div>
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="glass-card p-4"
                >
                    <p className="text-secondary text-sm">Avg Score</p>
                    <p className="text-3xl font-bold text-white">{insights.avgScore || '--'}</p>
                </motion.div>
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="glass-card p-4 border-success/30"
                >
                    <p className="text-success text-sm">Buy Signals</p>
                    <p className="text-3xl font-bold text-success">{insights.buyCount}</p>
                </motion.div>
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="glass-card p-4 border-error/30"
                >
                    <p className="text-error text-sm">Sell Signals</p>
                    <p className="text-3xl font-bold text-error">{insights.sellCount}</p>
                </motion.div>
            </div>

            {/* Add Stock Section */}
            <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Add Stock</h3>
                <div className="flex flex-wrap gap-3">
                    {/* Ticker Input with Autocomplete */}
                    <div className="relative flex-1 min-w-[200px]">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary" />
                        <input
                            ref={inputRef}
                            type="text"
                            value={newTicker}
                            onChange={(e) => {
                                setNewTicker(e.target.value);
                                setShowSuggestions(true);
                            }}
                            onFocus={() => setShowSuggestions(true)}
                            onKeyDown={(e) => e.key === 'Enter' && addStock()}
                            placeholder="Stock symbol (AAPL, TCS.NS...)"
                            className="input-glass pl-10"
                        />

                        {/* Autocomplete dropdown */}
                        <AnimatePresence>
                            {showSuggestions && suggestions.length > 0 && newTicker && (
                                <motion.div
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0 }}
                                    className="absolute top-full left-0 right-0 mt-1 bg-surface-light border border-glass-border rounded-xl shadow-glass-lg z-20 overflow-hidden"
                                >
                                    {suggestions.map(ticker => (
                                        <button
                                            key={ticker}
                                            onClick={() => {
                                                setNewTicker(ticker);
                                                setShowSuggestions(false);
                                            }}
                                            className="w-full px-4 py-3 text-left hover:bg-glass-light transition-colors flex items-center gap-2"
                                        >
                                            <TrendingUp className="w-4 h-4 text-primary-400" />
                                            <span className="text-white font-medium">{ticker}</span>
                                        </button>
                                    ))}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                    {/* Shares Input */}
                    <input
                        type="number"
                        value={newShares}
                        onChange={(e) => setNewShares(e.target.value)}
                        placeholder="Shares (optional)"
                        className="input-glass w-32"
                    />

                    {/* Buy Price Input */}
                    <input
                        type="number"
                        value={newBuyPrice}
                        onChange={(e) => setNewBuyPrice(e.target.value)}
                        placeholder="Buy price (optional)"
                        className="input-glass w-36"
                    />

                    <button onClick={() => addStock()} className="btn-primary">
                        <Plus className="w-4 h-4 mr-2" />
                        Add
                    </button>
                </div>

                {/* Quick add popular tickers */}
                <div className="mt-4 flex flex-wrap gap-2">
                    <span className="text-xs text-secondary mr-2">Quick add:</span>
                    {['AAPL', 'MSFT', 'GOOGL', 'RELIANCE.NS', 'TCS.NS'].map(ticker => (
                        <button
                            key={ticker}
                            onClick={() => addStock(ticker)}
                            disabled={portfolio.some(p => p.ticker === ticker)}
                            className="text-xs px-2 py-1 rounded-lg bg-surface-light border border-glass-border text-secondary hover:text-white hover:border-primary-500/50 transition disabled:opacity-30 disabled:cursor-not-allowed"
                        >
                            + {ticker}
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
                        className={`px-4 py-2 rounded-xl font-medium capitalize transition ${filter === f
                            ? 'bg-gradient-primary text-white shadow-glow'
                            : 'bg-surface-light text-secondary hover:text-white border border-glass-border'
                            }`}
                    >
                        {f}
                    </button>
                ))}
            </div>

            {/* Portfolio List */}
            {filteredPortfolio.length === 0 ? (
                <div className="glass-card p-12 text-center">
                    <Briefcase className="w-16 h-16 text-secondary/30 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-white mb-2">No stocks in portfolio</h3>
                    <p className="text-secondary">Add stocks above to start tracking</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {filteredPortfolio.map((stock, index) => (
                        <motion.div
                            key={stock.ticker}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className={`glass-card overflow-hidden ${expandedStock === stock.ticker ? 'ring-2 ring-primary-500/50' : ''
                                }`}
                        >
                            {/* Main Row */}
                            <div
                                className="p-4 flex items-center justify-between cursor-pointer hover:bg-glass-light transition"
                                onClick={() => setExpandedStock(expandedStock === stock.ticker ? null : stock.ticker)}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gradient-glass border border-glass-border flex items-center justify-center">
                                        <span className="text-sm font-bold text-white">
                                            {stock.ticker.replace('.NS', '').slice(0, 3)}
                                        </span>
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-white">{stock.ticker}</h4>
                                        <p className="text-sm text-secondary">
                                            {stock.status === 'pending' && 'Not analyzed'}
                                            {stock.status === 'analyzing' && 'Analyzing...'}
                                            {stock.status === 'analyzed' && `Score: ${stock.score}`}
                                            {stock.status === 'error' && 'Analysis failed'}
                                            {stock.shares && ` • ${stock.shares} shares`}
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4">
                                    {stock.status === 'analyzing' && (
                                        <Loader2 className="w-5 h-5 text-primary-400 animate-spin" />
                                    )}

                                    {stock.recommendation && (
                                        <span className={`px-4 py-1.5 rounded-xl border font-medium ${getActionBg(stock.recommendation)} ${getActionColor(stock.recommendation)}`}>
                                            {stock.recommendation}
                                        </span>
                                    )}

                                    {stock.score && (
                                        <div className="text-2xl font-bold text-gradient">
                                            {stock.score}
                                        </div>
                                    )}

                                    <button
                                        onClick={(e) => { e.stopPropagation(); removeStock(stock.ticker); }}
                                        className="p-2 text-secondary hover:text-error transition"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>

                                    {expandedStock === stock.ticker ? (
                                        <ChevronUp className="w-5 h-5 text-secondary" />
                                    ) : (
                                        <ChevronDown className="w-5 h-5 text-secondary" />
                                    )}
                                </div>
                            </div>

                            {/* Expanded Details */}
                            <AnimatePresence>
                                {expandedStock === stock.ticker && stock.status === 'analyzed' && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        className="border-t border-glass-border overflow-hidden"
                                    >
                                        <div className="p-4 bg-surface-light/30">
                                            <div className="grid grid-cols-3 gap-4 mb-4">
                                                <div className="p-3 bg-surface-light rounded-xl">
                                                    <p className="text-xs text-secondary">Match Score</p>
                                                    <p className="text-xl font-bold text-white">{stock.score}</p>
                                                </div>
                                                <div className="p-3 bg-surface-light rounded-xl">
                                                    <p className="text-xs text-secondary">Action</p>
                                                    <p className={`text-xl font-bold ${getActionColor(stock.recommendation)}`}>
                                                        {stock.recommendation}
                                                    </p>
                                                </div>
                                                <div className="p-3 bg-surface-light rounded-xl">
                                                    <p className="text-xs text-secondary">Risk</p>
                                                    <p className="text-xl font-bold text-white">{stock.risk || 'Medium'}</p>
                                                </div>
                                            </div>

                                            <button
                                                onClick={() => navigate(`/analysis/${stock.ticker}`)}
                                                className="btn-secondary w-full flex items-center justify-center gap-2"
                                            >
                                                <BarChart3 className="w-4 h-4" />
                                                View Full Analysis
                                            </button>
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    ))}
                </div>
            )}

            {/* Portfolio Insights Section */}
            {portfolio.filter(s => s.status === 'analyzed').length >= 2 && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-6"
                >
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <PieChart className="w-5 h-5 text-primary-400" />
                        Portfolio Insights
                    </h3>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Recommendation Distribution */}
                        <div>
                            <h4 className="text-sm text-secondary mb-3">Recommendation Distribution</h4>
                            <div className="space-y-2">
                                <div className="flex items-center gap-3">
                                    <div className="w-3 h-3 rounded-full bg-success" />
                                    <span className="text-white flex-1">Buy</span>
                                    <span className="font-bold text-success">{insights.buyCount}</span>
                                    <div className="w-24 h-2 bg-surface-light rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-success rounded-full"
                                            style={{ width: `${(insights.buyCount / insights.total) * 100}%` }}
                                        />
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div className="w-3 h-3 rounded-full bg-warning" />
                                    <span className="text-white flex-1">Hold</span>
                                    <span className="font-bold text-warning">{insights.holdCount}</span>
                                    <div className="w-24 h-2 bg-surface-light rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-warning rounded-full"
                                            style={{ width: `${(insights.holdCount / insights.total) * 100}%` }}
                                        />
                                    </div>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div className="w-3 h-3 rounded-full bg-error" />
                                    <span className="text-white flex-1">Sell</span>
                                    <span className="font-bold text-error">{insights.sellCount}</span>
                                    <div className="w-24 h-2 bg-surface-light rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-error rounded-full"
                                            style={{ width: `${(insights.sellCount / insights.total) * 100}%` }}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Diversification Tip */}
                        <div className="p-4 bg-surface-light/50 rounded-xl">
                            <h4 className="text-sm text-secondary mb-2">Diversification Tip</h4>
                            {insights.sellCount > insights.buyCount ? (
                                <p className="text-warning flex items-start gap-2">
                                    <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                    Portfolio has more sell signals than buy signals. Consider rebalancing.
                                </p>
                            ) : insights.buyCount > 0 ? (
                                <p className="text-success flex items-start gap-2">
                                    <TrendingUp className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                    Portfolio is well-positioned with strong buy signals.
                                </p>
                            ) : (
                                <p className="text-secondary">
                                    Analyze more stocks to get diversification insights.
                                </p>
                            )}
                        </div>
                    </div>
                </motion.div>
            )}

            {/* PDF Upload Modal */}
            <AnimatePresence>
                {showUploadModal && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
                        onClick={() => setShowUploadModal(false)}
                    >
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                            className="glass-card p-6 max-w-md w-full"
                        >
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-bold text-white">Import Portfolio</h3>
                                <button
                                    onClick={() => setShowUploadModal(false)}
                                    className="p-2 hover:bg-glass-light rounded-lg transition"
                                >
                                    <X className="w-5 h-5 text-secondary" />
                                </button>
                            </div>

                            <div className="border-2 border-dashed border-glass-border rounded-xl p-8 text-center hover:border-primary-500/50 transition cursor-pointer">
                                <Upload className="w-12 h-12 text-secondary mx-auto mb-4" />
                                <p className="text-white font-medium mb-2">
                                    Drop your portfolio PDF here
                                </p>
                                <p className="text-sm text-secondary mb-4">
                                    or click to browse files
                                </p>
                                <input
                                    type="file"
                                    accept=".pdf,.csv"
                                    className="hidden"
                                    onChange={(e) => {
                                        // PDF parsing would go here
                                        console.log('File selected:', e.target.files?.[0]);
                                        setShowUploadModal(false);
                                    }}
                                />
                                <p className="text-xs text-secondary">
                                    Supports: Zerodha, Groww, Angel One, generic CSV
                                </p>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default PortfolioPage;
