# TraceIQ --- Master Progress Checklist

> **Purpose:** Single GitHub checklist for tracking TraceIQ from the
> current working build to final submission.
>
> **Team** - **Karthi** --- Tech lead, final integration, model/LLM
> architecture - **Rishi** --- Backend intelligence, LLM support,
> validation, QA - **Rafeeq** --- UX/UI, frontend, video editing
>
> **Status rule:** Only mark `[x]` when the work is actually
> completed/verified. Keep `[ ]` for pending work and use `[~]` for
> partial/unverified work.

---

# 0. Current Project Baseline

- [x] Repository/project foundation created
- [x] Python environment/dependencies configured
- [x] Node/npm frontend environment configured
- [x] README created
- [x] `project.md` created
- [x] Navigation `.md` system established across meaningful
      directories
- [x] Demo data generator created
- [x] Demo datasets generated
- [x] Backend package structure created
- [x] Frontend package structure created
- [x] Test package created
- [x] Initial backend/frontend architecture established

---

# 1. Data Layer

## Datasets

- [x] Orders dataset
- [x] Products dataset
- [x] Inventory dataset
- [x] Suppliers dataset
- [x] Marketing dataset
- [x] Customers dataset
- [x] Deterministic demo-data generator
- [x] `data/data.md`

## Data engine

- [x] Multi-table data loader
- [x] Revenue calculation
- [x] Revenue growth calculation
- [x] SKU performance calculations
- [x] Stockout detection
- [x] Marketing anomaly detection
- [x] Driver/variance decomposition
- [x] Deterministic scenario simulator
- \[\~\] Edge-case handling
- \[\~\] Independent calculation validation
- [ ] Missing/null/invalid-data handling audit
- [ ] Test across additional datasets/scenarios
- [ ] Manual verification of all important calculations

**Owner:** Rishi\
**Support:** Karthi

---

# 2. Natural Language / Intent Layer

- [x] Question classifier
- [x] Parameter extraction
- [x] Natural-language intent improvements
- [x] Support for core business questions
- [x] Question variation testing
- [x] Unsupported/failure-case handling
- [ ] Expand question coverage further if needed
- [ ] Final regression test across representative questions

**Owner:** Karthi + Rishi

---

# 3. LLM Layer

## Core implementation

- [x] Local Ollama-based synthesis module
- [x] LLM synthesis integrated into decision engine
- [x] Prompt design
- [x] LLM response structure
- [x] Context construction
- [x] Evidence → LLM context
- [x] Output validation
- [x] Fallback for unavailable/invalid LLM responses
- [x] Timeout handling
- [x] Logging
- [x] Business-language explanations
- [x] Test prompts
- [x] Failure-case handling
- [x] Historical-vs-simulation separation
- [x] Evidence-date preservation
- [x] Cautious correlation language
- [x] Explanation-bullet deduplication
- \[\~\] Hallucination prevention --- implemented but requires broader
  validation
- \[\~\] Recommendation wording --- implemented but still requires
  unsupported-claim review

## Final LLM validation

- [ ] Verify LLM consistently follows supplied evidence
- [ ] Test more question variations against live Ollama
- [ ] Check all numerical claims against deterministic outputs
- [ ] Correct unsupported causal wording
- [ ] Correct percentage inconsistencies
- [ ] Ensure recommendations do not introduce unsupported claims
- [ ] Verify historical facts are not presented as simulation results
- [ ] Verify simulation projections are clearly labeled
- [ ] Finalize LLM guardrails
- [ ] Freeze LLM prompt/architecture

**Owner:** Karthi\
**LLM validation/prompt support:** Rishi

---

# 4. Evidence & Explainability

- [x] Evidence object/schema
- [x] Evidence builder
- [x] Formula trace
- [x] Raw CSV/source-row evidence
- [x] Evidence integrated with decision engine
- [x] Evidence drawer frontend
- \[\~\] Independent evidence-flow validation
- [ ] Verify every major displayed metric can be traced
- [ ] Verify every major driver has supporting evidence
- [ ] Verify recommendation has supporting evidence
- [ ] Verify source rows match displayed claims
- [ ] Verify evidence lookup endpoint independently
- [ ] Final evidence UX polish

