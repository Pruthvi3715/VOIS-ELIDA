# Finance Knowledge Base for ELIDA Chatbot
# Instant answers for common financial terms - no LLM needed

FINANCE_KNOWLEDGE_BASE = {
    # Market Indicators
    "vix": {
        "term": "VIX (Volatility Index)",
        "definition": "The VIX, also known as the 'Fear Index', measures the market's expectation of 30-day volatility based on S&P 500 options. A VIX above 30 indicates high fear/uncertainty, while below 20 suggests calm markets.",
        "why_important": "Helps gauge market sentiment. High VIX = risky time to buy; Low VIX = potentially safer entry point.",
        "simple_explanation": "Think of VIX as a 'fear meter' for the stock market. When people are scared, VIX goes up."
    },
    "india vix": {
        "term": "India VIX",
        "definition": "India VIX is the volatility index for the Indian stock market (NIFTY 50). It works similar to the US VIX and measures expected volatility over the next 30 days.",
        "why_important": "A high India VIX (above 25) suggests caution; low India VIX (below 15) suggests stable markets.",
        "simple_explanation": "India's version of the 'fear meter'. High = nervous market, Low = calm market."
    },
    
    # Fundamental Metrics
    "pe ratio": {
        "term": "P/E Ratio (Price-to-Earnings)",
        "definition": "P/E Ratio = Stock Price ÷ Earnings Per Share (EPS). It shows how much investors pay for each rupee of earnings. Example: P/E of 20 means you pay ₹20 for every ₹1 of profit.",
        "why_important": "Lower P/E might mean undervalued stock; Higher P/E suggests growth expectations or overvaluation.",
        "simple_explanation": "How many years of profits you're paying upfront. P/E of 15 = you're paying 15 years of profits to own the stock today."
    },
    "p/e ratio": {
        "term": "P/E Ratio (Price-to-Earnings)",
        "definition": "P/E Ratio = Stock Price ÷ Earnings Per Share (EPS). It shows how much investors pay for each rupee of earnings. Example: P/E of 20 means you pay ₹20 for every ₹1 of profit.",
        "why_important": "Lower P/E might mean undervalued stock; Higher P/E suggests growth expectations or overvaluation.",
        "simple_explanation": "How many years of profits you're paying upfront. P/E of 15 = you're paying 15 years of profits to own the stock today."
    },
    "eps": {
        "term": "EPS (Earnings Per Share)",
        "definition": "EPS = Net Profit ÷ Total Shares Outstanding. It tells you how much profit the company makes per share you own.",
        "why_important": "Higher EPS = more profitable. Growing EPS year-over-year is a positive sign.",
        "simple_explanation": "If you owned one share, this is 'your share' of the company's profit."
    },
    "roe": {
        "term": "ROE (Return on Equity)",
        "definition": "ROE = Net Income ÷ Shareholders' Equity × 100%. It measures how efficiently a company uses investor money to generate profits.",
        "why_important": "ROE above 15-20% is generally good. Consistently high ROE indicates a well-managed company.",
        "simple_explanation": "For every ₹100 investors put in, how much profit does the company make? ROE of 20% = ₹20 profit."
    },
    "pb ratio": {
        "term": "P/B Ratio (Price-to-Book)",
        "definition": "P/B Ratio = Stock Price ÷ Book Value Per Share. Book value is the company's assets minus liabilities, divided by shares.",
        "why_important": "P/B below 1 might indicate undervaluation; above 3 might suggest overvaluation. Useful for banks and asset-heavy companies.",
        "simple_explanation": "If the company sold everything today, would you get more or less than what you paid for the share?"
    },
    "debt to equity": {
        "term": "Debt-to-Equity Ratio (D/E)",
        "definition": "D/E = Total Debt ÷ Shareholders' Equity. It shows how much debt the company uses compared to its own money.",
        "why_important": "D/E below 1 is safer for most industries. High D/E (above 2) means high financial risk.",
        "simple_explanation": "For every ₹1 the company owns, how much has it borrowed? D/E of 0.5 = borrowed ₹0.50 for every ₹1 of its own."
    },
    "market cap": {
        "term": "Market Capitalization",
        "definition": "Market Cap = Current Stock Price × Total Shares Outstanding. It represents the total value of a company in the market.",
        "why_important": "Large Cap (>₹20,000 Cr) = stable; Mid Cap (₹5,000-20,000 Cr) = growth potential; Small Cap (<₹5,000 Cr) = higher risk/reward.",
        "simple_explanation": "The total price tag to buy the entire company at today's share price."
    },
    "dividend yield": {
        "term": "Dividend Yield",
        "definition": "Dividend Yield = (Annual Dividend ÷ Stock Price) × 100%. It shows the annual return you get just from dividends.",
        "why_important": "High dividend yield (3-6%) provides regular income. Very high (>8%) might indicate a company in trouble.",
        "simple_explanation": "Like interest on a bank deposit, but from stocks. 4% yield on ₹100 stock = ₹4 per year in your pocket."
    },
    
    # Technical Terms
    "moving average": {
        "term": "Moving Average (MA)",
        "definition": "A moving average smooths out price data by calculating the average price over a period (e.g., 50-day MA, 200-day MA).",
        "why_important": "When price crosses above 200-day MA = bullish signal; below = bearish. Used to identify trends.",
        "simple_explanation": "Average price over last X days. If today's price is above it, the trend might be up."
    },
    "rsi": {
        "term": "RSI (Relative Strength Index)",
        "definition": "RSI measures momentum on a scale of 0-100. Above 70 = overbought (might fall); Below 30 = oversold (might rise).",
        "why_important": "Helps identify if a stock has moved too fast in one direction and might reverse.",
        "simple_explanation": "A score from 0-100 showing if a stock is 'tired' from going up (>70) or down (<30) too much."
    },
    "support and resistance": {
        "term": "Support & Resistance",
        "definition": "Support is a price level where buying interest prevents further decline. Resistance is where selling pressure prevents further rise.",
        "why_important": "Stocks often bounce off support and retreat from resistance. Breaking these levels signals trend changes.",
        "simple_explanation": "Support = floor (price stops falling); Resistance = ceiling (price stops rising)."
    },
    "volume": {
        "term": "Trading Volume",
        "definition": "Volume is the number of shares traded in a given period. High volume confirms price moves; low volume suggests weak trends.",
        "why_important": "Price up + high volume = strong bullish signal. Price up + low volume = might be a fake move.",
        "simple_explanation": "How many shares changed hands today. More volume = more people agree on the price direction."
    },
    
    # Investment Concepts
    "bull market": {
        "term": "Bull Market",
        "definition": "A bull market is when stock prices rise 20% or more from recent lows, with general optimism and investor confidence.",
        "why_important": "Good time to hold growth stocks; however, be cautious of buying at peaks.",
        "simple_explanation": "When the market is charging upward like a bull attacking with its horns."
    },
    "bear market": {
        "term": "Bear Market",
        "definition": "A bear market is when stock prices fall 20% or more from recent highs, with widespread pessimism.",
        "why_important": "Potentially good time to buy quality stocks at discounts, but requires patience and strong conviction.",
        "simple_explanation": "When the market is swiping down like a bear's claw. Prices falling, people nervous."
    },
    "blue chip": {
        "term": "Blue Chip Stocks",
        "definition": "Large, well-established companies with a history of stable earnings and often dividend payments (e.g., Reliance, TCS, HDFC Bank in India).",
        "why_important": "Lower risk, steady returns. Good for conservative investors and long-term portfolios.",
        "simple_explanation": "The 'safe' stocks - big, famous companies that have been around for decades."
    },
    "diversification": {
        "term": "Diversification",
        "definition": "Spreading investments across different assets, sectors, and geographies to reduce risk. 'Don't put all eggs in one basket.'",
        "why_important": "If one investment fails, others may succeed, protecting your overall portfolio.",
        "simple_explanation": "Own different things (IT stocks + banks + gold) so if one crashes, you're not completely hurt."
    },
    "portfolio": {
        "term": "Portfolio",
        "definition": "A collection of all your investments - stocks, bonds, mutual funds, gold, real estate, etc.",
        "why_important": "Your portfolio's mix determines your risk and return. Review and rebalance periodically.",
        "simple_explanation": "Your investment 'basket' containing all the financial things you own."
    },
    "sip": {
        "term": "SIP (Systematic Investment Plan)",
        "definition": "A method to invest a fixed amount regularly (monthly/weekly) in mutual funds, regardless of market conditions.",
        "why_important": "Reduces timing risk through rupee-cost averaging. Best way for beginners to start investing.",
        "simple_explanation": "Auto-invest ₹5,000 every month. Buy more units when prices are low, fewer when high."
    },
    "mutual fund": {
        "term": "Mutual Fund",
        "definition": "A fund that pools money from many investors to invest in stocks, bonds, or other assets. Managed by professional fund managers.",
        "why_important": "Provides diversification even with small amounts. Good for investors who don't want to pick individual stocks.",
        "simple_explanation": "Many people put money together; an expert invests it for everyone. You get a small piece of a big basket."
    },
    "etf": {
        "term": "ETF (Exchange-Traded Fund)",
        "definition": "A fund that trades on stock exchanges like a regular stock. Often tracks an index (like NIFTY 50) with lower fees than mutual funds.",
        "why_important": "Low-cost way to get diversification. Can be bought/sold anytime during market hours.",
        "simple_explanation": "Like a mutual fund, but you can buy/sell it instantly on the stock exchange like a regular stock."
    },
    "nifty 50": {
        "term": "NIFTY 50",
        "definition": "India's benchmark stock index containing the top 50 companies by market cap listed on NSE. Represents ~65% of NSE's market cap.",
        "why_important": "If NIFTY goes up, the overall market sentiment is positive. Used as a benchmark to compare your returns.",
        "simple_explanation": "The 'top 50' companies in India. If NIFTY is up, generally the market is doing well."
    },
    "sensex": {
        "term": "SENSEX (BSE 30)",
        "definition": "India's oldest stock index from BSE, comprising 30 well-established and financially sound companies.",
        "why_important": "Like NIFTY, it's a barometer for the Indian market. Often quoted alongside NIFTY in news.",
        "simple_explanation": "The 'top 30' companies on the Bombay Stock Exchange. India's oldest stock index."
    },
    
    # Risk Terms
    "volatility": {
        "term": "Volatility",
        "definition": "How much and how quickly a stock's price changes. High volatility = big price swings; Low volatility = stable prices.",
        "why_important": "Higher volatility means higher risk but also higher potential returns. Match volatility to your risk tolerance.",
        "simple_explanation": "How 'jumpy' the stock price is. A volatile stock might go +5% one day and -4% the next."
    },
    "beta": {
        "term": "Beta",
        "definition": "Beta measures a stock's volatility relative to the market. Beta = 1 means moves with market; >1 = more volatile; <1 = less volatile.",
        "why_important": "High beta stocks amplify gains AND losses. Choose based on your risk appetite.",
        "simple_explanation": "If market goes up 10%, a stock with beta 1.5 might go up 15%. But it falls faster too."
    },
    "risk appetite": {
        "term": "Risk Appetite/Tolerance",
        "definition": "Your willingness and ability to handle investment losses. Depends on age, income stability, financial goals, and personality.",
        "why_important": "Invest according to your risk tolerance. Young = can take more risk; Near retirement = play it safe.",
        "simple_explanation": "How much loss can you sleep through without panicking? That's your risk appetite."
    },
    "stop loss": {
        "term": "Stop Loss",
        "definition": "An order to sell a stock automatically when it falls to a certain price, limiting your loss.",
        "why_important": "Protects you from big losses. Example: Buy at ₹100, set stop loss at ₹90 = max 10% loss.",
        "simple_explanation": "A safety net. 'If this stock drops below ₹90, sell it automatically to protect me.'"
    },
    
    # Types of Analysis
    "fundamental analysis": {
        "term": "Fundamental Analysis",
        "definition": "Evaluating a company based on financial statements, industry position, management quality, and economic factors to determine intrinsic value.",
        "why_important": "Helps find undervalued stocks for long-term investment. Warren Buffett uses this approach.",
        "simple_explanation": "Looking at a company's 'report card' - profits, debts, growth - to decide if it's worth buying."
    },
    "technical analysis": {
        "term": "Technical Analysis",
        "definition": "Studying historical price charts and trading volumes to predict future price movements using patterns and indicators.",
        "why_important": "Useful for timing entry/exit. Often used for short-term trading.",
        "simple_explanation": "Reading price charts like doctors read ECGs - looking for patterns to predict where price goes next."
    },
    
    # Order Types
    "limit order": {
        "term": "Limit Order",
        "definition": "An order to buy/sell at a specific price or better. Won't execute if market doesn't reach your price.",
        "why_important": "Gives you price control. Use when you're not in a hurry and want a specific price.",
        "simple_explanation": "\"I'll buy this stock, but ONLY if the price reaches ₹95 or lower.\""
    },
    "market order": {
        "term": "Market Order",
        "definition": "An order to buy/sell immediately at the current market price. Executes instantly but price might vary.",
        "why_important": "Use when you need to trade quickly and price isn't the priority.",
        "simple_explanation": "\"Buy this stock NOW at whatever price it's currently trading.\""
    },
    
    # IPO Related
    "ipo": {
        "term": "IPO (Initial Public Offering)",
        "definition": "When a private company first sells shares to the public on a stock exchange. The company 'goes public'.",
        "why_important": "Can offer good returns but also risky. Research thoroughly before investing in IPOs.",
        "simple_explanation": "A company's stock market debut. First time regular people can buy its shares."
    },
    "listing gain": {
        "term": "Listing Gain",
        "definition": "The profit when a stock's opening price on listing day is higher than its IPO issue price.",
        "why_important": "Not guaranteed - some IPOs list below issue price (listing loss). Past listing gains don't predict future.",
        "simple_explanation": "If you got IPO shares at ₹100 and they open at ₹120 on listing day, ₹20 is your listing gain."
    },
    
    # Behavioral Finance
    "fomo": {
        "term": "FOMO (Fear Of Missing Out)",
        "definition": "Anxiety that others are profiting from an investment you're not part of. Often leads to buying at peaks.",
        "why_important": "FOMO leads to emotional, poorly-timed decisions. Stick to your investment plan.",
        "simple_explanation": "That panic feeling when everyone's making money except you, making you buy without thinking."
    },
    "averaging down": {
        "term": "Averaging Down",
        "definition": "Buying more shares as price falls to lower your average purchase price.",
        "why_important": "Can be smart for good companies facing temporary issues. Dangerous for fundamentally weak stocks.",
        "simple_explanation": "Bought at ₹100, now it's ₹80. Buy more at ₹80 to average your price to ₹90."
    },
    
    # Indian Market Specific
    "nse": {
        "term": "NSE (National Stock Exchange)",
        "definition": "India's largest stock exchange by trading volume. Home to NIFTY 50 index. Ticker suffix: .NS",
        "why_important": "Most liquid exchange in India. Primary exchange for most retail investors.",
        "simple_explanation": "India's main stock exchange where you buy/sell shares. NIFTY is its main index."
    },
    "bse": {
        "term": "BSE (Bombay Stock Exchange)",
        "definition": "Asia's oldest stock exchange, located in Mumbai. Home to SENSEX index. Ticker suffix: .BO",
        "why_important": "Historical significance; SENSEX is often quoted in news alongside NIFTY.",
        "simple_explanation": "India's oldest stock exchange (since 1875). SENSEX is its famous index."
    },
    "sebi": {
        "term": "SEBI (Securities and Exchange Board of India)",
        "definition": "India's market regulator. Protects investor interests, regulates stock exchanges, and ensures fair markets.",
        "why_important": "Sets rules for brokers, mutual funds, and listed companies. Investor's protector.",
        "simple_explanation": "The 'police' for the stock market. Makes sure no one cheats you."
    },
    "demat account": {
        "term": "Demat Account",
        "definition": "An electronic account that holds your shares in digital form (dematerialized). Required to buy stocks in India.",
        "why_important": "Cannot trade stocks without it. Usually opened with broker along with trading account.",
        "simple_explanation": "Your digital locker where your shares are stored (instead of paper certificates)."
    },
    
    # Moat & ESG
    "moat": {
        "term": "Economic Moat",
        "definition": "A company's competitive advantage that protects it from competitors - like brand, patents, network effect, or cost leadership.",
        "why_important": "Companies with wide moats (like HDFC Bank, Asian Paints) tend to maintain profits for longer.",
        "simple_explanation": "What makes a company hard to beat? Coca-Cola's moat is its brand - you can't just copy that."
    },
    "esg": {
        "term": "ESG (Environmental, Social, Governance)",
        "definition": "A framework to evaluate companies on their environmental impact, social responsibility, and governance quality.",
        "why_important": "High ESG companies often have lower risk and better long-term returns. Growing importance for fund managers.",
        "simple_explanation": "Does the company care about the planet, its workers, and is it run honestly? That's ESG."
    },
    
    # More Common Terms
    "book value": {
        "term": "Book Value",
        "definition": "Book Value = Total Assets - Total Liabilities. It's what the company is 'worth' on paper if sold today.",
        "why_important": "If stock price is below book value (P/B < 1), it might be undervalued - or in trouble.",
        "simple_explanation": "If the company sold everything and paid all debts, book value is what's left."
    },
    "face value": {
        "term": "Face Value",
        "definition": "The original value of a share as stated in the company's charter (usually ₹10 or ₹1 in India). Not related to market price.",
        "why_important": "Used for calculating dividends and share splits. Don't confuse with market price.",
        "simple_explanation": "The 'official' value printed on the share certificate. Market price could be very different."
    },
    "bonus shares": {
        "term": "Bonus Shares",
        "definition": "Free additional shares given to existing shareholders (e.g., 1:1 bonus = for every share you own, get one free).",
        "why_important": "Your share count increases but price adjusts proportionally. Overall wealth remains same.",
        "simple_explanation": "Company gives you free shares! 1:1 bonus = your 100 shares become 200 shares."
    },
    "stock split": {
        "term": "Stock Split",
        "definition": "Dividing existing shares into multiple shares. A 2:1 split means 1 share becomes 2 (price halves proportionally).",
        "why_important": "Makes shares more affordable for retail investors. Total value remains same.",
        "simple_explanation": "Breaking one ₹1000 note into two ₹500 notes. You have more pieces but same total value."
    },
    "buyback": {
        "term": "Buyback",
        "definition": "When a company buys back its own shares from the market, reducing total shares outstanding.",
        "why_important": "Usually seen as positive - company thinks its stock is undervalued or has excess cash.",
        "simple_explanation": "Company: \"Our shares are so good, we're buying them back ourselves!\""
    },
    
    # Investor DNA Terms
    "investor dna": {
        "term": "Investor DNA (ELIDA Concept)",
        "definition": "Your unique investor profile combining risk tolerance, investment horizon, financial goals, and sector preferences. Used by ELIDA to personalize recommendations.",
        "why_important": "Not all stocks suit all investors. A 60-year-old needs different stocks than a 25-year-old.",
        "simple_explanation": "Your investing fingerprint - who you are as an investor. ELIDA uses this to find stocks that fit YOU."
    },
    "match score": {
        "term": "Match Score (ELIDA Metric)",
        "definition": "A 0-100 score showing how well a stock matches your Investor DNA. Higher = better fit for your profile.",
        "why_important": "A stock with 85% match score suits you better than one with 45%, even if both are 'buy' ratings.",
        "simple_explanation": "Like a compatibility score in a dating app, but for you and stocks. Higher = better match!"
    },
    "regret minimization": {
        "term": "Regret Minimization",
        "definition": "A decision framework asking: 'Will I regret NOT taking this chance?' or 'Will I regret losing this money?' Used by ELIDA's Regret Agent.",
        "why_important": "Helps make decisions you can live with, considering both upside and downside emotions.",
        "simple_explanation": "Before investing, ask: 'If this fails, can I handle the regret?' If no, invest less or skip."
    }
}

