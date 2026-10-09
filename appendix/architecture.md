# Appendix 4: Technical System Architecture & Integration Blueprint

This document details the complete end-to-end software architecture for the **Material Intelligence & Assisted Nesting Co-Pilot (MINC)** designed for **Client B**.

---

## 1. High-Level Architecture Diagram

```
+----------------------------------------------------------------------------------------------------+
|                                    CLIENT B ENTERPRISE SYSTEMS                                     |
|                                                                                                    |
|   +-----------------------+     +-----------------------+     +--------------------------------+   |
|   |  Strumis Steel ERP    |     |   Tekla / CAD / BIM   |     |    Yard & Logistics Roster     |   |
|   |  - Project BOMs       |     |   - DSTV / NC1 Files  |     |    - Plate Stacks & Bays       |   |
|   |  - Inventory & MTCs   |     |   - 2D DXF Contours   |     |    - CarTrack / Booking GPS    |   |
|   |  - Strumis Auto-Nest  |     |   - Revision Notices  |     |    - Crane Capacity Logs       |   |
|   +-----------+-----------+     +-----------+-----------+     +---------------+----------------+   |
+---------------|-----------------------------|---------------------------------|--------------------+
                | ODBC / SQL Extract          | File Watcher / SFTP             | REST / CSV Poller
                v                             v                                 v
+----------------------------------------------------------------------------------------------------+
|                                      DATA INGESTION LAYER                                          |
|                                                                                                    |
|   +--------------------------------------------------------------------------------------------+   |
|   | Secure On-Premises Connector / Data Pipeline Agent                                         |   |
|   | - Strumis Database Connector (Read-Only SQL Extraction)                                    |   |
|   | - CAD/DSTV Parser (Polygonal geometry extraction, thickness, grade, pierce points)          |   |
|   | - Revision Diff Engine (Timestamped line-item comparison: Old BOM vs New BOM)              |   |
|   +---------------------------------------------+----------------------------------------------+   |
+-------------------------------------------------|--------------------------------------------------+
                                                  v
+----------------------------------------------------------------------------------------------------+
|                              DATA NORMALIZATION & VALIDATION LAYER                                 |
|                                                                                                    |
|   - Geometric Validation: Checks closed planar polygons, minimum hole diameters, aspect ratios    |
|   - Physical Constraint Enrichment: Kerf width (4-6mm), clamp margins (25mm), thermal spacing      |
|   - Inventory & MTC Alignment: Material grade matching (S355/S275), rolling/grain direction        |
|   - Cross-Project Batching Rules: Project delivery windows, client contract accounting flags       |
+-------------------------------------------------+--------------------------------------------------+
                                                  v
+----------------------------------------------------------------------------------------------------+
|                         OPTIMIZATION & REMNANT INTELLIGENCE CORE                                   |
|                                                                                                    |
|   +-------------------------------+   +-----------------------------+   +----------------------+   |
|   | 1D Linear Profile Optimizer   |   | 2D Remnant-Preserving Nest  |   | Yard Remnant Scorer  |   |
|   | - Multi-project cut batching  |   | - No-Fit Polygon (NFP) pack |   | - Usable drop filter |   |
|   | - Gilmore-Gomory LP / Best-Fit|   | - Remnant cluster penalty   |   | - Crane depth penalty|   |
|   | - Offcut consolidation >=2.5m |   | - Heat dissipation paths    |   | - Net dollar scoring |   |
|   +-------------------------------+   +-----------------------------+   +----------------------+   |
+-------------------------------------------------+--------------------------------------------------+
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                    HUMAN-IN-THE-LOOP CO-PILOT DESK                                 |
|                                                                                                    |
|   +--------------------------------------------------------------------------------------------+   |
|   | Nesting Operator & Cost Control Interface (Web UI / Electron Desktop App)                  |   |
|   | - Side-by-Side Visual Comparison: Candidate Nest A (Manual) vs Candidate Nest B (MINC Opt)|   |
|   | - Key Explanatory Metrics: Utilization %, Scrap Delta, Preserved Remnant Area, $ Savings   |   |
|   | - Action Panel: [Accept Recommendation] | [Adjust in Strumis] | [Reject with Reason Code]   |   |
|   +---------------------------------------------+----------------------------------------------+   |
+-------------------------------------------------|--------------------------------------------------+
                                                  v
+----------------------------------------------------------------------------------------------------+
|                                 EXECUTION & FEEDBACK CAPTURE                                       |
|                                                                                                    |
|   - Post-Processor Export: Approved nests exported directly to Strumis / CNC post-processors       |
|   - Shop-Floor Actual Capture: Sizing CNC operator logs actual scrap bin weight & drop dimensions  |
|   - Variance Logger: Theoretical utilization vs Actual shop-floor yield recorded in database       |
|   - Reason Code Audit: Rejection telemetry analyzed weekly to continuously calibrate constraints   |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Ingestion & Data Transformation Specifications

### 2.1 Strumis ERP Connector
- **Method:** Read-only direct SQL query via ODBC connection to the Strumis Microsoft SQL Server database, running every 15 minutes (or on event trigger).
- **Core Entities Extracted:**
  - `Job_Header` (Project ID, client name, contract type, target completion date).
  - `BOM_Requirements` (Part marks, profile sizes, plate thicknesses, steel grade, quantities).
  - `Stock_Inventory` (Raw master plate dimensions, beam lengths, mill test certificates [MTCs], heat numbers, storage bay locations).
  - `Remnant_Inventory` (Recorded offcut dimensions, origin project, storage location).

### 2.2 CAD & Geometry Parser (DSTV / NC1 & DXF)
- Structural steel detailing packages (Tekla Structures, SDS/2) generate **DSTV-NC (Standard Description of Steel Structures for Numerical Controls)** files for CNC machines.
- The parser extracts:
  - Header data: Piece mark, drawing revision number, quantity, steel grade, profile/plate thickness.
  - Profile cuts: Saw bevel cuts, length, cope geometry, web/flange hole patterns.
  - Plate contours: Outer polygon boundary vertices, inner cutout boundaries, hole centers/diameters.
- Geometry is transformed into canonical `shapely.geometry.Polygon` objects with strict validation:
  - Polygons must be planar, non-self-intersecting, and oriented with positive area.
  - Small holes ($< \text{plate thickness}$) are flagged for drilling rather than thermal plasma piercing.

---

## 3. Optimization Engine Mechanics

### 3.1 Implemented Prototype Engine (`prototype/demo_benchmark.py`)
- **1D Profile Cutting Stock:** Best-Fit Decreasing (BFD) bin packing heuristic with strict `section_profile` and `material_grade` compatibility segregation, length guardrails ($12.0\text{m}$ max), configurable `allow_cross_project` pooling control, and exact kerf/remnant accounting.
- **2D Plate Nesting:** Maximal Rectangles (MaxRects) bin packing with Best-Short-Side-Fit (BSSF). Generates explicit millimeter coordinates $(x, y, w, l, \text{rotation})$ for every part, guarantees zero overlap, enforces $5\text{mm}$ kerf spacing and $25\text{mm}$ clamp margins, and measures actual largest remaining rectangular offcuts.
- **Remnant Matching:** Quantity-aware grid fit evaluator balancing virgin steel cost saved against crane unstack penalties and residual scrap costs.

### 3.2 Target Production Scaled Engine (Phase 1–2 Roadmap)
- **1D Linear Programming:** Hybrid Column Generation using Integer Linear Programming (CBC/HiGHS solver) to achieve global mathematical optimality across high-volume cut catalogs.
- **2D Irregular Polygon Nesting:** Guided Local Search (GLS) with No-Fit Polygon (NFP) collision evaluation to nest complex non-rectangular CAD geometries directly from Tekla DSTV/NC1 files.
- **Remnant-Preserving Objective:**
  Standard auto-nesters minimize bounding box length, often leaving an L-shaped or stepped jagged remnant that shop floor operators cannot use. MINC enforces a **Max-Rectangular Drop Incentive**:
  $$\text{Score} = \text{UtilArea} + \alpha \cdot \text{Area}(\text{MaxInscribedRectangle}(\text{UnusedDrop}))$$
  This mathematically drives the nesting layout to pack small gusset plates into one corner of the master plate, leaving a clean, rectangular remnant with minimum width $\ge 1,500\text{mm}$ and length $\ge 2,000\text{mm}$.
- **Thermal & Machine Constraints:**
  - Lead-in / lead-out torch paths: Minimum 8mm distance from neighboring parts.
  - Heat distribution sequence: Interleaves cut paths across alternating sides of the plate to prevent thermal expansion warping.

---

## 4. Human-in-the-Loop Co-Pilot Interface & Decision Workflow

```
[New Engineering Drawing Released]
                │
                ▼
