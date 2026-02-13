import React from 'react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

interface PriceData {
    date?: string;
    Date?: string;
    price?: number;
    close?: number;
    Close?: number;
    limit?: number;
    [key: string]: any;
}

interface PriceHistoryChartProps {
    data: PriceData[];
    currencySymbol?: string;
}

const PriceHistoryChart: React.FC<PriceHistoryChartProps> = ({ data, currencySymbol = '$' }) => {
    if (!data || data.length === 0) {
        return (
            <div className="flex items-center justify-center h-64 bg-surface-light/20 rounded-xl border border-glass-border">
                <p className="text-secondary">No price history available</p>
            </div>
        );
    }

    // Format data for chart - robustly handle various key formats
    const chartData = data.map(item => ({
        date: item.Date || item.date,
        // FIX: Added 'item.price' which comes from backend
        price: item.price || item.Close || item.close || item.limit || 0
    }));

    return (
        <div className="w-full animate-fade-in mb-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-white">Price Action (1 Year)</h3>
            </div>

            <div className="w-full h-[250px] glass-card p-4">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff08" vertical={false} />
                        <XAxis
                            dataKey="date"
                            tickFormatter={(str) => {
                                try {
                                    return new Date(str).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                                } catch { return str; }
                            }}
                            stroke="#94a3b8"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            minTickGap={30}
                        />
                        <YAxis
                            domain={['auto', 'auto']}
                            tickFormatter={(num) => `${currencySymbol}${num.toFixed(0)}`}
                            stroke="#94a3b8"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            orientation="right"
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgba(15, 16, 26, 0.9)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '12px',
                                color: '#fff',
                                boxShadow: '0 10px 30px -10px rgba(0,0,0,0.5)'
                            }}
                            itemStyle={{ color: '#a78bfa' }}
                            labelStyle={{ color: '#94a3b8' }}
                            formatter={(value: any) => [`${currencySymbol}${Number(value).toFixed(2)}`, 'Price']}
                            labelFormatter={(label) => {
                                try {
                                    return new Date(label).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                                } catch { return label; }
                            }}
                        />
                        <Area
                            type="monotone"
                            dataKey="price"
                            stroke="#8b5cf6"
                            strokeWidth={3}
                            fillOpacity={1}
                            fill="url(#colorPrice)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default PriceHistoryChart;
