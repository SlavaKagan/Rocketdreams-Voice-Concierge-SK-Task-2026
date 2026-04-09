import { useVoice } from "../hooks";
import { Badge, Button } from "../components/ui";
import type { VoiceOption } from "../types";

export default function VoicePage() {
  const { data, isLoading, setVoice } = useVoice();

  if (isLoading) return <p className="text-gray-500">Loading...</p>;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Voice Configuration</h1>
        <p className="text-gray-500 text-sm mt-1">
          Select the active concierge voice
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 max-w-2xl">
        {data?.voices.map((voice: VoiceOption) => {
          const isActive = voice.id === data.active_voice_id;
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
          );
        })}
      </div>
    </div>
  );
}