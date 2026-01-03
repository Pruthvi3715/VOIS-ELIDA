import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import Chatbot from '../Chatbot';

const Layout: React.FC = () => {
    return (
        <div className="min-h-screen bg-background text-white relative overflow-hidden">
            {/* Background effects */}
            <div className="fixed inset-0 pointer-events-none">
                {/* Top-right glow */}
                <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl" />
                {/* Bottom-left glow */}
                <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent/15 rounded-full blur-3xl" />
                {/* Center subtle glow */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-primary-500/5 to-transparent" />
            </div>

            {/* Navigation */}
            <Navbar />
            <Sidebar />
            <Chatbot />

            {/* Main content */}
            <main className="relative z-10 pt-16 md:pl-64 min-h-screen transition-all duration-300">
                <div className="p-6 max-w-7xl mx-auto">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
