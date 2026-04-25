"""
testing_main.py
Purdue Women's Soccer – Email Recruiting Parser
Standalone Python equivalent of testing_main.ipynb
"""

# ──────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────────────────────────────

import re
import os
import email as _email_lib
import csv
import math
import shutil
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ──────────────────────────────────────────────────────────────────────────────
# DEFINE REGEX INDICATORS
# ──────────────────────────────────────────────────────────────────────────────

BULLET_LINE_RE = re.compile(r"(?m)^\s*(?:[-•*]|\d+[.)])\s+(.+?)\s*$")
HEADER_LINE_RE = re.compile(r"(?i)^\s*(to|cc|bcc)\s*:\s*(.+)$")
SECTION_HEADERS_RE = re.compile(
    r"(?im)^\s*(here are|highlights|accomplishments|achievements|honors|awards|resume|profile)\b.*$"
)

def _normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

# Email Indicators
EMAIL_RE = re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", re.I)

# YouTube link extractor — catches youtube.com and youtu.be URLs with or without protocol
YOUTUBE_RE = re.compile(
    r"(?:https?://)?(?:www\.)?(?:"
    r"youtube\.com/(?:watch|playlist)[^\s<>\"'\)\]]*"   # query-string URLs (?v= or ?list=)
    r"|youtube\.com/(?:shorts|embed|channel|@\w+)/[^\s<>\"'\)\]]+"  # path-based URLs
    r"|youtu\.be/[^\s<>\"'\)\]]+"                       # short URL (youtu.be/ID)
    r")",
    re.I,
)
COACH_EMAIL_BLACKLIST = {
    "robward@purdue.edu",
    "esmaster@purdue.edu",
    "rmoode@purdue.edu",
}
COACH_DOMAIN_BLACKLIST = {
    "purdue.edu",
}
# System / no-reply addresses that should never be returned as a player email
SYSTEM_EMAIL_RE = re.compile(
    r"^(?:no[-.]?reply|noreply|bounce|mailer[-.]?daemon|postmaster|"
    r"info|admin|support|webmaster|notifications?|alerts?|do[-.]?not[-.]?reply)"
    r"@",
    re.I,
)
# Normalized (lowercase) coach names — never returned as a player name
COACH_NAME_BLACKLIST = {
    "rob ward",
    "eric masters",
    "eric sergent masters",
    "eric s masters",
    "r moode",
    "coach rob ward",
    "coach eric masters",
    "coach eric sergent masters",
}
PLAYER_EMAIL_CUE_RE = re.compile(
    r"(?i)\b(my\s+email|email\s*[:\-]|reach\s+me|contact\s+me|best\s+email|player\s+email)\b"
)

# Name Indicators
NAME_TRIGGER_RES = [
    re.compile(r"(?i)\bmy\s+name\s+is\s+(.+)$"),
    re.compile(r"(?i)\bname\s*[:\-]\s*(.+)$"),
    re.compile(r"(?i)\bplayer\s*name\s*[:\-]\s*(.+)$"),
    re.compile(r"(?i)\bplayer\s*[:\-]\s*(.+)$"),
    re.compile(r"(?i)\bi\s+am\s+(.+)$"),
    re.compile(r"(?i)\bi['']?m\s+(.+)$"),
    re.compile(r"(?i)\bthis\s+is\s+(.+)$"),
    re.compile(r"(?i)\bfrom\s*[:\-]\s*(.+)$"),
]
SIGNOFF_RE = re.compile(
    r"(?im)^\s*(best|regards|kind regards|sincerely|thank you|thanks|respectfully|cheers)\s*[,:\-–—]*\s*(.*)\s*$"
)
# Parses the display name from a Gmail/email From: header.
# Matches both quoted  → From: "Jane Smith" <jane@gmail.com>
# and unquoted         → From: Jane Smith <jane@gmail.com>
# Captures only the first From: line (the sender's own header, not forwarded ones)
FROM_DISPLAY_RE = re.compile(
    r"(?im)^From:\s+"
    r"(?:\"(?P<quoted>[^\"]+)\"|(?P<plain>[^<\n@][^<\n]*?))\s*<[^>@\n]+@[^>\n]+>",
)
COMMA_SIGNATURE_SAME_LINE_RE = re.compile(
    r"(?im)^\s*(?:looking forward.*?|thank you.*?|thanks.*?|best of luck.*?|respectfully.*?|sincerely.*?|regards.*?|best.*?),\s*([A-Za-z][A-Za-z''-]*(?:\s+[A-Za-z][A-Za-z''-]*){1,3})\s*$"
)
COMMA_SIGNATURE_LINE_ONLY_RE = re.compile(
    r"(?im)^\s*(?:looking forward.*?|thank you.*?|thanks.*?|best of luck.*?|respectfully.*?|sincerely.*?|regards.*?|best.*?)\s*,\s*$"
)

# ──────────────────────────────────────────────────────────────────────────────
# ACHIEVEMENT KEYWORD LOADER
# ──────────────────────────────────────────────────────────────────────────────
_DEFAULT_KEYWORDS_FILE = "achievement_keywords.xlsx"


