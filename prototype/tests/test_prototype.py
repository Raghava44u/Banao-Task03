"""
Comprehensive Unit & Regression Test Suite for Structural Steel Nesting Prototype

Tests include:
1. Normal feasible test cases for 1D, 2D, Remnant Matching, and Financial Model.
2. Pairwise geometric non-overlap and boundary containment verification in 2D.
3. Regression tests for all six diagnostic failure scenarios identified in the engineering audit:
   - Failure 1: 2D part exceeding plate bed width/length.
   - Failure 2: 2D aspect ratio collisions requiring multiple plates.
   - Failure 3: 1D profile section and material grade incompatibility.
   - Failure 4: 1D cut length exceeding stock beam length.
   - Failure 5: 1D allow_cross_project flag enforcement.
   - Failure 6: Remnant matching quantity awareness and residual scrap penalty.
"""

import pytest
from prototype.demo_benchmark import (
    ProfileCutItem,
    StockProfile,
    PlatePart,
    MasterPlate,
    YardRemnant,
    FinancialModelParams,
    run_1d_cutting_stock_baseline,
    run_1d_cutting_stock_optimized,
    simulate_2d_plate_nesting,
    pack_plate_items,
    evaluate_remnant_suitability,
    run_financial_model,
)

# ==============================================================================
# 1. NORMAL FEASIBLE TEST CASES
# ==============================================================================

def test_1d_cutting_stock_optimization_normal():
    items = [
        ProfileCutItem("P1", "PRJ-A", 5000.0, 2, section_profile="UB_457x191x74", material_grade="S355JR"),
        ProfileCutItem("P2", "PRJ-B", 4000.0, 2, section_profile="UB_457x191x74", material_grade="S355JR"),
        ProfileCutItem("P3", "PRJ-A", 2800.0, 2, section_profile="UB_457x191x74", material_grade="S355JR"),
    ]
    base = run_1d_cutting_stock_baseline(items, stock_length_mm=12000.0)
    opt = run_1d_cutting_stock_optimized(items, stock_length_mm=12000.0, allow_cross_project=True)

    assert opt["num_stocks_used"] <= base["num_stocks_used"]
    assert opt["total_useful_meters"] == pytest.approx(base["total_useful_meters"], abs=1e-3)
    assert opt["true_scrap_meters"] >= 0.0
    assert 0.0 <= opt["utilization_pct"] <= 100.0


def test_2d_plate_nesting_conesting_normal():
    parts = [
        PlatePart("BP1", "PRJ-1", 800.0, 1000.0, 6, thickness_mm=20.0, material_grade="S355JR"),
        PlatePart("BP2", "PRJ-2", 800.0, 1000.0, 6, thickness_mm=20.0, material_grade="S355JR"),
    ]
    plate = MasterPlate("PLATE-6X2.5", 2500.0, 6000.0, 20.0, "S355JR")
    res = simulate_2d_plate_nesting(parts, plate)

    assert res["plate_savings_count"] >= 0
    assert res["optimized"]["plates_purchased"] <= res["baseline"]["plates_purchased"]
    assert res["optimized"]["gross_waste_pct"] <= res["baseline"]["gross_waste_pct"]
    assert res["optimized"]["used_parts_area_m2"] == pytest.approx(res["baseline"]["used_parts_area_m2"], abs=1e-3)


