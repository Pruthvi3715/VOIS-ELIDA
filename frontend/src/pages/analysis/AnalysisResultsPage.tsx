import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { ArrowLeft, Play, Dna, TrendingUp, AlertTriangle, Target, Award, Save, Check, Loader2 as SpinLoader } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { AnalysisLoadingScreen, defaultSteps } from '../../components/AnalysisLoadingScreen';
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

interface AnalysisResult {
    match_score: number;
    recommendation: string;
    summary: string;
    risk_level: string;
    agents?: Record<string, any>;
    results?: Record<string, any>; // Add this to support backend format
    coach_verdict?: any;
    data_quality?: any;
    market_data?: any;
    [key: string]: any; // Allow other properties
}

const AnalysisResultsPage: React.FC = () => {
    const { symbol } = useParams<{ symbol: string }>();
    const { token } = useAuth();
    const navigate = useNavigate();

    const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);
    const [error, setError] = useState('');
    const [useDNA, setUseDNA] = useState(true);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);

    const handleSave = async () => {
        if (!analysis || !token || saved) return;
        setSaving(true);
        try {
            await axios.post('http://localhost:8000/api/v1/history', {
                query_type: 'analysis',
                query: symbol,
                result: analysis
            }, { headers: { Authorization: `Bearer ${token}` } });
            setSaved(true);
        } catch (err) {
            console.error('Failed to save history', err);
        } finally {
            setSaving(false);
        }
    };

    // Simulated step progress during analysis
    useEffect(() => {
        if (loading && currentStep < defaultSteps.length - 1) {
            const timer = setTimeout(() => {
                setCurrentStep(prev => Math.min(prev + 1, defaultSteps.length - 1));
            }, 1200 + Math.random() * 800); // Faster, snappy progress
            return () => clearTimeout(timer);
        }
    }, [loading, currentStep]);

    const runAnalysis = async () => {
        if (!symbol) return;

        setLoading(true);
        setCurrentStep(0);
        setError('');
        setAnalysis(null);

        try {
            const response = await axios.get(`http://localhost:8000/analyze/${symbol}`, {
                headers: { Authorization: `Bearer ${token}` },
                timeout: 300000 // 300 seconds (5 mins) timeout for local LLM analysis
            });
            setAnalysis(response.data);
            setCurrentStep(defaultSteps.length);
        } catch (err: any) {
            console.error('Analysis error:', err); // Log for debugging
            setError(err.response?.data?.detail || err.message || 'Analysis failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    // Auto-run analysis on mount if no data
    useEffect(() => {
        if (!analysis && !loading && symbol) {
            runAnalysis();
        }
    }, [symbol]);

    const getActionColor = (action: string) => {
        switch (action?.toLowerCase()) {
            case 'buy': return 'text-success bg-success/10 border-success/30';
            case 'sell': return 'text-error bg-error/10 border-error/30';
            default: return 'text-warning bg-warning/10 border-warning/30';
        }
    };

    // Show loading screen
    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <AnalysisLoadingScreen
                    symbol={symbol || ''}
                    steps={defaultSteps}
                    currentStep={currentStep}
                    error={error}
                />
            </div>
        );
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => navigate('/')}
                        className="btn-ghost flex items-center gap-2"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        Back
                    </button>
                    <div>
                        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                            {symbol}
                            <span className="text-lg text-secondary font-normal">Analysis</span>
                        </h1>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    {/* DNA Toggle */}
                    <button
                        onClick={() => setUseDNA(!useDNA)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all ${useDNA
                            ? 'bg-primary-500/20 text-primary-400 border border-primary-500/50'
                            : 'bg-surface-light text-secondary border border-glass-border'
                            }`}
                    >
                        <Dna className="w-4 h-4" />
                        <span className="text-sm font-medium">Investor DNA</span>
                    </button>

                    {/* Save Button */}
                    {analysis && (
                        <button
                            onClick={handleSave}
                            disabled={saving || saved}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl border transition-all ${saved
                                ? 'bg-success/10 text-success border-success/30'
                                : 'bg-surface-light text-secondary hover:text-white border-glass-border hover:border-primary-500/50'
                                }`}
                        >
                            {saving ? (
                                <SpinLoader className="w-4 h-4 animate-spin" />
                            ) : saved ? (
                                <Check className="w-4 h-4" />
                            ) : (
                                <Save className="w-4 h-4" />
                            )}
                            <span className="text-sm font-medium">{saved ? 'Saved' : 'Save'}</span>
                        </button>
                    )}

                    {/* Re-run button */}
                    <button
                        onClick={runAnalysis}
                        disabled={loading}
                        className="btn-primary flex items-center gap-2"
                    >
                        <Play className="w-4 h-4" />
                        Re-analyze
                    </button>
                </div>
            </div>

            {/* Error */}
            {error && !loading && (
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-4 bg-error/10 border border-error/30 rounded-xl text-error"
                >
                    {error}
                </motion.div>
            )}

            {/* Results */}
            {analysis && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="space-y-6"
                >
                    {/* Coach Summary Card */}
                    <div className="glass-card p-6 relative overflow-hidden">
                        {/* Background glow */}
                        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-glow opacity-30" />

                        <div className="relative z-10">
                            <div className="flex flex-col md:flex-row items-start justify-between gap-6">
                                <div className="flex items-center gap-4">
                                    <div className="p-4 rounded-2xl bg-gradient-primary shadow-glow">
                                        <Award className="w-10 h-10 text-white" />
                                    </div>
                                    <div>
                                        <h2 className="text-2xl font-bold text-white">Coach's Verdict</h2>
                                        <p className="text-secondary mt-1 max-w-md">
                                            Final synthesis combining quantitative execution, macro trends, and philosophical alignment.
                                        </p>
                                    </div>
                                </div>

                                {/* Score and Action */}
                                <div className="text-right">
                                    <div className="text-6xl font-bold text-gradient mb-2 drop-shadow-lg">
                                        {analysis.match_score || analysis.match_result?.score || '--'}
                                    </div>
                                    <div className={`inline-block px-5 py-2 rounded-full text-base font-bold border ${getActionColor(analysis.recommendation || analysis.match_result?.recommendation || 'hold')}`}>
                                        {analysis.recommendation || analysis.match_result?.recommendation || 'Hold'}
                                    </div>
                                </div>
                            </div>

                            {/* Action Scenarios */}
                            {(analysis.match_result?.action_if_owned || analysis.match_result?.action_if_not_owned) && (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
                                    <div className="p-4 rounded-xl bg-surface-light/40 border border-glass-border">
                                        <h4 className="text-xs uppercase tracking-wider text-secondary mb-2 font-semibold">If You Own It</h4>
                                        <p className="text-white font-medium">
                                            {analysis.match_result?.action_if_owned || 'Hold current position'}
                                        </p>
                                    </div>
                                    <div className="p-4 rounded-xl bg-surface-light/40 border border-glass-border">
                                        <h4 className="text-xs uppercase tracking-wider text-secondary mb-2 font-semibold">If You Don't Own It</h4>
                                        <p className="text-white font-medium">
                                            {analysis.match_result?.action_if_not_owned || 'Wait for entry'}
                                        </p>
                                    </div>
                                </div>
                            )}

                            {/* Summary */}
                            <div className="mt-6 p-5 bg-surface-dark/40 rounded-xl border border-glass-border">
                                <p className="text-lg text-white/90 leading-relaxed font-light">
                                    {analysis.summary || analysis.match_result?.summary}
                                </p>
                            </div>

                            {/* Fit vs Concerns Grid */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                                {/* Fit Reasons */}
                                {analysis.match_result?.fit_reasons && analysis.match_result.fit_reasons.length > 0 && (
                                    <div>
                                        <h4 className="text-success font-bold mb-4 flex items-center gap-2">
                                            <TrendingUp className="w-5 h-5" /> Why it fits
                                        </h4>
                                        <ul className="space-y-3">
                                            {analysis.match_result.fit_reasons.map((reason: string, i: number) => (
                                                <li key={i} className="flex items-start gap-3 text-secondary/90 bg-success/5 p-3 rounded-lg border border-success/10">
                                                    <div className="mt-1 w-1.5 h-1.5 rounded-full bg-success flex-shrink-0" />
                                                    <span className="text-sm">{reason}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Concerns */}
                                {analysis.match_result?.concern_reasons && analysis.match_result.concern_reasons.length > 0 && (
                                    <div>
                                        <h4 className="text-error font-bold mb-4 flex items-center gap-2">
                                            <AlertTriangle className="w-5 h-5" /> Risks to watch
                                        </h4>
                                        <ul className="space-y-3">
                                            {analysis.match_result.concern_reasons.map((reason: string, i: number) => (
                                                <li key={i} className="flex items-start gap-3 text-secondary/90 bg-error/5 p-3 rounded-lg border border-error/10">
                                                    <div className="mt-1 w-1.5 h-1.5 rounded-full bg-error flex-shrink-0" />
                                                    <span className="text-sm">{reason}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Price History Chart */}
                    {(analysis.market_data?.history || analysis.market_data?.technicals?.history) && (
                        <div className="mb-8">
                            <PriceHistoryChart
                                data={analysis.market_data?.history || analysis.market_data?.technicals?.history}
                                currencySymbol={getCurrencySymbol(symbol || '')}
                            />
                        </div>
                    )}

                    {/* Agent Cards Grid */}
                    <div>
                        <h3 className="text-xl font-bold text-white mb-4">Agent Analysis</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {(() => {
                                // Helper to normalize agent data
                                const getAgentData = (source: any, key: string) => {
                                    if (!source) return null;
                                    // Try lowercase first (backend format)
                                    if (source[key.toLowerCase()]) return source[key.toLowerCase()];
                                    // Try Capitalized
                                    if (source[key]) return source[key];
                                    // Try with " Agent" suffix
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

                    {/* Data Quality Indicator */}
                    {analysis.data_quality && (
                        <div className="glass-card p-4">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-secondary">Data Quality</span>
                                <div className="flex items-center gap-2">
                                    <div className={`w-2 h-2 rounded-full ${analysis.data_quality.overall === 'High' ? 'bg-success' :
                                        analysis.data_quality.overall === 'Medium' ? 'bg-warning' :
                                            'bg-error'
                                        }`} />
                                    <span className="text-sm font-medium text-white">
                                        {analysis.data_quality.overall}
                                    </span>
                                </div>
                            </div>
                        </div>
                    )}
                </motion.div>
            )}

            {/* No analysis yet */}
            {!analysis && !loading && !error && (
                <div className="glass-card p-12 text-center">
                    <Target className="w-16 h-16 text-secondary mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">Ready to Analyze</h3>
                    <p className="text-secondary mb-6">
                        Click the button below to run AI-powered analysis for {symbol}
                    </p>
                    <button onClick={runAnalysis} className="btn-primary">
                        <Play className="w-4 h-4 mr-2 inline" />
                        Run Analysis
                    </button>
                </div>
            )}
        </div>
    );
};

export default AnalysisResultsPage;
