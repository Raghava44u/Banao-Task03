"""
Unit and regression test suite for prototype/demo_benchmark.py
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
    evaluate_remnant_suitability,
    run_financial_model,
)

def test_1d_cutting_stock_optimization():
    items = [
        ProfileCutItem("P1", "PRJ-A", 5000.0, 2),
        ProfileCutItem("P2", "PRJ-B", 4000.0, 2),
        ProfileCutItem("P3", "PRJ-A", 2800.0, 2),
    ]
    base = run_1d_cutting_stock_baseline(items, stock_length_mm=12000.0)
    opt = run_1d_cutting_stock_optimized(items, stock_length_mm=12000.0)

    # Optimized should use equal or fewer beams
    assert opt["num_stocks_used"] <= base["num_stocks_used"]
    assert opt["utilization_pct"] >= base["utilization_pct"]
    assert opt["total_useful_meters"] == pytest.approx(base["total_useful_meters"], abs=1e-3)

def test_2d_plate_nesting_conesting_savings():
    parts = [
        PlatePart("BP1", "PRJ-1", 1000.0, 1000.0, 8),
        PlatePart("BP2", "PRJ-2", 1000.0, 1000.0, 6),
    ]
    plate = MasterPlate("PLATE-6X2.5", 2500.0, 6000.0, 20.0, "S355JR")
    res = simulate_2d_plate_nesting(parts, plate)

    assert res["plate_savings_count"] >= 0
    assert res["optimized"]["plates_purchased"] <= res["baseline"]["plates_purchased"]
    assert res["optimized"]["gross_waste_pct"] <= res["baseline"]["gross_waste_pct"]

def test_remnant_evaluation_crane_penalty():
    target = PlatePart("TARGET", "PRJ-NEW", 1000.0, 1000.0, 1, 20.0, "S355JR")
    remnants = [
        # Buried at position 5 (penalty = 4 * $35 = $140)
        YardRemnant("REM-DEEP", "PRJ-OLD", 1200.0, 1200.0, 20.0, "S355JR", stack_position=5, location_bay="BAY-A"),
        # Top of stack at position 1 (penalty = 0 * $35 = $0)
        YardRemnant("REM-TOP", "PRJ-OLD", 1200.0, 1200.0, 20.0, "S355JR", stack_position=1, location_bay="BAY-B"),
    ]
    best = evaluate_remnant_suitability(target, remnants, crane_cost_per_unstack_usd=35.0, steel_price_per_kg=0.95)
    assert best is not None
    # Top remnant should have higher net economic value
    assert best["remnant_id"] == "REM-TOP"
    assert best["crane_penalty_usd"] == 0.0
    assert best["recommended"] is True

def test_financial_model_scenarios():
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
