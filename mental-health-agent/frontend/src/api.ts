import axios from 'axios';
import type { ChatRequest, ChatResponse, JournalEntry, JournalAnalysisResponse, Resource } from './types';

const api = axios.create({ baseURL: '/api' });

export const sendChat = (req: ChatRequest): Promise<ChatResponse> =>
  api.post<ChatResponse>('/chat', req).then(r => r.data);

export const saveJournal = (entry: JournalEntry): Promise<JournalEntry> =>
  api.post<JournalEntry>('/journal', entry).then(r => r.data);

export const analyseJournal = (entry: JournalEntry): Promise<JournalAnalysisResponse> =>
  api.post<JournalAnalysisResponse>('/journal/analyse', entry).then(r => r.data);

export const getResources = (location?: string): Promise<Resource[]> =>
  api.get<Resource[]>('/resources', { params: location ? { location } : {} }).then(r => r.data);
