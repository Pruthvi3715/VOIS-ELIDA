import { useState } from 'react';
import {
    Calculator, Globe, Scale, AlertTriangle,
    ArrowUpRight, ArrowDownRight, Minus,
    CheckCircle, XCircle, Info
} from 'lucide-react';

/**
 * Agent Deep Dive Component
 * Displays detailed, structured analysis from each agent.
 */
function AgentDeepDive({ results }) {
    const [activeTab, setActiveTab] = useState('quant');

    if (!results) return null;

    const tabs = [
        { id: 'quant', label: 'Quantitative', icon: Calculator, color: 'blue' },
        { id: 'macro', label: 'Macro', icon: Globe, color: 'indigo' },
        { id: 'philosopher', label: 'Philosophy', icon: Scale, color: 'purple' },
        { id: 'regret', label: 'Risk & Regret', icon: AlertTriangle, color: 'amber' },
    ];

    return (
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
            {/* Tabs Header */}
            <div className="flex border-b border-gray-200 overflow-x-auto">
                {tabs.map((tab) => {
                    const Icon = tab.icon;
                    const isActive = activeTab === tab.id;
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors whitespace-nowrap
                                ${isActive
                                    ? `text-${tab.color}-600 border-b-2 border-${tab.color}-600 bg-${tab.color}-50`
                                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                                }`}
                        >
                            <Icon className={`w-4 h-4 ${isActive ? `text-${tab.color}-600` : 'text-gray-400'}`} />
                            {tab.label}
                        </button>
                    );
                })}
            </div>

            {/* Content Area */}
            <div className="p-6">
                {activeTab === 'quant' && <QuantDeepDive data={results.quant} />}
                {activeTab === 'macro' && <MacroDeepDive data={results.macro} />}
                {activeTab === 'philosopher' && <PhilosopherDeepDive data={results.philosopher} />}
                {activeTab === 'regret' && <RegretDeepDive data={results.regret} />}
            </div>
        </div>
    );
}

/**
 * Quant Tab Content
 */
function QuantDeepDive({ data }) {
    const output = data?.output || {};
    const analysis = data?.analysis || '';

    return (
        <div className="space-y-6">
            <div className="flex items-start justify-between">
                <div>
                    <h3 className="text-lg font-bold text-gray-900">Quantitative Assessment</h3>
                    <p className="text-sm text-gray-500">Based on financial statements and valuation metrics</p>
                </div>
                <div className="text-right">
                    <div className="text-3xl font-bold text-blue-600">{output.score || '—'}</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide">Score</div>
                </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
                    <h4 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                        <Calculator className="w-4 h-4 text-blue-500" />
                        Key Metrics
                    </h4>
                    <div className="space-y-3">
                        {Object.entries(output.metrics_values || {}).map(([key, value]) => (
                            <div key={key} className="flex justify-between items-center text-sm border-b border-gray-200 pb-2 last:border-0">
                                <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}</span>
                                <span className="font-mono font-medium text-gray-900">
                                    {typeof value === 'number' ? value.toFixed(2) : value}
                                </span>
                            </div>
                        ))}
                        {!output.metrics_values && <p className="text-gray-500 text-sm">No specific metrics extracted.</p>}
                    </div>
                </div>

                <div className="space-y-4">
                    {/* Strengths */}
                    <div className="bg-green-50 rounded-xl p-4 border border-green-100">
                        <h4 className="font-semibold text-green-800 mb-2 flex items-center gap-2">
                            <ArrowUpRight className="w-4 h-4" /> Strengths
                        </h4>
                        <ul className="space-y-2">
                            {output.strengths?.map((s, i) => (
                                <li key={i} className="text-sm text-green-700 flex items-start gap-2">
                                    <CheckCircle className="w-3 h-3 mt-1 flex-shrink-0 opacity-50" />
                                    {s}
                                </li>
                            ))}
                            {!output.strengths?.length && <li className="text-sm text-gray-500">None identified.</li>}
                        </ul>
                    </div>

                    {/* Weaknesses */}
                    <div className="bg-red-50 rounded-xl p-4 border border-red-100">
                        <h4 className="font-semibold text-red-800 mb-2 flex items-center gap-2">
                            <ArrowDownRight className="w-4 h-4" /> Weaknesses
                        </h4>
                        <ul className="space-y-2">
                            {output.weaknesses?.map((w, i) => (
                                <li key={i} className="text-sm text-red-700 flex items-start gap-2">
                                    <XCircle className="w-3 h-3 mt-1 flex-shrink-0 opacity-50" />
                                    {w}
                                </li>
                            ))}
                            {!output.weaknesses?.length && <li className="text-sm text-gray-500">None identified.</li>}
                        </ul>
                    </div>
                </div>
            </div>

            {/* Analysis Text */}
            <div className="bg-blue-50/50 rounded-xl p-5 border border-blue-100">
                <h4 className="font-semibold text-gray-900 mb-2">Detailed Analysis</h4>
                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{analysis}</p>
            </div>
        </div>
    );
}

/**
 * Macro Tab Content
 */
function MacroDeepDive({ data }) {
    const output = data?.output || {};
    const analysis = data?.analysis || '';

    return (
        <div className="space-y-6">
            <div className="flex items-start justify-between">
                <div>
                    <h3 className="text-lg font-bold text-gray-900">Macroeconomic Environment</h3>
                    <p className="text-sm text-gray-500">Market regime and external factors</p>
                </div>
                <div className="text-right">
                    <div className={`text-xl font-bold px-3 py-1 rounded-lg inline-block
                        ${output.trend === 'Bullish' ? 'bg-green-100 text-green-700' :
                            output.trend === 'Bearish' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}`}>
                        {output.trend || 'Neutral'}
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide mt-1">Market Trend</div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Indicators Table */}
                <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-gray-50 text-gray-500 font-medium">
                            <tr>
                                <th className="px-4 py-3">Indicator</th>
                                <th className="px-4 py-3">Value</th>
                                <th className="px-4 py-3">Signal</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {output.indicators_analyzed?.map((ind, i) => (
                                <tr key={i}>
                                    <td className="px-4 py-3 font-medium text-gray-900">{ind.name}</td>
                                    <td className="px-4 py-3 text-gray-600">{ind.value}</td>
                                    <td className="px-4 py-3">
                                        <span className={`px-2 py-1 rounded text-xs font-medium 
                                            ${ind.signal === 'positive' ? 'bg-green-100 text-green-700' :
                                                ind.signal === 'negative' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600'}`}>
                                            {ind.signal}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                            {!output.indicators_analyzed?.length && (
                                <tr><td colSpan="3" className="px-4 py-3 text-gray-500 text-center">No indicators found</td></tr>
                            )}
                        </tbody>
                    </table>
                </div>

                <div className="space-y-4">
                    <div className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                        <h4 className="font-semibold text-gray-800 mb-2">Risks & Tailwinds</h4>
                        <div className="space-y-3">
                            <div>
                                <h5 className="text-xs font-bold text-red-600 uppercase tracking-wide mb-1">Macro Risks</h5>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    {output.macro_risks?.map((r, i) => <li key={i}>• {r}</li>)}
                                    {!output.macro_risks?.length && <li>None identified.</li>}
                                </ul>
                            </div>
                            <div>
                                <h5 className="text-xs font-bold text-green-600 uppercase tracking-wide mb-1">Tailwinds</h5>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    {output.macro_tailwinds?.map((t, i) => <li key={i}>• {t}</li>)}
                                    {!output.macro_tailwinds?.length && <li>None identified.</li>}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-indigo-50/50 rounded-xl p-5 border border-indigo-100">
                <h4 className="font-semibold text-gray-900 mb-2">Strategic Commentary</h4>
                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{analysis}</p>
            </div>
        </div>
    );
}

/**
 * Philosopher Tab Content
 */
function PhilosopherDeepDive({ data }) {
    const output = data?.output || {};
    const analysis = data?.analysis || '';

    return (
        <div className="space-y-6">
            <div className="flex items-start justify-between">
                <div>
                    <h3 className="text-lg font-bold text-gray-900">Philosophical Alignment</h3>
                    <p className="text-sm text-gray-500">Ethics, sustainability, and long-term moat</p>
                </div>
                <div className="text-right">
                    <div className={`text-xl font-bold px-3 py-1 rounded-lg inline-block
                        ${output.alignment === 'High' ? 'bg-purple-100 text-purple-700' :
                            output.alignment === 'Low' ? 'bg-gray-200 text-gray-700' : 'bg-purple-50 text-purple-600'}`}>
                        {output.alignment || 'Medium'}
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide mt-1">Alignment</div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                    {output.factors_analyzed?.map((factor, i) => (
                        <div key={i} className="bg-white border border-gray-100 p-4 rounded-xl shadow-sm">
                            <div className="flex justify-between items-center mb-2">
                                <span className="font-semibold text-gray-800">{factor.factor}</span>
                                <span className="text-xs font-medium bg-gray-100 px-2 py-1 rounded text-gray-600 capitalize">
                                    {factor.assessment}
                                </span>
                            </div>
                            <p className="text-sm text-gray-600">{factor.reasoning}</p>
                        </div>
                    ))}
                    {!output.factors_analyzed?.length && <p className="text-gray-500 italic">No specific factors analyzed.</p>}
                </div>

                <div className="bg-purple-50/50 rounded-xl p-5 border border-purple-100 h-fit">
                    <h4 className="font-semibold text-purple-900 mb-3 flex items-center gap-2">
                        <Scale className="w-4 h-4" /> Long-Term View
                    </h4>
                    <div className="space-y-4">
                        <div>
                            <h5 className="text-xs font-bold text-gray-500 uppercase mb-1">Outlook</h5>
                            <p className="text-sm text-gray-800 font-medium">{output.long_term_outlook}</p>
                        </div>
                        <div>
                            <h5 className="text-xs font-bold text-gray-500 uppercase mb-1">Ethical Strengths</h5>
                            <ul className="text-sm text-gray-600 list-disc list-inside">
                                {output.ethical_strengths?.map((s, i) => <li key={i}>{s}</li>)}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-gray-50 rounded-xl p-5 border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-2">Philosophical Treatise</h4>
                <p className="text-sm text-gray-700 leading-relaxed font-serif italic text-justify whitespace-pre-wrap">{analysis}</p>
            </div>
        </div>
    );
}

/**
 * Regret Tab Content
 */
function RegretDeepDive({ data }) {
    const output = data?.output || {};
    const analysis = data?.analysis || '';

    return (
        <div className="space-y-6">
            <div className="flex items-start justify-between">
                <div>
                    <h3 className="text-lg font-bold text-gray-900">Risk & Regret Simulation</h3>
                    <p className="text-sm text-gray-500">Downside analysis and "Pre-Mortem" scenarios</p>
                </div>
                <div className="text-right">
                    <div className={`text-xl font-bold px-3 py-1 rounded-lg inline-block
                        ${output.risk_level === 'High' ? 'bg-red-100 text-red-700' :
                            output.risk_level === 'Low' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                        {output.risk_level || 'Medium'}
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide mt-1">Risk Level</div>
                </div>
            </div>

            <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-center gap-4">
                <div className="bg-amber-100 p-2 rounded-lg">
                    <AlertTriangle className="w-6 h-6 text-amber-600" />
                </div>
                <div>
                    <h4 className="font-semibold text-amber-900">Max Drawdown Estimate</h4>
                    <p className="text-amber-700 text-sm">Potential downside in adverse scenarios: <span className="font-bold">{output.max_drawdown_estimate || 'Unknown'}</span></p>
                </div>
            </div>

            <h4 className="font-semibold text-gray-800 mt-2">Simulated Failure Scenarios</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {output.scenarios?.map((scenario, i) => (
                    <div key={i} className="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-md transition-shadow relative overflow-hidden group">
                        <div className={`absolute top-0 left-0 w-1 h-full 
                            ${scenario.probability === 'High' ? 'bg-red-500' : 'bg-gray-300'}`}></div>
                        <h5 className="font-semibold text-gray-900 mb-1">{scenario.name}</h5>
                        <div className="flex gap-2 mb-2">
                            <span className="text-xs bg-gray-100 px-2 py-0.5 rounded text-gray-500">Prob: {scenario.probability}</span>
                            <span className="text-xs bg-red-50 px-2 py-0.5 rounded text-red-600">Drop: {scenario.estimated_drawdown}</span>
                        </div>
                        <p className="text-xs text-gray-600">{scenario.impact}</p>
                    </div>
                ))}
            </div>

            <div className="bg-white rounded-xl border border-gray-200 p-5 mt-4">
                <h4 className="font-semibold text-gray-900 mb-2">Values at Risk (Pre-Mortem Analysis)</h4>
                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{analysis}</p>
            </div>
        </div>
    );
}

export default AgentDeepDive;
