import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, PieChart, Settings, History, User, Sparkles, TrendingUp, Zap, Scale, BookOpen } from 'lucide-react';

const Sidebar: React.FC = () => {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: PieChart, label: 'Portfolio', path: '/portfolio' },
        { icon: Sparkles, label: 'Analysis', path: '/analysis', badge: 'AI' },
        { icon: Scale, label: 'Compare', path: '/compare' },
        { icon: History, label: 'History', path: '/history' },
        { icon: BookOpen, label: 'Learn', path: '/learn', badge: 'NEW' },
        { icon: User, label: 'Profile', path: '/profile' },
        { icon: Settings, label: 'Settings', path: '/settings' },
    ];

    return (
        <aside className="w-64 h-screen fixed left-0 top-0 z-40 hidden md:block">
            {/* Sidebar background */}
            <div className="absolute inset-0 bg-surface/90 backdrop-blur-xl border-r border-white/5" />

            <div className="relative h-full flex flex-col pt-24 pb-6">
                {/* Navigation */}
                <div className="px-4 flex-1">
                    <p className="text-xs font-semibold text-secondary uppercase tracking-wider mb-4 px-4">
                        Menu
                    </p>

                    <nav className="space-y-1">
                        {navItems.map((item) => (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                end={item.path === '/'}
                                className={({ isActive }) =>
                                    `nav-link ${isActive ? 'active' : ''}`
                                }
                            >
                                <item.icon className="w-5 h-5" />
                                <span>{item.label}</span>
                                {item.badge && (
                                    <span className="ml-auto badge-primary text-[10px] px-2 py-0.5">
                                        {item.badge}
                                    </span>
                                )}
                            </NavLink>
                        ))}
                    </nav>
                </div>

                {/* AI Status Card */}
                <div className="px-4 mt-4">
                    <div className="card-gradient p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <Zap className="w-4 h-4 text-accent" />
                            <span className="text-xs font-semibold text-secondary uppercase">
                                AI Status
                            </span>
                        </div>

                        <div className="flex items-center gap-2 mb-3">
                            <div className="relative">
                                <div className="w-2 h-2 rounded-full bg-success" />
                                <div className="absolute inset-0 w-2 h-2 rounded-full bg-success animate-ping" />
                            </div>
                            <span className="text-sm font-semibold text-white">
                                5 Agents Online
                            </span>
                        </div>

                        {/* Agent bars */}
                        <div className="flex gap-1">
                            {[1, 0.9, 0.8, 0.7, 0.6].map((opacity, i) => (
                                <div
                                    key={i}
                                    className="flex-1 h-1 rounded-full"
                                    style={{
                                        background: `linear-gradient(90deg, rgba(108, 92, 231, ${opacity}) 0%, rgba(0, 217, 255, ${opacity * 0.8}) 100%)`,
                                    }}
                                />
                            ))}
                        </div>
                    </div>

                    {/* Live indicator */}
                    <div className="mt-3 flex items-center justify-center gap-2 py-2 rounded-lg bg-white/5">
                        <TrendingUp className="w-4 h-4 text-success" />
                        <span className="text-xs text-secondary">Live Market</span>
                        <div className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
