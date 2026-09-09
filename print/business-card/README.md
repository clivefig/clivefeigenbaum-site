# Option 1 business cards — A4 10-up

Print-ready front and back sheets for Clive Feigenbaum’s identity card (85 × 55 mm) on A4, imposed for a Canon PIXMA G540.

## Print these

| File | What it is |
|---|---|
| `output/v1.4/option1-front-a4.pdf` | 10 fronts, 2 × 5, crop marks |
| `output/v1.4/option1-back-a4.pdf` | 10 backs, **columns swapped** for long-edge flip |
| `output/v1.4/option1-front-a4.png` / `option1-back-a4.png` | Same sheets at 300 dpi (drop onto a Canva A4 at 210 × 297 mm, X 0 Y 0) |
| `output/v1.4/option1-front-card.png` / `option1-back-card.png` | Single 85 × 55 mm cards if you want to rebuild the sheet |

## G540 settings

1. Paper: A4 180 gsm textured board, **one sheet** in the rear tray.
2. **Borderless: Off**
3. Scale: **100% / Actual size** — never Fit to page.
4. Media: Plain paper, High. If navy looks washed, try Matte Photo Paper on a spare sheet.
5. Print **front**. Let it dry.
6. Flip on the **long edge** (like turning a book). Keep the same edge feeding first.
7. Print **back**.
8. Hold one card to the light to confirm the QR sits on the reverse of the name before cutting the rest.

The G540 has no white ink. Unprinted areas show the light blue board — that is intended. The QR’s “white” is the board; scan a test card in indoor light before running a full sheet.

## Cut

Crop marks sit in the gutters (3 mm between columns, 2 mm between rows). Cut columns first with a metal ruler and craft knife, then rows.

## Regenerate / QA

```powershell
cd c:\Projects\clive-personal-site\print\business-card
python -m pip install -r requirements.txt
python generate.py
python -m unittest test_layout.py
```

Layout numbers live in `layout.py` so the generator and tests cannot drift.
