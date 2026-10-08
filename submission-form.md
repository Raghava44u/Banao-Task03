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
2. **Deterministic Geometric Optimization:** Paired Gilmore-Gomory Linear Programming for 1D structural beams with Guided Local Search / No-Fit Polygon algorithms for 2D plates, enforcing explicit **remnant-preserving rectangular drop constraints**.
3. **Operational Remnant Scoring:** Engineered a yard retrieval engine that incorporates a **crane unstacking penalty ($35/move)**, preventing the system from recommending remnants buried deep in plate stacks.
4. **Cross-Project Accounting Transfer:** Developed a fair material credit allocation rule to credit donating projects and debit receiving projects, removing the commercial barrier to shared nesting.
5. **Human-in-the-Loop Co-Pilot Interface:** Operators review side-by-side comparisons of manual vs optimized cut plans, retaining 100% final approval authority while logging 1-click reason codes to continuously calibrate shop-floor constraints.
6. **Empirical Gate & Stop Conditions:** Enforced a two-stage evaluation protocol (50–100 job Historical Replay benchmark in Week 4, followed by a live Shadow Pilot in Weeks 5–8) with explicit stop conditions.

---

### 3. Data Used
- `Given/discovery-call-notes.txt`: Verbatim transcripts from Discovery Calls 1 & 2 with Client B's Cost Control engineer and colleague.
- **Strumis ERP Data Entities (Assumed / Target):** `Job_Header`, `BOM_Requirements`, `Stock_Inventory`, `Remnant_Inventory`, and historical nesting run archives.
- **Engineering BIM / CAD Data (Assumed / Target):** Tekla Structures / SDS/2 exports in standard industry DSTV / NC1 format and 2D DXF plate boundary files.
- **Shop-Floor Telemetry:** CarTrack GPS vehicle idle logs, internal vehicle reservation bookings, and yard storage bay registers.
- **Synthetic Benchmark Dataset (`prototype/demo_benchmark.py`):** 60 cut pieces of heavy universal beam across 3 active projects, multi-project gusset/base plates (20mm S355JR), and simulated yard stack positions.

---

### 4. Technical Architecture & Optimization Engine
- **Primary Optimization Algorithms:**
  - **1D Profile Cutting Stock:** Hybrid Column Generation via Integer Linear Programming (HiGHS / CBC solver) coupled with Best-Fit Decreasing heuristic.
  - **2D Plate Nesting:** Guided Local Search (GLS) with No-Fit Polygon (NFP) collision evaluation, parameterized with a **Max-Rectangular Drop Incentive** to preserve contiguous reusable offcuts $\ge 1.5\text{m} \times 2.0\text{m}$.
  - **Yard Remnant Scorer:** Deterministic cost-benefit evaluator balancing virgin steel cost saved against crane unstack penalties and torch prep costs.
- **Candidate Architectures Benchmarked:**
  1. *Option A: Visibility / Scrap Intelligence Layer Only* (Read-only dashboards; insufficient to optimize cutting).
  2. *Option B: Commercial Off-The-Shelf (COTS) Nesting Upgrade* (High license cost; fatal user adoption risk because planners already rejected Strumis auto-nest).
  3. *Option C: Assisted Nesting & Remnant Co-Pilot [MINC]* (**Selected**: Combines deterministic optimization, cross-project credit rules, yard physics, and human review).
  4. *Option D: Autonomous AI Smart Factory* (Rejected: Extreme complexity, unacceptable safety/scrap risk, unexplainable).

---

