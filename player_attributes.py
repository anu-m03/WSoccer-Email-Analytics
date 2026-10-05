"""
player_attributes.py
Purdue Women's Soccer – Dominant Foot & Primary Position extraction

Pulls two recruiting attributes out of a player's email:

    Dominant Foot     → "Left" | "Right" | "Both" | None
    Primary Position  → one of POSITIONS below | None

Both extractors work the same way:
  1. Keep only the player's own writing: skip the email header block, stop at
     quoted replies / forwarded messages, drop ">" quoted lines and game-schedule
     lines ("Sep 20: Solar SC v Sting Dallas (Foothill College)").
  2. Find every candidate mention and score it by context
     ("I am a left-footed…", "Position: CB", subject line, signature line…).
  3. Pick the best-supported value.

`explain_*` returns every candidate with its score and source line so you can
see *why* a value was chosen — inspect_fields.py prints these for local testing.
"""

import re
from dataclasses import dataclass

# ──────────────────────────────────────────────────────────────────────────────
# CANONICAL VALUES
# ──────────────────────────────────────────────────────────────────────────────
FOOT_VALUES = ("Left", "Right", "Both")

POSITIONS = (
    # Goalkeeper
    "Goalkeeper",
    # Defenders
    "Center Back", "Left Back", "Right Back", "Left Wing Back", "Right Wing Back",
    "Fullback",             # side unknown ("outside back", "wing back")
    "Defender",             # generic
    # Midfielders
    "Defensive Midfielder", "Center Midfielder", "Attacking Midfielder",
    "Left Midfielder", "Right Midfielder",
    "Midfielder",           # generic
    # Forwards
    "Left Winger", "Right Winger",
    "Winger",               # side unknown
    "Striker",
    "Forward",              # generic
)

# A generic label is upgraded to a specific one from the same family when the
# email names both ("I'm a midfielder, mostly playing the 6 / CDM").
_GENERIC_FAMILIES = {
    "Defender":   {"Center Back", "Left Back", "Right Back", "Left Wing Back",
                   "Right Wing Back", "Fullback"},
    "Fullback":   {"Left Back", "Right Back", "Left Wing Back", "Right Wing Back"},
    "Midfielder": {"Defensive Midfielder", "Center Midfielder", "Attacking Midfielder",
                   "Left Midfielder", "Right Midfielder"},
    "Forward":    {"Striker", "Left Winger", "Right Winger", "Winger"},
    "Winger":     {"Left Winger", "Right Winger"},
}


@dataclass(frozen=True)
class Candidate:
    value: str
    score: float
    line_no: int        # 1-based line number in the original text
    line: str           # original line text
    match: str          # matched text
    reason: str         # which rule / context produced the score


# ──────────────────────────────────────────────────────────────────────────────
# TEXT SCOPING
# ──────────────────────────────────────────────────────────────────────────────
_HEADER_RE = re.compile(r"(?i)^\s*(from|to|cc|bcc|subject|date|sent|reply-to)\s*:\s*(.*)$")
_BARE_EMAIL_RE = re.compile(r"^\s*[\w.%+-]+@[\w.-]+\.[a-z]{2,}\s*$", re.I)
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}")
_QUOTE_PREFIX_RE = re.compile(r"^(?:\s*>)+\s?")
# Messages from these senders in a thread are staff, not the player
_STAFF_DOMAINS = ("purdue.edu",)
_REPLY_BOUNDARY_RE = re.compile(
    r"(?i)^\s*(?:"
    r"on\s.+\swrote:\s*$"                      # Gmail / Apple reply header
    r"|-{2,}\s*(?:original|forwarded)\s+message"
    r"|begin\s+forwarded\s+message"
    r"|_{5,}\s*$"                               # Outlook reply separator
    r"|(?:from|sent)\s*:\s"                     # Outlook quoted header
    r")"
)
# Game-schedule lines: "Sep 20, 2025: Solar SC v Sting (Foothill College)"
_SCHEDULE_RE = re.compile(r"(?i)\s(?:v|vs\.?|versus)\s")


