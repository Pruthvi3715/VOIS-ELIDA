import { useState, useEffect } from 'react'
import { Plus, Trash2, TrendingUp, TrendingDown, RefreshCw } from 'lucide-react'
import { Card, Button, Input, Badge } from '../components/ui'
import { api } from '../api/client'
import { useNavigate } from 'react-router-dom'

interface PortfolioItem {
  ticker: string
  shares: number
  avgPrice: number
}

export default function Portfolio() {
  const [portfolio, setPortfolio] = useState<PortfolioItem[]>([])
  const [marketData, setMarketData] = useState<Record<string, any>>({})
  const [loading, setLoading] = useState(false)
  const [newTicker, setNewTicker] = useState('')
  const [newShares, setNewShares] = useState('')
  const [newPrice, setNewPrice] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const saved = localStorage.getItem('elida_portfolio')
    if (saved) {
      setPortfolio(JSON.parse(saved))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem('elida_portfolio', JSON.stringify(portfolio))
    if (portfolio.length > 0) {
      refreshMarketData()
    }
  }, [portfolio])

  const refreshMarketData = async () => {
    setLoading(true)
    const results: Record<string, any> = {}
    await Promise.all(
      portfolio.map(async (item) => {
        try {
          const data = await api.getMarketData(item.ticker)
          results[item.ticker] = data
        } catch {
          results[item.ticker] = null
        }
      })
    )
    setMarketData(results)
    setLoading(false)
  }

  const addToPortfolio = () => {
    if (!newTicker || !newShares || !newPrice) return
    
    const ticker = newTicker.toUpperCase()
    const existing = portfolio.find(p => p.ticker === ticker)
    
    if (existing) {
      setPortfolio(portfolio.map(p => 
        p.ticker === ticker 
          ? { ...p, shares: p.shares + parseFloat(newShares), avgPrice: parseFloat(newPrice) }
          : p
      ))
    } else {
      setPortfolio([...portfolio, {
        ticker,
        shares: parseFloat(newShares),
        avgPrice: parseFloat(newPrice)
      }])
    }
    
    setNewTicker('')
    setNewShares('')
    setNewPrice('')
  }

  const removeFromPortfolio = (ticker: string) => {
    setPortfolio(portfolio.filter(p => p.ticker !== ticker))
  }

  const getTotalValue = () => {
    return portfolio.reduce((sum, item) => {
      const price = marketData[item.ticker]?.price || item.avgPrice
      return sum + (price * item.shares)
    }, 0)
  }

  const getTotalGainLoss = () => {
    return portfolio.reduce((sum, item) => {
      const currentPrice = marketData[item.ticker]?.price || item.avgPrice
      const gain = (currentPrice - item.avgPrice) * item.shares
      return sum + gain
    }, 0)
  }

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Portfolio</h1>
          <p className="text-slate-400">Track your investments</p>
        </div>
        <Button onClick={refreshMarketData} loading={loading} variant="secondary">
          <RefreshCw size={16} className="mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <p className="text-sm text-slate-400 mb-1">Total Value</p>
          <p className="text-2xl font-bold">₹{getTotalValue().toLocaleString()}</p>
        </Card>
        <Card>
          <p className="text-sm text-slate-400 mb-1">Total Gain/Loss</p>
          <p className={`text-2xl font-bold ${getTotalGainLoss() >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {getTotalGainLoss() >= 0 ? '+' : ''}₹{getTotalGainLoss().toLocaleString()}
          </p>
        </Card>
        <Card>
          <p className="text-sm text-slate-400 mb-1">Holdings</p>
          <p className="text-2xl font-bold">{portfolio.length}</p>
        </Card>
      </div>

      <Card className="mb-6">
        <h3 className="font-semibold mb-4">Add Stock</h3>
        <div className="flex gap-4">
          <Input
            placeholder="Ticker (e.g., TCS.NS)"
            value={newTicker}
            onChange={(e) => setNewTicker(e.target.value)}
          />
          <Input
            type="number"
            placeholder="Shares"
            value={newShares}
            onChange={(e) => setNewShares(e.target.value)}
          />
          <Input
            type="number"
            placeholder="Avg Price"
            value={newPrice}
            onChange={(e) => setNewPrice(e.target.value)}
          />
          <Button onClick={addToPortfolio}>
            <Plus size={16} className="mr-2" />
            Add
          </Button>
        </div>
      </Card>

      {portfolio.length === 0 ? (
        <Card className="text-center py-12">
          <p className="text-slate-400">No stocks in portfolio. Add some to get started.</p>
        </Card>
      ) : (
        <Card padding="none">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left p-4 text-sm font-medium text-slate-400">Stock</th>
                <th className="text-right p-4 text-sm font-medium text-slate-400">Shares</th>
                <th className="text-right p-4 text-sm font-medium text-slate-400">Avg Price</th>
                <th className="text-right p-4 text-sm font-medium text-slate-400">Current</th>
                <th className="text-right p-4 text-sm font-medium text-slate-400">P&L</th>
                <th className="p-4"></th>
              </tr>
            </thead>
            <tbody>
              {portfolio.map((item) => {
                const current = marketData[item.ticker]?.price || item.avgPrice
                const pl = (current - item.avgPrice) * item.shares
                const plPercent = ((current - item.avgPrice) / item.avgPrice) * 100

                return (
                  <tr key={item.ticker} className="border-b border-slate-700/50 hover:bg-slate-800/30">
                    <td className="p-4">
                      <button
                        onClick={() => navigate(`/analysis/${item.ticker}`)}
                        className="font-medium hover:text-primary-400 transition-colors"
                      >
                        {item.ticker}
                      </button>
                    </td>
                    <td className="p-4 text-right">{item.shares}</td>
                    <td className="p-4 text-right">₹{item.avgPrice.toLocaleString()}</td>
                    <td className="p-4 text-right">₹{current.toLocaleString()}</td>
                    <td className="p-4 text-right">
                      <div className={`flex items-center justify-end gap-1 ${pl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        {pl >= 0 ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                        <span>₹{Math.abs(pl).toLocaleString()}</span>
                        <span className="text-xs">({plPercent.toFixed(1)}%)</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <button
                        onClick={() => removeFromPortfolio(item.ticker)}
                        className="text-slate-400 hover:text-red-400 transition-colors"
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </Card>
      )}
    </div>
  )
}
