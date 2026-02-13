import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const PriceChart = ({ data, symbol }) => {
    if (!data || data.length === 0) return null;

    return (
        <div className="glass-card p-6 mb-8">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-lg font-bold text-white">Price Trend Analysis</h3>
                    <p className="text-sm text-gray-400">Last 100 Days | {symbol}</p>
                </div>
                <div className="flex gap-4">
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                        <span className="w-3 h-3 rounded-full bg-violet-500"></span> Price
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-300">
                        <span className="w-3 h-3 rounded-full bg-amber-500"></span> SMA 50
                    </div>
                </div>
            </div>

            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={data}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff10" />
                        <XAxis
                            dataKey="date"
                            tick={{ fontSize: 12, fill: '#94a3b8' }}
                            tickFormatter={(val) => val.slice(5)} // Show MM-DD
                            minTickGap={30}
                            axisLine={false}
                            tickLine={false}
                        />
                        <YAxis
                            domain={['auto', 'auto']}
                            tick={{ fontSize: 12, fill: '#94a3b8' }}
                            axisLine={false}
                            tickLine={false}
                            tickFormatter={(val) => `₹${val}`}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgba(15, 16, 26, 0.9)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '12px',
                                color: '#fff',
                                boxShadow: '0 10px 30px -10px rgba(0,0,0,0.5)'
                            }}
                            labelStyle={{ color: '#94a3b8', marginBottom: '4px' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="price"
                            stroke="#8b5cf6"
                            strokeWidth={3}
                            dot={false}
                            activeDot={{ r: 6, fill: '#8b5cf6', stroke: '#fff' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="sma_50"
                            stroke="#f59e0b"
                            strokeWidth={2}
                            strokeDasharray="5 5"
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default PriceChart;
