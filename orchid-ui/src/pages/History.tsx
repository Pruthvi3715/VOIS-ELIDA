import { useState, useEffect } from 'react'
import { Clock, TrendingUp, TrendingDown, Minus, Trash2 } from 'lucide-react'
import { Card, Badge } from '../components/ui'
import { api } from '../api/client'
import { useNavigate } from 'react-router-dom'

interface Analysis {
  ticker: string
  timestamp: string
  verdict: string
  match_score: number
  confidence: number
}

export default function History() {
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    api.getHistory()
      .then(data => {
        setAnalyses(data?.analyses || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const getVerdictIcon = (verdict: string) => {
    switch (verdict?.toUpperCase()) {
      case 'BUY':
      case 'STRONG BUY':
        return <TrendingUp size={16} className="text-emerald-400" />
      case 'SELL':
      case 'STRONG SELL':
        return <TrendingDown size={16} className="text-red-400" />
      default:
        return <Minus size={16} className="text-amber-400" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Analysis History</h1>
        <p className="text-slate-400">View your past stock analyses</p>
      </div>

      {analyses.length === 0 ? (
        <Card className="text-center py-12">
          <Clock size={48} className="mx-auto text-slate-600 mb-4" />
          <p className="text-slate-400">No analysis history yet.</p>
          <p className="text-sm text-slate-500 mt-1">Your analyses will appear here after you analyze stocks.</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {analyses.map((analysis, i) => (
            <Card
              key={i}
              className="cursor-pointer hover:border-primary-500/50 transition-all"
              onClick={() => navigate(`/analysis/${analysis.ticker}`)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center">
                    {getVerdictIcon(analysis.verdict)}
                  </div>
                  <div>
                    <div className="font-semibold">{analysis.ticker}</div>
                    <div className="text-sm text-slate-400">
                      {new Date(analysis.timestamp).toLocaleString()}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <div className="text-sm text-slate-400">Match Score</div>
                    <div className="font-semibold">{analysis.match_score || 'N/A'}%</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-400">Confidence</div>
                    <div className="font-semibold">{analysis.confidence || 'N/A'}%</div>
                  </div>
                  <Badge
                    variant={
                      analysis.verdict?.toUpperCase().includes('BUY') ? 'success' :
                      analysis.verdict?.toUpperCase().includes('SELL') ? 'danger' : 'warning'
                    }
                    size="md"
                  >
                    {analysis.verdict || 'HOLD'}
                  </Badge>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
