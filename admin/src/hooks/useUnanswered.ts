import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getUnanswered, convertToFAQ, dismissQuestion } from "../api/unanswered";
import type { ConvertToFAQRequest } from "../types";

export function useUnanswered() {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["unanswered"],
    queryFn: getUnanswered,
  });

  const convert = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ConvertToFAQRequest }) =>
      convertToFAQ(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["unanswered"] });
      queryClient.invalidateQueries({ queryKey: ["faqs"] });
    },
    onError: (error) => console.error("Failed to convert question:", error),
  });

  const dismiss = useMutation({
    mutationFn: (id: number) => dismissQuestion(id),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["unanswered"] }),
    onError: (error) => console.error("Failed to dismiss question:", error),
  });

  return { ...query, convert, dismiss };
}