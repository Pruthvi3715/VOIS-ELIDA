import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, AlertTriangle, TrendingUp, HelpCircle, X, MessageCircle } from 'lucide-react';

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
 * Chatbot Interface Component - Dark Theme
 * Floating, collapsible widget matching ELIDA theme
 */
function Chatbot({ analysisData, assetId }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

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
        // Optional: Auto-send
        // handleSend();
    };

    const generateResponse = async (question, data, asset) => {
        // 1. If we have context data, try to answer from it locally first (simple heuristic)
        // OR just send everything to backend.
        // Given complexity, let's try local heuristics for Data first, then fallback to backend Chat (Qwen/Google)

        const q = question.toLowerCase();

        // Use local heuristics ONLY if we have data AND the question matches specific patterns
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

        // 2. Fallback to Backend General Chat (which now includes Qwen -> Google)
        try {
            // Construct a context-aware query if possible
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
            {/* Chat Window - Dark Theme */}
            {isOpen && (
                <div className="w-96 h-[600px] bg-surface rounded-2xl shadow-glass-lg border border-glass-border flex flex-col overflow-hidden animate-fade-in origin-bottom-right transition-all backdrop-blur-xl">
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
                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-1.5 hover:bg-white/10 rounded-lg transition-colors"
                        >
                            <X className="w-5 h-5 text-white/70 hover:text-white" />
                        </button>
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
