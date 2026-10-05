"""
Run from the repo root:
    python -m unittest tests.test_report_export -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from player_attributes import POSITIONS
from report_export import POSITION_GROUP, write_report, write_summary_html

WEIGHTS = {"All-American": 10, "ECNL MVP": 7, "Showcase": 2}
CATEGORIES = {"Showcase": "team"}


def _players() -> pd.DataFrame:
    rows = [
        # name, email, club, foot, position, achievements, score, promoted, raw text
        ("Jane Doe", ["jane@gmail.com"], "Solar SC", "Left", "Center Back",
         ["Showcase", "All-American", "All-American"], 7.7, 1,
         "coach@purdue.edu\nFW: 2028 CB - Jane Doe\n2026-09-20 10:00:00+00:00\nHi"),
        ("Amy Lee", ["amy@gmail.com"], "Sting", None, None, ["ECNL MVP"], 4.4, 0,
         "From: Amy <amy@gmail.com>\nSubject: Amy Lee - 2029\nDate: Mon, 21 Sep 2026 08:00:00 -0500\n\nHi"),
        (None, None, None, None, "Striker", [], 0.0, 0, "x@y.com\nHello\n2026-09-22 10:00:00\nHi"),
    ]
    cols = ["player_name", "player_email(s)", "player_club", "Dominant Foot", "Primary Position",
            "achievements", "strength_score", "promoted", "_raw_text"]
    df = pd.DataFrame(rows, columns=cols)
    df["file_name"] = ["1.txt", "2.txt", "3.txt"]
    df["youtube_links"] = [["https://youtu.be/a"], None, None]
    return df


class TestReportExport(unittest.TestCase):
    def test_every_position_has_a_group(self):
        self.assertEqual(set(POSITIONS), set(POSITION_GROUP))

    def test_workbook(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.xlsx"
            write_report(_players(), out, 5.0, WEIGHTS, CATEGORIES)
            xl = pd.read_excel(out, sheet_name=None, keep_default_na=False)

        self.assertEqual(list(xl), ["Promoted", "All Players", "Needs Review", "Score Breakdown"])
        promoted = xl["Promoted"]
        self.assertEqual(promoted["Player"].tolist(), ["Jane Doe"])
        row = promoted.iloc[0]
        self.assertEqual(row["Position Group"], "Defender")
        self.assertEqual(row["Achievements"], "All-American; Showcase")   # unique, heaviest first
        self.assertEqual(row["Subject"], "2028 CB - Jane Doe")             # FW: prefix dropped
        self.assertEqual(row["Received"], "2026-09-20")

        everyone = xl["All Players"]
        self.assertEqual(everyone["Score"].tolist(), sorted(everyone["Score"], reverse=True))
        amy = everyone[everyone["Player"] == "Amy Lee"].iloc[0]
        self.assertEqual((amy["Dominant Foot"], amy["Position Group"]), ("", ""))   # blank, never None/nan
        self.assertEqual((amy["Subject"], amy["Received"]), ("Amy Lee - 2029", "2026-09-21"))

        review = xl["Needs Review"].set_index("File")["Reason"]
        self.assertEqual(review["2.txt"], "Position not found; Borderline score (4-5)")
        self.assertEqual(review["3.txt"], "Missing player; Missing email; Missing club")
        self.assertNotIn("1.txt", review.index)

        breakdown = xl["Score Breakdown"]
        self.assertEqual(len(breakdown), 3)                                 # 2 for Jane, 1 for Amy, none for empty
        self.assertEqual(breakdown.iloc[1]["Category"], "Team")

    def test_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            sheets = write_report(_players(), Path(tmp) / "r.xlsx", 5.0, WEIGHTS, CATEGORIES)
            out = Path(tmp) / "s.html"
            write_summary_html(sheets, out, 5.0)
            body = out.read_text(encoding="utf-8")
        self.assertIn("3 new emails", body)
        self.assertIn("<b>1 promoted</b>", body)
        self.assertIn("Jane Doe", body)
        self.assertNotIn("Amy Lee", body)
        self.assertIn("<!--ERRORS-->", body)    # send_emails.py fills this in


if __name__ == "__main__":
    unittest.main()
