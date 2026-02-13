import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import Chatbot from '../Chatbot';

const Layout: React.FC = () => {
    return (
        <div className="min-h-screen bg-background text-white">
            {/* Animated background */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                {/* Gradient orbs */}
                <div
                    className="absolute -top-40 -right-40 w-96 h-96 rounded-full animate-pulse-glow"
                    style={{
                        background: 'radial-gradient(circle, rgba(108, 92, 231, 0.3) 0%, transparent 70%)',
                        filter: 'blur(60px)',
                    }}
                />
                <div
                    className="absolute top-1/2 -left-40 w-80 h-80 rounded-full animate-pulse-glow"
                    style={{
                        background: 'radial-gradient(circle, rgba(0, 217, 255, 0.2) 0%, transparent 70%)',
                        filter: 'blur(60px)',
                        animationDelay: '1s',
                    }}
                />
                <div
                    className="absolute -bottom-20 right-1/3 w-72 h-72 rounded-full animate-pulse-glow"
                    style={{
                        background: 'radial-gradient(circle, rgba(0, 245, 160, 0.15) 0%, transparent 70%)',
                        filter: 'blur(60px)',
                        animationDelay: '2s',
                    }}
                />

                {/* Grid pattern */}
                <div
                    className="absolute inset-0 opacity-[0.03]"
                    style={{
                        backgroundImage: `
                            linear-gradient(rgba(108, 92, 231, 0.5) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(108, 92, 231, 0.5) 1px, transparent 1px)
                        `,
                        backgroundSize: '50px 50px',
                    }}
                />
            </div>

            {/* Navigation */}
            <Navbar />
            <Sidebar />
            <Chatbot />

            {/* Main content */}
            <main className="relative z-10 pt-20 md:pl-64 min-h-screen">
                <div className="p-6 lg:p-8 max-w-7xl mx-auto">
                    <div className="page-enter">
                        <Outlet />
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Layout;
