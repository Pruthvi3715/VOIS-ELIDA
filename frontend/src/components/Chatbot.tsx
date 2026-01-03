import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, X, MessageCircle, Sparkles, Maximize2, Minimize2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

interface Message {
    text: string;
    isBot: boolean;
    timestamp: Date;
}

const Chatbot: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        { text: "Hello! I'm your AI Investment Assistant. How can I help you analyze the market today?", isBot: true, timestamp: new Date() }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { text: userMessage, isBot: false, timestamp: new Date() }]);
        setIsLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/chat/general', {
                query: userMessage
            });

            const botResponse = response.data.response || "I couldn't process that request.";
            setMessages(prev => [...prev, { text: botResponse, isBot: true, timestamp: new Date() }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                text: "I'm having trouble connecting to the server. Please try again later.",
                isBot: true,
                timestamp: new Date()
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={`fixed z-50 transition-all duration-300 ${isExpanded
                ? 'bottom-0 right-0 w-full h-full md:w-[600px] md:h-[80vh] md:bottom-6 md:right-6'
                : 'bottom-6 right-6 flex flex-col items-end gap-4'
            }`}>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        className={`glass-card flex flex-col overflow-hidden shadow-2xl border border-glass-border bg-[#0f111a]/95 backdrop-blur-xl ${isExpanded ? 'w-full h-full rounded-none md:rounded-2xl' : 'w-[400px] h-[600px] rounded-2xl'
                            }`}
                    >
                        {/* Header */}
                        <div className="bg-gradient-to-r from-primary-900/50 to-primary-800/50 px-5 py-4 flex items-center justify-between border-b border-white/5 backdrop-blur-md">
                            <div className="flex items-center gap-3">
                                <div className="bg-gradient-primary p-2 rounded-xl shadow-glow">
                                    <Bot className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-white text-base tracking-wide">AI Advisor</h3>
                                    <div className="flex items-center gap-1.5">
                                        <span className="w-1.5 h-1.5 rounded-full bg-success shadow-[0_0_8px_rgba(34,197,94,0.6)] animate-pulse"></span>
                                        <span className="text-gray-400 text-xs font-medium">Online</span>
                                    </div>
                                </div>
                            </div>
                            <div className="flex items-center gap-1">
                                <button
                                    onClick={() => setIsExpanded(!isExpanded)}
                                    className="p-2 hover:bg-white/5 rounded-lg transition-colors text-gray-400 hover:text-white"
                                >
                                    {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                                </button>
                                <button
                                    onClick={() => setIsOpen(false)}
                                    className="p-2 hover:bg-white/5 rounded-lg transition-colors text-gray-400 hover:text-white"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>
                        </div>

                        {/* Messages Area */}
                        <div className="flex-1 overflow-y-auto p-5 space-y-5 bg-gradient-to-b from-transparent to-black/20">
                            {messages.map((msg, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`flex gap-4 ${msg.isBot ? '' : 'flex-row-reverse'}`}
                                >
                                    <div className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg ${msg.isBot
                                            ? 'bg-gradient-to-br from-indigo-500/20 to-violet-500/20 border border-indigo-500/30'
                                            : 'bg-surface-light border border-glass-border'
                                        }`}>
                                        {msg.isBot ? (
                                            <Sparkles className="w-4 h-4 text-primary-400" />
                                        ) : (
                                            <User className="w-4 h-4 text-gray-400" />
                                        )}
                                    </div>
                                    <div className="flex flex-col gap-1 max-w-[80%]">
                                        <div className={`rounded-2xl px-5 py-3 text-[14px] leading-relaxed shadow-sm ${msg.isBot
                                                ? 'bg-[#1a1b26] border border-white/5 text-gray-200 rounded-tl-none'
                                                : 'bg-gradient-primary text-white rounded-tr-none shadow-glow-sm'
                                            }`}>
                                            {msg.text}
                                        </div>
                                        <span className={`text-[10px] text-gray-500 ${msg.isBot ? 'pl-2' : 'pr-2 text-right'}`}>
                                            {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>
                                </motion.div>
                            ))}
                            {isLoading && (
                                <div className="flex gap-4">
                                    <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 bg-gradient-to-br from-indigo-500/20 to-violet-500/20 border border-indigo-500/30">
                                        <Sparkles className="w-4 h-4 text-primary-400" />
                                    </div>
                                    <div className="bg-[#1a1b26] border border-white/5 rounded-2xl rounded-tl-none px-5 py-4 flex items-center gap-2">
                                        <span className="w-1.5 h-1.5 bg-primary-400/50 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                                        <span className="w-1.5 h-1.5 bg-primary-400/50 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                                        <span className="w-1.5 h-1.5 bg-primary-400/50 rounded-full animate-bounce"></span>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="p-4 bg-[#0f111a] border-t border-glass-border">
                            <div className="flex gap-3 relative bg-surface-light/30 rounded-xl p-1.5 border border-white/5 focus-within:border-primary-500/50 focus-within:bg-surface-light/50 transition-all duration-300">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                    placeholder="Ask anything about finance..."
                                    className="flex-1 bg-transparent px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none"
                                />
                                <button
                                    onClick={handleSend}
                                    disabled={!input.trim() || isLoading}
                                    className="p-2.5 bg-gradient-primary rounded-lg text-white shadow-glow disabled:opacity-50 disabled:shadow-none hover:scale-105 active:scale-95 transition-all"
                                >
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                            <div className="text-center mt-2">
                                <p className="text-[10px] text-gray-600">
                                    AI provides investment insights, not financial advice.
                                </p>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Toggle Button */}
            {!isExpanded && (
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setIsOpen(!isOpen)}
                    className={`w-16 h-16 rounded-full shadow-[0_0_20px_rgba(99,102,241,0.3)] flex items-center justify-center transition-all duration-300 border border-white/10 ${isOpen
                            ? 'bg-[#1a1b26] text-gray-400 rotate-90 hover:text-white'
                            : 'bg-gradient-primary text-white shadow-glow-lg'
                        }`}
                >
                    {isOpen ? (
                        <X className="w-7 h-7" />
                    ) : (
                        <MessageCircle className="w-8 h-8" />
                    )}
                </motion.button>
            )}
        </div>
    );
};

export default Chatbot;