def _normalize_line(line: str) -> str:
    """Same-length normalization so match offsets still line up with the original."""
    line = line.replace("’", "'").replace("–", "-").replace("—", "-")
    line = re.sub(r"(?i)centre", lambda m: "center" if m.group(0).islower() else m.group(0)[:4] + "er", line)
    line = re.sub(r"(?i)defence", lambda m: m.group(0)[:5] + "se", line)
    # join hyphenated words with a space: "left-footed" → "left footed"
    return re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", " ", line)


def _is_staff(sender: str) -> bool:
    return any(d in sender.lower() for d in _STAFF_DOMAINS)


def _scoped_lines(text: str, history: bool = False) -> list[tuple[int, str, str, bool]]:
    """Return (line_no, original, normalized, is_subject) for the player's own text.

    By default only the newest message is read.  history=True also reads the
    earlier messages quoted below it (a follow-up often leaves the details in the
    player's first email), skipping any message sent by staff.
    """
    lines = text.splitlines()
    out: list[tuple[int, str, str, bool]] = []
    start = 0
    staff_block = False

    if lines and _BARE_EMAIL_RE.match(lines[0]):
        # get_gmails.py .txt layout: sender / subject (may wrap) / date / body
        date_idx = next((i for i in range(2, min(len(lines), 6)) if _TIMESTAMP_RE.match(lines[i])), 2)
        if len(lines) > 1:
            subject = " ".join(l.strip() for l in lines[1:date_idx] if l.strip())
            out.append((2, lines[1], _normalize_line(subject), True))
        start = date_idx + 1
        # a staff member forwarding the player's email: their own note above the
        # forwarded message isn't the player's writing
        staff_block = _is_staff(lines[0]) and any(_REPLY_BOUNDARY_RE.match(l) for l in lines[start:])
    else:
        # .eml layout: "Header: value" lines up to the first blank line
        i = 0
        while i < len(lines) and _HEADER_RE.match(lines[i]):
            m = _HEADER_RE.match(lines[i])
            if m.group(1).lower() == "subject":
                out.append((i + 1, lines[i], _normalize_line(m.group(2)), True))
            i += 1
        start = i

    unquote = (lambda l: _QUOTE_PREFIX_RE.sub("", l)) if history else (lambda l: l)
    has_body = False
    idx = start
    while idx < len(lines):
        line = unquote(lines[idx])
        if _REPLY_BOUNDARY_RE.match(line):
            if has_body and not history:
                break
            # Nothing of the player's above the separator means a forward wrapper
            # (staff forwarding the player's email); in history mode every separator
            # starts an earlier message.  Skip the header block and read what's under it.
            sender = line
            subjects = []
            idx += 1
            while idx < len(lines):
                h = unquote(lines[idx])
                if h.strip() and not _HEADER_RE.match(h) and not _REPLY_BOUNDARY_RE.match(h):
                    break
                m = _HEADER_RE.match(h)
                if m and m.group(1).lower() == "from":
                    sender += " " + h
                if m and m.group(1).lower() == "subject":
                    subjects.append((idx + 1, h, _normalize_line(m.group(2)), True))
                idx += 1
            staff_block = _is_staff(sender)
            if not staff_block:
                out.extend(subjects)
            continue
        idx += 1
        if staff_block or not line.strip() or line.lstrip().startswith(">"):
            continue
        if _SCHEDULE_RE.search(line):
            continue
        out.append((idx, line, _normalize_line(line), False))
        has_body = True
    return out


def _sentence_before(norm: str, pos: int) -> str:
    """Text from the start of the current sentence up to pos (lowercased)."""
    head = norm[:pos]
    cut = max(head.rfind(ch) for ch in ".!?;")
    return head[cut + 1:].lower()


