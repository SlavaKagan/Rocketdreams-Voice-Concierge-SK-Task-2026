import { useState } from "react";
import { Button } from "./ui";

const CATEGORIES = [
  "General",
  "Gaming",
  "Dining",
  "Accommodations",
  "Bars",
  "Entertainment",
  "Events",
  "Partners",
];

export interface FAQFormData {
  question: string;
  answer: string;
  category: string;
}

interface FAQFormProps {
  initial?: Partial<FAQFormData>;
  onSubmit: (data: FAQFormData) => void;
  onClose: () => void;
  loading: boolean;
}

export default function FAQForm({
  initial = {},
  onSubmit,
  onClose,
  loading,
}: FAQFormProps) {
  const [form, setForm] = useState<FAQFormData>({
    question: initial.question ?? "",
    answer: initial.answer ?? "",
    category: initial.category ?? "General",
  });

  const set = <K extends keyof FAQFormData>(key: K, value: FAQFormData[K]) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(form);
      }}
      className="space-y-4"
    >
      <div>
        <label className="text-sm text-gray-400 block mb-1">Category</label>
        <select
          value={form.category}
          onChange={(e) => set("category", e.target.value)}
          className="w-full bg-dark-600 border border-dark-500 rounded px-3 py-2 text-white text-sm"
        >
          {CATEGORIES.map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-sm text-gray-400 block mb-1">Question</label>
        <input
          value={form.question}
          onChange={(e) => set("question", e.target.value)}
          required
          className="w-full bg-dark-600 border border-dark-500 rounded px-3 py-2 text-white text-sm"
          placeholder="e.g. What time does the pool open?"
        />
      </div>

      <div>
        <label className="text-sm text-gray-400 block mb-1">Answer</label>
        <textarea
          value={form.answer}
          onChange={(e) => set("answer", e.target.value)}
          required
          rows={4}
          className="w-full bg-dark-600 border border-dark-500 rounded px-3 py-2 text-white text-sm resize-none"
          placeholder="The full answer..."
        />
      </div>

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="ghost" onClick={onClose}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save"}
        </Button>
      </div>
    </form>
  );
}