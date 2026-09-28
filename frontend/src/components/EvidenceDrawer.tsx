import React, { useState } from 'react';
import { X, FileSpreadsheet, Calculator, Database, Copy, Check } from 'lucide-react';
import { EvidenceItem } from '../types';

interface EvidenceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  evidence: EvidenceItem | null;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ isOpen, onClose, evidence }) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !evidence) return null;

  const handleCopyFormula = () => {
    navigator.clipboard.writeText(evidence.formula);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const columns = evidence.sample_rows.length > 0 ? Object.keys(evidence.sample_rows[0]) : [];

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 50,
        display: 'flex',
        justifyContent: 'flex-end',
        background: 'rgba(0, 0, 0, 0.7)',
        backdropFilter: 'blur(4px)',
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '680px',
          height: '100vh',
          borderRadius: '0',
          borderLeft: '1px solid var(--border-subtle)',
          padding: '2rem',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '-10px 0 35px rgba(0, 0, 0, 0.6)',
          background: '#0c111d',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-subtle)' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
              <span className="badge badge-cyan">
                Deterministic Evidence Trace
              </span>
              <span className="badge badge-emerald">
                Confidence: 100%
              </span>
            </div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc' }}>
              Evidence & Mathematical Proof
            </h2>
          </div>

          <button
            type="button"
            onClick={onClose}
            style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px',
              padding: '0.5rem',
              color: 'var(--text-muted)',
              cursor: 'pointer',
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Claim Box */}
        <div style={{ background: 'rgba(6, 182, 212, 0.08)', padding: '1.25rem', borderRadius: '12px', border: '1px solid rgba(6, 182, 212, 0.25)', marginBottom: '1.5rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '0.375rem' }}>
            Verified Business Claim
          </div>
          <div style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', lineHeight: '1.5' }}>
            {evidence.claim}
          </div>
        </div>

        {/* Scope & Timing */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '0.875rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Analyzed Period</span>
            <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: '#f8fafc', marginTop: '2px' }} className="font-mono">
              {evidence.period}
            </div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '0.875rem', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>Comparison Baseline</span>
            <div style={{ fontSize: '0.9375rem', fontWeight: 600, color: '#f8fafc', marginTop: '2px' }} className="font-mono">
              {evidence.comparison || 'N/A'}
            </div>
          </div>
        </div>

        {/* Calculation Details */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', fontSize: '0.8125rem', fontWeight: 600, color: '#cbd5e1' }}>
              <Calculator size={15} color="#38bdf8" />
              <span>Calculation & Formula Steps</span>
            </div>
            <button
              type="button"
              onClick={handleCopyFormula}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-muted)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
                fontSize: '0.75rem',
              }}
            >
              {copied ? <Check size={12} color="#34d399" /> : <Copy size={12} />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>

          <div
            className="font-mono"
            style={{
              background: '#060910',
              padding: '1rem',
              borderRadius: '8px',
              border: '1px solid var(--border-subtle)',
              fontSize: '0.8125rem',
              color: '#38bdf8',
              lineHeight: '1.6',
            }}
          >
            <div style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>// Logic</div>
            <div style={{ color: '#e2e8f0', marginBottom: '0.5rem' }}>{evidence.calculation}</div>
            <div style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>// Evaluated Numeric Expression</div>
            <div style={{ color: '#34d399', fontWeight: 600 }}>{evidence.formula}</div>
          </div>
        </div>

        {/* Source Files */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', fontSize: '0.8125rem', fontWeight: 600, color: '#cbd5e1', marginBottom: '0.5rem' }}>
            <Database size={15} color="#818cf8" />
            <span>Underlying Source Datasets</span>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {evidence.source_files.map((file, idx) => (
              <span key={idx} className="badge badge-indigo" style={{ textTransform: 'none', fontFamily: 'var(--font-mono)' }}>
                <FileSpreadsheet size={12} />
                {file}
              </span>
            ))}
          </div>
        </div>

        {/* Source Rows Sample */}
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#cbd5e1' }}>
              Sample Source Records ({evidence.sample_rows.length} rows)
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Audited from CSV layer</span>
          </div>

          {evidence.sample_rows.length > 0 ? (
            <div
              style={{
                overflowX: 'auto',
                background: '#060910',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                maxHeight: '260px',
              }}
            >
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.75rem', textAlign: 'left' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', background: 'rgba(255, 255, 255, 0.03)' }}>
                    {columns.map((col) => (
                      <th key={col} style={{ padding: '0.5rem 0.75rem', color: 'var(--text-muted)', fontWeight: 600 }} className="font-mono">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {evidence.sample_rows.map((row, rIdx) => (
                    <tr
                      key={rIdx}
                      style={{
                        borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                        backgroundColor: rIdx % 2 === 0 ? 'transparent' : 'rgba(255, 255, 255, 0.01)',
                      }}
                    >
                      {columns.map((col) => (
                        <td key={col} style={{ padding: '0.5rem 0.75rem', color: '#e2e8f0' }} className="font-mono">
                          {String(row[col])}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ padding: '1rem', color: 'var(--text-dim)', fontSize: '0.8125rem', textAlign: 'center' }}>
              No direct rows attached to this claim.
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'flex-end' }}>
          <button type="button" className="btn-outline" onClick={onClose}>
            Close Evidence Drawer
          </button>
        </div>
      </div>
    </div>
  );
};
