import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Sparkles, Loader2, Save, CheckCircle, Search, Zap } from 'lucide-react';
import { API_BASE_URL, getUserId, retrieveContext, ingestAsset } from '../api';
import Chatbot from '../components/Chatbot';
import MatchScoreCard from '../components/MatchScoreCard';
import AgentDeepDive from '../components/AgentDeepDive';
import RegretWarningBox from '../components/RegretWarningBox';

function AnalysisPage() {
    const { symbol } = useParams();
    const navigate = useNavigate();
    const [searchTicker, setSearchTicker] = useState(symbol || '');
    const [analysisData, setAnalysisData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);

    // Popular stocks for quick analysis
    const popularStocks = [
        { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology' },
        { symbol: 'MSFT', name: 'Microsoft', sector: 'Technology' },
        { symbol: 'GOOGL', name: 'Alphabet', sector: 'Technology' },
        { symbol: 'TSLA', name: 'Tesla', sector: 'Automotive' },
        { symbol: 'NVDA', name: 'NVIDIA', sector: 'Semiconductors' },
        { symbol: 'RELIANCE.NS', name: 'Reliance Industries', sector: 'Conglomerate' },
        { symbol: 'TCS.NS', name: 'Tata Consultancy', sector: 'IT Services' },
        { symbol: 'INFY.NS', name: 'Infosys', sector: 'IT Services' },
    ];

    // If no symbol provided, show enhanced search interface
    if (!symbol) {
        return (
            <div className="space-y-8 animate-fade-in">
                {/* Hero Section */}
                <div className="text-center py-8">
                    <div className="inline-flex items-center justify-center p-4 rounded-2xl bg-gradient-to-br from-primary-500/20 to-accent/20 border border-primary-500/30 mb-6">
                        <Sparkles className="w-10 h-10 text-amber-400" />
                    </div>
                    <h1 className="text-4xl font-bold text-white mb-3">
                        AI-Powered Stock Analysis
                    </h1>
                    <p className="text-secondary text-lg max-w-2xl mx-auto">
                        Get comprehensive investment insights from our multi-agent AI system.
                        Analyze any stock with quantitative, macro, philosophical, and risk perspectives.
                    </p>
                </div>

                {/* Search Card */}
                <div className="glass-card p-8 max-w-3xl mx-auto relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-accent/5" />

                    <div className="relative z-10">
                        <div className="flex gap-3">
                            <div className="flex-1 relative">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                                <input
                                    type="text"
                                    value={searchTicker}
                                    onChange={(e) => setSearchTicker(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && searchTicker.trim() && navigate(`/analysis/${searchTicker.trim().toUpperCase()}`)}
                                    placeholder="Enter stock symbol (e.g., AAPL, TSLA, RELIANCE.NS)"
                                    className="input-glass pl-12 text-lg py-4"
                                />
                            </div>
                            <button
                                onClick={() => searchTicker.trim() && navigate(`/analysis/${searchTicker.trim().toUpperCase()}`)}
                                disabled={!searchTicker.trim()}
                                className="btn-primary px-8 py-4 text-lg flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Zap className="w-5 h-5 fill-current" />
                                Analyze
                            </button>
                        </div>
                    </div>
                </div>

                {/* Popular Stocks Grid */}
                <div className="glass-card p-6">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <span className="text-2xl">🔥</span>
                        Popular Stocks
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {popularStocks.map((stock) => (
                            <button
                                key={stock.symbol}
                                onClick={() => navigate(`/analysis/${stock.symbol}`)}
                                className="p-4 rounded-xl bg-surface-light border border-white/10 hover:border-primary-500/50 hover:bg-white/5 transition-all text-left group"
                            >
                                <p className="font-bold text-white group-hover:text-primary-400 transition-colors">
                                    {stock.symbol}
                                </p>
                                <p className="text-sm text-secondary truncate">{stock.name}</p>
                                <p className="text-xs text-gray-500 mt-1">{stock.sector}</p>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Features Grid */}
                <div className="grid md:grid-cols-4 gap-4">
                    <div className="glass-card p-5 text-center">
                        <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center mx-auto mb-3">
                            <span className="text-2xl">📊</span>
                        </div>
                        <h4 className="font-semibold text-white mb-1">Quant Analysis</h4>
                        <p className="text-sm text-secondary">Financial metrics & valuation</p>
                    </div>
                    <div className="glass-card p-5 text-center">
                        <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center mx-auto mb-3">
                            <span className="text-2xl">🌍</span>
                        </div>
                        <h4 className="font-semibold text-white mb-1">Macro Insights</h4>
                        <p className="text-sm text-secondary">Market conditions & trends</p>
                    </div>
                    <div className="glass-card p-5 text-center">
                        <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mx-auto mb-3">
                            <span className="text-2xl">🧠</span>
                        </div>
                        <h4 className="font-semibold text-white mb-1">Philosophy</h4>
                        <p className="text-sm text-secondary">Long-term investment thesis</p>
                    </div>
                    <div className="glass-card p-5 text-center">
                        <div className="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center mx-auto mb-3">
                            <span className="text-2xl">⚠️</span>
                        </div>
                        <h4 className="font-semibold text-white mb-1">Risk Analysis</h4>
                        <p className="text-sm text-secondary">Downside scenarios & regret</p>
                    </div>
                </div>
            </div>
        );
    }

    // Start analysis on mount
    useEffect(() => {
        if (symbol) {
            runAnalysis();
        }
    }, [symbol]);

    const runAnalysis = async () => {
        setLoading(true);
        setError(null);
        setSaved(false);

        try {
            // Use API functions
            await ingestAsset(symbol);
            const data = await retrieveContext(symbol, 'comprehensive analysis');

            if (!data) throw new Error('No data received');
            setAnalysisData(data);
        } catch (err) {
            console.error(err);
            setError(err.message || 'Analysis failed');
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!analysisData || saved) return;
        setSaving(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/history`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query_type: 'analysis',
                    query: symbol,
                    result: analysisData
                })
            });

            if (response.ok) {
                setSaved(true);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="space-y-6">
                <div className="glass-card rounded-xl border border-glass-border p-8">
                    <div className="flex flex-col items-center justify-center py-12">
                        <div className="relative mb-6">
                            <div className="absolute inset-0 bg-primary-500/20 blur-xl rounded-full animate-pulse"></div>
                            <Loader2 className="w-16 h-16 text-primary-400 animate-spin relative z-10" />
                        </div>
                        <h3 className="text-2xl font-bold text-white mb-2">Analyzing {symbol}</h3>
                        <p className="text-secondary text-sm mb-8">Our multi-agent system is analyzing your request...</p>
                    </div>

                    {/* Agent Progress Cards - Dark Theme */}
                    <div className="grid grid-cols-2 gap-4 max-w-3xl mx-auto">
                        <div className="p-4 border border-amber-500/30 rounded-xl bg-amber-500/10 backdrop-blur-sm">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-amber-500 rounded-full animate-pulse shadow-glow"></div>
                                <span className="font-semibold text-white">Quant Agent</span>
                            </div>
                            <p className="text-sm text-gray-400">Analyzing financials & valuation metrics...</p>
                        </div>

                        <div className="p-4 border border-blue-500/30 rounded-xl bg-blue-500/10 backdrop-blur-sm">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-white">Macro Agent</span>
                            </div>
                            <p className="text-sm text-gray-400">Evaluating market conditions & economic indicators...</p>
                        </div>

                        <div className="p-4 border border-purple-500/30 rounded-xl bg-purple-500/10 backdrop-blur-sm">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-white">Philosopher Agent</span>
                            </div>
                            <p className="text-sm text-gray-400">Assessing long-term investment thesis...</p>
                        </div>

                        <div className="p-4 border border-red-500/30 rounded-xl bg-red-500/10 backdrop-blur-sm">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-white">Regret Agent</span>
                            </div>
                            <p className="text-sm text-gray-400">Identifying potential downside scenarios...</p>
                        </div>
                    </div>

                    <p className="text-center text-secondary text-sm mt-6">
                        This typically takes 15-30 seconds...
                    </p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="glass-card rounded-xl border border-error/30 p-8 text-center bg-error/5">
                <div className="w-16 h-16 rounded-full bg-error/20 flex items-center justify-center mx-auto mb-4">
                    <span className="text-3xl">⚠️</span>
                </div>
                <h3 className="text-lg font-semibold text-error mb-2">Analysis Failed</h3>
                <p className="text-secondary mb-6">{error}</p>
                <button
                    onClick={runAnalysis}
                    className="px-6 py-3 bg-gradient-to-r from-primary-600 to-accent-dark text-white rounded-xl font-medium hover:shadow-glow transition-all"
                >
                    Try Again
                </button>
            </div>
        );
    }

    if (!analysisData) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="w-12 h-12 text-primary-400 animate-spin mb-4" />
                <h3 className="text-lg font-semibold text-white">Initializing...</h3>
            </div>
        );
    }

    // Safe access to data
    const matchResult = analysisData.match_result || {};
    const results = analysisData.results || {};

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-white">{symbol} Analysis</h1>
                    <p className="text-secondary">AI-powered investment analysis</p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={runAnalysis}
                        className="flex items-center gap-2 px-4 py-2 bg-surface-light text-gray-300 rounded-xl border border-glass-border hover:bg-surface-light/80 hover:text-white transition-all"
                    >
                        <Sparkles className="w-4 h-4" />
                        Refresh
                    </button>
                    <button
                        onClick={handleSave}
                        disabled={saving || saved}
                        className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all border ${saved
                            ? 'bg-success/20 text-success border-success/30'
                            : 'bg-surface-light text-gray-300 border-glass-border hover:bg-surface-light/80 hover:text-white'
                            }`}
                    >
                        {saving ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : saved ? (
                            <CheckCircle className="w-4 h-4" />
                        ) : (
                            <Save className="w-4 h-4" />
                        )}
                        {saved ? 'Saved' : 'Save to History'}
                    </button>
                </div>
            </div>

            {/* Match Score Card */}
            <MatchScoreCard matchResult={matchResult} assetId={symbol} />

            {/* Regret Warning Box */}
            <RegretWarningBox regretData={results.regret} />

            {/* Coach Detailed Reasoning */}
            {analysisData.verdict?.analysis && (
                <div className="glass-card rounded-xl border border-glass-border p-6">
                    <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-amber-400" />
                        Coach's Detailed Investment Thesis
                    </h3>
                    <div className="prose prose-sm max-w-none text-gray-300 whitespace-pre-line leading-relaxed">
                        {analysisData.verdict.analysis}
                    </div>
                </div>
            )}

            {/* Agent Deep Dive (Replaces old grid) */}
            <div className="mt-8">
                <AgentDeepDive results={results} />
            </div>

            {/* Chatbot */}
            <div className="mt-6">
                <Chatbot analysisData={analysisData} assetId={symbol} />
            </div>
        </div>
    );
}

export default AnalysisPage;
