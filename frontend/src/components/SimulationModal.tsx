import React, { useState, useEffect } from 'react';
import { X, Zap, Sliders, TrendingUp, CheckCircle, RotateCcw, Loader2 } from 'lucide-react';
import { SimulationResponse } from '../types';
import { runSimulation } from '../api/client';

interface SimulationModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialSimulation: SimulationResponse | null;
  onOpenEvidence: (evidenceId: string) => void;
}

export const SimulationModal: React.FC<SimulationModalProps> = ({
  isOpen,
  onClose,
  initialSimulation,
  onOpenEvidence,
}) => {
  const [simulation, setSimulation] = useState<SimulationResponse | null>(initialSimulation);
  const [reorderDelta, setReorderDelta] = useState<number>(20);
  const [leadTimeReduction, setLeadTimeReduction] = useState<number>(3);
  const [mktDelta, setMktDelta] = useState<number>(0);
  const [priceDelta, setPriceDelta] = useState<number>(0);
  const [isRecalculating, setIsRecalculating] = useState<boolean>(false);
  const [appliedNotification, setAppliedNotification] = useState<boolean>(false);

  useEffect(() => {
    if (initialSimulation) {
      setSimulation(initialSimulation);
      setReorderDelta(initialSimulation.parameters_applied.reorder_quantity_delta_pct ?? 20);
      setLeadTimeReduction(initialSimulation.parameters_applied.lead_time_days_reduction ?? 3);
    }
  }, [initialSimulation]);

  if (!isOpen || !simulation) return null;

  const handleRunSimulation = async (
    reorder: number = reorderDelta,
    leadTime: number = leadTimeReduction,
    mkt: number = mktDelta,
    price: number = priceDelta
  ) => {
    setIsRecalculating(true);
    try {
      const res = await runSimulation({
        product_id: simulation.product_id || 'PROD-001',
        reorder_quantity_delta_pct: reorder,
        lead_time_days_reduction: leadTime,
        marketing_budget_delta_pct: mkt,
        price_change_pct: price,
      });
      setSimulation(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setIsRecalculating(false);
    }
  };

  const handleReset = () => {
    setReorderDelta(20);
    setLeadTimeReduction(3);
    setMktDelta(0);
    setPriceDelta(0);
    handleRunSimulation(20, 3, 0, 0);
  };

  const handleApplyToOperations = () => {
    setAppliedNotification(true);
    setTimeout(() => setAppliedNotification(false), 4000);
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 50,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(6px)',
        padding: '1.5rem',
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '860px',
          maxHeight: '92vh',
          overflowY: 'auto',
          padding: '2rem',
          background: '#0e1322',
          border: '1px solid rgba(99, 102, 241, 0.4)',
          boxShadow: '0 20px 50px rgba(0, 0, 0, 0.7)',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Zap size={22} color="#ffffff" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc' }}>
                  Simulate Business Decision
                </h2>
                <span className="badge badge-indigo">
                  {isRecalculating ? (
                    <>
                      <Loader2 size={12} className="animate-spin" />
                      Recalculating...
                    </>
                  ) : (
                    'Deterministic Model'
                  )}
                </span>
              </div>
              <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                {simulation.product_name} ({simulation.product_id})
              </p>
            </div>
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

        {appliedNotification && (
          <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.4)', padding: '0.875rem 1.25rem', borderRadius: '10px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <CheckCircle size={18} color="#34d399" />
            <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#34d399' }}>
              Action plan dispatched to ERP & Inventory procurement queue.
            </span>
          </div>
        )}

        {/* Interactive Scenario Controls */}
        <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.25rem', borderRadius: '12px', border: '1px solid var(--border-subtle)', marginBottom: '1.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8125rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase' }}>
              <Sliders size={16} />
              Adjust Operational Levers
            </div>
            <button
              type="button"
              onClick={handleReset}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-muted)',
                cursor: 'pointer',
                fontSize: '0.75rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.25rem',
              }}
            >
              <RotateCcw size={12} />
              Reset
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            {/* Reorder Lever */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.8125rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Reorder Quantity Target:</span>
                <span style={{ fontWeight: 700, color: '#38bdf8' }} className="font-mono">{reorderDelta > 0 ? `+${reorderDelta}%` : `${reorderDelta}%`}</span>
              </div>
              <input
                type="range"
                min="-20"
                max="60"
                step="5"
                value={reorderDelta}
                onChange={(e) => {
                  const val = Number(e.target.value);
                  setReorderDelta(val);
                  handleRunSimulation(val, leadTimeReduction, mktDelta, priceDelta);
                }}
              />
            </div>

            {/* Lead Time Lever */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.8125rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Supplier Lead Time Reduction:</span>
                <span style={{ fontWeight: 700, color: '#34d399' }} className="font-mono">{leadTimeReduction} days faster</span>
              </div>
              <input
                type="range"
                min="0"
                max="6"
                step="1"
                value={leadTimeReduction}
                onChange={(e) => {
                  const val = Number(e.target.value);
                  setLeadTimeReduction(val);
                  handleRunSimulation(reorderDelta, val, mktDelta, priceDelta);
                }}
              />
            </div>
          </div>
        </div>

        {/* Current vs Simulated Comparison Matrix */}
        <div style={{ marginBottom: '1.75rem' }}>
          <div style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '0.75rem' }}>
            Deterministic Scenario Comparison (Current vs Simulated)
          </div>

          <div
            style={{
              background: '#080c16',
              borderRadius: '12px',
              border: '1px solid var(--border-subtle)',
              overflow: 'hidden',
            }}
          >
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ background: 'rgba(255, 255, 255, 0.03)', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
                  <th style={{ padding: '0.75rem 1rem', color: 'var(--text-muted)', fontWeight: 600 }}>Metric</th>
                  <th style={{ padding: '0.75rem 1rem', color: '#fb7185', fontWeight: 600 }}>Current (Actual)</th>
                  <th style={{ padding: '0.75rem 1rem', color: '#38bdf8', fontWeight: 600 }}>Simulated Scenario</th>
                  <th style={{ padding: '0.75rem 1rem', color: '#34d399', fontWeight: 600 }}>Delta Improvement</th>
                </tr>
              </thead>
              <tbody>
                {simulation.metrics.map((m, idx) => (
                  <tr
                    key={idx}
                    style={{
                      borderBottom: '1px solid rgba(255, 255, 255, 0.03)',
                      backgroundColor: idx % 2 === 0 ? 'transparent' : 'rgba(255, 255, 255, 0.01)',
                    }}
                  >
                    <td style={{ padding: '0.875rem 1rem', fontWeight: 500, color: '#f8fafc' }}>
                      {m.name}
                    </td>
                    <td style={{ padding: '0.875rem 1rem', color: '#e2e8f0' }} className="font-mono">
                      {m.current}
                    </td>
                    <td style={{ padding: '0.875rem 1rem', fontWeight: 700, color: '#38bdf8' }} className="font-mono">
                      {m.simulated}
                    </td>
                    <td
                      style={{
                        padding: '0.875rem 1rem',
                        fontWeight: 700,
                        color: m.is_positive ? '#34d399' : '#fb7185',
                      }}
                      className="font-mono"
                    >
                      {m.difference}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Narrative Executive Summary */}
        <div style={{ background: 'rgba(16, 185, 129, 0.08)', padding: '1.25rem', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.25)', marginBottom: '1.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.375rem' }}>
            <TrendingUp size={16} color="#34d399" />
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#34d399', textTransform: 'uppercase' }}>
              Projected Business Impact
            </span>
          </div>
          <p style={{ fontSize: '0.9375rem', color: '#f8fafc', lineHeight: '1.6' }}>
            {simulation.executive_summary}
          </p>
        </div>

        {/* Footer Actions */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
          <button
            type="button"
            className="btn-outline"
            onClick={() => onOpenEvidence(simulation.evidence_link || 'ev-stockout-PROD-001')}
          >
            Inspect Baseline Evidence →
          </button>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button type="button" className="btn-outline" onClick={onClose}>
              Close
            </button>
            <button type="button" className="btn-simulate" onClick={handleApplyToOperations}>
              <CheckCircle size={16} />
              Execute Decision Plan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
