import React from 'react';
import './CrisisPage.css';

const helplines = [
  { country: '🇮🇳 India', lines: [
    { name: 'iCall', contact: '9152987821', url: 'https://icallhelpline.org', note: 'Mon–Sat, 8am–10pm' },
    { name: 'Vandrevala Foundation', contact: '1860-2662-345', url: 'https://vandrevalafoundation.com', note: '24×7' },
    { name: 'Snehi', contact: '+91-44-24640050', url: 'https://snehi.org', note: 'Mon–Sat 8am–10pm' },
    { name: 'iCall (WhatsApp)', contact: '+91 9152987821', url: '', note: 'Chat available' },
  ]},
  { country: '🇺🇸 USA', lines: [
    { name: '988 Suicide & Crisis Lifeline', contact: '988', url: 'https://988lifeline.org', note: '24×7 free' },
    { name: 'Crisis Text Line', contact: 'Text HOME to 741741', url: 'https://www.crisistextline.org', note: '24×7 free' },
    { name: 'NAMI Helpline', contact: '1-800-950-6264', url: 'https://www.nami.org/help', note: 'Mon–Fri 10am–10pm ET' },
  ]},
  { country: '🇬🇧 UK & Ireland', lines: [
    { name: 'Samaritans', contact: '116 123', url: 'https://www.samaritans.org', note: '24×7 free' },
    { name: 'PAPYRUS HOPEline', contact: '0800 068 4141', url: 'https://papyrus-uk.org', note: 'Young people' },
    { name: 'Shout', contact: 'Text SHOUT to 85258', url: 'https://giveusashout.org', note: '24×7 text' },
  ]},
  { country: '🌍 Global', lines: [
    { name: 'Crisis Text Line', contact: 'Text HOME to 741741', url: 'https://www.crisistextline.org', note: 'USA, UK, Canada, Ireland' },
    { name: 'Befrienders Worldwide', contact: '', url: 'https://www.befrienders.org', note: 'Find local helpline' },
    { name: 'IASP', contact: '', url: 'https://www.iasp.info/resources/Crisis_Centres/', note: 'Crisis centres directory' },
    { name: 'WHO Resources', contact: '', url: 'https://www.who.int/health-topics/mental-health', note: 'Global' },
  ]},
];

const steps = [
  { icon: '🗣️', title: 'Talk to someone you trust', body: 'Reach out to a friend, family member, or mentor. You do not have to face this alone.' },
  { icon: '📞', title: 'Call a crisis helpline', body: 'Trained crisis counselors are available 24/7 — they are confidential and non-judgmental.' },
  { icon: '🏥', title: 'Go to your nearest emergency room', body: 'If you are in immediate danger, emergency care is available to keep you safe.' },
  { icon: '💬', title: 'Use the AI Chat', body: 'MindBridge AI Chat is available anytime to listen and provide supportive guidance.' },
];

export default function CrisisPage() {
  return (
    <div className="crisis-page">
      <div className="crisis-hero">
        <h1>🆘 You Are Not Alone</h1>
        <p>
          If you are in crisis or experiencing thoughts of self-harm, please reach out immediately.
          Help is available — and recovery is possible. Your life has value.
        </p>
        <a className="btn btn-danger emergency-btn" href="tel:112">
          📞 Emergency: Call 112 / 911 / 999
        </a>
      </div>

      <div className="card">
        <h2>What to do right now</h2>
        <div className="steps-grid">
          {steps.map((s, i) => (
            <div key={i} className="step-card">
              <span className="step-icon">{s.icon}</span>
              <h4>{s.title}</h4>
              <p>{s.body}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="helplines-section">
        <h2>Crisis Helplines by Region</h2>
        {helplines.map((region, i) => (
          <div key={i} className="card region-card">
            <h3>{region.country}</h3>
            <div className="lines-grid">
              {region.lines.map((line, j) => (
                <div key={j} className="line-card">
                  <div className="line-name">{line.name}</div>
                  {line.contact && <div className="line-contact">📞 {line.contact}</div>}
                  {line.url && (
                    <a href={line.url} target="_blank" rel="noopener noreferrer" className="line-url">
                      Visit website ↗
                    </a>
                  )}
                  <div className="line-note">{line.note}</div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="card warning-signs-card">
        <h3>⚠️ Warning Signs to Watch For</h3>
        <ul>
          <li>Talking about wanting to die or feeling hopeless</li>
          <li>Withdrawing from friends, family, or activities</li>
          <li>Giving away prized possessions</li>
          <li>Extreme mood changes — sudden calmness after deep depression</li>
          <li>Increased substance use</li>
          <li>Saying goodbye as if not expecting to see people again</li>
        </ul>
        <p className="warning-action">
          If you notice these signs in yourself or someone else,
          please reach out to a crisis helpline or emergency services immediately.
        </p>
      </div>

      <p className="crisis-disclaimer">
        MindBridge is an AI tool and is not a substitute for professional crisis intervention.
        In any emergency, please contact your local emergency services immediately.
      </p>
    </div>
  );
}