def _drop_overlaps(hits: list[tuple[int, int, str, str, bool]]):
    """Keep the longest match wherever matches overlap (e.g. 'left wing back' over 'wing back')."""
    hits = sorted(hits, key=lambda h: (-(h[1] - h[0]), h[0]))
    kept: list[tuple[int, int, str, str, bool]] = []
    for h in hits:
        if all(h[1] <= k[0] or h[0] >= k[1] for k in kept):
            kept.append(h)
    return sorted(kept, key=lambda h: h[0])


# ──────────────────────────────────────────────────────────────────────────────
# DOMINANT FOOT
# ──────────────────────────────────────────────────────────────────────────────
_SIDE = r"(left|right|l|r)"
# "primarily right back" is a position, not a foot
_NOT_POSITION = r"(?!\s+(?:back|wing|winger|mid|midfield|midfielder|forward|defender|side|full\s?back|outside|center))"
# (regex, score, mode) — mode "side" = group 1 is the side, "opposite" = group 1
# is the WEAK side, "both" = two-footed.  Order matters only for readability;
# overlaps are resolved by longest match.
_FOOT_RULES: list[tuple[re.Pattern, float, str, str]] = [
    (re.compile(r"\b(?:dominant|preferred|strong|stronger|natural|main|primary|better|favorite|favourite)\s+"
                r"foot\s*(?:is|:|-|=)?\s*(?:my\s+|the\s+)?" + _SIDE + r"\b", re.I),
     3, "side", "labeled dominant/preferred foot"),
    (re.compile(r"\bfoot(?:edness)?\s*(?::|-|=)\s*" + _SIDE + r"\b", re.I),
     3, "side", "'Foot:' label"),
    (re.compile(r"\b(left|right)\s?foot(?:ed|er)\b", re.I),
     3, "side", "'<side>-footed'"),
    (re.compile(r"\b(left|right)\s+foot\s+(?:is\s+)?(?:my\s+)?(?:dominant|preferred|strong|stronger|natural)\b", re.I),
     3, "side", "'<side> foot dominant'"),
    (re.compile(r"\bprefer(?:s|red)?\s+(?:to\s+use\s+)?(?:my\s+|the\s+|her\s+)?(left|right)\b(?:\s+foot\b)?" + _NOT_POSITION, re.I),
     3, "side", "'prefer my <side>'"),
    (re.compile(r"\b(?:naturally|primarily|predominantly)\s+(left|right)\b" + _NOT_POSITION, re.I),
     2, "side", "'naturally <side>'"),
    (re.compile(r"\b(left|right)\s+(?:foot\s+|footed\s+)?dominant\b", re.I),
     2, "side", "'<side> dominant'"),
    (re.compile(r"\b(lefty|leftie|righty|rightie)\b", re.I),
     2, "side", "lefty/righty"),
    (re.compile(r"\b(?:dominant|preferred|strong|stronger|natural|main|primary|better|favorite|favourite)\s+"
                r"foot\s*(?:is|:|-|=)?\s*(?:both|either|left\s*(?:and|&|/)\s*right|right\s*(?:and|&|/)\s*left)\b"
                r"|\bfoot(?:edness)?\s*(?::|-|=)\s*(?:both|either)\b"
                r"|\b(?:left\s*(?:and|&|/)\s*right|right\s*(?:and|&|/)\s*left)\s+(?:foot|footed|feet)\b", re.I),
     3, "both", "labeled both feet"),
    (re.compile(r"\b(?:two|both|2)\s?footed\b|\bambipedal\b"
                r"|\b(?:comfortable|confident|strong|effective|equally\s+\w+)\s+(?:with|on|using)\s+(?:both|either)\s+(?:feet|foot)\b"
                r"|\bus(?:e|es|ing)\s+(?:both|either)\s+(?:feet|foot)\b", re.I),
     2.5, "both", "two-footed"),
    # Weak-foot mentions point to the OTHER side
    (re.compile(r"\b(?:weak|weaker|off|non\s?dominant|other)\s+foot\s*(?:is|:|-)?\s*(?:my\s+)?(left|right)\b", re.I),
     2, "opposite", "labeled weak foot"),
    (re.compile(r"\b(?:weak|weaker|non\s?dominant)\s+(left|right)\s+foot\b", re.I),
     2, "opposite", "'weak <side> foot'"),
    (re.compile(r"\b(left|right)\s+foot\s+is\s+(?:my\s+)?(?:weak|weaker)\b", re.I),
     2, "opposite", "'<side> foot is weaker'"),
    (re.compile(r"\b(?:working\s+on|improving|improve|developing|develop|strengthening|strengthen)\s+(?:my\s+)?(left|right)\s+foot\b", re.I),
     1, "opposite", "'working on my <side> foot'"),
    # Weakest signal: incidental "with my left foot"
    (re.compile(r"\b(?:my|her)\s+(left|right)\s+foot\b", re.I),
     1, "side", "incidental '<side> foot'"),
]

