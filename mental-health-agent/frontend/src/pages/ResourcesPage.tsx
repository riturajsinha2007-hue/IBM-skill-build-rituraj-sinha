import React from 'react';
import './ResourcesPage.css';

const topics = [
  {
    title: '😟 Stress',
    body: `Stress is the body's natural response to challenges. Chronic stress can affect physical
and mental health. Common symptoms include difficulty concentrating, irritability, fatigue,
sleep disturbances, and physical tension.`,
    tips: [
      'Regular physical activity (even a 20-minute walk)',
      'Adequate sleep — 7 to 9 hours per night',
      'Mindful breathing or meditation',
      'Setting realistic goals and saying no when needed',
      'Talking to a trusted person',
    ],
  },
  {
    title: '😰 Anxiety',
    body: `Anxiety disorders involve excessive fear or worry that interferes with daily activities.
They are among the most common mental health conditions. Symptoms include persistent worry,
restlessness, fatigue, muscle tension, and physical symptoms like rapid heartbeat.`,
    tips: [
      '5-4-3-2-1 grounding: name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste',
      'Box breathing: inhale 4s → hold 4s → exhale 4s → hold 4s',
      'Limit news and social media consumption',
      'Challenge anxious thoughts — is this based on facts or fears?',
      'Seek professional support if symptoms persist',
    ],
  },
  {
    title: '😔 Depression',
    body: `Depression is a serious but treatable condition. Symptoms include persistent sadness,
loss of interest, changes in appetite, sleep disturbances, fatigue, difficulty concentrating,
and in severe cases, thoughts of death. It is not a sign of weakness — it is a medical condition.`,
    tips: [
      'Therapy — CBT (Cognitive Behavioral Therapy) is highly effective',
      'Medication as prescribed by a qualified professional',
      'Regular physical activity — even gentle movement helps',
      'Maintain social connections even when it feels difficult',
      'Seek help early — early intervention leads to better outcomes',
    ],
  },
  {
    title: '🧘 Mindfulness',
    body: `Mindfulness is the practice of paying attention to the present moment without judgment.
It can reduce stress, anxiety, and depressive symptoms and improve overall wellbeing.`,
    tips: [
      'Mindful breathing — focus on each in-breath and out-breath',
      'Body scan — bring awareness slowly to each part of your body',
      'Mindful walking — notice the sensations of each step',
      'Gratitude journaling — write 3 things you are grateful for each day',
      'Apps like Headspace or Insight Timer can guide beginners',
    ],
  },
  {
    title: '💙 Self-Care',
    body: `Self-care is any intentional action taken to care for your physical, mental, and emotional
health. It is not selfish — it is necessary. Regular self-care builds resilience against stress.`,
    tips: [
      'Sleep 7-9 hours and keep a consistent sleep schedule',
      'Eat nourishing food and stay hydrated',
      'Move your body daily — any movement counts',
      'Set healthy boundaries in relationships and work',
      'Do activities that bring you joy, even small ones',
    ],
  },
  {
    title: '🤝 Seeking Help',
    body: `Seeking professional mental-health support is a sign of strength, not weakness.
Early intervention leads to significantly better outcomes. Many effective treatments exist.`,
    tips: [
      'Talk to your primary care doctor as a starting point',
      'Ask for a referral to a psychologist, psychiatrist, or counselor',
      'Consider online therapy platforms if in-person access is difficult',
      'Community mental-health centers often offer subsidized support',
      'You deserve support — reaching out is the most important first step',
    ],
  },
];

export default function ResourcesPage() {
  return (
    <div className="resources-page">
      <h1 className="page-title">Mental Health Resources 📚</h1>
      <p className="page-subtitle">
        Evidence-informed educational content to support your mental wellbeing.
        All information is for awareness only — please consult a professional for personal advice.
      </p>

      <div className="topics-grid">
        {topics.map((t, i) => (
          <div key={i} className="card topic-card">
            <h3>{t.title}</h3>
            <p className="topic-body">{t.body}</p>
            <h4>Helpful tips</h4>
            <ul>
              {t.tips.map((tip, j) => <li key={j}>{tip}</li>)}
            </ul>
          </div>
        ))}
      </div>

      <div className="card external-links">
        <h3>🌐 Trusted External Resources</h3>
        <ul>
          <li><a href="https://www.who.int/health-topics/mental-health" target="_blank" rel="noopener noreferrer">WHO Mental Health</a></li>
          <li><a href="https://www.nimh.nih.gov/health" target="_blank" rel="noopener noreferrer">NIMH — Mental Health Information</a></li>
          <li><a href="https://www.mind.org.uk" target="_blank" rel="noopener noreferrer">Mind UK</a></li>
          <li><a href="https://www.nimhans.ac.in" target="_blank" rel="noopener noreferrer">NIMHANS India</a></li>
          <li><a href="https://icallhelpline.org" target="_blank" rel="noopener noreferrer">iCall India</a></li>
        </ul>
      </div>
    </div>
  );
}
