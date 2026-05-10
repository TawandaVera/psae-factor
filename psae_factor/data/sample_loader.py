"""Helpers to load pricing and signals for research."""
import pandas as pd
import yfinance as yf
from pathlib import Path

DEFAULT_UNIVERSE = [
    "SPY", "XLI", "XLE", "JETS", "SLX", "TAN", "FXI",
    "ITA", "KBE", "TLT", "GLD", "QQQ",
]


def download_pricing(
    tickers: list[str] | None = None,
    start: str = "2017-01-01",
    end: str = "2021-01-20",
    interval: str = "1h",
    cache_path: str | None = None,
) -> pd.DataFrame:
    if tickers is None:
        tickers = DEFAULT_UNIVERSE
    if cache_path and Path(cache_path).exists():
        return pd.read_parquet(cache_path)
    data = yf.download(tickers, start=start, end=end, interval=interval, progress=False)
    df = data["Close"]
    if cache_path:
        df.to_parquet(cache_path)
    return df


def load_signals_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    assert "ticker" in df.columns
    assert "signal_score" in df.columns
    return df
