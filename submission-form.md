# Structural Steel Operations & Nesting Intelligence — Task 3 V2 (Client B)
## Official Submission Form

---

### 1. General Project Information
- **Project Name:** Client B Structural Steel Material Intelligence & Assisted Nesting Co-Pilot (MINC) — Task 3 V2
- **Candidate / Lead Engineer:** Senior Forward Deployed Engineer / AI Product Solutions Architect Lead
- **Target Organization:** Client B — Tier-1 Structural Steel Fabricator (80,000 tonnes/year)
- **Repository URL:** https://github.com/Raghava44u/Banao-Task03.git
- **Target Git Branch:** `main`

---

### 2. High-Level Approach
We conducted an operational diagnostic of Client B's structural steel fabrication business based on verbatim discovery call notes. Rather than prematurely deploying an unexplainable deep-learning model or buying another black-box COTS nesting package, we designed **MINC (Material Intelligence & Assisted Nesting Co-Pilot)**:
1. **Root-Cause Alignment:** Addressed the core operational breakdown where Strumis's existing automated nesting was rejected by planners due to unusable offcuts, while project-siloed purchasing prevented cross-project steel sharing and unsequenced yard stacking buried valuable remnants.
2. **Deterministic Geometric Packing:** Implemented a working 1D Best-Fit Decreasing profile nesting engine (with section and grade segregation) and a genuine 2D Maximal Rectangles (MaxRects) plate nesting engine that generates exact part coordinates, enforces clamp margins and kerf spacing, prevents overlaps, and preserves contiguous rectangular offcuts ($\ge 3.0\text{m}^2$).
3. **Operational Remnant Scoring:** Engineered a quantity-aware yard retrieval engine that incorporates physical grid packing capacity, residual scrap cost, and a **crane unstacking penalty ($35/move)**, preventing recommendations that shop-floor crane riggers will refuse to retrieve.
4. **Cross-Project Accounting Transfer:** Developed a fair material credit allocation rule to credit donating projects and debit receiving projects, removing the commercial barrier to shared nesting.
5. **Human-in-the-Loop Co-Pilot Interface:** Operators review side-by-side comparisons of manual vs optimized cut plans, retaining 100% final approval authority while logging 1-click reason codes to continuously calibrate shop-floor constraints.
6. **Empirical Gate & Stop Conditions:** Enforced a two-stage evaluation protocol (50–100 job Historical Replay benchmark in Week 4, followed by a live Shadow Pilot in Weeks 5–8) with explicit stop conditions.

---

### 3. Data Used
- `Given/discovery-call-notes.txt`: Verbatim transcripts from Discovery Calls 1 & 2 with Client B's Cost Control engineer and colleague.
- **Strumis ERP Data Entities (Target Production):** `Job_Header`, `BOM_Requirements`, `Stock_Inventory`, `Remnant_Inventory`, and historical nesting run archives.
- **Engineering BIM / CAD Data (Target Production):** Tekla Structures / SDS/2 exports in standard industry DSTV / NC1 format and 2D DXF plate boundary files.
- **Shop-Floor Telemetry (Target Production):** CarTrack GPS vehicle idle logs, internal vehicle reservation bookings, and yard storage bay registers.
- **Synthetic Feasibility Dataset (`prototype/demo_benchmark.py`):** 60 cut pieces of heavy universal beam across 3 active projects, 76 gusset/base plates (20mm S355JR), and simulated yard stack positions.

---

### 4. Technical Architecture & Algorithmic Capabilities

#### Current Prototype Implementation (Tested & Verifiable)
- **1D Profile Cutting:** Best-Fit Decreasing (BFD) bin packing heuristic with strict segregation by `section_profile` (e.g. UB 457 vs UC 203) and `material_grade` (e.g. S355JR vs S275), explicit length guardrails ($12.0\text{m}$ max), configurable `allow_cross_project` control, and exact kerf/remnant accounting.
- **2D Plate Nesting:** Maximal Rectangles (MaxRects) bin packing heuristic with Best-Short-Side-Fit (BSSF). Generates exact $(x, y, w, l, \text{rotation})$ millimeter coordinates, prevents overlaps, enforces $5\text{mm}$ kerf and $25\text{mm}$ perimeter clamp margins, and measures actual preserved rectangular offcut dimensions.
- **Remnant Scorer:** Quantity-aware capacity evaluator balancing virgin steel cost saved against crane unstack penalties and residual scrap costs.

