# Candidate Interview Preparation Guide & Project Debrief
## Task 3 V2: Structural Steel Operations & Nesting Intelligence (Client B)

This comprehensive interview guide prepares you to discuss every aspect of the Client B project during technical and architectural interviews. It covers the operational reality, technical architecture, mathematical modeling, commercial strategy, and 40 exact interview defense questions.

---

### 1. What was the problem?
Client B is a large structural steel fabricator producing ~80,000 tonnes of steel annually across 10–15 concurrent projects. They lose 7% to 10% of all purchased steel to scrap, with plate scrap running as high as 20% to 25%. This translates to over **$5.2 million per year in lost steel**. The company lacked data to determine how much of that scrap was avoidable, why valuable leftover steel was abandoned, and how much material loss was caused by late client drawing revisions.

### 2. What did the client originally ask for?
The Cost Control engineer asked: *"How can AI be integrated into our company? If I have to pick one area, it's nesting optimisation."* They also floated ideas around AI for yard storage, trailer loading, trailer fleet idle time, and equipment scheduling.

### 3. What was the deeper problem?
The deeper problem was not a missing AI algorithm—it was a breakdown across systems, accounting, and shop-floor physics:
1. **The Strumis Auto-Nest Paradox:** They *already own* automated nesting software inside Strumis, but the human nesting planners turned it off because it created jagged, unusable offcuts. Cost Control had zero data to verify if the planners were right.
2. **Project Accounting Silos:** Steel is purchased per project and costs are loaded 100% to that project. Because of this accounting rule, planners cannot easily co-nest parts from two projects on the same plate, nor can one project buy a leftover remnant from another without friction.
3. **Yard Physical Friction:** Leftover plates are dumped in unsequenced piles up to 8 plates deep. Moving 4 heavy plates to retrieve a small piece costs ~$105 in crane time and delays cutting tables. Planners and operators naturally cut brand-new plates instead.
4. **Opaque Waste Categories:** The reported 7–10% scrap lumped together unavoidable cutting torch width (kerf), client-billable drawing revisions, unrecovered remnants, and genuine geometric packing waste.

### 4. Who were the stakeholders?
- **Cost Control (Contact):** Cares about project profit margins and scrap $/tonne. Wants an empirical baseline and revision cost recovery.
- **Nesting Team (Absent from calls):** Cares about turnaround time and machine cutability. Risk of fierce resistance if software produces uncuttable nests or threatens their jobs.
- **Engineering / Detailing (Absent):** Cares about release deadlines. Wants automated revision diffs without administrative burden.
- **Yard / Crane Rigging (Absent):** Cares about crane time and safety. Will ignore offcut pull tickets if plates are buried deep in stacks.
- **Shop Floor / CNC Operators (Absent):** Cares about table uptime and avoiding torch collisions from warped parts.
- **Project Managers (Absent):** Cares about meeting contract deadlines; wary of sharing steel across projects.
- **Procurement (Absent):** Cares about mill plate order lead times and supplier discounts.
- **Executive Leadership (Absent):** Cares about EBITDA, cash flow, and low capital risk.

### 5. What did we know?
- 80,000 tonnes/year capacity; 7,000–8,000 tonnes/month.
- 10–15 active projects running concurrently.
- Plate waste: 20–25%; Profile waste: 5–10%; Overall waste: 7–10%.
- Strumis ERP used for data and nesting; auto-nesting bypassed by planners.
- Material purchased and cost-loaded per project.
- Yard is unsequenced; plates end up at the bottom of stacks.
- Fleet of 13 trailers with CarTrack GPS and a vehicle booking system, but low utilization and extra rentals.
- Discovery was incomplete: only Cost Control was interviewed.

### 6. What didn't we know?
- The exact split between unavoidable process kerf and avoidable geometric waste.
- The technical reason why planners rejected Strumis auto-nesting.
- The digital file formats exported by Engineering (DSTV/NC1 vs DXF vs PDFs).
- Whether 6–12 months of historical nesting files still exist in Strumis.
- The contract accounting rules regarding whether cross-project steel sharing is legally permitted.
- The realized scrap salvage price ($/tonne).
- How client drawing revisions are currently tracked and billed.

### 7. What questions should we ask before starting?
Prioritized P0 questions:
1. *What exact components make up the 20–25% plate waste (kerf, clamp margin, revisions, offcuts)?*
2. *Why specifically did the nesting team reject Strumis auto-nesting? What happened when they ran it?*
3. *Can we access 50–100 historical nesting jobs in native digital format to establish a baseline?*
4. *Do client contracts legally permit cross-project steel sharing, or do some jobs prohibit it?*
5. *How accessible is the Strumis SQL database (direct ODBC vs scheduled CSV exports)?*

