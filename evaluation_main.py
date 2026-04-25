"""
evaluation_main.py
Purdue Women's Soccer – Algorithm Accuracy Evaluation

Runs the recruiting email pipeline across all group folders inside test_emails/,
collects per-group strength score statistics, and reports cross-group distribution
metrics to evaluate algorithm consistency.

Target: 10–15% promotion rate per group.

Usage:
    python evaluation_main.py                         # auto-discovers all group folders
    python evaluation_main.py --groups-dir test_emails
    python evaluation_main.py --threshold 5.0
    python evaluation_main.py --out all_player_scores.csv
"""

import argparse
import math
import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import testing_main as tm


# ──────────────────────────────────────────────────────────────────────────────
# CORE: run one group folder through the pipeline
# ──────────────────────────────────────────────────────────────────────────────
def evaluate_group(
    group_dir: Path,
    matcher: tm.ClubMatcher,
    threshold: float,
) -> tuple[dict, pd.DataFrame] | None:
    """
    Parse all emails in group_dir, score them, and return:
      (stats_dict, per_player_df)
    Returns None if the folder contains no email files.

    per_player_df columns:
      group, file_name, player_name, player_club, achievements,
      achievements_score, strength_score, promoted[, youtube_links]
    """
    email_files = sorted(
        p for ext in ("*.txt", "*.eml") for p in group_dir.glob(ext)
    )
    if not email_files:
        return None

    rows        = [tm.parse_email_file(p, matcher) for p in email_files]
    playersDF   = pd.DataFrame(rows)
    players_ach = tm.build_player_ach(playersDF, threshold=threshold)

    # Attach club info to per-player df for the all-scores CSV
    players_ach = players_ach.copy()
    players_ach.insert(0, "group", group_dir.name)
    if "player_club" in playersDF.columns:
        players_ach["player_club"] = playersDF["player_club"].values

    scores     = players_ach["strength_score"]
    ind_scores  = players_ach["individual_score"] if "individual_score" in players_ach.columns else pd.Series([0.0] * len(players_ach))
    team_scores = players_ach["team_score"]       if "team_score"       in players_ach.columns else pd.Series([0.0] * len(players_ach))
    n_total    = len(scores)
    n_promoted = int((scores >= threshold).sum())

    def _agg(s: pd.Series) -> dict:
        if len(s) == 0:
            return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "median": 0.0}
        return {
            "mean":   round(float(s.mean()), 4),
            "std":    round(float(s.std(ddof=1)), 4) if len(s) > 1 else 0.0,
            "min":    round(float(s.min()), 4),
            "max":    round(float(s.max()), 4),
            "median": round(float(s.median()), 4),
        }

    s_agg   = _agg(scores)
    ind_agg = _agg(ind_scores)
    tm_agg  = _agg(team_scores)

    stats = {
        "group":         group_dir.name,
        "n_players":     n_total,
        "n_promoted":    n_promoted,
        "pct_promoted":  round(n_promoted / n_total * 100, 2) if n_total else 0.0,
        "score_mean":    s_agg["mean"],
        "score_std":     s_agg["std"],
        "score_min":     s_agg["min"],
        "score_max":     s_agg["max"],
        "score_median":  s_agg["median"],
        "ind_score_mean":    ind_agg["mean"],
        "ind_score_std":     ind_agg["std"],
        "ind_score_min":     ind_agg["min"],
        "ind_score_max":     ind_agg["max"],
        "ind_score_median":  ind_agg["median"],
        "team_score_mean":   tm_agg["mean"],
        "team_score_std":    tm_agg["std"],
        "team_score_min":    tm_agg["min"],
        "team_score_max":    tm_agg["max"],
        "team_score_median": tm_agg["median"],
    }

    return stats, players_ach


# ──────────────────────────────────────────────────────────────────────────────
# DISPLAY
# ──────────────────────────────────────────────────────────────────────────────
TARGET_LOW  = 10.0
TARGET_HIGH = 15.0

def _flag(pct: float) -> str:
    if pct < TARGET_LOW:
        return "↓ LOW"
    if pct > TARGET_HIGH:
        return "↑ HIGH"
    return "✓"

def print_group_table(results: list[dict], tgt_low: float, tgt_high: float) -> None:
    def flag(pct):
        if pct < tgt_low:   return "↓ LOW"
        if pct > tgt_high:  return "↑ HIGH"
        return "✓"

    print()
    header = (
        f"{'Group':<22} {'N':>5} {'Promoted':>9} {'%Promo':>7} "
        f"{'Mean':>7} {'Std':>7} {'Min':>6} {'Max':>6} {'Flag':>7}"
    )
    print(header)
    print("─" * len(header))
    for r in results:
        print(
            f"{r['group']:<22} {r['n_players']:>5} {r['n_promoted']:>9} "
            f"{r['pct_promoted']:>6.1f}% {r['score_mean']:>7.3f} "
            f"{r['score_std']:>7.3f} {r['score_min']:>6.2f} "
            f"{r['score_max']:>6.2f} {flag(r['pct_promoted']):>7}"
        )