#### Target Production Architecture (Phase 1–2 Roadmap)
- **1D Profile Optimizer:** Gilmore-Gomory Linear Programming / Column Generation for mathematical optimality.
- **2D Plate Optimizer:** Guided Local Search (GLS) with No-Fit Polygon (NFP) collision evaluation for irregular CAD polygons.
- **Data Connectors:** Direct read-only SQL/ODBC connectors to Strumis and direct Tekla DSTV/NC1 parsers.

---

### 5. Validation Methodology & Benchmark Results
- **Validation Protocol:** Two-stage evaluation: (1) Stage 1 Historical Replay Benchmark across 50–100 past completed jobs; (2) Stage 2 Live Shadow-Mode Pilot on 10 active jobs across 4 weeks.
- **Synthetic Benchmark Validation (`prototype/`):**
  - **1D Cutting Stock:** Stock 12m universal beams reduced from 25 to 24 (4.0% reduction in ordered steel) when cross-project pooling is enabled; preserves 4.2m of prime reusable offcut; reduces true net scrap to 8.79%.
  - **2D Plate Nesting:** Master 6m x 2.5m plates reduced from 4 to 3 (2.35 tonnes saved) via cross-project MaxRects packing; preserves a verified $2.45\text{m} \times 2.76\text{m}$ ($6.77\text{ m}^2$) prime rectangular drop with zero part overlap.
  - **Remnant Engine:** Accurately allocates quantity (1 of 10) to accessible offcut, netting +$106.85 after crane and residual scrap penalties.
  - **Test Suite Status:** **11/11 automated tests passing** (`pytest prototype/tests/test_prototype.py`), including 6 regression tests covering all audit failure modes.

---

### 6. Target Production Performance & Business Economics
- **Baseline Annual Steel Throughput:** 80,000 tonnes/year (60,000t profiles @ 6.0% waste; 20,000t plates @ 22.5% waste = 8,100t total waste, costing $5,265,000/year at $650 net loss/t).
- **Target Planning Scenarios (Subject to Historical Replay Verification):**
  - **Target Avoidable Material Waste Reduction:** 1.50% absolute reduction (1.0% profiles = 600t; 3.0% plates = 600t; Total = **1,200 tonnes saved/year**).
  - **Projected Direct Steel Cost Savings:** **$780,000 / year**.
  - **Projected Client Revision Scrap Recovery:** **$332,500 / year** (350 tonnes captured @ $950/t).
  - **Target Gross Annual Benefit:** **$1,112,500 / year**.
- **Financial Return Metrics:**
  - **One-Time Implementation Cost:** $280,000 (milestone-gated).
  - **Annual Recurring SaaS & Support:** $60,000 / year.
  - **Target Year 1 Net Economic Benefit:** **+$772,500**.
  - **Target Year 1 ROI:** **227.2%**.
  - **Payback Period:** **3.7 months**.
  - **3-Year NPV (@ 10% Discount Rate):** **$2,336,548**.
- **Sensitivity Range:** Conservative Scenario yields $532,500 gross benefit (56.6% Year 1 ROI, 7.7 mo payback); Upside Scenario yields $1,692,500 gross benefit (397.8% Year 1 ROI, 2.4 mo payback).

---

### 7. Data Controls & Manufacturing Feasibility
- **Audit Logging:** Every nesting recommendation, operator override, revision timestamp, and scrap bin weight is permanently logged for Cost Control reconciliation.
- **MTC & Section Traceability:** Strict metallurgical and structural validation prevents mixing incompatible steel grades (e.g. S275 vs S355JR) or cross-cutting incompatible profile sections (e.g. UB vs UC).
- **Physical Feasibility Gating:** All candidate nests are evaluated against machine clamp margins (25mm), torch kerf widths (5mm), and piece length limits before reaching operator screens.

---

