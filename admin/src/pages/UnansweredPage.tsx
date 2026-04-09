import { useState } from "react";
import type { UnansweredQuestion } from "../types";
import { useUnanswered } from "../hooks";
import { Button, Badge, Modal } from "../components/ui";
import { FAQ_CATEGORIES } from "../constants";

export default function UnansweredPage() {
  const { data: questions = [], isLoading, convert, dismiss } = useUnanswered();
  const [selected, setSelected] = useState<UnansweredQuestion | null>(null);
  const [answer, setAnswer] = useState("");
  const [category, setCategory] = useState("General");

  const handleConvert = async () => {
    if (!selected) return;
    await convert.mutateAsync({ id: selected.id, data: { answer, category } });
    setSelected(null);
    setAnswer("");
    setCategory("General");
  };

  const handleDismiss = async (id: number) => {
    if (!confirm("Dismiss this question?")) return;
    await dismiss.mutateAsync(id);
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Unanswered Questions</h1>
        <p className="text-gray-500 text-sm mt-1">
          {questions.length} questions waiting for review
        </p>
      </div>

      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : questions.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg">No unanswered questions 🎉</p>
          <p className="text-sm mt-1">All guest questions are being handled.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {questions.map((q) => (
            <div
              key={q.id}
              className="bg-dark-700 border border-dark-600 rounded-lg p-4 flex items-center gap-4"
            >
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm font-medium">{q.question}</p>
                <p className="text-gray-500 text-xs mt-1">
                  First asked: {new Date(q.created_at).toLocaleDateString()}
                </p>
              </div>
              <Badge color={q.frequency > 3 ? "red" : "gray"}>
                Asked {q.frequency}×
              </Badge>
              <div className="flex gap-2">
                <Button
                  className="text-xs py-1 px-3"
                  onClick={() => {
                    setSelected(q);
                    setAnswer("");
                    setCategory("General");
                  }}
                >
                  Answer
                </Button>
                <Button
                  variant="ghost"
                  className="text-xs py-1 px-3"
                  onClick={() => handleDismiss(q.id)}
                >
                  Dismiss
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {selected && (
        <Modal title="Convert to FAQ" onClose={() => setSelected(null)}>
          <div className="space-y-4">
            <div className="bg-dark-600 rounded p-3">
              <p className="text-xs text-gray-500 mb-1">Guest question</p>
              <p className="text-white text-sm">{selected.question}</p>
            </div>

            <div>
              <label className="text-sm text-gray-400 block mb-1">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-dark-600 border border-dark-500 rounded px-3 py-2 text-white text-sm"
              >
                {FAQ_CATEGORIES.map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-sm text-gray-400 block mb-1">Answer</label>
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                rows={4}
                className="w-full bg-dark-600 border border-dark-500 rounded px-3 py-2 text-white text-sm resize-none"
                placeholder="Write the answer..."
              />
            </div>

            <div className="flex gap-2 justify-end">
              <Button variant="ghost" onClick={() => setSelected(null)}>
                Cancel
              </Button>
              <Button
                onClick={handleConvert}
                disabled={!answer || convert.isPending}
              >
                {convert.isPending ? "Saving..." : "Save as FAQ"}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}