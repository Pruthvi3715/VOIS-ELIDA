import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Clock, Award, Loader2 } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import AgentCard from '../../components/AgentCard';
import PriceHistoryChart from '../../components/PriceHistoryChart.tsx';

// Currency symbol based on stock exchange
const getCurrencySymbol = (ticker: string): string => {
    const upperTicker = ticker.toUpperCase();
    if (upperTicker.endsWith('.NS') || upperTicker.endsWith('.BO')) {
        return '₹';
    }
    return '$';
};

interface HistoryItem {
    id: number;
    query: string;
    query_type: string;
    timestamp: string;
    result?: any;
}

const HistoryDetailPage: React.FC = () => {
    const { id: historyId } = useParams<{ id: string }>();
    const location = useLocation();
    const navigate = useNavigate();
    const { token } = useAuth();

    // Get history item from navigation state OR fetch from API
    const stateItem = (location.state as { historyItem?: HistoryItem })?.historyItem;

    const [historyItem, setHistoryItem] = useState<HistoryItem | null>(stateItem || null);
    const [loading, setLoading] = useState(!stateItem?.result);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // If we already have full result, no need to fetch
        if (stateItem?.result) {
            setHistoryItem(stateItem);
            setLoading(false);
            return;
        }

        // Fetch from API
        const fetchEntry = async () => {
            try {
                setLoading(true);
                const response = await axios.get(`http://localhost:8000/api/v1/history/${historyId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setHistoryItem(response.data);
            } catch (err) {
                console.error('Failed to fetch history entry:', err);
                setError('Failed to load analysis');
            } finally {
                setLoading(false);
            }
        };

        if (historyId) {
            fetchEntry();
        }
    }, [historyId, token, stateItem]);

    const analysis = historyItem?.result;
    const symbol = historyItem?.query || '';

    if (loading) {
        return (
            <div className="space-y-6 animate-fade-in">
                <button onClick={() => navigate('/history')} className="btn-ghost flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Back to History
                </button>
                <div className="flex items-center justify-center py-24">
                    <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
                </div>
            </div>
        );
    }

    if (error || !analysis) {
        return (
            <div className="space-y-6 animate-fade-in">
                <button onClick={() => navigate('/history')} className="btn-ghost flex items-center gap-2">
                    <ArrowLeft className="w-4 h-4" /> Back to History
                </button>
                <div className="glass-card p-12 text-center">
                    <Clock className="w-16 h-16 text-secondary/30 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">Analysis not found</h3>
                    <p className="text-secondary">{error || 'The saved analysis could not be loaded.'}</p>
                </div>
            </div>
        );
    }

    const getActionColor = (action: string) => {
        switch (action?.toLowerCase()) {
            case 'buy': return 'text-success bg-success/10 border-success/30';
            case 'sell': return 'text-error bg-error/10 border-error/30';
            default: return 'text-warning bg-warning/10 border-warning/30';
        }
    };

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <button onClick={() => navigate('/history')} className="btn-ghost flex items-center gap-2">
                        <ArrowLeft className="w-4 h-4" /> Back
                    </button>
                    <div>
                        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                            {symbol}
                            <span className="text-lg text-secondary font-normal">Saved Analysis</span>
                        </h1>
                        <p className="text-sm text-secondary flex items-center gap-2 mt-1">
                            <Clock className="w-4 h-4" />
                            Saved on {new Date(historyItem?.timestamp || '').toLocaleString()}
                        </p>
                    </div>
                </div>
            </div>

            {/* Coach Summary Card */}
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                <div className="glass-card p-6 relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-primary-500/5 via-transparent to-success/5 pointer-events-none" />

                    <div className="relative z-10">
                        <div className="flex items-start justify-between">
                            <div className="flex items-center gap-4">
                                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-500/30 to-primary-600/20 flex items-center justify-center border border-primary-500/20">
                                    <Award className="w-7 h-7 text-primary-400" />
                                </div>
                                <div>
                                    <h2 className="text-2xl font-bold text-white">Coach's Verdict</h2>
                                    <p className="text-secondary text-sm mt-0.5">
                                        Final synthesis combining quantitative execution, macro trends, and philosophical alignment.
                                    </p>
                                </div>
                            </div>

                            {/* Score */}
                            <div className="flex flex-col items-end gap-2">
                                <div className="text-5xl font-bold text-white">
                                    {analysis.match_score || 50}
                                </div>
                                <span className={`px-4 py-1 rounded-full text-sm font-bold border ${getActionColor(analysis.recommendation || 'hold')}`}>
                                    {analysis.recommendation || 'Hold'}
                                </span>
                            </div>
                        </div>

                        {/* Summary */}
                        <div className="mt-6 p-5 bg-surface-dark/40 rounded-xl border border-glass-border">
                            <p className="text-lg text-white/90 leading-relaxed font-light">
                                {analysis.summary || analysis.match_result?.summary}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Price History Chart */}
                {(analysis.market_data?.history || analysis.market_data?.technicals?.history) && (
                    <div className="mb-8">
                        <PriceHistoryChart
                            data={analysis.market_data?.history || analysis.market_data?.technicals?.history}
                            currencySymbol={getCurrencySymbol(symbol)}
                        />
                    </div>
                )}

                {/* Agent Cards Grid */}
                <div>
                    <h3 className="text-xl font-bold text-white mb-4">Agent Analysis</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {(() => {
                            const getAgentData = (source: any, key: string) => {
                                if (!source) return null;
                                if (source[key.toLowerCase()]) return source[key.toLowerCase()];
                                if (source[key]) return source[key];
                                if (source[`${key} Agent`]) return source[`${key} Agent`];
                                return null;
                            };

                            const agents = ['Quant', 'Macro', 'Philosopher', 'Regret'];
                            return agents.map(name => {
                                const source = analysis.results || analysis.agents;
                                const data = getAgentData(source, name);
                                if (!data) return null;

                                return (
                                    <AgentCard
                                        key={name}
                                        name={`${name} Agent`}
                                        score={data.score || data.output?.score || 50}
                                        confidence={data.confidence || 75}
                                        analysis={data.analysis || data.output?.reasoning || data.output?.analysis || ''}
                                        strengths={data.output?.strengths || []}
                                        weaknesses={data.output?.weaknesses || []}
                                        metricsUsed={data.output?.metrics_used || []}
                                        metricsValues={data.output?.metrics_values || {}}
                                        dataQuality={data.data_quality || 'Medium'}
                                        fallbackUsed={data.fallback_used || false}
                                    />
                                );
                            });
                        })()}
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default HistoryDetailPage;