# Quick lookup aliases (case-insensitive matching)
ALIASES = {
    "price to earnings": "pe ratio",
    "price to earnings ratio": "pe ratio",
    "price-earnings": "pe ratio",
    "price earnings": "pe ratio",
    "what is pe": "pe ratio",
    "what is p/e": "pe ratio",
    "earnings per share": "eps",
    "return on equity": "roe",
    "price to book": "pb ratio",
    "price-to-book": "pb ratio",
    "d/e ratio": "debt to equity",
    "de ratio": "debt to equity",
    "marketcap": "market cap",
    "market capitalization": "market cap",
    "50 dma": "moving average",
    "200 dma": "moving average",
    "relative strength index": "rsi",
    "nifty": "nifty 50",
    "nifty50": "nifty 50",
    "bse30": "sensex",
    "bse 30": "sensex",
    "initial public offering": "ipo",
    "systematic investment plan": "sip",
    "exchange traded fund": "etf",
    "national stock exchange": "nse",
    "bombay stock exchange": "bse",
    "fear of missing out": "fomo",
    "environmental social governance": "esg",
    "volatility index": "vix",
    "fear index": "vix",
    "demat": "demat account"
}


def lookup_knowledge_base(query: str) -> dict | None:
    """
    Look up a query in the finance knowledge base.
    Returns the knowledge entry if found, None otherwise.
    """
    # Normalize query
    query_lower = query.lower().strip()
    
    # Remove common prefixes
    prefixes_to_remove = [
        "what is ", "what's ", "explain ", "define ", 
        "tell me about ", "what does ", " mean", "meaning of ",
        "what are ", "how does ", " work", "?"
    ]
    
    cleaned_query = query_lower
    for prefix in prefixes_to_remove:
        cleaned_query = cleaned_query.replace(prefix, "")
    cleaned_query = cleaned_query.strip()
    
    # Direct match
    if cleaned_query in FINANCE_KNOWLEDGE_BASE:
        return FINANCE_KNOWLEDGE_BASE[cleaned_query]
    
    # Alias match
    if cleaned_query in ALIASES:
        return FINANCE_KNOWLEDGE_BASE[ALIASES[cleaned_query]]
    
    # Partial match (word in query)
    for key in FINANCE_KNOWLEDGE_BASE:
        if key in cleaned_query or cleaned_query in key:
            return FINANCE_KNOWLEDGE_BASE[key]
    
    # Check aliases for partial match
    for alias, key in ALIASES.items():
        if alias in cleaned_query:
            return FINANCE_KNOWLEDGE_BASE[key]
    
    return None


def format_knowledge_response(entry: dict) -> str:
    """
    Format a knowledge base entry into a human-readable response.
    """
    response = f"**{entry['term']}**\n\n"
    response += f"📖 **Definition:** {entry['definition']}\n\n"
    response += f"💡 **Why It's Important:** {entry['why_important']}\n\n"
    response += f"🎯 **Simple Explanation:** {entry['simple_explanation']}"
    return response
