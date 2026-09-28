import React from 'react';
import { Lightbulb, Zap, TrendingUp, ArrowRight } from 'lucide-react';
import { RecommendationAction } from '../types';

interface RecommendedActionProps {
  recommendation: RecommendationAction;
  onOpenSimulation: () => void;
}

export const RecommendedAction: React.FC<RecommendedActionProps> = ({ recommendation, onOpenSimulation }) => {
  return (
    <div
      className="glass-panel"
      style={{
        padding: '1.75rem',
        marginBottom: '1.75rem',
        background: 'linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(17, 24, 39, 0.9) 100%)',
        border: '1px solid rgba(99, 102, 241, 0.4)',
        boxShadow: '0 8px 32px rgba(99, 102, 241, 0.15)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'rgba(99, 102, 241, 0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid rgba(99, 102, 241, 0.4)',
            }}
          >
            <Lightbulb size={20} color="#a5b4fc" />
          </div>
          <div>
            <span className="badge badge-indigo">
              Recommended Executive Action
            </span>
            <span className="badge badge-rose" style={{ marginLeft: '0.5rem' }}>
              Urgency: High
            </span>
          </div>
        </div>

        <button type="button" className="btn-simulate" onClick={onOpenSimulation}>
          <Zap size={18} />
          Simulate Decision
          <ArrowRight size={16} />
        </button>
      </div>

      <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.625rem' }}>
        {recommendation.title}
      </div>

      <p style={{ fontSize: '0.9375rem', color: '#cbd5e1', lineHeight: '1.6', marginBottom: '1.25rem' }}>
        {recommendation.description}
      </p>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          background: 'rgba(16, 185, 129, 0.1)',
          padding: '0.875rem 1.25rem',
          borderRadius: '10px',
          border: '1px solid rgba(16, 185, 129, 0.3)',
        }}
      >
        <TrendingUp size={20} color="#34d399" />
        <div>
          <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#34d399', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Expected Impact & Revenue Recovery:
          </span>
          <div style={{ fontSize: '0.875rem', color: '#f8fafc', fontWeight: 500, marginTop: '2px' }}>
            {recommendation.expected_impact}
          </div>
        </div>
      </div>
    </div>
  );
};
