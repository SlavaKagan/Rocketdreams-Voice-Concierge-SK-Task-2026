import client from "./client";
import type { VoicesResponse, PlaygroundToken } from "../types";

export const getVoices = (): Promise<VoicesResponse> =>
  client.get("/api/voices").then((r) => r.data);

export const setActiveVoice = (
  voice_id: number
): Promise<{ active_voice_id: number }> =>
  client.put("/api/voices/active", { voice_id }).then((r) => r.data);

export const getPlaygroundToken = (): Promise<PlaygroundToken> =>
  client.get("/api/playground/token").then((r) => r.data);