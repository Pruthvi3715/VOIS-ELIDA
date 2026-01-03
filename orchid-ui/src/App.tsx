import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Analysis from './pages/Analysis'
import Portfolio from './pages/Portfolio'
import Profile from './pages/Profile'
import History from './pages/History'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="analysis" element={<Analysis />} />
        <Route path="analysis/:ticker" element={<Analysis />} />
        <Route path="portfolio" element={<Portfolio />} />
        <Route path="profile" element={<Profile />} />
        <Route path="history" element={<History />} />
      </Route>
    </Routes>
  )
}