def print_summary(results: list[dict], threshold: float, tgt_low: float, tgt_high: float) -> None:
    df = pd.DataFrame(results)

    pct_vals   = df["pct_promoted"].values
    mean_vals  = df["score_mean"].values
    std_vals   = df["score_std"].values

    n_in_target  = int(((pct_vals >= tgt_low) & (pct_vals <= tgt_high)).sum())
    n_low        = int((pct_vals < tgt_low).sum())
    n_high       = int((pct_vals > tgt_high).sum())

    total_players  = int(df["n_players"].sum())
    total_promoted = int(df["n_promoted"].sum())

    W = 62
    print(f"\n{'═' * W}")
    print(f"  CROSS-GROUP SUMMARY  ({len(results)} groups, threshold ≥ {threshold})")
    print(f"{'═' * W}")
    print(f"  Total players evaluated        : {total_players}")
    print(f"  Total promoted                 : {total_promoted}  "
          f"({round(total_promoted / total_players * 100, 2)}% overall)")
    print(f"{'─' * W}")
    print(f"  Promotion rate  — mean         : {np.mean(pct_vals):.2f}%")
    print(f"  Promotion rate  — std dev      : {np.std(pct_vals, ddof=1):.2f}%")
    print(f"  Promotion rate  — min / max    : {np.min(pct_vals):.1f}% / {np.max(pct_vals):.1f}%")
    print(f"{'─' * W}")
    print(f"  Target window ({tgt_low:.0f}–{tgt_high:.0f}%):")
    print(f"    ✓  Within target             : {n_in_target} / {len(results)} groups "
          f"({round(n_in_target / len(results) * 100, 1)}%)")
    print(f"    ↓  Below target (<{tgt_low:.0f}%)        : {n_low} groups")
    print(f"    ↑  Above target (>{tgt_high:.0f}%)       : {n_high} groups")
    print(f"{'─' * W}")
    print(f"  Strength score  — grand mean   : {np.mean(mean_vals):.3f}")
    print(f"  Strength score  — mean of stds : {np.mean(std_vals):.3f}")
    print(f"  Strength score  — std of means : {np.std(mean_vals, ddof=1):.3f}  "
          f"(consistency across groups)")
    print(f"{'═' * W}\n")


