import React from 'react';
import { TrendingDown, TrendingUp, AlertTriangle, BarChart3 } from 'lucide-react';
import { MetricValue } from '../types';

interface KeyMetricsProps {
  metrics: MetricValue[];
  onViewEvidence: (metricKey: string) => void;
}

export const KeyMetrics: React.FC<KeyMetricsProps> = ({ metrics, onViewEvidence }) => {
  return (
    <div style={{ marginBottom: '1.75rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.875rem' }}>
        <BarChart3 size={17} color="#818cf8" />
        <h2 style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Key Metrics
        </h2>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
        {metrics.map((metric) => {
          const isNegative = metric.change_pct !== null && metric.change_pct !== undefined && metric.change_pct < 0;
          const isStockout = metric.key === 'stockout_days';

          return (
            <div
              key={metric.key}
              className="glass-panel"
              style={{
                padding: '1.25rem',
                position: 'relative',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                  <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                    {metric.name}
                  </span>
                  {isStockout ? (
                    <span className="badge badge-rose">
                      <AlertTriangle size={11} />
                      High Risk
                    </span>
                  ) : isNegative ? (
                    <span className="badge badge-rose">
                      <TrendingDown size={11} />
                      {metric.change_pct?.toFixed(1)}%
                    </span>
                  ) : (
                    <span className="badge badge-emerald">
                      <TrendingUp size={11} />
                      {metric.change_pct ? `+${metric.change_pct.toFixed(1)}%` : 'Baseline'}
                    </span>
                  )}
                </div>

                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc', marginBottom: '0.5rem' }} className="font-mono">
                  {metric.formatted}
                </div>

                <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', lineHeight: '1.4' }}>
                  {metric.description}
                </p>
              </div>

              <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  className="btn-outline"
                  style={{ fontSize: '0.75rem', padding: '0.25rem 0.625rem' }}
                  onClick={() => onViewEvidence(metric.key)}
                >
                  View Evidence Trace →
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
