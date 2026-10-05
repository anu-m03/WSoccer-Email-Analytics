"""
report_export.py
Purdue Women's Soccer – coach-facing recruiting report

Builds the two things the report email carries (see docs/report-redesign.md):

    Recruiting_Report_<date>.xlsx   one workbook, every sheet sorted by score with
                                    filters on and the header row frozen
        Promoted         promoted players only
        All Players      everyone, plus a Promoted column
        Needs Review     rows a person should check, with the reason
        Score Breakdown  player x achievement x weight, to see why a score is what it is
    Report_Summary_<date>.html      the email body: counts + the promoted table

Position Group (Goalkeeper / Defender / Midfielder / Forward) sits next to
Primary Position so one filter selects e.g. every defender regardless of how
specifically the player described it.  Blank always means "not found".
"""

import html
import re
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

POSITION_GROUP = {
    "Goalkeeper": "Goalkeeper",
    "Center Back": "Defender", "Left Back": "Defender", "Right Back": "Defender",
    "Left Wing Back": "Defender", "Right Wing Back": "Defender",
    "Fullback": "Defender", "Defender": "Defender",
    "Defensive Midfielder": "Midfielder", "Center Midfielder": "Midfielder",
    "Attacking Midfielder": "Midfielder", "Left Midfielder": "Midfielder",
    "Right Midfielder": "Midfielder", "Midfielder": "Midfielder",
    "Left Winger": "Forward", "Right Winger": "Forward", "Winger": "Forward",
    "Striker": "Forward", "Forward": "Forward",
}

PLAYER_COLS = [
    "Player", "Position Group", "Primary Position", "Dominant Foot", "Club",
    "Score", "Achievements", "Email", "Video", "Subject", "Received",
]
_WRAP_COLS = {"Achievements", "Reason"}
_WIDTHS = {
    "Player": 22, "Position Group": 15, "Primary Position": 21, "Dominant Foot": 14,
    "Club": 30, "Score": 8, "Achievements": 50, "Email": 30, "Video": 40,
    "Subject": 50, "Received": 12, "Promoted": 11, "Reason": 34, "File": 12,
    "Achievement": 36, "Category": 12, "Weight": 9,
}
_TIMESTAMP_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}) \d{2}:\d{2}")
_REPLY_PREFIX_RE = re.compile(r"^(?:\s*(?:fw|fwd|re)\s*:\s*)+", re.I)
_HEADER_RE = re.compile(r"(?i)^\s*(subject|date)\s*:\s*(.*)$")


def _as_list(val) -> list:
    if isinstance(val, (list, tuple)):
        return [v for v in val if isinstance(v, str) and v.strip()]
    if isinstance(val, str) and val.strip():
        return [val.strip()]
    return []


def _blank(val) -> str:
    return "" if val is None or (isinstance(val, float) and pd.isna(val)) else str(val).strip()


def _subject_and_date(raw_text) -> tuple[str, str]:
    """get_gmails.py layout (sender / subject (may wrap) / timestamp / body),
    falling back to "Subject:" / "Date:" header lines (.eml layout)."""
    if not isinstance(raw_text, str):
        return "", ""
    lines = raw_text.splitlines()[:15]
    date_idx = next((i for i in range(2, min(len(lines), 6)) if _TIMESTAMP_RE.match(lines[i])), None)
    if date_idx is not None:
        subject = " ".join(l.strip() for l in lines[1:date_idx] if l.strip())
        return _REPLY_PREFIX_RE.sub("", subject), _TIMESTAMP_RE.match(lines[date_idx]).group(1)
    headers = {}
    for l in lines:
        m = _HEADER_RE.match(l)
        if m:
            headers.setdefault(m.group(1).lower(), m.group(2).strip())
    received = ""
    if headers.get("date"):
        parsed = pd.to_datetime(headers["date"], errors="coerce", utc=True)
        received = "" if pd.isna(parsed) else parsed.strftime("%Y-%m-%d")
    return _REPLY_PREFIX_RE.sub("", headers.get("subject", "")), received


def _achievements_text(achs, weights: dict) -> str:
    """Unique labels, heaviest first: 'All-American; ECNL MVP'."""
    labels = sorted(set(_as_list(achs)), key=lambda a: (-weights.get(a, 0), a))
    return "; ".join(labels)


def build_player_table(playersDF: pd.DataFrame, weights: dict) -> pd.DataFrame:
    """One coach-readable row per player, sorted by score (highest first)."""
    subj_date = playersDF["_raw_text"].apply(_subject_and_date)
    out = pd.DataFrame({
        "Player":           playersDF["player_name"].map(_blank),
        "Position Group":   playersDF["Primary Position"].map(lambda p: POSITION_GROUP.get(p, "")),
        "Primary Position": playersDF["Primary Position"].map(_blank),
        "Dominant Foot":    playersDF["Dominant Foot"].map(_blank),
        "Club":             playersDF["player_club"].map(_blank),
        "Score":            playersDF["strength_score"].astype(float).round(2),
        "Achievements":     playersDF["achievements"].map(lambda a: _achievements_text(a, weights)),
        "Email":            playersDF["player_email(s)"].map(lambda e: "; ".join(_as_list(e))),
        "Video":            playersDF["youtube_links"].map(lambda v: "; ".join(_as_list(v))),
        "Subject":          subj_date.map(lambda t: t[0]),
        "Received":         subj_date.map(lambda t: t[1]),
        "Promoted":         playersDF["promoted"].map(lambda p: "Yes" if p == 1 else "No"),
        "File":             playersDF["file_name"],
    })
    return out.sort_values(["Score", "Player"], ascending=[False, True], kind="stable").reset_index(drop=True)


