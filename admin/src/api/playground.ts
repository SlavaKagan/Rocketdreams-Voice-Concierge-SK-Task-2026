import client from "./client";
import type { PlaygroundToken } from "../types";

export const getPlaygroundToken = (): Promise<PlaygroundToken> =>
  client.get("/api/playground/token").then((r) => r.data);