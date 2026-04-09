import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
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
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["faqs"] }),
    onError: (error) => console.error("Failed to create FAQ:", error),
  });

  const update = useMutation({
    mutationFn: ({ id, data }: { id: number; data: FAQUpdate }) =>
      updateFAQ(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["faqs"] }),
    onError: (error) => console.error("Failed to update FAQ:", error),
  });

  const remove = useMutation({
    mutationFn: (id: number) => deleteFAQ(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["faqs"] }),
    onError: (error) => console.error("Failed to delete FAQ:", error),
  });

  return { ...query, create, update, remove };
}