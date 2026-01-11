import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, AlertTriangle, TrendingUp, HelpCircle, X, MessageCircle, Maximize2, Minimize2 } from 'lucide-react';

/**
 * Chat Message Component - Dark Theme
 */
function ChatMessage({ message, isBot, isLoading }) {
    return (
        <div className={`flex gap-3 ${isBot ? '' : 'flex-row-reverse'}`}>
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 border ${isBot
                ? 'bg-gradient-to-br from-primary-500/20 to-accent-dark/20 border-primary-500/30'
                : 'bg-gradient-to-br from-amber-500/20 to-orange-500/20 border-amber-500/30'
                }`}>
                {isBot ? (
                    <Bot className="w-4 h-4 text-primary-400" />
                ) : (
                    <User className="w-4 h-4 text-amber-400" />
                )}
            </div>

            {/* Message */}
            <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${isBot
                ? 'bg-surface-light/80 border border-glass-border text-gray-200'
                : 'bg-gradient-to-r from-primary-600 to-accent-dark text-white'
                }`}>
                {isLoading ? (
                    <div className="flex items-center gap-2 text-gray-400">
                        <Loader2 className="w-4 h-4 animate-spin text-primary-400" />
                        <span>Analyzing...</span>
                    </div>
                ) : (
                    <div className="text-sm whitespace-pre-wrap leading-relaxed">{message}</div>
                )}
            </div>
        </div>
    );
}

/**
 * Quick Action Button - Dark Theme
 */
function QuickAction({ icon, label, onClick }) {
    return (
        <button
            onClick={onClick}
            className="flex items-center gap-2 px-3 py-2 bg-surface-light/50 hover:bg-surface-light rounded-lg text-sm text-gray-300 hover:text-white transition-all border border-glass-border hover:border-primary-500/30 whitespace-nowrap"
        >
            {icon}
            {label}
        </button>
    );
}

/**
 * Chatbot Interface Component - Dark Theme with Resizable Window
 * Floating, collapsible widget matching ELIDA theme
 */
