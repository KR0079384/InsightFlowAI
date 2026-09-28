import React from 'react';
import { Compass, CheckCircle2 } from 'lucide-react';

interface ExecutiveAnswerProps {
  answer: string;
}

export const ExecutiveAnswer: React.FC<ExecutiveAnswerProps> = ({ answer }) => {
  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem', borderLeft: '4px solid #06b6d4' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
        <Compass size={18} color="#38bdf8" />
        <h2 style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Executive Answer
        </h2>
      </div>

      <div style={{ fontSize: '1.125rem', fontWeight: 600, lineHeight: '1.6', color: '#f8fafc' }}>
        {answer}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1rem', color: '#34d399', fontSize: '0.75rem', fontWeight: 600 }}>
        <CheckCircle2 size={14} />
        <span>Synthesized from 100% deterministic calculation logs & inventory audit</span>
      </div>
    </div>
  );
};
