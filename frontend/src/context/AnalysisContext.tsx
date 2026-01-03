import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

interface AnalysisContextType {
    isAnalyzing: boolean;
    portfolioRequestId: string | null;
    startPortfolioAnalysis: (tickers: string[]) => Promise<void>;
    progress: number;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export const AnalysisProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { token, user } = useAuth();
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [portfolioRequestId, setPortfolioRequestId] = useState<string | null>(() => {
        return localStorage.getItem('portfolio_request_id');
    });
    const [progress, setProgress] = useState(0);

    // Poll for status if we have a request ID
    useEffect(() => {
        if (!portfolioRequestId || !token) return;

        let pollInterval: any;

        const checkStatus = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/portfolio/status/${portfolioRequestId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                const { status, progress: currentProgress, results } = response.data;
                setProgress(currentProgress || 0);

                if (status === 'completed' || status === 'failed') {
                    setIsAnalyzing(false);
                    setPortfolioRequestId(null);
                    localStorage.removeItem('portfolio_request_id');

                    // Update local storage portfolio with results
                    if (results && results.length > 0) {
                        const saved = localStorage.getItem('elida_portfolio');
                        let portfolio = saved ? JSON.parse(saved) : [];

                        // Merge results
                        portfolio = portfolio.map((p: any) => {
                            const result = results.find((r: any) => r.ticker === p.ticker);
                            if (result) {
                                return {
                                    ...p,
                                    status: 'analyzed',
                                    score: result.match_score,
                                    recommendation: result.recommendation,
                                    risk: result.risk,
                                    analyzedAt: new Date().toISOString()
                                };
                            }
                            return p;
                        });

                        localStorage.setItem('elida_portfolio', JSON.stringify(portfolio));
                        // Dispatch storage event to notify PortfolioPage
                        window.dispatchEvent(new Event('storage'));
                    }
                } else {
                    setIsAnalyzing(true);
                }
            } catch (error) {
                console.error("Polling error", error);
                setIsAnalyzing(false);
                setPortfolioRequestId(null);
                localStorage.removeItem('portfolio_request_id');
            }
        };

        checkStatus(); // Initial check
        pollInterval = setInterval(checkStatus, 2000); // Poll every 2 seconds

        return () => clearInterval(pollInterval);
    }, [portfolioRequestId, token]);

    const startPortfolioAnalysis = async (tickers: string[]) => {
        if (!user || !token) return;

        setIsAnalyzing(true);
        setProgress(0);

        try {
            const response = await axios.post('http://localhost:8000/api/portfolio/scan',
                { user_id: user.id || 1, tickers },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            const { request_id } = response.data;
            setPortfolioRequestId(request_id);
            localStorage.setItem('portfolio_request_id', request_id);
        } catch (error) {
            console.error("Failed to start scan", error);
            setIsAnalyzing(false);
        }
    };

    return (
        <AnalysisContext.Provider value={{ isAnalyzing, portfolioRequestId, startPortfolioAnalysis, progress }}>
            {children}
        </AnalysisContext.Provider>
    );
};

export const useAnalysis = () => {
    const context = useContext(AnalysisContext);
    if (!context) {
        throw new Error('useAnalysis must be used within an AnalysisProvider');
    }
    return context;
};
