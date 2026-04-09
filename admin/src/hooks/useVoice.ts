import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getVoices, setActiveVoice } from "../api/voice";

export function useVoice() {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["voices"],
    queryFn: getVoices,
  });

  const setVoice = useMutation({
    mutationFn: (voice_id: number) => setActiveVoice(voice_id),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["voices"] }),
    onError: (error) => console.error("Failed to set voice:", error),
  });

  return { ...query, setVoice };
}