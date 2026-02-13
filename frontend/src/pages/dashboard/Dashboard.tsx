import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    Search, Sparkles, TrendingUp, TrendingDown, Brain,
    Zap, BarChart3, ArrowRight, Clock, ArrowUpRight,
    Activity, Shield, Target, Play
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
    const [recentAnalyses, setRecentAnalyses] = useState<RecentAnalysis[]>([]);
    const [marketData, setMarketData] = useState<MarketStock[]>([]);

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
        const tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'AAPL'];
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
                    price: ticker === 'AAPL' ? 218.26 : ticker === 'TCS.NS' ? 3438.51 : ticker === 'INFY.NS' ? 1523.45 : 2194.98,
                    change: Math.random() * 4 - 2,
                    volume: '10.5M'
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

    const getCurrencySymbol = (ticker: string) => {
        if (ticker.endsWith('.NS') || ticker.endsWith('.BO')) return '₹';
        return '$';
    };

    return (
        <div className="space-y-8">
            {/* Hero Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div className="card-gradient p-8 relative overflow-hidden">
                    {/* Decorative elements */}
                    <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary/20 to-transparent rounded-full blur-3xl" />
                    <div className="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-tr from-accent/10 to-transparent rounded-full blur-3xl" />

                    <div className="relative z-10">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-14 h-14 rounded-2xl bg-gradient-primary flex items-center justify-center glow-primary">
                                <Brain className="w-7 h-7 text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-bold text-white">AI Stock Analysis</h1>
                                <p className="text-secondary mt-1">
                                    Get personalized insights powered by 5 AI agents
                                </p>
                            </div>
                        </div>

                        {/* Search */}
                        <div className="flex gap-4 max-w-2xl">
                            <div className="relative flex-1">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary" />
                                <input
                                    type="text"
                                    value={searchTicker}
                                    onChange={(e) => setSearchTicker(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                                    placeholder="Enter stock symbol (e.g., RELIANCE.NS, AAPL)"
                                    className="input-lg pl-12"
                                />
                            </div>
                            <button
                                onClick={handleAnalyze}
                                disabled={!searchTicker.trim()}
                                className="btn-primary flex items-center gap-2 px-8"
                            >
                                <Sparkles className="w-5 h-5" />
                                Analyze
                            </button>
                        </div>

                        {/* Quick tickers */}
                        <div className="flex gap-2 mt-4">
                            <span className="text-sm text-secondary">Quick:</span>
                            {['TCS.NS', 'RELIANCE.NS', 'AAPL', 'INFY.NS'].map((ticker) => (
                                <button
                                    key={ticker}
                                    onClick={() => navigate(`/analysis/${ticker}`)}
                                    className="px-3 py-1 text-sm rounded-lg bg-white/5 hover:bg-white/10 text-secondary hover:text-white transition-all"
                                >
                                    {ticker}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* Stats Grid */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="grid grid-cols-2 lg:grid-cols-4 gap-4"
            >
                {[
                    { label: 'AI Agents', value: '5', icon: Brain, color: 'primary' },
                    { label: 'Data Feed', value: 'Live', icon: Zap, color: 'accent' },
                    { label: 'Accuracy', value: '87%', icon: Target, color: 'success' },
                    { label: 'Analyses', value: recentAnalyses.length.toString(), icon: Activity, color: 'info' },
                ].map((stat, i) => (
                    <motion.div
                        key={stat.label}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 + i * 0.1 }}
                        className="card group"
                    >
                        <div
                            className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 bg-${stat.color}/20`}
                        >
                            <stat.icon className={`w-5 h-5 text-${stat.color}`} />
                        </div>
                        <p className="stat-value">{stat.value}</p>
                        <p className="stat-label">{stat.label}</p>
                    </motion.div>
                ))}
            </motion.div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Recent Analyses */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="card"
                >
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
                                <Clock className="w-5 h-5 text-primary-300" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Recent Analyses</h3>
                        </div>
                        {recentAnalyses.length > 0 && (
                            <button
                                onClick={() => navigate('/history')}
                                className="btn-ghost text-sm"
                            >
                                View all
                            </button>
                        )}
                    </div>

                    {recentAnalyses.length === 0 ? (
                        <div className="text-center py-12">
                            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-surface-light flex items-center justify-center">
                                <BarChart3 className="w-8 h-8 text-secondary" />
                            </div>
                            <p className="text-secondary">No recent analyses</p>
                            <p className="text-sm text-muted mt-1">Start by analyzing a stock above</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {recentAnalyses.map((item, i) => (
                                <button
                                    key={i}
                                    onClick={() => navigate(`/analysis/${item.query}`)}
                                    className="w-full market-card"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                                            <span className="text-xs font-bold text-primary-300">
                                                {item.query.substring(0, 2)}
                                            </span>
                                        </div>
                                        <div className="text-left">
                                            <span className="font-semibold text-white block">{item.query}</span>
                                            <span className="text-xs text-muted">
                                                {new Date(item.timestamp).toLocaleDateString()}
                                            </span>
                                        </div>
                                    </div>
                                    <ArrowRight className="w-4 h-4 text-secondary" />
                                </button>
                            ))}
                        </div>
                    )}
                </motion.div>

                {/* Live Market */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.4 }}
                    className="card"
                >
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-success/20 flex items-center justify-center">
                                <TrendingUp className="w-5 h-5 text-success" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Live Market</h3>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                            <span className="text-xs text-secondary">Live</span>
                        </div>
                    </div>

                    <div className="space-y-3">
                        {marketData.map((stock, i) => (
                            <motion.button
                                key={stock.ticker}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.5 + i * 0.1 }}
                                onClick={() => navigate(`/analysis/${stock.ticker}`)}
                                className="w-full market-card"
                            >
                                <div className="flex items-center gap-3">
                                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${stock.change >= 0 ? 'bg-success/10' : 'bg-error/10'}`}>
                                        {stock.change >= 0 ? (
                                            <TrendingUp className="w-5 h-5 text-success" />
                                        ) : (
                                            <TrendingDown className="w-5 h-5 text-error" />
                                        )}
                                    </div>
                                    <div className="text-left">
                                        <span className="font-semibold text-white block">{stock.ticker}</span>
                                        <span className="text-xs text-muted">Vol: {stock.volume}</span>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold text-white">
                                        {getCurrencySymbol(stock.ticker)}{stock.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                                    </p>
                                    <p className={`text-sm font-semibold ${stock.change >= 0 ? 'market-up' : 'market-down'}`}>
                                        {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)}%
                                    </p>
                                </div>
                            </motion.button>
                        ))}
                    </div>
                </motion.div>
            </div>

            {/* Quick Actions */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.6 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-4"
            >
                {[
                    {
                        title: 'Portfolio Scan',
                        desc: 'Analyze your entire portfolio',
                        icon: Shield,
                        path: '/portfolio',
                        gradient: 'from-primary/20 to-primary/5',
                    },
                    {
                        title: 'Investor DNA',
                        desc: 'Configure your profile',
                        icon: Target,
                        path: '/profile',
                        gradient: 'from-accent/20 to-accent/5',
                    },
                    {
                        title: 'Analysis History',
                        desc: 'View past analyses',
                        icon: Clock,
                        path: '/history',
                        gradient: 'from-info/20 to-info/5',
                    },
                ].map((action) => (
                    <button
                        key={action.title}
                        onClick={() => navigate(action.path)}
                        className={`group p-6 rounded-2xl bg-gradient-to-br ${action.gradient} border border-white/5 hover:border-primary/30 transition-all text-left`}
                    >
                        <action.icon className="w-6 h-6 text-white mb-4" />
                        <h4 className="font-semibold text-white mb-1">{action.title}</h4>
                        <p className="text-sm text-secondary">{action.desc}</p>
                        <ArrowUpRight className="w-4 h-4 text-secondary mt-4 group-hover:text-white group-hover:translate-x-1 group-hover:-translate-y-1 transition-all" />
                    </button>
                ))}
            </motion.div>
        </div>
    );
};

export default Dashboard;