**Owner:** Karthi\
**QA:** Rishi\
**UI:** Rafeeq

---

# 5. Recommendation Engine

- [x] Recommendation generation
- [x] Recommendation integrated into Decision Canvas
- \[\~\] Recommendation wording
- [ ] Verify recommendations are fully evidence-backed
- [ ] Verify recommendations do not overstate causality
- [ ] Verify recommendation assumptions
- [ ] Connect recommendation clearly to driver
- [ ] Connect recommendation clearly to simulation
- [ ] Final recommendation UX polish

**Owner:** Karthi + Rishi\
**UI:** Rafeeq

---

# 6. Simulation / What-If Engine

- [x] Deterministic simulator
- [x] Reorder-target scenario
- [x] Lead-time scenario
- [x] Stockout projection
- [x] Units-fulfilled projection
- [x] Revenue-recovery projection
- [x] Simulation API
- [x] Simulation UI/modal
- \[\~\] Independent simulation validation
- [ ] Validate multiple scenario combinations
- [ ] Validate invalid/extreme inputs
- [ ] Verify historical vs projected labeling
- [ ] Display simulation assumptions clearly
- [ ] Independently test simulation endpoint
- [ ] Final simulation UX polish

**Owner:** Karthi\
**Validation:** Rishi\
**UI:** Rafeeq

---

# 7. Backend / API

- [x] FastAPI application
- [x] Health endpoint
- [x] Overview endpoint
- [x] Analyze endpoint
- [x] Simulation endpoint
- [x] Pydantic request/response schemas
- [x] Static frontend serving
- [x] API integration tests
- [x] Live `/api/v1/analyze` verification
- \[\~\] Error handling across full pipeline
- [ ] Review API logs for unintended debug output
- [ ] Verify request validation
- [ ] Verify failure responses
- [ ] Final production/demo startup check

**Owner:** Karthi\
**QA:** Rishi

---

# 8. Frontend / Decision Canvas

## Existing

- [x] React + TypeScript setup
- [x] Vite setup
- [x] Header
- [x] Data overview
- [x] Question input
- [x] Executive answer
- [x] Key metrics
- [x] Why-drivers section
- [x] Recommended action
- [x] Evidence drawer
- [x] Simulation modal
- [x] API client
- [x] TypeScript interfaces
- [x] Initial visual design
- [x] Frontend build verified

## Final UX

- [ ] Final layout polish
- [ ] Typography polish
- [ ] Spacing consistency
- [ ] KPI visual polish
- [ ] Driver-card polish
- [ ] Evidence drawer polish
- [ ] Simulation modal polish
- [ ] Recommendation CTA polish
- [ ] Loading states
- [ ] Error states
- [ ] Empty states
- [ ] Responsive/browser-size validation
- [ ] Remove visual inconsistencies
- [ ] Remove unnecessary UI
- [ ] Check browser console for errors
- [ ] Complete browser workflow verification

**Owner:** Rafeeq

---

# 9. Testing & QA

## Existing automated tests

- [x] Metrics tests
- [x] Evidence tests
- [x] Simulation tests
- [x] API tests
- [x] Initial 10-test suite passed
- [x] Regression suite expanded to 40 passing tests as reported by
      Rishi

## Remaining QA

- \[\~\] Backend intelligence validation
- \[\~\] Evidence validation
- \[\~\] Simulation validation
- \[\~\] End-to-end validation
- \[\~\] Fresh-startup validation
- [ ] Re-run complete Python test suite after latest changes
- [ ] Add/verify intent tests
- [ ] Add/verify LLM regression tests
- [ ] Add edge-case tests
- [ ] Add invalid-input tests
- [ ] Add missing-data tests
- [ ] Manually verify key metrics
- [ ] Manually verify drivers
- [ ] Manually verify simulation
- [ ] Test evidence lookup
- [ ] Test simulation endpoint
- [ ] Test complete browser flow
- [ ] Test fresh startup from clean environment
- [ ] Review logs/debug output
- [ ] Final regression run after integration

