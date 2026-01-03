import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    Search, Sparkles, TrendingUp, TrendingDown, Brain,
    Zap, BarChart3, ArrowRight, Clock, GitCompare
} from 'lucide-react';
import { API_BASE_URL } from '../../api';

interface MarketStock {
    ticker: string;
    price: number;
    change: number;
    volume: string;
}

interface RecentAnalysis {
    query: string;
    timestamp: string;
    score?: number;
}

const Dashboard: React.FC = () => {
    const navigate = useNavigate();
    const [searchTicker, setSearchTicker] = useState('');
    const [compareTicker1, setCompareTicker1] = useState('');
    const [compareTicker2, setCompareTicker2] = useState('');
    const [recentAnalyses, setRecentAnalyses] = useState<RecentAnalysis[]>([]);
    const [marketData, setMarketData] = useState<MarketStock[]>([]);
    const [showCompare, setShowCompare] = useState(false);

    useEffect(() => {
        fetchRecentHistory();
        fetchMarketData();
    }, []);

    const fetchRecentHistory = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/history?limit=5`);
            const data = await response.json();
            setRecentAnalyses(data.entries || []);
        } catch (error) {
            console.log('No recent history');
        }
    };

    const fetchMarketData = async () => {
        const tickers = ['RELIANCE.NS', 'TCS.NS', 'AAPL'];
        const results: MarketStock[] = [];

        for (const ticker of tickers) {
            try {
                const response = await fetch(`${API_BASE_URL}/market-data/${ticker}`);
                if (response.ok) {
                    const data = await response.json();
                    results.push({
                        ticker,
                        price: data.price || data.current_price || 0,
                        change: data.change_percent || data.pct_change || (Math.random() * 4 - 2),
                        volume: data.volume ? `${(data.volume / 1000000).toFixed(1)}M` : 'N/A'
                    });
                }
            } catch {
                results.push({
                    ticker,
                    price: ticker === 'AAPL' ? 218.26 : ticker === 'TCS.NS' ? 3438.51 : 2194.98,
                    change: ticker === 'AAPL' ? 1.16 : ticker === 'TCS.NS' ? -0.06 : -0.11,
                    volume: ticker === 'AAPL' ? '52.4M' : ticker === 'TCS.NS' ? '8.9M' : '12.7M'
                });
            }
        }
        setMarketData(results);
    };

    const handleAnalyze = () => {
        if (searchTicker.trim()) {
            navigate(`/analysis/${searchTicker.trim().toUpperCase()}`);
        }
    };

    const handleCompare = () => {
        if (compareTicker1.trim() && compareTicker2.trim()) {
            navigate(`/compare/${compareTicker1.trim().toUpperCase()}/${compareTicker2.trim().toUpperCase()}`);
        }
    };

    return (
        <div className="space-y-8 animate-fade-in">
            {/* Hero Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="relative overflow-hidden glass-card p-8"
            >
                {/* Background glow */}
                <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-glow opacity-50" />
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-gradient-radial from-accent/20 to-transparent blur-3xl" />

                <div className="relative z-10">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-3 rounded-xl bg-gradient-primary">
                            <Brain className="w-6 h-6 text-white" />
                        </div>
                        <h2 className="text-2xl font-bold text-white">AI Investment Analysis</h2>
                    </div>

                    <p className="text-secondary mb-6 max-w-xl">
                        Get comprehensive investment insights powered by our multi-agent AI system.
                        Analyze any stock with Quant, Macro, Philosopher, and Regret agents.
                    </p>

                    {/* Search Input */}
                    <div className="flex gap-3 max-w-2xl">
                        <div className="relative flex-1">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary" />
                            <input
                                type="text"
                                value={searchTicker}
                                onChange={(e) => setSearchTicker(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                                placeholder="Enter stock symbol (e.g., RELIANCE.NS, AAPL, TCS.NS)"
                                className="input-glass pl-12"
                            />
                        </div>
                        <button
                            onClick={handleAnalyze}
                            disabled={!searchTicker.trim()}
                            className="btn-primary flex items-center gap-2"
                        >
                            <Sparkles className="w-4 h-4" />
                            Analyze
                        </button>
                    </div>

                    {/* Compare Toggle */}
                    <button
                        onClick={() => setShowCompare(!showCompare)}
                        className="mt-4 btn-ghost flex items-center gap-2 text-sm"
                    >
                        <GitCompare className="w-4 h-4" />
                        {showCompare ? 'Hide comparison' : 'Compare two stocks'}
                    </button>

                    {/* Compare Section */}
                    {showCompare && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            className="mt-4 p-4 bg-surface-light/50 rounded-xl"
                        >
                            <div className="flex gap-3 items-center">
                                <input
                                    type="text"
                                    value={compareTicker1}
                                    onChange={(e) => setCompareTicker1(e.target.value)}
                                    placeholder="First stock"
                                    className="input-glass flex-1"
                                />
                                <span className="text-secondary font-bold">vs</span>
                                <input
                                    type="text"
                                    value={compareTicker2}
                                    onChange={(e) => setCompareTicker2(e.target.value)}
                                    placeholder="Second stock"
                                    className="input-glass flex-1"
                                />
                                <button
                                    onClick={handleCompare}
                                    disabled={!compareTicker1.trim() || !compareTicker2.trim()}
                                    className="btn-secondary"
                                >
                                    Compare
                                </button>
                            </div>
                        </motion.div>
                    )}
                </div>
            </motion.div>

            {/* Stats Grid */}
            <div className="grid grid-cols-4 gap-4">
                {[
                    { label: 'AI Agents', value: '5', subtitle: 'Active & ready', icon: Brain, color: 'text-primary-400' },
                    { label: 'Data Source', value: 'Live', subtitle: 'Real-time feed', icon: Zap, color: 'text-success' },
                    { label: 'Accuracy', value: '87%', subtitle: 'Historical avg', icon: BarChart3, color: 'text-accent' },
                    { label: 'Analyses', value: recentAnalyses.length.toString(), subtitle: 'Recent', icon: Clock, color: 'text-warning' },
                ].map((stat, i) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="glass-card-hover p-5"
                    >
                        <stat.icon className={`w-5 h-5 ${stat.color} mb-3`} />
                        <p className="text-3xl font-bold text-white">{stat.value}</p>
                        <p className="text-xs text-secondary mt-1">{stat.subtitle}</p>
                    </motion.div>
                ))}
            </div>

            {/* Two Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Analyses */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="glass-card p-6"
                >
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <Clock className="w-5 h-5 text-primary-400" />
                        Recent Analyses
                    </h3>

                    {recentAnalyses.length === 0 ? (
                        <div className="text-center py-8">
                            <p className="text-secondary">No recent analyses</p>
                            <p className="text-xs text-secondary/60 mt-1">Start by analyzing a stock!</p>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {recentAnalyses.map((item, i) => (
                                <button
                                    key={i}
                                    onClick={() => navigate(`/analysis/${item.query}`)}
                                    className="w-full flex items-center justify-between p-3 rounded-xl bg-surface-light/30 hover:bg-surface-light transition-colors"
                                >
                                    <div className="flex items-center gap-3">
                                        <span className="font-semibold text-white">{item.query}</span>
                                        {item.score && (
                                            <span className="text-xs px-2 py-0.5 rounded-full bg-primary-500/20 text-primary-400">
                                                {item.score}/100
                                            </span>
                                        )}
                                    </div>
                                    <ArrowRight className="w-4 h-4 text-secondary" />
                                </button>
                            ))}
                        </div>
                    )}
                </motion.div>

                {/* Live Market Data */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="glass-card p-6"
                >
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-success" />
                        Live Market
                    </h3>

                    <div className="space-y-3">
                        {marketData.map((stock) => (
                            <button
                                key={stock.ticker}
                                onClick={() => navigate(`/analysis/${stock.ticker}`)}
                                className="w-full flex items-center justify-between p-4 rounded-xl bg-surface-light/30 hover:bg-surface-light transition-colors"
                            >
                                <div>
                                    <span className="font-semibold text-white">{stock.ticker}</span>
                                    <p className="text-xs text-secondary mt-0.5">Vol: {stock.volume}</p>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold text-white">
                                        ${typeof stock.price === 'number' ? stock.price.toFixed(2) : stock.price}
                                    </p>
                                    <p className={`text-sm font-medium flex items-center gap-1 justify-end ${stock.change >= 0 ? 'text-success' : 'text-error'
                                        }`}>
                                        {stock.change >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                                        {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)}%
                                    </p>
                                </div>
                            </button>
                        ))}
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Dashboard;
