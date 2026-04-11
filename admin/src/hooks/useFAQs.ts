import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { getFAQs, createFAQ, updateFAQ, deleteFAQ } from "../api/faqs";
import type { FAQCreate, FAQUpdate } from "../types";

export function useFAQs() {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["faqs"],
    queryFn: getFAQs,
  });

  const create = useMutation({
    mutationFn: (data: FAQCreate) => createFAQ(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["faqs"] });
      toast.success("FAQ created successfully");
    },
    onError: () => toast.error("Failed to create FAQ"),
  });

  const update = useMutation({
    mutationFn: ({ id, data }: { id: number; data: FAQUpdate }) =>
      updateFAQ(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["faqs"] });
      toast.success("FAQ updated successfully");
    },
    onError: () => toast.error("Failed to update FAQ"),
  });

  const remove = useMutation({
    mutationFn: (id: number) => deleteFAQ(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["faqs"] });
      toast.success("FAQ deleted");
    },
    onError: () => toast.error("Failed to delete FAQ"),
  });

  return { ...query, create, update, remove };
}