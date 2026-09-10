import React, { useState } from 'react';
import { saveJournal, analyseJournal } from '../api';
import type { JournalAnalysisResponse, RiskLevel } from '../types';
import { Link } from 'react-router-dom';
import './JournalPage.css';

const riskLabel: Record<RiskLevel, string> = {
  low: 'Low Concern',
  moderate: 'Moderate Concern',
  high: 'High Concern',
};

export default function JournalPage() {
  const [content, setContent] = useState('');
  const [analyze, setAnalyze] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [analysis, setAnalysis] = useState<JournalAnalysisResponse | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!content.trim()) return;
    setLoading(true);
    setError('');
    setAnalysis(null);
    setSaved(false);

    try {
      if (analyze) {
        const result = await analyseJournal({ content, analyze: true });
        setAnalysis(result);
      } else {
        await saveJournal({ content, analyze: false });
        setSaved(true);
      }
      setContent('');
    } catch (e) {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="journal-page">
      <h1 className="page-title">Journal 📓</h1>
      <p className="page-subtitle">
        A private space to reflect on your thoughts and feelings. Your entries are yours.
      </p>

      <div className="card journal-card">
        <textarea
          className="journal-textarea"
          value={content}
          onChange={e => setContent(e.target.value)}
          placeholder="Write what's on your mind today…"
          rows={8}
          disabled={loading}
        />

        <div className="journal-controls">
          <label className="consent-label">
            <input
              type="checkbox"
              checked={analyze}
              onChange={e => setAnalyze(e.target.checked)}
              disabled={loading}
            />
            <span>
              I consent to AI analysis of this entry to receive supportive feedback.
              <em> (Optional — data is not stored permanently.)</em>
            </span>
          </label>

          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={loading || !content.trim()}
          >
            {loading ? 'Processing…' : analyze ? '🔍 Save & Analyse' : '💾 Save Entry'}
          </button>
        </div>
      </div>

      {/* Success / error */}
      {saved && <div className="feedback-banner feedback-ok">✅ Entry saved privately.</div>}
      {error && <div className="feedback-banner feedback-err">⚠️ {error}</div>}

      {/* Analysis results */}
      {analysis && (
        <div className="card analysis-card">
          <h3>📊 Journal Analysis</h3>

          <div className="analysis-row">
            <span>Sentiment:</span>
            <strong>{analysis.sentiment}</strong>
          </div>
          <div className="analysis-row">
            <span>Risk level:</span>
            <span className={`risk-badge risk-${analysis.risk_level}`}>
              {riskLabel[analysis.risk_level]}
            </span>
          </div>

          <div className="analysis-section">
            <h4>Reflection</h4>
            <p>{analysis.reflection}</p>
          </div>

          <div className="analysis-section">
            <h4>Suggestions</h4>
            <ul>
              {analysis.suggestions.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
          </div>

          {analysis.risk_level === 'high' && (
            <div className="analysis-crisis-prompt">
              ⚠️ We noticed significant distress signals.
              Please consider reaching out to a professional or a crisis helpline.
              <Link to="/crisis"> View crisis support →</Link>
            </div>
          )}

          <p className="analysis-disclaimer">
            This analysis is for supportive awareness only and does not constitute
            clinical diagnosis. Please consult a qualified professional for medical advice.
          </p>
        </div>
      )}
    </div>
  );
}
