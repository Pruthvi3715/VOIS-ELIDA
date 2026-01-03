import React from 'react';
import { motion } from 'framer-motion';
import {
    Brain, Globe, Heart, AlertTriangle, TrendingUp, CheckCircle2, XCircle
} from 'lucide-react';

interface AgentCardProps {
    name: string;
    score: number;
    confidence: number;
    analysis: string;
    strengths?: string[];
    weaknesses?: string[];
    metricsUsed?: string[];
    metricsValues?: Record<string, number | string>;
    dataQuality?: string;
    fallbackUsed?: boolean;
}

const agentIcons: Record<string, React.ElementType> = {
    'Quant Agent': TrendingUp,
    'Macro Agent': Globe,
    'Philosopher Agent': Heart,
    'Regret Simulation Agent': AlertTriangle,
    'Coach Synthesizer': Brain,
};

const agentColors: Record<string, string> = {
    'Quant Agent': 'from-blue-500 to-cyan-500',
    'Macro Agent': 'from-purple-500 to-pink-500',
    'Philosopher Agent': 'from-emerald-500 to-teal-500',
    'Regret Simulation Agent': 'from-orange-500 to-red-500',
    'Coach Synthesizer': 'from-indigo-500 to-violet-500',
};

const ScoreGauge: React.FC<{ score: number; id: string }> = ({ score, id }) => {
    const circumference = 2 * Math.PI * 40;
    const strokeDashoffset = circumference - (score / 100) * circumference;
    const uniqueId = `gauge-${id.replace(/\s+/g, '-')}`;

    return (
        <div className="relative w-20 h-20 flex-shrink-0">
            <svg className="w-full h-full -rotate-90">
                {/* Background circle */}
                <circle
                    cx="40"
                    cy="40"
                    r="34"
                    stroke="rgba(255,255,255,0.1)"
                    strokeWidth="6"
                    fill="none"
                />
                {/* Progress circle */}
                <motion.circle
                    cx="40"
                    cy="40"
                    r="34"
                    stroke={`url(#${uniqueId})`}
                    strokeWidth="6"
                    fill="none"
                    strokeLinecap="round"
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                    style={{ strokeDasharray: circumference }}
                />
                <defs>
                    <linearGradient id={uniqueId} x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#6366f1" />
                        <stop offset="100%" stopColor="#8b5cf6" />
                    </linearGradient>
                </defs>
            </svg>
            {/* Score text */}
            <div className="absolute inset-0 flex items-center justify-center">
                <motion.span
                    className="text-xl font-bold text-white"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                >
                    {score}
                </motion.span>
            </div>
        </div>
    );
};

const AgentCard: React.FC<AgentCardProps> = ({
    name,
    score,
    confidence,
    analysis,
    strengths = [],
    weaknesses = [],
    metricsUsed = []
}) => {
    const Icon = agentIcons[name] || Brain;
    const colorClass = agentColors[name] || 'from-indigo-500 to-violet-500';

    // Text Cleaning Logic
    const cleanAnalysis = (text: string) => {
        if (!text) return [];
        // Remove JSON artifacts like ```json { ... } ```
        let cleaned = text.replace(/```json[\s\S]*?```/g, '')
            .replace(/```[\s\S]*?```/g, '')
            .replace(/\{"score":[\s\S]*?\}/g, ''); // aggressive json removal

        // Remove "Paragraph X -" headers
        cleaned = cleaned.replace(/Paragraph \d+ -/g, '');

        // Split by newlines and filter empty
        return cleaned.split('\n\n')
            .map(p => p.trim())
            .filter(p => p.length > 20); // Filter out short artifacts
    };

    const analysisParagraphs = cleanAnalysis(analysis);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card overflow-hidden h-full flex flex-col"
        >
            {/* Header */}
            <div className="p-5 border-b border-glass-border bg-surface-light/30">
                <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-3">
                        <div className={`p-2.5 rounded-xl bg-gradient-to-br ${colorClass} bg-opacity-20 shadow-glow`}>
                            <Icon className="w-5 h-5 text-white" />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-white leading-tight">{name}</h3>
                            <div className="flex items-center gap-2 mt-1">
                                <div className="h-1.5 w-1.5 rounded-full bg-success shadow-[0_0_8px_rgba(34,197,94,0.6)]" />
                                <span className="text-xs text-secondary font-medium">
                                    {confidence}% confident
                                </span>
                            </div>
                        </div>
                    </div>
                    <ScoreGauge score={score} id={name} />
                </div>
            </div>

            {/* Content Body */}
            <div className="p-5 space-y-5 flex-grow">
                {/* Analysis Text */}
                <div className="space-y-4">
                    {analysisParagraphs.length > 0 ? (
                        analysisParagraphs.map((para, i) => (
                            <p key={i} className="text-gray-100 text-[15px] leading-7 font-normal bg-white/5 p-3 rounded-lg border border-white/5">
                                {para}
                            </p>
                        ))
                    ) : (
                        <p className="text-secondary italic">Analysis pending...</p>
                    )}
                </div>

                {/* Bullets Grid */}
                {(strengths.length > 0 || weaknesses.length > 0) && (
                    <div className="grid grid-cols-1 gap-3 pt-2">
                        {strengths.slice(0, 2).map((s, i) => (
                            <div key={`s-${i}`} className="flex items-start gap-2 text-xs bg-success/5 p-2 rounded-lg border border-success/10">
                                <CheckCircle2 className="w-3.5 h-3.5 text-success flex-shrink-0 mt-0.5" />
                                <span className="text-gray-300">{s}</span>
                            </div>
                        ))}
                        {weaknesses.slice(0, 2).map((w, i) => (
                            <div key={`w-${i}`} className="flex items-start gap-2 text-xs bg-error/5 p-2 rounded-lg border border-error/10">
                                <XCircle className="w-3.5 h-3.5 text-error flex-shrink-0 mt-0.5" />
                                <span className="text-gray-300">{w}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Footer with Metrics */}
            {metricsUsed.length > 0 && (
                <div className="px-5 py-3 bg-surface-dark/30 border-t border-glass-border flex flex-wrap gap-2">
                    {metricsUsed.slice(0, 4).map((metric, i) => (
                        <span key={i} className="text-[10px] uppercase tracking-wider px-2 py-1 rounded bg-surface-light/50 text-secondary">
                            {metric}
                        </span>
                    ))}
                </div>
            )}
        </motion.div>
    );
};

export default AgentCard;
