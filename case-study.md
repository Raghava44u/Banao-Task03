# Client B: Structural Steel Operations & Material Intelligence
## Forward Deployed Engineering Case Study & Production Pilot Proposal

**Client:** Tier-1 Structural Steel Fabricator (80,000 tonnes/year | 10–15 concurrent projects)  
**Author:** Senior Forward Deployed Engineer / AI Product Solutions Architect  
**Primary Client Contact:** Cost Control Engineering Lead  
**Systems Landscape:** Strumis Steel ERP/Nesting, Tekla BIM/CAD (DSTV/NC1), CNC Cutting Tables, 13-Trailer Fleet, CarTrack GPS  

---

## 1. Executive Summary

Client B fabricates approximately **80,000 tonnes of structural steel annually** across 10 to 15 concurrent projects. In preliminary discovery calls, Cost Control requested guidance on "AI for nesting optimisation," reporting substantial material losses: **20% to 25% waste on steel plate**, **5% to 10% on structural profiles**, and an **overall average waste of 7% to 10%** across operations. At current prime steel prices ($950/t) and scrap salvage rates ($300/t), this equates to an annual financial loss of over **$5.2M in scrapped steel**.

However, a disciplined Forward Deployed Engineering (FDE) operational audit reveals that **the client’s core bottleneck is not the absence of an AI nesting algorithm**. Rather, it is a compound operational disconnect:
1. **The Strumis Auto-Nest Paradox:** The client *already owns* commercial automated nesting software inside Strumis, but human operators deliberately bypass it, claiming manual nesting saves more steel. Cost Control has zero data to verify or refute this claim.
2. **Project Accounting Silos:** Steel is procured and 100% cost-loaded to individual projects, preventing cross-project plate batching and penalizing remnant transfers.
3. **Physical Yard Retrieval Friction:** Plates are stored in unsequenced yard stacks up to 8 plates deep; shop-floor crane riggers ignore recorded offcuts because digging them out causes massive crane delays.
4. **Conflated Waste Classifications:** The reported 7–10% waste conflates unavoidable torch kerf, client-billable drawing revisions, unrecovered remnants, and genuine geometric packing inefficiencies.

**The Recommended Solution:** We recommend **NOT** building an unexplainable deep-learning model or buying another black-box COTS nesting tool. Instead, we propose the **Material Intelligence & Assisted Nesting Co-Pilot (MINC)**: a human-in-the-loop decision-support system that integrates with Strumis and CAD exports. MINC pairs a deterministic remnant-preserving optimization engine with a cross-project material attribution mechanism and an operational remnant retrieval scorer that accounts for crane unstacking penalties. (A functional prototype demonstrating 1D Best-Fit Decreasing and 2D Maximal Rectangles packing is implemented and verified in `prototype/demo_benchmark.py`).

**Target Planning Scenario (Subject to Historical Replay Verification):**
- **1,200 tonnes of avoidable scrap targeted annually** (1.50% absolute reduction in material waste).
- **350 tonnes of client-driven revision scrap captured** for contractual reimbursement ($332,500).
- **Target Gross Annual Benefit:** **$1,112,500 / year**.
- **Investment:** $280,000 one-time implementation + $60,000/year recurring SaaS/support.
- **Projected Economics:** **227.2% Year 1 ROI** with a **3.7-month payback period** and a 3-Year NPV of **$2.34M**.

---

## 2. Problem Understanding & Operational Diagnosis

During discovery, the Cost Control engineer stated:
> *"Honestly, even we don't have a clear idea of how AI can be integrated into our company... If I have to pick one, it's nesting... Our nesting is planned by hand. We don't have the data to say how much steel is wasted, how much of that we could have prevented, or which material is sitting unused."*

A superficial response would be to pitch an "AI-driven nesting platform." A Forward Deployed Engineer must look deeper into the physical and organizational reality:

```
[Drawing Released] ──> [Project-Siloed PO] ──> [Manual Nesting] ──> [CNC Cutting] ──> [Yard Dumping]
        │                      │                       │                   │                  │
        ▼                      ▼                       ▼                   ▼                  ▼
 Client Revisions       100% Cost Loaded        Strumis Auto-Nest    Kerf & Margins     Remnants Buried
 Lack Audit Trail        Blocks Sharing          Bypassed by Team     Not Measured       in Deep Stacks
 ($332k unbilled)      (High Drop Waste)       (Zero Baseline Data) (Opaque Scrap)      ($1.2M Abandoned)
```

### The Root Causes Behind the Symptoms:
1. **Zero Ground-Truth Measurement:** Cost Control does not possess a structured baseline separating unavoidable process scrap (torch kerf, skeleton web integrity, clamp margins) from avoidable geometric scrap.
2. **Shop-Floor Rejection of Auto-Nesting:** Commercial automated nesting engines optimize for single-sheet fill density, scattering parts and leaving jagged, unusable "Swiss-cheese" skeletons. Human operators nest manually because they intuitively preserve rectangular offcuts, but humans cannot mentally optimize 200 parts across 15 active projects.
3. **Physical-Digital Inventory Disconnect:** Strumis logs offcuts digitally, but the physical yard lacks location tracking. Moving 4 heavy plates to retrieve a 1.2m offcut costs ~$105 in crane time and delays the cutting table. Operators naturally cut fresh virgin plates instead.
4. **Accounting Disincentives:** If Project A purchases a plate, its budget absorbs 100% of the cost. If an offcut is left over, Project A receives no credit, and Project B has no mechanism to buy it cleanly.

---

## 3. Stakeholder Analysis & As-Is Process Reconstruction

### 3.1 Stakeholder Alignment Matrix
Crucially, only Cost Control attended the discovery calls. The table below outlines the full operational landscape:

| Stakeholder | Primary Incentive / Metric | Need from System | Risk of Resistance | Decision Owned |
| :--- | :--- | :--- | :--- | :--- |
| **Cost Control (Contact)** | Project margin variance, scrap $/tonne | Empirical waste baseline; revision cost recovery | Low (project champion) | Budget sign-off & financial auditing |
| **Nesting Team (Absent)** | Nesting turnaround speed, machine cutability | Explainable nesting co-pilot; zero complex rework | **VERY HIGH:** Will reject black-box automation that produces uncuttable nests | Final nest plan sign-off & NC generation |
| **Engineering / Detailing (Absent)** | Model release schedule, RFI resolution | Automated drawing diffs; revision tracking | Medium: Resents administrative overhead | CAD/DSTV drawing release & revision control |
| **Yard / Rigging (Absent)** | Crane utilization, zero plate re-handling | Realistic retrieval plans; no unstacking deep piles | **HIGH:** Will ignore offcut pull tickets if plates are buried | Physical steel storage & material staging |
| **Shop Floor / CNC Sizing (Absent)** | Table uptime, tons cut/shift, zero torch head crashes | Clean lead-in paths, heat dissipation, rigid skeletons | Medium: Wary of warped plates or small parts falling into table | Physical CNC cutting & scrap bin dumping |
| **Project Managers (Absent)** | On-time delivery milestones, project P&L | Guaranteed plate availability for project schedule | Medium: Wary of sharing steel across projects | Project schedule & priority overrides |
| **Procurement (Absent)** | Purchase order batching, supplier discounts | Advance cut-list visibility for mill plate orders | Low: Welcomes consolidated buying | Steel supplier purchase orders |
| **Executive Leadership (Absent)** | EBITDA, company ROIC, asset utilization | Verified bottom-line dollar savings; low capital risk | Low: Driven by margin expansion | Pilot capital expenditure approval |

### 3.2 As-Is Process Reconstruction
*Status Legend: [Confirmed by Client] | [Inferred from Industry Benchmark] | [Unknown / To Validate]*

