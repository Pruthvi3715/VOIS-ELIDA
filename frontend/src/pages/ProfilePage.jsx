import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Save, ArrowLeft, User, Target, Clock, Shield, Heart } from 'lucide-react';
import { API_BASE_URL, getUserId } from '../api';

function ProfilePage() {
    const navigate = useNavigate();
    const [saving, setSaving] = useState(false);
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

    const riskLevels = [
        { value: 'Conservative', icon: Shield, desc: 'Preserve capital, minimal volatility' },
        { value: 'Medium', icon: Target, desc: 'Balanced growth with moderate risk' },
        { value: 'Aggressive', icon: Heart, desc: 'Maximum growth, accept high volatility' }
    ];

    const horizons = [
        { value: '0-1 year', icon: Clock, desc: 'Short-term trading' },
        { value: '1-3 years', icon: Clock, desc: 'Medium-term investing' },
        { value: '3-5 years', icon: Clock, desc: 'Long-term wealth building' },
        { value: '5+ years', icon: Clock, desc: 'Retirement planning' }
    ];

    const ethicalFilters = [
        'No Tobacco',
        'No Alcohol',
        'No Gambling',
        'No Weapons',
        'ESG Focused',
        'Renewable Energy Only'
    ];

    const handleSave = async () => {
        setSaving(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/profile`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profile)
            });

            if (response.ok) {
                alert('✅ Investor DNA saved! Your analysis will now be personalized.');
                navigate('/');
            }
        } catch (error) {
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

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <button
                        onClick={() => navigate('/')}
                        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-2"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        Back to Dashboard
                    </button>
                    <h1 className="text-3xl font-bold text-gray-900">Investor DNA Profile</h1>
                    <p className="text-gray-500">Personalize your investment analysis</p>
                </div>
                <User className="w-12 h-12 text-gray-300" />
            </div>

            {/* Risk Tolerance */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Tolerance</h2>
                <div className="grid grid-cols-3 gap-4">
                    {riskLevels.map(({ value, icon: Icon, desc }) => (
                        <button
                            key={value}
                            onClick={() => setProfile({ ...profile, risk_tolerance: value })}
                            className={`p-4 border-2 rounded-lg text-left transition ${profile.risk_tolerance === value
                                    ? 'border-gray-900 bg-gray-50'
                                    : 'border-gray-200 hover:border-gray-300'
                                }`}
                        >
                            <Icon className={`w-6 h-6 mb-2 ${profile.risk_tolerance === value ? 'text-gray-900' : 'text-gray-400'
                                }`} />
                            <div className="font-semibold text-gray-900">{value}</div>
                            <div className="text-sm text-gray-500">{desc}</div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Investment Horizon */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Investment Horizon</h2>
                <div className="grid grid-cols-2 gap-4">
                    {horizons.map(({ value, icon: Icon, desc }) => (
                        <button
                            key={value}
                            onClick={() => setProfile({ ...profile, investment_horizon: value })}
                            className={`p-4 border-2 rounded-lg text-left transition ${profile.investment_horizon === value
                                    ? 'border-gray-900 bg-gray-50'
                                    : 'border-gray-200 hover:border-gray-300'
                                }`}
                        >
                            <Icon className={`w-5 h-5 mb-2 ${profile.investment_horizon === value ? 'text-gray-900' : 'text-gray-400'
                                }`} />
                            <div className="font-semibold text-gray-900">{value}</div>
                            <div className="text-sm text-gray-500">{desc}</div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Ethical Filters */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Ethical Filters (Optional)</h2>
                <div className="flex flex-wrap gap-2">
                    {ethicalFilters.map(filter => (
                        <button
                            key={filter}
                            onClick={() => toggleEthicalFilter(filter)}
                            className={`px-4 py-2 rounded-lg border-2 text-sm font-medium transition ${profile.ethical_filters.includes(filter)
                                    ? 'border-gray-900 bg-gray-900 text-white'
                                    : 'border-gray-200 text-gray-600 hover:border-gray-300'
                                }`}
                        >
                            {filter}
                        </button>
                    ))}
                </div>
            </div>

            {/* Custom Rules */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Custom Rules</h2>
                <p className="text-gray-500 text-sm mb-4">
                    Add specific constraints like "Avoid airline stocks" or "Only tech companies"
                </p>

                <div className="flex gap-2 mb-4">
                    <input
                        type="text"
                        value={newRule}
                        onChange={(e) => setNewRule(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && addCustomRule()}
                        placeholder="e.g., Avoid airline stocks"
                        className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-200"
                    />
                    <button
                        onClick={addCustomRule}
                        className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition"
                    >
                        Add Rule
                    </button>
                </div>

                {profile.custom_rules.length > 0 && (
                    <div className="space-y-2">
                        {profile.custom_rules.map((rule, index) => (
                            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="text-gray-900">{rule}</span>
                                <button
                                    onClick={() => removeRule(index)}
                                    className="text-red-600 hover:text-red-700 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
                <button
                    onClick={handleSave}
                    disabled={saving}
                    className="flex items-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition disabled:opacity-50"
                >
                    <Save className="w-4 h-4" />
                    {saving ? 'Saving...' : 'Save Investor DNA'}
                </button>
            </div>
        </div>
    );
}

export default ProfilePage;