[MINC Ingests Cut List & Scans Inventory]
                │
                ├─────────────────────────────────────────────────┐
                │                                                 │
    [Remnant Matching]                              [Virgin Plate Multi-Project Nest]
    Scans Yard Remnants                             Batches compatible parts across
    Applies Crane Depth Penalty                     current 10-day project releases
    Evaluates net $ value                           Preserves rectangular offcuts
                │                                                 │
                └────────────────────────┬────────────────────────┘
                                         ▼
                   [MINC Generates Candidate Nest Plans]
                                         │
                                         ▼
            ┌────────────────────────────────────────────────────────┐
            │       HUMAN-IN-THE-LOOP CO-PILOT OPERATOR DESK         │
            │                                                        │
            │  Shows side-by-side comparison:                        │
            │  - Plan A: Manual Baseline (or Strumis default)        │
            │  - Plan B: MINC Assisted Recommendation                │
            │                                                        │
            │  Operator sees:                                        │
            │  - Steel Utilization %: 76.5% vs 86.2% (+9.7%)        │
            │  - Scrap Cost Delta: -$245.00                          │
            │  - Preserved Remnant: 1,800mm x 2,500mm (Reusable)     │
            │  - Yard Retrieval: Remnant in Bay A, Stack Depth 2     │
            │                                                        │
            │  [ ACCEPT RECOMMENDATION ]   [ OVERRIDE / REJECT ]     │
            └────────────────────────────┬───────────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
          [Operator Accepts]                          [Operator Rejects]
                   │                                           │
  - Exports cut plan to Strumis CNC               - Operator selects reason:
  - Generates yard pull ticket for crane            * "Plate warped / damaged"
  - Automatically posts project cost credit         * "Crane stack too deep"
                                                    * "Thermal warping risk"
                                                    * "Urgent schedule change"
                                                  - Rejection logged in DB
                                                  - Optimizer adjusts weights
```

---

## 5. Security, Infrastructure & Scalability

- **Deployment Footprint:**
  - **On-Premises Local Agent:** Lightweight Docker container deployed on a dedicated local VM inside the client’s LAN. Communicates securely with Strumis SQL Server and local file shares.
  - **Cloud Processing Hub (Optional / Hybrid):** Dedicated single-tenant VPC (AWS/Azure) running the optimization microservices, API Gateway, and web UI. All customer data and geometry files encrypted in transit (TLS 1.3) and at rest (AES-256).
  - **Air-Gapped Option:** If defense or client confidentiality prohibits cloud processing, the entire MINC engine can run 100% on-premises on a single quad-core Linux/Windows server with 32GB RAM.
- **Auditing & Governance:**
  - Every nesting decision, operator override, revision diff, and actual shop-floor scrap weight is permanently logged with user ID and timestamp for Cost Control auditing.