_SIDE_NORMAL = {"left": "Left", "l": "Left", "lefty": "Left", "leftie": "Left",
                "right": "Right", "r": "Right", "righty": "Right", "rightie": "Right"}
_OPPOSITE = {"Left": "Right", "Right": "Left"}


def _with_history(collect, text: str) -> list[Candidate]:
    """Read the newest message; fall back to the player's earlier messages in the thread."""
    if not isinstance(text, str) or not text.strip():
        return []
    return collect(_scoped_lines(text)) or collect(_scoped_lines(text, history=True))


def explain_dominant_foot(text: str) -> list[Candidate]:
    return _with_history(_foot_candidates, text)


def _foot_candidates(scoped) -> list[Candidate]:
    cands: list[Candidate] = []
    for line_no, orig, norm, _ in scoped:
        hits = []
        for rx, score, mode, reason in _FOOT_RULES:
            for m in rx.finditer(norm):
                hits.append((m.start(), m.end(), f"{score}|{mode}|{reason}", m.group(0),
                             m.group(1) if m.lastindex else None))
        for start, end, meta, matched, side in _drop_overlaps(hits):
            score, mode, reason = meta.split("|", 2)
            if mode == "both":
                value = "Both"
            else:
                value = _SIDE_NORMAL.get((side or "").lower())
                if not value:
                    continue
                if mode == "opposite":
                    value = _OPPOSITE[value]
            cands.append(Candidate(value, float(score), line_no, orig.strip(), matched, reason))
    return cands


def extract_dominant_foot(text: str) -> str | None:
    """Return "Left", "Right", "Both", or None when not stated / ambiguous."""
    cands = explain_dominant_foot(text)
    if not cands:
        return None
    totals: dict[str, float] = {}
    best_single: dict[str, float] = {}
    for c in cands:
        totals[c.value] = totals.get(c.value, 0.0) + c.score
        best_single[c.value] = max(best_single.get(c.value, 0.0), c.score)
    ranked = sorted(totals, key=lambda v: (totals[v], best_single[v]), reverse=True)
    if len(ranked) > 1 and (totals[ranked[0]], best_single[ranked[0]]) == \
            (totals[ranked[1]], best_single[ranked[1]]):
        return None     # genuinely conflicting evidence
    return ranked[0]


# ──────────────────────────────────────────────────────────────────────────────
# PRIMARY POSITION
# ──────────────────────────────────────────────────────────────────────────────
_MID = r"(?:midfielder|midfield|mid)"

