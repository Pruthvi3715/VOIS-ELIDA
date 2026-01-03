import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ProtectedRoute from './components/auth/ProtectedElement';

// Import pages
import Dashboard from './pages/dashboard/Dashboard';
import PortfolioPage from './pages/portfolio/PortfolioPage';
import ProfilePage from './pages/ProfilePage';
import AnalysisPage from './pages/AnalysisPage'; // Legacy, consider removing
import AnalysisResultsPage from './pages/analysis/AnalysisResultsPage';
import HistoryPage from './pages/history/HistoryPage';
import StockComparison from './pages/comparison/StockComparison';
import SettingsPage from './pages/settings/SettingsPage';

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected Routes */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="portfolio" element={<PortfolioPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="settings" element={<SettingsPage />} />
        <Route path="analysis" element={<AnalysisPage />} />
        <Route path="analysis/:symbol" element={<AnalysisResultsPage />} />
        <Route path="compare/:symbol1/:symbol2" element={<StockComparison />} />
      </Route>

      {/* Catch all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
