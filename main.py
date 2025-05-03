import pandas as pd
from src.ofi_best_level import compute_best_level_ofi
from src.ofi_multi_level import compute_multi_level_ofi
from src.ofi_integrated import compute_integrated_ofi
from src.ofi_cross_asset import compute_cross_asset_ofi

# Load data
df = pd.read_csv("data/first_25000_rows.csv")
print("Data loaded:", df.shape)

# Compute Best-Level OFI
best_ofi = compute_best_level_ofi(df)
df["best_level_ofi"] = best_ofi
df[["ts_event", "best_level_ofi"]].to_csv("data/best_level_ofi.csv", index=False)
print("Best-Level OFI saved.")

# Compute Multi-Level OFI
multi_ofi = compute_multi_level_ofi(df, levels=5)
df["multi_level_ofi"] = multi_ofi
df[["ts_event", "multi_level_ofi"]].to_csv("data/multi_level_ofi.csv", index=False)
print("Multi-Level OFI saved.")

# Compute Integrated OFI (rolling sum over multi-level OFI)
integrated_ofi = compute_integrated_ofi(df["multi_level_ofi"], method="sum", window=10)
df["integrated_ofi"] = integrated_ofi
df[["ts_event", "integrated_ofi"]].to_csv("data/integrated_ofi.csv", index=False)
print("Integrated OFI saved.")

# Compute Cross-Asset OFI
# Only run if multiple symbols present
if "symbol" in df.columns and df["symbol"].nunique() > 1:
    base_symbol = "SPY"  # Can be changed if needed
    unique_symbols = df["symbol"].unique()
    target_symbols = [sym for sym in unique_symbols if sym != base_symbol]

    for target_symbol in target_symbols:
        try:
            cross_ofi = compute_cross_asset_ofi(
                df,
                ofi_func=compute_best_level_ofi,
                base_symbol=base_symbol,
                target_symbol=target_symbol
            )
            df_target = df[df["symbol"] == target_symbol].copy()
            df_target["cross_asset_ofi"] = cross_ofi
            output_path = f"data/cross_asset_ofi_{target_symbol}.csv"
            df_target[["ts_event", "cross_asset_ofi"]].to_csv(output_path, index=False)
            print(f"Cross-Asset OFI saved for {target_symbol}.")
        except Exception as e:
            print(f"Error computing Cross-Asset OFI for {target_symbol}: {e}")
else:
    print("Cross-Asset OFI skipped (symbol column missing or only one symbol present).")
