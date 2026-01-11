import React, { useState } from 'react';
import { ExternalLink, BookOpen, GraduationCap, Youtube, FileText, TrendingUp, AlertTriangle, HelpCircle, ChevronRight, Sparkles } from 'lucide-react';

interface Resource {
    title: string;
    description: string;
    url: string;
    type: 'course' | 'video' | 'article' | 'tool';
    badge?: string;
}

interface Section {
    title: string;
    icon: React.ElementType;
    description: string;
    resources: Resource[];
}

const LearnPage: React.FC = () => {
    const [activeSection, setActiveSection] = useState<string>('basics');

    const sections: Record<string, Section> = {
        basics: {
            title: 'Stock Market Basics',
            icon: BookOpen,
            description: 'Start here if you\'re new to investing',
            resources: [
                {
                    title: 'Zerodha Varsity',
                    description: 'Free, comprehensive course covering stocks, technical & fundamental analysis',
                    url: 'https://zerodha.com/varsity/',
                    type: 'course',
                    badge: 'Recommended'
                },
                {
                    title: 'Investopedia Dictionary',
                    description: 'Look up any financial term with beginner-friendly explanations',
                    url: 'https://www.investopedia.com/financial-term-dictionary-4769738',
                    type: 'article'
                },
                {
                    title: 'Khan Academy Finance',
                    description: 'Free video lessons on stocks, bonds, and investing basics',
                    url: 'https://www.khanacademy.org/economics-finance-domain/core-finance',
                    type: 'course'
                }
            ]
        },
        analysis: {
            title: 'Analysis Techniques',
            icon: TrendingUp,
            description: 'Learn to analyze stocks like a pro',
            resources: [
                {
                    title: 'Understanding P/E Ratio',
                    description: 'What it means and how to interpret it',
                    url: 'https://www.investopedia.com/terms/p/price-earningsratio.asp',
                    type: 'article'
                },
                {
                    title: 'Technical Analysis Guide',
                    description: 'Learn chart patterns, indicators, and trading signals',
                    url: 'https://zerodha.com/varsity/module/technical-analysis/',
                    type: 'course'
                },
                {
                    title: 'Fundamental Analysis',
                    description: 'How to read balance sheets and assess company health',
                    url: 'https://zerodha.com/varsity/module/fundamental-analysis/',
                    type: 'course'
                }
            ]
        },
        youtube: {
            title: 'YouTube Channels',
            icon: Youtube,
            description: 'Learn from expert educators',
            resources: [
                {
                    title: 'Pranjal Kamra',
                    description: 'Indian stock market analysis and investment strategies',
                    url: 'https://www.youtube.com/@PranjalKamra',
                    type: 'video',
                    badge: 'Hindi'
                },
                {
                    title: 'CA Rachana Ranade',
                    description: 'Stock market education for beginners',
                    url: 'https://www.youtube.com/@CARachanaRanade',
                    type: 'video',
                    badge: 'Hindi/English'
                },
                {
                    title: 'The Plain Bagel',
                    description: 'Clear explanations of investing concepts',
                    url: 'https://www.youtube.com/@ThePlainBagel',
                    type: 'video',
                    badge: 'English'
                },
                {
                    title: 'Two Cents (PBS)',
                    description: 'Personal finance fundamentals',
                    url: 'https://www.youtube.com/@TwoCentsPBS',
                    type: 'video',
                    badge: 'English'
                }
            ]
        },
        books: {
            title: 'Recommended Books',
            icon: GraduationCap,
            description: 'Classic investing wisdom',
            resources: [
                {
                    title: 'The Intelligent Investor',
                    description: 'By Benjamin Graham - The bible of value investing',
                    url: 'https://www.amazon.in/Intelligent-Investor-English-Paperback-2013/dp/0062312685',
                    type: 'article',
                    badge: 'Classic'
                },
                {
                    title: 'One Up On Wall Street',
                    description: 'By Peter Lynch - Practical investing from a legendary fund manager',
                    url: 'https://www.amazon.in/One-Up-Wall-Street-Already/dp/0743200403',
                    type: 'article'
                },
                {
                    title: 'Coffee Can Investing',
                    description: 'By Saurabh Mukherjea - Great for Indian market investors',
                    url: 'https://www.amazon.in/Coffee-Can-Investing-Stupendous-Wealth/dp/067009045X',
                    type: 'article',
                    badge: 'India'
                }
            ]
        }
    };

    const quickTerms = [
        { term: 'P/E Ratio', meaning: 'Price-to-Earnings. Lower = cheaper (usually)' },
        { term: 'Market Cap', meaning: 'Total company value (Price × Shares)' },
        { term: '52-Week High', meaning: 'Highest stock price in past year' },
        { term: 'Beta', meaning: 'Volatility measure. >1 = more volatile than market' },
        { term: 'Match Score', meaning: 'ELIDA\'s personalized fit rating (0-100%)' }
    ];

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'course': return <GraduationCap className="w-4 h-4" />;
            case 'video': return <Youtube className="w-4 h-4" />;
            case 'article': return <FileText className="w-4 h-4" />;
            default: return <FileText className="w-4 h-4" />;
        }
    };

    return (
        <div className="min-h-screen p-6 md:p-8">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 bg-gradient-to-br from-primary-500/20 to-accent-dark/20 rounded-xl">
                        <BookOpen className="w-6 h-6 text-primary-400" />
                    </div>
                    <h1 className="text-2xl md:text-3xl font-bold text-white">Learning Center</h1>
                    <span className="px-2 py-0.5 bg-primary-500/20 text-primary-400 text-xs font-medium rounded-full">
                        NEW
                    </span>
                </div>
                <p className="text-secondary">
                    Master the fundamentals of investing with curated resources
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column - Navigation & Quick Terms */}
                <div className="space-y-6">
                    {/* Section Navigation */}
                    <div className="glass-card p-4">
                        <h3 className="text-sm font-semibold text-secondary uppercase mb-3">Topics</h3>
                        <div className="space-y-1">
                            {Object.entries(sections).map(([key, section]) => (
                                <button
                                    key={key}
                                    onClick={() => setActiveSection(key)}
                                    className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all ${activeSection === key
                                            ? 'bg-primary-500/20 text-primary-400 border border-primary-500/30'
                                            : 'text-secondary hover:text-white hover:bg-surface-light'
                                        }`}
                                >
                                    <section.icon className="w-5 h-5" />
                                    <span className="font-medium">{section.title}</span>
                                    <ChevronRight className={`w-4 h-4 ml-auto transition-transform ${activeSection === key ? 'rotate-90' : ''
                                        }`} />
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Quick Terms */}
                    <div className="glass-card p-4">
                        <div className="flex items-center gap-2 mb-4">
                            <HelpCircle className="w-4 h-4 text-accent" />
                            <h3 className="text-sm font-semibold text-secondary uppercase">Quick Terms</h3>
                        </div>
                        <div className="space-y-3">
                            {quickTerms.map((item, idx) => (
                                <div key={idx} className="p-3 bg-surface-light/50 rounded-lg">
                                    <div className="font-medium text-white text-sm">{item.term}</div>
                                    <div className="text-xs text-secondary mt-1">{item.meaning}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Column - Resources */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Active Section Header */}
                    <div className="glass-card p-6">
                        <div className="flex items-center gap-3 mb-2">
                            {React.createElement(sections[activeSection].icon, { className: 'w-6 h-6 text-primary-400' })}
                            <h2 className="text-xl font-bold text-white">{sections[activeSection].title}</h2>
                        </div>
                        <p className="text-secondary">{sections[activeSection].description}</p>
                    </div>

                    {/* Resource Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {sections[activeSection].resources.map((resource, idx) => (
                            <a
                                key={idx}
                                href={resource.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="glass-card p-5 hover:border-primary-500/30 transition-all group"
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <div className="flex items-center gap-2">
                                        <div className="p-2 bg-surface-light rounded-lg text-secondary group-hover:text-primary-400 transition-colors">
                                            {getTypeIcon(resource.type)}
                                        </div>
                                        {resource.badge && (
                                            <span className="px-2 py-0.5 bg-accent/20 text-accent text-xs font-medium rounded-full">
                                                {resource.badge}
                                            </span>
                                        )}
                                    </div>
                                    <ExternalLink className="w-4 h-4 text-secondary opacity-0 group-hover:opacity-100 transition-opacity" />
                                </div>
                                <h3 className="font-semibold text-white mb-2 group-hover:text-primary-400 transition-colors">
                                    {resource.title}
                                </h3>
                                <p className="text-sm text-secondary line-clamp-2">
                                    {resource.description}
                                </p>
                            </a>
                        ))}
                    </div>

                    {/* Disclaimer */}
                    <div className="flex items-start gap-3 p-4 bg-warning/10 border border-warning/30 rounded-xl">
                        <AlertTriangle className="w-5 h-5 text-warning flex-shrink-0 mt-0.5" />
                        <div>
                            <p className="text-sm text-warning font-medium">Educational Content Only</p>
                            <p className="text-xs text-secondary mt-1">
                                ELIDA is a learning tool, not financial advice. Always do your own research and consider consulting a SEBI-registered advisor.
                            </p>
                        </div>
                    </div>

                    {/* Ask Chatbot CTA */}
                    <div className="glass-card p-6 bg-gradient-to-r from-primary-500/10 to-accent-dark/10 border-primary-500/20">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-primary-500/20 rounded-xl">
                                <Sparkles className="w-6 h-6 text-primary-400" />
                            </div>
                            <div className="flex-1">
                                <h3 className="font-semibold text-white">Have Questions?</h3>
                                <p className="text-sm text-secondary">
                                    Use the AI chatbot (bottom-right) to ask about any investing concept!
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LearnPage;