1. **Bidding & Estimation:** BD bids; Estimation prices based on historical scrap percentages. *[Confirmed]*
2. **Planning & Detailing:** Planning sets delivery milestones; Engineering models structural frame in Tekla/CAD and releases fabrication drawings. *[Confirmed]*
3. **Material Purchasing:** Steel purchased in standard full sizes (e.g. 12m beams, 6m x 2.5m plates) per project. Cost loaded 100% to project. *[Confirmed]*
4. **Digital Nesting:** Nesting team receives drawings and nests manually in Strumis, bypassing auto-nesting. *[Confirmed]* Cross-project nesting is not done due to cost loading. *[Confirmed]*
5. **Physical Cutting (Sizing):** CNC machines execute cutting. *[Confirmed]* Kerf, slag, and small scrap dumped into scrap bins without weighing. *[Inferred]*
6. **Remnant Management:** Offcuts recorded in Strumis. *[Confirmed]* Placed in store yard without sequencing; required pieces end up at stack bottoms. *[Confirmed]* Operators re-cut fresh steel rather than unstacking buried remnants. *[Inferred]*
7. **Downstream Fabrication:** Fitting, welding, coating (painting/galvanizing/fireproofing), and trailer dispatch. *[Confirmed]*

---

## 4. What We Know vs. What We Don't Know

