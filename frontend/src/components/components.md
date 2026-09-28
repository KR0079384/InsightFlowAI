# frontend/src/components/

## Purpose
Reusable and specialized React UI components constructing the TraceIQ Decision Canvas interface.

## Files

### `Header.tsx`
Application top navigation header with project branding, tagline, active workspace selector, and deterministic verification badge.

### `DataOverview.tsx`
Badge ribbon showing live ingested counts for orders, products catalog, inventory log, suppliers, marketing campaigns, and customer profiles.

### `QuestionInput.tsx`
Natural language query interface with interactive search input, submit button, and one-click suggested inquiry chips.

### `ExecutiveAnswer.tsx`
Primary executive summary card providing high-impact takeaways derived from deterministic backend calculations.

### `KeyMetrics.tsx`
Grid of KPI metric cards (Revenue, Growth %, Stockout Days, Completed Orders) with comparison badges and direct evidence trace links.

### `WhyDrivers.tsx`
Root-cause decomposition cards isolating positive and negative contributors to revenue shifts with direct evidence inspection triggers.

### `RecommendedAction.tsx`
Prescriptive executive action card highlighting urgency level, estimated revenue recovery, and the primary "Simulate Decision" CTA button.

### `EvidenceDrawer.tsx`
Slide-out drawer displaying verifiable mathematical evidence: claims, metric calculations, formulas, source datasets, and live source CSV row tables.

### `SimulationModal.tsx`
Interactive what-if scenario simulator with sliders for reorder targets and lead time reductions, side-by-side Current vs Simulated comparison tables, and projected business impact summaries.

## Relationships
```text
App.tsx
  ├── Header
  ├── DataOverview
  ├── QuestionInput
  ├── ExecutiveAnswer
  ├── KeyMetrics
  ├── WhyDrivers
  ├── RecommendedAction
  ├── EvidenceDrawer
  └── SimulationModal
```