**Primary QA owner:** Rishi\
**Final integration QA:** Karthi\
**Frontend QA:** Rafeeq

---

# 10. Documentation & Agent Navigation

## Existing

- [x] Root `README.md`
- [x] `project.md`
- [x] `data/data.md`
- [x] `src/src.md`
- [x] `src/models/models.md`
- [x] `src/data_engine/data_engine.md`
- [x] `src/decision_engine/decision_engine.md`
- [x] `frontend/frontend.md`
- [x] `frontend/src/src.md`
- [x] `frontend/src/types/types.md`
- [x] `frontend/src/api/api.md`
- [x] `frontend/src/components/components.md`
- [x] `tests/tests.md`

## Final documentation audit

- [ ] Audit every meaningful project folder
- [ ] Ensure every navigation `.md` is accurate
- [ ] Update `.md` files after structural changes
- [ ] Document final architecture
- [ ] Document deterministic-vs-LLM responsibilities
- [ ] Document evidence flow
- [ ] Document simulation flow
- [ ] Document assumptions
- [ ] Document limitations
- [ ] Document setup instructions
- [ ] Document troubleshooting
- [ ] Add architecture/workflow diagram
- [ ] Add final demo flow to README

**Owner:** Rishi\
**Final review:** Karthi

---

# 11. Git / Branch Hygiene

## Rishi

- [x] `1e584d8` --- Improve natural language intent understanding
- [x] `f41d7f4` --- Add local Ollama LLM synthesis module
- [x] `e315129` --- Ignore Python cache files
- [x] `425753f` --- Integrate LLM synthesis into decision engine
- [x] Review latest narrative-consistency changes
- [ ] Review latest live API output
- [ ] Commit latest changes
- [ ] Push Rishi branch

## Team

- [ ] Review all branches
- [ ] Resolve merge conflicts
- [ ] Integrate Rishi changes
- [ ] Integrate Rafeeq frontend changes
- [ ] Run full tests after merge
- [ ] Final cleanup commit
- [ ] Freeze `main`

---

# 12. Final Integration

**Owner: Karthi**

- [ ] Merge Rishi's final LLM/backend changes
- [ ] Merge Rafeeq's final frontend changes
- [ ] Resolve integration issues
- [ ] Run complete Python test suite
- [ ] Run frontend build
- [ ] Start backend from clean state
- [ ] Start frontend from clean state
- [ ] Verify API
- [ ] Verify LLM
- [ ] Verify evidence
- [ ] Verify recommendation
- [ ] Verify simulation
- [ ] Verify complete browser flow
- [ ] Verify no console errors
- [ ] Verify no debug output
- [ ] Verify no hard-coded local paths
- [ ] Verify no secrets/API keys
- [ ] Freeze architecture
- [ ] Freeze features

---

# 13. Demo Readiness

## Core demo flow

- [ ] Ask: "Why did revenue fall this month?"
- [ ] Show executive answer
- [ ] Show revenue decline
- [ ] Show key metrics
- [ ] Show root causes
- [ ] Open evidence
- [ ] Show source rows/formula
- [ ] Show recommendation
- [ ] Open simulation
- [ ] Change scenario lever
- [ ] Show projected outcome
- [ ] Explain historical vs projected data

## Demo stability

- [ ] Clean browser session
- [ ] Clean backend startup
- [ ] Clean frontend startup
- [ ] Demo dataset reproducible
- [ ] No visible errors
- [ ] No accidental debug output
- [ ] Demo questions prepared
- [ ] Backup demo plan prepared

---

# 14. Video Production

**Owner: Rafeeq**

## Content preparation

- [ ] Final demo flow locked
- [ ] Technical explanation supplied by Karthi/Rishi
- [ ] Screen-recording scenes planned
- [ ] Architecture visual prepared
- [ ] Evidence scene captured
- [ ] Simulation scene captured
- [ ] Recommendation scene captured

## Editing

