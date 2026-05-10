from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from psae_factor.analysis.ic import compute_ic, compute_ic_decay, ic_summary
from psae_factor.analysis.quantiles import compute_quantile_returns


def create_full_tear_sheet(
    factor_data,
    periods=None,
    quantiles=5,
    benchmark_period=24,
    title="PSAE Factor Tear Sheet",
):
    if periods is None:
        periods = [1, 4, 24, 120]

    fig = plt.figure(figsize=(20, 20))
    fig.suptitle(title, fontsize=15, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.3)

    # Panel 1: IC by period
    ax1 = fig.add_subplot(gs[0, :])
    ic_df = compute_ic(factor_data, periods=periods)
    if not ic_df.empty:
        colors = ["green" if x > 0 else "red" for x in ic_df["IC_mean"]]
        ax1.bar([str(p) + "h" for p in ic_df.index], ic_df["IC_mean"], color=colors)
        ax1.axhline(0, color="black", linewidth=0.8)
        ax1.axhline(0.03, color="green", linestyle="--", alpha=0.5, label="IC=0.03 threshold")
        summary = ic_summary(ic_df)
        ax1.text(0.02, 0.95, str(summary), transform=ax1.transAxes, fontsize=8,
                 verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.4))
        ax1.legend(fontsize=8)
    ax1.set_title("Mean IC by Forward Period")
    ax1.set_ylabel("Information Coefficient")

    # Panel 2: Quantile returns
    ax2 = fig.add_subplot(gs[1, 0])
    qr = compute_quantile_returns(factor_data, quantiles=quantiles, period=benchmark_period)
    if not qr.empty:
        bar_colors = ["red", "salmon", "gray", "lightgreen", "green"][:len(qr)]
        ax2.bar(qr.index, qr["mean_return"] * 100, color=bar_colors)
        ax2.axhline(0, color="black", linewidth=0.8)
        ls = qr.attrs.get("ls_spread", None)
        if ls:
            ax2.set_xlabel(f"Q5-Q1 L/S Spread: {ls*100:.3f}%")
    ax2.set_title(f"Quantile Returns ({benchmark_period}h forward)")
    ax2.set_ylabel("Mean Return (%)")

    # Panel 3: IC Decay
    ax3 = fig.add_subplot(gs[1, 1])
    decay = compute_ic_decay(factor_data, max_hours=120, step=4)
    if not decay.empty:
        ax3.plot(decay.index, decay["IC_mean"], color="blue", linewidth=1.5)
        ax3.axhline(0, color="black", linewidth=0.8)
        ax3.fill_between(decay.index, 0, decay["IC_mean"],
                         where=(decay["IC_mean"] > 0), alpha=0.3, color="green")
        ax3.fill_between(decay.index, 0, decay["IC_mean"],
                         where=(decay["IC_mean"] < 0), alpha=0.3, color="red")
    ax3.set_title("IC Decay Curve")
    ax3.set_xlabel("Hours Forward")
    ax3.set_ylabel("IC")

    # Panel 4: Sector breakdown (if available)
    ax4 = fig.add_subplot(gs[2, :])
    if "sector" in factor_data.columns:
        col = f"return_{benchmark_period}h"
        if col in factor_data.columns:
            by_sector = factor_data.groupby("sector")[col].mean().sort_values()
            colors = ["green" if v > 0 else "red" for v in by_sector.values]
            ax4.barh(by_sector.index, by_sector.values * 100, color=colors)
            ax4.axvline(0, color="black", linewidth=0.8)
            ax4.set_title(f"Mean Return by Sector ({benchmark_period}h forward)")
            ax4.set_xlabel("Mean Return (%)")

    plt.tight_layout()
    return fig
