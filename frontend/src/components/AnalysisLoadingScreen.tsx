import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, Loader2, Circle, Brain, TrendingUp, Globe, Heart, AlertTriangle, Award } from 'lucide-react';

interface AnalysisStep {
    id: string;
    label: string;
    icon: React.ElementType;
    status: 'pending' | 'active' | 'complete' | 'error';
}

interface AnalysisLoadingScreenProps {
    symbol: string;
    steps: AnalysisStep[];
    currentStep: number;
    error?: string;
}

const defaultSteps: AnalysisStep[] = [
    { id: 'fetch', label: 'Fetching market data', icon: TrendingUp, status: 'pending' },
    { id: 'quant', label: 'Running Quant Agent', icon: Brain, status: 'pending' },
    { id: 'macro', label: 'Running Macro Agent', icon: Globe, status: 'pending' },
    { id: 'philosopher', label: 'Running Philosopher Agent', icon: Heart, status: 'pending' },
    { id: 'regret', label: 'Running Regret Agent', icon: AlertTriangle, status: 'pending' },
    { id: 'coach', label: 'Coach synthesizing insights', icon: Award, status: 'pending' },
];

const AnalysisLoadingScreen: React.FC<AnalysisLoadingScreenProps> = ({
    symbol,
    steps = defaultSteps,
    currentStep,
    error
}) => {
    const getStepStatus = (index: number): 'pending' | 'active' | 'complete' => {
        if (index < currentStep) return 'complete';
        if (index === currentStep) return 'active';
        return 'pending';
    };

    return (
        <div className="min-h-[60vh] flex items-center justify-center">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass-card p-8 max-w-md w-full relative overflow-hidden"
            >
                {/* Background glow effect */}
                <div className="absolute inset-0 bg-gradient-glow opacity-50" />

                {/* Header */}
                <div className="relative z-10 text-center mb-8">
                    <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                        className="w-20 h-20 mx-auto mb-4 relative"
                    >
                        <div className="absolute inset-0 bg-gradient-primary rounded-full opacity-20 blur-xl" />
                        <div className="absolute inset-0 flex items-center justify-center">
                            <Brain className="w-10 h-10 text-primary-400" />
                        </div>
                        <svg className="absolute inset-0 w-full h-full -rotate-90">
                            <circle
                                cx="40"
                                cy="40"
                                r="36"
                                stroke="rgba(255,255,255,0.1)"
                                strokeWidth="4"
                                fill="none"
                            />
                            <motion.circle
                                cx="40"
                                cy="40"
                                r="36"
                                stroke="url(#gradient)"
                                strokeWidth="4"
                                fill="none"
                                strokeLinecap="round"
                                initial={{ pathLength: 0 }}
                                animate={{ pathLength: (currentStep + 1) / steps.length }}
                                transition={{ duration: 0.5 }}
                            />
                            <defs>
                                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stopColor="#6366f1" />
                                    <stop offset="100%" stopColor="#8b5cf6" />
                                </linearGradient>
                            </defs>
                        </svg>
                    </motion.div>

                    <h2 className="text-2xl font-bold text-white mb-2">
                        Analyzing <span className="text-gradient">{symbol}</span>
                    </h2>
                    <p className="text-secondary text-sm">
                        Our AI agents are processing your request
                    </p>
                </div>

                {/* Steps */}
                <div className="relative z-10 space-y-3">
                    {steps.map((step, index) => {
                        const status = getStepStatus(index);
                        const Icon = step.icon;

                        return (
                            <motion.div
                                key={step.id}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-300 ${status === 'active'
                                        ? 'bg-primary-500/10 border border-primary-500/30'
                                        : status === 'complete'
                                            ? 'bg-success/5'
                                            : 'bg-glass'
                                    }`}
                            >
                                {/* Status indicator */}
                                <div className="flex-shrink-0">
                                    <AnimatePresence mode="wait">
                                        {status === 'complete' ? (
                                            <motion.div
                                                key="complete"
                                                initial={{ scale: 0 }}
                                                animate={{ scale: 1 }}
                                                exit={{ scale: 0 }}
                                            >
                                                <CheckCircle2 className="w-5 h-5 text-success" />
                                            </motion.div>
                                        ) : status === 'active' ? (
                                            <motion.div
                                                key="active"
                                                initial={{ scale: 0 }}
                                                animate={{ scale: 1 }}
                                            >
                                                <Loader2 className="w-5 h-5 text-primary-400 animate-spin" />
                                            </motion.div>
                                        ) : (
                                            <Circle className="w-5 h-5 text-secondary/30" />
                                        )}
                                    </AnimatePresence>
                                </div>

                                {/* Icon */}
                                <Icon className={`w-5 h-5 ${status === 'complete' ? 'text-success' :
                                        status === 'active' ? 'text-primary-400' :
                                            'text-secondary/50'
                                    }`} />

                                {/* Label */}
                                <span className={`font-medium ${status === 'complete' ? 'text-white' :
                                        status === 'active' ? 'text-primary-300' :
                                            'text-secondary/50'
                                    }`}>
                                    {step.label}
                                </span>

                                {/* Active indicator */}
                                {status === 'active' && (
                                    <motion.div
                                        className="ml-auto text-xs text-primary-400"
                                        animate={{ opacity: [0.5, 1, 0.5] }}
                                        transition={{ duration: 1.5, repeat: Infinity }}
                                    >
                                        Processing...
                                    </motion.div>
                                )}
                            </motion.div>
                        );
                    })}
                </div>

                {/* Error message */}
                {error && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-4 p-3 bg-error/10 border border-error/30 rounded-xl text-error text-sm"
                    >
                        {error}
                    </motion.div>
                )}

                {/* Progress text */}
                <div className="mt-6 text-center">
                    <p className="text-secondary text-sm">
                        Step {Math.min(currentStep + 1, steps.length)} of {steps.length}
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export { AnalysisLoadingScreen, defaultSteps };
export type { AnalysisStep };
