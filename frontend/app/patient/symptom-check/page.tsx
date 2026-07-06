"use client";

import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  Send,
  Bot,
  User,
  Loader2,
  Sparkles,
  CircleStop,
  Activity,
  ChevronRight,
} from "lucide-react";
import { aiApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";

interface ChatMessage {
  id: string;
  role: "user" | "ai";
  content: string;
  timestamp: Date;
}

export default function PatientSymptomCheckPage(): React.ReactElement {
  const { showToast } = useToast();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isAiTyping, setIsAiTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isAiTyping]);

  const createSessionMutation = useMutation({
    mutationFn: () => aiApi.createSession(),
    onSuccess: (session) => {
      setSessionId(session.id);
      setMessages([
        {
          id: "welcome",
          role: "ai",
          content:
            "Hello! I am your AI symptom checker. Please tell me what symptoms you are experiencing, and I will guide you through some questions.",
          timestamp: new Date(),
        },
      ]);
      showToast({
        title: "Session started",
        message: "Your AI assessment session has started.",
        type: "success",
      });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to start session";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const sendMessageMutation = useMutation({
    mutationFn: async (content: string) => {
      if (!sessionId) throw new Error("No active session");
      return aiApi.sendMessage(sessionId, content);
    },
    onMutate: () => {
      setIsAiTyping(true);
    },
    onSuccess: (response) => {
      setMessages((prev) => [
        ...prev,
        {
          id: `ai-${response.id}`,
          role: "ai",
          content: response.content,
          timestamp: new Date(response.created_at),
        },
      ]);
      setIsAiTyping(false);
    },
    onError: (err: unknown) => {
      setIsAiTyping(false);
      const msg = err instanceof Error ? err.message : "Failed to get AI response";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || sendMessageMutation.isPending || isAiTyping) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    const text = input.trim();
    setInput("");
    sendMessageMutation.mutate(text);
  };

  const handleEndSession = () => {
    setSessionId(null);
    setMessages([]);
    setInput("");
    setIsAiTyping(false);
    showToast({
      title: "Session ended",
      message: "Your symptom check session has been ended.",
      type: "info",
    });
  };

  const suggestedQuestions = [
    "I have a headache and fever",
    "My chest feels tight when I breathe",
    "I have a rash on my arm",
  ];

  return (
    <div className="flex flex-col h-full pb-20">
      {/* Header */}
      <div className="shrink-0 p-4 border-b border-border bg-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-healthGreen/10 flex items-center justify-center">
              <Activity className="w-4 h-4 text-healthGreen" />
            </div>
            <div>
              <h1 className="text-body font-semibold text-mirageBlack">AI Symptom Check</h1>
              <p className="text-micro text-clinicalGrey">
                {sessionId ? "Session active" : "Start a new session"}
              </p>
            </div>
          </div>
          {sessionId && (
            <button
              onClick={handleEndSession}
              className="flex items-center gap-1 px-3 py-1.5 border border-errorRed/20 text-errorRed rounded-button text-micro font-medium hover:bg-errorRed-50 transition-colors"
            >
              <CircleStop className="w-3 h-3" />
              End
            </button>
          )}
        </div>
      </div>

      {/* Chat Area */}
      {!sessionId ? (
        <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="w-16 h-16 rounded-full bg-healthGreen/10 flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-8 h-8 text-healthGreen" />
            </div>
            <h2 className="text-section-title font-semibold text-mirageBlack mb-2">
              AI Symptom Assessment
            </h2>
            <p className="text-caption text-clinicalGrey max-w-[260px] mx-auto mb-6">
              Describe your symptoms and our AI will ask follow-up questions to help assess your condition.
            </p>
            <button
              onClick={() => createSessionMutation.mutate()}
              disabled={createSessionMutation.isPending}
              className="inline-flex items-center gap-2 px-6 py-3 bg-healthGreen text-white rounded-button text-body font-medium hover:bg-healthGreen-600 transition-colors disabled:opacity-50"
            >
              {createSessionMutation.isPending ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Sparkles className="w-4 h-4" />
              )}
              {createSessionMutation.isPending ? "Starting..." : "Start Assessment"}
            </button>

            <div className="mt-8 space-y-2">
              <p className="text-micro text-clinicalGrey mb-2">Try asking about:</p>
              {suggestedQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => {
                    createSessionMutation.mutate(undefined, {
                      onSuccess: () => {
                        setMessages((prev) => [
                          ...prev,
                          {
                            id: `user-${Date.now()}`,
                            role: "user",
                            content: q,
                            timestamp: new Date(),
                          },
                        ]);
                        sendMessageMutation.mutate(q);
                      },
                    });
                  }}
                  className="block w-full text-left px-3 py-2 bg-white border border-border rounded-card text-caption text-mirageBlack hover:border-celestialBlue/30 hover:shadow-elevation-1 transition-all"
                >
                  <div className="flex items-center justify-between">
                    <span>{q}</span>
                    <ChevronRight className="w-3.5 h-3.5 text-clinicalGrey" />
                  </div>
                </button>
              ))}
            </div>
          </motion.div>
        </div>
      ) : (
        <>
          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
            <AnimatePresence>
              {messages.map((msg, index) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index === messages.length - 1 ? 0 : 0, duration: 0.2 }}
                  className={`flex gap-2 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  {msg.role === "ai" && (
                    <div className="w-7 h-7 rounded-full bg-healthGreen/10 flex items-center justify-center shrink-0 mt-0.5">
                      <Bot className="w-3.5 h-3.5 text-healthGreen" />
                    </div>
                  )}
                  <div
                    className={`max-w-[80%] rounded-2xl px-3 py-2 ${
                      msg.role === "user"
                        ? "bg-celestialBlue text-white rounded-br-md"
                        : "bg-white border border-border text-mirageBlack rounded-bl-md"
                    }`}
                  >
                    <p className="text-body leading-relaxed">{msg.content}</p>
                    <p
                      className={`text-micro mt-1 ${
                        msg.role === "user" ? "text-white/70" : "text-clinicalGrey"
                      }`}
                    >
                      {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </p>
                  </div>
                  {msg.role === "user" && (
                    <div className="w-7 h-7 rounded-full bg-celestialBlue/10 flex items-center justify-center shrink-0 mt-0.5">
                      <User className="w-3.5 h-3.5 text-celestialBlue" />
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>

            {isAiTyping && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex gap-2 justify-start"
              >
                <div className="w-7 h-7 rounded-full bg-healthGreen/10 flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="w-3.5 h-3.5 text-healthGreen" />
                </div>
                <div className="bg-white border border-border rounded-2xl rounded-bl-md px-3 py-2">
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 rounded-full bg-clinicalGrey animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 rounded-full bg-clinicalGrey animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 rounded-full bg-clinicalGrey animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Input */}
          <div className="shrink-0 p-3 bg-white border-t border-border">
            <form onSubmit={handleSend} className="flex items-center gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your symptom..."
                disabled={sendMessageMutation.isPending || isAiTyping}
                className="flex-1 bg-stellarWhite-100 border border-border rounded-input px-4 py-2.5 text-body text-mirageBlack placeholder:text-clinicalGrey focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!input.trim() || sendMessageMutation.isPending || isAiTyping}
                className="w-10 h-10 rounded-full bg-celestialBlue text-white flex items-center justify-center hover:bg-celestialBlue-600 transition-colors disabled:opacity-50 disabled:hover:bg-celestialBlue"
              >
                {sendMessageMutation.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </button>
            </form>
          </div>
        </>
      )}
    </div>
  );
}
