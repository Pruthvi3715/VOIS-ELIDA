import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { LogOut, User, Cpu } from 'lucide-react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
    const { user, logout } = useAuth();

    return (
        <nav className="h-16 fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6">
            {/* Background */}
            <div className="absolute inset-0 bg-background/80 backdrop-blur-xl border-b border-white/5" />

            {/* Logo */}
            <Link to="/" className="relative flex items-center gap-3 group">
                <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center transition-transform group-hover:scale-105"
                    style={{
                        background: 'linear-gradient(135deg, #6c5ce7 0%, #a855f7 100%)',
                        boxShadow: '0 4px 20px rgba(108, 92, 231, 0.4)',
                    }}
                >
                    <Cpu className="w-5 h-5 text-white" />
                </div>
                <div className="flex flex-col">
                    <span className="text-lg font-bold text-gradient">ELIDA</span>
                    <span className="text-[10px] text-secondary uppercase tracking-wider hidden sm:block">
                        AI Investment Advisor
                    </span>
                </div>
            </Link>

            {/* Right side */}
            <div className="relative flex items-center gap-3">
                {user ? (
                    <>
                        <Link
                            to="/profile"
                            className="flex items-center gap-3 px-4 py-2 rounded-xl bg-white/5 border border-white/5 hover:border-primary/30 transition-all"
                        >
                            <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                                <User className="w-4 h-4 text-primary-300" />
                            </div>
                            <span className="text-sm font-medium text-white hidden sm:block">
                                {user.username}
                            </span>
                            <div className="w-2 h-2 rounded-full bg-success hidden sm:block" />
                        </Link>

                        <button
                            onClick={logout}
                            className="p-2.5 rounded-xl bg-white/5 border border-white/5 hover:bg-error/10 hover:border-error/30 transition-all"
                            title="Sign out"
                        >
                            <LogOut className="w-4 h-4 text-secondary hover:text-error" />
                        </button>
                    </>
                ) : (
                    <Link to="/login" className="btn-primary text-sm px-5 py-2.5">
                        Sign In
                    </Link>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
