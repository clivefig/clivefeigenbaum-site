"""Option 1 business-card geometry — single source of truth for generate + QA.

All values are millimetres. Origin is top-left of the A4 sheet (or of the card,
when a function is card-relative).
"""

from __future__ import annotations

A4_W = 210.0
A4_H = 297.0
CARD_W = 85.0
CARD_H = 55.0
COLS = 2
ROWS = 5

MARGIN_L = 18.5
MARGIN_T = 6.0
GUTTER_X = 3.0
GUTTER_Y = 2.0

# Canon PIXMA G540 A4 printable area (Canon printing-area spec).
G540_INSET_X = 3.4
G540_INSET_Y = 3.4
G540_PRINTABLE_W = 203.2
G540_PRINTABLE_H = 289.0

NAVY = (30, 58, 95)
MUTED = (91, 107, 122)
RED = (228, 69, 58)
WHITE = (255, 255, 255)
MARK = (154, 164, 176)

# Card-relative Option 1 front — name + invitation, no job title.
FRONT = {
    "name": dict(x=6, y=8, w=73, h=14, text="Clive"),
    "surname": dict(x=6, y=24, w=73, h=8, text="Feigenbaum"),
    "rule": dict(x=6, y=36, w=24, h=0.7),
    "invite": dict(x=6, y=41, w=73, h=6, text="Let's talk."),
}

# Card-relative Option 1 back — QR left, icon + value rows (no word labels).
BACK = {
    "pad": dict(x=5, y=10, w=34, h=34),
    "qr": dict(x=8, y=13, w=28, h=28),
    "caption": dict(x=5, y=45.5, w=34, h=4, text="Save my details"),
    "icon_phone": dict(x=43, y=14.2, w=4.2, h=4.2),
    "phone": dict(x=49, y=14.6, w=30, h=5, text="+972 52 408 3159"),
    "icon_email": dict(x=43, y=24.2, w=4.2, h=4.2),
    "email": dict(x=49, y=24.6, w=30, h=5, text="clive.fig@gmail.com"),
    "icon_linkedin": dict(x=43, y=34.2, w=4.2, h=4.2),
    "linkedin": dict(x=49, y=34.2, w=30, h=10, text="clive-feigenbaum-israel"),
}


def card_origin(col: int, row: int) -> tuple[float, float]:
    if not (0 <= col < COLS and 0 <= row < ROWS):
        raise ValueError(f"col/row out of range: {col},{row}")
    x = MARGIN_L + col * (CARD_W + GUTTER_X)
    y = MARGIN_T + row * (CARD_H + GUTTER_Y)
    return (round(x, 1), round(y, 1))


def front_cards() -> list[tuple[int, int, float, float]]:
    """(col, row, x, y) for the front sheet — natural reading order."""
    out = []
    for row in range(ROWS):
        for col in range(COLS):
            x, y = card_origin(col, row)
            out.append((col, row, x, y))
    return out


def back_cards() -> list[tuple[int, int, float, float]]:
    """Back sheet for long-edge flip: columns swapped, rows unchanged.

    Front card at (col, row) is backed by the card placed at (1 - col, row)
    so that after flipping A4 on the long edge, fronts and backs coincide.
    """
    out = []
    for row in range(ROWS):
        for col in range(COLS):
            x, y = card_origin(1 - col, row)
            out.append((col, row, x, y))
    return out


def card_rect(x: float, y: float) -> tuple[float, float, float, float]:
    return (x, y, x + CARD_W, y + CARD_H)


def printable_rect() -> tuple[float, float, float, float]:
    return (
        G540_INSET_X,
        G540_INSET_Y,
        G540_INSET_X + G540_PRINTABLE_W,
        G540_INSET_Y + G540_PRINTABLE_H,
    )


def is_inside(inner: tuple[float, float, float, float], outer: tuple[float, float, float, float], tol: float = 0.05) -> bool:
    ix0, iy0, ix1, iy1 = inner
    ox0, oy0, ox1, oy1 = outer
    return ix0 >= ox0 - tol and iy0 >= oy0 - tol and ix1 <= ox1 + tol and iy1 <= oy1 + tol