# ──────────────────────────────────────────────────────────────────────────────
# TABLEAU EXPORT
# ──────────────────────────────────────────────────────────────────────────────
def save_tableau_csv(
    results: list[dict],
    threshold: float,
    tgt_low: float,
    tgt_high: float,
    out_path: Path,
) -> None:
    df = pd.DataFrame(results).copy()

    # Derived columns
    df.insert(0, "group_index", range(1, len(df) + 1))

    pct   = df["pct_promoted"].values.astype(float)
    means = df["score_mean"].values.astype(float)

    # Z-scores (handle edge case of single group / zero std)
    pct_std  = float(np.std(pct,   ddof=1)) if len(pct)   > 1 else 1.0
    mean_std = float(np.std(means, ddof=1)) if len(means) > 1 else 1.0
    pct_mu   = float(np.mean(pct))
    mean_mu  = float(np.mean(means))

    df["score_range"]   = (df["score_max"] - df["score_min"]).round(4)
    df["promo_status"]  = df["pct_promoted"].apply(
        lambda p: "In Target" if tgt_low <= p <= tgt_high
                  else ("Below Target" if p < tgt_low else "Above Target")
    )
    df["in_target"]     = (
        (df["pct_promoted"] >= tgt_low) & (df["pct_promoted"] <= tgt_high)
    ).astype(int)
    df["promo_z_score"] = ((pct   - pct_mu)  / pct_std ).round(4)
    df["mean_z_score"]  = ((means - mean_mu) / mean_std).round(4)

    # Quartile labels (1 = lowest, 4 = highest)
    df["promo_quartile"] = pd.qcut(df["pct_promoted"], q=4,
                                   labels=[1, 2, 3, 4], duplicates="drop")
    df["mean_quartile"]  = pd.qcut(df["score_mean"],   q=4,
                                   labels=[1, 2, 3, 4], duplicates="drop")

    # Metadata columns for Tableau context
    df["threshold"]    = threshold
    df["target_low"]   = tgt_low
    df["target_high"]  = tgt_high

    # Column order — explicit so Tableau sees them cleanly
    cols = [
        "group_index", "group",
        "n_players", "n_promoted", "pct_promoted",
        "score_mean", "score_std", "score_min", "score_max", "score_median", "score_range",
        "ind_score_mean", "ind_score_std", "ind_score_min", "ind_score_max", "ind_score_median",
        "team_score_mean", "team_score_std", "team_score_min", "team_score_max", "team_score_median",
        "promo_status", "in_target",
        "promo_z_score", "mean_z_score",
        "promo_quartile", "mean_quartile",
        "threshold", "target_low", "target_high",
    ]
    df[cols].to_csv(out_path, index=False)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Evaluate algorithm accuracy across all group folders in test_emails/."
    )
    parser.add_argument(
        "--groups-dir", default="test_emails",
        help="Folder containing group subfolders (default: test_emails/).",
    )
    parser.add_argument(
        "--clubs", default="clubs.xlsx",
        help="Path to clubs.xlsx (default: clubs.xlsx in project dir).",
    )
    parser.add_argument(
        "--threshold", type=float, default=tm.PROMOTION_THRESHOLD,
        help=f"Promotion score threshold (default: {tm.PROMOTION_THRESHOLD}).",
    )
    parser.add_argument(
        "--out", default="all_player_scores.csv",
        help="Output CSV path for all individual player scores (default: all_player_scores.csv).",
    )
    parser.add_argument(
        "--target-low", type=float, default=TARGET_LOW,
        help=f"Lower bound of target promotion %% (default: {TARGET_LOW}).",
    )
    parser.add_argument(
        "--target-high", type=float, default=TARGET_HIGH,
        help=f"Upper bound of target promotion %% (default: {TARGET_HIGH}).",
    )
    args = parser.parse_args()

    # Allow overriding the target window from CLI
    tgt_low  = args.target_low
    tgt_high = args.target_high

    # Anchor to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)

    clubs_xlsx  = Path(args.clubs)
    groups_root = Path(args.groups_dir)

    if not clubs_xlsx.exists():
        sys.exit(f"[error] clubs.xlsx not found at: {clubs_xlsx.resolve()}")
    if not groups_root.exists():
        sys.exit(f"[error] Groups directory not found: {groups_root.resolve()}")

    # Discover group folders (any subfolder inside groups_root)
    group_dirs = sorted(
        d for d in groups_root.iterdir()
        if d.is_dir()
    )
    if not group_dirs:
        sys.exit(f"[error] No subfolders found in {groups_root}.")

    print(f"Clubs file   : {clubs_xlsx.resolve()}")
    print(f"Groups dir   : {groups_root.resolve()}")
    print(f"Groups found : {len(group_dirs)}")
    print(f"Threshold    : strength_score >= {args.threshold}")
    print(f"Target window: {tgt_low:.0f}–{tgt_high:.0f}% promotion rate")

    # Build clubs matcher once — reused for all groups
    print("\nBuilding club matcher...")
    clubs_df = tm.get_clubs(str(clubs_xlsx))
    matcher  = tm.build_club_matcher(clubs_df)
    print(f"  {len(clubs_df)} clubs loaded.\n")

    # Run each group
    results          = []   # per-group stats (for tableau)
    all_player_parts = []   # per-player dfs (for all_player_scores.csv)
    for i, gdir in enumerate(group_dirs, 1):
        print(f"  [{i:>3}/{len(group_dirs)}] {gdir.name} ...", end=" ", flush=True)
        outcome = evaluate_group(gdir, matcher, args.threshold)
        if outcome is None:
            print("no email files — skipped")
            continue
        stats, player_df = outcome
        # Tag each player row with its group index so it's joinable with the tableau CSV
        player_df = player_df.copy()
        player_df.insert(1, "group_index", i)
        results.append(stats)
        all_player_parts.append(player_df)
        print(
            f"{stats['n_players']} players | "
            f"{stats['n_promoted']} promoted ({stats['pct_promoted']:.1f}%) | "
            f"mean score {stats['score_mean']:.3f}"
        )

    if not results:
        sys.exit("[error] No groups produced results.")

    # Display detailed table and summary
    print_group_table(results, tgt_low, tgt_high)
    print_summary(results, args.threshold, tgt_low, tgt_high)

    # Save all-player scores CSV (one row per player across all groups)
    out_path     = Path(args.out)
    all_scores   = pd.concat(all_player_parts, ignore_index=True)

    # Build a clean, ordered column list (youtube_links optional)
    base_cols = [
        "group_index", "group",
        "file_name", "player_name", "player_club",
        "achievements", "achievements_score",
        "individual_score", "team_score", "strength_score", "promoted",
    ]
    # Drop any columns not actually present (e.g. achievements_score legacy name)
    base_cols = [c for c in base_cols if c in all_scores.columns or c in ("group_index", "group")]
    if "youtube_links" in all_scores.columns:
        base_cols.append("youtube_links")
    all_scores[base_cols].to_csv(out_path, index=False)
    print(f"All player scores → {out_path.resolve()}  ({len(all_scores)} rows)")

    # Save Tableau scatter-plot CSV (per-group stats, unchanged)
    tableau_path = out_path.parent / "evaluation_results_tableau.csv"
    save_tableau_csv(results, args.threshold, tgt_low, tgt_high, tableau_path)
    print(f"Tableau CSV       → {tableau_path.resolve()}\n")


if __name__ == "__main__":
    main()
