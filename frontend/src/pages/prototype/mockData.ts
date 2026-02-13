export const MOCK_TCS_DATA = {
    header: {
        ticker: "TCS.NS",
        name: "TATA CONSULTANCY SERVICES",
        price: 3295.60,
        change: 39.80,
        changePercent: 1.22
    },
    snapshot: {
        focus: [
            { tag: "STRATEGIC FOCUS", title: "AI-Led Transformation", description: "TCS is aggressively pivoting to AI, with annualised AI revenues hitting $1.5 Billion. The company is deploying Microsoft Copilot and partnering with AWS to drive enterprise modernization.", badges: ["GenAI Center of Excellence", "AWS & Microsoft Partners"] }
        ],
        consensus: {
            targetMean: 3557.36,
            potentialUpside: 7.94,
            analysts: 45,
            sentiment: "BUY" // Gauge needle position
        },
        about: "Tata Consultancy Services Limited provides information technology (IT) and IT enabled services in the Americas, Europe, India, and internationally. The company provides TCS ADD, a suite of AI powered life sciences platforms...",
        keyMetrics: {
            marketCap: "11.92 T",
            peRatio: 24.10,
            divYield: "1.90%",
            employees: "6,07,979"
        }
    },
    financials: {
        margins: [
            { label: "Gross Margin", value: 39.07, color: "bg-purple-500" },
            { label: "Operating Margin", value: 25.18, color: "bg-blue-500" },
            { label: "Net Profit Margin", value: 19.19, color: "bg-green-500" }
        ],
        balanceSheet: {
            cash: 487.14, // Billions
            debt: 109.32,
            debtToEquity: 10.17
        },
        performance: {
            revenue: "2.58 T",
            revenueGrowth: 2.40,
            ebitda: "NaN", // Mimicking screenshot
            netIncome: "193.18 B",
            netIncomeGrowth: 1.40,
            freeCashFlow: "392.65 B",
            liquidityPower: "High"
        }
    },
    marketData: {
        tradingInfo: {
            prevClose: 3255.80,
            open: 3242.90,
            volume: "19,89,207",
            avgVol: "20,54,239",
            beta: "Low Volatility",
            currency: "INR (₹)"
        },
        ranges: {
            dayLow: 3223.2,
            dayHigh: 3300.6,
            yearLow: 2866.6,
            yearHigh: 4322.95
        },
        dividend: {
            rate: 62,
            payoutRatio: "44.65%"
        }
    }
};
