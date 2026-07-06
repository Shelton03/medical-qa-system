"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Loader2, User, Bot, Sparkles } from "lucide-react";
import { aiApi } from "@/lib/api";
import type { AIMessageResponse } from "@/lib/types";

interface AIChatPanelProps {
  sessionId: string;
  patientId?: string;
  initialMessages?: AIMessageResponse[];
}

type ChatMessage = AIMessageResponse & { isStreaming?: boolean };

export function AIChatPanel({ sessionId, patientId, initialMessages = [] }: AIChatPanelProps): React.ReactElement {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent, scrollToBottom]);

  useEffect(() => {
    if (initialMessages.length > 0) {
      setMessages(initialMessages);
    }
  }, [initialMessages]);

  const handleSend = useCallback(async () => {
    const trimmed = input.trim();
    if (!trimmed || isTyping) return;

    const userMessage: ChatMessage = {
      id: `temp-${Date.now()}`,
      session_id: sessionId,
      role: "user",
      content: trimmed,
      model_name: null,
      token_count: null,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);
    setStreamingContent("");

    try {
      const streamBuffer: string[] = [];
      await aiApi.sendMessageStream(sessionId, trimmed, (chunk) => {
        streamBuffer.push(chunk);
        setStreamingContent(streamBuffer.join(""));
      });

      // Once streaming completes, add the full AI message
      const fullContent = streamBuffer.join("");
      if (fullContent) {
        setMessages((prev) => [
          ...prev,
          {
            id: `ai-${Date.now()}`,
            session_id: sessionId,
            role: "assistant",
            content: fullContent,
            model_name: null,
            token_count: null,
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          session_id: sessionId,
          role: "assistant",
          content: "I'm sorry, I encountered an error processing your request. Please try again.",
          model_name: null,
          token_count: null,
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsTyping(false);
      setStreamingContent("");
    }
  }, [input, isTyping, sessionId]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestion = (suggestion: string) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-card border border-border overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-stellarWhite">
        <div className="w-8 h-8 rounded-full bg-celestialBlue/10 flex items-center justify-center">
          <Bot className="w-4 h-4 text-celestialBlue" />
        </div>
        <div>
          <p className="text-sm font-semibold text-mirageBlack">AI Clinical Assistant</p>
          <p className="text-[11px] text-clinicalGrey">{patientId ? `Patient session #${sessionId.slice(0, 8)}` : `Session #${sessionId.slice(0, 8)}`}</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin">
        <AnimatePresence mode="popLayout">
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              layout
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role !== "user" && (
                <div className="w-7 h-7 rounded-full bg-celestialBlue/10 flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="w-3.5 h-3.5 text-celestialBlue" />
                </div>
              )}
              <div
                className={`max-w-[80%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-mirageBlack text-white rounded-br-md"
                    : "bg-secondary text-mirageBlack rounded-bl-md"
                }`}
              >
                {msg.content}
                {msg.role === "assistant" && (
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    <SuggestionChip onClick={() => handleSuggestion("Can you explain your reasoning?")}>
                      Explain
                    </SuggestionChip>
                    <SuggestionChip onClick={() => handleSuggestion("What else should I consider?")}>
                      Follow-up
                    </SuggestionChip>
                    <SuggestionChip onClick={() => handleSuggestion("Generate a clinical summary.")}>
                      Summary
                    </SuggestionChip>
                  </div>
                )}
              </div>
              {msg.role === "user" && (
                <div className="w-7 h-7 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0 mt-0.5">
                  <User className="w-3.5 h-3.5 text-mirageBlack" />
                </div>
              )}
            </motion.div>
          ))}

          {/* Streaming indicator */}
          {isTyping && streamingContent && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3"
            >
              <div className="w-7 h-7 rounded-full bg-celestialBlue/10 flex items-center justify-center shrink-0 mt-0.5">
                <Bot className="w-3.5 h-3.5 text-celestialBlue" />
              </div>
              <div className="max-w-[80%] px-4 py-2.5 rounded-2xl rounded-bl-md bg-secondary text-mirageBlack text-sm leading-relaxed">
                {streamingContent}
                <span className="inline-block w-1.5 h-3.5 ml-0.5 bg-celestialBlue animate-pulse rounded-sm" />
              </div>
            </motion.div>
          )}

          {/* Typing indicator while waiting for first chunk */}
          {isTyping && !streamingContent && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3"
            >
              <div className="w-7 h-7 rounded-full bg-celestialBlue/10 flex items-center justify-center shrink-0">
                <Loader2 className="w-3.5 h-3.5 text-celestialBlue animate-spin" />
              </div>
              <div className="px-4 py-2.5 rounded-2xl rounded-bl-md bg-secondary text-clinicalGrey text-sm flex items-center gap-2">
                <span>AI is thinking</span>
                <span className="flex gap-0.5">
                  <span className="w-1 h-1 bg-clinicalGrey rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-1 h-1 bg-clinicalGrey rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-1 h-1 bg-clinicalGrey rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-3 border-t border-border bg-white">
        <div className="flex items-end gap-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask the AI assistant..."
            rows={1}
            className="flex-1 min-h-[40px] max-h-32 px-3 py-2.5 rounded-input bg-secondary text-sm text-mirageBlack placeholder:text-clinicalGrey focus:outline-none focus:ring-2 focus:ring-celestialBlue/20 resize-none scrollbar-thin"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="p-2.5 rounded-button bg-mirageBlack text-white hover:bg-mirageBlack/90 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            aria-label="Send message"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

function SuggestionChip({ children, onClick }: { children: React.ReactNode; onClick: () => void }): React.ReactElement {
  return (
    <button
      onClick={onClick}
      className="inline-flex items-center gap-1 px-2 py-1 text-[10px] font-medium rounded-full bg-celestialBlue/5 text-celestialBlue hover:bg-celestialBlue/10 transition-colors border border-celestialBlue/10"
    >
      <Sparkles className="w-2.5 h-2.5" />
      {children}
    </button>
  );
}