# (label, regex, needs_context) — needs_context=True means the word is too
# ambiguous on its own ("looking forward", "the wing", "defense") and only
# counts next to a player cue, in the subject, or on a short signature line.
_POSITION_RULES: list[tuple[str, re.Pattern, bool]] = [
    ("Goalkeeper",           re.compile(r"\bgoal\s?keeper\b|\bgoalie\b|\bkeeper\b|\bshot\s?stopper\b|\bsweeper\s+keeper\b", re.I), False),
    ("Goalkeeper",           re.compile(r"\bgoal\s?keeping\b", re.I), True),
    ("Left Wing Back",       re.compile(r"\bleft\s+wing\s?back\b", re.I), False),
    ("Right Wing Back",      re.compile(r"\bright\s+wing\s?back\b", re.I), False),
    ("Left Back",            re.compile(r"\bleft\s+(?:full\s?back|outside\s+back|side\s+back|back|defender)\b|\bleftback\b", re.I), False),
    ("Right Back",           re.compile(r"\bright\s+(?:full\s?back|outside\s+back|side\s+back|back|defender)\b|\brightback\b", re.I), False),
    ("Fullback",             re.compile(r"\b(?:full\s?back|outside\s+back|wide\s+back|wing\s?back)\b", re.I), False),
    ("Center Back",          re.compile(r"\b(?:center|central)\s?(?:back|defender)\b|\bcenter\s+half\b|\bsweeper\b", re.I), False),
    ("Defensive Midfielder", re.compile(rf"\b(?:defensive|holding)\s+(?:center\s+|central\s+)?{_MID}\b|\bcenter\s+defensive\s+{_MID}\b|\banchor\s+{_MID}\b", re.I), False),
    ("Attacking Midfielder", re.compile(rf"\b(?:attacking|offensive)\s+(?:center\s+|central\s+)?{_MID}\b|\bcenter\s+attacking\s+{_MID}\b|\bplaymaker\b", re.I), False),
    ("Center Midfielder",    re.compile(rf"\b(?:center|central)\s+{_MID}\b|\bbox\s+to\s+box(?:\s+{_MID})?\b", re.I), False),
    ("Left Midfielder",      re.compile(rf"\bleft\s+(?:side\s+|wide\s+|outside\s+)?{_MID}\b", re.I), False),
    ("Right Midfielder",     re.compile(rf"\bright\s+(?:side\s+|wide\s+|outside\s+)?{_MID}\b", re.I), False),
    ("Left Winger",          re.compile(r"\bleft\s+(?:winger|wing|wide\s+forward|forward|attacker)\b", re.I), False),
    ("Right Winger",         re.compile(r"\bright\s+(?:winger|wing|wide\s+forward|forward|attacker)\b", re.I), False),
    ("Winger",               re.compile(r"\bwinger\b", re.I), False),
    ("Winger",               re.compile(r"\b(?:wing|wide\s+forward|wide\s+attacker)\b", re.I), True),
    ("Striker",              re.compile(r"\bstriker\b|\b(?:center|central)\s+forward\b|\btarget\s+(?:forward|striker)\b", re.I), False),
    ("Forward",              re.compile(r"\bforward\b|\battacker\b", re.I), True),
    ("Midfielder",           re.compile(rf"\bmidfielder\b|\b(?:outside|wide|two\s+way)\s+{_MID}\b", re.I), False),
    ("Midfielder",           re.compile(r"\bmidfield\b", re.I), True),
    ("Defender",             re.compile(r"\bdefender\b", re.I), False),
    ("Defender",             re.compile(r"\bdefense\b", re.I), True),
]

# Abbreviations — case-sensitive and always need context ("Position: CB", "2028 GK")
_ABBREV_TO_POS = {
    "GK": "Goalkeeper", "FB": "Fullback", "CB": "Center Back", "LCB": "Center Back", "RCB": "Center Back",
    "LB": "Left Back", "RB": "Right Back", "LWB": "Left Wing Back", "RWB": "Right Wing Back",
    "CDM": "Defensive Midfielder", "CM": "Center Midfielder", "CAM": "Attacking Midfielder",
    "LM": "Left Midfielder", "RM": "Right Midfielder",
    "LW": "Left Winger", "RW": "Right Winger", "ST": "Striker", "CF": "Striker",
}
_ABBREV_RE = re.compile(r"(?<![\w'])(" + "|".join(sorted(_ABBREV_TO_POS, key=len, reverse=True)) + r")(?![\w'])")

