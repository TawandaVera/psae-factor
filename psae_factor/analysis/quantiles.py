from __future__ import annotations
import pandas as pd


def compute_quantile_returns(
    factor_data: pd.DataFrame,
    quantiles: int = 5,
    period: int = 24,
) -> pd.DataFrame:
    """Q1=most bearish, Q5=most bullish. Q5-Q1 spread = long-short alpha."""
    col = f"return_{period}h"
    clean = factor_data[["signal", col]].dropna()
    if len(clean) < quantiles * 5:
        return pd.DataFrame()
    clean = clean.copy()
    clean["quantile"] = pd.qcut(clean["signal"], q=quantiles, labels=False, duplicates="drop") + 1
    result = clean.groupby("quantile")[col].agg(["mean", "std", "count"])
    result.columns = ["mean_return", "std_return", "n_obs"]
    if len(result) >= 2:
        result.attrs["ls_spread"] = result["mean_return"].iloc[-1] - result["mean_return"].iloc[0]
    return result
