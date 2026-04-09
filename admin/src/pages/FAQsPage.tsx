import { useState } from "react";
import type { FAQItem, FAQCreate, FAQUpdate } from "../types";
import { useFAQs } from "../hooks";
import { Button, Modal } from "../components/ui";
import FAQForm from "../components/FAQForm";

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