import client from "./client";
import type { FAQItem, FAQCreate, FAQUpdate } from "../types";

export const getFAQs = (): Promise<FAQItem[]> =>
  client.get("/api/faqs").then((r) => r.data);

export const createFAQ = (data: FAQCreate): Promise<FAQItem> =>
  client.post("/api/faqs", data).then((r) => r.data);

export const updateFAQ = (id: number, data: FAQUpdate): Promise<FAQItem> =>
  client.put(`/api/faqs/${id}`, data).then((r) => r.data);

export const deleteFAQ = (id: number): Promise<void> =>
  client.delete(`/api/faqs/${id}`).then((r) => r.data);