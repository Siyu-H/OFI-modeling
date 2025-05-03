import pandas as pd

def compute_cross_asset_ofi(
    df: pd.DataFrame, ofi_func, base_symbol: str, target_symbol: str
) -> pd.Series:
    """
    Compute Cross-Asset OFI: Use the OFI from base_symbol as a predictive feature for target_symbol.

    Parameters:
    - df: DataFrame containing order book data for multiple symbols
    - ofi_func: function to compute OFI (e.g., compute_best_level_ofi)
    - base_symbol: str, the asset providing the OFI (e.g., 'SPY')
    - target_symbol: str, the asset receiving the OFI (e.g., 'AAPL')

    Returns:
    - pd.Series containing the base_symbol's OFI aligned to the target_symbol's timestamps
    """
    # Split the dataset into base and target symbol data
    df_base = df[df["symbol"] == base_symbol].copy()
    df_target = df[df["symbol"] == target_symbol].copy()

    # Compute OFI for the base asset
    base_ofi = ofi_func(df_base)
    df_base["cross_ofi"] = base_ofi
    df_base = df_base[["ts_event", "cross_ofi"]]

    # Ensure timestamps are datetime and sort both DataFrames
    df_target["ts_event"] = pd.to_datetime(df_target["ts_event"])
    df_base["ts_event"] = pd.to_datetime(df_base["ts_event"])

    df_target = df_target.sort_values("ts_event")
    df_base = df_base.sort_values("ts_event")

    # Align base OFI to target timestamps (at most 1 second before)
    merged = pd.merge_asof(
        df_target,
        df_base,
        on="ts_event",
        direction="backward",
        tolerance=pd.Timedelta("1s"),
    )

    return merged["cross_ofi"].fillna(0)
