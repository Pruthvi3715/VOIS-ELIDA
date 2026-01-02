function StatusBadge({ type, value, size = 'md' }) {
    const configs = {
        confidence: {
            high: { bg: 'from-green-400 to-emerald-500', text: 'High Confidence', icon: '✓' },
            medium: { bg: 'from-amber-400 to-orange-500', text: 'Medium Confidence', icon: '○' },
            low: { bg: 'from-red-400 to-rose-500', text: 'Low Confidence', icon: '!' }
        },
        risk: {
            high: { bg: 'from-red-400 to-rose-500', text: 'High Risk', icon: '⚠️' },
            medium: { bg: 'from-amber-400 to-orange-500', text: 'Medium Risk', icon: '△' },
            low: { bg: 'from-green-400 to-emerald-500', text: 'Low Risk', icon: '✓' }
        },
        action: {
            buy: { bg: 'from-green-400 to-emerald-500', text: 'Buy', icon: '↗' },
            hold: { bg: 'from-blue-400 to-cyan-500', text: 'Hold', icon: '=' },
            sell: { bg: 'from-red-400 to-rose-500', text: 'Sell', icon: '↘' }
        }
    };

    const getConfig = () => {
        const typeConfig = configs[type] || configs.confidence;
        const level = String(value).toLowerCase();
        return typeConfig[level] || typeConfig.medium || Object.values(typeConfig)[0];
    };

    const config = getConfig();
    const sizeClasses = {
        sm: 'px-2 py-1 text-xs',
        md: 'px-3 py-1.5 text-sm',
        lg: 'px-4 py-2 text-base'
    };

    return (
        <div className="relative inline-block group">
            {/* 3D shadow layers */}
            <div className={`absolute inset-0 bg-gradient-to-br ${config.bg} rounded-full blur-md opacity-40 group-hover:opacity-60 transition-opacity`}></div>

            {/* Main badge with 3D effect */}
            <div className={`relative bg-gradient-to-br ${config.bg} ${sizeClasses[size]} rounded-full font-semibold text-white shadow-lg transform transition-all duration-200 hover:scale-105 hover:shadow-xl flex items-center gap-1.5`}
                style={{
                    boxShadow: '0 4px 14px rgba(0,0,0,0.15), inset 0 -2px 4px rgba(0,0,0,0.1), inset 0 2px 4px rgba(255,255,255,0.3)'
                }}>
                <span className="text-white/90">{config.icon}</span>
                <span>{config.text}</span>
            </div>
        </div>
    );
}

export default StatusBadge;
