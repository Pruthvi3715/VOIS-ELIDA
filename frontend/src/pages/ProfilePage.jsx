import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Save, ArrowLeft, User, Target, Clock, Shield, Heart, Zap, TrendingUp, Activity } from 'lucide-react';
import { motion } from 'framer-motion';
import { API_BASE_URL, getUserId } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data for the chart
const activityData = [
    { name: 'Mon', score: 65 },
    { name: 'Tue', score: 68 },
    { name: 'Wed', score: 75 },
    { name: 'Thu', score: 72 },
    { name: 'Fri', score: 85 },
    { name: 'Sat', score: 82 },
    { name: 'Sun', score: 88 },
];

function ProfilePage() {
    const navigate = useNavigate();
    const [saving, setSaving] = useState(false);
    const [loading, setLoading] = useState(true);
    const [profile, setProfile] = useState({
        user_id: getUserId(),
        risk_tolerance: 'Medium',
        investment_horizon: '3-5 years',
        ethical_filters: [],
        custom_rules: [],
        preferences: {
            sectors: [],
            max_allocation: 10
        }
    });
    const [newRule, setNewRule] = useState('');

    // Load saved profile from backend on mount
    useEffect(() => {
        const loadProfile = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setLoading(false);
                    return;
                }

                const response = await fetch(`${API_BASE_URL}/api/v1/profile/me`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const savedProfile = await response.json();
                    console.log('Loaded profile:', savedProfile);

                    // Map backend fields to frontend state
                    setProfile(prev => ({
                        ...prev,
                        risk_tolerance: mapRiskTolerance(savedProfile.risk_tolerance),
                        investment_horizon: savedProfile.investment_horizon || '3-5 years',
                        ethical_filters: savedProfile.ethical_filters || [],
                        custom_rules: savedProfile.custom_rules || [],
                        preferences: {
                            sectors: savedProfile.sectors || [],
                            max_allocation: 10
                        }
                    }));
                }
            } catch (error) {
                console.error('Error loading profile:', error);
            }
            setLoading(false);
        };

        loadProfile();
    }, []);

    // Map backend risk tolerance to frontend display value
    const mapRiskTolerance = (backendValue) => {
        const map = {
            'conservative': 'Conservative',
            'moderate': 'Medium',
            'medium': 'Medium',
            'aggressive': 'Aggressive'
        };
        return map[backendValue?.toLowerCase()] || 'Medium';
    };

    const riskLevels = [
        { value: 'Conservative', icon: Shield, color: 'text-green-400', desc: 'Preserve capital, minimal volatility' },
        { value: 'Medium', icon: Target, color: 'text-blue-400', desc: 'Balanced growth with moderate risk' },
        { value: 'Aggressive', icon: Heart, color: 'text-red-400', desc: 'Maximum growth, accept high volatility' }
    ];

    const horizons = [
        { value: '0-1 year', icon: Zap, desc: 'Short-term trading' },
        { value: '1-3 years', icon: Activity, desc: 'Medium-term investing' },
        { value: '3-5 years', icon: TrendingUp, desc: 'Long-term wealth building' },
        { value: '5+ years', icon: Clock, desc: 'Retirement planning' }
    ];

    const ethicalFilters = [
        'No Tobacco', 'No Alcohol', 'No Gambling', 'No Weapons', 'ESG Focused', 'Renewable Energy Only'
    ];

    const handleSave = async () => {
        setSaving(true);
        try {
            const token = localStorage.getItem('token');

            // Map frontend fields to backend schema
            const profileData = {
                risk_tolerance: profile.risk_tolerance.toLowerCase(), // "Medium" -> "moderate"
                investment_horizon: profile.investment_horizon,
                ethical_filters: profile.ethical_filters,
                custom_rules: profile.custom_rules,
                sectors: profile.preferences?.sectors || []
            };

            const response = await fetch(`${API_BASE_URL}/api/v1/profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(token && { 'Authorization': `Bearer ${token}` })
                },
                body: JSON.stringify(profileData)
            });

            if (response.ok) {
                // Add a small delay for effect
                setTimeout(() => {
                    alert('✅ Investor DNA saved! Your analysis will now be personalized.');
                    navigate('/');
                }, 500);
            } else {
                const errorData = await response.json().catch(() => ({}));
                alert(`Error: ${errorData.detail || 'Failed to save profile'}`);
            }
        } catch (error) {
            console.error('Save error:', error);
            alert('Error saving profile. Please try again.');
        }
        setSaving(false);
    };

    const addCustomRule = () => {
        if (newRule.trim()) {
            setProfile({
                ...profile,
                custom_rules: [...profile.custom_rules, newRule.trim()]
            });
            setNewRule('');
        }
    };

    const removeRule = (index) => {
        setProfile({
            ...profile,
            custom_rules: profile.custom_rules.filter((_, i) => i !== index)
        });
    };

    const toggleEthicalFilter = (filter) => {
        const current = profile.ethical_filters;
        setProfile({
            ...profile,
            ethical_filters: current.includes(filter)
                ? current.filter(f => f !== filter)
                : [...current, filter]
        });
    };

    const cardVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white p-6 relative overflow-hidden">
            {/* Ambient Background Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600 rounded-full mix-blend-multiply filter blur-[128px] opacity-30 animate-blob"></div>
                <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600 rounded-full mix-blend-multiply filter blur-[128px] opacity-30 animate-blob animation-delay-2000"></div>
                <div className="absolute bottom-[-10%] left-[20%] w-[40%] h-[40%] bg-pink-600 rounded-full mix-blend-multiply filter blur-[128px] opacity-30 animate-blob animation-delay-4000"></div>
            </div>

            <div className="max-w-6xl mx-auto relative z-10">
                {/* Header Section */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col md:flex-row items-start md:items-center justify-between mb-8"
                >
                    <div>
                        <button
                            onClick={() => navigate('/')}
                            className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors mb-4"
                        >
                            <ArrowLeft className="w-5 h-5" />
                            <span>Back to Dashboard</span>
                        </button>
                        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                            Investor DNA Profile
                        </h1>
                        <p className="text-gray-400 mt-2">Customize your AI financial advisor's personality.</p>
                    </div>
                    <div className="mt-4 md:mt-0 flex gap-4">
                        <div className="p-4 bg-gray-800/50 backdrop-blur-md rounded-2xl border border-gray-700/50 flex flex-col items-center">
                            <span className="text-xs text-gray-400 uppercase tracking-wider">DNA Type</span>
                            <span className="font-bold text-blue-400 text-lg">Architect</span>
                        </div>
                        <div className="p-4 bg-gray-800/50 backdrop-blur-md rounded-2xl border border-gray-700/50 flex flex-col items-center">
                            <span className="text-xs text-gray-400 uppercase tracking-wider">Profile Strength</span>
                            <span className="font-bold text-green-400 text-lg">85%</span>
                        </div>
                    </div>
                </motion.div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                    {/* Left Column: Settings */}
                    <div className="lg:col-span-2 space-y-8">

                        {/* Risk Tolerance */}
                        <motion.section
                            variants={cardVariants}
                            initial="hidden"
                            animate="visible"
                            className="bg-gray-800/30 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-6 shadow-xl"
                        >
                            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                                <Shield className="w-5 h-5 text-purple-400" />
                                Risk Tolerance
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {riskLevels.map(({ value, icon: Icon, color, desc }) => (
                                    <button
                                        key={value}
                                        onClick={() => setProfile({ ...profile, risk_tolerance: value })}
                                        className={`relative group p-4 rounded-2xl border transition-all duration-300 text-left h-full ${profile.risk_tolerance === value
                                            ? 'bg-blue-600/20 border-blue-500 shadow-[0_0_20px_rgba(37,99,235,0.2)]'
                                            : 'bg-gray-800/50 border-gray-700 hover:border-gray-600 hover:bg-gray-800'
                                            }`}
                                    >
                                        <div className={`p-3 rounded-xl bg-gray-900/50 w-fit mb-3 ${profile.risk_tolerance === value ? 'text-blue-400' : 'text-gray-400'}`}>
                                            <Icon className="w-6 h-6" />
                                        </div>
                                        <div className="font-bold text-lg mb-1">{value}</div>
                                        <div className="text-xs text-gray-400 group-hover:text-gray-300 transition-colors">{desc}</div>
                                        {profile.risk_tolerance === value && (
                                            <motion.div layoutId="risk-active" className="absolute inset-0 border-2 border-blue-500 rounded-2xl" />
                                        )}
                                    </button>
                                ))}
                            </div>
                        </motion.section>

                        {/* Investment Horizon */}
                        <motion.section
                            variants={cardVariants}
                            initial="hidden"
                            animate="visible"
                            transition={{ delay: 0.1 }}
                            className="bg-gray-800/30 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-6 shadow-xl"
                        >
                            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                                <Clock className="w-5 h-5 text-purple-400" />
                                Investment Horizon
                            </h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                                {horizons.map(({ value, icon: Icon, desc }) => (
                                    <button
                                        key={value}
                                        onClick={() => setProfile({ ...profile, investment_horizon: value })}
                                        className={`p-4 rounded-xl border transition-all text-center flex flex-col items-center gap-3 ${profile.investment_horizon === value
                                            ? 'bg-purple-600/20 border-purple-500 text-white'
                                            : 'bg-gray-800/50 border-gray-700 text-gray-400 hover:bg-gray-800'
                                            }`}
                                    >
                                        <Icon className={`w-6 h-6 ${profile.investment_horizon === value ? 'text-purple-400' : ''}`} />
                                        <span className="font-medium text-sm">{value}</span>
                                    </button>
                                ))}
                            </div>
                        </motion.section>

                        {/* Ethical Filters */}
                        <motion.section
                            variants={cardVariants}
                            initial="hidden"
                            animate="visible"
                            transition={{ delay: 0.2 }}
                            className="bg-gray-800/30 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-6 shadow-xl"
                        >
                            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                                <Heart className="w-5 h-5 text-pink-400" />
                                Ethical Priorities
                            </h2>
                            <div className="flex flex-wrap gap-3">
                                {ethicalFilters.map(filter => (
                                    <button
                                        key={filter}
                                        onClick={() => toggleEthicalFilter(filter)}
                                        className={`px-4 py-2 rounded-full border text-sm font-medium transition-all ${profile.ethical_filters.includes(filter)
                                            ? 'bg-pink-500/20 border-pink-500 text-pink-300 shadow-[0_0_10px_rgba(236,72,153,0.2)]'
                                            : 'bg-gray-800/50 border-gray-700 text-gray-400 hover:border-gray-600'
                                            }`}
                                    >
                                        {filter}
                                    </button>
                                ))}
                            </div>
                        </motion.section>

                        {/* Custom Rules */}
                        <motion.section
                            variants={cardVariants}
                            initial="hidden"
                            animate="visible"
                            transition={{ delay: 0.3 }}
                            className="bg-gray-800/30 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-6 shadow-xl"
                        >
                            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                                <User className="w-5 h-5 text-blue-400" />
                                Custom Constraints
                            </h2>
                            <div className="flex gap-2 mb-4">
                                <input
                                    type="text"
                                    value={newRule}
                                    onChange={(e) => setNewRule(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && addCustomRule()}
                                    placeholder="e.g., 'Avoid airline stocks' or 'Prefer dividend payers'"
                                    className="flex-1 px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-white placeholder-gray-500"
                                />
                                <button
                                    onClick={addCustomRule}
                                    className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-medium hover:opacity-90 transition-opacity"
                                >
                                    Add
                                </button>
                            </div>
                            <div className="space-y-2">
                                {profile.custom_rules.map((rule, index) => (
                                    <motion.div
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        key={index}
                                        className="flex items-center justify-between p-3 bg-gray-900/50 border border-gray-700 rounded-xl"
                                    >
                                        <span className="text-gray-300">{rule}</span>
                                        <button
                                            onClick={() => removeRule(index)}
                                            className="text-red-400 hover:text-red-300 text-sm transition-colors"
                                        >
                                            Remove
                                        </button>
                                    </motion.div>
                                ))}
                                {profile.custom_rules.length === 0 && (
                                    <div className="text-gray-500 text-sm italic text-center py-4">
                                        No custom rules added yet.
                                    </div>
                                )}
                            </div>
                        </motion.section>
                    </div>

                    {/* Right Column: Analytics & Save */}
                    <div className="space-y-8">
                        {/* Profile Impact Chart */}
                        <motion.div
                            variants={cardVariants}
                            initial="hidden"
                            animate="visible"
                            transition={{ delay: 0.4 }}
                            className="bg-gray-800/30 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-6 shadow-xl"
                        >
                            <h3 className="text-lg font-semibold mb-4 text-gray-200">Alignment Score Impact</h3>
                            <div className="h-48 w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={activityData}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                        <XAxis dataKey="name" stroke="#9CA3AF" fontSize={10} tickLine={false} axisLine={false} />
                                        <YAxis stroke="#9CA3AF" fontSize={10} tickLine={false} axisLine={false} />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', color: '#fff' }}
                                            itemStyle={{ color: '#60A5FA' }}
                                        />
                                        <Line type="monotone" dataKey="score" stroke="#8B5CF6" strokeWidth={3} dot={{ r: 4, fill: '#8B5CF6' }} activeDot={{ r: 6 }} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                            <p className="text-xs text-gray-400 mt-2 text-center">Projected alignment based on current settings.</p>
                        </motion.div>

                        {/* Save Action */}
                        <motion.div
                            variants={cardVariants}
                            initial="hidden"
                            animate="visible"
                            transition={{ delay: 0.5 }}
                            className="sticky top-6"
                        >
                            <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl -mr-8 -mt-8"></div>
                                <h3 className="text-xl font-bold mb-2">Ready to Upgrade?</h3>
                                <p className="text-gray-400 text-sm mb-6">
                                    Your new "Investor DNA" will immediately recalibrate all 5 active AI agents.
                                </p>
                                <button
                                    onClick={handleSave}
                                    disabled={saving}
                                    className={`w-full py-4 rounded-xl font-bold text-lg shadow-lg flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-[0.98] ${saving
                                        ? 'bg-gray-700 cursor-not-allowed'
                                        : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white shadow-blue-500/25'
                                        }`}
                                >
                                    {saving ? (
                                        <>
                                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                            <span>Syncing...</span>
                                        </>
                                    ) : (
                                        <>
                                            <Save className="w-5 h-5" />
                                            <span>Save & Activate</span>
                                        </>
                                    )}
                                </button>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProfilePage;
