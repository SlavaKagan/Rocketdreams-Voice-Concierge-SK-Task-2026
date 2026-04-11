import { useState, useCallback } from "react";
import {
  LiveKitRoom,
  useVoiceAssistant,
  BarVisualizer,
  VoiceAssistantControlBar,
  RoomAudioRenderer,
  DisconnectButton,
  useChat,
} from "@livekit/components-react";
import "@livekit/components-styles";
import { getPlaygroundToken } from "../api/playground";
import type { PlaygroundToken } from "../types";
import { Button } from "../components/ui";

interface TranscriptEntry {
  id: string;
  role: "user" | "assistant";
  text: string;
  timestamp: Date;
}

function ConciergeChatUI() {
  const { state, audioTrack } = useVoiceAssistant();
  console.log("Agent state:", state);
  const { chatMessages } = useChat();

  // Build transcript from chat messages
  const entries: TranscriptEntry[] = chatMessages.map((msg) => ({
    id: msg.id,
    role: msg.from?.isAgent ? "assistant" : "user",
    text: typeof msg.message === "string" ? msg.message : "",
    timestamp: new Date(msg.timestamp),
  }));

  const stateLabels: Record<string, string> = {
    disconnected: "Disconnected",
  connecting: "Connecting...",
  initializing: "Initializing...",
  listening: "Listening...",
  thinking: "Thinking...",
  speaking: "Speaking...",
  // LiveKit v1 actual state names
  idle: "Ready",
  processing: "Thinking...",
  responding: "Speaking...",
  waiting: "Waiting...",
  };

const stateColors: Record<string, string> = {
  disconnected: "text-gray-500",
  connecting: "text-yellow-400",
  initializing: "text-yellow-400",
  listening: "text-green-400",
  thinking: "text-blue-400",
  speaking: "text-gold-400",
  // LiveKit v1 actual state names
  idle: "text-gray-400",
  processing: "text-blue-400",
  responding: "text-gold-400",
  waiting: "text-gray-400",
};

  return (
    <div className="flex h-full">
      {/* Left — voice controls */}
      <div className="flex flex-col items-center justify-between py-8 px-6 w-72 border-r border-dark-600">
        <div className="text-center">
          <p className="text-gray-500 text-xs uppercase tracking-widest mb-1">
            Concierge Status
          </p>
          <p className={`text-lg font-semibold ${stateColors[state] ?? "text-gray-400"}`}>
            {stateLabels[state] ?? state}
          </p>
        </div>

        <div className="w-full">
          <BarVisualizer
            state={state}
            trackRef={audioTrack}
            className="w-full"
            style={{ height: "80px" }}
            barCount={24}
            options={{ minHeight: 4 }}
          />
        </div>

        <p className="text-gray-500 text-sm text-center">
          {state === "listening"
            ? "Go ahead, ask your question..."
            : state === "speaking"
            ? "The concierge is speaking..."
            : "The concierge is ready"}
        </p>

        <div className="flex flex-col items-center gap-4 w-full">
          <VoiceAssistantControlBar />
          <DisconnectButton>
            <button className="w-full py-2 px-4 rounded bg-red-600/20 text-red-400 border border-red-600/30 hover:bg-red-600/30 transition-all text-sm font-medium">
              End Conversation
            </button>
          </DisconnectButton>
        </div>
      </div>

      {/* Right — transcript */}
      <div className="flex-1 flex flex-col">
        <div className="px-4 py-3 border-b border-dark-600 flex items-center justify-between">
          <p className="text-xs text-gray-500 uppercase tracking-wider">
            Conversation Transcript
          </p>
          <p className="text-xs text-gray-600">
            {entries.length} messages
          </p>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {entries.length === 0 ? (
            <p className="text-gray-600 text-sm text-center mt-8">
              Transcript will appear here as you speak...
            </p>
          ) : (
            entries.map((entry) => (
              <div
                key={entry.id}
                className={`flex gap-3 ${
                  entry.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {entry.role === "assistant" && (
                  <div className="w-6 h-6 rounded-full bg-gold-500/20 border border-gold-500/30 flex items-center justify-center shrink-0 mt-1">
                    <span className="text-gold-400 text-xs">M</span>
                  </div>
                )}
                <div
                  className={`max-w-xs rounded-lg px-3 py-2 text-sm ${
                    entry.role === "user"
                      ? "bg-dark-600 text-white"
                      : "bg-gold-500/10 border border-gold-500/20 text-gray-200"
                  }`}
                >
                  <p>{entry.text}</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {entry.timestamp.toLocaleTimeString()}
                  </p>
                </div>
                {entry.role === "user" && (
                  <div className="w-6 h-6 rounded-full bg-dark-500 border border-dark-400 flex items-center justify-center shrink-0 mt-1">
                    <span className="text-gray-400 text-xs">G</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default function PlaygroundPage() {
  const [session, setSession] = useState<PlaygroundToken | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleConnect = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const token = await getPlaygroundToken();
      setSession(token);
    } catch {
      setError("Failed to connect. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }, []);

  const handleDisconnect = useCallback(() => {
    setSession(null);
  }, []);

  return (
    <div>
      <div className="mb-6">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-white">Playground</h1>
          <span className="text-xs bg-gold-500/10 text-gold-400 border border-gold-500/20 px-2 py-0.5 rounded-full font-medium">
            Test Mode
          </span>
        </div>
        <p className="text-gray-500 text-sm mt-1">
          Test the voice concierge with current FAQ and voice configuration
        </p>
      </div>

      {!session ? (
        <div
          className="bg-dark-700 border border-dark-600 rounded-lg flex flex-col items-center justify-center gap-6 p-12"
          style={{ height: "60vh" }}
        >
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-gold-500/10 border border-gold-500/20 flex items-center justify-center mb-4 mx-auto">
              <span className="text-2xl">🎙️</span>
            </div>
            <p className="text-white text-lg font-medium mb-2">
              Meridian Voice Concierge
            </p>
            <p className="text-gray-400 text-sm max-w-sm">
              Start a conversation to test the concierge with the current FAQ
              knowledge base and active voice configuration.
            </p>
          </div>

          {error && (
            <p className="text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded px-4 py-2">
              {error}
            </p>
          )}

          <Button onClick={handleConnect} disabled={loading} className="px-8">
            {loading ? "Connecting..." : "Start Conversation"}
          </Button>
        </div>
      ) : (
        <div
          className="bg-dark-700 border border-gold-500/30 rounded-lg overflow-hidden"
          style={{ height: "65vh" }}
        >
          <div className="bg-dark-800 border-b border-dark-600 px-6 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              <span className="text-white text-sm font-medium">
                Connected to Meridian Concierge
              </span>
            </div>
            <span className="text-gray-500 text-xs">Room: {session.room}</span>
          </div>

          <LiveKitRoom
            token={session.token}
            serverUrl={session.url}
            connect={true}
            audio={true}
            video={false}
            onDisconnected={handleDisconnect}
            className="h-full"
          >
            <RoomAudioRenderer />
            <ConciergeChatUI />
          </LiveKitRoom>
        </div>
      )}
    </div>
  );
}