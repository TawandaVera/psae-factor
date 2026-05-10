from psae_factor.analysis.returns import get_factor_and_returns
from psae_factor.analysis.ic import compute_ic, compute_ic_decay
from psae_factor.analysis.quantiles import compute_quantile_returns
from psae_factor.tears.full_tear import create_full_tear_sheet

__version__ = "0.1.0"
__all__ = [
    "get_factor_and_returns",
    "compute_ic",
    "compute_ic_decay",
    "compute_quantile_returns",
    "create_full_tear_sheet",
]
