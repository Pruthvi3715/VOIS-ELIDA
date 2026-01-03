interface AgentStatus {
  name: string
  status: 'pending' | 'running' | 'complete' | 'error'
  message?: string
}

interface AnalysisProgressProps {
  agents: AgentStatus[]
  currentAgent?: string
}

export function AnalysisProgress({ agents, currentAgent }: AnalysisProgressProps) {
  const getStatusIcon = (status: AgentStatus['status']) => {
    switch (status) {
      case 'complete':
        return <span className="text-emerald-400">&#10003;</span>
      case 'running':
        return (
          <span className="inline-block w-4 h-4 border-2 border-primary-400 border-t-transparent rounded-full animate-spin" />
        )
      case 'error':
        return <span className="text-red-400">&#10007;</span>
      default:
        return <span className="text-slate-500">&#9679;</span>
    }
  }

  return (
    <div className="space-y-3">
      {agents.map((agent) => (
        <div
          key={agent.name}
          className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${
            agent.status === 'running'
              ? 'bg-primary-500/10 border border-primary-500/30'
              : agent.status === 'complete'
              ? 'bg-emerald-500/10 border border-emerald-500/20'
              : 'bg-slate-800/30'
          }`}
        >
          <div className="w-6 h-6 flex items-center justify-center">
            {getStatusIcon(agent.status)}
          </div>
          <div className="flex-1">
            <div className="font-medium text-sm">{agent.name}</div>
            {agent.message && (
              <div className="text-xs text-slate-400 mt-0.5">{agent.message}</div>
            )}
          </div>
          {agent.status === 'running' && (
            <div className="w-24 h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <div className="h-full bg-primary-500 rounded-full animate-pulse" style={{ width: '60%' }} />
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
