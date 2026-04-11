interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <span className="text-red-400 text-lg">⚠️</span>
        <p className="text-red-400 text-sm">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-xs text-red-400 border border-red-500/30 rounded px-3 py-1 hover:bg-red-500/10 transition-all"
        >
          Retry
        </button>
      )}
    </div>
  );
}