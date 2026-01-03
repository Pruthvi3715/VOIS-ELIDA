import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Dna, Bell, Shield, Palette, Moon, Sun, Save } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface UserSettings {
    dnaEnabled: boolean;
    dnaDefault: boolean;
    darkMode: boolean;
    notifications: boolean;
    riskTolerance: 'low' | 'medium' | 'high';
}

const SettingsPage: React.FC = () => {
    const { user } = useAuth();

    const [settings, setSettings] = useState<UserSettings>(() => {
        const saved = localStorage.getItem('vois_settings');
        return saved ? JSON.parse(saved) : {
            dnaEnabled: true,
            dnaDefault: true,
            darkMode: true,
            notifications: true,
            riskTolerance: 'medium'
        };
    });
    const [saved, setSaved] = useState(false);

    const saveSettings = () => {
        localStorage.setItem('vois_settings', JSON.stringify(settings));
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    };

    const updateSetting = (key: keyof UserSettings, value: any) => {
        setSettings(prev => ({ ...prev, [key]: value }));
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center gap-4">
                <div className="p-3 rounded-xl bg-gradient-primary">
                    <SettingsIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-white">Settings</h1>
                    <p className="text-secondary text-sm">Customize your VOIS experience</p>
                </div>
            </div>

            {/* Investor DNA Settings */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-card p-6"
            >
                <div className="flex items-center gap-3 mb-6">
                    <Dna className="w-5 h-5 text-primary-400" />
                    <h2 className="text-lg font-semibold text-white">Investor DNA</h2>
                </div>

                <div className="space-y-4">
                    {/* DNA Enabled */}
                    <div className="flex items-center justify-between p-4 bg-surface-light/50 rounded-xl">
                        <div>
                            <p className="text-white font-medium">Enable Investor DNA</p>
                            <p className="text-sm text-secondary">Personalize recommendations based on your profile</p>
                        </div>
                        <button
                            onClick={() => updateSetting('dnaEnabled', !settings.dnaEnabled)}
                            className={`relative w-14 h-7 rounded-full transition-colors ${settings.dnaEnabled ? 'bg-primary-500' : 'bg-surface'
                                }`}
                        >
                            <motion.div
                                animate={{ x: settings.dnaEnabled ? 28 : 4 }}
                                className="absolute top-1 w-5 h-5 bg-white rounded-full shadow"
                            />
                        </button>
                    </div>

                    {/* DNA Default On */}
                    <div className="flex items-center justify-between p-4 bg-surface-light/50 rounded-xl">
                        <div>
                            <p className="text-white font-medium">DNA On by Default</p>
                            <p className="text-sm text-secondary">Start analysis with DNA toggle enabled</p>
                        </div>
                        <button
                            onClick={() => updateSetting('dnaDefault', !settings.dnaDefault)}
                            className={`relative w-14 h-7 rounded-full transition-colors ${settings.dnaDefault ? 'bg-primary-500' : 'bg-surface'
                                }`}
                        >
                            <motion.div
                                animate={{ x: settings.dnaDefault ? 28 : 4 }}
                                className="absolute top-1 w-5 h-5 bg-white rounded-full shadow"
                            />
                        </button>
                    </div>

                    {/* Risk Tolerance */}
                    <div className="p-4 bg-surface-light/50 rounded-xl">
                        <p className="text-white font-medium mb-3">Risk Tolerance</p>
                        <div className="flex gap-2">
                            {(['low', 'medium', 'high'] as const).map(level => (
                                <button
                                    key={level}
                                    onClick={() => updateSetting('riskTolerance', level)}
                                    className={`flex-1 py-2 px-4 rounded-lg font-medium capitalize transition ${settings.riskTolerance === level
                                            ? 'bg-gradient-primary text-white'
                                            : 'bg-surface text-secondary hover:text-white'
                                        }`}
                                >
                                    {level}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* Appearance Settings */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="glass-card p-6"
            >
                <div className="flex items-center gap-3 mb-6">
                    <Palette className="w-5 h-5 text-accent" />
                    <h2 className="text-lg font-semibold text-white">Appearance</h2>
                </div>

                <div className="flex items-center justify-between p-4 bg-surface-light/50 rounded-xl">
                    <div className="flex items-center gap-3">
                        {settings.darkMode ? <Moon className="w-5 h-5 text-primary-400" /> : <Sun className="w-5 h-5 text-warning" />}
                        <div>
                            <p className="text-white font-medium">Dark Mode</p>
                            <p className="text-sm text-secondary">Use dark theme (recommended)</p>
                        </div>
                    </div>
                    <button
                        onClick={() => updateSetting('darkMode', !settings.darkMode)}
                        className={`relative w-14 h-7 rounded-full transition-colors ${settings.darkMode ? 'bg-primary-500' : 'bg-surface'
                            }`}
                    >
                        <motion.div
                            animate={{ x: settings.darkMode ? 28 : 4 }}
                            className="absolute top-1 w-5 h-5 bg-white rounded-full shadow"
                        />
                    </button>
                </div>
            </motion.div>

            {/* Notifications */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="glass-card p-6"
            >
                <div className="flex items-center gap-3 mb-6">
                    <Bell className="w-5 h-5 text-warning" />
                    <h2 className="text-lg font-semibold text-white">Notifications</h2>
                </div>

                <div className="flex items-center justify-between p-4 bg-surface-light/50 rounded-xl">
                    <div>
                        <p className="text-white font-medium">Analysis Alerts</p>
                        <p className="text-sm text-secondary">Get notified when analysis completes</p>
                    </div>
                    <button
                        onClick={() => updateSetting('notifications', !settings.notifications)}
                        className={`relative w-14 h-7 rounded-full transition-colors ${settings.notifications ? 'bg-primary-500' : 'bg-surface'
                            }`}
                    >
                        <motion.div
                            animate={{ x: settings.notifications ? 28 : 4 }}
                            className="absolute top-1 w-5 h-5 bg-white rounded-full shadow"
                        />
                    </button>
                </div>
            </motion.div>

            {/* Save Button */}
            <motion.button
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                onClick={saveSettings}
                className={`w-full btn-primary flex items-center justify-center gap-2 ${saved ? 'bg-success hover:bg-success' : ''
                    }`}
            >
                <Save className="w-4 h-4" />
                {saved ? 'Saved!' : 'Save Settings'}
            </motion.button>
        </div>
    );
};

export default SettingsPage;
