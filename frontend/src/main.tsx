import React from 'react'
// Force HMR update
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { AnalysisProvider } from './context/AnalysisContext'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <AnalysisProvider>
          <App />
        </AnalysisProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
