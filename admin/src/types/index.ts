export interface FAQItem {
  id: number;
  question: string;
  answer: string;
  category: string | null;
  created_at: string;
}

export interface FAQCreate {
  question: string;
  answer: string;
  category: string;
}

export interface FAQUpdate {
  question?: string;
  answer?: string;
  category?: string;
}

export interface UnansweredQuestion {
  id: number;
  question: string;
  frequency: number;
  created_at: string;
  last_asked_at: string;
}

export interface ConvertToFAQRequest {
  answer: string;
  category: string;
}

export interface VoiceOption {
  id: number;
  name: string;
  elevenlabs_id: string;
  description: string;
}

export interface VoicesResponse {
  active_voice_id: number;
  voices: VoiceOption[];
}

export interface SearchResponse {
  found: boolean;
  question?: string;
  answer?: string;
  category?: string;
  similarity?: number;
}