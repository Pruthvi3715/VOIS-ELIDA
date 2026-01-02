import { CheckCircle, XCircle, AlertTriangle, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import RadialMatchScore from './RadialMatchScore';
import StatusBadge from './StatusBadge';

/**
 * Match Score Card Component with 3D Effects
 * Displays the match score prominently with radial gauge and visual enhancements
 */
function MatchScoreCard({ matchResult, assetId }) {
    if (!matchResult) return null;

    const {
        score,
        recommendation,
        action_if_owned,
        action_if_not_owned,
        fit_reasons = [],
        concern_reasons = [],
        summary,
        breakdown = {}
    } = matchResult;

    // Determine risk level based on score
    const getRiskLevel = (score) => {
        if (score >= 70) return 'low';
        if (score >= 50) return 'medium';
        return 'high';
    };

    const getConfidenceLevel = (score) => {
        if (score >= 70) return 'high';
        if (score >= 50) return 'medium';
        return 'low';
    };

    return (
        <div className="relative group">
            {/* 3D Shadow layers */}
            <div className="absolute inset-0 bg-gradient-to-br from-gray-200 to-gray-300 rounded-3xl blur-2xl opacity-30 group-hover:opacity-50 transition-opacity"></div>
            <div className="absolute inset-2 bg-gradient-to-br from-white to-gray-100 rounded-3xl blur-xl opacity-40"></div>

            {/* Main Card */}
            <div className="relative bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-100 transform transition-all duration-300 hover:scale-[1.01]"
                style={{ boxShadow: '0 20px 60px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.05)' }}>

                {/* Header Section with 3D gradient */}
                <div className="relative bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8 overflow-hidden">
                    {/* Animated background pattern */}
                    <div className="absolute inset-0 opacity-10">
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent animate-pulse"></div>
                    </div>

                    <div className="relative flex items-center justify-between">
                        <div className="flex-1">
                            <p className="text-white/60 text-sm uppercase tracking-wider font-medium mb-2">
                                Personalized Match Score
                            </p>
                            <h2 className="text-3xl font-bold text-white mb-3 drop-shadow-lg">
                                {assetId} Analysis
                            </h2>
                            <div className="flex items-center gap-3 mb-4">
                                <StatusBadge type="confidence" value={getConfidenceLevel(score)} size="md" />
                                <StatusBadge type="risk" value={getRiskLevel(score)} size="md" />
                                <StatusBadge type="action" value={recommendation?.toLowerCase() || 'hold'} size="md" />
                            </div>
                            <p className="text-white/80 max-w-md text-sm leading-relaxed">
                                {summary}
                            </p>
                        </div>

                        {/* Radial Match Score Gauge */}
                        <div className="ml-6">
                            <RadialMatchScore score={score} size={220} />
                        </div>
                    </div>
                </div>

                {/* Action Cards with 3D effect */}
                <div className="grid grid-cols-2 gap-4 p-6 bg-gradient-to-br from-gray-50 to-white">
                    <div className="relative group/card">
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-100 to-cyan-100 rounded-xl blur-lg opacity-0 group-hover/card:opacity-50 transition-opacity"></div>
                        <div className="relative bg-white p-5 rounded-xl border-2 border-gray-200 shadow-lg hover:shadow-xl transition-all hover:border-blue-300"
                            style={{ boxShadow: '0 4px 14px rgba(0,0,0,0.08)' }}>
                            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2 font-semibold">If You Own It</p>
                            <div className="flex items-center gap-2">
                                {getRecommendationIcon(action_if_owned)}
                                <span className="font-bold text-gray-900 text-lg">{action_if_owned}</span>
                            </div>
                        </div>
                    </div>

                    <div className="relative group/card">
                        <div className="absolute inset-0 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl blur-lg opacity-0 group-hover/card:opacity-50 transition-opacity"></div>
                        <div className="relative bg-white p-5 rounded-xl border-2 border-gray-200 shadow-lg hover:shadow-xl transition-all hover:border-purple-300"
                            style={{ boxShadow: '0 4px 14px rgba(0,0,0,0.08)' }}>
                            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2 font-semibold">If You Don't Own</p>
                            <div className="flex items-center gap-2">
                                {getRecommendationIcon(action_if_not_owned)}
                                <span className="font-bold text-gray-900 text-lg">{action_if_not_owned}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Score Breakdown with 3D bars */}
                <div className="p-6 bg-white">
                    <h3 className="font-bold text-gray-900 mb-5 text-lg flex items-center gap-2">
                        <span className="w-1 h-6 bg-gradient-to-b from-blue-500 to-purple-500 rounded-full shadow-md"></span>
                        Score Breakdown
                    </h3>
                    <div className="space-y-4">
                        <ScoreBar3D label="Fundamentals" value={breakdown.fundamental} weight="30%" color="blue" />
                        <ScoreBar3D label="Risk Profile" value={breakdown.risk} weight="20%" color="orange" />
                        <ScoreBar3D label="Macro Environment" value={breakdown.macro} weight="20%" color="green" />
                        <ScoreBar3D label="DNA Match" value={breakdown.dna_match} weight="15%" color="purple" />
                        <ScoreBar3D label="Philosophy" value={breakdown.philosophy} weight="15%" color="pink" />
                    </div>
                </div>

                {/* Key Reasons with Checkmarks */}
                <div className="grid grid-cols-2 gap-4 p-6 pt-0">
                    {/* Fit Reasons */}
                    <div className="relative group/fit">
                        <div className="absolute inset-0 bg-gradient-to-br from-green-100 to-emerald-100 rounded-2xl blur-xl opacity-50"></div>
                        <div className="relative bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-5 border-2 border-green-200 shadow-lg">
                            <h4 className="font-bold text-green-900 flex items-center gap-2 mb-4 text-sm">
                                <CheckCircle className="w-5 h-5 text-green-600" />
                                Key Reasons to Invest
                            </h4>
                            <ul className="space-y-2.5">
                                {fit_reasons.slice(0, 4).map((reason, idx) => (
                                    <li key={idx} className="text-sm text-green-800 flex items-start gap-2.5">
                                        <span className="text-green-600 font-bold text-lg leading-none">✓</span>
                                        <span className="flex-1">{reason}</span>
                                    </li>
                                ))}
                                {fit_reasons.length === 0 && (
                                    <li className="text-sm text-green-700 italic">No strong fit reasons identified</li>
                                )}
                            </ul>
                        </div>
                    </div>

                    {/* Concerns */}
                    <div className="relative group/concern">
                        <div className="absolute inset-0 bg-gradient-to-br from-red-100 to-rose-100 rounded-2xl blur-xl opacity-50"></div>
                        <div className="relative bg-gradient-to-br from-red-50 to-rose-50 rounded-2xl p-5 border-2 border-red-200 shadow-lg">
                            <h4 className="font-bold text-red-900 flex items-center gap-2 mb-4 text-sm">
                                <AlertTriangle className="w-5 h-5 text-red-600" />
                                Key Concerns
                            </h4>
                            <ul className="space-y-2.5">
                                {concern_reasons.slice(0, 4).map((reason, idx) => (
                                    <li key={idx} className="text-sm text-red-800 flex items-start gap-2.5">
                                        <span className="text-red-600 font-bold text-lg leading-none">⚠</span>
                                        <span className="flex-1">{reason}</span>
                                    </li>
                                ))}
                                {concern_reasons.length === 0 && (
                                    <li className="text-sm text-red-700 italic">No major concerns identified</li>
                                )}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

/**
 * 3D Score Bar Component with gradient effects
 */
function ScoreBar3D({ label, value, weight, color = 'blue' }) {
    const numValue = typeof value === 'number' ? value : 0;
    const barWidth = Math.min(100, Math.max(0, numValue));

    const colorGradients = {
        blue: 'from-blue-400 to-blue-600',
        green: 'from-green-400 to-green-600',
        orange: 'from-orange-400 to-orange-600',
        purple: 'from-purple-400 to-purple-600',
        pink: 'from-pink-400 to-pink-600'
    };

    return (
        <div className="flex items-center gap-3">
            <div className="w-32 text-sm font-medium text-gray-700">{label}</div>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden shadow-inner relative">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                <div
                    className={`h-full bg-gradient-to-r ${colorGradients[color]} transition-all duration-1000 ease-out relative`}
                    style={{
                        width: `${barWidth}%`,
                        boxShadow: '0 2px 8px rgba(0,0,0,0.2), inset 0 1px 2px rgba(255,255,255,0.3)'
                    }}
                >
                    <div className="absolute inset-0 bg-gradient-to-b from-white/30 to-transparent"></div>
                </div>
            </div>
            <div className="w-12 text-right text-sm font-bold text-gray-800">
                {numValue ? Math.round(numValue) : '—'}
            </div>
            <div className="w-12 text-right text-xs text-gray-500 font-medium">{weight}</div>
        </div>
    );
}

// Helper to get recommendation icon
function getRecommendationIcon(rec) {
    const lower = (rec || '').toLowerCase();
    if (lower === 'buy') return <TrendingUp className="w-5 h-5 text-green-500" />;
    if (lower === 'avoid') return <XCircle className="w-5 h-5 text-red-500" />;
    if (lower === 'hold') return <Minus className="w-5 h-5 text-yellow-500" />;
    return <AlertTriangle className="w-5 h-5 text-orange-500" />;
}

export default MatchScoreCard;
