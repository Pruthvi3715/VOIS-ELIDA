import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, RefreshCw, AlertTriangle, CheckCircle, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { Card, Button, Badge } from '../components/ui'
import { MatchScore } from '../components/MatchScore'
import { AnalysisProgress } from '../components/AnalysisProgress'
import { api } from '../api/client'

const AGENTS = [
  { name: 'Scout Agent', description: 'Collecting market data & news' },
  { name: 'Quant Agent', description: 'Analyzing fundamentals' },
  { name: 'Macro Agent', description: 'Evaluating economic indicators' },
  { name: 'Philosopher Agent', description: 'Assessing business quality' },
  { name: 'Regret Agent', description: 'Simulating risk scenarios' },
  { name: 'Coach Agent', description: 'Synthesizing final verdict' },
]

export default function Analysis() {
  const { ticker } = useParams()
  const navigate = useNavigate()
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [agentStatuses, setAgentStatuses] = useState<{name: string, description: string, status: 'pending' | 'running' | 'complete' | 'error', message?: string}[]>(
    AGENTS.map(a => ({ ...a, status: 'pending' }))
  )
  const [currentAgentIndex, setCurrentAgentIndex] = useState(-1)
  const [elapsedTime, setElapsedTime] = useState(0)

  useEffect(() => {
    if (ticker) {
      runAnalysis()
    }
  }, [ticker])

  useEffect(() => {
    let interval: number
    if (analyzing) {
      interval = setInterval(() => setElapsedTime(t => t + 1), 1000)
    }
    return () => clearInterval(interval)
  }, [analyzing])

  const simulateAgentProgress = () => {
    return new Promise<void>((resolve) => {
      let idx = 0
      const interval = setInterval(() => {
        if (idx < AGENTS.length) {
          setAgentStatuses(prev => prev.map((a, i) => ({
            ...a,
            status: i < idx ? 'complete' : i === idx ? 'running' : 'pending',
            message: i === idx ? a.description : undefined
          })))
          setCurrentAgentIndex(idx)
          idx++
        } else {
          clearInterval(interval)
          setAgentStatuses(prev => prev.map(a => ({ ...a, status: 'complete' })))
          resolve()
        }
      }, 2000)
    })
  }

  const runAnalysis = async () => {
    if (!ticker) return
    
    setAnalyzing(true)
    setResult(null)
    setError(null)
    setElapsedTime(0)
    setAgentStatuses(AGENTS.map(a => ({ ...a, status: 'pending' as const })))

    const progressPromise = simulateAgentProgress()

    try {
      const [analysisResult] = await Promise.all([
        api.analyzeStock(ticker),
        progressPromise
      ])
      setResult(analysisResult)
    } catch (err: any) {
      setError(err.message || 'Analysis failed')
      setAgentStatuses(prev => prev.map(a => 
        a.status === 'running' ? { ...a, status: 'error' } : a
      ))
    } finally {
      setAnalyzing(false)
    }
  }

  const getVerdictStyle = (verdict: string) => {
    switch (verdict?.toUpperCase()) {
      case 'BUY':
      case 'STRONG BUY':
        return { color: 'text-emerald-400', bg: 'bg-emerald-500/20', icon: TrendingUp }
      case 'SELL':
      case 'STRONG SELL':
        return { color: 'text-red-400', bg: 'bg-red-500/20', icon: TrendingDown }
      default:
        return { color: 'text-amber-400', bg: 'bg-amber-500/20', icon: Minus }
    }
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <button
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-slate-400 hover:text-white mb-6 transition-colors"
      >
        <ArrowLeft size={20} />
        Back to Dashboard
      </button>

      {ticker && (
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold">{ticker}</h1>
            <p className="text-slate-400">Investment Analysis</p>
          </div>
          <Button
            onClick={runAnalysis}
            disabled={analyzing}
            loading={analyzing}
            variant="secondary"
          >
            <RefreshCw size={16} className="mr-2" />
            Re-analyze
          </Button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <Card className="mb-6">
            <h3 className="font-semibold mb-4">Analysis Progress</h3>
            <AnalysisProgress agents={agentStatuses} />
            {analyzing && (
              <div className="mt-4 text-center text-sm text-slate-400">
                Elapsed: {Math.floor(elapsedTime / 60)}:{(elapsedTime % 60).toString().padStart(2, '0')}
              </div>
            )}
          </Card>
        </div>

        <div className="lg:col-span-2">
          {error && (
            <Card className="mb-6 border-red-500/30 bg-red-500/10">
              <div className="flex items-center gap-3 text-red-400">
                <AlertTriangle size={20} />
                <span>{error}</span>
              </div>
            </Card>
          )}

          {result && (
            <>
              <Card className="mb-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold mb-2">Match Score</h3>
                    <p className="text-sm text-slate-400">Based on your Investor DNA profile</p>
                  </div>
                  <MatchScore score={result.match_score || 0} size="lg" />
                </div>
              </Card>

              <Card className="mb-6">
                <h3 className="text-lg font-semibold mb-4">Final Verdict</h3>
                {(() => {
                  const style = getVerdictStyle(result.verdict)
                  const Icon = style.icon
                  return (
                    <div className={`flex items-center gap-4 p-4 rounded-lg ${style.bg}`}>
                      <Icon size={32} className={style.color} />
                      <div>
                        <div className={`text-2xl font-bold ${style.color}`}>
                          {result.verdict || 'HOLD'}
                        </div>
                        <div className="text-sm text-slate-400">
                          Confidence: {result.confidence || 'N/A'}%
                        </div>
                      </div>
                    </div>
                  )
                })()}
              </Card>

              {result.summary && (
                <Card className="mb-6">
                  <h3 className="text-lg font-semibold mb-3">Summary</h3>
                  <p className="text-slate-300 leading-relaxed">{result.summary}</p>
                </Card>
              )}

              {result.agents && (
                <Card>
                  <h3 className="text-lg font-semibold mb-4">Agent Insights</h3>
                  <div className="space-y-4">
                    {Object.entries(result.agents).map(([agent, data]: [string, any]) => (
                      <div key={agent} className="p-4 bg-slate-800/50 rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium capitalize">{agent.replace('_', ' ')}</span>
                          {data.sentiment && (
                            <Badge variant={
                              data.sentiment === 'positive' ? 'success' :
                              data.sentiment === 'negative' ? 'danger' : 'warning'
                            }>
                              {data.sentiment}
                            </Badge>
                          )}
                        </div>
                        {data.summary && (
                          <p className="text-sm text-slate-400">{data.summary}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </Card>
              )}
            </>
          )}

          {!result && !analyzing && !error && (
            <Card className="text-center py-12">
              <p className="text-slate-400">Enter a stock symbol to start analysis</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
