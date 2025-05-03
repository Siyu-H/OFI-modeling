import pandas as pd


def compute_multi_level_ofi(df: pd.DataFrame, levels: int = 5) -> pd.Series:
    """
    Compute Multi-Level Order Flow Imbalance (OFI) using the top N levels of the order book.

    Formula:
        OFI = sum over i of (1 / (i+1)) * (bid_size_i[t] - bid_size_i[t-1] - ask_size_i[t] + ask_size_i[t-1])

    This represents the weighted difference between the change in bid size and ask size at each depth level i.
    Deeper levels receive less weight (1 / (i+1)) as they have less immediate price impact.

    Parameters:
    - df: pandas DataFrame with columns like 'bid_sz_00', 'ask_sz_00', ..., for multiple levels
    - levels: int, number of levels to include (default is 5)

    Returns:
    - pd.Series of multi-level OFI values
    """
    ofi = pd.Series(0.0, index=df.index)

    for i in range(levels):
        bid_col = f"bid_sz_0{i}"
        ask_col = f"ask_sz_0{i}"

        if bid_col in df.columns and ask_col in df.columns:
            bid_diff = df[bid_col].diff().fillna(0)
            ask_diff = df[ask_col].diff().fillna(0)
            weight = 1.0 / (i + 1)
            ofi += weight * (bid_diff - ask_diff)

    return ofi
