import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { DataOverview } from './components/DataOverview';
import { QuestionInput } from './components/QuestionInput';
import { ExecutiveAnswer } from './components/ExecutiveAnswer';
import { KeyMetrics } from './components/KeyMetrics';
import { WhyDrivers } from './components/WhyDrivers';
import { RecommendedAction } from './components/RecommendedAction';
import { EvidenceDrawer } from './components/EvidenceDrawer';
import { SimulationModal } from './components/SimulationModal';
import { DecisionReport, DatasetOverview, EvidenceItem } from './types';
import { fetchOverview, analyzeQuestion, fetchEvidenceDetail } from './api/client';
import { AlertCircle } from 'lucide-react';

export function App() {
  const [overview, setOverview] = useState<DatasetOverview | null>(null);
  const [report, setReport] = useState<DecisionReport | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Evidence Drawer state
  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceItem | null>(null);
  const [isEvidenceOpen, setIsEvidenceOpen] = useState<boolean>(false);

  // Simulation Modal state
  const [isSimulationOpen, setIsSimulationOpen] = useState<boolean>(false);

  useEffect(() => {
    // Initial load: dataset overview + default revenue question
    const loadInitialData = async () => {
      try {
        const ov = await fetchOverview();
        setOverview(ov);
        const rep = await analyzeQuestion('Why did revenue fall this month?');
        setReport(rep);
      } catch (err: any) {
        console.error('Initial load error:', err);
        setError('Failed to connect to TraceIQ backend. Please ensure the backend server is running on port 8000.');
      }
    };
    loadInitialData();
  }, []);

  const handleAnalyze = async (query: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const rep = await analyzeQuestion(query);
      setReport(rep);
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError('Analysis failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenEvidenceById = async (evidenceId: string) => {
    if (report) {
      const found = report.evidence_list.find((e) => e.id === evidenceId || evidenceId.includes(e.id));
      if (found) {
        setSelectedEvidence(found);
        setIsEvidenceOpen(true);
        return;
      }
    }
    // Fetch from API fallback
    try {
      const ev = await fetchEvidenceDetail(evidenceId);
      setSelectedEvidence(ev);
      setIsEvidenceOpen(true);
    } catch (err) {
      if (report && report.evidence_list.length > 0) {
        setSelectedEvidence(report.evidence_list[0]);
        setIsEvidenceOpen(true);
      }
    }
  };

  const handleOpenEvidenceByMetricKey = (metricKey: string) => {
    if (!report || report.evidence_list.length === 0) return;
    if (metricKey === 'stockout_days') {
      const found = report.evidence_list.find((e) => e.metric === 'stockout_days');
      setSelectedEvidence(found || report.evidence_list[0]);
    } else {
      setSelectedEvidence(report.evidence_list[0]);
    }
    setIsEvidenceOpen(true);
  };

  return (
    <div className="container" style={{ paddingTop: '1.5rem', paddingBottom: '3rem' }}>
      <Header companyName="Apex Retail Group (Q3 2026)" />

      <DataOverview overview={overview} />

      <QuestionInput onAnalyze={handleAnalyze} isLoading={isLoading} />

      {error && (
        <div style={{ background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', padding: '1rem 1.25rem', borderRadius: '10px', color: '#fb7185', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {report && (
        <main>
          {/* Executive Answer */}
          <ExecutiveAnswer answer={report.executive_answer} />

          {/* Key Metrics */}
          <KeyMetrics metrics={report.key_metrics} onViewEvidence={handleOpenEvidenceByMetricKey} />

          {/* Why? Root Causes & Drivers */}
          <WhyDrivers
            whyExplanation={report.why_explanation}
            drivers={report.drivers}
            onOpenEvidence={handleOpenEvidenceById}
          />

          {/* Recommended Action + CTA */}
          <RecommendedAction
            recommendation={report.recommendation}
            onOpenSimulation={() => setIsSimulationOpen(true)}
          />
        </main>
      )}

      {/* Verifiable Evidence Drawer */}
      <EvidenceDrawer
        isOpen={isEvidenceOpen}
        onClose={() => setIsEvidenceOpen(false)}
        evidence={selectedEvidence}
      />

      {/* What-If Decision Simulation Modal */}
      {report && (
        <SimulationModal
          isOpen={isSimulationOpen}
          onClose={() => setIsSimulationOpen(false)}
          initialSimulation={report.default_simulation}
          onOpenEvidence={handleOpenEvidenceById}
        />
      )}

      {/* Footer Branding */}
      <footer style={{ marginTop: '3rem', textAlign: 'center', color: 'var(--text-dim)', fontSize: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
        <span>TraceIQ Decision Engine</span>
        <span>•</span>
        <span>Build Fast with AI Challenge 2026</span>
        <span>•</span>
        <span style={{ color: '#34d399' }}>Deterministic Layer Active</span>
      </footer>
    </div>
  );
}
