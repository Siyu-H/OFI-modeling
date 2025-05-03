from typing import Literal
import pandas as pd

def compute_integrated_ofi(
    ofi_series: pd.Series, method: Literal["sum", "mean"] = "sum", window: int = 10
) -> pd.Series:
    """
    Compute Integrated OFI by applying a rolling window to existing OFI series.

    Parameters:
    - ofi_series: pd.Series, output from Best-Level or Multi-Level OFI
    - method: "sum" or "mean" for rolling calculation
    - window: rolling window size

    Returns:
    - pd.Series of integrated OFI
      Only outputs values when the full window is available (min_periods=window).
      This ensures that each integrated value reflects a complete and stable window of past order flow,
      which aligns with the methodology discussed in 'Cross-Impact of Order Flow Imbalance in Equity Markets'.

    Raises:
    - ValueError if method is not 'sum' or 'mean'
    """
    if method == "sum":
        return ofi_series.rolling(window=window, min_periods=window).sum()
    elif method == "mean":
        return ofi_series.rolling(window=window, min_periods=window).mean()
    else:
        raise ValueError("method must be 'sum' or 'mean'")

