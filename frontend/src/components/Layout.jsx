import { Link, Outlet, useLocation } from 'react-router-dom';
import { Brain, Wifi, Settings } from 'lucide-react';
import { useState } from 'react';
import Chatbot from './Chatbot';
import InvestorDNASettings from './InvestorDNASettings';

function Layout() {
    const location = useLocation();
    const [showSettings, setShowSettings] = useState(false);

    const tabs = [
        { name: 'Dashboard', path: '/' },
        { name: 'Analysis', path: '/analysis' },
        { name: 'History', path: '/history' },
        { name: 'Portfolio', path: '/portfolio' },
        { name: 'Learn', path: '/learn' },
    ];

    const isActive = (path) => {
        if (path === '/') return location.pathname === '/';
        return location.pathname.startsWith(path);
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 px-6 py-4">
                <div className="max-w-7xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        {/* Logo */}
                        <div className="flex items-center gap-2">
                            <Brain className="w-8 h-8 text-gray-800" />
                            <span className="text-xl font-bold text-gray-900">AI Financial Advisor</span>
                        </div>
                        {/* Badges */}
                        <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full border border-gray-200">
                            Multi-Agent System
                        </span>
                        <div className="flex items-center gap-1.5 text-green-600 text-sm">
                            <Wifi className="w-4 h-4" />
                            <span>Live</span>
                        </div>
                    </div>
                    <Link
                        to="/profile"
                        className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
                    >
                        <Settings className="w-4 h-4 text-gray-600" />
                        <span className="text-gray-700">Profile</span>
                    </Link>
                </div>
            </header>

            {/* Tab Navigation */}
            <nav className="bg-white px-6 py-2 border-b border-gray-100">
                <div className="max-w-7xl mx-auto flex gap-2">
                    {tabs.map((tab) => (
                        <Link
                            key={tab.path}
                            to={tab.path}
                            className={`px-6 py-2.5 rounded-lg text-sm font-medium transition ${isActive(tab.path)
                                ? 'border-2 border-gray-800 text-gray-900 bg-white'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                                }`}
                        >
                            {tab.name}
                        </Link>
                    ))}
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-6 py-6">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="mt-auto py-6 text-center text-sm text-gray-500 border-t border-gray-100 bg-white">
                <p>AI Financial Advisor - Multi-Agent Investment Analysis System</p>
                <p className="text-amber-600">Powered by advanced AI algorithms | Not financial advice</p>
            </footer>

            {/* Floating Chatbot */}
            <div className="fixed bottom-6 left-6 z-50">
                <Chatbot />
            </div>

            {/* Settings Modal */}
            {showSettings && (
                <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
                    <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                        <InvestorDNASettings onClose={() => setShowSettings(false)} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default Layout;
