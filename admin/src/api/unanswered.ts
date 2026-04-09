import client from "./client";
import type { UnansweredQuestion, ConvertToFAQRequest } from "../types";

export const getUnanswered = (): Promise<UnansweredQuestion[]> =>
  client.get("/api/unanswered").then((r) => r.data);

export const convertToFAQ = (
  id: number,
  data: ConvertToFAQRequest
): Promise<{ converted: boolean; faq_id: number }> =>
  client.post(`/api/unanswered/${id}/convert`, data).then((r) => r.data);

export const dismissQuestion = (id: number): Promise<void> =>
  client.delete(`/api/unanswered/${id}/dismiss`).then((r) => r.data);