### 8. What assumptions did we make?
- Product mix: 75% structural profiles (60,000t) and 25% plate (20,000t). This yields a 10.1% blended baseline, matching the client's 7–10% statement.
- Pricing: Prime steel = $950/t; Scrap salvage = $300/t; Net loss per tonne scrapped = $650/t.
- Engineering exports standard DSTV/NC1 and DXF files from Tekla Structures.
- Plate storage stacks reach 4–8 plates high; crane unstack cost is ~$35 per moved plate.
- Internal accounting can be configured to credit donating projects at raw material cost.

### 9. What solutions did we consider?
- **Option A (Visibility Layer Only):** Ingests Strumis data and builds dashboards. Low cost, but doesn't actually optimize cutting plans.
- **Option B (COTS Nesting Upgrade):** Buying a new commercial nesting package. High license cost ($220k) and fatal user adoption risk—they already own Strumis auto-nest and rejected it!
- **Option C (Assisted Nesting Co-Pilot - MINC):** **RECOMMENDED**. Combines deterministic optimization, remnant preservation, crane depth penalties, cross-project cost credits, and a human-in-the-loop desk.
- **Option D (Autonomous AI Smart Factory):** Full end-to-end autonomous factory automation. Rejected: extreme risk, impossible feasibility, shop-floor rejection.

### 10. Why did we choose the recommended solution?
Because it directly removes the four real operational blockers:
1. It preserves rectangular offcuts rather than creating Swiss-cheese scrap.
2. It respects yard physics via a crane depth penalty ($35/move).
3. It automates cross-project cost credits.
4. It keeps the human planner in control, eliminating adoption resistance while logging rejection reasons to continuously improve.

### 11. How does the solution work?
1. Ingests cut lists, BOMs, and raw inventory from Strumis and Tekla CAD.
2. Identifies parts across active projects with compatible delivery windows and steel grades.
3. Evaluates yard remnants, scoring them against fresh plates, checking grid capacity against quantity, and penalizing buried pieces.
4. Optimizes cutting: the prototype implements 1D Best-Fit Decreasing and 2D Maximal Rectangles (MaxRects) bin packing with exact millimeter coordinates and remnant preservation; the production roadmap scales this to Gilmore-Gomory Linear Programming and Guided Local Search with No-Fit Polygons for complex polygonal CAD parts.
5. Displays candidate nests side-by-side with the planner's manual layout on the Co-Pilot Desk.
6. The planner reviews metrics (utilization %, dollar savings, crane moves) and clicks "Accept" or logs a reason code.
7. Approved plans export directly to Strumis CNC post-processors, and actual scrap bin weights are logged to measure real-world savings.

### 12. Where is AI used?
- **Remnant Recommendation Scoring:** Machine learning heuristic ranking that predicts whether a stored remnant is worth retrieving based on yard stack depth, steel grade demand probability, and age.
- **Revision Diff Parsing:** NLP and structured diff extraction on engineering revision notices and BOM changes to classify whether scrap was caused by client design changes (billable) or internal detailing errors.
- **Operator Feedback Learning:** Analyzing planner rejection reason codes to dynamically calibrate constraint weights in the optimization engine.

### 13. Where should AI NOT be used?
- **Geometric 2D/1D Nesting:** AI / LLMs must NOT perform polygonal packing. That is an NP-hard geometric cutting stock problem requiring deterministic mathematical optimization and computational geometry.
- **CNC Machine Execution:** AI must NOT send raw motion commands to physical cutting torches. All cut code must pass through validated post-processors.
- **Autonomous Production Approvals:** AI must NOT bypass human planner review.

### 14. Why use optimization instead of an LLM for nesting?
- **Geometry & Physics:** LLMs are autoregressive token predictors; they have no spatial reasoning to compute No-Fit Polygons, calculate 5mm torch kerfs, or detect polygon overlap down to the millimeter.
- **Guaranteed Feasibility:** Mathematical optimization (Integer Linear Programming, Guided Local Search) provides mathematical proofs of non-overlap and constraint compliance. An LLM outputting coordinates would cause torch collisions and scrap expensive steel.

