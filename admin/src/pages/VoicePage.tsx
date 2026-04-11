import { useState } from "react";
import { useVoice } from "../hooks";
import { Badge, Button, ErrorMessage, LoadingSpinner } from "../components/ui";
import { previewVoice } from "../api/voice";
import type { VoiceOption } from "../types";

export default function VoicePage() {
  const { data, isLoading, isError, refetch, setVoice } = useVoice();
  const [previewingId, setPreviewingId] = useState<number | null>(null);

  const handlePreview = async (voice: VoiceOption) => {
    if (previewingId === voice.id) return;
    setPreviewingId(voice.id);
    try {
      const blob = await previewVoice(voice.id);
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.play();
      audio.onended = () => {
        setPreviewingId(null);
        URL.revokeObjectURL(url);
      };
    } catch {
      console.error("Preview failed");
      setPreviewingId(null);
    }
  };

  if (isLoading) return <LoadingSpinner text="Loading voices..." />;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Voice Configuration</h1>
        <p className="text-gray-500 text-sm mt-1">
          Select the active concierge voice
        </p>
      </div>

      {isError && (
        <div className="mb-6">
          <ErrorMessage
            message="Failed to load voices. Is the backend running?"
            onRetry={() => refetch()}
          />
        </div>
      )}

      <div className="grid grid-cols-1 gap-4 max-w-2xl">
        {data?.voices.map((voice: VoiceOption) => {
          const isActive = voice.id === data.active_voice_id;
          const isPreviewing = previewingId === voice.id;
          return (
            <div
              key={voice.id}
              className={`bg-dark-700 border rounded-lg p-5 flex items-center gap-4 transition-all ${
                isActive ? "border-gold-500" : "border-dark-600"
              }`}
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-white font-semibold">{voice.name}</span>
                  {isActive && <Badge color="gold">Active</Badge>}
                </div>
                <p className="text-gray-400 text-sm">{voice.description}</p>
              </div>
              <div className="flex gap-2 shrink-0">
                <Button
                  variant="ghost"
                  className="text-xs py-1 px-3"
                  onClick={() => handlePreview(voice)}
                  disabled={isPreviewing}
                >
                  {isPreviewing ? "▶ Playing..." : "▶ Preview"}
                </Button>
                {!isActive && (
                  <Button
                    variant="ghost"
                    onClick={() => setVoice.mutate(voice.id)}
                    disabled={setVoice.isPending}
                  >
                    Select
                  </Button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}