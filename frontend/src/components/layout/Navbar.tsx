import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { LogOut, User, Brain } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    const { user, logout } = useAuth();

    return (
        <nav className="h-16 border-b border-glass-border bg-surface/80 backdrop-blur-xl fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group">
                <div className="relative">
                    <div className="absolute inset-0 bg-gradient-primary blur-lg opacity-50 group-hover:opacity-75 transition-opacity" />
                    <div className="relative w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center shadow-glow">
                        <Brain className="w-5 h-5 text-white" />
                    </div>
                </div>
                <div>
                    <span className="text-xl font-bold text-gradient">ELIDA</span>
                    <span className="hidden md:inline text-xs text-secondary ml-2">AI Investment Advisor</span>
                </div>
            </Link>

            {/* Right side */}
            <div className="flex items-center gap-4">
                {user ? (
                    <>
                        <Link
                            to="/profile"
                            className="flex items-center gap-2 px-3 py-2 rounded-xl bg-surface-light/50 border border-glass-border hover:border-primary-500/50 transition-colors"
                        >
                            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
                                <User className="w-4 h-4 text-white" />
                            </div>
                            <span className="text-sm text-white font-medium hidden md:inline">
                                {user.username}
                            </span>
                        </Link>
                        <button
                            onClick={logout}
                            className="p-2.5 rounded-xl bg-surface-light/50 border border-glass-border hover:border-error/50 hover:bg-error/10 text-secondary hover:text-error transition-all"
                            title="Logout"
                        >
                            <LogOut className="w-4 h-4" />
                        </button>
                    </>
                ) : (
                    <Link to="/login" className="btn-primary text-sm">
                        Login
                    </Link>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