# Context that says "this is the player describing herself", matched against the
# sentence text immediately before the position mention.
_SELF_CUE_RE = re.compile(
    r"(?:\bi\s+am\b|\bi'?m\b|\bim\b)\s+(?:a|an|the)\b[^.!?]{0,60}$"
    r"|\b(?:is|was)\s+(?:a|an)\b[^.!?]{0,50}$"                    # parent: "Jane is a …"
    r"|\bplay(?:s|ed|ing)?\b(?!\s+(?:against|with|alongside|for|under|behind|beside|next|vs)\b)(?:\s+(?:as|at|in))?(?:\s+(?:a|an|the))?\s*(?:[\w'/-]+\s+){0,3}$"
    r"|\bas\s+(?:a|an|the)\b\s*(?:[\w'/-]+\s+){0,4}$"
    r"|\bpositions?\b\s*(?:is|are|was|:|-|=|of)?\s*(?:[\w'/-]+\s+){0,3}$"
    r"|\b(?:class\s+of\s+)?20\d\d\b\s*(?:[\w'/|-]+\s+){0,3}$"
    r"|\brecruiting\s+(?:a|an)\s*(?:[\w'/-]+\s+){0,2}$"
)
# List continuation ("I play center back, right back") — only inside a self-described sentence
_LIST_CONT_RE = re.compile(r"(?:[,/&|(]|\band|\bor)\s*$")
_SELF_ANY_RE = re.compile(r"\bi\s+am\b|\bi'?m\b|\bplay|\bpositions?\b|\b(?:is|was)\s+(?:a|an)\b|\b20\d\d\b")
_PRIMARY_CUE_RE = re.compile(
    r"\b(?:primar(?:y|ily)|natural(?:ly)?|main(?:ly)?|best|usual(?:ly)?|typical(?:ly)?|preferred|favorite|mostly)\b[^.!?]{0,40}$"
)
_SECONDARY_CUE_RE = re.compile(
    r"\b(?:also|secondary|second|backup|as\s+well\s+as|other\s+positions?|can\s+(?:also\s+)?play|filled\s+in|experience\s+(?:at|in|playing))\b[^.!?]{0,40}$"
)
# Someone else's position: "your goalkeepers", "my sister is a defender"
_OTHER_PERSON_RE = re.compile(
    r"\b(?:your|their|opposing|the\s+other)\s+(?:[\w'-]+\s+){0,2}$"
    r"|\bour\s+(?:starting\s+|current\s+|senior\s+|other\s+)?$"
    r"|\bmy\s+(?:sister|brother|teammate|teammates|friend|cousin|mom|dad|mother|father)\b[^.!?]{0,40}$"
)
_AFTER_REJECT_RE = re.compile(r"(?i)^\s*(?:coach|coaches|coaching|trainer|training\s+staff|union|gloves)\b")
# "looking forward", "moving forward", "get right back to you"
_FORWARD_IDIOM_BEFORE_RE = re.compile(
    r"\b(?:look|looking|looks|looked|move|moving|going|go|step|stepping|put|putting|come|coming|carry|"
    r"carrying|push|pushing|fast|straight|bring|brought|pay|paying|way|path|leap)\s*$", re.I)
_FORWARD_IDIOM_AFTER_RE = re.compile(r"(?i)^\s*(?:to|with|thinking|in\s+time|motion)\b")
_BACK_IDIOM_BEFORE_RE = re.compile(
    r"\b(?:get|got|getting|be|been|write|wrote|reply|respond|come|came|go|went|call|email|text|head|bounce|bounced|fight|fought)\s+$", re.I)
