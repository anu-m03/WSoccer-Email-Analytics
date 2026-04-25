"""
zscore_distribution.py
Purdue Women's Soccer – Population Z-Score & Distribution Analysis

Reconstructs ~5000 individual strength scores from per-group statistics
(mean, std, n) stored in evaluation_results_tableau.csv, computes population
z-scores, and plots the distribution vs. a fitted normal curve.

Outputs:
    zscore_distribution.png   — 3-panel distribution figure
    evaluation_results_tableau.csv  — updated in-place with z-score columns
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
TABLEAU_CSV  = Path(__file__).parent / "evaluation_results_tableau.csv"
OUT_PNG      = Path(__file__).parent / "strength_score_distribution.png"
SEED         = 42
SCORE_LO, SCORE_HI = 0.0, 10.0

BG       = "#F8FAFC"
BLUE     = "#2563EB"
GREEN    = "#16A34A"
RED      = "#DC2626"
GRAY     = "#6B7280"
GRID_CLR = "#E2E8F0"

plt.rcParams.update({
    "font.family":       "sans-serif",
    "axes.facecolor":    BG,
    "figure.facecolor":  BG,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        GRID_CLR,
    "grid.linewidth":    0.7,
})


# ── 1. Load group stats ───────────────────────────────────────────────────────
df = pd.read_csv(TABLEAU_CSV)
n_arr  = df["n_players"].values.astype(float)
mu_arr = df["score_mean"].values.astype(float)
sg_arr = df["score_std"].values.astype(float)
N_total = int(n_arr.sum())


# ── 2. Compute pooled population parameters ───────────────────────────────────
grand_mu  = (n_arr * mu_arr).sum() / N_total
pooled_var = (
    ((n_arr - 1) * sg_arr**2).sum()
    + (n_arr * (mu_arr - grand_mu)**2).sum()
) / (N_total - 1)
grand_sig = math.sqrt(pooled_var)

print(f"Population mean  μ  = {grand_mu:.4f}")
print(f"Population std   σ  = {grand_sig:.4f}")
print(f"Population var   σ² = {pooled_var:.4f}")
print(f"Total players    N  = {N_total}")


# ── 3. Reconstruct individual scores (truncated normal per group) ─────────────
rng    = np.random.default_rng(SEED)
scores = []
for n_i, mu_i, sg_i in zip(n_arr, mu_arr, sg_arr):
    n_i = int(n_i)
    # Draw from N(μ_i, σ_i), clip to [0, 10]
    s = rng.normal(loc=mu_i, scale=max(sg_i, 0.001), size=n_i)
    s = np.clip(s, SCORE_LO, SCORE_HI)
    scores.append(s)

scores = np.concatenate(scores)   # shape (5000,)

# Adjust to match exact grand_mu and grand_sig
scores = (scores - scores.mean()) / scores.std(ddof=1) * grand_sig + grand_mu
scores = np.clip(scores, SCORE_LO, SCORE_HI)


# ── 4. Compute z-scores ───────────────────────────────────────────────────────
z_scores = (scores - grand_mu) / grand_sig

# Manual skewness & kurtosis (no scipy)
z_skew = np.mean(((scores - grand_mu) / grand_sig) ** 3)
z_kurt = np.mean(((scores - grand_mu) / grand_sig) ** 4) - 3  # excess

print(f"\nDistribution shape:")
print(f"  Skewness (γ₁) = {z_skew:.4f}  (0 = symmetric)")
print(f"  Kurtosis (γ₂) = {z_kurt:.4f}  (0 = normal)")
print(f"  % at floor=0  = {(scores == 0.0).mean()*100:.1f}%")


# ── 5. Update tableau CSV with population z-score columns ─────────────────────
df["population_mean"] = round(grand_mu,  4)
df["population_std"]  = round(grand_sig, 4)
df["group_z_score"]   = ((df["score_mean"] - grand_mu) / grand_sig).round(4)
df.to_csv(TABLEAU_CSV, index=False)
print(f"\nTableau CSV updated → {TABLEAU_CSV}")


# ── 6. Normal PDF helper ──────────────────────────────────────────────────────
def norm_pdf(x, mu=0.0, sigma=1.0):
    return (1 / (sigma * math.sqrt(2 * math.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


# ── 7. Plot ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 5.5), facecolor=BG)
fig.suptitle(
    "Purdue WS Recruiting – Strength Score Distribution  (N = 5,000 players, 50 groups)",
    fontsize=13, fontweight="bold", color="#111827", y=1.01
)
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.38)

# ── Panel A: Raw strength score histogram + Normal fit ────────────────────────
ax1 = fig.add_subplot(gs[0])
bins_raw = np.linspace(SCORE_LO, SCORE_HI, 36)
counts, edges, _ = ax1.hist(
    scores, bins=bins_raw, density=True, color=BLUE, alpha=0.65,
    edgecolor="white", linewidth=0.4, label="Simulated scores", zorder=3
)
x_raw = np.linspace(SCORE_LO, SCORE_HI, 400)
ax1.plot(x_raw, norm_pdf(x_raw, grand_mu, grand_sig), color=RED, lw=2.2,
         label=f"N(μ={grand_mu:.2f}, σ={grand_sig:.2f})", zorder=4)
ax1.axvline(grand_mu, color=RED, lw=1.2, ls="--", alpha=0.7)
ax1.set_xlabel("Strength Score (0–10)", fontsize=10, color="#374151")
ax1.set_ylabel("Density", fontsize=10, color="#374151")
ax1.set_title("A  Raw Score Distribution", fontsize=11, fontweight="bold", color="#111827")
ax1.legend(fontsize=8.5, framealpha=0.6)
ax1.set_xlim(SCORE_LO, SCORE_HI)

# ── Panel B: Z-score histogram + N(0,1) ──────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
z_lo, z_hi = -1.5, 4.5
bins_z = np.linspace(z_lo, z_hi, 36)
ax2.hist(
    z_scores, bins=bins_z, density=True, color=GREEN, alpha=0.65,
    edgecolor="white", linewidth=0.4, label="Z-scores", zorder=3
)
x_z = np.linspace(z_lo, z_hi, 400)
ax2.plot(x_z, norm_pdf(x_z, 0, 1), color=RED, lw=2.2,
         label="N(0, 1) reference", zorder=4)
ax2.axvline(0, color=RED, lw=1.2, ls="--", alpha=0.7)

# Shade ±1σ / ±2σ bands
for lo, hi, alpha in [(-1, 1, 0.08), (-2, 2, 0.04)]:
    ax2.axvspan(lo, hi, color=GREEN, alpha=alpha, zorder=1)

stats_text = (
    f"μ = {grand_mu:.3f}\n"
    f"σ = {grand_sig:.3f}\n"
    f"skew = {z_skew:.3f}\n"
    f"kurt = {z_kurt:.3f}"
)
ax2.text(0.97, 0.96, stats_text, transform=ax2.transAxes,
         fontsize=8.5, va="top", ha="right",
         bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.7, ec=GRID_CLR))
ax2.set_xlabel("Z-Score  (σ units from μ)", fontsize=10, color="#374151")
ax2.set_ylabel("Density", fontsize=10, color="#374151")
ax2.set_title("B  Z-Score Distribution vs N(0,1)", fontsize=11, fontweight="bold", color="#111827")
ax2.legend(fontsize=8.5, framealpha=0.6)
ax2.set_xlim(z_lo, z_hi)

# ── Panel C: Group means plotted as z-scores (dot strip + N(0,1)) ─────────────
ax3 = fig.add_subplot(gs[2])
group_z = df["group_z_score"].values
z_lo3, z_hi3 = -3.2, 3.2
bins_g = np.linspace(z_lo3, z_hi3, 22)
ax3.hist(
    group_z, bins=bins_g, density=True, color="#7C3AED", alpha=0.65,
    edgecolor="white", linewidth=0.4, label="Group mean z-scores", zorder=3
)
x_g = np.linspace(z_lo3, z_hi3, 400)
ax3.plot(x_g, norm_pdf(x_g, 0, 1), color=RED, lw=2.2,
         label="N(0, 1) expected", zorder=4)
ax3.axvline(0, color=RED, lw=1.2, ls="--", alpha=0.7)

gm_skew = float(np.mean(group_z**3))
gm_kurt = float(np.mean(group_z**4)) - 3
ax3.text(0.97, 0.96,
         f"n groups = {len(group_z)}\nskew = {gm_skew:.3f}\nkurt = {gm_kurt:.3f}",
         transform=ax3.transAxes, fontsize=8.5, va="top", ha="right",
         bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.7, ec=GRID_CLR))
ax3.set_xlabel("Z-Score of Group Mean", fontsize=10, color="#374151")
ax3.set_ylabel("Density", fontsize=10, color="#374151")
ax3.set_title("C Group Score Mean Distribution (CLT)", fontsize=11, fontweight="bold", color="#111827")
ax3.legend(fontsize=8.5, framealpha=0.6)
ax3.set_xlim(z_lo3, z_hi3)

plt.tight_layout()
plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
print(f"Plot saved        → {OUT_PNG}")
plt.close()
