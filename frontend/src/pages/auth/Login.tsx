import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Lock, User, Loader2, AlertCircle, Cpu, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const Login: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/api/auth/login', {
                username: username,
                password: password
            });

            const { access_token, user_id } = response.data;
            login(access_token, { id: user_id, email: '', username: username });
            navigate('/');
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    const handleDemoLogin = async () => {
        setUsername('demo');
        setPassword('demo123');
        setError('');
        setLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/api/auth/login', {
                username: 'demo',
                password: 'demo123'
            });

            const { access_token, user_id } = response.data;
            login(access_token, { id: user_id, email: '', username: 'demo' });
            navigate('/');
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || 'Demo login failed. Please try manual login.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            className="min-h-screen flex items-center justify-center relative overflow-hidden"
            style={{ background: '#0f0f12' }}
        >
            {/* Animated background */}
            <div className="absolute inset-0 pointer-events-none">
                <div
                    className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(108, 92, 231, 0.25) 0%, transparent 70%)',
                        filter: 'blur(60px)',
                        animation: 'pulse 3s ease-in-out infinite',
                    }}
                />
                <div
                    className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(0, 217, 255, 0.2) 0%, transparent 70%)',
                        filter: 'blur(60px)',
                        animation: 'pulse 3s ease-in-out infinite 1s',
                    }}
                />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="relative z-10 w-full max-w-md mx-4"
            >
                {/* Logo */}
                <div className="text-center mb-8">
                    <motion.div
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.1 }}
                        className="inline-flex items-center justify-center mb-6"
                    >
                        <div
                            className="w-16 h-16 rounded-2xl flex items-center justify-center"
                            style={{
                                background: 'linear-gradient(135deg, #6c5ce7 0%, #a855f7 100%)',
                                boxShadow: '0 0 40px rgba(108, 92, 231, 0.5)',
                            }}
                        >
                            <Cpu className="w-8 h-8 text-white" />
                        </div>
                    </motion.div>

                    <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
                    <p style={{ color: '#9ca3af' }}>Sign in to access your dashboard</p>
                </div>

                {/* Form Card */}
                <div
                    className="rounded-2xl p-8"
                    style={{
                        background: '#18181c',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        boxShadow: '0 4px 24px rgba(0, 0, 0, 0.4)'
                    }}
                >
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="mb-6 p-4 rounded-xl flex items-center gap-3"
                            style={{
                                background: 'rgba(255, 71, 87, 0.1)',
                                border: '1px solid rgba(255, 71, 87, 0.2)'
                            }}
                        >
                            <AlertCircle className="w-5 h-5 flex-shrink-0" style={{ color: '#ff4757' }} />
                            <span className="text-sm" style={{ color: '#ff4757' }}>{error}</span>
                        </motion.div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div className="space-y-2">
                            <label
                                className="text-sm font-medium block ml-1"
                                style={{ color: '#9ca3af' }}
                            >
                                Username
                            </label>
                            <div className="relative">
                                <User
                                    className="absolute left-4 top-1/2 w-5 h-5"
                                    style={{ transform: 'translateY(-50%)', color: '#9ca3af' }}
                                />
                                <input
                                    type="text"
                                    required
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full rounded-xl text-white"
                                    placeholder="Enter your username"
                                    style={{
                                        background: '#222228',
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        padding: '14px 16px 14px 48px',
                                        outline: 'none',
                                        fontSize: '16px',
                                    }}
                                    onFocus={(e) => {
                                        e.target.style.borderColor = 'rgba(108, 92, 231, 0.5)';
                                        e.target.style.boxShadow = '0 0 0 3px rgba(108, 92, 231, 0.2)';
                                    }}
                                    onBlur={(e) => {
                                        e.target.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                                        e.target.style.boxShadow = 'none';
                                    }}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label
                                className="text-sm font-medium block ml-1"
                                style={{ color: '#9ca3af' }}
                            >
                                Password
                            </label>
                            <div className="relative">
                                <Lock
                                    className="absolute left-4 top-1/2 w-5 h-5"
                                    style={{ transform: 'translateY(-50%)', color: '#9ca3af' }}
                                />
                                <input
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full rounded-xl text-white"
                                    placeholder="Enter your password"
                                    style={{
                                        background: '#222228',
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        padding: '14px 16px 14px 48px',
                                        outline: 'none',
                                        fontSize: '16px',
                                    }}
                                    onFocus={(e) => {
                                        e.target.style.borderColor = 'rgba(108, 92, 231, 0.5)';
                                        e.target.style.boxShadow = '0 0 0 3px rgba(108, 92, 231, 0.2)';
                                    }}
                                    onBlur={(e) => {
                                        e.target.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                                        e.target.style.boxShadow = 'none';
                                    }}
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex items-center justify-center gap-2 font-semibold rounded-xl text-white"
                            style={{
                                background: 'linear-gradient(135deg, #6c5ce7 0%, #a855f7 100%)',
                                padding: '14px 24px',
                                boxShadow: '0 4px 20px rgba(108, 92, 231, 0.4)',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                opacity: loading ? 0.5 : 1,
                                transition: 'all 0.3s ease',
                            }}
                        >
                            {loading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    Sign In
                                    <ArrowRight className="w-5 h-5" />
                                </>
                            )}
                        </button>

                        {/* Demo Login Button */}
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t" style={{ borderColor: 'rgba(255, 255, 255, 0.1)' }}></div>
                            </div>
                            <div className="relative flex justify-center text-xs">
                                <span style={{ background: '#18181c', padding: '0 12px', color: '#6b7280' }}>
                                    OR
                                </span>
                            </div>
                        </div>

                        <button
                            type="button"
                            onClick={handleDemoLogin}
                            disabled={loading}
                            className="w-full flex items-center justify-center gap-2 font-medium rounded-xl transition-all"
                            style={{
                                background: 'rgba(108, 92, 231, 0.1)',
                                border: '1px solid rgba(108, 92, 231, 0.3)',
                                padding: '14px 24px',
                                color: '#c4b5fd',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                opacity: loading ? 0.5 : 1,
                            }}
                            onMouseEnter={(e) => {
                                if (!loading) {
                                    e.currentTarget.style.background = 'rgba(108, 92, 231, 0.2)';
                                    e.currentTarget.style.borderColor = 'rgba(108, 92, 231, 0.5)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.background = 'rgba(108, 92, 231, 0.1)';
                                e.currentTarget.style.borderColor = 'rgba(108, 92, 231, 0.3)';
                            }}
                        >
                            <Cpu className="w-5 h-5" />
                            Try Demo Account
                        </button>
                    </form>
                </div>

                {/* Register link */}
                <p className="mt-6 text-center text-sm" style={{ color: '#9ca3af' }}>
                    Don't have an account?{' '}
                    <Link
                        to="/register"
                        className="font-medium hover:underline"
                        style={{ color: '#c4b5fd' }}
                    >
                        Create one
                    </Link>
                </p>

                {/* Demo hint */}
                <p className="mt-4 text-center text-xs" style={{ color: '#6b7280' }}>
                    Try demo: <span style={{ color: '#9ca3af' }}>demo / demo123</span>
                </p>
            </motion.div>
        </div>
    );
};

export default Login;
