# Prototype Benchmark & Financial Validation Suite

This prototype supports the Forward Deployed Engineering Case Study for **Client B (Structural Steel Fabricator)**.

It provides a lightweight, deterministic validation harness demonstrating that material savings, cross-project co-nesting, remnant retrieval economics, and multi-scenario ROI can be modeled rigorously without deploying unexplainable deep learning or black-box LLMs to geometric nesting.

---

## 1. What This Prototype Demonstrates

1. **1D Profile Cutting Stock (Beams & Columns):**
   - Compares current project-siloed sequential/first-fit cutting against cross-project best-fit linear packing.
   - Preserves large, usable remnants ($\ge 2.5\text{m}$) and reduces true scrap by 3.6% absolute on sample profile runs.
2. **2D Plate Nesting & Cross-Project Co-Nesting:**
   - Demonstrates that combining plate requirements across active projects (e.g. 20mm S355JR gusset and base plates) eliminates partial sheet drop waste and consolidates remnants into clean, reusable rectangular plates.
3. **Remnant Matching Engine & Yard Retrieval Penalty:**
   - Evaluates whether pulling a remnant from the yard is financially and operationally justified.
   - Explicitly models the **crane unstack penalty** (\$35/move for buried plates) to ensure the system never asks crane riggers to unstack deep piles for small parts.
4. **Comprehensive Financial Sensitivity Model:**
   - Models the full 80,000 tonnes/year fabrication operation.
   - Evaluates Conservative, Base, and Upside scenarios (0.75%, 1.50%, and 2.25% absolute waste reduction).
   - Incorporates client revision scrap cost recovery.
   - Calculates Year 1 ROI, Payback Period, and 3-Year NPV.

---

## 2. Quick Run Instructions

### Run the Benchmark Runner
```bash
python prototype/demo_benchmark.py
```

### Run the Automated Test Suite
```bash
python -m pytest prototype/tests/test_prototype.py -v
```

---

## 3. Key Synthetic Benchmark Output Highlights

- **1D Cutting Stock:** Stock 12m universal beams reduced from 25 to 24 (4.0% reduction in ordered stock), with 4.2m preserved as prime reusable offcut.
- **2D Plate Nesting:** Master 6m x 2.5m plates reduced from 4 to 3 (2.35 tonnes saved), preserving 6.0 $m^2$ clean rectangular drop.
- **Remnant Evaluation:** Identified accessible remnant in Position 2, netting +$149.20 net gain after paying crane move penalty.
- **Financial Validation (Base Scenario):**
  - **1,200 tonnes material waste saved/year**
  - **$780,000 direct steel savings + $332,500 revision recovery**
  - **$1,112,500 Gross Annual Benefit**
  - **227.2% Year 1 ROI with 3.7 months payback period**