### 15. What data is required?
- BOM cut lists (part marks, dimensions, thickness, steel grade, quantities, project IDs).
- Raw material stock lists (master plate dimensions, 12m beam lengths, heat numbers, MTCs).
- Yard remnant inventory (dimensions, origin project, bay location, stack depth).
- CAD geometry files (Tekla DSTV/NC1 files and 2D DXF profiles).
- Machine cutting parameters (kerf width, clamp margins, pierce lead-ins).

### 16. Where does the data come from?
- Read-only direct SQL extract from Strumis ERP (via ODBC).
- Engineering file shares hosting Tekla CAD exports.
- Yard inventory logs and CarTrack GPS telemetry.

### 17. What does the architecture look like?
A 4-tier pipeline:
1. **Ingestion Layer:** Local on-premise agent pulling Strumis SQL tables and parsing Tekla DSTV/DXF files.
2. **Normalization & Validation Layer:** Checks closed planar polygons, material grade compatibility, and applies kerf/clamp margins.
3. **Optimization Core:** 1D Linear Profile Optimizer, 2D Remnant-Preserving Nesting Engine, and Crane Depth Scorer.
4. **Co-Pilot Desk & Execution:** Web/desktop UI showing side-by-side comparisons, export hook back into Strumis, and variance logger tracking actual shop-floor scrap bin weights.

### 18. Where does a human make the final decision?
At the Co-Pilot Desk. Every single nest plan must be reviewed and signed off by the human nesting planner. If the planner overrides or rejects a plan, they select a structured reason code (e.g., "Heat distortion risk", "Plate warped", "Remnant buried").

### 19. How do we measure success?
- **Primary Metric:** Avoidable material waste reduction percentage on plate and profile cutting.
- **Secondary Metrics:** Net dollar scrap savings, client revision scrap recovered ($/month), planner acceptance rate ($\ge 75\%$), remnant turnover rate, and zero increase in CNC machine collisions or plate warping.

### 20. What is the baseline?
- Total steel throughput: 80,000 tonnes/year.
- Profile waste: 6.0% (3,600 tonnes/year).
- Plate waste: 22.5% (4,500 tonnes/year).
- Blended total waste: 10.12% (8,100 tonnes/year).
- Annual financial loss: $5,265,000/year (at $650 net loss/tonne).

### 21. What are the proposed thresholds?
- Replay Benchmark Gate: $\ge 1.0\%$ absolute waste reduction on 50–100 historical jobs.
- Live Shadow Pilot Gate: $\ge 75\%$ operator recommendation acceptance rate.
- Production Target (Base Case): 1.50% absolute material waste reduction (1,200 tonnes saved/year) and 350 tonnes of client revision scrap captured ($332,500).

