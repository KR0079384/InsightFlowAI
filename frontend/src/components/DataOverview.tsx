import React from 'react';
import { Layers, ShoppingBag, Package, Truck, Target, Users } from 'lucide-react';
import { DatasetOverview } from '../types';

interface DataOverviewProps {
  overview: DatasetOverview | null;
}

export const DataOverview: React.FC<DataOverviewProps> = ({ overview }) => {
  if (!overview) return null;

  const items = [
    { label: 'Orders Log', count: overview.datasets.orders, icon: ShoppingBag, color: '#38bdf8' },
    { label: 'Products Master', count: overview.datasets.products, icon: Package, color: '#818cf8' },
    { label: 'Inventory Ledger', count: overview.datasets.inventory, icon: Layers, color: '#34d399' },
    { label: 'Suppliers', count: overview.datasets.suppliers, icon: Truck, color: '#fbbf24' },
    { label: 'Marketing Ad Log', count: overview.datasets.marketing, icon: Target, color: '#fb7185' },
    { label: 'Customer Cohorts', count: overview.datasets.customers, icon: Users, color: '#c084fc' },
  ];

  return (
    <div className="glass-panel" style={{ padding: '0.875rem 1.25rem', marginBottom: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Ingested Business Layer:
          </span>
          <span style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
            {overview.date_range}
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          {items.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.375rem',
                  background: 'rgba(255, 255, 255, 0.03)',
                  padding: '0.25rem 0.625rem',
                  borderRadius: '6px',
                  border: '1px solid var(--border-subtle)',
                  fontSize: '0.75rem',
                }}
              >
                <Icon size={13} color={item.color} />
                <span style={{ color: 'var(--text-muted)' }}>{item.label}:</span>
                <span style={{ fontWeight: 700, color: '#f8fafc' }} className="font-mono">{item.count}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
