import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
    History,
    Search,
    Clock,
    TrendingUp,
    ChevronRight,
    Loader2,
    BarChart3,
    Trash2,
    RefreshCw
} from 'lucide-react';
import { API_BASE_URL, getUserId } from '../api';

function HistoryPage() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/history?limit=50`);
            const data = await response.json();
            // Handle both array and {entries: []} format
            const entries = data.entries || data;
            setHistory(Array.isArray(entries) ? entries : []);
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

    const filteredHistory = history.filter(item => {
        const queryVal = item.query || item.asset_id || '';
        return queryVal.toLowerCase().includes(searchQuery.toLowerCase());
    });

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-surface-light border border-glass-border">
                            <History className="w-6 h-6 text-primary-400" />
                        </div>
                        Analysis History
                    </h1>
                    <p className="text-secondary mt-1">View your past stock analyses</p>
                </div>
                <button
                    onClick={fetchHistory}
                    className="flex items-center gap-2 px-4 py-2 bg-surface-light border border-glass-border rounded-xl text-gray-300 hover:text-white hover:bg-surface-light/80 transition-all"
                >
                    <RefreshCw className="w-4 h-4" />
                    Refresh
                </button>
            </div>

            {/* Search */}
            <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search history..."
                    className="w-full bg-surface-light/50 border border-glass-border rounded-xl pl-12 pr-4 py-3 text-white placeholder-gray-500 outline-none focus:border-primary-500/50 focus:ring-1 focus:ring-primary-500/30 transition"
                />
            </div>

            {/* History List */}
            {loading ? (
                <div className="flex items-center justify-center py-16">
                    <div className="text-center">
                        <Loader2 className="w-10 h-10 text-primary-400 animate-spin mx-auto mb-4" />
                        <p className="text-secondary">Loading history...</p>
                    </div>
                </div>
            ) : filteredHistory.length === 0 ? (
                <div className="glass-card rounded-xl border border-glass-border p-12 text-center">
                    <div className="w-20 h-20 rounded-full bg-surface-light border border-glass-border flex items-center justify-center mx-auto mb-4">
                        <Clock className="w-10 h-10 text-secondary" />
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">No history yet</h3>
                    <p className="text-secondary mb-6">Analyze some stocks to see them here</p>
                    <Link
                        to="/"
                        className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-accent-dark text-white rounded-xl font-medium hover:shadow-glow transition-all"
                    >
                        <TrendingUp className="w-5 h-5" />
                        Start Analyzing
                    </Link>
                </div>
            ) : (
                <div className="glass-card rounded-xl border border-glass-border overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="bg-surface-light/50 border-b border-glass-border">
                                    <th className="px-6 py-4 font-medium text-secondary text-sm uppercase tracking-wider">Asset</th>
                                    <th className="px-6 py-4 font-medium text-secondary text-sm uppercase tracking-wider">Type</th>
                                    <th className="px-6 py-4 font-medium text-secondary text-sm uppercase tracking-wider">Date</th>
                                    <th className="px-6 py-4 font-medium text-secondary text-sm text-right uppercase tracking-wider">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-glass-border">
                                {filteredHistory.map((item, index) => {
                                    const assetId = item.query || item.asset_id || 'Unknown';
                                    const queryType = item.query_type || item.type || 'analysis';
                                    const timestamp = item.timestamp || item.created_at;

                                    return (
                                        <tr
                                            key={item.id || index}
                                            className="hover:bg-surface-light/30 transition group cursor-pointer"
                                            onClick={() => navigate(`/analysis/${assetId}`)}
                                        >
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-10 h-10 rounded-lg bg-surface-light border border-glass-border flex items-center justify-center">
                                                        <BarChart3 className="w-5 h-5 text-primary-400" />
                                                    </div>
                                                    <span className="font-semibold text-white">{assetId}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium capitalize border ${queryType === 'analysis'
                                                        ? 'bg-primary-500/10 text-primary-400 border-primary-500/30'
                                                        : 'bg-success/10 text-success border-success/30'
                                                    }`}>
                                                    {queryType}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-secondary text-sm">
                                                {timestamp ? (
                                                    <>
                                                        {new Date(timestamp).toLocaleDateString()}
                                                        <span className="text-gray-600 mx-1">•</span>
                                                        {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                    </>
                                                ) : 'N/A'}
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <Link
                                                    to={`/analysis/${assetId}`}
                                                    className="inline-flex items-center justify-center w-8 h-8 rounded-full hover:bg-surface-light text-gray-400 hover:text-white transition"
                                                    onClick={(e) => e.stopPropagation()}
                                                >
                                                    <ChevronRight className="w-5 h-5" />
                                                </Link>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}

export default HistoryPage;
