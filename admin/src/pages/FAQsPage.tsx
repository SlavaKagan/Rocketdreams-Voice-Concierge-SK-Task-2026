import { useState } from "react";
import type { FAQItem, FAQCreate, FAQUpdate } from "../types";
import { useFAQs } from "../hooks/useFAQs";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import Modal from "../components/ui/Modal";

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

interface FAQFormData {
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

function FAQForm({ initial = {}, onSubmit, onClose, loading }: FAQFormProps) {
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

type ModalState =
  | { mode: "create" }
  | { mode: "edit"; faq: FAQItem }
  | null;

export default function FAQsPage() {
  const { data: faqs = [], isLoading, create, update, remove } = useFAQs();
  const [modal, setModal] = useState<ModalState>(null);
  const [search, setSearch] = useState("");

  const filtered = faqs.filter(
    (f) =>
      f.question.toLowerCase().includes(search.toLowerCase()) ||
      (f.category ?? "").toLowerCase().includes(search.toLowerCase())
  );

  const grouped = filtered.reduce<Record<string, FAQItem[]>>((acc, faq) => {
    const cat = faq.category ?? "General";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(faq);
    return acc;
  }, {});

  const handleCreate = async (form: FAQCreate) => {
    await create.mutateAsync(form);
    setModal(null);
  };

  const handleUpdate = async (form: FAQUpdate) => {
    if (modal?.mode !== "edit") return;
    await update.mutateAsync({ id: modal.faq.id, data: form });
    setModal(null);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this FAQ?")) return;
    await remove.mutateAsync(id);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">FAQ Management</h1>
          <p className="text-gray-500 text-sm mt-1">
            {faqs.length} items in knowledge base
          </p>
        </div>
        <Button onClick={() => setModal({ mode: "create" })}>+ Add FAQ</Button>
      </div>

      <input
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search FAQs..."
        className="w-full bg-dark-700 border border-dark-500 rounded px-4 py-2 text-white text-sm mb-6"
      />

      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="space-y-6">
          {Object.entries(grouped).map(([category, items]) => (
            <div key={category}>
              <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                {category}
              </h2>
              <div className="space-y-2">
                {items.map((faq) => (
                  <div
                    key={faq.id}
                    className="bg-dark-700 border border-dark-600 rounded-lg p-4 flex gap-4"
                  >
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm font-medium">
                        {faq.question}
                      </p>
                      <p className="text-gray-400 text-sm mt-1 line-clamp-2">
                        {faq.answer}
                      </p>
                    </div>
                    <div className="flex gap-2 shrink-0 items-start">
                      <Button
                        variant="ghost"
                        className="text-xs py-1 px-3"
                        onClick={() => setModal({ mode: "edit", faq })}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="danger"
                        className="text-xs py-1 px-3"
                        onClick={() => handleDelete(faq.id)}
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {modal && (
        <Modal
          title={modal.mode === "create" ? "Add FAQ" : "Edit FAQ"}
          onClose={() => setModal(null)}
        >
          <FAQForm
            initial={
              modal.mode === "edit"
                ? {
                  question: modal.faq.question,
                  answer: modal.faq.answer,
                  category: modal.faq.category ?? "General",
                }
                : {}
            }
            onSubmit={modal.mode === "create" ? handleCreate : handleUpdate}
            onClose={() => setModal(null)}
            loading={create.isPending || update.isPending}
          />
        </Modal>
      )}
    </div>
  );
}