```
+------------------------------------------------+------------------------------------------------+
|             CONFIRMED FACTS                    |             CRITICAL UNKNOWNS (P0)             |
| - 80,000 tonnes/year across 10-15 projects     | - Exact kerf vs avoidable waste breakdown      |
| - 20-25% plate waste; 5-10% profile waste      | - Concrete reason nesting team rejects auto-nest|
| - Strumis ERP used; auto-nest bypassed         | - Digital format of drawings (Tekla/DSTV/DXF)  |
| - Material cost loaded 100% to projects        | - Accessibility of historical nesting logs     |
| - Store yard unsequenced; plates buried deep   | - Contractual permissibility of shared steel   |
| - 13 owned trailers; CarTrack GPS installed    | - Realized scrap salvage price ($/tonne)       |
+------------------------------------------------+------------------------------------------------+
```
*(See [Appendix 1: Discovery Questions](file:///D:/Banao-technologies/Task-3/appendix/discovery-questions.md) for full prioritized P0/P1/P2 question matrix and [Appendix 2: Assumptions](file:///D:/Banao-technologies/Task-3/appendix/assumptions.md) for detailed operational assumptions.)*

---

## 5. Evaluation of Solution Options

We evaluated four architectural approaches across ten industrial feasibility dimensions:

| Dimension | Option A: Visibility / Scrap Intelligence Layer | Option B: COTS Nesting Software Upgrade | Option C: Assisted Nesting & Remnant Co-Pilot (MINC) | Option D: Autonomous AI Smart Factory |
| :--- | :--- | :--- | :--- | :--- |
| **1. Expected Annual Value** | Moderate ($300k–$400k) | High on paper ($600k) | **Very High ($800k–$1.5M)** | Unattainable in practice |
| **2. Implementation Complexity** | Low (3–4 weeks) | Medium (3–4 months) | **Medium (8–10 weeks)** | Extreme (18–24 months) |
| **3. Data Requirements** | Strumis DB read-only | Standard CAD/DXF | **Strumis DB + CAD + Yard logs**| Full digital twin + IoT |
| **4. Integration Complexity**| Very Low (SQL/ODBC) | High (ERP swap/add-on) | **Moderate (Strumis 2-way hook)**| Extreme (All shop machines) |
| **5. User Adoption Risk** | Very Low | **FATAL (History repeats)**| **Low (Human-in-the-Loop desk)** | **FATAL (Total rejection)** |
| **6. Time to First Value** | 4 weeks | 16 weeks | **6 weeks (Replay benchmark)** | >12 months |
| **7. Physical Safety / Scrap Risk**| None (Analytics only) | High (Machine crashes) | **Very Low (Human signs off)** | Catastrophic |
| **8. Explainability** | High (Dashboards) | Low (Black-box vendor) | **High (Visual delta + cost)** | Zero (Neural black-box) |
| **9. Total Year 1 Cost** | $90,000 | $220,000 | **$340,000** | >$1,500,000 |
| **10. Scalability Wedge** | Limited (Read-only) | Low (Siloed software) | **High (Platform for yard/fleet)**| Unstable foundation |
| **DECISION** | *Included as Subsystem* | **REJECTED** | **RECOMMENDED SOLUTION** | **REJECTED** |

---

## 6. Recommended Solution: The MINC Platform

We recommend deploying **MINC (Material Intelligence & Assisted Nesting Co-Pilot)** as a targeted operational wedge.

```
                      +---------------------------------------+
                      |       MINC DECISION ENGINE            |
                      |                                       |
  [Strumis ERP] ───>  | 1. Ingestion & Geometry Validation    |
  [Tekla CAD]   ───>  | 2. Remnant-Preserving 1D/2D Optimizer | ───> [Co-Pilot Desk]
  [Yard Inventory]──> | 3. Crane Depth Penalty Scorer         |      (Side-by-side review)
                      | 4. Cross-Project Cost Attribution     |               │
                      +---------------------------------------+               ▼
                                                                     [Operator Approves]
                                                                              │
                                                                              ▼
                                                                     [Strumis NC Cutting]
```

### Why This is the Right First Step:
1. **Respects Human Expertise:** Operators maintain 100% final approval authority. The system acts as a high-speed calculator finding combinations across 15 projects that no human can compute manually.
2. **Solves the Accounting Blocker:** Automatically generates an internal cost-transfer record crediting Project A when Project B consumes its remnant or shares a raw plate.
3. **Solves the Yard Reality:** Features a **Crane Depth Penalty Scorer** ($35/unstack move). If a remnant is buried 5 plates deep, MINC mathematically skips it and nests virgin stock, matching shop-floor physics.
4. **Deterministic Optimization, NOT LLMs for Geometry:** The current working prototype implements 1D Best-Fit Decreasing and 2D Maximal Rectangles (MaxRects) packing. The production roadmap (Phases 1–2) scales this to Gilmore-Gomory Linear Programming for 1D and Guided Local Search with No-Fit Polygons for complex polygonal CAD parts. LLMs are strictly confined to parsing text revision markups.

---

## 7. Solution Engineering & Optimization Logic

### 7.1 Objective Function
For any nesting cluster across active projects, MINC minimizes total economic cost:

$$\min \quad \sum_{m \in M_{\text{virgin}}} C_{\text{raw}}(m) + \sum_{r \in R_{\text{yard}}} \left[ C_{\text{crane\_unstack}}(r) + C_{\text{prep}}(r) \right] - \sum_{k \in \text{Drops}} V_{\text{remnant}}(k) + \sum_{p \in P} \text{Penalty}_{\text{heat}}(p)$$

**Subject to Physical & Fabrication Constraints:**
1. **Geometric Containment & Non-Overlap:** $(p_i \cap p_j = \emptyset)$ evaluated via No-Fit Polygons (NFP) with $5\text{mm}$ kerf margin.
2. **Remnant Consolidation:** Maximizes contiguous rectangular drop area: $\text{Drop} \ge 1,500\text{mm} \times 2,000\text{mm}$.
3. **Metallurgical Alignment:** Material grade (e.g. S355JR vs S275) and thickness must match exactly; rolling/grain direction constraints respected for bending gussets.
4. **Delivery Window Batching:** Parts can only be co-nested across projects if fabrication required dates are within a 10-day window.

*(See [Appendix 4: Technical Architecture](file:///D:/Banao-technologies/Task-3/appendix/architecture.md) for detailed data schemas and pipeline specifications.)*

---

## 8. Evaluation Plan & Test Protocol

Success must be validated empirically before touching live production.

### 8.1 Primary & Secondary Metrics
- **Primary Metric:** **Avoidable Material Waste Reduction (%)** on plate and profile runs.
- **Secondary Metrics:**
  - Net Dollar Scrap Savings ($/month).
  - Billable Client Revision Scrap Captured ($/month).
  - Reusable Remnant Inventory Turnover Rate.
  - Nesting Planner Acceptance Rate of Recommendations (Target: $\ge 75\%$).
  - Zero increase in CNC torch collisions, plate warping, or fabrication defects.

### 8.2 Two-Stage Pilot Protocol
1. **Stage 1: Historical Replay Benchmark (Weeks 3–4):**
   - Ingest **50 to 100 historical completed jobs** from the past 12 months.
   - Run MINC on identical BOMs, raw plates, and machine constraints.
   - Measure actual historical steel used vs MINC proposed steel.
   - **Gate 1 Success Threshold:** MINC must demonstrate $\ge 1.0\%$ absolute scrap reduction on identical historical data.
2. **Stage 2: Live Shadow-Mode Pilot (Weeks 5–8):**
   - MINC runs in parallel with active nesting team on 10 live jobs.
   - Operators review MINC candidate nests alongside their manual plans.
   - Track operator acceptance rate and log concrete rejection reasons.

### 8.3 Explicit Stop Conditions
The project will be **halted or re-scoped** if:
- Historical replay reveals that avoidable nesting waste is $<0.5\%$ (proving manual nesting is already optimal).
- Physical yard inventory accuracy is $<70\%$ (remnants logged in software do not physically exist).
- Operators reject $>50\%$ of recommendations due to uncapturable CNC machine anomalies.
- Client contract audits strictly prohibit cross-project steel accounting transfers.

---

## 9. Phased Build Plan

```
Phase 0: Discovery & Audit (W1-2)    ──> Phase 1: Replay Prototype (W3-4)   ──> Phase 2: Shadow Pilot (W5-8)
- Onsite interviews (Nesting, Yard)       - Ingest 50-100 historical jobs        - Side-by-side operator co-pilot
- Strumis database & CAD audit            - Benchmark Manual vs Auto vs MINC     - Log overrides & crane moves
- GATE: Ground truth data verified        - GATE: >=1.0% verified replay delta   - GATE: >=75% acceptance rate
```

- **Phase 0: Operational Audit & Data Foundation (Weeks 1–2):** Interview nesting, yard, and engineering teams; map Strumis schema; inspect physical yard stacking.
- **Phase 1: Ingestion Pipeline & Historical Replay (Weeks 3–4):** Build DSTV/DXF parsers; execute 100-job historical replay benchmark.
- **Phase 2: Live Shadow Pilot & Co-Pilot Desk (Weeks 5–8):** Deploy operator UI; run shadow pilot; calibrate crane unstack penalties.
- **Phase 3: Production Rollout & Value Verification (Weeks 9–12):** Activate two-way Strumis sync; reconcile actual scrap bin weights with Cost Control; initiate monthly recurring savings audit.

---

## 10. Cost Model & Business Economics

### 10.1 Multi-Scenario Sensitivity Matrix (80,000 Tonnes / Year)

$$\text{Annual Baseline Loss} = 8,100\text{ tonnes waste} \times \$650\text{ net loss/tonne} = \$5,265,000\text{ / year}$$

| Scenario | Avoidable Waste Reduction | Material Saved | Direct Savings (@ $650/t) | Revision Recovery (@ $950/t) | Gross Annual Benefit | Year 1 Net Benefit | Year 1 ROI | Payback |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Conservative** | $0.75\%$ absolute | $600\text{ t}$ | $\$390,000$ | $\$142,500$ ($150\text{ t}$) | **$\$532,500$** | $\$192,500$ | **$56.6\%$** | $7.7\text{ mo}$ |
| **Base Case** | **$1.50\%$ absolute** | **$1,200\text{ t}$**| **$\$780,000$**| **$\$332,500$ ($350\text{ t}$)** | **$\$1,112,500$**| **$\$772,500$**| **$227.2\%$**| **$3.7\text{ mo}$**|
| **Upside Case** | $2.25\%$ absolute | $1,800\text{ t}$ | $\$1,170,000$ | $\$522,500$ ($550\text{ t}$) | **$\$1,692,500$**| $\$1,352,500$| **$397.8\%$**| **$2.4\text{ mo}$**|

*(All formulas and 3-Year NPV models detailed in [Appendix 3: Calculations](file:///D:/Banao-technologies/Task-3/appendix/calculations.md).)*

### 10.2 Commercial Pricing Structure
- **One-Time Implementation Fee:** **$280,000** (Milestone-based: 30% kickoff, 40% historical replay gate, 30% validated pilot completion).
- **Annual Recurring SaaS & Support:** **$60,000 / year** (Optimization cloud engine, maintenance, and ongoing algorithm calibration).

---

## 11. Operational Risk Matrix

| Risk | Prob. | Impact | Mitigation Strategy | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Nesting Team Operator Resistance**| High | High | Human-in-the-Loop desk; operator retains veto; 1-click reason logging; incentives tied to scrap reduction. | FDE Lead |
| **Yard Remnant Phantom Inventory** | High | High | Strict Remnant Scorer filters out drops buried $>3$ deep; weekly cycle-counting of top stacks. | Yard Mgr / FDE |
| **Cross-Project Accounting Rejection**| Med | High | Pre-cleared internal credit transfer rule; strict boolean flag `allow_cross_project=FALSE` for audit-restricted jobs. | Cost Control |
| **Thermal Warping on Cut Table** | Med | High | Interleaved cut-sequence path generation; enforcement of 8mm thermal bridge margins between parts. | Nesting Lead |
| **Drawing Revision Desynchronization**| Med | Med | Automated Revision Diff Engine alerts planner immediately if nested parts are modified in Tekla. | Eng Lead / FDE |

---

## 12. Scope Boundaries: What We Deliberately Will NOT Build

To ensure delivery within 8 weeks, the following items are strictly out of scope for Phase 1:
- **NO Autonomous Cutting Machine Control:** MINC will never send raw G-code directly to CNC tables; all exports pass through Strumis post-processors.
- **NO Replacement of Nesting Planners:** Humans remain in the loop for every production run.
- **NO Deep Learning for Geometry:** 2D packing is handled via deterministic mathematical programming, not LLMs or black-box neural networks.
- **NO Trailer Loading & Yard Robotics (Yet):** Fleet dispatch and mobile crane automation will only be addressed after nesting and inventory data are stabilized.

---

## 13. Future Opportunities Roadmap

Nesting serves as the high-ROI operational wedge. Once the data pipeline is operational, the platform naturally expands:

```
[Phase 1 Wedge: MINC Nesting Co-Pilot] ($1.11M/yr value | Weeks 1-8)
         │
         ├───> [Phase 2: Drawing Revision & Engineering Audit] ($350k/yr recovery | Weeks 9-16)
         │
         ├───> [Phase 3: Yard Storage & Dynamic Crane Staging] ($250k/yr crane savings | Months 5-8)
         │
         └───> [Phase 4: Fleet & Trailer Dispatch Optimizer] ($200k/yr hire reduction | Months 9-12)
```

---

## 14. Conclusion & Next Steps

Client B does not need generic AI buzzwords or a speculative multi-million-dollar digital overhaul. They need an industrial-grade **Material Intelligence Co-Pilot** that solves the real operational blockers: baseline visibility, remnant preservation, and crane retrieval friction.

**Immediate Next Steps (Week 1):**
1. Authorize Phase 0 Operational Discovery & Data Audit.
2. Conduct 45-minute discovery sessions with the Nesting, Detailing, and Yard leads.
3. Extract 50 historical Strumis nesting files to execute the Stage 1 Historical Replay Benchmark.
