import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const PriceChart = ({ data, symbol }) => {
    if (!data || data.length === 0) return null;

    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-lg font-bold text-gray-800">Price Trend Analysis</h3>
                    <p className="text-sm text-gray-500">Last 100 Days | {symbol}</p>
                </div>
                <div className="flex gap-4">
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-3 h-3 rounded-full bg-blue-600"></span> Price
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-3 h-3 rounded-full bg-orange-500"></span> SMA 50
                    </div>
                </div>
            </div>

            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={data}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                        <XAxis
                            dataKey="date"
                            tick={{ fontSize: 12, fill: '#9ca3af' }}
                            tickFormatter={(val) => val.slice(5)} // Show MM-DD
                            minTickGap={30}
                            axisLine={false}
                            tickLine={false}
                        />
                        <YAxis
                            domain={['auto', 'auto']}
                            tick={{ fontSize: 12, fill: '#9ca3af' }}
                            axisLine={false}
                            tickLine={false}
                            tickFormatter={(val) => `₹${val}`}
                        />
                        <Tooltip
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                            labelStyle={{ color: '#6b7280', marginBottom: '4px' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="price"
                            stroke="#2563eb"
                            strokeWidth={2}
                            dot={false}
                            activeDot={{ r: 6 }}
                        />
                        <Line
                            type="monotone"
                            dataKey="sma_50"
                            stroke="#f97316"
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
