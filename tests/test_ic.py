import pandas as pd
import numpy as np
from psae_factor.analysis.ic import compute_ic, ic_summary


def _make_factor_data():
    np.random.seed(42)
    n = 200
    signals = np.random.uniform(-1, 1, n)
    # Correlated returns (IC ~ 0.3)
    returns = signals * 0.3 + np.random.normal(0, 0.5, n)
    return pd.DataFrame({
        "signal": signals,
        "return_24h": returns,
    }, index=pd.MultiIndex.from_tuples(
        [(pd.Timestamp("2020-01-01") + pd.Timedelta(hours=i), f"T{i%10}") for i in range(n)],
        names=["date", "asset"]
    ))


def test_compute_ic_returns_dataframe():
    data = _make_factor_data()
    ic = compute_ic(data, periods=[24])
    assert not ic.empty
    assert "IC_mean" in ic.columns
    assert "t_stat" in ic.columns


def test_ic_summary():
    data = _make_factor_data()
    ic = compute_ic(data, periods=[24])
    summary = ic_summary(ic)
    assert "mean_ic" in summary
    assert isinstance(summary["mean_ic"], float)
