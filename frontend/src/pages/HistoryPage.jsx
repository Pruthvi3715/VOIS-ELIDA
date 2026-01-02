import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
    History,
    Search,
    Clock,
    TrendingUp,
    ChevronRight,
    Loader2,
    BarChart3
} from 'lucide-react';
import { API_BASE_URL, getUserId } from '../api';

function HistoryPage() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/history/${getUserId()}`);
            const data = await response.json();
            setHistory(Array.isArray(data) ? data : []);
        } catch (error) {
            console.error('Failed to fetch history:', error);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (timestamp) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
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
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
                    <History className="w-7 h-7 text-gray-700" />
                    Analysis History
                </h1>
                <p className="text-gray-500 mt-1">View your past stock analyses</p>
            </div>

            {/* Search */}
            <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search history..."
                    className="w-full bg-white border border-gray-200 rounded-xl pl-12 pr-4 py-3 text-gray-900 placeholder-gray-400 outline-none focus:border-gray-300 focus:ring-2 focus:ring-gray-100 transition"
                />
            </div>

            {/* History List */}
            {loading ? (
                <div className="flex items-center justify-center py-16">
                    <Loader2 className="w-8 h-8 text-gray-400 animate-spin" />
                </div>
            ) : filteredHistory.length === 0 ? (
                <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
                    <Clock className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">No history yet</h3>
                    <p className="text-gray-500 mb-4">Analyze some stocks to see them here</p>
                    <Link
                        to="/"
                        className="inline-flex items-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800 transition"
                    >
                        <TrendingUp className="w-5 h-5" />
                        Start Analyzing
                    </Link>
                </div>
            ) : (
                <div className="space-y-3">
                    {filteredHistory.map((item) => (
                        <Link
                            key={item.id}
                            to={`/analysis/${item.query}`}
                            className="block bg-white rounded-xl border border-gray-200 p-4 hover:bg-gray-50 hover:border-gray-300 transition group"
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">
                                        <BarChart3 className="w-6 h-6 text-gray-500" />
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-gray-900 group-hover:text-gray-700 transition">
                                            {item.query}
                                        </h4>
                                        <div className="flex items-center gap-2 text-sm text-gray-500">
                                            <Clock className="w-4 h-4" />
                                            <span>{formatDate(item.timestamp)}</span>
                                            <span className="text-gray-300">•</span>
                                            <span className="capitalize">{item.type}</span>
                                        </div>
                                    </div>
                                </div>
                                <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all" />
                            </div>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    );
}

export default HistoryPage;
