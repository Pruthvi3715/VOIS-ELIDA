import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import { ArrowLeft, Play } from 'lucide-react';

const AssetDetail: React.FC = () => {
    const { symbol } = useParams<{ symbol: string }>();
    const { token } = useAuth();
    const navigate = useNavigate();
    const [analysis, setAnalysis] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchLatestAnalysis();
    }, [symbol]);

    const fetchLatestAnalysis = async () => {
        try {
            // Fixed: Use correct API path /api/v1/history
            const response = await axios.get('http://localhost:8000/api/v1/history', {
                headers: { Authorization: `Bearer ${token}` }
            });
            // Filter for this asset and take the most recent
            const history = response.data.entries || [];
            const match = history.find((h: any) => h.asset_id === symbol?.toUpperCase());

            if (match) {
                setAnalysis(match.result);
            }
        } catch (err) {
            console.error(err);
            setError('Failed to load analysis history');
        } finally {
            setLoading(false);
        }
    };

    const runNewAnalysis = async () => {
        setLoading(true);
        try {
            // Fixed: Use GET /analyze/{symbol} instead of POST /api/analyze
            const response = await axios.get(`http://localhost:8000/analyze/${symbol}`, {
                headers: { Authorization: `Bearer ${token}` },
                timeout: 120000 // 120 seconds timeout
            });
            setAnalysis(response.data);
        } catch (err) {
            console.error('Analysis failed:', err);
            setError('Analysis failed');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-8 text-center text-white">Loading analysis...</div>;

    return (
        <div className="space-y-6">
            <button onClick={() => navigate('/')} className="flex items-center gap-2 text-secondary hover:text-primary transition-colors">
                <ArrowLeft size={20} /> Back to Dashboard
            </button>

            <div className="flex justify-between items-center">
                <h1 className="text-4xl font-bold text-white">{symbol} Analysis</h1>
                {!analysis && (
                    <button onClick={runNewAnalysis} className="bg-primary px-4 py-2 rounded-lg text-white font-bold flex gap-2">
                        <Play size={20} /> Run Analysis
                    </button>
                )}
            </div>

            {error && <div className="text-error">{error}</div>}

            {/* Main Content */}
            {analysis ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Coach Verdict */}
                    <div className="col-span-full bg-surface/50 border border-primary/20 p-6 rounded-2xl">
                        <h2 className="text-2xl font-bold text-white mb-2">Coach's Verdict</h2>
                        <div className="grid md:grid-cols-2 gap-8">
                            <div>
                                <div className="text-4xl font-bold text-primary mb-2">{analysis.match_score} / 100</div>
                                <div className="text-xl font-bold text-white">{analysis.recommendation}</div>
                            </div>
                            <div>
                                <p className="text-secondary leading-relaxed">{analysis.summary}</p>
                            </div>
                        </div>
                    </div>

                    {/* Agent Cards */}
                    {analysis.agents && Object.entries(analysis.agents).map(([name, data]: [string, any]) => (
                        <div key={name} className="bg-surface/30 p-6 rounded-xl border border-white/5">
                            <div className="flex justify-between mb-4">
                                <h3 className="text-lg font-bold text-white capitalize">{name} Agent</h3>
                                <div className="text-primary font-bold">{data.score || '-'}</div>
                            </div>
                            {/* Simplified view of agent output */}
                            <div className="space-y-2 text-sm text-secondary">
                                <p>{data.analysis || 'No detailed analysis provided.'}</p>
                                {data.details && (
                                    <div className="mt-4 p-3 bg-black/20 rounded-lg">
                                        <pre className="whitespace-pre-wrap font-mono text-xs">{JSON.stringify(data.details, null, 2)}</pre>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-20 text-secondary border-2 border-dashed border-white/10 rounded-2xl">
                    No analysis data found for {symbol}. Run a new analysis to see insights.
                </div>
            )}
        </div>
    );
};

export default AssetDetail;
