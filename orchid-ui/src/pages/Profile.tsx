import { useState, useEffect } from 'react'
import { Save, RotateCcw } from 'lucide-react'
import { Card, Button, Input } from '../components/ui'
import { api } from '../api/client'

const DEFAULT_PROFILE = {
  risk_tolerance: 'moderate',
  time_horizon: 'medium',
  investment_style: 'growth',
  max_portfolio_allocation: 10,
  sector_preferences: [] as string[],
  excluded_sectors: [] as string[],
}

const SECTORS = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer', 'Industrial', 'Materials', 'Utilities']
const RISK_LEVELS = ['conservative', 'moderate', 'aggressive']
const TIME_HORIZONS = ['short', 'medium', 'long']
const INVESTMENT_STYLES = ['value', 'growth', 'dividend', 'momentum']

export default function Profile() {
  const [profile, setProfile] = useState(DEFAULT_PROFILE)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    api.getProfile().then(data => {
      if (data) {
        setProfile({ ...DEFAULT_PROFILE, ...data })
      }
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const handleSave = async () => {
    setSaving(true)
    try {
      await api.saveProfile('default_user', profile)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (err) {
      console.error('Failed to save profile', err)
    }
    setSaving(false)
  }

  const handleReset = () => {
    setProfile(DEFAULT_PROFILE)
  }

  const toggleSector = (sector: string, type: 'preferences' | 'excluded') => {
    const key = type === 'preferences' ? 'sector_preferences' : 'excluded_sectors'
    const otherKey = type === 'preferences' ? 'excluded_sectors' : 'sector_preferences'
    
    setProfile(prev => ({
      ...prev,
      [key]: prev[key].includes(sector) 
        ? prev[key].filter(s => s !== sector)
        : [...prev[key], sector],
      [otherKey]: prev[otherKey].filter(s => s !== sector)
    }))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Investor DNA</h1>
          <p className="text-slate-400">Configure your investment profile for personalized analysis</p>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" onClick={handleReset}>
            <RotateCcw size={16} className="mr-2" />
            Reset
          </Button>
          <Button onClick={handleSave} loading={saving}>
            <Save size={16} className="mr-2" />
            {saved ? 'Saved!' : 'Save'}
          </Button>
        </div>
      </div>

      <div className="space-y-6">
        <Card>
          <h3 className="font-semibold mb-4">Risk & Time</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Risk Tolerance</label>
              <div className="flex gap-2">
                {RISK_LEVELS.map(level => (
                  <button
                    key={level}
                    onClick={() => setProfile(p => ({ ...p, risk_tolerance: level }))}
                    className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                      profile.risk_tolerance === level
                        ? 'bg-primary-500 text-white'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Time Horizon</label>
              <div className="flex gap-2">
                {TIME_HORIZONS.map(horizon => (
                  <button
                    key={horizon}
                    onClick={() => setProfile(p => ({ ...p, time_horizon: horizon }))}
                    className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                      profile.time_horizon === horizon
                        ? 'bg-primary-500 text-white'
                        : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    {horizon.charAt(0).toUpperCase() + horizon.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="font-semibold mb-4">Investment Style</h3>
          <div className="flex flex-wrap gap-2">
            {INVESTMENT_STYLES.map(style => (
              <button
                key={style}
                onClick={() => setProfile(p => ({ ...p, investment_style: style }))}
                className={`py-2 px-4 rounded-lg text-sm font-medium transition-all ${
                  profile.investment_style === style
                    ? 'bg-primary-500 text-white'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
              >
                {style.charAt(0).toUpperCase() + style.slice(1)}
              </button>
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="font-semibold mb-4">Max Portfolio Allocation</h3>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min="5"
              max="50"
              value={profile.max_portfolio_allocation}
              onChange={(e) => setProfile(p => ({ ...p, max_portfolio_allocation: parseInt(e.target.value) }))}
              className="flex-1 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
            />
            <span className="text-lg font-semibold w-16 text-right">{profile.max_portfolio_allocation}%</span>
          </div>
          <p className="text-xs text-slate-500 mt-2">Maximum allocation per stock in your portfolio</p>
        </Card>

        <Card>
          <h3 className="font-semibold mb-4">Sector Preferences</h3>
          <p className="text-sm text-slate-400 mb-3">Click to prefer (green) or exclude (red) sectors</p>
          <div className="flex flex-wrap gap-2">
            {SECTORS.map(sector => {
              const isPreferred = profile.sector_preferences.includes(sector)
              const isExcluded = profile.excluded_sectors.includes(sector)
              
              return (
                <button
                  key={sector}
                  onClick={() => {
                    if (isPreferred) {
                      toggleSector(sector, 'excluded')
                    } else if (isExcluded) {
                      setProfile(p => ({
                        ...p,
                        excluded_sectors: p.excluded_sectors.filter(s => s !== sector)
                      }))
                    } else {
                      toggleSector(sector, 'preferences')
                    }
                  }}
                  className={`py-2 px-4 rounded-lg text-sm font-medium transition-all ${
                    isPreferred
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : isExcluded
                      ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                      : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                  }`}
                >
                  {sector}
                </button>
              )
            })}
          </div>
        </Card>
      </div>
    </div>
  )
}
