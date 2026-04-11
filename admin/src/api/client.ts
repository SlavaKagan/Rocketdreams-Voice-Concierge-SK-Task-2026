import axios, { AxiosError } from "axios";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

client.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const status = error.response?.status ?? 0;
    const detail =
      (error.response?.data as { detail?: string })?.detail ??
      error.message ??
      "Unknown error";
    console.error(`API Error [${status}]:`, detail);
    return Promise.reject(new ApiError(detail, status));
  }
);

export default client;