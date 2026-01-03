import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { ArrowLeft, RefreshCw, Trophy, Minus, Dna } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { AnalysisLoadingScreen } from '../../components/AnalysisLoadingScreen';

interface ComparisonData {
    symbol: string;
    match_score?: number;
    recommendation?: string;
    agents?: Record<string, any>;
}

interface Dimension {
    name: string;
    stock1: number;
    stock2: number;
    description: string;
}

const StockComparison: React.FC = () => {
    const { symbol1, symbol2 } = useParams<{ symbol1: string; symbol2: string }>();
    const { token } = useAuth();
    const navigate = useNavigate();

    const [stock1Data, setStock1Data] = useState<ComparisonData | null>(null);
    const [stock2Data, setStock2Data] = useState<ComparisonData | null>(null);
    const [loading, setLoading] = useState(true);
    const [currentStep, setCurrentStep] = useState(0);
    const [error, setError] = useState('');
    const [useDNA, setUseDNA] = useState(true);

    useEffect(() => {
        if (symbol1 && symbol2) {
            runComparison();
        }
    }, [symbol1, symbol2]);

    // Simulate progress
    useEffect(() => {
        if (loading && currentStep < 11) {
            const timer = setTimeout(() => setCurrentStep(prev => prev + 1), 7000);
            return () => clearTimeout(timer);
        }
    }, [loading, currentStep]);

    const runComparison = async () => {
        setLoading(true);
        setCurrentStep(0);
        setError('');

        try {
            // Run both analyses in parallel
            const [res1, res2] = await Promise.all([
                axios.get(`http://localhost:8000/analyze/${symbol1}`, {
                    headers: { Authorization: `Bearer ${token}` }
                }),
                axios.get(`http://localhost:8000/analyze/${symbol2}`, {
                    headers: { Authorization: `Bearer ${token}` }
                })
            ]);

            setStock1Data({ symbol: symbol1!, ...res1.data });
            setStock2Data({ symbol: symbol2!, ...res2.data });
        } catch (err: any) {
            setError('Comparison failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const getDimensions = (): Dimension[] => {
        if (!stock1Data?.agents || !stock2Data?.agents) return [];

        const dims: Dimension[] = [
            {
                name: 'Overall Score',
                stock1: stock1Data.match_score || 0,
                stock2: stock2Data.match_score || 0,
                description: 'Combined AI agent assessment'
            },
            {
                name: 'Quant Score',
                stock1: stock1Data.agents['Quant Agent']?.output?.score || 50,
                stock2: stock2Data.agents['Quant Agent']?.output?.score || 50,
                description: 'Fundamental & valuation analysis'
            },
            {
                name: 'Macro Score',
                stock1: stock1Data.agents['Macro Agent']?.output?.score || 50,
                stock2: stock2Data.agents['Macro Agent']?.output?.score || 50,
                description: 'Macroeconomic environment fit'
            },
            {
                name: 'Philosophy Score',
                stock1: stock1Data.agents['Philosopher Agent']?.output?.score || 50,
                stock2: stock2Data.agents['Philosopher Agent']?.output?.score || 50,
                description: 'Long-term alignment & ethics'
            },
            {
                name: 'Regret Score',
                stock1: 100 - (stock1Data.agents['Regret Simulation Agent']?.output?.score || 50),
                stock2: 100 - (stock2Data.agents['Regret Simulation Agent']?.output?.score || 50),
                description: 'Risk-adjusted confidence (inverse of regret)'
            },
        ];

        return dims;
    };

    const getWinner = (s1: number, s2: number): 'stock1' | 'stock2' | 'tie' => {
        if (Math.abs(s1 - s2) < 3) return 'tie';
        return s1 > s2 ? 'stock1' : 'stock2';
    };

    const getActionColor = (action: string) => {
        switch (action?.toLowerCase()) {
            case 'buy': return 'text-success';
            case 'sell': return 'text-error';
            default: return 'text-warning';
        }
    };

    // Loading state
    if (loading) {
        const comparisonSteps = [
            { id: 'fetch1', label: `Fetching ${symbol1} data`, icon: null, status: 'pending' as const },
            { id: 'quant1', label: `${symbol1}: Quant Agent`, icon: null, status: 'pending' as const },
            { id: 'macro1', label: `${symbol1}: Macro Agent`, icon: null, status: 'pending' as const },
            { id: 'other1', label: `${symbol1}: Other Agents`, icon: null, status: 'pending' as const },
            { id: 'coach1', label: `${symbol1}: Coach Synthesis`, icon: null, status: 'pending' as const },
            { id: 'divider', label: '---', icon: null, status: 'pending' as const },
            { id: 'fetch2', label: `Fetching ${symbol2} data`, icon: null, status: 'pending' as const },
            { id: 'quant2', label: `${symbol2}: Quant Agent`, icon: null, status: 'pending' as const },
            { id: 'macro2', label: `${symbol2}: Macro Agent`, icon: null, status: 'pending' as const },
            { id: 'other2', label: `${symbol2}: Other Agents`, icon: null, status: 'pending' as const },
            { id: 'coach2', label: `${symbol2}: Coach Synthesis`, icon: null, status: 'pending' as const },
        ];

        return (
            <div className="min-h-[60vh] flex items-center justify-center">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="glass-card p-8 max-w-lg w-full text-center"
                >
                    <h2 className="text-2xl font-bold text-white mb-2">
                        Comparing <span className="text-gradient">{symbol1}</span>
                        {' '}vs{' '}
                        <span className="text-gradient-accent">{symbol2}</span>
                    </h2>
                    <p className="text-secondary mb-6">Running parallel AI analysis on both stocks</p>

                    <div className="flex justify-center gap-4">
                        <div className="spinner" />
                        <span className="text-primary-400">
                            Step {Math.min(currentStep + 1, 11)} of 11
                        </span>
                    </div>
                </motion.div>
            </div>
        );
    }

    const dimensions = getDimensions();

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <button onClick={() => navigate('/')} className="btn-ghost">
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back
                    </button>
                    <h1 className="text-2xl font-bold text-white">
                        Stock Comparison
                    </h1>
                </div>

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => setUseDNA(!useDNA)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all ${useDNA
                                ? 'bg-primary-500/20 text-primary-400 border border-primary-500/50'
                                : 'bg-surface-light text-secondary border border-glass-border'
                            }`}
                    >
                        <Dna className="w-4 h-4" />
                        DNA
                    </button>
                    <button onClick={runComparison} className="btn-secondary flex items-center gap-2">
                        <RefreshCw className="w-4 h-4" />
                        Re-compare
                    </button>
                </div>
            </div>

            {error && (
                <div className="p-4 bg-error/10 border border-error/30 rounded-xl text-error">
                    {error}
                </div>
            )}

            {stock1Data && stock2Data && (
                <>
                    {/* Head-to-head summary */}
                    <div className="grid grid-cols-3 gap-4">
                        {/* Stock 1 */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="glass-card p-6 text-center"
                        >
                            <h3 className="text-xl font-bold text-white mb-2">{symbol1}</h3>
                            <div className="text-5xl font-bold text-gradient mb-3">
                                {stock1Data.match_score || '--'}
                            </div>
                            <p className={`font-semibold ${getActionColor(stock1Data.recommendation || 'hold')}`}>
                                {stock1Data.recommendation || 'Hold'}
                            </p>
                        </motion.div>

                        {/* VS */}
                        <div className="flex items-center justify-center">
                            <div className="text-4xl font-bold text-secondary">VS</div>
                        </div>

                        {/* Stock 2 */}
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="glass-card p-6 text-center"
                        >
                            <h3 className="text-xl font-bold text-white mb-2">{symbol2}</h3>
                            <div className="text-5xl font-bold text-gradient-accent mb-3">
                                {stock2Data.match_score || '--'}
                            </div>
                            <p className={`font-semibold ${getActionColor(stock2Data.recommendation || 'hold')}`}>
                                {stock2Data.recommendation || 'Hold'}
                            </p>
                        </motion.div>
                    </div>

                    {/* Dimension-by-dimension comparison */}
                    <div className="glass-card p-6">
                        <h3 className="text-lg font-bold text-white mb-6">Dimension Breakdown</h3>

                        <div className="space-y-4">
                            {dimensions.map((dim, i) => {
                                const winner = getWinner(dim.stock1, dim.stock2);

                                return (
                                    <motion.div
                                        key={dim.name}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: i * 0.1 }}
                                        className="p-4 bg-surface-light/30 rounded-xl"
                                    >
                                        <div className="flex items-center justify-between mb-3">
                                            <div>
                                                <h4 className="font-semibold text-white">{dim.name}</h4>
                                                <p className="text-xs text-secondary">{dim.description}</p>
                                            </div>
                                            {winner !== 'tie' && (
                                                <div className={`flex items-center gap-1 text-sm ${winner === 'stock1' ? 'text-primary-400' : 'text-accent'
                                                    }`}>
                                                    <Trophy className="w-4 h-4" />
                                                    {winner === 'stock1' ? symbol1 : symbol2}
                                                </div>
                                            )}
                                            {winner === 'tie' && (
                                                <div className="flex items-center gap-1 text-sm text-secondary">
                                                    <Minus className="w-4 h-4" />
                                                    Tie
                                                </div>
                                            )}
                                        </div>

                                        {/* Score bars */}
                                        <div className="space-y-2">
                                            <div className="flex items-center gap-3">
                                                <span className="text-sm text-secondary w-20">{symbol1}</span>
                                                <div className="flex-1 h-3 bg-surface rounded-full overflow-hidden">
                                                    <motion.div
                                                        initial={{ width: 0 }}
                                                        animate={{ width: `${dim.stock1}%` }}
                                                        transition={{ duration: 1, delay: i * 0.1 }}
                                                        className="h-full bg-gradient-primary rounded-full"
                                                    />
                                                </div>
                                                <span className={`text-sm font-bold w-10 text-right ${winner === 'stock1' ? 'text-primary-400' : 'text-white'
                                                    }`}>
                                                    {dim.stock1}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-3">
                                                <span className="text-sm text-secondary w-20">{symbol2}</span>
                                                <div className="flex-1 h-3 bg-surface rounded-full overflow-hidden">
                                                    <motion.div
                                                        initial={{ width: 0 }}
                                                        animate={{ width: `${dim.stock2}%` }}
                                                        transition={{ duration: 1, delay: i * 0.1 }}
                                                        className="h-full bg-gradient-accent rounded-full"
                                                    />
                                                </div>
                                                <span className={`text-sm font-bold w-10 text-right ${winner === 'stock2' ? 'text-accent' : 'text-white'
                                                    }`}>
                                                    {dim.stock2}
                                                </span>
                                            </div>
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Final verdict */}
                    <div className="glass-card p-6 text-center">
                        <h3 className="text-lg font-bold text-white mb-4">Overall Winner</h3>
                        {(() => {
                            const s1 = stock1Data.match_score || 0;
                            const s2 = stock2Data.match_score || 0;
                            const winner = getWinner(s1, s2);

                            if (winner === 'tie') {
                                return (
                                    <p className="text-2xl text-secondary">
                                        Both stocks are comparable. Consider your specific goals.
                                    </p>
                                );
                            }

                            const winnerSymbol = winner === 'stock1' ? symbol1 : symbol2;
                            const winnerScore = winner === 'stock1' ? s1 : s2;
                            const loserScore = winner === 'stock1' ? s2 : s1;

                            return (
                                <div>
                                    <div className="flex items-center justify-center gap-3 mb-2">
                                        <Trophy className="w-8 h-8 text-warning" />
                                        <span className="text-3xl font-bold text-gradient">
                                            {winnerSymbol}
                                        </span>
                                    </div>
                                    <p className="text-secondary">
                                        Leads by {winnerScore - loserScore} points ({winnerScore} vs {loserScore})
                                    </p>
                                </div>
                            );
                        })()}
                    </div>
                </>
            )}
        </div>
    );
};

export default StockComparison;
