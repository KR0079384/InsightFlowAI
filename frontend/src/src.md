# frontend/src/

## Purpose
Core React 18 TypeScript application source for the **TraceIQ Decision Canvas**.

## Files

### `main.tsx`
React DOM mount entry point rendering the root `App` component into `#root`.

### `App.tsx`
Main Decision Canvas application container. Orchestrates data fetching, query execution, executive answer presentation, key metrics visualization, driver list, evidence drawer toggling, and what-if scenario simulations.

### `index.css`
Design system tokens, glassmorphism panel styles, color variables, glowing badges, range inputs, and dark-theme aesthetics.

## Subdirectories

### [`components/`](file:///k:/Projects/TraceIQ/frontend/src/components/components.md)
Specialized UI modules:
- `Header.tsx`: Brand and system status.
- `DataOverview.tsx`: Ingested table badges.
- `QuestionInput.tsx`: Natural language search input and inquiry chips.
- `ExecutiveAnswer.tsx`: Summary narrative card.
- `KeyMetrics.tsx`: KPI grid with evidence trace actions.
- `WhyDrivers.tsx`: Root-cause decomposition cards.
- `RecommendedAction.tsx`: Actionable recommendations with simulation CTA.
- `EvidenceDrawer.tsx`: Traceability inspection drawer with raw CSV data table.
- `SimulationModal.tsx`: Interactive scenario levers and Current vs Simulated metrics.

### [`types/`](file:///k:/Projects/TraceIQ/frontend/src/types/types.md)
TypeScript interfaces matching backend models (`index.ts`).

### [`api/`](file:///k:/Projects/TraceIQ/frontend/src/api/api.md)
REST client library (`client.ts`).

## Relationships
```text
main.tsx ──> App.tsx ──> components/ + api/ + types/
```