- [ ] Clean screen recordings
- [ ] Intro
- [ ] Problem statement
- [ ] TraceIQ solution
- [ ] Product walkthrough
- [ ] Evidence demonstration
- [ ] Simulation demonstration
- [ ] Architecture explanation
- [ ] Closing
- [ ] Text overlays
- [ ] Subtitles
- [ ] Audio/narration
- [ ] Transitions
- [ ] Final export
- [ ] Final video QA

---

# 15. Submission Checklist

- [ ] Final repository cleaned
- [ ] README finalized
- [ ] Architecture documented
- [ ] Navigation `.md` files audited
- [ ] Dependencies verified
- [ ] No secrets
- [ ] No temporary/debug files
- [ ] Fresh setup tested
- [ ] All automated tests passing
- [ ] Frontend build passing
- [ ] Backend startup verified
- [ ] Full demo verified
- [ ] Video finalized
- [ ] Video reviewed by all 3 members
- [ ] Submission files verified
- [ ] Final submission completed

---

# 16. Definition of Done

TraceIQ is considered **DONE** only when all of these are true:

- [ ] A user can ask a natural-language business question
- [ ] TraceIQ analyzes the underlying deterministic data
- [ ] TraceIQ identifies measurable drivers
- [ ] TraceIQ explains the result in business language
- [ ] Every important claim can be traced to evidence
- [ ] Recommendations are evidence-backed
- [ ] What-if scenarios can be simulated
- [ ] Historical and projected values are clearly separated
- [ ] LLM output does not invent unsupported numbers/claims
- [ ] Backend and frontend work together end-to-end
- [ ] Automated tests pass
- [ ] Fresh startup works
- [ ] Demo works without manual intervention
- [ ] Documentation is complete
- [ ] Video is complete
- [ ] Final repository is clean
- [ ] `main` is frozen for submission

---

# Current Priority Queue

## 🔴 P0 --- Do these first

- [ ] Rishi: review latest narrative-consistency changes
- [x] Rishi: correct unsupported causal wording
- [ ] Rishi: correct percentage inconsistencies
- [ ] Rishi: run complete Python test suite
- [ ] Rishi: manually validate metrics/drivers/simulation
- [ ] Rishi: test evidence + simulation endpoints
- [ ] Rishi: review debug output/logs
- [ ] Rishi: commit + push latest changes
- [ ] Karthi: integrate Rishi's branch
- [ ] Rafeeq: finish core UX polish
- [ ] Team: complete browser end-to-end test

## 🟠 P1 --- Then

- [ ] Edge-case testing
- [ ] Additional question validation
- [ ] Evidence UX validation
- [ ] Simulation UX validation
- [ ] Documentation audit
- [ ] Fresh-install test
- [ ] Final architecture freeze

## 🟢 P2 --- Final submission

- [ ] Demo recording
- [ ] Video editing
- [ ] Video review
- [ ] Repository cleanup
- [ ] Final README
- [ ] Final regression test
- [ ] Submission

---

# Team Ownership Summary

Area Karthi Rishi Rafeeq

---

Overall architecture **Owner** Support  
 Model/LLM architecture **Owner** Support  
 LLM prompts/evaluation **Owner** **Owner**  
 Backend integration **Owner** Support  
 Data intelligence **Owner** **Owner**  
 Evidence **Owner** QA UI
Recommendation **Owner** Support/QA UI
Simulation backend **Owner** QA UI
Frontend/UX Support **Owner**
Testing/QA Final **Owner** Frontend QA
Documentation Final review **Owner**  
 Git integration **Owner** Branch owner Branch owner
Video content/story **Owner** Support **Owner**
Video editing **Owner**
Final submission **Owner** Support Support

---

## Current status

**Foundation:** ✅ Complete\
**Core backend:** ✅ Substantially complete\
**LLM implementation:** ✅ Complete\
**LLM validation:** 🟡 In progress\
**Evidence:** 🟡 Needs final validation\
**Simulation:** 🟡 Needs final validation\
**Frontend:** 🟡 Needs final UX polish\
**Integration:** 🟡 Pending final merge\
**QA:** 🟡 In progress\
**Documentation:** 🟡 Needs final audit\
**Video:** ⬜ Pending final product freeze\
**Submission:** ⬜ Pending
