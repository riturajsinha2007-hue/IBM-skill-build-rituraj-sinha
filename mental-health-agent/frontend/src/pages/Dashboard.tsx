import React from 'react';
import { Link } from 'react-router-dom';
import './Dashboard.css';

const tips = [
  'Take 5 slow, deep breaths when feeling overwhelmed.',
  'A short walk — even 10 minutes — can improve mood significantly.',
  'Write down 3 things you are grateful for today.',
  'Reach out to one person you trust today.',
  'Set one small, achievable goal for today.',
];

export default function Dashboard() {
  const tip = tips[Math.floor(new Date().getDate() % tips.length)];

  return (
    <div className="dashboard">
      <h1 className="page-title">Welcome to MindBridge 🧠</h1>
      <p className="page-subtitle">
        Your safe, private AI-powered mental wellbeing companion.
      </p>

      {/* Disclaimer Banner */}
      <div className="disclaimer-banner">
        ℹ️ MindBridge is an AI support tool and is <strong>not a replacement</strong> for
        professional medical or psychological care. If you are in immediate danger,
        please call emergency services or visit our{' '}
        <Link to="/crisis">Crisis Support</Link> page.
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <Link to="/chat" className="qa-card qa-chat">
          <span className="qa-icon">💬</span>
          <span className="qa-label">Start AI Chat</span>
          <span className="qa-desc">Talk with your empathetic AI companion</span>
        </Link>
        <Link to="/journal" className="qa-card qa-journal">
          <span className="qa-icon">📓</span>
          <span className="qa-label">Write in Journal</span>
          <span className="qa-desc">Reflect on your thoughts privately</span>
        </Link>
        <Link to="/resources" className="qa-card qa-resources">
          <span className="qa-icon">📚</span>
          <span className="qa-label">Learn & Explore</span>
          <span className="qa-desc">Mental health awareness resources</span>
        </Link>
        <Link to="/crisis" className="qa-card qa-crisis">
          <span className="qa-icon">🆘</span>
          <span className="qa-label">Crisis Support</span>
          <span className="qa-desc">Immediate help & helplines</span>
        </Link>
      </div>

      {/* Daily Tip */}
      <div className="card tip-card">
        <h3>💡 Daily Wellbeing Tip</h3>
        <p>{tip}</p>
      </div>

      {/* About the System */}
      <div className="card about-card">
        <h3>🤖 How MindBridge Works</h3>
        <p>
          MindBridge uses multiple specialised AI agents powered by{' '}
          <strong>IBM Granite</strong> via <strong>IBM watsonx.ai</strong>.
          Every response is grounded in verified mental-health resources through
          a <strong>RAG (Retrieval-Augmented Generation)</strong> pipeline,
          reducing the risk of AI hallucination on sensitive topics.
        </p>
        <ul className="agent-list">
          <li>🎓 <strong>Awareness Agent</strong> — Educational mental-health information</li>
          <li>🔍 <strong>Distress Detection Agent</strong> — Identifies potential risk signals</li>
          <li>💙 <strong>Empathetic Support Agent</strong> — Warm conversational support</li>
          <li>🆘 <strong>Crisis Response Agent</strong> — Safety-first high-risk guidance</li>
        </ul>
      </div>
    </div>
  );
}
