import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Lock, Mail, Loader2, AlertCircle, User, Cpu, ArrowRight, Check } from 'lucide-react';
import { motion } from 'framer-motion';

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
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
            const response = await axios.post('http://localhost:8001/api/auth/register', {
                username,
                email,
                password
            });

            const { access_token, user_id } = response.data;
            login(access_token, { id: user_id, email, username });
            navigate('/');

        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const features = [
        'AI-powered stock analysis',
        'Personalized Investor DNA',
        'Real-time market insights',
    ];

    const inputStyle = {
        background: '#222228',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '14px 16px 14px 48px',
        outline: 'none',
        fontSize: '16px',
    };

    return (
        <div
            className="min-h-screen flex items-center justify-center relative overflow-hidden"
            style={{ background: '#0f0f12' }}
        >
            {/* Animated background */}
            <div className="absolute inset-0 pointer-events-none">
                <div
                    className="absolute bottom-1/4 left-1/4 w-96 h-96 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(0, 217, 255, 0.25) 0%, transparent 70%)',
                        filter: 'blur(60px)',
                        animation: 'pulse 3s ease-in-out infinite',
                    }}
                />
                <div
                    className="absolute top-1/4 right-1/4 w-80 h-80 rounded-full"
                    style={{
                        background: 'radial-gradient(circle, rgba(0, 245, 160, 0.2) 0%, transparent 70%)',
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
                                background: 'linear-gradient(135deg, #00d9ff 0%, #00f5a0 100%)',
                                boxShadow: '0 0 40px rgba(0, 217, 255, 0.5)',
                            }}
                        >
                            <Cpu className="w-8 h-8" style={{ color: '#0f0f12' }} />
                        </div>
                    </motion.div>

                    <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
                    <p style={{ color: '#9ca3af' }}>Join ELIDA to start investing smarter</p>
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

                    <form onSubmit={handleSubmit} className="space-y-4">
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
                                    placeholder="Choose a username"
                                    style={inputStyle}
                                    onFocus={(e) => {
                                        e.target.style.borderColor = 'rgba(0, 217, 255, 0.5)';
                                        e.target.style.boxShadow = '0 0 0 3px rgba(0, 217, 255, 0.2)';
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
                                Email
                            </label>
                            <div className="relative">
                                <Mail
                                    className="absolute left-4 top-1/2 w-5 h-5"
                                    style={{ transform: 'translateY(-50%)', color: '#9ca3af' }}
                                />
                                <input
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full rounded-xl text-white"
                                    placeholder="Enter your email"
                                    style={inputStyle}
                                    onFocus={(e) => {
                                        e.target.style.borderColor = 'rgba(0, 217, 255, 0.5)';
                                        e.target.style.boxShadow = '0 0 0 3px rgba(0, 217, 255, 0.2)';
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
                                    placeholder="Create a password"
                                    style={inputStyle}
                                    onFocus={(e) => {
                                        e.target.style.borderColor = 'rgba(0, 217, 255, 0.5)';
                                        e.target.style.boxShadow = '0 0 0 3px rgba(0, 217, 255, 0.2)';
                                    }}
                                    onBlur={(e) => {
                                        e.target.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                                        e.target.style.boxShadow = 'none';
                                    }}
                                />
                            </div>
                        </div>

                        {/* Features */}
                        <div className="py-3 space-y-2">
                            {features.map((feature, i) => (
                                <motion.div
                                    key={feature}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.3 + i * 0.1 }}
                                    className="flex items-center gap-2 text-sm"
                                    style={{ color: '#9ca3af' }}
                                >
                                    <Check className="w-4 h-4" style={{ color: '#00f5a0' }} />
                                    {feature}
                                </motion.div>
                            ))}
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex items-center justify-center gap-2 font-semibold rounded-xl"
                            style={{
                                background: 'linear-gradient(135deg, #00d9ff 0%, #00f5a0 100%)',
                                color: '#0f0f12',
                                padding: '14px 24px',
                                boxShadow: '0 4px 20px rgba(0, 217, 255, 0.4)',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                opacity: loading ? 0.5 : 1,
                                transition: 'all 0.3s ease',
                            }}
                        >
                            {loading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    Create Account
                                    <ArrowRight className="w-5 h-5" />
                                </>
                            )}
                        </button>
                    </form>
                </div>

                {/* Login link */}
                <p className="mt-6 text-center text-sm" style={{ color: '#9ca3af' }}>
                    Already have an account?{' '}
                    <Link
                        to="/login"
                        className="font-medium hover:underline"
                        style={{ color: '#c4b5fd' }}
                    >
                        Sign in
                    </Link>
                </p>
            </motion.div>
        </div>
    );
};

export default Register;
