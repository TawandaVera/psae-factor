from __future__ import annotations
import pandas as pd
import numpy as np
from scipy import stats


def compute_ic(
    factor_data: pd.DataFrame,
    periods: list[int] | None = None,
    method: str = "spearman",
) -> pd.DataFrame:
    """Compute Information Coefficient per forward period."""
    if periods is None:
        periods = [1, 4, 24, 120]

    rows = []
    for p in periods:
        col = f"return_{p}h"
        if col not in factor_data.columns:
            continue
        clean = factor_data[["signal", col]].dropna()
        if len(clean) < 10:
            continue
        if method == "spearman":
            ic, p_val = stats.spearmanr(clean["signal"], clean[col])
        else:
            ic, p_val = stats.pearsonr(clean["signal"], clean[col])

        rows.append({
            "period_hours": p,
            "IC_mean": round(ic, 6),
            "t_stat": round(ic / (1 / np.sqrt(len(clean))), 3),
            "p_value": round(p_val, 4),
            "n_observations": len(clean),
        })

    return pd.DataFrame(rows).set_index("period_hours") if rows else pd.DataFrame()


def compute_ic_decay(
    factor_data: pd.DataFrame,
    max_hours: int = 120,
    step: int = 4,
) -> pd.DataFrame:
    periods = list(range(1, max_hours + 1, step))
    return compute_ic(factor_data, periods=periods)


def ic_summary(ic_df: pd.DataFrame) -> dict:
    if ic_df.empty:
        return {}
    return {
        "mean_ic": round(ic_df["IC_mean"].mean(), 6),
        "ic_ir": round(ic_df["IC_mean"].mean() / ic_df["IC_mean"].std(), 3) if ic_df["IC_mean"].std() > 0 else None,
        "pct_positive": round((ic_df["IC_mean"] > 0).mean(), 3),
        "max_t_stat": round(ic_df["t_stat"].max(), 3),
        "best_period_h": int(ic_df["IC_mean"].idxmax()),
    }
