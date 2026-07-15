"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Loader2, User, Bot, Sparkles, Mic } from "lucide-react";
import { aiApi, doctorApi } from "@/lib/api";
import { useVoiceRecorder } from "@/hooks/useVoiceRecorder";
import { useToast } from "@/hooks/useToast";
import type { AIMessageResponse } from "@/lib/types";

interface AIChatPanelProps {
  sessionId: string;
  patientId?: string;
  visitId?: string;
  initialMessages?: AIMessageResponse[];
}

type ChatMessage = AIMessageResponse & { isStreaming?: boolean };

/** Simple audio waveform bars. */
function Waveform({ active }: { active: boolean }): React.ReactElement {
  return (
    <div className="flex items-center gap-0.5 h-4">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={
            active
              ? {
                  height: [4, 12, 6, 14, 4],
                }
              : { height: 4 }
          }
          transition={{
            duration: 0.6,
            repeat: Infinity,
            repeatType: "reverse",
            delay: i * 0.15,
          }}
          className="w-0.5 bg-red-400 rounded-full"
        />
      ))}
    </div>
  );
}

export function AIChatPanel({
  sessionId,
  patientId,
  visitId,
  initialMessages = [],
}: AIChatPanelProps): React.ReactElement {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [finalTranscript, setFinalTranscript] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const { showToast } = useToast();

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

  const handleSendMessage = useCallback(
    async (content: string) => {
      const trimmed = content.trim();
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
    },
    [isTyping, sessionId]
  );

  const handleSend = useCallback(() => {
    handleSendMessage(input);
  }, [input, handleSendMessage]);

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

  // ---------------------------------------------------------------------
  // Voice Recorder integration
  // ---------------------------------------------------------------------
  const onTranscript = useCallback(
    async (text: string) => {
      setFinalTranscript(text);
      // Auto-send the transcript as a chat message
      await handleSendMessage(text);
      // Also persist to the visit record if visitId is available
      if (visitId) {
        try {
          await doctorApi.updateVisitTranscript(visitId, text);
        } catch {
          // Silently ignore persistence errors — the transcript is still in chat
        }
      }
    },
    [handleSendMessage, visitId]
  );

  const { recording, liveText, startRecording, stopRecording } =
    useVoiceRecorder(onTranscript);

  // Show live transcript in input while recording
  useEffect(() => {
    if (recording && liveText) {
      setInput(liveText);
    }
  }, [recording, liveText]);

  const toggleRecording = useCallback(() => {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  }, [recording, startRecording, stopRecording]);

  return (
    <div className="flex flex-col h-full bg-white rounded-card border border-border overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-stellarWhite">
        <div className="w-8 h-8 rounded-full bg-celestialBlue/10 flex items-center justify-center">
          <Bot className="w-4 h-4 text-celestialBlue" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-mirageBlack">AI Clinical Assistant</p>
          <p className="text-[11px] text-clinicalGrey">
            {patientId ? `Patient session #${sessionId.slice(0, 8)}` : `Session #${sessionId.slice(0, 8)}`}
          </p>
        </div>
        {recording && (
          <div className="flex items-center gap-1.5 shrink-0">
            <Waveform active={recording} />
            <span className="text-[10px] font-medium text-red-500">Recording</span>
            <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
          </div>
        )}
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
          {/* Mic button */}
          <button
            onClick={toggleRecording}
            className={`p-2.5 rounded-button transition-colors shrink-0 ${
              recording
                ? "bg-red-500 text-white hover:bg-red-600"
                : "bg-secondary text-clinicalGrey hover:bg-clinicalGrey/20"
            }`}
            aria-label={recording ? "Stop recording" : "Start voice recording"}
            title={recording ? "Stop recording" : "Start voice recording"}
          >
            <Mic className={`w-4 h-4 ${recording ? "animate-pulse" : ""}`} />
          </button>
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={recording ? "Recording… speak now" : "Ask the AI assistant…"}
            rows={1}
            className={`flex-1 min-h-[40px] max-h-32 px-3 py-2.5 rounded-input text-sm transition-colors resize-none scrollbar-thin ${
              recording
                ? "bg-red-50 text-mirageBlack placeholder:text-red-400 focus:ring-2 focus:ring-red-500/20 border border-red-200"
                : "bg-secondary text-mirageBlack placeholder:text-clinicalGrey focus:ring-2 focus:ring-celestialBlue/20"
            }`}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="p-2.5 rounded-button bg-mirageBlack text-white hover:bg-mirageBlack/90 transition-colors disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
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