### 22. What would make us stop?
- If the Week 4 Historical Replay proves avoidable waste reduction is $<0.5\%$ (proving manual planning is already optimal).
- If physical yard inventory accuracy is $<70\%$ (remnants logged in software don't exist in reality).
- If planners reject $>50\%$ of recommendations due to uncapturable shop-floor machine constraints.
- If client contract audits strictly prohibit cross-project steel accounting transfers.

### 23. What is the implementation timeline?
- **Phase 0 (Weeks 1–2):** Operational audit, onsite interviews with Nesting and Yard leads, Strumis database mapping.
- **Phase 1 (Weeks 3–4):** Ingestion pipeline, DSTV parsers, 100-job Historical Replay Benchmark.
- **Phase 2 (Weeks 5–8):** Deploy Co-Pilot Desk, 4-week live shadow-mode pilot, crane penalty calibration.
- **Phase 3 (Weeks 9–12):** Production rollout, two-way Strumis sync, monthly Cost Control savings reconciliation.

### 24. What does the client need to provide?
- Exports of 50–100 historical nesting jobs and inventory logs from Strumis.
- Access to the Lead Nesting Planner, Yard Supervisor, and Engineering Lead (45-minute discovery interviews).
- Read-only ODBC database credentials to Strumis.
- Agreement on an internal cost-transfer rule for shared steel.

### 25. What does it cost?
- **One-time implementation:** **$280,000**, paid against performance milestones (30% kickoff, 40% historical replay gate, 30% live pilot completion).
- **Annual recurring software & support:** **$60,000 / year**.

### 26. How do we calculate ROI?
- **Base Case Annual Benefit:**
  - 1,200 tonnes steel saved $\times$ $650 net loss/t = $780,000.
  - 350 tonnes client revision scrap recovered $\times$ $950 raw steel cost = $332,500.
  - Gross Annual Benefit = **$1,112,500**.
- **Year 1 Costs:** $280,000 implementation + $60,000 SaaS = $340,000.
- **Year 1 Net Benefit:** $1,112,500 - $340,000 = **+$772,500**.
- **Year 1 ROI:** $\frac{772,500}{340,000} \times 100 = \mathbf{227.2\%}$.
- **Payback Period:** $\frac{340,000}{1,112,500} \times 12 = \mathbf{3.7\text{ months}}$.

### 27. What are the major risks?
- *Planner resistance:* Mitigated by making it an assisted co-pilot where planners retain final veto.
- *Phantom yard inventory:* Mitigated by filtering out remnants buried $>3$ deep and weekly top-stack cycle counts.
- *Thermal plate warping:* Mitigated by enforcing 8mm thermal margins and interleaved cut paths.
- *Drawing revision desync:* Mitigated by automated BOM diff alerts.

### 28. What did we deliberately NOT build?
- No direct CNC motion control or raw G-code streaming.
- No replacement of human planners.
- No LLMs for geometric nesting.
- No trailer loading or yard robotics in Phase 1.

### 29. What could we build next?
1. Phase 2: Drawing Revision & Engineering Scrap Tracking ($350k/yr).
2. Phase 3: Yard Storage & Dynamic Crane Staging ($250k/yr).
3. Phase 4: Fleet & Trailer Dispatch Optimizer ($200k/yr).

### 30. What are the biggest challenges?
- Managing change management and building trust with skeptical nesting planners.
- Reconciling the digital Strumis database with messy physical yard stacks.
- Navigating project-based cost accounting rules with finance.

### 31. What would I say if the interviewer asks “Why this approach?”
*"Because in industrial operations, throwing an unexplainable AI algorithm at a problem where operators have already rejected automated software is a guaranteed path to failure. Client B already owns automated nesting in Strumis, but planners bypass it because standard auto-nesting creates unusable offcuts. Our approach tackles the actual root causes: remnant preservation, crane retrieval friction, cross-project cost allocation, and human-in-the-loop trust. It delivers hard dollar proof in 4 weeks before touching live cutting."*

### 32. What would I say if they ask “Why AI?”
*"We don't use AI for everything. We use deterministic mathematical optimization where it excels—solving 1D and 2D geometric packing. We apply AI specifically where heuristics and pattern recognition add unique value: scoring yard remnant reuse against crane delay penalties, parsing unstructured engineering revision notices to classify reimbursable scrap, and learning from planner overrides to fine-tune constraint weights."*

### 33. What would I say if they ask “Why not just buy nesting software?”
*"They already bought it! Strumis has an automated nesting module. Planners don't use it because COTS nesting software optimizes for single-sheet fill density, creating Swiss-cheese offcuts, and lacks visibility into yard stack depths or cross-project accounting rules. Buying another black-box COTS tool will cost $200k and get rejected again within 60 days."*

### 34. What would I say if they ask “Why not use an LLM?”
*"LLMs are autoregressive token predictors, not spatial geometric solvers. An LLM cannot compute No-Fit Polygons, respect 5mm plasma kerf widths, or guarantee zero geometric overlap down to the millimeter. If an LLM hallucinates part coordinates by 3 millimeters, cutting torches collide, expensive steel plates are ruined, and production halts. We use proven computational geometry and linear programming for cutting, reserving language models for document diffs."*

### 35. What would I say if they ask “How do you prove the savings?”
*"Through a strict Two-Stage Protocol: Stage 1 is a Historical Replay Benchmark. We take 50 to 100 completed jobs from the past year, re-run them with MINC on identical constraints, and compare the exact steel consumed against their historical records. That gives Cost Control audited mathematical proof. In Stage 2, we run a 4-week live shadow pilot and reconcile theoretical yield with actual scrap bin scale weights on the factory floor."*

### 36. What would I say if they ask “What if the data is bad?”
*"We engineered explicit Stop Conditions and validation gates. During the Phase 0 audit, if we discover that historical Strumis nesting runs were not digitally archived, we establish a 4-week live logging baseline. If yard remnant inventory accuracy is under 70%, we deactivate remnant reuse in Phase 1 and focus 100% of optimization on virgin plate yield, which still captures over $700k in annual value without depending on yard accuracy."*

### 37. What would I say if they ask “How do you get operators to trust it?”
*"By giving them complete control and total transparency. The Co-Pilot Desk shows their manual nest side-by-side with the MINC recommendation, detailing exact scrap deltas, dollar savings, and preserved remnant dimensions. Operators have full veto power. When they reject a plan, they click a reason like 'heat distortion risk' or 'plate warped.' That shows we respect their shop-floor expertise, and the algorithm uses those reasons to get smarter."*

### 38. What would I say if they ask “How would you scale this?”
*"Nesting is the high-value wedge that establishes a validated data foundation connecting CAD, ERP, and the shop floor. Once MINC is live, that same data pipeline enables Phase 2: Drawing Revision Tracking, Phase 3: Dynamic Yard Storage Sequencing, and Phase 4: Trailer Fleet Dispatch Optimization. We scale by solving one high-ROI operational problem at a time, letting each phase fund the next."*

---

### 39. 60-Second Elevator Pitch
> *"Client B is an 80,000-tonne structural steel fabricator losing over $5.2 million a year in scrap steel. They asked for 'AI for nesting,' but when you look under the hood, they already own automated nesting software in Strumis—their planners turned it off because it creates unusable, fragmented offcuts. At the same time, steel is purchased in project silos, valuable leftovers are buried in unsequenced yard piles, and client drawing revisions are scrapped without being billed back.*
>
> *As a Forward Deployed Engineer, I didn't pitch a generic AI model. We designed MINC: a human-in-the-loop nesting co-pilot. It uses deterministic linear programming and 2D packing to consolidate offcuts into clean, reusable rectangles, models crane unstacking penalties so workers aren't digging out buried plates, and automates cross-project cost credits.*
>
> *Under our base case, MINC saves 1,200 tonnes of steel and recovers $332,000 in revision scrap—delivering $1.11 million in annual benefit with a 227% Year 1 ROI and a 3.7-month payback. Crucially, we prove savings first through a 50-job historical replay benchmark before touching live production."*

---

### 40. 3-Minute Executive Walk-Through
> *"When Client B approached us, Cost Control reported 20–25% plate waste, 5–10% profile waste, and wanted to know how AI could optimize their nesting. A lot of AI vendors would immediately pitch a deep learning model or computer vision system. But having worked with industrial operations, the first thing an FDE does is ask: What is the physical and commercial reality on the shop floor?*
>
> *In discovery, three critical facts stood out. First, Client B already has automated nesting inside Strumis, but their planners bypass it and nest by hand, claiming manual saves more steel. Second, steel is purchased and cost-loaded per project, meaning planners cannot easily share plates or remnants across their 10 to 15 active jobs. Third, their yard stacks plates up to 8 deep without location tracking; crane riggers ignore recorded offcuts because digging them out causes massive production delays.*
>
> *So the problem isn't a missing AI algorithm. It's an operational breakdown between CAD, ERP, project accounting, and yard physics. Dropping a black-box AI model or buying another commercial nesting tool would face 100% operator rejection.*
>
> *Instead, we designed MINC: the Material Intelligence & Assisted Nesting Co-Pilot. MINC connects directly to Strumis and Tekla CAD files. It uses proven deterministic optimization—Gilmore-Gomory Linear Programming for beams and Guided Local Search with No-Fit Polygons for plates. But unlike standard auto-nesters, MINC is programmed with an explicit Remnant-Preserving Constraint: it packs parts to leave large, clean, rectangular offcuts that can actually be stored and reused.*
>
> *To solve the yard bottleneck, MINC features an operational Crane Depth Penalty Scorer: it calculates the cost of moving buried plates at $35 per crane move. If a remnant is buried 5 plates deep, MINC mathematically skips it and cuts virgin stock, matching the reality of the shop floor. To solve the accounting barrier, it automatically generates internal credit transfers so projects can share steel seamlessly.*
>
> *Most importantly, this is a human-in-the-loop co-pilot. Planners see a side-by-side comparison of their manual layout versus the MINC proposal, showing exact utilization, dollar savings, and preserved remnant dimensions. Planners retain 100% final approval authority, and whenever they override a plan, they click a reason code that feeds back into calibrating our constraints.*
>
> *Commercially, the economics are compelling: on 80,000 tonnes of steel, a 1.5% absolute waste reduction saves 1,200 tonnes of material, generating $780,000 in direct steel savings, plus $332,500 in captured client revision claims. That's $1.11 million in annual gross benefit against a $280,000 implementation fee—delivering a 227% Year 1 ROI and paying for itself in under 4 months.*
>
> *We de-risk adoption by running a 100-job Historical Replay Benchmark in Week 4. Cost Control sees audited proof of savings on their own past jobs before we touch live factory cutting. That is how an FDE builds trust, aligns stakeholders, and delivers measurable industrial value."*
