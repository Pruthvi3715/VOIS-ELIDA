import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Scale, Search, ArrowRight, TrendingUp, X } from 'lucide-react';

const POPULAR_STOCKS = [
    { symbol: 'AAPL', name: 'Apple Inc.' },
    { symbol: 'MSFT', name: 'Microsoft' },
    { symbol: 'GOOGL', name: 'Alphabet' },
    { symbol: 'TSLA', name: 'Tesla' },
    { symbol: 'RELIANCE.NS', name: 'Reliance Industries' },
    { symbol: 'TCS.NS', name: 'Tata Consultancy' },
    { symbol: 'INFY.NS', name: 'Infosys' },
    { symbol: 'HDFCBANK.NS', name: 'HDFC Bank' },
];

const ComparePage: React.FC = () => {
    const navigate = useNavigate();
    const [stock1, setStock1] = useState('');
    const [stock2, setStock2] = useState('');
    const [focused, setFocused] = useState<1 | 2 | null>(null);

    const handleCompare = () => {
        if (stock1.trim() && stock2.trim()) {
            navigate(`/compare/${stock1.trim().toUpperCase()}/${stock2.trim().toUpperCase()}`);
        }
    };

    const selectStock = (symbol: string) => {
        if (focused === 1) {
            setStock1(symbol);
        } else if (focused === 2) {
            setStock2(symbol);
        } else if (!stock1) {
            setStock1(symbol);
        } else if (!stock2) {
            setStock2(symbol);
        }
        setFocused(null);
    };

    const clearStock = (which: 1 | 2) => {
        if (which === 1) setStock1('');
        else setStock2('');
    };

    return (
        <div className="space-y-8 animate-fade-in">
            {/* Header */}
            <div className="text-center">
                <div className="inline-flex items-center justify-center p-4 rounded-2xl bg-gradient-to-br from-primary-500/20 to-accent/20 border border-primary-500/30 mb-4">
                    <Scale className="w-8 h-8 text-primary-400" />
                </div>
                <h1 className="text-3xl font-bold text-white mb-2">Compare Stocks</h1>
                <p className="text-secondary max-w-md mx-auto">
                    Select two stocks to compare side-by-side with AI-powered analysis
                </p>
            </div>

            {/* Stock Selection Cards */}
            <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
                {/* Stock 1 */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="glass-card p-6"
                >
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-full bg-primary-500/20 flex items-center justify-center text-primary-400 text-sm font-bold">1</span>
                        First Stock
                    </h3>
                    <div className="relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary" />
                        <input
                            type="text"
                            value={stock1}
                            onChange={(e) => setStock1(e.target.value.toUpperCase())}
                            onFocus={() => setFocused(1)}
                            onKeyDown={(e) => e.key === 'Enter' && handleCompare()}
                            placeholder="Enter symbol (e.g., AAPL)"
                            className="input-glass pl-12 pr-10"
                        />
                        {stock1 && (
                            <button
                                onClick={() => clearStock(1)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded transition"
                            >
                                <X className="w-4 h-4 text-secondary" />
                            </button>
                        )}
                    </div>
                </motion.div>

                {/* Stock 2 */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="glass-card p-6"
                >
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent text-sm font-bold">2</span>
                        Second Stock
                    </h3>
                    <div className="relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary" />
                        <input
                            type="text"
                            value={stock2}
                            onChange={(e) => setStock2(e.target.value.toUpperCase())}
                            onFocus={() => setFocused(2)}
                            onKeyDown={(e) => e.key === 'Enter' && handleCompare()}
                            placeholder="Enter symbol (e.g., MSFT)"
                            className="input-glass pl-12 pr-10"
                        />
                        {stock2 && (
                            <button
                                onClick={() => clearStock(2)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-white/10 rounded transition"
                            >
                                <X className="w-4 h-4 text-secondary" />
                            </button>
                        )}
                    </div>
                </motion.div>
            </div>

            {/* Compare Button */}
            <div className="text-center">
                <button
                    onClick={handleCompare}
                    disabled={!stock1.trim() || !stock2.trim()}
                    className="btn-primary inline-flex items-center gap-3 px-8 py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <Scale className="w-5 h-5" />
                    Compare Stocks
                    <ArrowRight className="w-5 h-5" />
                </button>
            </div>

            {/* Popular Stocks */}
            <div className="glass-card p-6 max-w-4xl mx-auto">
                <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-success" />
                    Popular Stocks
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {POPULAR_STOCKS.map((stock) => (
                        <button
                            key={stock.symbol}
                            onClick={() => selectStock(stock.symbol)}
                            disabled={stock.symbol === stock1 || stock.symbol === stock2}
                            className={`p-4 rounded-xl border transition-all text-left ${stock.symbol === stock1 || stock.symbol === stock2
                                    ? 'bg-primary-500/20 border-primary-500/50 cursor-default'
                                    : 'bg-surface-light border-white/10 hover:border-primary-500/30 hover:bg-white/5'
                                }`}
                        >
                            <p className="font-bold text-white">{stock.symbol}</p>
                            <p className="text-xs text-secondary truncate">{stock.name}</p>
                        </button>
                    ))}
                </div>
            </div>

            {/* Instructions */}
            <div className="text-center text-secondary text-sm max-w-lg mx-auto">
                <p>
                    Select two stocks to compare their match scores, recommendations,
                    and multi-agent analysis side by side.
                </p>
            </div>
        </div>
    );
};

export default ComparePage;
