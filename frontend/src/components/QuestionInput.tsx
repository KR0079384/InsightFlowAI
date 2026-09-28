import React, { useState } from 'react';
import { Search, Sparkles, ArrowRight, Loader2 } from 'lucide-react';

interface QuestionInputProps {
  onAnalyze: (query: string) => void;
  isLoading: boolean;
}

export const QuestionInput: React.FC<QuestionInputProps> = ({ onAnalyze, isLoading }) => {
  const [query, setQuery] = useState('Why did revenue fall this month?');

  const sampleQuestions = [
    'Why did revenue fall this month?',
    'What caused AeroMax Pro Headphones sales to drop?',
    'Show stockout impact on audio category',
    'What if we increase reorder quantity by 20%?',
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onAnalyze(query.trim());
    }
  };

  const handleChipClick = (q: string) => {
    setQuery(q);
    onAnalyze(q);
  };

  return (
    <div className="glass-panel glass-panel-glow" style={{ padding: '1.5rem', marginBottom: '1.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.875rem' }}>
        <Sparkles size={16} color="#38bdf8" />
        <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Ask Your Business
        </span>
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.75rem', position: 'relative' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={18} color="var(--text-dim)" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            className="search-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. Why did revenue drop in September? Which SKUs drove the change?"
            style={{ paddingLeft: '2.75rem' }}
          />
        </div>
        <button type="submit" className="btn-primary" disabled={isLoading} style={{ minWidth: '130px', justifyContent: 'center' }}>
          {isLoading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Proving...
            </>
          ) : (
            <>
              Analyze
              <ArrowRight size={16} />
            </>
          )}
        </button>
      </form>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Suggested inquiries:</span>
        {sampleQuestions.map((sq, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleChipClick(sq)}
            style={{
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-muted)',
              fontSize: '0.75rem',
              padding: '0.25rem 0.625rem',
              borderRadius: '9999px',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
            }}
            onMouseOver={(e) => (e.currentTarget.style.borderColor = 'rgba(6, 182, 212, 0.4)')}
            onMouseOut={(e) => (e.currentTarget.style.borderColor = 'var(--border-subtle)')}
          >
            {sq}
          </button>
        ))}
      </div>
    </div>
  );
};
