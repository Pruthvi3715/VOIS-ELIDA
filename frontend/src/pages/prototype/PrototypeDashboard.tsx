import React, { useState } from 'react';
import { MOCK_TCS_DATA } from './mockData';
import { motion, AnimatePresence } from 'framer-motion';
// Icons
import { FiTrendingUp, FiActivity, FiGlobe, FiCpu, FiAlertCircle, FiDollarSign, FiFileText } from 'react-icons/fi';

const PrototypeDashboard = () => {
    const [activeTab, setActiveTab] = useState('snapshot');
    const d = MOCK_TCS_DATA;

    const TabButton = ({ id, label, icon: Icon }) => (
        <button
            onClick={() => setActiveTab(id)}
            className={`relative px-6 py-4 flex items-center space-x-2 text-sm font-medium transition-colors ${activeTab === id ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
                }`}
        >
            <Icon className="w-4 h-4" />
            <span>{label}</span>
            {activeTab === id && (
                <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"
                />
            )}
        </button>
    );

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
            {/* Header Section */}
            <header className="bg-white border-b sticky top-0 z-10 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="py-4 flex justify-between items-start">
                        <div className="flex items-center space-x-4">
                            <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg">
                                TCS
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900 leading-none">{d.header.ticker}</h1>
                                <p className="text-xs text-gray-500 mt-1 tracking-wider">{d.header.name}</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <div className="text-3xl font-bold text-gray-900">₹{d.header.price.toLocaleString()}</div>
                            <div className={`text-sm font-semibold flex items-center justify-end ${d.header.change > 0 ? 'text-green-600' : 'text-red-500'}`}>
                                {d.header.change > 0 ? '▲' : '▼'} {d.header.change} ({d.header.changePercent}%)
                            </div>
                        </div>
                    </div>

                    {/* Navigation - Mimicking screenshots */}
                    <div className="flex space-x-2 mt-4 overflow-x-auto no-scrollbar border-t border-gray-100">
                        <TabButton id="snapshot" label="Snapshot" icon={FiActivity} />
                        <TabButton id="financials" label="Financials" icon={FiDollarSign} />
                        <TabButton id="market" label="Market Data" icon={FiTrendingUp} />
                        <TabButton id="ai" label="AI Analysis" icon={FiCpu} />
                    </div>
                </div>
            </header>

            {/* Main Content Area */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <AnimatePresence mode="wait">

                    {/* SNAPSHOT TAB - Banner style from image 1 */}
                    {activeTab === 'snapshot' && (
                        <motion.div
                            key="snapshot"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="space-y-6"
                        >
                            {/* Hero Banner */}
                            <div className="relative rounded-2xl overflow-hidden bg-gradient-to-r from-blue-700 to-purple-800 text-white shadow-xl min-h-[300px] flex items-center">
                                {/* Decorative background circles */}
                                <div className="absolute top-0 right-0 w-96 h-96 bg-white opacity-5 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl"></div>
                                <div className="absolute bottom-0 left-20 w-64 h-64 bg-blue-400 opacity-10 rounded-full translate-y-1/2 blur-2xl"></div>

                                <div className="relative z-10 p-8 md:p-12 w-full md:w-2/3">
                                    <div className="inline-block px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-xs font-semibold tracking-wide mb-4 border border-white/10 uppercase">
                                        {d.snapshot.focus[0].tag}
                                    </div>
                                    <h2 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
                                        {d.snapshot.focus[0].title}
                                    </h2>
                                    <p className="text-lg text-blue-100 leading-relaxed mb-8 max-w-xl">
                                        {d.snapshot.focus[0].description}
                                    </p>
                                    <div className="flex flex-wrap gap-3">
                                        {d.snapshot.focus[0].badges.map((b, i) => (
                                            <span key={i} className="px-4 py-2 bg-purple-900/50 backdrop-blur-md rounded-lg text-sm font-medium border border-purple-500/30 flex items-center">
                                                <FiCpu className="mr-2" /> {b}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Metrics Grid */}
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                                {/* About Card */}
                                <div className="md:col-span-3 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                                    <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                                        <FiFileText className="mr-2 text-blue-500" /> About TCS
                                    </h3>
                                    <p className="text-gray-600 leading-relaxed text-sm">
                                        {d.snapshot.about}
                                        <button className="text-blue-600 font-semibold ml-1 hover:underline">Show less</button>
                                    </p>

                                    {/* Key Stats Row */}
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-6 border-t border-gray-100">
                                        <div>
                                            <div className="text-xs text-gray-400 uppercase font-semibold">Market Cap</div>
                                            <div className="text-xl font-bold text-gray-900">₹{d.snapshot.keyMetrics.marketCap}</div>
                                        </div>
                                        <div>
                                            <div className="text-xs text-gray-400 uppercase font-semibold">P/E Ratio</div>
                                            <div className="text-xl font-bold text-gray-900">{d.snapshot.keyMetrics.peRatio}</div>
                                        </div>
                                        <div>
                                            <div className="text-xs text-gray-400 uppercase font-semibold">Div Yield</div>
                                            <div className="text-xl font-bold text-green-600">{d.snapshot.keyMetrics.divYield}</div>
                                        </div>
                                        <div>
                                            <div className="text-xs text-gray-400 uppercase font-semibold">Employees</div>
                                            <div className="text-xl font-bold text-gray-900">{d.snapshot.keyMetrics.employees}</div>
                                        </div>
                                    </div>
                                </div>

                                {/* Consensus Gauge */}
                                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 flex flex-col justify-center items-center">
                                    <h3 className="text-sm font-bold text-gray-500 mb-6 uppercase tracking-wider w-full text-left">Analyst Consensus</h3>
                                    <div className="relative w-48 h-24 overflow-hidden mb-4">
                                        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-red-200 via-yellow-200 to-green-200 rounded-t-full opacity-30"></div>
                                        <div className="absolute top-0 left-0 w-full h-full border-[20px] border-t-emerald-400 border-r-transparent border-b-transparent border-l-transparent rounded-full rotate-45 transform origin-bottom"></div>
                                        {/* This is a CSS quick hack for a gauge, normally use chart library */}
                                        <div className="absolute bottom-0 left-1/2 w-1 h-24 bg-gray-800 origin-bottom transform rotate-[45deg] z-10 transition-all duration-1000 ease-out" style={{ transform: 'translateX(-50%) rotate(30deg)' }}></div>
                                        <div className="absolute bottom-0 left-1/2 w-4 h-4 bg-gray-900 rounded-full -translate-x-1/2 translate-y-1/2 z-20"></div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-sm text-gray-400">Target Mean</div>
                                        <div className="text-2xl font-bold text-gray-900">₹{d.snapshot.consensus.targetMean.toLocaleString()}</div>
                                        <div className="text-xs font-bold text-emerald-500 mt-1">+{d.snapshot.consensus.potentialUpside}% Potential</div>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* FINANCIALS TAB - Based on image 3 */}
                    {activeTab === 'financials' && (
                        <motion.div
                            key="financials"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="grid grid-cols-1 md:grid-cols-2 gap-6"
                        >
                            {/* Margin Analysis */}
                            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                                <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center">
                                    <div className="w-1 h-6 bg-purple-500 rounded-full mr-3"></div>
                                    Margin Analysis
                                </h3>
                                <div className="space-y-6">
                                    {d.financials.margins.map((m, i) => (
                                        <div key={i}>
                                            <div className="flex justify-between text-sm font-medium mb-2">
                                                <span className="text-gray-600">{m.label}</span>
                                                <span className="text-gray-900">{m.value}%</span>
                                            </div>
                                            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                                                <motion.div
                                                    initial={{ width: 0 }}
                                                    animate={{ width: `${m.value}%` }}
                                                    transition={{ duration: 1, delay: i * 0.2 }}
                                                    className={`h-full rounded-full ${m.color}`}
                                                ></motion.div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <p className="mt-6 text-xs text-gray-400 italic">
                                    Strong profitability margins reflect TCS's operational efficiency.
                                </p>
                            </div>

                            {/* Balance Sheet Strength */}
                            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                                <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center">
                                    <div className="w-1 h-6 bg-blue-500 rounded-full mr-3"></div>
                                    Balance Sheet Strength
                                </h3>
                                <div className="flex justify-center items-center space-x-12 mt-8">
                                    {/* Cash Ring */}
                                    <div className="relative w-32 h-32 flex items-center justify-center">
                                        <svg className="w-full h-full transform -rotate-90">
                                            <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-green-100" />
                                            <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-green-400" strokeDasharray={351} strokeDashoffset={351 * 0.2} />
                                        </svg>
                                        <div className="absolute text-center">
                                            <div className="text-xs text-gray-400 font-bold">CASH</div>
                                            <div className="text-lg font-bold text-green-600">₹{d.financials.balanceSheet.cash} B</div>
                                        </div>
                                    </div>

                                    {/* Debt Ring */}
                                    <div className="relative w-32 h-32 flex items-center justify-center">
                                        <svg className="w-full h-full transform -rotate-90">
                                            <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-red-100" />
                                            <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-red-400" strokeDasharray={351} strokeDashoffset={351 * 0.8} />
                                        </svg>
                                        <div className="absolute text-center">
                                            <div className="text-xs text-gray-400 font-bold">DEBT</div>
                                            <div className="text-lg font-bold text-red-500">₹{d.financials.balanceSheet.debt} B</div>
                                        </div>
                                    </div>
                                </div>
                                <div className="mt-8 bg-blue-50 rounded-lg p-4 text-center">
                                    <div className="text-2xl font-bold text-blue-700">{d.financials.balanceSheet.debtToEquity}%</div>
                                    <div className="text-xs font-bold text-blue-400 uppercase">Debt to Equity Ratio</div>
                                </div>
                            </div>

                            {/* Annual Performance Banner */}
                            <div className="md:col-span-2 bg-gray-900 rounded-xl p-8 text-white flex flex-wrap justify-between items-center shadow-lg">
                                <div>
                                    <div className="flex items-center space-x-2 mb-6">
                                        <FiTrendingUp className="text-yellow-400 w-6 h-6" />
                                        <h3 className="text-lg font-bold">Annual Performance</h3>
                                    </div>
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-12">
                                        <div>
                                            <div className="text-xs text-gray-400 mb-1">Total Revenue</div>
                                            <div className="text-3xl font-bold">₹{d.financials.performance.revenue}</div>
                                            <div className="text-xs text-green-400 mt-1">↑ {d.financials.performance.revenueGrowth}%</div>
                                        </div>
                                        <div>
                                            <div className="text-xs text-gray-400 mb-1">EBITDA</div>
                                            <div className="text-3xl font-bold text-gray-500">{d.financials.performance.ebitda}</div>
                                            <div className="text-xs text-gray-500 mt-1">Inv. Data</div>
                                        </div>
                                        <div>
                                            <div className="text-xs text-gray-400 mb-1">Net Income</div>
                                            <div className="text-3xl font-bold">₹{d.financials.performance.netIncome}</div>
                                            <div className="text-xs text-green-400 mt-1">↑ {d.financials.performance.netIncomeGrowth}%</div>
                                        </div>
                                        <div>
                                            <div className="text-xs text-gray-400 mb-1">Free Cash Flow</div>
                                            <div className="text-3xl font-bold text-yellow-400">₹{d.financials.performance.freeCashFlow}</div>
                                            <div className="text-xs text-yellow-200/50 mt-1">{d.financials.performance.liquidityPower} Liquidity</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* MARKET DATA TAB - Based on image 2 */}
                    {activeTab === 'market' && (
                        <motion.div
                            key="market"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="grid grid-cols-1 md:grid-cols-3 gap-6"
                        >
                            <div className="md:col-span-2 space-y-6">
                                {/* Main Price Card */}
                                <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-100">
                                    <div className="flex justify-between items-start mb-8">
                                        <div>
                                            <div className="text-sm text-gray-500 mb-1">Current Price</div>
                                            <div className="text-5xl font-bold text-gray-900 tracking-tight">₹{d.header.price.toLocaleString()}</div>
                                            <div className="flex items-center mt-2 text-green-600 font-medium">
                                                <FiTrendingUp className="mr-2" />
                                                {d.header.change} ({d.header.changePercent}%) vs prev close
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-sm text-gray-500 mb-1">Volume</div>
                                            <div className="text-2xl font-bold text-gray-800">{d.marketData.tradingInfo.volume}</div>
                                            <div className="text-xs text-gray-400">Avg (10d): {d.marketData.tradingInfo.avgVol}</div>
                                        </div>
                                    </div>

                                    {/* Range Sliders */}
                                    <div className="space-y-8">
                                        <div>
                                            <div className="flex justify-between text-sm font-medium text-gray-600 mb-2">
                                                <span>Day Low</span>
                                                <span>Day High</span>
                                            </div>
                                            <div className="relative h-2 bg-gray-100 rounded-full">
                                                <div className="absolute left-0 top-0 h-full bg-blue-500 rounded-full" style={{ width: '60%' }}></div>
                                                <div className="flex justify-between text-xs font-bold text-gray-900 mt-3">
                                                    <span>₹{d.marketData.ranges.dayLow}</span>
                                                    <span>₹{d.marketData.ranges.dayHigh}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div>
                                            <div className="flex justify-between text-sm font-medium text-gray-600 mb-2">
                                                <span>52 Week Low</span>
                                                <span>52 Week High</span>
                                            </div>
                                            <div className="relative h-2 bg-gray-100 rounded-full">
                                                <div className="absolute left-0 top-0 h-full bg-blue-500 rounded-full" style={{ width: '40%' }}></div>
                                                <div className="flex justify-between text-xs font-bold text-gray-900 mt-3">
                                                    <span>₹{d.marketData.ranges.yearLow}</span>
                                                    <span>₹{d.marketData.ranges.yearHigh}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-6">
                                {/* Trading Info */}
                                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
                                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-6">Trading Info</h3>
                                    <div className="space-y-4">
                                        <div className="flex justify-between border-b border-gray-50 pb-3">
                                            <span className="text-gray-500 text-sm">Previous Close</span>
                                            <span className="font-semibold text-gray-900">₹{d.marketData.tradingInfo.prevClose}</span>
                                        </div>
                                        <div className="flex justify-between border-b border-gray-50 pb-3">
                                            <span className="text-gray-500 text-sm">Open</span>
                                            <span className="font-semibold text-gray-900">₹{d.marketData.tradingInfo.open}</span>
                                        </div>
                                        <div className="flex justify-between border-b border-gray-50 pb-3">
                                            <span className="text-gray-500 text-sm">Beta (Volatility)</span>
                                            <span className="font-semibold text-gray-900">{d.marketData.tradingInfo.beta}</span>
                                        </div>
                                        <div className="flex justify-between pb-1">
                                            <span className="text-gray-500 text-sm">Currency</span>
                                            <span className="font-semibold text-gray-900">{d.marketData.tradingInfo.currency}</span>
                                        </div>
                                    </div>
                                </div>

                                {/* Dividend Info - Blue Box */}
                                <div className="bg-blue-50/50 rounded-xl p-6 border border-blue-100">
                                    <h3 className="text-xs font-bold text-blue-800 uppercase tracking-wider mb-4">Dividend Info</h3>
                                    <div className="flex items-baseline space-x-2">
                                        <span className="text-4xl font-bold text-blue-600">62</span>
                                        <span className="text-sm font-medium text-blue-400">INR / Share</span>
                                    </div>
                                    <div className="text-xs text-blue-400/80 mb-6">Trailing Annual Dividend</div>

                                    <div className="bg-white rounded-lg p-3 flex justify-between items-center shadow-sm">
                                        <span className="text-xs font-bold text-gray-500">Payout Ratio</span>
                                        <span className="text-sm font-bold text-gray-900">{d.marketData.dividend.payoutRatio}</span>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* AI ANALYSIS TAB - The "Extra Thing" Requested */}
                    {activeTab === 'ai' && (
                        <motion.div
                            key="ai"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="grid grid-cols-1 md:grid-cols-4 gap-6"
                        >
                            <div className="md:col-span-4 bg-gradient-to-r from-gray-900 to-gray-800 rounded-xl p-8 text-white shadow-xl relative overflow-hidden">
                                <div className="relative z-10 flex justify-between items-center">
                                    <div>
                                        <h2 className="text-2xl font-bold mb-2 flex items-center">
                                            <FiCPU className="mr-3 text-cyan-400" /> ELIDA AI Intelligence
                                        </h2>
                                        <p className="text-gray-400 max-w-2xl">
                                            Our proprietary multi-agent system has analyzed thousands of data points to generate this strategic outlook.
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-5xl font-bold text-cyan-400">87</div>
                                        <div className="text-xs font-bold uppercase tracking-widest text-cyan-200/50 mt-1">Confidence Score</div>
                                    </div>
                                </div>
                                <div className="absolute top-0 right-0 w-full h-full bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
                            </div>

                            {['Quant', 'Macro', 'Philosopher', 'Regret'].map((agent, i) => (
                                <motion.div
                                    key={agent}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.1 }}
                                    className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
                                >
                                    <div className="flex items-center justify-between mb-4">
                                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold
                            ${agent === 'Quant' ? 'bg-blue-500' :
                                                agent === 'Macro' ? 'bg-purple-500' :
                                                    agent === 'Philosopher' ? 'bg-emerald-500' : 'bg-orange-500'
                                            }`}>
                                            {agent[0]}
                                        </div>
                                        <div className="text-right">
                                            <div className="text-2xl font-bold text-gray-900">{80 + i * 2}</div>
                                            <div className="text-[10px] uppercase font-bold text-gray-400">Agent Score</div>
                                        </div>
                                    </div>
                                    <h3 className="font-bold text-gray-800 mb-2">{agent} Analysis</h3>
                                    <p className="text-sm text-gray-500 leading-relaxed">
                                        {agent === 'Quant' ? 'Strong fundamentals with high ROE and pristine balance sheet. Valuation indicates fair entry point.' :
                                            agent === 'Macro' ? 'Sector tailwinds from AI adoption and global digital transformation robust despite currency risks.' :
                                                agent === 'Philosopher' ? 'High ethical alignment score. Strong governance and employee welfare programs detected.' :
                                                    'Low regret probability. Downside limited by strong cash position and market leadership.'}
                                    </p>
                                </motion.div>
                            ))}
                        </motion.div>
                    )}

                </AnimatePresence>
            </main>
        </div>
    );
};

// Fix the icon typo in the AI tab just to be safe (FiCpu usually imported as FiCpu)
const FiCPU = FiCpu;

export default PrototypeDashboard;
