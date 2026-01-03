interface MatchScoreProps {
  score: number
  size?: 'sm' | 'md' | 'lg'
}

export function MatchScore({ score, size = 'md' }: MatchScoreProps) {
  const getColor = (s: number) => {
    if (s >= 80) return { stroke: '#10b981', text: 'text-emerald-400', label: 'Excellent Match' }
    if (s >= 60) return { stroke: '#0ea5e9', text: 'text-primary-400', label: 'Good Match' }
    if (s >= 40) return { stroke: '#f59e0b', text: 'text-amber-400', label: 'Moderate' }
    return { stroke: '#ef4444', text: 'text-red-400', label: 'Poor Match' }
  }

  const { stroke, text, label } = getColor(score)
  
  const sizes = {
    sm: { size: 80, strokeWidth: 6, fontSize: 'text-lg' },
    md: { size: 120, strokeWidth: 8, fontSize: 'text-2xl' },
    lg: { size: 160, strokeWidth: 10, fontSize: 'text-4xl' }
  }

  const { size: svgSize, strokeWidth, fontSize } = sizes[size]
  const radius = (svgSize - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        <svg width={svgSize} height={svgSize} className="-rotate-90">
          <circle
            cx={svgSize / 2}
            cy={svgSize / 2}
            r={radius}
            stroke="#334155"
            strokeWidth={strokeWidth}
            fill="none"
          />
          <circle
            cx={svgSize / 2}
            cy={svgSize / 2}
            r={radius}
            stroke={stroke}
            strokeWidth={strokeWidth}
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`font-bold ${fontSize} ${text}`}>{score}</span>
        </div>
      </div>
      <span className={`mt-2 text-sm font-medium ${text}`}>{label}</span>
    </div>
  )
}
