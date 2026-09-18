"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import { getStoredAccessToken } from "@/lib/api";

interface VoiceRecorderProps {
  onTranscript?: (text: string) => void;
}

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/transcription";

export default function VoiceRecorder({ onTranscript }: VoiceRecorderProps) {
  const [recording, setRecording] = useState(false);
  const [liveText, setLiveText] = useState("");
  const [finalText, setFinalText] = useState("");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const finalBufferRef = useRef("");

  const startRecording = useCallback(async () => {
    if (mediaRecorderRef.current) return;

    const token = getStoredAccessToken();
    if (!token) {
      // eslint-disable-next-line no-console
      console.error("No access token available for WebSocket transcription.");
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mimeType = MediaRecorder.isTypeSupported("audio/webm")
      ? "audio/webm"
      : MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : "";

    const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
    mediaRecorderRef.current = recorder;

    const wsUrl = `${WS_URL}?token=${encodeURIComponent(token)}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
      setRecording(true);
      recorder.start(100); // 100 ms chunks
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data) as {
          text?: string;
          is_final?: boolean;
          type?: string;
        };
        if (msg.type === "pong") return;

        const text = msg.text || "";
        const isFinal = msg.is_final ?? false;

        if (isFinal) {
          finalBufferRef.current += (finalBufferRef.current ? " " : "") + text;
          setFinalText(finalBufferRef.current);
          setLiveText("");
          onTranscript?.(finalBufferRef.current);
        } else {
          setLiveText(text);
        }
      } catch {
        // ignore malformed messages
      }
    };

    ws.onclose = () => {
      setRecording(false);
      setLiveText("");
      // Cleanup recorder
      if (mediaRecorderRef.current?.state !== "inactive") {
        try {
          mediaRecorderRef.current?.stop();
        } catch {
          // ignore
        }
      }
      stream.getTracks().forEach((t) => t.stop());
      mediaRecorderRef.current = null;
      wsRef.current = null;
    };

    ws.onerror = (err) => {
      // eslint-disable-next-line no-console
      console.error("Transcription WebSocket error:", err);
    };

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
        event.data.arrayBuffer().then((buffer) => {
          ws.send(buffer);
        });
      }
    };

    recorder.onstop = () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: "stop" }));
      }
      stream.getTracks().forEach((t) => t.stop());
    };
  }, [onTranscript]);

  const stopRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      recorder.stop();
    }
    // onstop handler will trigger stop action and close WS
  }, []);

  useEffect(() => {
    return () => {
      const recorder = mediaRecorderRef.current;
      if (recorder && recorder.state !== "inactive") {
        recorder.stop();
      }
      mediaRecorderRef.current = null;
      wsRef.current = null;
    };
  }, []);

  return (
    <div className="flex flex-col gap-3 p-4 border rounded-lg bg-white shadow-sm">
      <div className="flex items-center gap-2">
        <button
          onClick={recording ? stopRecording : startRecording}
          className={`px-4 py-2 rounded-full font-medium text-white transition-colors ${
            recording
              ? "bg-red-500 hover:bg-red-600"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
          type="button"
        >
          {recording ? "Stop Recording" : "Start Recording"}
        </button>
        {recording && (
          <span className="inline-flex items-center gap-1 text-sm text-red-500 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-red-500" />
            Recording…
          </span>
        )}
      </div>

      {(finalText || liveText) && (
        <div className="space-y-1">
          {finalText && (
            <p className="text-sm text-gray-700">
              <strong>Final:</strong> {finalText}
            </p>
          )}
          {liveText && (
            <p className="text-sm text-gray-500 italic">
              <strong>Interim:</strong> {liveText}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
