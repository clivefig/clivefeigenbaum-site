"""QA for Option 1 A4 10-up geometry and generated files."""

from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image

import layout as L

OUTPUT = Path(__file__).resolve().parent / "output"
NEW = OUTPUT / "v1.4"
DPI = 300


def mm_from_px(px: int) -> float:
    return px * 25.4 / DPI


class LayoutContract(unittest.TestCase):
    def test_ten_cards(self):
        self.assertEqual(len(L.front_cards()), 10)
        self.assertEqual(len(L.back_cards()), 10)

    def test_front_positions_match_canva_sheet(self):
        expected = [
            (18.5, 6.0),
            (106.5, 6.0),
            (18.5, 63.0),
            (106.5, 63.0),
            (18.5, 120.0),
            (106.5, 120.0),
            (18.5, 177.0),
            (106.5, 177.0),
            (18.5, 234.0),
            (106.5, 234.0),
        ]
        got = [(x, y) for _c, _r, x, y in L.front_cards()]
        self.assertEqual(got, expected)

    def test_back_columns_are_swapped(self):
        front = {(c, r): (x, y) for c, r, x, y in L.front_cards()}
        back = {(c, r): (x, y) for c, r, x, y in L.back_cards()}
        for row in range(L.ROWS):
            self.assertEqual(back[(0, row)], front[(1, row)])
            self.assertEqual(back[(1, row)], front[(0, row)])

    def test_every_card_inside_g540_printable(self):
        printable = L.printable_rect()
        for source in (L.front_cards(), L.back_cards()):
            for _c, _r, x, y in source:
                rect = L.card_rect(x, y)
                self.assertTrue(
                    L.is_inside(rect, printable),
                    f"card {rect} escapes printable {printable}",
                )

    def test_qr_inside_card_and_safe_inset(self):
        q = L.BACK["qr"]
        self.assertEqual((q["w"], q["h"]), (28, 28))
        self.assertGreaterEqual(q["x"], 4)
        self.assertGreaterEqual(q["y"], 4)
        self.assertLessEqual(q["x"] + q["w"], L.CARD_W - 4)
        self.assertLessEqual(q["y"] + q["h"], L.CARD_H - 4)

    def test_front_is_not_a_job_title(self):
        copy = " ".join(
            str(v.get("text", "")) for v in L.FRONT.values() if isinstance(v, dict)
        )
        for banned in ("SAAS", "SaaS", "Onboarding", "Customer Support", "Customer"):
            self.assertNotIn(banned, copy)
        self.assertIn("Clive", copy)
        self.assertIn("Let's talk.", copy)

    def test_back_uses_icons_not_word_labels(self):
        self.assertIn("icon_phone", L.BACK)
        self.assertIn("icon_email", L.BACK)
        self.assertIn("icon_linkedin", L.BACK)
        for key in L.BACK:
            text = L.BACK[key].get("text", "")
            self.assertNotIn(text, ("PHONE", "EMAIL", "LINKEDIN"))

    def test_gutters_are_positive(self):
        cards = L.front_cards()
        left = cards[0]
        right = cards[1]
        self.assertEqual(right[2] - (left[2] + L.CARD_W), L.GUTTER_X)
        below = cards[2]
        self.assertEqual(below[3] - (left[3] + L.CARD_H), L.GUTTER_Y)


class GeneratedFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front = NEW / "option1-front-a4.png" if (NEW / "option1-front-a4.png").exists() else OUTPUT / "option1-front-a4.png"
        cls.back = NEW / "option1-back-a4.png" if (NEW / "option1-back-a4.png").exists() else OUTPUT / "option1-back-a4.png"
        cls.front_pdf = NEW / "option1-front-a4.pdf" if (NEW / "option1-front-a4.pdf").exists() else OUTPUT / "option1-front-a4.pdf"
        cls.back_pdf = NEW / "option1-back-a4.pdf" if (NEW / "option1-back-a4.pdf").exists() else OUTPUT / "option1-back-a4.pdf"
        if not cls.front.exists() or not cls.back.exists():
            raise unittest.SkipTest("Run generate.py first")

    def test_a4_pixel_size_at_300dpi(self):
        for path in (self.front, self.back):
            with Image.open(path) as im:
                w_mm = mm_from_px(im.size[0])
                h_mm = mm_from_px(im.size[1])
                self.assertAlmostEqual(w_mm, L.A4_W, delta=0.3)
                self.assertAlmostEqual(h_mm, L.A4_H, delta=0.3)
                dpi = im.info.get("dpi", (DPI, DPI))
                self.assertAlmostEqual(float(dpi[0]), float(DPI), delta=1)
                self.assertAlmostEqual(float(dpi[1]), float(DPI), delta=1)

    def test_pdfs_exist(self):
        self.assertTrue(self.front_pdf.exists())
        self.assertTrue(self.back_pdf.exists())


if __name__ == "__main__":
    unittest.main()
