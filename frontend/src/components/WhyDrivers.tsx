import React from 'react';
import { HelpCircle, AlertOctagon, TrendingUp, ChevronRight, FileText } from 'lucide-react';
import { DriverItem } from '../types';

interface WhyDriversProps {
  whyExplanation: string;
  drivers: DriverItem[];
  onOpenEvidence: (evidenceId: string) => void;
}

export const WhyDrivers: React.FC<WhyDriversProps> = ({ whyExplanation, drivers, onOpenEvidence }) => {
  return (
    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
        <HelpCircle size={18} color="#f59e0b" />
        <h2 style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--accent-amber)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Why? Root Cause Decomposition
        </h2>
      </div>

      <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-subtle)', marginBottom: '1.25rem', fontSize: '0.875rem', color: '#cbd5e1', lineHeight: '1.6', whiteSpace: 'pre-line' }}>
        {whyExplanation}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {drivers.map((driver) => {
          const isNegative = driver.impact_type === 'negative';
          return (
            <div
              key={driver.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '1rem',
                padding: '0.875rem 1.25rem',
                borderRadius: '10px',
                background: isNegative ? 'rgba(244, 63, 94, 0.05)' : 'rgba(16, 185, 129, 0.05)',
                border: isNegative ? '1px solid rgba(244, 63, 94, 0.2)' : '1px solid rgba(16, 185, 129, 0.2)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', flex: 1, minWidth: '280px' }}>
                <div style={{ marginTop: '2px' }}>
                  {isNegative ? (
                    <AlertOctagon size={18} color="#fb7185" />
                  ) : (
                    <TrendingUp size={18} color="#34d399" />
                  )}
                </div>
                <div>
                  <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: '#f8fafc' }}>
                    {driver.title}
                  </div>
                  <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {driver.explanation}
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Impact</div>
                  <div
                    className="font-mono"
                    style={{
                      fontSize: '1.125rem',
                      fontWeight: 700,
                      color: isNegative ? '#fb7185' : '#34d399',
                    }}
                  >
                    {driver.impact_formatted}
                  </div>
                </div>

                <button
                  type="button"
                  className="btn-outline"
                  style={{ fontSize: '0.8125rem', borderColor: isNegative ? 'rgba(244, 63, 94, 0.3)' : 'rgba(16, 185, 129, 0.3)' }}
                  onClick={() => onOpenEvidence(driver.evidence_id)}
                >
                  <FileText size={14} />
                  Trace Evidence
                  <ChevronRight size={14} />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
