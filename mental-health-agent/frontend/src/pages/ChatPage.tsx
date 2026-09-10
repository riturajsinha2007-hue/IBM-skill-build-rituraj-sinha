import React, { useState, useRef, useEffect } from 'react';
import { v4 as uuid } from 'uuid';
import ReactMarkdown from 'react-markdown';
import { sendChat } from '../api';
import type { Message, ChatResponse, RiskLevel } from '../types';
import { Link } from 'react-router-dom';
import './ChatPage.css';

const SESSION_ID = uuid();

const riskLabel: Record<RiskLevel, string> = {
  low: 'Low Concern',
  moderate: 'Moderate Concern',
  high: 'High Concern',
};

export default function ChatPage() {
  const [history, setHistory] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lastResponse, setLastResponse] = useState<ChatResponse | null>(null);
  const [location, setLocation] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history, loading]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMsg: Message = { role: 'user', content: trimmed };
    const nextHistory = [...history, userMsg];
    setHistory(nextHistory);
    setInput('');
    setLoading(true);

    try {
      const res = await sendChat({
        session_id: SESSION_ID,
        message: trimmed,
        history: history,
        location: location || undefined,
      });
      const assistantMsg: Message = { role: 'assistant', content: res.reply };
      setHistory([...nextHistory, assistantMsg]);
      setLastResponse(res);
    } catch {
      setHistory([
        ...nextHistory,
        {
          role: 'assistant',
          content:
            'I encountered an error. If you are in distress, please contact a crisis helpline immediately.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <div>
          <h1 className="page-title">AI Chat 💬</h1>
          <p className="page-subtitle">Talk with your empathetic AI companion — powered by IBM Granite</p>
        </div>
        {lastResponse && (
          <div className="chat-status">
            <span className={`risk-badge risk-${lastResponse.risk_level}`}>
              {riskLabel[lastResponse.risk_level]}
            </span>
            <span className="agent-tag">via {lastResponse.agent_used} agent</span>
          </div>
        )}
      </div>

      {/* High-risk alert */}
      {lastResponse?.risk_level === 'high' && (
        <div className="crisis-alert">
          <strong>⚠️ We noticed signs of significant distress.</strong> Please reach out to a crisis
          support resource. <Link to="/crisis">View crisis support →</Link>
        </div>
      )}

      {/* Messages */}
      <div className="chat-messages">
        {history.length === 0 && (
          <div className="chat-empty">
            <p>👋 Hi, I'm here to listen. What's on your mind?</p>
            <p className="chat-empty-hint">You can ask about mental health, share how you're feeling, or just chat.</p>
          </div>
        )}
        {history.map((msg, i) => (
          <div key={i} className={`bubble bubble-${msg.role}`}>
            <div className="bubble-avatar">{msg.role === 'user' ? '🧑' : '🤖'}</div>
            <div className="bubble-content">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div className="bubble bubble-assistant">
            <div className="bubble-avatar">🤖</div>
            <div className="bubble-content typing-indicator">
              <span/><span/><span/>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Resources panel (crisis) */}
      {lastResponse?.resources && lastResponse.resources.length > 0 && (
        <div className="resources-inline card">
          <h4>🆘 Immediate Support Resources</h4>
          <div className="resources-grid">
            {lastResponse.resources.map((r, i) => (
              <div key={i} className="resource-chip">
                <strong>{r.name}</strong>
                {r.contact && <span> · {r.contact}</span>}
                {r.url && <a href={r.url} target="_blank" rel="noopener noreferrer"> ↗</a>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input area */}
      <div className="chat-input-area">
        <input
          type="text"
          placeholder="Optional: your location (for relevant resources)"
          value={location}
          onChange={e => setLocation(e.target.value)}
          className="location-input"
        />
        <div className="input-row">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Type your message… (Enter to send, Shift+Enter for new line)"
            rows={2}
            disabled={loading}
          />
          <button className="btn btn-primary send-btn" onClick={handleSend} disabled={loading || !input.trim()}>
            {loading ? '…' : 'Send ➤'}
          </button>
        </div>
        <p className="input-disclaimer">
          MindBridge is an AI and not a substitute for professional care.
          In emergency, call your local emergency number immediately.
        </p>
      </div>
    </div>
  );
}
