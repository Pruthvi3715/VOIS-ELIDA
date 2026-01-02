import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Sparkles, Loader2 } from 'lucide-react';
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

    // If no symbol provided, show search interface
    if (!symbol) {
        return (
            <div className="space-y-6">
                <div className="bg-white rounded-xl border border-gray-200 p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-2">Investment Analysis</h2>
                    <p className="text-gray-500 text-sm mb-6">
                        Our multi-agent AI system will analyze your request from multiple perspectives
                    </p>

                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={searchTicker}
                            onChange={(e) => setSearchTicker(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && searchTicker.trim() && navigate(`/analysis/${searchTicker.trim().toUpperCase()}`)}
                            placeholder="Enter stock symbol or company name"
                            className="flex-1 px-4 py-3 border border-gray-200 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-200 focus:border-gray-300"
                        />
                        <button
                            onClick={() => searchTicker.trim() && navigate(`/analysis/${searchTicker.trim().toUpperCase()}`)}
                            disabled={!searchTicker.trim()}
                            className="flex items-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Analyze
                        </button>
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

    if (loading) {
        return (
            <div className="space-y-6">
                <div className="bg-white rounded-xl border border-gray-200 p-8">
                    <div className="flex flex-col items-center justify-center py-12">
                        <Loader2 className="w-16 h-16 text-gray-400 animate-spin mb-6" />
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">Analyzing {symbol}</h3>
                        <p className="text-gray-500 text-sm mb-8">Our multi-agent system is analyzing your request...</p>
                    </div>

                    {/* Agent Progress Cards */}
                    <div className="grid grid-cols-2 gap-4 max-w-3xl mx-auto">
                        <div className="p-4 border border-amber-200 rounded-lg bg-amber-50">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-amber-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-gray-900">Quant Agent</span>
                            </div>
                            <p className="text-sm text-gray-600">Analyzing financials & valuation metrics...</p>
                        </div>

                        <div className="p-4 border border-blue-200 rounded-lg bg-blue-50">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-gray-900">Macro Agent</span>
                            </div>
                            <p className="text-sm text-gray-600">Evaluating market conditions & economic indicators...</p>
                        </div>

                        <div className="p-4 border border-purple-200 rounded-lg bg-purple-50">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-gray-900">Philosopher Agent</span>
                            </div>
                            <p className="text-sm text-gray-600">Assessing long-term investment thesis...</p>
                        </div>

                        <div className="p-4 border border-red-200 rounded-lg bg-red-50">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                                <span className="font-semibold text-gray-900">Regret Agent</span>
                            </div>
                            <p className="text-sm text-gray-600">Identifying potential downside scenarios...</p>
                        </div>
                    </div>

                    <p className="text-center text-gray-400 text-sm mt-6">
                        This typically takes 15-30 seconds...
                    </p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-white rounded-xl border border-gray-200 p-8 text-center">
                <h3 className="text-lg font-semibold text-red-600 mb-2">Analysis Failed</h3>
                <p className="text-gray-500 mb-4">{error}</p>
                <button
                    onClick={runAnalysis}
                    className="px-6 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition"
                >
                    Try Again
                </button>
            </div>
        );
    }

    if (!analysisData) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="w-12 h-12 text-gray-400 animate-spin mb-4" />
                <h3 className="text-lg font-semibold text-gray-900">Initializing...</h3>
            </div>
        );
    }

    // Safe access to data
    const matchResult = analysisData.match_result || {};
    const results = analysisData.results || {};

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">{symbol} Analysis</h1>
                    <p className="text-gray-500">AI-powered investment analysis</p>
                </div>
                <button
                    onClick={runAnalysis}
                    className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
                >
                    <Sparkles className="w-4 h-4" />
                    Refresh Analysis
                </button>
            </div>

            {/* Match Score Card */}
            <MatchScoreCard matchResult={matchResult} assetId={symbol} />

            {/* Regret Warning Box */}
            <RegretWarningBox regretData={results.regret} />

            {/* Coach Detailed Reasoning */}
            {analysisData.verdict?.analysis && (
                <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                    <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-yellow-500" />
                        Coach's Detailed Investment Thesis
                    </h3>
                    <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-line">
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
