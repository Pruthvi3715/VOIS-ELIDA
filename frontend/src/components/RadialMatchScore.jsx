import { useEffect, useState } from 'react';

function RadialMatchScore({ score, size = 200 }) {
    const [animatedScore, setAnimatedScore] = useState(0);

    useEffect(() => {
        // Animate score from 0 to target
        const timer = setTimeout(() => {
            let current = 0;
            const interval = setInterval(() => {
                current += 2;
                if (current >= score) {
                    setAnimatedScore(score);
                    clearInterval(interval);
                } else {
                    setAnimatedScore(current);
                }
            }, 20);
            return () => clearInterval(interval);
        }, 300);
        return () => clearTimeout(timer);
    }, [score]);

    const radius = size / 2 - 15;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (animatedScore / 100) * circumference;

    // Color based on score
    const getColor = () => {
        if (animatedScore >= 75) return '#10b981'; // green
        if (animatedScore >= 50) return '#f59e0b'; // amber
        return '#ef4444'; // red
    };

    const getLabel = () => {
        if (animatedScore >= 75) return 'Strong Match';
        if (animatedScore >= 50) return 'Moderate Match';
        return 'Weak Match';
    };

    return (
        <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
            {/* 3D Shadow layers */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 blur-xl opacity-60"></div>
            <div className="absolute inset-2 rounded-full bg-gradient-to-br from-gray-50 to-white blur-lg opacity-80"></div>

            {/* Main SVG */}
            <svg width={size} height={size} className="relative transform rotate-[-90deg]">
                {/* Background circle */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="12"
                />
                {/* Progress circle with 3D effect */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    fill="none"
                    stroke={getColor()}
                    strokeWidth="12"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                    style={{
                        filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.15))'
                    }}
                />
                {/* Inner glow */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius - 8}
                    fill="none"
                    stroke={getColor()}
                    strokeWidth="2"
                    opacity="0.3"
                />
            </svg>

            {/* Center content */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <div className="text-5xl font-bold text-gray-900" style={{ textShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                    {animatedScore}
                </div>
                <div className="text-xs text-gray-500 font-medium mt-1">
                    {getLabel()}
                </div>
            </div>
        </div>
    );
}

export default RadialMatchScore;