### 5. Validation Methodology & Primary Results
- **Validation Protocol:** Two-stage evaluation: (1) Stage 1 Historical Replay Benchmark across 50–100 past completed jobs; (2) Stage 2 Live Shadow-Mode Pilot on 10 active jobs across 4 weeks.
- **Synthetic Benchmark Validation (`prototype/`):**
  - **1D Cutting Stock:** Reduced 12m stock beams from 25 to 24 (4.0% reduction in ordered steel); preserved 4.2m of prime reusable offcut; reduced true net scrap to 8.68%.
  - **2D Plate Nesting:** Reduced master 6m x 2.5m plates from 4 to 3 (2.35 tonnes saved); preserved 6.0 $m^2$ clean rectangular drop; cut gross waste from 44.75% to 26.33% (-18.42% absolute reduction on sample run).
  - **Remnant Engine:** Successfully penalized buried remnants in Position 5 while selecting accessible remnant in Position 2, netting +$149.20 net economic gain.
  - **Test Suite Status:** 4/4 automated tests passing (`pytest prototype/tests/test_prototype.py`).

---

### 6. Expected Production Performance & Business Economics
- **Baseline Annual Steel Throughput:** 80,000 tonnes/year (60,000t profiles @ 6.0% waste; 20,000t plates @ 22.5% waste = 8,100t total waste, costing $5,265,000/year at $650 net loss/t).
- **Base Case Target Outcomes:**
  - **Avoidable Material Waste Reduction:** 1.50% absolute reduction (1.0% profiles = 600t; 3.0% plates = 600t; Total = **1,200 tonnes saved/year**).
  - **Direct Steel Cost Savings:** **$780,000 / year**.
  - **Client Revision Scrap Recovery:** **$332,500 / year** (350 tonnes captured @ $950/t).
  - **Gross Annual Benefit:** **$1,112,500 / year**.
- **Financial Return Metrics:**
  - **One-Time Implementation Cost:** $280,000.
  - **Annual Recurring SaaS & Support:** $60,000 / year.
  - **Year 1 Net Economic Benefit:** **+$772,500**.
  - **Year 1 ROI:** **227.2%**.
  - **Payback Period:** **3.7 months**.
  - **3-Year NPV (@ 10% Discount Rate):** **$2,336,548**.
- **Sensitivity Range:** Conservative Scenario yields $532,500 gross benefit (56.6% Year 1 ROI, 7.7 mo payback); Upside Scenario yields $1,692,500 gross benefit (397.8% Year 1 ROI, 2.4 mo payback).

---

### 7. Data Leakage Controls & Integrity Verification
- **Audit Logging:** Every nesting recommendation, operator override, revision timestamp, and scrap bin weight is permanently logged for Cost Control reconciliation.
- **MTC & Heat Number Traceability:** Strict metallurgical validation prevents mixing incompatible steel grades (e.g. S275 vs S355JR) or violating mill test certificate compliance.
- **Physical Feasibility Gating:** All candidate nests are evaluated against machine clamp margins (25mm), torch kerf widths (4–6mm), and minimum thermal spacing (8mm) before reaching operator screens.

---

### 8. Key Operational Mechanics
1. `remnant_consolidation_penalty`: Forces parts to pack tightly against sheet edges, ensuring leftover steel forms a large, usable rectangular offcut rather than unusable perimeter strip waste.
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
- **Runtime Inference Dependencies:** 100% Local Deterministic Optimization (Python, HiGHS/CBC Linear Programming, Shapely geometric algorithms). Zero external LLMs or paid inference APIs required for core nesting.
- **Paid API Cost:** $0.00 at runtime.
- **What Was Discarded:**
  - *Discarded Large Language Models (LLMs) for geometric nesting:* LLMs cannot solve NP-hard 2D cutting stock problems or compute No-Fit Polygons.
  - *Discarded Deep Reinforcement Learning for nesting:* Extreme sample inefficiency, unpredictable collision bugs, and zero shop-floor explainability.
  - *Discarded Full Autonomous Production Automation:* Removing human planners would guarantee immediate shop-floor revolt and dangerous torch collision risks.

---

### 14. Reproducibility & Quick Run Instructions
```bash
# 1. Run the Synthetic Benchmark Harness
python prototype/demo_benchmark.py

# 2. Run the Automated Test Suite
python -m pytest prototype/tests/test_prototype.py -v
```
