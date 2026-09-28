# frontend/

## Purpose
React 18 + TypeScript + Vite web client hosting the **TraceIQ Decision Canvas**. Provides an executive dashboard for asking natural-language business questions, examining root-cause drivers, verifying calculation traces and source CSV rows in the Evidence Drawer, and testing what-if scenarios in the Scenario Simulator.

## Files

### `package.json`
Client package definition, bundling scripts, and dependencies (`lucide-react`, `react`, `react-dom`, `vite`, `typescript`).

### `vite.config.ts`
Vite configuration with API proxy forwarding `/api` calls to `http://127.0.0.1:8000`.

### `index.html`
HTML5 entry page with Google Fonts (`Plus Jakarta Sans`, `JetBrains Mono`) and SEO meta descriptions.

### `tsconfig.json`
TypeScript compiler settings.

## Subdirectories

### [`src/`](file:///k:/Projects/TraceIQ/frontend/src/src.md)
Frontend source code directory:
- `App.tsx`: Main Decision Canvas orchestration view.
- `index.css`: Design system tokens, glassmorphism, glowing cards, and dark theme styling.
- `main.tsx`: React DOM mount.
- [`components/`](file:///k:/Projects/TraceIQ/frontend/src/components/components.md): UI component modules.
- [`types/`](file:///k:/Projects/TraceIQ/frontend/src/types/types.md): TypeScript interfaces.
- [`api/`](file:///k:/Projects/TraceIQ/frontend/src/api/api.md): REST client communicating with FastAPI backend.

## Relationships
```text
frontend/ (Vite Dev Server :5173) ──proxy──> backend/ (FastAPI :8000)
```
