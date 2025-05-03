import pandas as pd
import numpy as np
from src.ofi_best_level import compute_best_level_ofi
from src.ofi_multi_level import compute_multi_level_ofi
from src.ofi_integrated import compute_integrated_ofi
from src.ofi_cross_asset import compute_cross_asset_ofi


def test_best_level_ofi():
    data = {
        "bid_sz_00": [100, 110, 120],
        "ask_sz_00": [90, 95, 85]
    }
    df = pd.DataFrame(data)

    result = compute_best_level_ofi(df)

    expected = pd.Series([0, (110 - 100) - (95 - 90), (120 - 110) - (85 - 95)])
    assert np.allclose(result, expected), "Best-Level OFI computation incorrect"

    print("test_best_level_ofi passed.")


def test_integrated_ofi():
    ofi_series = pd.Series([1, 2, 3, 4, 5])
    result = compute_integrated_ofi(ofi_series, method="sum", window=3)

    expected = pd.Series([np.nan, np.nan, 6, 9, 12])
    assert np.allclose(result.dropna(), expected.dropna()), "Integrated OFI incorrect"

    print("test_integrated_ofi passed.")


def test_multi_level_ofi():
    data = {
        "bid_sz_00": [100, 120],
        "ask_sz_00": [90, 110],
        "bid_sz_01": [80, 100],
        "ask_sz_01": [85, 105]
    }
    df = pd.DataFrame(data)

    result = compute_multi_level_ofi(df, levels=2)

    expected = pd.Series([
        0,
        ((120 - 100) + (100 - 80)) - ((110 - 90) + (105 - 85))
    ])
    assert np.allclose(result, expected), "Multi-Level OFI computation incorrect"

    print("test_multi_level_ofi passed.")


def test_cross_asset_ofi():
    """
    Test compute_cross_asset_ofi function using mocked two-symbol dataset.
    Ensure that cross-asset OFI aligns base OFI to target timestamps correctly.
    """
    # Mock dataset: 3 timestamps for each symbol
    data = {
        "symbol": ["SPY"] * 3 + ["AAPL"] * 3,
        "ts_event": pd.to_datetime([
            "2024-01-01 10:00:01",
            "2024-01-01 10:00:02",
            "2024-01-01 10:00:03",
            "2024-01-01 10:00:02",
            "2024-01-01 10:00:03",
            "2024-01-01 10:00:04",
        ]),
        "bid_price": [1.0, 1.1, 1.2, 2.0, 2.1, 2.2],
        "ask_price": [1.1, 1.2, 1.3, 2.1, 2.2, 2.3],
        "bid_sz_00": [100, 110, 120, 200, 210, 220],
        "ask_sz_00": [90, 95, 100, 190, 195, 200],
    }
    df = pd.DataFrame(data)

    # Call function under test
    result = compute_cross_asset_ofi(
        df,
        compute_best_level_ofi,
        base_symbol="SPY",
        target_symbol="AAPL",
    )

    # Assertions
    assert isinstance(result, pd.Series), "Output should be a pandas Series"
    assert len(result) == 3, "Should return one OFI value per target timestamp"
    assert result.isna().sum() == 0, "There should be no missing values in the result"


if __name__ == "__main__":
    test_best_level_ofi()
    test_multi_level_ofi()
    test_integrated_ofi()
    test_cross_asset_ofi()
