export default function LoadingSpinner({ text = "Loading..." }: { text?: string }) {
  return (
    <div className="flex items-center gap-3 text-gray-500">
      <div className="w-4 h-4 border-2 border-gray-600 border-t-gold-400 rounded-full animate-spin" />
      <span className="text-sm">{text}</span>
    </div>
  );
}