function Chatbot({ analysisData, assetId }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [size, setSize] = useState({ width: 384, height: 600 }); // Default: w-96 = 384px
    const [isResizing, setIsResizing] = useState(false);
    const messagesEndRef = useRef(null);
    const chatRef = useRef(null);

    // Size constraints
    const MIN_WIDTH = 320;
    const MAX_WIDTH = 600;
    const MIN_HEIGHT = 400;
    const MAX_HEIGHT = 800;

    // Initial Greeting
    useEffect(() => {
        if (isOpen && messages.length === 0) {
            if (analysisData) {
                const greeting = generateGreeting(analysisData, assetId);
                setMessages([{ text: greeting, isBot: true }]);
            } else {
                setMessages([{ text: "👋 Hi! I'm your AI Financial Assistant. Ask me anything about finance, or search for a stock analysis.", isBot: true }]);
            }
        }
    }, [isOpen, analysisData, assetId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const generateGreeting = (data, asset) => {
        const matchScore = data?.match_result?.score || data?.match_score || 'N/A';
        const recommendation = data?.match_result?.recommendation || 'Hold';

        let greeting = `👋 Hi! I've analyzed **${asset}**.\n`;
        greeting += `📊 Match Score: ${matchScore}%\n`;
        greeting += `💡 Recommendation: ${recommendation}\n\n`;
        greeting += `Ask me about valuation, risks, or specific metrics!`;
        return greeting;
    };

    // Resize handlers
    const handleResizeStart = (e) => {
        e.preventDefault();
        setIsResizing(true);

        const startX = e.clientX;
        const startY = e.clientY;
        const startWidth = size.width;
        const startHeight = size.height;

        const handleMouseMove = (moveEvent) => {
            const deltaX = startX - moveEvent.clientX; // Inverted for top-left corner
            const deltaY = startY - moveEvent.clientY;

            const newWidth = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, startWidth + deltaX));
            const newHeight = Math.min(MAX_HEIGHT, Math.max(MIN_HEIGHT, startHeight + deltaY));

            setSize({ width: newWidth, height: newHeight });
        };

        const handleMouseUp = () => {
            setIsResizing(false);
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };

        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    };

    const toggleExpand = () => {
        if (isExpanded) {
            setSize({ width: 384, height: 600 });
        } else {
            setSize({ width: MAX_WIDTH, height: MAX_HEIGHT });
        }
        setIsExpanded(!isExpanded);
    };

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { text: userMessage, isBot: false }]);
        setIsLoading(true);

        try {
            const response = await generateResponse(userMessage, analysisData, assetId);
            setMessages(prev => [...prev, { text: response, isBot: true }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                text: "Sorry, I encountered an error. Please try again.",
                isBot: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleQuickAction = (question) => {
        setInput(question);
    };

    const generateResponse = async (question, data, asset) => {
        const q = question.toLowerCase();

        // Learning-related quick responses
        if (q.includes('p/e') || q.includes('pe ratio') || q.includes('price to earnings')) {
            return `**P/E Ratio (Price-to-Earnings)**\n\nIt's the stock price divided by earnings per share.\n\n📊 **How to interpret:**\n- Lower P/E = potentially cheaper (but investigate why)\n- Higher P/E = market expects growth\n- Compare within same industry\n\n💡 Visit the **Learn** section for more!`;
        }

        if (q.includes('market cap') || q.includes('marketcap')) {
            return `**Market Cap (Market Capitalization)**\n\nTotal company value = Share Price × Total Shares\n\n📊 **Categories:**\n- Large Cap: >₹20,000 Cr (stable)\n- Mid Cap: ₹5,000-20,000 Cr (growth potential)\n- Small Cap: <₹5,000 Cr (higher risk/reward)\n\n💡 Check the **Learn** section for more!`;
        }

        if (q.includes('what is') && (q.includes('beta') || q.includes('volatility'))) {
            return `**Beta (Volatility Measure)**\n\nMeasures how much a stock moves vs the market.\n\n📊 **How to read:**\n- Beta = 1: Moves with market\n- Beta > 1: More volatile (risky but higher potential)\n- Beta < 1: Less volatile (defensive)\n\n💡 Visit **Learn** for more terms!`;
        }

        if (q.includes('learn') || q.includes('tutorial') || q.includes('beginner') || q.includes('how to invest')) {
            return `🎓 **Want to Learn?**\n\nCheck out our **Learn** section in the sidebar! It includes:\n\n📚 Free courses (Zerodha Varsity, Khan Academy)\n📹 YouTube channels\n📖 Book recommendations\n🔤 Quick term definitions\n\n**Click "Learn" in the menu to explore!**`;
        }

        if (data && asset) {
            const financials = data?.market_data || {};
            const results = data?.results || {};

            if (q.includes('risk')) {
                const risk = results.regret?.output?.risk_level || 'Unknown';
                return `The calculated risk level for ${asset} is **${risk}**.\n\n` +
                    (results.regret?.output?.justification || '');
            }
            if (q.includes('score')) {
                return `The match score is **${data.match_result?.score}%**.\nFit: ${data.match_result?.fit_reasons?.join(', ')}`;
            }
        }

        try {
            let finalQuery = question;
            if (asset && data) {
                finalQuery = `Context: Analyzing ${asset}. User Question: ${question}`;
            }

            const res = await fetch('http://localhost:8000/chat/general', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: finalQuery })
            });
            const json = await res.json();
            return json.response;
        } catch (e) {
            console.error(e);
            return "I'm having trouble connecting to the server.";
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-4 font-sans">
            {/* Chat Window - Dark Theme with Resizable */}
            {isOpen && (
                <div
                    ref={chatRef}
                    style={{ width: size.width, height: size.height }}
                    className={`bg-surface rounded-2xl shadow-glass-lg border border-glass-border flex flex-col overflow-hidden animate-fade-in origin-bottom-right backdrop-blur-xl ${isResizing ? 'select-none' : 'transition-all'}`}
                >
                    {/* Resize Handle - Top Left Corner */}
                    <div
                        onMouseDown={handleResizeStart}
                        className="absolute top-0 left-0 w-4 h-4 cursor-nwse-resize z-10 group"
                        title="Drag to resize"
                    >
                        <div className="absolute top-1 left-1 w-2 h-2 border-t-2 border-l-2 border-gray-500 group-hover:border-primary-400 transition-colors rounded-tl" />
                    </div>

                    {/* Header - Gradient */}
                    <div className="bg-gradient-to-r from-primary-600/90 to-accent-dark/90 text-white px-4 py-3 flex items-center justify-between shadow-lg backdrop-blur-sm">
                        <div className="flex items-center gap-3">
                            <div className="bg-white/10 p-2 rounded-lg border border-white/10">
                                <Bot className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-sm">ELIDA Assistant</h3>
                                <p className="text-white/70 text-xs flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></span>
                                    {analysisData ? `Focus: ${assetId}` : 'Online'}
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center gap-1">
                            {/* Expand/Collapse Button */}
                            <button
                                onClick={toggleExpand}
                                className="p-1.5 hover:bg-white/10 rounded-lg transition-colors"
                                title={isExpanded ? "Minimize" : "Maximize"}
                            >
                                {isExpanded ? (
                                    <Minimize2 className="w-4 h-4 text-white/70 hover:text-white" />
                                ) : (
                                    <Maximize2 className="w-4 h-4 text-white/70 hover:text-white" />
                                )}
                            </button>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-1.5 hover:bg-white/10 rounded-lg transition-colors"
                            >
                                <X className="w-5 h-5 text-white/70 hover:text-white" />
                            </button>
                        </div>
                    </div>

                    {/* Quick Actions (if context exists) - Dark Theme */}
                    {analysisData && (
                        <div className="px-4 py-3 bg-surface-light/50 border-b border-glass-border flex gap-2 overflow-x-auto scrollbar-hide">
                            <QuickAction icon={<AlertTriangle className="w-3 h-3 text-warning" />} label="Risks" onClick={() => handleQuickAction("What are the main risks?")} />
                            <QuickAction icon={<TrendingUp className="w-3 h-3 text-success" />} label="Entry?" onClick={() => handleQuickAction("Is this a good entry point?")} />
                            <QuickAction icon={<HelpCircle className="w-3 h-3 text-primary-400" />} label="Score?" onClick={() => handleQuickAction("Explain expected performance")} />
                        </div>
                    )}

                    {/* Messages Area - Dark Theme */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-background/50">
                        {messages.map((msg, idx) => (
                            <ChatMessage key={idx} message={msg.text} isBot={msg.isBot} />
                        ))}
                        {isLoading && <ChatMessage isBot isLoading />}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area - Dark Theme */}
                    <div className="p-4 bg-surface border-t border-glass-border">
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Ask a question..."
                                className="flex-1 px-4 py-2.5 bg-surface-light border border-glass-border rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500/50 transition-all"
                            />
                            <button
                                onClick={handleSend}
                                disabled={!input.trim() || isLoading}
                                className="p-2.5 bg-gradient-to-r from-primary-600 to-accent-dark text-white rounded-xl hover:shadow-glow disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-105"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                    </div>

                    {/* Size indicator while resizing */}
                    {isResizing && (
                        <div className="absolute bottom-2 left-2 text-xs text-gray-500 bg-surface-light/80 px-2 py-1 rounded">
                            {size.width} × {size.height}
                        </div>
                    )}
                </div>
            )}

            {/* Toggle Button - Gradient */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`w-14 h-14 rounded-full shadow-glow flex items-center justify-center transition-all duration-300 hover:scale-110 ${isOpen
                    ? 'bg-surface-light border border-glass-border rotate-90'
                    : 'bg-gradient-to-r from-primary-600 to-accent-dark hover:shadow-glow-lg'
                    }`}
            >
                {isOpen ? (
                    <X className="w-6 h-6 text-white" />
                ) : (
                    <MessageCircle className="w-7 h-7 text-white" />
                )}
            </button>
        </div>
    );
}

export default Chatbot;

