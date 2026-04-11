import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import Layout from "./components/Layout";
import { FAQsPage, UnansweredPage, VoicePage, PlaygroundPage } from "./pages";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Navigate to="/faqs" replace />} />
            <Route path="/faqs" element={<FAQsPage />} />
            <Route path="/unanswered" element={<UnansweredPage />} />
            <Route path="/voice" element={<VoicePage />} />
            <Route path="/playground" element={<PlaygroundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background: "#1a1a1a",
            color: "#f5f5f5",
            border: "1px solid #2a2a2a",
            borderRadius: "8px",
            fontSize: "14px",
          },
          success: {
            iconTheme: {
              primary: "#e6b800",
              secondary: "#0a0a0a",
            },
          },
          error: {
            iconTheme: {
              primary: "#ef4444",
              secondary: "#0a0a0a",
            },
          },
          duration: 3000,
        }}
      />
    </QueryClientProvider>
  );
}