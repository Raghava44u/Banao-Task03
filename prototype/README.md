# Prototype Benchmark & Engineering Feasibility Validation Harness

This prototype provides an empirical, deterministic validation harness supporting the Forward Deployed Engineering Case Study for **Client B (Structural Steel Fabricator)**.

It demonstrates the operational mechanics of material consolidation, physical constraint enforcement, and economic modeling **without deploying black-box AI or unexplainable models to geometric cutting**.

---

## 1. What This Prototype Implements (Current Capabilities)

1. **1D Profile Cutting Stock Heuristic:**
   - **Algorithm:** Best-Fit Decreasing (BFD) bin packing with strict segregation by `section_profile` (e.g. UB vs UC) and `material_grade` (e.g. S355JR vs S275).
   - **Dimensional Feasibility:** Explicit guardrail rejecting pieces exceeding the 12.0m stock beam length.
   - **Cross-Project Control:** Configurable `allow_cross_project` toggle demonstrating that pooling cuts across compatible projects reduces rounding/boundary scrap.
   - **Scrap Accounting:** Exact accounting for saw kerf ($5\text{mm}$), reusable prime offcuts ($\ge 2.5\text{m}$), and true process scrap.
2. **2D Rectangular Plate MaxRects Nesting Engine:**
   - **Algorithm:** Maximal Rectangles (MaxRects) bin packing heuristic with Best-Short-Side-Fit (BSSF).
   - **Physical Feasibility:** Generates exact $(x, y, w, l, \text{rotation})$ coordinates for every part.
   - **Manufacturing Constraints:** Enforces $5\text{mm}$ torch kerf spacing, $25\text{mm}$ plate perimeter clamp margins, and strict dimension checks rejecting oversized parts.
   - **Zero Overlap:** Mathematically verified pairwise non-overlap across all placed parts.
   - **Remnant Detection:** Measures the actual largest contiguous free rectangle $(W_{\text{rem}}, L_{\text{rem}})$ remaining on the plate bed to identify reusable rectangular offcuts ($\ge 3.0\text{m}^2$).
3. **Quantity-Aware Remnant Matching & Economics:**
   - Evaluates grid packing capacity on stored yard offcuts against required order quantities.
   - Deducts crane retrieval penalties based on stack depth ($35/unstack move).
   - Penalizes residual scrap created when cutting small parts from larger offcuts.
4. **Parametric Financial Sensitivity Model:**
   - Models the full 80,000 tonnes/year fabrication operation across Conservative, Base, and Upside scenarios.
   - Incorporates client revision scrap cost recovery, Year 1 ROI, payback period, and 3-Year NPV.

---

## 2. Distinction Between Prototype vs Target Production Architecture

| Capability | Current Prototype Implementation | Target Production Architecture (Phase 1–2) |
| :--- | :--- | :--- |
| **1D Profile Nesting** | Best-Fit Decreasing (BFD) greedy heuristic | Gilmore-Gomory Linear Programming / Column Generation |
| **2D Plate Nesting** | MaxRects rectangular bin packing heuristic | Guided Local Search with No-Fit Polygons (NFP) for irregular CAD shapes |
| **Geometry Input** | Parametric rectangular part dimensions | Direct parsing of Tekla Structures DSTV/NC1 and DXF files |
| **ERP / Inventory Integration** | In-memory synthetic datastructures | Read-only SQL/ODBC connectors to Strumis ERP tables |
| **Financial Savings** | **Unvalidated Target Scenarios** ($1,200\text{t} / \$1.11\text{M}$) | **Empirical Ground Truth** measured via 50-job Historical Replay |

> **IMPORTANT:** The financial figures ($1.11M base annual benefit, 227% Year 1 ROI) are **target planning scenarios** calibrated to Client B's reported capacity. They are **NOT** claimed as guaranteed or proven until the Phase 1 Historical Replay Benchmark is executed against 50–100 actual completed Strumis jobs.

---

## 3. Quick Run Instructions

### Run the Benchmark Harness
```bash
python prototype/demo_benchmark.py
```

### Run the Automated Test Suite (11 Tests)
```bash
python -m pytest prototype/tests/test_prototype.py -v
```

---

## 4. Key Verified Benchmark Outputs

- **1D Cutting Stock:** Stock 12m universal beams reduced from 25 to 24 (4.0% reduction in ordered stock) solely when cross-project pooling is enabled, preserving 4.2m of reusable drop.
- **2D Plate Nesting:** Master 6m x 2.5m plates reduced from 4 to 3 (2.35 tonnes saved), preserving a verified $2.45\text{m} \times 2.76\text{m}$ ($6.77\text{ m}^2$) prime rectangular offcut with zero part overlap.
- **Remnant Evaluation:** Correctly allocates partial quantity (1 of 10) to accessible offcut with positive net gain (+$106.85) after crane move and residual scrap penalties.
