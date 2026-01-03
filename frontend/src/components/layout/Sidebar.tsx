import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, PieChart, Settings, Activity, History, User, Sparkles } from 'lucide-react';

const Sidebar: React.FC = () => {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: PieChart, label: 'Portfolio', path: '/portfolio' },
        { icon: Sparkles, label: 'Analysis', path: '/analysis' },
        { icon: History, label: 'History', path: '/history' },
        { icon: User, label: 'Profile', path: '/profile' },
        { icon: Settings, label: 'Settings', path: '/settings' },
    ];

    return (
        <aside className="w-64 h-screen bg-surface/50 backdrop-blur-xl border-r border-glass-border pt-20 flex flex-col fixed left-0 top-0 z-40 transition-transform duration-300 transform md:translate-x-0 -translate-x-full">
            {/* Menu Label */}
            <div className="px-4 py-4">
                <p className="text-xs font-semibold text-secondary/60 uppercase tracking-wider mb-2 px-3">
                    Navigation
                </p>

                {/* Nav Items */}
                <nav className="space-y-1">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            end={item.path === '/'}
                            className={({ isActive }) => `
                                group flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200
                                ${isActive
                                    ? 'bg-gradient-primary text-white shadow-glow'
                                    : 'text-secondary hover:bg-glass-light hover:text-white'
                                }
                            `}
                        >
                            {({ isActive }) => (
                                <>
                                    <item.icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-secondary group-hover:text-white'}`} />
                                    <span className="font-medium">{item.label}</span>
                                </>
                            )}
                        </NavLink>
                    ))}
                </nav>
            </div>

            {/* Bottom section */}
            <div className="mt-auto p-4">
                <div className="p-4 rounded-xl bg-gradient-glass border border-glass-border">
                    <p className="text-xs text-secondary mb-2">AI Agents Status</p>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                        <span className="text-sm text-white font-medium">5 Active</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
