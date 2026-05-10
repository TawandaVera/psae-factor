from __future__ import annotations
import pandas as pd
import numpy as np


def get_factor_and_returns(
    signals: pd.DataFrame,
    pricing: pd.DataFrame,
    periods: list[int] | None = None,
    groupby: dict | None = None,
    neutralise: list[str] | None = None,
    min_confidence: float = 0.6,
) -> pd.DataFrame:
    """
    Main entry point — analogous to alphalens.utils.get_clean_factor_and_forward_returns().

    Args:
        signals: DataFrame with columns [timestamp, ticker, signal_score, confidence, ...]
        pricing: Wide DataFrame: DatetimeIndex (hourly), columns=tickers
        periods: Forward periods in hours, default [1, 4, 24, 120]
        groupby: ticker → sector string mapping
        neutralise: list of neutralisation methods, e.g. ['beta', 'sector']
        min_confidence: Drop signals below this confidence

    Returns:
        MultiIndex DataFrame (date, asset) with signal + forward returns
    """
    if periods is None:
        periods = [1, 4, 24, 120]
    if neutralise is None:
        neutralise = []

    signals = signals[signals.get("confidence", pd.Series(1.0, index=signals.index)) >= min_confidence].copy()

    records = []
    for _, row in signals.iterrows():
        t = pd.Timestamp(row["timestamp"])
        ticker = row["ticker"]
        score = float(row["signal_score"])

        if ticker not in pricing.columns:
            continue

        col_data = pricing[ticker].dropna()
        future_idx = col_data.index[col_data.index >= t]
        if len(future_idx) == 0:
            continue
        t_start = future_idx[0]

        record = {
            "date": t,
            "asset": ticker,
            "signal": score,
            "sector": groupby.get(ticker, "Unknown") if groupby else "Unknown",
        }

        for p in periods:
            future_p = col_data.index[col_data.index >= t + pd.Timedelta(hours=p)]
            if len(future_p) == 0:
                record[f"return_{p}h"] = np.nan
            else:
                t_end = future_p[0]
                ret = (col_data[t_end] / col_data[t_start]) - 1
                record[f"return_{p}h"] = round(ret, 6)

        records.append(record)

    df = pd.DataFrame(records)
    if df.empty:
        return df
    df = df.set_index(["date", "asset"])
    return df
