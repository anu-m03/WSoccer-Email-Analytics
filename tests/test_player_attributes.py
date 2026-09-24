"""
Run from the repo root:
    python -m unittest tests.test_player_attributes -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from player_attributes import POSITIONS, extract_dominant_foot, extract_primary_position

# (email text, expected value)
FOOT_CASES = [
    ("I am a left-footed center back for Solar SC.", "Left"),
    ("I'm a Right footed midfielder.", "Right"),
    ("Dominant foot: Left", "Left"),
    ("Preferred Foot - R", "Right"),
    ("Foot: L", "Left"),
    ("My strong foot is my right and I love to switch play.", "Right"),
    ("I am a lefty who can deliver crosses.", "Left"),
    ("I'm two-footed and comfortable anywhere on the field.", "Both"),
    ("I'm comfortable with both feet but prefer my left.", "Left"),
    ("I've been working on my left foot this offseason.", "Right"),
    ("My weaker foot is my left.", "Right"),
    # traps — no foot information
    ("I play primarily right back for Sting.", None),
    ("I play right back and left back.", None),
    ("Sep 20, 2025: MVLA v Marin FC (Foothill College)", None),
    ("I left the club last spring. Right now I play for Solar SC.", None),
    ("Thanks for your time, I look forward to hearing from you.", None),
]

POSITION_CASES = [
    ("I am a Class of 2028 Center Back with a 3.9 GPA.", "Center Back"),
    ("I play center-back and right back for Solar SC.", "Center Back"),
    ("I primarily play as a right back, but I also have experience at center back.", "Right Back"),
    ("I'm a versatile midfielder, mostly playing CDM this season.", "Defensive Midfielder"),
    ("Position: CB/RB", "Center Back"),
    ("Position: GK", "Goalkeeper"),
    ("I am a goalkeeper for the Sting Dallas ECNL team.", "Goalkeeper"),
    ("I'm an attacking mid who loves to create chances.", "Attacking Midfielder"),
    ("I play Striker for FC Dallas.", "Striker"),
    ("I am a forward for Solar SC.", "Forward"),
    ("I play left wing back in a 3-5-2.", "Left Wing Back"),
    ("I am a Right Midfielder/Winger and scored 12 goals.", "Right Midfielder"),
    ("I am a Left Midfielder/Left Winger for Beach FC.", "Left Midfielder"),
    ("Her primary position is outside back, and she is left footed.", "Fullback"),
    ("My daughter Jane is a central midfielder at Solar SC.", "Center Midfielder"),
    # signature block (generator layout)
    ("Thank you,\nJane Doe\n\nSolar SC ECNL\nClass of 2028\nCenter Back/Sweeper", "Center Back"),
    # get_gmails.py .txt layout with the position only in the subject
    ("jane@gmail.com\n2028 Goalkeeper - Jane Doe - Solar SC\n2026-09-20 10:00:00\nHi Coach,\nI wanted to introduce myself.",
     "Goalkeeper"),
    # traps — no position information
    ("I look forward to hearing from you. Moving forward I hope to stay in touch.", None),
    ("I'll get right back to you with my schedule.", None),
    ("Sep 06, 2025: Stanford Strikers10G v San Ramon FC (Rossotti Field)", None),
    ("I am 5'7 / 170 CM and play for Solar SC in the Mid-Atlantic conference.", None),
    ("I'd love to meet your goalkeeper coach at camp.", None),
    ("We played against a strong forward last weekend.", None),
    # quoted reply from the coach is ignored
    ("I am a center back.\n\nOn Mon, Sep 1, 2025 at 9:00 AM Coach Ward <robward@purdue.edu> wrote:\n> We are looking for a striker.",
     "Center Back"),
]


class TestDominantFoot(unittest.TestCase):
    def test_cases(self):
        for text, expected in FOOT_CASES:
            with self.subTest(text=text):
                self.assertEqual(extract_dominant_foot(text), expected)


class TestPrimaryPosition(unittest.TestCase):
    def test_cases(self):
        for text, expected in POSITION_CASES:
            with self.subTest(text=text):
                self.assertEqual(extract_primary_position(text), expected)

    def test_outputs_are_canonical(self):
        for text, _ in POSITION_CASES:
            value = extract_primary_position(text)
            self.assertTrue(value is None or value in POSITIONS, value)


if __name__ == "__main__":
    unittest.main()