def build_needs_review(players: pd.DataFrame, threshold: float, review_band: float) -> pd.DataFrame:
    """Rows where a person should look: missing basics, just under the threshold, or a
    promoted/borderline player whose position wasn't found."""
    low = round(threshold - review_band, 2)
    reasons = []
    for _, r in players.iterrows():
        why = [f"Missing {f.lower()}" for f in ("Player", "Email", "Club") if not r[f]]
        if not r["Primary Position"] and r["Score"] >= low:
            why.append("Position not found")
        if low <= r["Score"] < threshold:
            why.append(f"Borderline score ({low:g}-{threshold:g})")
        reasons.append("; ".join(why))
    out = players.assign(Reason=reasons)
    out = out[out["Reason"] != ""]
    return out[["Reason", *PLAYER_COLS, "Promoted", "File"]].reset_index(drop=True)


def build_score_breakdown(players: pd.DataFrame, playersDF: pd.DataFrame,
                          weights: dict, categories: dict) -> pd.DataFrame:
    """Player x achievement x weight; players with no achievements are left out."""
    by_file = playersDF.set_index("file_name")["achievements"]
    rows = []
    for _, r in players.iterrows():
        for ach in sorted(set(_as_list(by_file.get(r["File"]))), key=lambda a: (-weights.get(a, 0), a)):
            rows.append({
                "Player": r["Player"], "Position Group": r["Position Group"],
                "Club": r["Club"], "Score": r["Score"], "Promoted": r["Promoted"],
                "Achievement": ach, "Category": categories.get(ach, "individual").title(),
                "Weight": weights.get(ach, 0), "File": r["File"],
            })
    cols = ["Player", "Position Group", "Club", "Score", "Promoted",
            "Achievement", "Category", "Weight", "File"]
    return pd.DataFrame(rows, columns=cols)


def _format_sheet(ws, df: pd.DataFrame) -> None:
    header_fill = PatternFill("solid", fgColor="1F1F1F")
    for cell in ws[1]:
        cell.font = Font(bold=True, color="CFB991")      # Purdue old gold on black
        cell.fill = header_fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "B2"                               # header row + player name stay visible
    ws.auto_filter.ref = ws.dimensions
    for i, col in enumerate(df.columns, 1):
        ws.column_dimensions[get_column_letter(i)].width = _WIDTHS.get(col, 16)
        if ws.max_row < 2:
            continue
        if col in _WRAP_COLS:
            for cell in next(ws.iter_cols(min_col=i, max_col=i, min_row=2)):
                cell.alignment = Alignment(wrap_text=True, vertical="top")
        if col == "Video":
            for cell in next(ws.iter_cols(min_col=i, max_col=i, min_row=2)):
                if cell.value:
                    cell.hyperlink = str(cell.value).split("; ")[0]
                    cell.font = Font(color="0563C1", underline="single")


def write_report(playersDF: pd.DataFrame, out_path: Path, threshold: float,
                 weights: dict, categories: dict, review_band: float = 1.0) -> dict:
    """Write the workbook; return the tables so the email summary can reuse them."""
    players = build_player_table(playersDF, weights)
    promoted = players[players["Promoted"] == "Yes"][PLAYER_COLS]
    sheets = {
        "Promoted":        promoted,
        "All Players":     players[[*PLAYER_COLS, "Promoted"]],
        "Needs Review":    build_needs_review(players, threshold, review_band),
        "Score Breakdown": build_score_breakdown(players, playersDF, weights, categories),
    }
    with pd.ExcelWriter(out_path, engine="openpyxl") as xw:
        for name, df in sheets.items():
            df.to_excel(xw, sheet_name=name, index=False)
            _format_sheet(xw.sheets[name], df)
    return sheets


def write_summary_html(sheets: dict, out_path: Path, threshold: float) -> None:
    """Email body that works without opening the attachment."""
    promoted = sheets["Promoted"]
    n_total = len(sheets["All Players"])
    n_review = len(sheets["Needs Review"])
    esc = lambda v: html.escape(_blank(v))

    rows = "".join(
        "<tr>" + "".join(f"<td style='padding:4px 8px;border-bottom:1px solid #ddd'>{esc(r[c])}</td>"
                         for c in ("Player", "Primary Position", "Dominant Foot", "Club", "Score"))
        + f"<td style='padding:4px 8px;border-bottom:1px solid #ddd'>{esc('; '.join(r['Achievements'].split('; ')[:3]))}</td></tr>"
        for _, r in promoted.iterrows()
    )
    head = "".join(f"<th style='text-align:left;padding:4px 8px;border-bottom:2px solid #333'>{h}</th>"
                   for h in ("Player", "Position", "Foot", "Club", "Score", "Top honors"))
    table = (f"<table style='border-collapse:collapse;font-family:Arial,sans-serif;font-size:13px'>"
             f"<tr>{head}</tr>{rows}</table>") if len(promoted) else "<p>No players promoted this run.</p>"

    out_path.write_text(
        "<div style='font-family:Arial,sans-serif;font-size:14px'>"
        "<!--ERRORS-->"
        f"<p>{n_total} new emails &middot; <b>{len(promoted)} promoted</b> (score &ge; {threshold:g}) "
        f"&middot; {n_review} need review</p>"
        f"{table}"
        "<p style='color:#555'>Full details in the attached Recruiting Report: filter by Position Group, "
        "Primary Position or Dominant Foot. Blank means the email didn't say.</p></div>",
        encoding="utf-8",
    )
