// Shared TypeScript types mirroring the backend Pydantic models

export type RiskLevel = 'low' | 'moderate' | 'high';
export type AgentType = 'awareness' | 'distress' | 'empathetic' | 'crisis';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface Resource {
  name: string;
  description: string;
  contact?: string;
  url?: string;
  location?: string;
}

export interface ChatRequest {
  session_id: string;
  message: string;
  history: Message[];
  location?: string;
}

export interface ChatResponse {
  session_id: string;
  reply: string;
  agent_used: AgentType;
  risk_level: RiskLevel;
  resources: Resource[];
  disclaimer: string;
}

export interface JournalEntry {
  entry_id?: string;
  content: string;
  analyze: boolean;
}

export interface JournalAnalysisResponse {
  entry_id: string;
  sentiment: string;
  risk_level: RiskLevel;
  reflection: string;
  suggestions: string[];
}
