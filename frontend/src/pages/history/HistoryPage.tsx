import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { History, Search, Clock, TrendingUp, ChevronRight, Loader2, Trash2, Calendar } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';

interface HistoryItem {
    id: number;
    query: string;
    query_type: string;
    timestamp: string;
    result?: any;
}

const HistoryPage: React.FC = () => {
    const { token } = useAuth();
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            setLoading(true);
            const response = await axios.get('http://localhost:8000/api/v1/history', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setHistory(response.data.entries || []);
        } catch (err) {
            console.error('Failed to fetch history:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id: number, e: React.MouseEvent) => {
        e.preventDefault(); // Prevent navigation
        try {
            await axios.delete(`http://localhost:8000/api/v1/history/${id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setHistory(prev => prev.filter(item => item.id !== id));
        } catch (err) {
            console.error('Failed to delete history item:', err);
        }
    };

    const formatDate = (timestamp: string) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString();
    };

    const filteredHistory = history.filter(item =>
        item.query?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <History className="w-8 h-8 text-primary-400" />
                        Analysis History
                    </h1>
                    <p className="text-secondary mt-1">View your past stock analyses and research</p>
                </div>
            </div>

            {/* Search */}
            <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-secondary" />
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search history..."
                    className="input-glass pl-12"
                />
            </div>

            {/* History List */}
            {loading ? (
                <div className="flex items-center justify-center py-24">
                    <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
                </div>
            ) : filteredHistory.length === 0 ? (
                <div className="glass-card p-12 text-center">
                    <Clock className="w-16 h-16 text-secondary/30 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-white mb-2">No history yet</h3>
                    <p className="text-secondary mb-6">Analyze some stocks to see them here</p>
                    <Link
                        to="/"
                        className="btn-primary inline-flex items-center gap-2"
                    >
                        <TrendingUp className="w-4 h-4" />
                        Start Analyzing
                    </Link>
                </div>
            ) : (
                <div className="grid gap-4">
                    {filteredHistory.map((item) => (
                        <motion.div
                            key={item.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="group"
                        >
                            <Link
                                to={`/analysis/${item.query}`}
                                className="glass-card p-4 flex items-center justify-between hover:border-primary-500/30 hover:bg-glass-light transition-all"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500/20 to-secondary/20 flex items-center justify-center border border-glass-border">
                                        <TrendingUp className="w-6 h-6 text-white" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-white text-lg group-hover:text-primary-400 transition-colors">
                                            {item.query}
                                        </h4>
                                        <div className="flex items-center gap-3 text-sm text-secondary">
                                            <div className="flex items-center gap-1">
                                                <Calendar className="w-3.5 h-3.5" />
                                                <span>{formatDate(item.timestamp)}</span>
                                            </div>
                                            <span className="w-1 h-1 rounded-full bg-secondary/50" />
                                            <span className="capitalize px-2 py-0.5 rounded bg-surface-light border border-glass-border text-xs">
                                                {item.query_type}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex items-center gap-3">
                                    <button
                                        onClick={(e) => handleDelete(item.id, e)}
                                        className="p-2 rounded-lg text-secondary hover:text-error hover:bg-error/10 transition-colors opacity-0 group-hover:opacity-100"
                                        title="Delete entry"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                    <ChevronRight className="w-5 h-5 text-secondary group-hover:text-white group-hover:translate-x-1 transition-all" />
                                </div>
                            </Link>
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default HistoryPage;
