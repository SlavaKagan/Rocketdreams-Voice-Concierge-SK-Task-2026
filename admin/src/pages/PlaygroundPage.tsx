export default function PlaygroundPage() {
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

      <div
        className="bg-dark-700 border border-dark-600 rounded-lg overflow-hidden"
        style={{ height: "70vh" }}
      >
        <iframe
          src="https://agents-playground.livekit.io"
          className="w-full h-full"
          allow="microphone; camera; autoplay"
          title="Meridian Voice Concierge Playground"
        />
      </div>
    </div>
  );
}