_BACK_IDIOM_AFTER_RE = re.compile(r"(?i)^\s*(?:to|at|into|in|on|home|here|there|then|with|from)\b")


def _is_short_line(norm: str) -> bool:
    """Signature / label style line ("Class of 2028 | Center Back"), not a sentence."""
    s = norm.strip()
    return len(s) <= 60 and len(s.split()) <= 7 and not s.endswith((".", "!", "?"))


def _position_hits(norm: str) -> list[tuple[int, int, str, str, bool]]:
    hits = []
    for label, rx, needs_ctx in _POSITION_RULES:
        for m in rx.finditer(norm):
            hits.append((m.start(), m.end(), label, m.group(0), needs_ctx))
    for m in _ABBREV_RE.finditer(norm):
        # "170 CM" is a height, not a center mid
        if m.group(1) == "CM" and re.search(r"\d\s*$", norm[:m.start()]):
            continue
        hits.append((m.start(), m.end(), _ABBREV_TO_POS[m.group(1)], m.group(0), True))
    return _drop_overlaps(hits)


def explain_primary_position(text: str) -> list[Candidate]:
    return _with_history(_position_candidates, text)


def _position_candidates(scoped) -> list[Candidate]:
    cands: list[Candidate] = []
    for line_no, orig, norm, is_subject in scoped:
        short = _is_short_line(norm)
        for start, end, label, matched, needs_ctx in _position_hits(norm):
            before = _sentence_before(norm, start)
            after = norm[end:]

            if label in ("Forward", "Left Winger", "Right Winger") and matched.lower().endswith("forward"):
                if _FORWARD_IDIOM_BEFORE_RE.search(before) or _FORWARD_IDIOM_AFTER_RE.match(after):
                    continue
            if label in ("Left Back", "Right Back") and matched.lower().endswith(" back"):
                if _BACK_IDIOM_BEFORE_RE.search(before) or _BACK_IDIOM_AFTER_RE.match(after):
                    continue
            if _AFTER_REJECT_RE.match(after):
                continue

            self_cue = bool(_SELF_CUE_RE.search(before)) or bool(
                _LIST_CONT_RE.search(before) and _SELF_ANY_RE.search(before))
            if _OTHER_PERSON_RE.search(before) and not re.search(r"\bi\b|\bi'?m\b|\bmy\s+position", before[-25:]):
                continue

            if self_cue:
                score, reason = 3.0, "player cue"
            elif is_subject:
                score, reason = 2.5, "subject line"
            elif short:
                score, reason = 2.0, "short/signature line"
            elif not needs_ctx:
                score, reason = 1.0, "bare mention"
            else:
                continue

            if _SECONDARY_CUE_RE.search(before):
                score, reason = 0.5, reason + " (secondary)"
            elif _PRIMARY_CUE_RE.search(before):
                score, reason = score + 2.0, reason + " + primary"

            cands.append(Candidate(label, score, line_no, orig.strip(), matched, reason))
    return cands


def extract_primary_position(text: str) -> str | None:
    """Return the canonical primary position (see POSITIONS) or None."""
    cands = explain_primary_position(text)
    if not cands:
        return None

    agg: dict[str, dict] = {}
    for order, c in enumerate(cands):
        a = agg.setdefault(c.value, {"best": 0.0, "n": 0, "first": order})
        a["best"] = max(a["best"], c.score)
        a["n"] += 1
    # best single mention, small bonus for repetition, earliest mention breaks ties
    rank = lambda v: (agg[v]["best"] + 0.25 * min(agg[v]["n"] - 1, 2), -agg[v]["first"])
    best = max(agg, key=rank)

    # Upgrade a generic label to a specific one from the same family if named
    while best in _GENERIC_FAMILIES:
        specifics = [v for v in agg if v in _GENERIC_FAMILIES[best] and agg[v]["best"] >= 1.0]
        if not specifics:
            break
        best = max(specifics, key=rank)
    return best
