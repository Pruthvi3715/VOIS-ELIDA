import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, TrendingUp, TrendingDown, Clock, Star } from 'lucide-react'
import { Card, Button, Badge } from '../components/ui'
import { api } from '../api/client'

const TRENDING = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']

export default function Dashboard() {
  const [query, setQuery] = useState('')
  const [trendingData, setTrendingData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [recentAnalyses, setRecentAnalyses] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    Promise.all(TRENDING.map(t => api.getMarketData(t).catch(() => null)))
      .then(results => {
        setTrendingData(results.filter(Boolean))
        setLoading(false)
      })

    api.getHistory().then(data => {
      setRecentAnalyses(data?.analyses?.slice(0, 3) || [])
    }).catch(() => {})
  }, [])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      navigate(`/analysis/${query.trim().toUpperCase()}`)
    }
  }

  const handleQuickAnalyze = (ticker: string) => {
    navigate(`/analysis/${ticker}`)
  }

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in">
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold mb-4">
          AI-Powered <span className="gradient-text">Investment Analysis</span>
        </h1>
        <p className="text-slate-400 text-lg mb-8">
          Get personalized investment insights from our multi-agent AI system
        </p>

        <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter stock symbol (e.g., TCS.NS, RELIANCE.NS)"
              className="w-full bg-slate-800/50 border border-slate-600/50 rounded-xl pl-12 pr-32 py-4 text-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <Button
              type="submit"
              size="lg"
              className="absolute right-2 top-1/2 -translate-y-1/2"
            >
              Analyze
            </Button>
          </div>
        </form>

        <div className="flex items-center justify-center gap-2 mt-4">
          <span className="text-sm text-slate-500">Quick:</span>
          {TRENDING.map(t => (
            <button
              key={t}
              onClick={() => handleQuickAnalyze(t)}
              className="px-3 py-1 text-sm bg-slate-800/50 hover:bg-slate-700/50 rounded-full text-slate-300 transition-colors"
            >
              {t.replace('.NS', '')}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {loading ? (
          Array(4).fill(0).map((_, i) => (
            <Card key={i} className="animate-pulse">
              <div className="h-4 bg-slate-700 rounded w-20 mb-3" />
              <div className="h-8 bg-slate-700 rounded w-28 mb-2" />
              <div className="h-3 bg-slate-700 rounded w-16" />
            </Card>
          ))
        ) : (
          trendingData.map((stock, i) => (
            <Card
              key={i}
              className="cursor-pointer hover:border-primary-500/50 transition-all"
              onClick={() => handleQuickAnalyze(TRENDING[i])}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-slate-300">{TRENDING[i].replace('.NS', '')}</span>
                <Badge variant={stock?.change >= 0 ? 'success' : 'danger'}>
                  {stock?.change >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                  <span className="ml-1">{stock?.change?.toFixed(2) || 0}%</span>
                </Badge>
              </div>
              <div className="text-2xl font-bold text-white">
                ₹{stock?.price?.toLocaleString() || 'N/A'}
              </div>
              <div className="text-xs text-slate-500 mt-1">
                Vol: {stock?.volume?.toLocaleString() || 'N/A'}
              </div>
            </Card>
          ))
        )}
      </div>

      {recentAnalyses.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Clock size={18} className="text-slate-400" />
            Recent Analyses
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recentAnalyses.map((analysis, i) => (
              <Card
                key={i}
                className="cursor-pointer hover:border-primary-500/50 transition-all"
                onClick={() => handleQuickAnalyze(analysis.ticker)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold">{analysis.ticker}</span>
                  <Badge variant={analysis.verdict === 'BUY' ? 'success' : analysis.verdict === 'SELL' ? 'danger' : 'warning'}>
                    {analysis.verdict}
                  </Badge>
                </div>
                <div className="flex items-center gap-2">
                  <Star size={14} className="text-amber-400" />
                  <span className="text-sm">Match: {analysis.match_score || 'N/A'}%</span>
                </div>
                <div className="text-xs text-slate-500 mt-2">
                  {new Date(analysis.timestamp).toLocaleDateString()}
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
