"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { getStoredAccessToken } from "@/lib/api";

function getWsBase(): string {
  if (typeof window === "undefined") return "";
  if (process.env.NEXT_PUBLIC_WS_URL) return process.env.NEXT_PUBLIC_WS_URL;
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}`;
}

interface UseVoiceRecorderReturn {
  recording: boolean;
  liveText: string;
  finalText: string;
  startRecording: () => Promise<void>;
  stopRecording: () => void;
}

export function useVoiceRecorder(onTranscript?: (text: string) => void): UseVoiceRecorderReturn {
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

    const wsUrl = `${getWsBase()}/transcription?token=${encodeURIComponent(token)}`;
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

  return { recording, liveText, finalText, startRecording, stopRecording };
}