### 8. Key Operational Mechanics
1. `maxrects_remnant_detection`: Packs parts compactly against sheet edges, measuring actual remaining free rectangles to verify whether a reusable offcut ($\ge 3.0\text{m}^2$) is physically cuttable.
2. `crane_unstack_penalty`: Deducts $35 per plate moved from the economic value of stored remnants, preventing recommendations that shop-floor crane riggers will refuse to retrieve.
3. `cross_project_material_credit`: Automated accounting ledger entry crediting the donating project and debiting the receiving project at standard raw material cost.
4. `revision_diff_audit`: Timestamped line-item comparison between Tekla drawing releases identifying pre-cut parts invalidated by client revisions for contractual reimbursement.
5. `human_veto_reason_capture`: Captures 1-click reason codes when planners reject recommendations, continuously fine-tuning optimization constraints.

---

### 9. Root-Cause Analysis Conclusion
- **Client's Initial Belief:** Cost Control believed they needed an "AI model for nesting" because manual planning was causing high waste.
- **FDE Empirical Finding:** The failure is operational and systemic:
  - The client already owned Strumis auto-nesting, but planners bypassed it because standard auto-nesting generates jagged, unusable offcuts.
  - Steel was purchased in single-project silos, preventing multi-project batching.
  - Offcuts were stacked randomly up to 8 plates deep without physical location tracking, making retrieval more expensive than cutting virgin plate.
  - Revisions lacked audit trails, causing the fabricator to absorb client change costs.
- **Conclusion:** An AI deep-learning model would fail completely. The correct intervention is a **human-in-the-loop assisted optimization co-pilot** that solves remnant preservation, crane retrieval friction, and cross-project cost allocation.

---

### 10. System & Integration Specification
- **Strumis Connector:** Read-only direct SQL extraction via ODBC every 15 minutes.
- **CAD Parser:** Automated ingestion of Tekla Structures DSTV / NC1 CNC files and 2D DXF plate contours.
- **Architecture:** Lightweight Docker container deployed on a local on-premises agent inside the client LAN, paired with an optional single-tenant cloud optimization engine. 100% on-premises deployment supported if mandated by client confidentiality.
- **Export Hook:** Approved cut plans exported directly to Strumis nesting tables for standard CNC post-processing.

---

### 11. User Interface
- **Framework:** Web-based and desktop Electron Co-Pilot Desk (`app/copilot_desk`).
- **Operator Features:** Side-by-side visual layout comparison (Manual vs MINC), steel utilization %, scrap delta, preserved remnant dimensions, crane unstack move count, 1-click "Accept Plan" button, and structured rejection reason dropdown.

---

### 12. Known Failure Modes & Stop Conditions
1. **Unresolvable Yard Stacking Friction:** If physical yard disorganization is so severe that crane riggers refuse to pull any remnants, remnant reuse is deactivated in Phase 1, focusing optimization strictly on virgin plate yield.
2. **Contractual Co-Nesting Prohibitions:** If client contracts legally prohibit shared steel (e.g. government/defense work), the system activates a strict single-project constraint flag.
3. **Explicit Stop Conditions:** The project is halted if:
   - Week 4 Historical Replay proves avoidable waste reduction is $<0.5\%$.
   - Inventory accuracy for yard steel is $<70\%$.
   - Planners reject $>50\%$ of recommendations due to uncapturable shop-floor machine constraints.

---

### 13. AI Tools & Costs Disclosure
- **Development Coding Assistant:** Claude Code & Gemini CLI (Agentic pair-programming, test authoring, and documentation architecture).
- **Runtime Inference Dependencies:** 100% Local Deterministic Optimization (Python, HiGHS/CBC Linear Programming, MaxRects geometric algorithms). Zero external LLMs or paid inference APIs required for core nesting.
- **Paid API Cost:** $0.00 at runtime.
- **What Was Discarded:**
  - *Discarded Large Language Models (LLMs) for geometric nesting:* LLMs cannot solve NP-hard 2D cutting stock problems or compute millimeter-precise coordinates.
  - *Discarded Deep Reinforcement Learning for nesting:* Extreme sample inefficiency, unpredictable collision bugs, and zero shop-floor explainability.
  - *Discarded Full Autonomous Production Automation:* Removing human planners would guarantee immediate shop-floor revolt and dangerous torch collision risks.

---

### 14. Reproducibility & Quick Run Instructions
```bash
# 1. Run the Benchmark Harness
python prototype/demo_benchmark.py

# 2. Run the Automated Test Suite (11 passing tests)
python -m pytest prototype/tests/test_prototype.py -v
```
