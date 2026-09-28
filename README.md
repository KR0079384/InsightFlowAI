# InsightFlowAI — AI Decision Engine for Business Data

> **Turn scattered business data into accurate answers and decisions you can trace.**

## Core Workflow
**Observe → Explain → Recommend → Simulate**

## Core Engineering Principle
**LLM proposes. Data engine proves.**

TraceIQ is a decision-support system built for the **Build Fast with AI: AI Build Challenge 2026**. It ingests business data (orders, inventory, products, marketing, suppliers), calculates deterministic business metrics, isolates drivers and anomalies, formulates actionable executive decisions with end-to-end verifiable evidence, and allows leaders to simulate scenarios deterministically.

---

## Directory Navigation Map

| Directory | Navigation Map | Purpose |
| :--- | :--- | :--- |
| `src/` | [`src.md`](file:///k:/Projects/TraceIQ/src/src.md) | Backend FastAPI app, deterministic data engine, and decision engine |
| `data/` | [`data.md`](file:///k:/Projects/TraceIQ/data/data.md) | Deterministic business datasets (orders, inventory, products, marketing, suppliers) |
| `frontend/` | [`frontend.md`](file:///k:/Projects/TraceIQ/frontend/frontend.md) | Vite + React + TypeScript Decision Canvas UI |
| `tests/` | [`tests.md`](file:///k:/Projects/TraceIQ/tests/tests.md) | Automated tests for deterministic metrics, evidence, and simulator |

---

## Quick Start

### 1. Backend Setup & Run
```bash
# Install Python dependencies (FastAPI, uvicorn, pandas, pydantic, pytest)
pip install -r requirements.txt

# Generate or refresh deterministic demo data
python data/generate_demo_data.py

# Run FastAPI backend
python src/main.py
```
Backend API docs available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup & Run
```bash
cd frontend
npm install
npm run dev
```
TraceIQ Decision Canvas will run at `http://localhost:5173`.

### 3. Run Automated Tests
```bash
pytest tests/ -v
```
