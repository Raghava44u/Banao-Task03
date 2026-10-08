# Appendix 2: Explicit Operational & Technical Assumptions

Every assumption in this document is explicitly grounded either in the verbatim discovery call notes from **Client B** or established industrial benchmarks in structural steel fabrication. All assumptions are subject to verification during Phase 0 (Discovery & Data Audit).

---

## 1. Operating Baseline & Capacity Assumptions

### A1. Annual Throughput & Steel Product Mix
- **Client Fact:** 80,000 tonnes/year overall capacity (~7,000–8,000 tonnes/month); 10–15 concurrent active projects.
- **Assumption:** 
  - Heavy structural profiles (Universal Columns, Universal Beams, Channels, Hollow Sections, Angles) comprise **75% of volume = 60,000 tonnes/year**.
  - Structural steel plates (Base plates, connection gussets, stiffeners, splice plates, built-up girder webs/flanges) comprise **25% of volume = 20,000 tonnes/year**.
- **Rationale:** Standard heavy industrial and commercial structural steel fabrications (e.g., warehouses, industrial plants, multi-story frames) exhibit a 70:30 to 80:20 profile-to-plate weight ratio. Furthermore, blending 75% profiles at 6.0% waste and 25% plates at 22.5% waste yields a total blended waste of **10.1%**, perfectly matching the client's stated range of **7% to 10% overall average waste**.
- **Sensitivity:** High for plate savings, moderate for overall economics.
- **Validation:** Audit past 12 months of Strumis purchasing and inventory logs during Phase 0.

### A2. Raw Steel & Scrap Metal Commercial Economics
- **Client Fact:** Strumis tracks costs loaded to projects; steel is purchased per project. Exact unit prices were not disclosed on calls.
- **Assumption:**
  - Prime structural steel purchase price: **$950 / tonne** (blended average for S355 / S275 grades).
  - Scrap metal salvage recovery value (re-melt scrap sold to recyclers): **$300 / tonne**.
  - Net economic loss per tonne of unrecovered scrap: **$950 - $300 = $650 / tonne**.
- **Rationale:** Global structural steel benchmark prices in industrial fabrication typically range from $850 to $1,100/tonne for mill plate and beams, while heavy structural scrap trades between $250 and $350/tonne.
- **Sensitivity:** Linear impact on dollar savings. If net loss is $550/t (-15%), base savings decrease from $1.11M to $0.99M; if net loss is $750/t (+15%), base savings increase to $1.23M.
- **Validation:** Review Cost Control's scrap sales invoices and mill purchase orders in Week 1.

---

## 2. Nesting & Process Assumptions

### A3. Root Cause of Strumis Automated Nesting Rejection
- **Client Fact:** Strumis has an automatic nesting option, but operators bypass it, claiming manual nesting saves more material. Cost Control admits they do not have the data to confirm or refute this.
- **Assumption:** The nesting team's claim is partially true regarding remnant usability and shop-floor constraints, but false regarding global geometric packing efficiency:
  1. *Remnant Geometry:* Commercial auto-nesting tends to scatter small parts across the full sheet to maximize instant plate area fill, leaving irregular "Swiss-cheese" skeletons with zero reusable drop value. Human operators deliberately cluster parts to one side, preserving a clean rectangular offcut.
  2. *Shop-Floor Cutting Constraints:* Auto-nesters often ignore torch lead-in pierce points, heat distortion dissipation (thermal expansion causing cut parts to pinch the torch), and plate edge clamp clearances.
  3. *Global Multi-Job Visibility:* Human operators cannot mentally solve multi-dimensional bin packing across 10–15 projects and 200 part geometries simultaneously.
- **Impact & Action:** We must not replace the operators with a black-box auto-nester. Instead, we implement a **Human-in-the-Loop Co-Pilot** that optimizes for *compact rectangular remnant preservation* and displays side-by-side metrics.
- **Validation:** Replay 20 historical jobs through Strumis auto-nest vs manual nests vs our optimizer in Phase 1.

### A4. Physical Cutting Constraints & Process Waste Breakdown
- **Client Fact:** CNC cutting machines sizing plates and profiles in factory; plate waste reported at 20–25%, profiles at 5–10%.
- **Assumption:**
  - **Plate Waste Breakdown (22.5% baseline):**
    - Unavoidable process loss (torch kerf 4–6mm, plate clamp edge margins 25mm, skeletal bridge webs): **~3.5%**.
    - Unrecovered / abandoned offcuts (usable drops dumped in yard): **~6.0%**.
    - Avoidable geometric packing inefficiency: **~9.0%**.
    - Scrapped parts due to untracked engineering/client drawing revisions: **~4.0%**.
  - **Profile Waste Breakdown (6.0% baseline):**
    - Unavoidable saw kerf (5mm) and end-trim facing loss: **~1.5%**.
    - Short end-drops (<1.5m) scrapped: **~3.0%**.
    - Avoidable cut-length sequencing inefficiency: **~1.5%**.
