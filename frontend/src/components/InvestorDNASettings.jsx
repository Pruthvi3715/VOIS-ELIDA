import { useState, useEffect } from 'react';
import { Settings, Save, User, Shield, TrendingUp, Leaf, X } from 'lucide-react';
import { getProfile, updateProfile } from '../api';

/**
 * Investor DNA Settings Modal
 * Allows users to configure their investment preferences
 */
function InvestorDNASettings({ isOpen, onClose, onSave }) {
    const [profile, setProfile] = useState({
        risk_tolerance: 'moderate',
        investment_style: 'blend',
        holding_period: 'long',
        exclude_tobacco: false,
        exclude_alcohol: false,
        exclude_gambling: false,
        exclude_weapons: false,
        exclude_fossil_fuels: false,
        max_pe_ratio: 50,
        min_dividend_yield: 0,
        prefer_profitable: true,
        avoid_52w_highs: false,
        prefer_oversold: false,
    });
    const [loading, setLoading] = useState(false);
    const [saved, setSaved] = useState(false);

    useEffect(() => {
        if (isOpen) {
            loadProfile();
        }
    }, [isOpen]);

    const loadProfile = async () => {
        try {
            const data = await getProfile();
            if (data.profile) {
                setProfile(prev => ({ ...prev, ...data.profile }));
            }
        } catch (e) {
            console.error('Failed to load profile:', e);
        }
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            await updateProfile(profile);
            setSaved(true);
            setTimeout(() => setSaved(false), 2000);
            if (onSave) onSave(profile);
        } catch (e) {
            console.error('Failed to save profile:', e);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                {/* Header */}
                <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="bg-blue-100 p-2 rounded-lg">
                            <User className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                            <h2 className="font-bold text-lg text-gray-800">Investor DNA</h2>
                            <p className="text-sm text-gray-500">Personalize your investment preferences</p>
                        </div>
                    </div>
                    <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                        <X className="w-5 h-5 text-gray-500" />
                    </button>
                </div>

                <div className="p-6 space-y-8">
                    {/* Risk Profile */}
                    <Section icon={<Shield className="w-5 h-5 text-purple-600" />} title="Risk Profile">
                        <div className="grid grid-cols-3 gap-3">
                            {['conservative', 'moderate', 'aggressive'].map(level => (
                                <button
                                    key={level}
                                    onClick={() => setProfile(p => ({ ...p, risk_tolerance: level }))}
                                    className={`p-3 rounded-xl border-2 transition-all capitalize ${profile.risk_tolerance === level
                                        ? 'border-purple-500 bg-purple-50 text-purple-700'
                                        : 'border-gray-200 hover:border-gray-300'
                                        }`}
                                >
                                    {level}
                                </button>
                            ))}
                        </div>
                    </Section>

                    {/* Investment Style */}
                    <Section icon={<TrendingUp className="w-5 h-5 text-blue-600" />} title="Investment Style">
                        <div className="grid grid-cols-5 gap-2">
                            {['value', 'growth', 'dividend', 'index', 'blend'].map(style => (
                                <button
                                    key={style}
                                    onClick={() => setProfile(p => ({ ...p, investment_style: style }))}
                                    className={`p-2 rounded-lg border-2 transition-all capitalize text-sm ${profile.investment_style === style
                                        ? 'border-blue-500 bg-blue-50 text-blue-700'
                                        : 'border-gray-200 hover:border-gray-300'
                                        }`}
                                >
                                    {style}
                                </button>
                            ))}
                        </div>

                        <div className="mt-4">
                            <label className="text-sm text-gray-600 mb-2 block">Holding Period</label>
                            <div className="grid grid-cols-3 gap-3">
                                {[
                                    { value: 'short', label: 'Short (<1 yr)' },
                                    { value: 'medium', label: 'Medium (1-5 yr)' },
                                    { value: 'long', label: 'Long (5+ yr)' },
                                ].map(({ value, label }) => (
                                    <button
                                        key={value}
                                        onClick={() => setProfile(p => ({ ...p, holding_period: value }))}
                                        className={`p-2 rounded-lg border-2 transition-all text-sm ${profile.holding_period === value
                                            ? 'border-blue-500 bg-blue-50 text-blue-700'
                                            : 'border-gray-200 hover:border-gray-300'
                                            }`}
                                    >
                                        {label}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </Section>

                    {/* Ethical Filters */}
                    <Section icon={<Leaf className="w-5 h-5 text-green-600" />} title="Ethical Exclusions">
                        <div className="grid grid-cols-2 gap-3">
                            {[
                                { key: 'exclude_tobacco', label: 'No Tobacco' },
                                { key: 'exclude_alcohol', label: 'No Alcohol' },
                                { key: 'exclude_gambling', label: 'No Gambling' },
                                { key: 'exclude_weapons', label: 'No Weapons' },
                                { key: 'exclude_fossil_fuels', label: 'No Fossil Fuels' },
                            ].map(({ key, label }) => (
                                <label key={key} className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={profile[key]}
                                        onChange={e => setProfile(p => ({ ...p, [key]: e.target.checked }))}
                                        className="w-4 h-4 text-green-600 rounded"
                                    />
                                    <span className="text-sm text-gray-700">{label}</span>
                                </label>
                            ))}
                        </div>
                    </Section>

                    {/* Custom Rules */}
                    <Section icon={<div className="bg-orange-100 p-1 rounded"><Settings className="w-4 h-4 text-orange-600" /></div>} title="Custom Rules">
                        <div className="space-y-3">
                            <p className="text-sm text-gray-500">Add specific rules for agents to follow (e.g., "Avoid companies with recent scandals").</p>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    placeholder="Enter a rule..."
                                    className="flex-1 p-2 border border-gray-200 rounded-lg text-sm"
                                    id="new-rule-input"
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            const val = e.target.value.trim();
                                            if (val) {
                                                setProfile(p => ({ ...p, custom_rules: [...(p.custom_rules || []), val] }));
                                                e.target.value = '';
                                            }
                                        }
                                    }}
                                />
                                <button
                                    onClick={() => {
                                        const input = document.getElementById('new-rule-input');
                                        const val = input.value.trim();
                                        if (val) {
                                            setProfile(p => ({ ...p, custom_rules: [...(p.custom_rules || []), val] }));
                                            input.value = '';
                                        }
                                    }}
                                    className="px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors"
                                >
                                    Add
                                </button>
                            </div>

                            <div className="space-y-2">
                                {(profile.custom_rules || []).map((rule, idx) => (
                                    <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg border border-gray-100">
                                        <span className="text-sm text-gray-700">{rule}</span>
                                        <button
                                            onClick={() => setProfile(p => ({ ...p, custom_rules: p.custom_rules.filter((_, i) => i !== idx) }))}
                                            className="p-1 hover:bg-red-50 text-gray-400 hover:text-red-500 rounded transition-colors"
                                        >
                                            <X className="w-4 h-4" />
                                        </button>
                                    </div>
                                ))}
                                {(!profile.custom_rules || profile.custom_rules.length === 0) && (
                                    <p className="text-xs text-center text-gray-400 py-2">No custom rules added yet.</p>
                                )}
                            </div>
                        </div>
                    </Section>

                    {/* Valuation Preferences */}
                    <Section icon={<Settings className="w-5 h-5 text-gray-600" />} title="Preferences">
                        <div className="space-y-4">
                            <div>
                                <label className="text-sm text-gray-600 mb-1 block">
                                    Max P/E Ratio: <span className="font-medium">{profile.max_pe_ratio}</span>
                                </label>
                                <input
                                    type="range"
                                    min="10"
                                    max="100"
                                    value={profile.max_pe_ratio}
                                    onChange={e => setProfile(p => ({ ...p, max_pe_ratio: parseInt(e.target.value) }))}
                                    className="w-full"
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <label className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={profile.prefer_profitable}
                                        onChange={e => setProfile(p => ({ ...p, prefer_profitable: e.target.checked }))}
                                        className="w-4 h-4 text-blue-600 rounded"
                                    />
                                    <span className="text-sm text-gray-700">Prefer Profitable Companies</span>
                                </label>

                                <label className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={profile.prefer_oversold}
                                        onChange={e => setProfile(p => ({ ...p, prefer_oversold: e.target.checked }))}
                                        className="w-4 h-4 text-blue-600 rounded"
                                    />
                                    <span className="text-sm text-gray-700">Prefer Oversold (RSI &lt; 30)</span>
                                </label>
                            </div>
                        </div>
                    </Section>
                </div>

                {/* Footer */}
                <div className="sticky bottom-0 bg-white border-t border-gray-100 px-6 py-4 flex justify-end gap-3">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleSave}
                        disabled={loading}
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:opacity-50"
                    >
                        {loading ? 'Saving...' : saved ? (
                            <>
                                <Save className="w-4 h-4" />
                                Saved!
                            </>
                        ) : (
                            <>
                                <Save className="w-4 h-4" />
                                Save Profile
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div >
    );
}

function Section({ icon, title, children }) {
    return (
        <div>
            <div className="flex items-center gap-2 mb-3">
                {icon}
                <h3 className="font-semibold text-gray-800">{title}</h3>
            </div>
            {children}
        </div>
    );
}

export default InvestorDNASettings;
