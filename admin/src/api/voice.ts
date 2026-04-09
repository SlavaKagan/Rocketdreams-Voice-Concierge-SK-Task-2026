import client from "./client";
import type { VoicesResponse } from "../types";

export const getVoices = (): Promise<VoicesResponse> =>
  client.get("/api/voices").then((r) => r.data);

export const setActiveVoice = (
  voice_id: number
): Promise<{ active_voice_id: number }> =>
  client.put("/api/voices/active", { voice_id }).then((r) => r.data);

export const previewVoice = (voice_id: number): Promise<Blob> =>
  client
    .get(`/api/voices/${voice_id}/preview`, { responseType: "blob" })
    .then((r) => r.data);