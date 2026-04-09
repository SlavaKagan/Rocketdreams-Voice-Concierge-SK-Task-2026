import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
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
    </QueryClientProvider>
  );
}