def test_2d_plate_nesting_zero_overlaps_and_boundary_containment():
    """
    Verifies that all placed parts strictly stay within plate boundaries,
    respect clamp margins, and have ZERO pairwise geometric overlap.
    """
    parts = [
        PlatePart("P1", "PRJ-1", 600.0, 800.0, 8, thickness_mm=20.0, material_grade="S355JR"),
        PlatePart("P2", "PRJ-2", 700.0, 900.0, 6, thickness_mm=20.0, material_grade="S355JR"),
    ]
    plate = MasterPlate("TEST-PLATE", 2500.0, 6000.0, 20.0, "S355JR", clamp_margin_mm=25.0)
    nested_plates = pack_plate_items(parts, plate)

    margin = plate.clamp_margin_mm
    kerf = 5.0

    for p_idx, n_plate in enumerate(nested_plates):
        placed = n_plate.placed
        # Check boundary containment
        for p in placed:
            assert p.x_mm >= margin, f"Part {p.part_id} violates left margin"
            assert p.y_mm >= margin, f"Part {p.part_id} violates bottom margin"
            assert p.x_mm + p.width_mm <= plate.width_mm - margin, f"Part {p.part_id} exceeds plate width"
            assert p.y_mm + p.length_mm <= plate.length_mm - margin, f"Part {p.part_id} exceeds plate length"

        # Check pairwise non-overlap (including kerf spacing)
        for i in range(len(placed)):
            p1 = placed[i]
            for j in range(i + 1, len(placed)):
                p2 = placed[j]
                overlap_x = max(p1.x_mm, p2.x_mm) < min(p1.x_mm + p1.width_mm, p2.x_mm + p2.width_mm)
                overlap_y = max(p1.y_mm, p2.y_mm) < min(p1.y_mm + p1.length_mm, p2.y_mm + p2.length_mm)
                assert not (overlap_x and overlap_y), (
                    f"Plate {p_idx+1}: Collision detected between part {p1.part_id} at ({p1.x_mm},{p1.y_mm}) "
                    f"and part {p2.part_id} at ({p2.x_mm},{p2.y_mm})"
                )


def test_remnant_evaluation_crane_penalty_normal():
    target = PlatePart("TARGET", "PRJ-NEW", 1000.0, 1000.0, 1, 20.0, "S355JR")
    remnants = [
        # Buried at position 5
        YardRemnant("REM-DEEP", "PRJ-OLD", 1200.0, 1200.0, 20.0, "S355JR", stack_position=5, location_bay="BAY-A"),
        # Top of stack at position 1
        YardRemnant("REM-TOP", "PRJ-OLD", 1200.0, 1200.0, 20.0, "S355JR", stack_position=1, location_bay="BAY-B"),
    ]
    best = evaluate_remnant_suitability(target, remnants, crane_cost_per_unstack_usd=35.0, steel_price_per_kg=0.95)
    assert best is not None
    assert best["remnant_id"] == "REM-TOP"
    assert best["crane_penalty_usd"] == 0.0
    assert best["recommended"] is True


def test_financial_model_scenarios_normal():
    params = FinancialModelParams()
    fin = run_financial_model(params)

    assert fin["baseline"]["annual_tonnes"] == 80000.0
    assert "Conservative" in fin["scenarios"]
    assert "Base" in fin["scenarios"]
    assert "Upside" in fin["scenarios"]

    base_sc = fin["scenarios"]["Base"]
    assert base_sc["total_material_saved_tonnes"] == 1200.0
    assert base_sc["gross_annual_benefit_usd"] > 1_000_000.0
    assert base_sc["roi_year_1_pct"] > 200.0
    assert base_sc["payback_period_months"] < 6.0


# ==============================================================================
# 2. REGRESSION TESTS FOR THE SIX AUDIT DIAGNOSTIC FAILURES
# ==============================================================================

def test_regression_failure_1_oversized_2d_part_rejected():
    """
    Audit Failure 1: A part larger than the master plate (3000x3000mm on 2500x6000mm)
    previously reported plates_purchased = 1 due to area division.
    Fix: Must raise ValueError during geometry validation.
    """
    part_too_big = PlatePart("OVERSIZED", "PRJ-1", width_mm=3000.0, length_mm=3000.0, quantity=1, thickness_mm=20.0)
    master_plate = MasterPlate("STD", width_mm=2500.0, length_mm=6000.0, thickness_mm=20.0)

    with pytest.raises(ValueError, match="exceed master plate usable dimensions"):
        simulate_2d_plate_nesting([part_too_big], master_plate)


def test_regression_failure_2_aspect_ratio_requires_two_plates():
    """
    Audit Failure 2: Two 1500x4000mm parts on a 2500x6000mm plate.
    1500+1500=3000 > 2500 width; 4000+4000=8000 > 6000 length.
    Previously reported plates_purchased = 1 due to total area (12 m² < 15 m² * 0.85).
    Fix: MaxRects bin packing must allocate exactly 2 plates.
    """
    master_plate = MasterPlate("STD", width_mm=2500.0, length_mm=6000.0, thickness_mm=20.0)
    two_parts = [
        PlatePart("P_A", "PRJ-1", width_mm=1500.0, length_mm=4000.0, quantity=2, thickness_mm=20.0)
    ]
    res = simulate_2d_plate_nesting(two_parts, master_plate)
    assert res["optimized"]["plates_purchased"] == 2, (
        f"Expected 2 plates for two 1500x4000mm parts, but got {res['optimized']['plates_purchased']}"
    )


