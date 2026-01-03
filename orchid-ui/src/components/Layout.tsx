import { Outlet, NavLink } from 'react-router-dom'
import { LayoutDashboard, LineChart, Briefcase, User, History, Bot } from 'lucide-react'
import { useState } from 'react'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/analysis', icon: LineChart, label: 'Analysis' },
  { to: '/portfolio', icon: Briefcase, label: 'Portfolio' },
  { to: '/profile', icon: User, label: 'Profile' },
  { to: '/history', icon: History, label: 'History' },
]

export default function Layout() {
  const [chatOpen, setChatOpen] = useState(false)

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-slate-900/50 border-r border-slate-700/50 p-4 flex flex-col">
        <div className="mb-8">
          <h1 className="text-2xl font-bold gradient-text">ELIDA</h1>
          <p className="text-xs text-slate-500">AI Investment Advisor</p>
        </div>

        <nav className="flex-1 space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-500/20 text-primary-400'
                    : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'
                }`
              }
            >
              <Icon size={20} />
              <span className="font-medium">{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="pt-4 border-t border-slate-700/50">
          <p className="text-xs text-slate-500 text-center">Orchid UI v1.0</p>
        </div>
      </aside>

      <main className="flex-1 overflow-auto">
        <div className="p-6">
          <Outlet />
        </div>
      </main>

      <button
        onClick={() => setChatOpen(!chatOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-primary-500 hover:bg-primary-600 rounded-full flex items-center justify-center shadow-lg shadow-primary-500/30 transition-all duration-200 z-50"
      >
        <Bot size={24} className="text-white" />
      </button>

      {chatOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[500px] bg-slate-900 border border-slate-700 rounded-xl shadow-2xl z-50 flex flex-col animate-slide-up">
          <div className="p-4 border-b border-slate-700 flex items-center justify-between">
            <h3 className="font-semibold">AI Assistant</h3>
            <button onClick={() => setChatOpen(false)} className="text-slate-400 hover:text-white">
              &times;
            </button>
          </div>
          <div className="flex-1 p-4 overflow-auto">
            <div className="text-slate-400 text-sm text-center mt-20">
              Ask me anything about your investments...
            </div>
          </div>
          <div className="p-4 border-t border-slate-700">
            <input
              type="text"
              placeholder="Type your question..."
              className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>
      )}
    </div>
  )
}