- **Rationale:** Laser/plasma/oxyfuel torches physically vaporize steel into slag along the cut contour (kerf). Structural fabricators also require a minimum 20–30mm perimeter margin to ensure plate clamping rigidity on CNC water/downdraft cutting beds.
- **Validation:** Measure actual CNC cut contours and skeleton weights during shop-floor visit in Week 1.

---

## 3. Data & Systems Architecture Assumptions

### A5. Systems of Record & Data Formats
- **Client Fact:** Strumis is the main software and works like an ERP for all data, including nesting. Engineering releases drawings. CNC machines execute cutting.
- **Assumption:**
  - Strumis runs on an accessible Microsoft SQL Server or PostgreSQL relational database.
  - Engineering models in 3D BIM software (Tekla Structures, SDS/2, or Advance Steel) and exports industry-standard **DSTV / NC1** format files for CNC machinery and **2D DXF** files for plate contours.
  - Nesting cut plans, plate allocations, and BOMs are digitally archived in Strumis.
- **Contingency:** If Strumis direct SQL access is restricted by IT security policies, we will implement an automated CSV/XML scheduled export/import agent that polls Strumis export directories every 15 minutes.
- **Validation:** Inspect Strumis server connectivity and sample NC1/DXF exports on Discovery Day 2.

### A6. Drawing Revision Frequency & Traceability
- **Client Fact:** Drawings change continuously. The client has no clear data record of revisions, but noted: "When a loss comes from a client revision, we can claim it back. But right now we don't know how many tonnes we lose to our own engineering errors."
- **Assumption:**
  - Revisions occur on 40–60% of projects after drawing release.
  - 60% of revision-induced scrap is caused by client design changes (contractually reimbursable), while 40% stems from internal detailing clashes or fabricator drafting errors.
  - Capturing and timestamping BOM changes between revision releases will allow the client to bill back **150 to 500 tonnes/year of revision scrap** to clients that is currently absorbed as unallocated fabrication loss.
- **Validation:** Audit 10 completed project revision logs and client change orders in Phase 0.

---

## 4. Yard Operations & Accounting Assumptions

### A7. Cross-Project Material Allocation & Accounting
- **Client Fact:** Steel costs are loaded 100% to the specific purchasing project. The client is unsure how feasible it is to split material between projects without consulting the team.
- **Assumption:**
  - Physical cross-project co-nesting (cutting parts for Project A and Project B from the same raw plate or 12m beam) is legally permissible under general commercial fabrication contracts, provided material grade, mill test certificates (MTC), and project delivery schedules align.
  - An internal **"Material Credit Transfer Protocol"** can be configured in Cost Control: Project B pays a standard internal transfer rate to Project A for the exact weight of steel consumed, crediting Project A's job-cost ledger.
- **Contingency:** If certain contracts (e.g., government, defense, or strict cost-plus clients) legally mandate single-project steel segregation, the optimization engine will enforce a strict boolean flag: `allow_cross_project = FALSE` for those specific job IDs.
- **Validation:** Meet with Cost Control lead and Project Accounting Controller in Week 1 to ratify internal transfer rules.

### A8. Yard Storage Physics & Crane Unstacking Penalty
- **Client Fact:** Steel arrives and is stored without sequence. Required material ends up at the bottom of stacks, taking excessive time to retrieve.
- **Assumption:**
  - Plate storage stacks reach 4 to 8 plates in height.
  - Moving one 4-tonne plate to reach a buried remnant takes an overhead gantry crane / mobile crane operator and rigger approximately 8–12 minutes, representing an operational cost penalty of **~$35 per unstack move**.
  - Therefore, retrieving a remnant buried at stack depth $\ge 4$ costs >$105 in crane delay and shop-floor disruption, which exceeds the scrap value of small drops.
  - Remnant optimization must incorporate a **stack depth retrieval penalty** to prevent recommending buried remnants that shop-floor operators will simply ignore.
- **Validation:** Time 5 crane retrieval cycles in the yard during the Phase 0 operational audit.
