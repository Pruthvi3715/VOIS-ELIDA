import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, AlertTriangle, TrendingUp, HelpCircle, X, MessageCircle } from 'lucide-react';

/**
 * Chat Message Component
 */
function ChatMessage({ message, isBot, isLoading }) {
    return (
        <div className={`flex gap-3 ${isBot ? '' : 'flex-row-reverse'}`}>
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isBot ? 'bg-blue-100' : 'bg-gray-100'
                }`}>
                {isBot ? (
                    <Bot className="w-4 h-4 text-blue-600" />
                ) : (
                    <User className="w-4 h-4 text-gray-600" />
                )}
            </div>

            {/* Message */}
            <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${isBot
                ? 'bg-white border border-gray-100 shadow-sm'
                : 'bg-blue-600 text-white'
                }`}>
                {isLoading ? (
                    <div className="flex items-center gap-2 text-gray-500">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Analyzing...</span>
                    </div>
                ) : (
                    <div className="text-sm whitespace-pre-wrap">{message}</div>
                )}
            </div>
        </div>
    );
}

/**
 * Quick Action Button
 */
function QuickAction({ icon, label, onClick }) {
    return (
        <button
            onClick={onClick}
            className="flex items-center gap-2 px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors border border-gray-100 whitespace-nowrap"
        >
            {icon}
            {label}
        </button>
    );
}

/**
 * Chatbot Interface Component
 * Floating, collapsible widget
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
            {/* Chat Window */}
            {isOpen && (
                <div className="w-96 h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden animate-fade-in-up origin-bottom-right transition-all">
                    {/* Header */}
                    <div className="bg-gray-900 text-white px-4 py-3 flex items-center justify-between shadow-sm">
                        <div className="flex items-center gap-3">
                            <div className="bg-white/10 p-2 rounded-lg">
                                <Bot className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-sm">AI Financial Assistant</h3>
                                <p className="text-gray-400 text-xs flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                                    {analysisData ? `Focus: ${assetId}` : 'Online'}
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-1.5 hover:bg-white/10 rounded-lg transition-colors"
                        >
                            <X className="w-5 h-5 text-gray-400" />
                        </button>
                    </div>

                    {/* Quick Actions (if context exists) */}
                    {analysisData && (
                        <div className="px-4 py-3 bg-gray-50 border-b border-gray-100 flex gap-2 overflow-x-auto scrollbar-hide">
                            <QuickAction icon={<AlertTriangle className="w-3 h-3" />} label="Risks" onClick={() => handleQuickAction("What are the main risks?")} />
                            <QuickAction icon={<TrendingUp className="w-3 h-3" />} label="Entry?" onClick={() => handleQuickAction("Is this a good entry point?")} />
                            <QuickAction icon={<HelpCircle className="w-3 h-3" />} label="Score?" onClick={() => handleQuickAction("Explain expected performance")} />
                        </div>
                    )}

                    {/* Messages Area */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
                        {messages.map((msg, idx) => (
                            <ChatMessage key={idx} message={msg.text} isBot={msg.isBot} />
                        ))}
                        {isLoading && <ChatMessage isBot isLoading />}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-4 bg-white border-t border-gray-100">
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Ask a question..."
                                className="flex-1 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-gray-200 focus:bg-white transition-all"
                            />
                            <button
                                onClick={handleSend}
                                disabled={!input.trim() || isLoading}
                                className="p-2.5 bg-gray-900 text-white rounded-xl hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-105 ${isOpen ? 'bg-gray-700 rotate-90' : 'bg-gray-900 hover:bg-black'
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
