import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ChatPage from './pages/ChatPage';
import JournalPage from './pages/JournalPage';
import ResourcesPage from './pages/ResourcesPage';
import CrisisPage from './pages/CrisisPage';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <nav className="sidebar">
          <div className="sidebar-brand">
            <span className="brand-icon">🧠</span>
            <span className="brand-name">MindBridge</span>
          </div>
          <ul className="nav-links">
            <li><NavLink to="/" end>🏠 Home</NavLink></li>
            <li><NavLink to="/chat">💬 AI Chat</NavLink></li>
            <li><NavLink to="/journal">📓 Journal</NavLink></li>
            <li><NavLink to="/resources">📚 Resources</NavLink></li>
            <li><NavLink to="/crisis" className="crisis-link">🆘 Crisis Support</NavLink></li>
          </ul>
          <div className="sidebar-disclaimer">
            <p>MindBridge is an AI support tool.<br/>It is <strong>not</strong> a replacement for professional care.</p>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/journal" element={<JournalPage />} />
            <Route path="/resources" element={<ResourcesPage />} />
            <Route path="/crisis" element={<CrisisPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
