import React from 'react';
import { Database, ShieldCheck, Sparkles } from 'lucide-react';

interface HeaderProps {
  companyName?: string;
}

export const Header: React.FC<HeaderProps> = ({ companyName = 'Demo Retail Co.' }) => {
  return (
    <header className="glass-panel" style={{ padding: '1.25rem 1.75rem', marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #0284c7 0%, #6366f1 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px rgba(6, 182, 212, 0.4)'
          }}>
            <Sparkles size={22} color="#ffffff" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <h1 style={{ fontSize: '1.5rem', fontWeight: 800, letterSpacing: '-0.025em' }} className="heading-gradient">
                TraceIQ
              </h1>
              <span className="badge badge-cyan">
                AI Decision Engine
              </span>
            </div>
            <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginTop: '2px' }}>
              Turn scattered business data into accurate answers and decisions you can trace.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255, 255, 255, 0.04)', padding: '0.4rem 0.8rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <Database size={15} color="#38bdf8" />
            <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>Workspace:</span>
            <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#f8fafc' }}>{companyName}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', background: 'rgba(16, 185, 129, 0.1)', padding: '0.4rem 0.75rem', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
            <ShieldCheck size={16} color="#34d399" />
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#34d399', letterSpacing: '0.05em' }}>
              DETERMINISTIC VERIFIED
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