def load_achievement_keywords(path: str | Path = _DEFAULT_KEYWORDS_FILE,
                              ) -> tuple[dict[str, list[str]], dict[str, int], dict[str, str]]:
    """Load achievement labels, weights, categories, and regex patterns from Excel.

    Expected columns:
        A  achievement_label   — display name (e.g. "ECNL MVP")
        B  weight              — integer weight used in scoring
        C  category            — "individual" or "team"
        D  pattern             — raw regex string (one per row; multiple rows per label)

    Rows that share the same label are grouped together.  Blank rows and rows
    whose label cell is empty are skipped.  Weight and category are taken from
    the first row of each label group; subsequent rows may leave them blank.

    Returns (ACHIEVEMENT_PATTERNS, ACH_WEIGHTS, ACH_CATEGORIES).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Achievement keywords file not found: {path.resolve()}\n"
            "Either provide the file or pass --keywords <path> on the CLI."
        )

    df = pd.read_excel(path, dtype=str).fillna("")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    required = {"achievement_label", "weight", "pattern"}
    if not required.issubset(set(df.columns)):
        raise ValueError(
            f"Keywords Excel must have columns {required}. Found: {set(df.columns)}"
        )

    has_category = "category" in df.columns

    patterns: dict[str, list[str]] = {}
    weights: dict[str, int] = {}
    categories: dict[str, str] = {}

    current_label = ""
    current_weight = 1
    current_cat = "individual"

    for _, row in df.iterrows():
        label = row["achievement_label"].strip()
        w_str = row["weight"].strip()
        pat   = row["pattern"].strip()
        cat   = row["category"].strip().lower() if has_category else ""

        # A non-empty label cell starts a new group
        if label:
            current_label = label
            current_weight = int(w_str) if w_str else current_weight
            current_cat = cat if cat in ("individual", "team") else "individual"
            weights.setdefault(current_label, current_weight)
            categories.setdefault(current_label, current_cat)
            patterns.setdefault(current_label, [])

        if not current_label or not pat:
            continue

        # Validate the regex compiles before accepting it
        try:
            re.compile(pat, re.I)
        except re.error as e:
            raise ValueError(
                f"Invalid regex for '{current_label}': {pat!r}\n  → {e}"
            )

        patterns[current_label].append(pat)

    # Ensure every label has at least one pattern and a weight
    empty_labels = [l for l, p in patterns.items() if not p]
    if empty_labels:
        raise ValueError(f"Labels with no patterns: {empty_labels}")

    missing_w = set(patterns.keys()) - set(weights.keys())
    if missing_w:
        raise ValueError(f"Labels with no weight: {missing_w}")

    return patterns, weights, categories



NEGATIVE_PATTERNS = [
    r"\bseason[-\s]?ending\b",
    r"\bout\s+for\s+the\s+season\b",
    r"\binjury\b",
    r"\bbroken\s+(?:leg|arm|ankle|foot|wrist)\b",
    r"\bconcussion\b",
    r"\bsuspended\b",
    r"\bdisqualified\b",
    r"\bineligible\b",
    r"\bacademic\s+ineligible\b",
    r"\bdisciplinary\b",
    r"\becnl[-\s]*rl\b",              # ECNL RL / ECNL-RL / ECNLRL
    r"\becnl\b.*\bregional\s+league\b",  # ECNL Regional League (long-form name)
]

KILL_RE = re.compile("|".join(f"(?:{p})" for p in NEGATIVE_PATTERNS), re.I)

# Dedicated ECNL-RL kill — checked at player level (whole-text) in extract_achievements
ECNL_RL_KILL_RE = re.compile(
    r"\becnl[-\s]*rl\b"               # ECNL RL / ECNL-RL / ECNLRL
    r"|\becnl\b.*\bregional\s+league\b",  # ECNL Regional League
    re.I,
)
# Exception: if player was promoted FROM ECNL-RL → ECNL, they are NOT disqualified
ECNL_RL_PROMOTED_RE = re.compile(
    r"\bpromoted\b.{0,40}\becnl[-\s]*rl\b"
    r"|\becnl[-\s]*rl\b.{0,40}\bpromoted\b"
    r"|\bmoved\s+up\b.{0,40}\becnl[-\s]*rl\b"
    r"|\becnl[-\s]*rl\b.{0,40}\bmoved\s+up\b"
    r"|\bfrom\s+ecnl[-\s]*rl\b"
    r"|\becnl[-\s]*rl\b.{0,40}\bto\s+ecnl\b",
    re.I,
)


def neg_trigger(text: str) -> str | None:
    if not isinstance(text, str) or not text.strip():
        return None
    m = KILL_RE.search(text)
    return m.group(0) if m else None


# ──────────────────────────────────────────────────────────────────────────────
# CLUB / NAME FINDING
# ──────────────────────────────────────────────────────────────────────────────
_non_alnum = re.compile(r"[^a-z0-9]+")
_multi_space = re.compile(r"\s+")


def normalize(s: str) -> str:
    s = s.lower()
    s = _non_alnum.sub(" ", s)
    s = _multi_space.sub(" ", s).strip()
    return s


def _strip_noise(s: str) -> str:
    s = s.strip()
    s = re.split(r"[.!?,;:\)\]\}<>|/\\]", s, maxsplit=1)[0].strip()
    return s


_name_token = r"(?:[A-Z][a-z]+|[A-Z]{2,}|[A-Z]\.)"
_name_join = r"(?:[-'][A-Za-z]+)?"
NAME_CANDIDATE_RE = re.compile(
    rf"^\s*({_name_token}{_name_join})(?:\s+({_name_token}{_name_join}|\b[A-Z]\.\b))*\s*$"
)


def _clean_name_candidate(s: str) -> str:
    s = _strip_noise(s)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r"^(player|athlete|name|student)\s*[-:]\s*", "", s, flags=re.I).strip()
    return s


def _pick_best_name(line: str) -> str:
    line = _clean_name_candidate(line)
    if not line:
        return ""

    bad_starts = ("thank", "best", "regards", "sincerely", "respectfully", "cheers",
                  "hello", "hi", "dear", "schedule", "phone", "email", "instagram",
                  "coach")   # skip "Coach <Name>" lines — coach names handled by blacklist
    if line.lower().startswith(bad_starts):
        return ""

    tokens = line.split()
    if len(tokens) < 2:
        return ""

    kept = []
    for t in tokens[:6]:
        if re.fullmatch(r"[A-Z]\.", t):
            kept.append(t)
        elif re.fullmatch(r"[A-Z]{2,}([-'][A-Z]{2,})?", t):
            kept.append(t)
        elif re.fullmatch(r"[A-Z][a-z]+([-'][A-Za-z]+)?", t):
            kept.append(t)
        else:
            break

    if len(kept) < 2:
        return ""

    kept = kept[:4]
    name = " ".join(kept)

    if name.isupper():
        name = " ".join([w if w.endswith(".") else w.title() for w in kept])

    # Reject if the extracted name matches or is the leading portion of a known coach name
    # (handles cases where the fallback regex only captures first 2 tokens of a 3-token name)
    name_lc = name.lower()
    if any(name_lc == entry or entry.startswith(name_lc + " ")
           for entry in COACH_NAME_BLACKLIST):
        return ""

    return name


def build_state_pattern():
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    ]
    return re.compile(r"\b(" + "|".join(states) + r")\b", re.I)


STATE_RE = build_state_pattern()


def get_clubs(clubs_xlsx: str) -> pd.DataFrame:
    df = pd.read_excel(clubs_xlsx)
    df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(" ", "_")
    df = df.dropna(subset=["club_name"]).copy()
    df["club_name"] = df["club_name"].astype(str).str.strip()

    base = df["club_name"].str.split("-").str[0].str.strip()
    base = base.str.replace(r"[()]", "", regex=True)
    base = base.str.replace(",", "", regex=False)
    base = base.str.replace(STATE_RE, "", regex=True)
    df["club_names_normal"] = base.map(normalize)

    df["club_name_norm_full"] = df["club_name"].map(normalize)
    return df


@dataclass(frozen=True)
class ClubMatcher:
    alias_to_club: dict
    big_re: re.Pattern


def build_club_matcher(clubs_df: pd.DataFrame) -> ClubMatcher:
    alias_to_club = {}

    for club_name, a1, a2 in clubs_df[["club_name", "club_names_normal", "club_name_norm_full"]].itertuples(index=False, name=None):
        club_name = str(club_name).strip()
        for a in (a1, a2):
            a = str(a).strip()
            if not a:
                continue
            alias_to_club.setdefault(a, club_name)

    aliases = sorted(alias_to_club.keys(), key=len, reverse=True)
    pat = r"(?:^| )(" + "|".join(re.escape(a) for a in aliases) + r")(?: |$)"
    big_re = re.compile(pat)

    return ClubMatcher(alias_to_club=alias_to_club, big_re=big_re)


def find_club_from_text(text: str, matcher: ClubMatcher) -> str | None:
    t = f" {normalize(text)} "
    m = matcher.big_re.search(t)
    if not m:
        return None
    alias = m.group(1)
    return matcher.alias_to_club.get(alias)


def _parse_from_header(text: str) -> str:
    """
    Extract and validate the display name from the first From: header line.
    Returns a clean name string or "" if none found / fails validation.

    Handles Gmail metadata formats:
        From: Jane Smith <jane@gmail.com>
        From: "Jane Smith" <jane@gmail.com>
    """
    m = FROM_DISPLAY_RE.search(text)
    if not m:
        return ""
    raw = (m.group("quoted") or m.group("plain") or "").strip()
    if not raw:
        return ""
    return _pick_best_name(raw)   # runs token validation + coach blacklist


def find_name_from_text(text: str) -> str:
    lines = text.splitlines()

    m = COMMA_SIGNATURE_SAME_LINE_RE.search(text)
    if m:
        cand = _pick_best_name(m.group(1))
        if cand:
            return cand

    for line in lines[:80]:
        l = line.strip()
        if not l:
            continue
        for rx in NAME_TRIGGER_RES:
            m = rx.search(l)
            if not m:
                continue
            cand = _pick_best_name(m.group(1))
            if cand:
                return cand

    cutoff = len(lines)
    for i, line in enumerate(lines):
        if re.search(r"(?i)^\s*(from:|sent:|to:|subject:)\s", line):
            cutoff = min(cutoff, i)
        if re.search(r"(?i)^\s*on .+ wrote:\s*$", line):
            cutoff = min(cutoff, i)
    scan = lines[:cutoff]

    for idx in range(len(scan) - 1, -1, -1):
        line = scan[idx]

        if COMMA_SIGNATURE_LINE_ONLY_RE.match(line):
            for j in range(idx + 1, min(idx + 5, len(scan))):
                nxt = scan[j].strip()
                if not nxt:
                    continue
                cand = _pick_best_name(nxt)
                if cand:
                    return cand
                break

        m = SIGNOFF_RE.match(line)
        if not m:
            continue
        tail = (m.group(2) or "").strip()
        cand = _pick_best_name(tail)
        if cand:
            return cand
        for j in range(idx + 1, min(idx + 4, len(scan))):
            nxt = scan[j].strip()
            if not nxt:
                continue
            cand = _pick_best_name(nxt)
            if cand:
                return cand
            break

    window = " \n".join(lines[:40])
    m = re.search(r"(?m)\b([A-Z][a-z]+(?:[-'][A-Za-z]+)?\s+[A-Z][a-z]+(?:[-'][A-Za-z]+)?)\b", window)
    if m:
        cand = _pick_best_name(m.group(1))
        if cand:
            return cand

    # Last resort: display name from the Gmail From: header
    # Reliable when the email was imported directly from Gmail metadata
    cand = _parse_from_header(text)
    if cand:
        return cand

    return ""


# Signature / forwarded-content boundary — YouTube links below this are likely
# coach, club, or program links rather than the player's own highlight reel
_SIG_BOUNDARY_RE = re.compile(
    r"(?im)^(?:\s*-{2,}\s*$"                      # -- separator
    r"|\s*_{3,}\s*$"                               # ___ separator
    r"|\s*={3,}\s*$"                               # === separator
    r"|.*Sent\s+from\s+my\s+"                      # mobile signature
    r"|.*------\s*Forwarded\s+message\s*------"     # Gmail forward
    r"|.*Begin\s+forwarded\s+message"               # Apple forward
    r"|.*On\s+.{10,60}\s+wrote:\s*$"               # reply header
    r")"
)


def _dedup_youtube(matches: list[str]) -> list[str]:
    """Deduplicate and strip trailing punctuation from YouTube URL matches."""
    cleaned, seen = [], set()
    for url in matches:
        url = url.rstrip(".,;:!?)")
        url_lc = url.lower()
        if url_lc not in seen:
            seen.add(url_lc)
            cleaned.append(url)
    return cleaned


def extract_youtube_links(text: str) -> list[str] | None:
    """Return a deduplicated list of YouTube URLs found in the email.

    First tries the player body (before signature/forwarded boundaries).
    If nothing is found there, falls back to the full text so that links
    placed after a separator (e.g. "-- \\nhighlight reel: …") are still
    captured.
    """
    # Try body before signature first
    sig_match = _SIG_BOUNDARY_RE.search(text)
    body = text[:sig_match.start()] if sig_match else text

    cleaned = _dedup_youtube(YOUTUBE_RE.findall(body))
    if cleaned:
        return cleaned

    # Fallback: search the full text (catches links after sig boundaries)
    cleaned = _dedup_youtube(YOUTUBE_RE.findall(text))
    return cleaned if cleaned else None


def extract_player_emails(text: str) -> list[str] | None:
    text_lc = text.lower()

    header_recipients = set()
    for line in text.splitlines()[:80]:
        m = HEADER_LINE_RE.match(line)
        if m:
            header_recipients.update(e.lower() for e in EMAIL_RE.findall(m.group(2)))

    emails = [(m.group(0).lower(), m.start()) for m in EMAIL_RE.finditer(text_lc)]
    if not emails:
        return None

    scored = []
    cue_positions = [m.start() for m in PLAYER_EMAIL_CUE_RE.finditer(text_lc)]

    for e, pos in emails:
        domain = e.split("@", 1)[1]

        if e in COACH_EMAIL_BLACKLIST:
            continue
        if domain in COACH_DOMAIN_BLACKLIST:
            continue
        if SYSTEM_EMAIL_RE.match(e):
            continue
        if e in header_recipients:
            continue

        prox = 10 ** 9
        for cp in cue_positions:
            d = abs(pos - cp)
            if d < prox:
                prox = d

        scored.append((prox, pos, e))

    if not scored:
        return None

    scored.sort()
    best_prox = scored[0][0]
    if best_prox < 10 ** 9:
        kept = [e for prox, _, e in scored if prox <= 600]
    else:
        kept = [e for _, _, e in scored]

    seen = set()
    out = []
    for e in kept:
        if e not in seen:
            seen.add(e)
            out.append(e)
    return out if out else None


# ──────────────────────────────────────────────────────────────────────────────
# ACHIEVEMENT FINDING
# ──────────────────────────────────────────────────────────────────────────────
# NOTE: ACH_RE is compiled further below, after ACHIEVEMENT_PATTERNS is loaded.

def extract_achievements(text: str) -> tuple[list[str], list[str]]:
    """Returns (labels, evidence_lines)."""
    # Hard kill: any ECNL-RL mention in the email disqualifies the player —
    # UNLESS context indicates promotion FROM ECNL-RL (a strong positive signal)
    if ECNL_RL_KILL_RE.search(text) and not ECNL_RL_PROMOTED_RE.search(text):
        return [], []

    block = extract_achievement_blocks(text)
    haystacks = [text, block] if block else [text]

    found = set()
    evidence = []

    candidate_lines = []
    if block:
        candidate_lines.extend([ln.strip() for ln in block.splitlines() if ln.strip()])
    else:
        candidate_lines.extend([ln.strip() for ln in text.splitlines()[:120] if ln.strip()])

    for label, regs in ACH_RE.items():
        hit = False
        for hs in haystacks:
            for r in regs:
                if r.search(hs):
                    hit = True
                    break
            if hit:
                found.add(label)
                break

    if found:
        for ln in candidate_lines:
            ln_norm = _normalize_ws(ln)
            for label in found:
                if any(r.search(ln_norm) for r in ACH_RE[label]):
                    evidence.append(ln_norm)
                    break

    # ── Deduplication ────────────────────────────────────────────────────────
    # Rule 0: USWNT (senior) subsumes all youth / ID national team labels
    if "USWNT" in found:
        found.discard("US Youth Soccer Team")
        found.discard("USYNT ID Center")
        found.discard("National Team Camp")
        found.discard("Talent ID")

    # Rule 1: specific ECNL All-Conference tier subsumed the generic;
    #         also discard catch-all "All-Conference" whenever any league-specific fires
    ECNL_AC_SPECIFIC = {
        "ECNL All-Conference First Team",
        "ECNL All-Conference Second Team",
        "ECNL All-Conference Third Team",
    }
    ANY_AC_SPECIFIC = ECNL_AC_SPECIFIC | {
        "ECNL All-Conference",
        "GA All-Conference",
    }
    if found & ECNL_AC_SPECIFIC:
        found.discard("ECNL All-Conference")
        found.discard("First Team")   # avoids +2 double-count with specific tier
    if found & ANY_AC_SPECIFIC:
        found.discard("All-Conference")   # generic subsumed by any league-specific

    # Rule 2: national champion → implies finalist and national playoffs
    if "ECNL National Champion" in found:
        found.discard("ECNL National Finalist")
        found.discard("ECNL National Playoffs")
    elif "ECNL National Finalist" in found:
        found.discard("ECNL National Playoffs")

    if "GA National Champion" in found:
        found.discard("GA National Finalist")
        found.discard("GA National Playoffs")
    elif "GA National Finalist" in found:
        found.discard("GA National Playoffs")

    # Rule 3: conference champion → implies conference finalist at same level
    if "ECNL Conference Champion" in found:
        found.discard("ECNL Conference Finalist")
    if "GA Conference Champion" in found:
        found.discard("GA Conference Finalist")

    # Rule 4: Showcase XI → implies Showcase Invitee (XI is a subset of invitees)
    if "ECNL Showcase XI" in found:
        found.discard("ECNL Showcase Invitee")
        found.discard("ECNL All-Star")   # Showcase XI is more specific

    # Rule 4b: any ECNL showcase label → discard generic Showcase
    ECNL_SHOWCASE = {"ECNL Showcase XI", "ECNL Showcase Invitee"}
    if found & ECNL_SHOWCASE:
        found.discard("Showcase")

    # Rule 5: NPL champion → implies NPL finalist
    if "NPL National Champion" in found:
        found.discard("NPL National Finalist")

    # Rule 6: national team membership subsumes talent ID / ID center labels
    if "US Youth Soccer Team" in found:
        found.discard("USYNT ID Center")
        found.discard("National Team Camp")
        found.discard("Talent ID")
    elif "National Team Camp" in found:
        found.discard("USYNT ID Center")
        found.discard("Talent ID")
    elif "USYNT ID Center" in found:
        found.discard("Talent ID")

    # Rule 7: ECNL MVP subsumes generic MVP and generic Player of the Year
    if "ECNL MVP" in found:
        found.discard("MVP")
        found.discard("Player of the Year")

    # Rule 8: ECNL Position Award subsumes generic Position Award and MVP
    if "ECNL Position Award" in found:
        found.discard("Position Award")
        found.discard("MVP")   # position-specific is more precise

    # Rule 9: ECNL All-Star subsumes generic All-Star and GA All-Star
    if "ECNL All-Star" in found:
        found.discard("All-Star")
        found.discard("GA All-Star")
    elif "GA All-Star" in found:
        found.discard("All-Star")

    # Rule 10: ECNL All-Tournament subsumes generic All-Tournament
    if "ECNL All-Tournament" in found:
        found.discard("All-Tournament")

    labels = sorted(found)
    seen = set()
    ev_out = []
    for e in evidence:
        if e not in seen:
            seen.add(e)
            ev_out.append(e)
    return labels, ev_out


def extract_achievement_blocks(text: str) -> str:
    """Returns a smaller text containing likely achievement content."""
    lines = text.splitlines()

    bullets = [m.group(1) for m in BULLET_LINE_RE.finditer(text)]
    bullets_block = "\n".join(bullets)

    section_lines = []
    header_idxs = [i for i, ln in enumerate(lines) if SECTION_HEADERS_RE.match(ln)]
    for hi in header_idxs:
        for j in range(hi, min(hi + 25, len(lines))):
            ln = lines[j]
            if re.search(r"(?i)^\s*(from:|sent:|to:|subject:)\s", ln):
                break
            section_lines.append(ln)

    section_block = "\n".join(section_lines)
    return "\n".join([bullets_block, section_block]).strip()

# ──────────────────────────────────────────────────────────────────────────────
# KEYWORD FINDING
# ──────────────────────────────────────────────────────────────────────────────
WORD_RE = re.compile(r"[a-z0-9]+")

def _tokens(s: str) -> set[str]:
    return set(WORD_RE.findall(s.lower()))

def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def build_label_token_bank(achievement_patterns: dict) -> dict[str, set[str]]:
    return {label: _tokens(label) for label in achievement_patterns.keys()}


# NOTE: LABEL_TOKENS is built below, after ACHIEVEMENT_PATTERNS is loaded.

ACH_ADJACENT_RE = re.compile(
    r"(?i)\b("
    r"selected|named|earned|received|awarded|recognized|honored|invited|chosen|"
    r"all[-\s]?conference|all[-\s]?state|all[-\s]?region|all[-\s]?american|"
    r"player\s+of|goalkeeper\s+of|defender\s+of|"
    r"showcase|national|regional|"
    r"first\s+team|second\s+team|third\s+team|1st\s+team|2nd\s+team|3rd\s+team|"
    r"top\s+\d+|ranked|mvp|most\s+valuable|"
    r"honor|award|recognition|distinction|achievement"
    r")\b"
)

EMAIL_HEADER_RE = re.compile(r"(?i)^\s*(from:|to:|cc:|bcc:|sent:|subject:|date:|on .+ wrote:)\s*")


def line_matches_any_achievement(line: str) -> bool:
    ln = line.strip()
    if not ln:
        return False
    for regs in ACH_RE.values():
        if any(r.search(ln) for r in regs):
            return True
    return False


def best_label_match(line: str) -> tuple[str, float]:
    lt = _tokens(line)
    best_label = ""
    best_score = 0.0
    for label, tset in LABEL_TOKENS.items():
        s = _jaccard(lt, tset)
        if s > best_score:
            best_score = s
            best_label = label
    return best_label, best_score


def export_new_keyword_candidates(playersDF: pd.DataFrame, out_csv="keyword_candidates.csv", threshold=0.20):
    rows = []

    for _, row in playersDF.iterrows():
        file   = row.get("file", "")
        player = row.get("player_name", "")
        text   = row.get("_raw_text", "")

        if not isinstance(text, str) or not text.strip():
            continue

        block       = extract_achievement_blocks(text)
        block_lines = {ln.strip() for ln in block.splitlines() if ln.strip()}

        prose_lines = set()
        for ln in text.splitlines():
            ln = ln.strip()
            if not ln or len(ln) < 20:
                continue
            if EMAIL_HEADER_RE.match(ln):
                continue
            if ACH_ADJACENT_RE.search(ln):
                prose_lines.add(ln)

        candidate_lines = block_lines | prose_lines

        for ln in candidate_lines:
            if line_matches_any_achievement(ln):
                continue

            label, score = best_label_match(ln)

            if ln in prose_lines or score >= threshold:
                rows.append({
                    "file":                   file,
                    "player_name":            player,
                    "candidate_line":         ln,
                    "closest_existing_label": label,
                    "similarity":             round(score, 3),
                    "source":                 "prose" if ln in prose_lines else "block",
                })

    seen    = set()
    deduped = []
    for r in rows:
        key = (r["candidate_line"].lower(), r["closest_existing_label"])
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    deduped.sort(key=lambda r: (r["source"] != "block", -r["similarity"]))

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "player_name", "candidate_line",
                                          "closest_existing_label", "similarity", "source"])
        w.writeheader()
        w.writerows(deduped)

    return pd.DataFrame(deduped)


# ──────────────────────────────────────────────────────────────────────────────
# SCORING
# ──────────────────────────────────────────────────────────────────────────────
PROMOTION_THRESHOLD = 5.0  # default strength score (blended ind/team scale)

# ──────────────────────────────────────────────────────────────────────────────
# LOAD ACHIEVEMENT DATA — requires achievement_keywords.xlsx
# ──────────────────────────────────────────────────────────────────────────────
def _init_achievements(keywords_path: str | Path | None = None,
                       ) -> tuple[dict[str, list[str]], dict[str, int], dict[str, str]]:
    """Return (ACHIEVEMENT_PATTERNS, ACH_WEIGHTS, ACH_CATEGORIES) loaded from Excel.

    The Excel file is required. If it does not exist the pipeline will raise
    FileNotFoundError immediately so the problem is obvious.
    """
    path = Path(keywords_path) if keywords_path else Path(_DEFAULT_KEYWORDS_FILE)

    if not path.exists():
        raise FileNotFoundError(
            f"Achievement keywords Excel not found: {path.resolve()}\n"
            "This file is required for the pipeline to run. "
            "Place achievement_keywords.xlsx in the project directory."
        )

    pats, wts, cats = load_achievement_keywords(path)
    n_ind = sum(1 for c in cats.values() if c == "individual")
    n_team = sum(1 for c in cats.values() if c == "team")
    print(f"[info] Loaded {len(pats)} achievement labels from {path} "
          f"({n_ind} individual, {n_team} team)")
    return pats, wts, cats


# Module-level init (overridden at CLI time via main())
ACHIEVEMENT_PATTERNS, ACH_WEIGHTS, ACH_CATEGORIES = _init_achievements()

# Compile regex and token bank from the loaded patterns
ACH_RE = {label: [re.compile(p, re.I) for p in pats]
          for label, pats in ACHIEVEMENT_PATTERNS.items()}
LABEL_TOKENS = build_label_token_bank(ACHIEVEMENT_PATTERNS)

# ── Validate weight coverage ──────────────────────────────────────────────────
_missing_weights = set(ACHIEVEMENT_PATTERNS.keys()) - set(ACH_WEIGHTS.keys())
if _missing_weights:
    raise RuntimeError(
        f"ACHIEVEMENT_PATTERNS has labels with no ACH_WEIGHTS entry: {_missing_weights}. "
        "Add a weight for each new pattern to prevent silent scoring errors."
    )


def achievement_score(ach_list) -> float:
    """Sum of raw weights for all matched achievement labels."""
    if not isinstance(ach_list, list) or len(ach_list) == 0:
        return 0.0
    return float(sum(ACH_WEIGHTS[label] for label in set(ach_list)))


# ── Individual vs Team scoring ────────────────────────────────────────────────
# Individual achievements (All-American, MVP, ODP, …) reflect a player's own
# merit.  Team achievements (tournament attendance, showcase participation, …)
# are contextual — they show environment, not ability.
#
# Scoring:
#   individual_raw = Σ weights of individual-category labels
#   team_raw       = Σ weights of team-category labels
#   ind_score  = 10 × (1 − e^(−individual_raw / 7))    ← steep curve
#   team_score = 10 × (1 − e^(−team_raw / 10))        ← softer curve
#   strength   = 0.7 × ind_score + 0.3 × team_score
#
# At threshold 5.0:
#   Player of the Year (ind=10)       → 5.32  ✓ promotes
#   ECNL National Champion (ind=9)    → 5.06  ✓ promotes
#   ODP alone (ind=7)                 → 4.42  ✗ needs team context
#   ECNL MVP + showcase (ind=7,t=2)  → 4.97  ✗ borderline
#   3 tournaments only (team=6)       → 1.35  ✗ never promotes
#   Heavy team stacking (team=15)     → 2.33  ✗ never promotes

_IND_N  = 7    # individual asymptote denominator
_TEAM_N = 10   # team asymptote denominator (softer)
_IND_W  = 0.7  # individual weight in final blend
_TEAM_W = 0.3  # team weight in final blend


def _split_ind_team(ach_list) -> tuple[float, float]:
    """Return (individual_raw, team_raw) weight sums from an achievement list."""
    if not isinstance(ach_list, list) or len(ach_list) == 0:
        return 0.0, 0.0
    ind = team = 0.0
    for label in set(ach_list):
        w = ACH_WEIGHTS.get(label, 0)
        cat = ACH_CATEGORIES.get(label, "individual")
        if cat == "team":
            team += w
        else:
            ind += w
    return ind, team


def _compute_scores(ach_list) -> tuple[float, float, float]:
    """Return (individual_score, team_score, strength_score) on 0-10 scales."""
    ind_raw, team_raw = _split_ind_team(ach_list)
    ind_score  = round(10 * (1 - math.exp(-ind_raw  / _IND_N)), 2)
    team_score = round(10 * (1 - math.exp(-team_raw / _TEAM_N)), 2)
    strength   = round(_IND_W * ind_score + _TEAM_W * team_score, 2)
    return ind_score, team_score, strength


# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT BUILDING
# ──────────────────────────────────────────────────────────────────────────────
def _read_file_as_text(path: Path) -> str:
    """Return the plain-text content of a .txt or .eml file."""
    if path.suffix.lower() != ".eml":
        return path.read_text(encoding="utf-8", errors="ignore")

    with open(path, "rb") as f:
        msg = _email_lib.message_from_bytes(f.read())

    parts: list[str] = []
    for header in ("From", "To", "Cc", "Subject", "Date"):
        val = msg.get(header, "")
        if val:
            parts.append(f"{header}: {val}")
    parts.append("")

    if msg.is_multipart():
        for part in msg.walk():
            if (part.get_content_type() == "text/plain"
                    and "attachment" not in str(part.get("Content-Disposition", ""))):
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    parts.append(payload.decode(charset, errors="ignore"))
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            parts.append(payload.decode(charset, errors="ignore"))

    return "\n".join(parts)


def parse_email_file(txt_path: Path, matcher: ClubMatcher) -> dict:
    text = _read_file_as_text(txt_path)
    name = find_name_from_text(text)
    club = find_club_from_text(text, matcher)
    emails = extract_player_emails(text)
    ach_labels, ach_evidence = extract_achievements(text)
    youtube = extract_youtube_links(text)
    return {
        "file_name":              txt_path.name,
        "_file_path":             str(txt_path.resolve()),
        "player_name":            name,
        "player_email(s)":        emails,
        "player_club":            club,
        "achievements":           ach_labels,
        "achievements_evidence":  ach_evidence,
        "youtube_links":          youtube,
        "_raw_text":              text,
    }


def build_player_ach(playersDF: pd.DataFrame, threshold: float = None) -> pd.DataFrame:
    if threshold is None:
        threshold = PROMOTION_THRESHOLD
    base_cols = ["file_name", "player_name", "achievements"]
    players_ach = playersDF[base_cols].copy()
    players_ach["achievements_score"] = players_ach["achievements"].apply(achievement_score)
    # Individual/team split scoring
    scores = players_ach["achievements"].apply(_compute_scores)
    players_ach["individual_score"] = scores.apply(lambda x: x[0])
    players_ach["team_score"]       = scores.apply(lambda x: x[1])
    players_ach["strength_score"]   = scores.apply(lambda x: x[2])
    players_ach["promoted"]         = (players_ach["strength_score"] >= threshold).astype(int)
    # Carry youtube_links through if present in playersDF
    if "youtube_links" in playersDF.columns:
        players_ach["youtube_links"] = playersDF["youtube_links"].values
    return players_ach


def build_missing_fields(playersDF: pd.DataFrame) -> pd.DataFrame:
    name_missing  = playersDF["player_name"].isna()    | playersDF["player_name"].astype(str).str.strip().eq("")
    email_missing = playersDF["player_email(s)"].isna() | playersDF["player_email(s)"].astype(str).str.strip().eq("")
    club_missing  = playersDF["player_club"].isna()    | playersDF["player_club"].astype(str).str.strip().eq("")
    return playersDF[name_missing | email_missing | club_missing].copy()

def build_missing_names(playersDF: pd.DataFrame) -> pd.DataFrame:
    name_missing  = playersDF["player_name"].isna()    | playersDF["player_name"].astype(str).str.strip().eq("")
    return playersDF[name_missing].copy()

def build_missing_emails(playersDF: pd.DataFrame) -> pd.DataFrame:
    email_missing = playersDF["player_email(s)"].isna() | playersDF["player_email(s)"].astype(str).str.strip().eq("")
    return playersDF[email_missing].copy()
    
def build_missing_clubs(playersDF: pd.DataFrame) -> pd.DataFrame:
    club_missing  = playersDF["player_club"].isna()    | playersDF["player_club"].astype(str).str.strip().eq("")
    return playersDF[club_missing].copy()

    
def export_achievements_flat(
    playersDF: pd.DataFrame,
    players_ach: pd.DataFrame,
    out_csv: str = "player_achievements.csv",
) -> pd.DataFrame:
    """
    Flat CSV: one row per player × achievement label.
    Players with no achievements get a single row with achievement = None.
    Each row includes the label's weight and category so you can see exactly
    what was picked up and how it contributed to the score.
    """
    import ast

    def _parse_list(val) -> list:
        if isinstance(val, list):
            return val
        try:
            result = ast.literal_eval(str(val))
            return result if isinstance(result, list) else []
        except Exception:
            return []

    rows = []
    for i, prow in playersDF.iterrows():
        score_row = players_ach.iloc[i] if i < len(players_ach) else {}
        achs = _parse_list(prow.get("achievements", []))
        base = {
            "file_name":        prow.get("file_name", ""),
            "player_name":      prow.get("player_name", ""),
            "player_email(s)":  prow.get("player_email(s)", ""),
            "player_club":      prow.get("player_club", ""),
            "individual_score": score_row.get("individual_score", 0),
            "team_score":       score_row.get("team_score", 0),
            "strength_score":   score_row.get("strength_score", 0),
            "promoted":         score_row.get("promoted", 0),
        }
        if achs:
            for ach in achs:
                rows.append({
                    **base,
                    "achievement_label": ach,
                    "weight":            ACH_WEIGHTS.get(ach, 0),
                    "category":          ACH_CATEGORIES.get(ach, "individual"),
                })
        else:
            rows.append({
                **base,
                "achievement_label": None,
                "weight":            0,
                "category":          None,
            })

    col_order = [
        "file_name", "player_name", "player_email(s)", "player_club",
        "achievement_label", "weight", "category",
        "individual_score", "team_score", "strength_score", "promoted",
    ]
    flat = pd.DataFrame(rows, columns=col_order)
    flat.to_csv(out_csv, index=False)
    return flat


# ──────────────────────────────────────────────────────────────────────────────
# EXPORT PROMOTED TEXTS
# ──────────────────────────────────────────────────────────────────────────────
def export_promoted_texts(
    promoted_df: pd.DataFrame,
    out_dir: str | Path = "promoted_texts",
    txt_col: str = "txt_path",
    name_col: str | None = "player_name",
    copy_files: bool = True,
) -> Path:
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if txt_col not in promoted_df.columns:
        raise KeyError(f"Missing column '{txt_col}' in promoted_df.")

    for i, row in promoted_df.reset_index(drop=True).iterrows():
        src = Path(row[txt_col])
        if not src.exists():
            continue

        stem = src.stem
        if name_col and name_col in promoted_df.columns:
            nm = str(row[name_col] or "").strip()
            if nm:
                nm = "".join(c for c in nm if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
                stem = f"{nm}__{stem}"

        dst = out_dir / f"{i:04d}__{stem}{src.suffix}"

        if copy_files:
            shutil.copy2(src, dst)
        else:
            shutil.move(src, dst)

    return out_dir


# ──────────────────────────────────────────────────────────────────────────────
# VISUALIZATIONS
# ──────────────────────────────────────────────────────────────────────────────
ACCENT   = "#2563EB"
ACCENT2  = "#16A34A"
BG       = "#F8FAFC"
GRID_CLR = "#E2E8F0"

plt.rcParams.update({
    "font.family":       "sans-serif",
    "axes.facecolor":    BG,
    "figure.facecolor":  BG,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        GRID_CLR,
    "grid.linewidth":    0.8,
})


def plot_strength_bar(players_ach: pd.DataFrame, out_path: str = "strength_scores.png"):
    df = (players_ach[["player_name", "strength_score"]]
          .dropna()
          .sort_values("strength_score", ascending=True)
          .tail(15))

    fig, ax = plt.subplots(figsize=(9, max(4, len(df) * 0.38)))
    fig.patch.set_facecolor(BG)

    bars = ax.barh(df["player_name"], df["strength_score"],
                   color=ACCENT, height=0.65, zorder=3)

    for bar, val in zip(bars, df["strength_score"]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", ha="left", fontsize=8.5, color="#374151")

    ax.set_xlim(0, 11)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.set_xlabel("Strength Score (out of 10)", fontsize=10, color="#374151")
    ax.set_title("Top Player Strength Score Rankings", fontsize=13, fontweight="bold",
                 color="#111827", pad=9)
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)
    ax.grid(axis="x", zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.show()

def plot_strength_histogram(players_ach: pd.DataFrame, out_path: str = "strength_histogram.png"):
    scores = players_ach["strength_score"].dropna()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BG)

    n_bins = min(20, max(5, len(scores) // 2))
    counts, edges, patches = ax.hist(scores, bins=n_bins,
                                     range=(0, 10),
                                     color=ACCENT2, edgecolor="white",
                                     linewidth=0.8, zorder=3)

    max_c = max(counts) if max(counts) > 0 else 1
    for patch, c in zip(patches, counts):
        patch.set_alpha(0.4 + 0.6 * (c / max_c))

    mean_val = scores.mean()
    ax.axvline(mean_val, color="#DC2626", linewidth=1.6, linestyle="--", zorder=4)
    ax.text(mean_val + 0.1, ax.get_ylim()[1] * 0.92,
            f"mean = {mean_val:.1f}", color="#DC2626", fontsize=9)

    ax.set_xlim(0, 10)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_xlabel("Strength Score (out of 10)", fontsize=10, color="#374151")
    ax.set_ylabel("Number of Players", fontsize=10, color="#374151")
    ax.set_title("Distribution of Player Strength Scores", fontsize=13,
                 fontweight="bold", color="#111827", pad=12)
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.show()


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
import argparse as _argparse

def main():
    parser = _argparse.ArgumentParser(
        description="Run the recruiting email pipeline on a single group folder."
    )
    parser.add_argument(
        "group",
        nargs="?",
        default=None,
        help=(
            'Subfolder name inside test_emails/ to evaluate (e.g. "Test 6", "group 1", "2026-04-14"). '
            "Omit to default to today's date folder (YYYY-MM-DD)."
        ),
    )
    parser.add_argument(
        "--clubs", default="clubs.xlsx",
        help="Path to clubs.xlsx (default: clubs.xlsx).",
    )
    parser.add_argument(
        "--threshold", type=float, default=PROMOTION_THRESHOLD,
        help=f"Promotion score threshold (default: {PROMOTION_THRESHOLD}).",
    )
    parser.add_argument(
        "--out-dir", default="results",
        help="Directory to write output CSVs into (default: results/).",
    )
    parser.add_argument(
        "--keywords", default=None,
        help=(
            f"Path to achievement keywords Excel (default: {_DEFAULT_KEYWORDS_FILE}). "
            "Overrides the hardcoded fallback patterns and weights."
        ),
    )
    parser.add_argument(
        "--no-charts", action="store_true",
        help="Skip generating chart images.",
    )
    args = parser.parse_args()

    # ── Reload achievement data if a custom keywords file was specified ────────
    global ACHIEVEMENT_PATTERNS, ACH_WEIGHTS, ACH_RE, LABEL_TOKENS
    if args.keywords is not None:
        ACHIEVEMENT_PATTERNS, ACH_WEIGHTS = _init_achievements(args.keywords)
        ACH_RE = {label: [re.compile(p, re.I) for p in pats]
                  for label, pats in ACHIEVEMENT_PATTERNS.items()}
        LABEL_TOKENS = build_label_token_bank(ACHIEVEMENT_PATTERNS)

    # ── Anchor working directory ──────────────────────────────────────────────
    cwd = Path.cwd()
    if not (cwd / "test_emails").exists():
        for candidate in cwd.parents:
            if (candidate / "test_emails").exists():
                os.chdir(candidate)
                print(f"[info] Changed cwd → {candidate}")
                break
        else:
            raise FileNotFoundError(
                f"Could not locate 'test_emails/' starting from {cwd}."
            )

    # ── Resolve paths ─────────────────────────────────────────────────────────
    # Default to today's date folder (YYYY-MM-DD) when no group is supplied.
    if args.group is None:
        group_label = date.today().strftime("%Y-%m-%d")
        print(f"[info] No group specified — defaulting to today's folder: {group_label}")
    else:
        group_label = args.group

    input_dir = Path("test_emails") / group_label if group_label else Path("test_emails")

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Group folder not found: {input_dir.resolve()}\n"
            f"  (Defaulted to today's date folder. Pass a folder name explicitly to override, "
            f"e.g. `python testing_main.py \"group 1\"`)"
        )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Date tag: D_Mon_Year (e.g. 2_Apr_2026) ─────────────────────────────────
    today = date.today()
    date_tag = today.strftime("%-d_%b_%Y")          # e.g. "2_Apr_2026"

    players_csv         = out_dir / f"Player_Data_{date_tag}.csv"
    promoted_csv        = out_dir / f"Promoted_Players_{date_tag}.csv"
    achievements_csv    = out_dir / f"Achievement_Details_{date_tag}.csv"
    keyword_csv         = out_dir / f"Keyword_Candidates_{date_tag}.csv"
    promoted_emails_dir = out_dir / "promoted_emails"

    threshold = args.threshold

    # ── Load clubs ────────────────────────────────────────────────────────────
    clubsDF = get_clubs(args.clubs)
    matcher = build_club_matcher(clubsDF)

    # ── Parse emails ──────────────────────────────────────────────────────────
    email_files = sorted(
        p for ext in ("*.txt", "*.eml") for p in input_dir.glob(ext)
    )
    if not email_files:
        print(f"[warning] No email files found in {input_dir.resolve()}")
        return

    rows      = [parse_email_file(p, matcher) for p in email_files]
    playersDF = pd.DataFrame(rows)
    _INTERNAL_COLS = {"_file_path", "_raw_text"}

    # ── Score players ─────────────────────────────────────────────────────────
    players_ach = build_player_ach(playersDF, threshold=threshold)

    # ── Build unified export columns ─────────────────────────────────────────
    playersDF["individual_score"] = players_ach["individual_score"].values
    playersDF["team_score"]       = players_ach["team_score"].values
    playersDF["strength_score"]   = players_ach["strength_score"].values
    playersDF["promoted"]         = players_ach["promoted"].values

    _EXPORT_COLS = [
        "file_name", "player_name", "player_email(s)", "player_club",
        "individual_score", "team_score", "strength_score", "promoted",
        "youtube_links", "achievements",
    ]

    # 1) Player_Data — all players
    playersDF[_EXPORT_COLS].to_csv(players_csv, index=False)

    # 2) Promoted_Players — promoted only + email texts
    promoted = playersDF[playersDF["promoted"] == 1].copy()
    promoted[_EXPORT_COLS].to_csv(promoted_csv, index=False)
    export_promoted_texts(promoted, out_dir=str(promoted_emails_dir), txt_col="_file_path")

    # 3) Achievement_Details — one row per player × achievement label
    export_achievements_flat(playersDF, players_ach, out_csv=str(achievements_csv))

    # 4) Keyword_Candidates — same as before
    export_new_keyword_candidates(playersDF, out_csv=str(keyword_csv), threshold=0.20)

    # ── Missing field reports ─────────────────────────────────────────────────
    missing_names  = build_missing_names(playersDF)
    missing_emails = build_missing_emails(playersDF)
    missing_clubs  = build_missing_clubs(playersDF)

    # ── Summary ───────────────────────────────────────────────────────────────
    n_total    = playersDF["file_name"].count()
    n_promoted = promoted["file_name"].count()
    pct        = n_promoted / n_total * 100 if n_total else 0.0

    print(f"\nGroup            : {group_label or '(root)'}")
    print(f"Emails parsed    : {n_total}")
    print(f"Threshold        : strength_score >= {threshold}")
    print(f"\nMissing names    : {missing_names['file_name'].count()}")
    print(f"Missing emails   : {missing_emails['file_name'].count()}")
    print(f"Missing clubs    : {missing_clubs['file_name'].count()}")
    print(f"\nPromoted         : {n_promoted} / {n_total}  ({round(pct, 2)}%)")
    print()
    print(players_ach[players_ach["promoted"] == 1].to_string(index=False))

    # ── Charts ────────────────────────────────────────────────────────────────
    if not args.no_charts:
        plot_strength_bar(players_ach,       out_path=str(out_dir / "strength_scores.png"))
        plot_strength_histogram(players_ach, out_path=str(out_dir / "strength_histogram.png"))


if __name__ == "__main__":
    main()
