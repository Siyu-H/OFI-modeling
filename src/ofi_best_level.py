import pandas as pd

def compute_best_level_ofi(df: pd.DataFrame) -> pd.Series:
    """
    Compute Best-Level Order Flow Imbalance (OFI) using only the top level (Level 0) of the order book.

    Formula:
        OFI = bid_size_0[t] - bid_size_0[t-1] - (ask_size_0[t] - ask_size_0[t-1])

    This captures the net change in liquidity at the best bid and ask. 
    A positive value indicates strengthening demand (more bids or fewer asks),
    while a negative value indicates increasing supply pressure.

    Parameters:
    - df: pandas DataFrame containing at least 'bid_sz_00' and 'ask_sz_00' columns
    - These represent the visible liquidity at the top of the order book

    Returns:
    - pd.Series of best-level OFI values, aligned with the input index
    """
    required_cols = {"bid_sz_00", "ask_sz_00"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

    bid_diff = df["bid_sz_00"].diff().fillna(0)
    ask_diff = df["ask_sz_00"].diff().fillna(0)
    return bid_diff - ask_diff