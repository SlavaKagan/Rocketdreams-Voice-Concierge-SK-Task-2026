import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { getVoices, setActiveVoice } from "../api/voice";

export function useVoice() {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["voices"],
    queryFn: getVoices,
  });

  const setVoice = useMutation({
    mutationFn: (voice_id: number) => setActiveVoice(voice_id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["voices"] });
      toast.success("Voice updated successfully");
    },
    onError: () => toast.error("Failed to update voice"),
  });

  return { ...query, setVoice };
}