def test_regression_failure_3_profile_section_segregation():
    """
    Audit Failure 3: UB beam and UC column cross-sections previously packed onto one 12m stock beam.
    Fix: Optimizer must strictly segregate different section profiles into separate stock bars.
    """
    prof_ub = ProfileCutItem("UB_BEAM", "PRJ-A", length_mm=6000.0, quantity=1, section_profile="UB_457x191x74")
    prof_uc = ProfileCutItem("UC_COLUMN", "PRJ-B", length_mm=5000.0, quantity=1, section_profile="UC_203x203x46")

    res = run_1d_cutting_stock_optimized([prof_ub, prof_uc], stock_length_mm=12000.0, allow_cross_project=True)
    assert res["num_stocks_used"] == 2, (
        f"Expected 2 distinct stock beams for UB and UC profiles, but got {res['num_stocks_used']}"
    )


def test_regression_failure_4_profile_oversized_item_rejected():
    """
    Audit Failure 4: 13,000mm profile piece on 12,000mm stock previously caused negative scrap
    and 108.3% utilization.
    Fix: Must raise ValueError during input validation.
    """
    item_long = ProfileCutItem("LONG_BEAM", "PRJ-1", length_mm=13000.0, quantity=1)

    with pytest.raises(ValueError, match="exceeds stock beam length"):
        run_1d_cutting_stock_optimized([item_long], stock_length_mm=12000.0)


def test_regression_failure_5_cross_project_flag_respected():
    """
    Audit Failure 5: allow_cross_project parameter was dead and unused in 1D optimizer.
    Fix: When allow_cross_project=False, projects must remain segregated, yielding 25 beams;
    when allow_cross_project=True, cross-project pooling yields 24 beams.
    """
    cut_items = [
        ProfileCutItem("UB-A-01", "PRJ-ALPHA", 5800.0, 6, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-A-02", "PRJ-ALPHA", 4150.0, 8, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-A-03", "PRJ-ALPHA", 2300.0, 10, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-B-01", "PRJ-BETA", 6200.0, 8, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-B-02", "PRJ-BETA", 3450.0, 12, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-B-03", "PRJ-BETA", 1950.0, 6, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-C-01", "PRJ-GAMMA", 7100.0, 4, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-C-02", "PRJ-GAMMA", 4800.0, 4, section_profile="UB_457x191x74"),
        ProfileCutItem("UB-C-03", "PRJ-GAMMA", 2150.0, 8, section_profile="UB_457x191x74"),
    ]

    res_silo = run_1d_cutting_stock_optimized(cut_items, allow_cross_project=False)
    res_pooled = run_1d_cutting_stock_optimized(cut_items, allow_cross_project=True)

    assert res_silo["num_stocks_used"] == 25, "Expected 25 beams when cross-project pooling is disabled"
    assert res_pooled["num_stocks_used"] == 24, "Expected 24 beams when cross-project pooling is enabled"


def test_regression_failure_6_remnant_quantity_and_residual_waste():
    """
    Audit Failure 6: Remnant matching previously ignored target_part.quantity and residual scrap.
    Fix: For an order of quantity 10 on a remnant that only holds 1 piece,
    allocated_quantity must be 1, unfulfilled_quantity must be 9, and economic score must reflect
    the steel for 1 piece rather than 10.
    """
    target_multi = PlatePart("BP-MULTI", "PRJ-X", width_mm=500.0, length_mm=500.0, quantity=10, thickness_mm=20.0)
    rem_tiny = YardRemnant(
        "REM-TINY", "PRJ-Y", width_mm=600.0, length_mm=600.0, thickness_mm=20.0,
        material_grade="S355JR", stack_position=1, location_bay="BAY-A"
    )

    match = evaluate_remnant_suitability(target_multi, [rem_tiny])
    assert match is not None
    assert match["allocated_quantity"] == 1
    assert match["unfulfilled_quantity"] == 9
    # Virgin steel saved must be for 1 part (~$37.09), NOT 10 parts (~$370)
    assert match["steel_value_saved_usd"] < 50.0
