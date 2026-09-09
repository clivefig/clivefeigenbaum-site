"""Render Option 1 cards 10-up on A4 (front + long-edge-flip back).

Outputs 300 dpi PNG and PDF into ./output/
"""

from __future__ import annotations

from pathlib import Path

import img2pdf
from PIL import Image, ImageDraw, ImageFont

import layout as L

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"
DPI = 300


def px(mm: float) -> float:
    return mm * DPI / 25.4


def pt(size: float) -> int:
    return max(1, round(size * DPI / 72))


def load_font(filename: str, size_pt: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / filename), pt(size_pt))


def draw_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    x_mm: float,
    y_mm: float,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    box_w_mm: float | None = None,
    align: str = "left",
) -> None:
    """Place text so the top of the glyphs sits at y_mm (Canva-style)."""
    x = px(x_mm)
    y = px(y_mm)
    bbox = font.getbbox(text)
    y -= bbox[1]
    if box_w_mm is not None and align == "center":
        tw = bbox[2] - bbox[0]
        x += (px(box_w_mm) - tw) / 2
    draw.text((x, y), text, font=font, fill=fill)


def crop_marks(draw: ImageDraw.ImageDraw, x_mm: float, y_mm: float) -> None:
    """Hairline ticks just outside each card corner."""
    w = max(1, round(px(0.15)))
    outer = 4.0
    inner = 1.2
    gap = 0.4
    corners = [
        (x_mm, y_mm, -1, -1),
        (x_mm + L.CARD_W, y_mm, 1, -1),
        (x_mm, y_mm + L.CARD_H, -1, 1),
        (x_mm + L.CARD_W, y_mm + L.CARD_H, 1, 1),
    ]
    for cx, cy, dx, dy in corners:
        # Prefer the long outer mark when the tick sits in a page margin.
        in_side_margin = cx <= L.MARGIN_L + 0.1 or cx >= L.A4_W - L.MARGIN_L - 0.1
        in_tb_margin = cy <= L.MARGIN_T + 0.1 or cy >= L.A4_H - 8.1
        hx = outer if in_side_margin else inner
        hy = outer if in_tb_margin else inner
        draw.line(
            [px(cx + dx * gap), px(cy), px(cx + dx * (gap + hx)), px(cy)],
            fill=L.MARK,
            width=w,
        )
        draw.line(
            [px(cx), px(cy + dy * gap), px(cx), px(cy + dy * (gap + hy))],
            fill=L.MARK,
            width=w,
        )


def stroke() -> int:
    return max(2, round(px(0.32)))


def icon_phone(draw: ImageDraw.ImageDraw, x_mm: float, y_mm: float, s_mm: float) -> None:
    """Smartphone outline — clearer at 4 mm than a tiny handset."""
    x, y, s = px(x_mm), px(y_mm), px(s_mm)
    w = stroke()
    body = [x + s * 0.30, y + s * 0.06, x + s * 0.70, y + s * 0.94]
    draw.rounded_rectangle(body, radius=max(2, round(s * 0.12)), outline=L.NAVY, width=w)
    cx = x + s / 2
    draw.line([cx - s * 0.08, y + s * 0.18, cx + s * 0.08, y + s * 0.18], fill=L.NAVY, width=w)
    draw.ellipse(
        [cx - s * 0.05, y + s * 0.78, cx + s * 0.05, y + s * 0.88],
        outline=L.NAVY,
        width=max(1, w - 1),
    )


def icon_email(draw: ImageDraw.ImageDraw, x_mm: float, y_mm: float, s_mm: float) -> None:
    x, y, s = px(x_mm), px(y_mm), px(s_mm)
    w = stroke()
    pad = s * 0.12
    box = [x + pad, y + s * 0.22, x + s - pad, y + s * 0.82]
    draw.rounded_rectangle(box, radius=max(1, round(s * 0.08)), outline=L.NAVY, width=w)
    cx = x + s / 2
    draw.line([box[0], box[1], cx, y + s * 0.55, box[2], box[1]], fill=L.NAVY, width=w)


def icon_linkedin(draw: ImageDraw.ImageDraw, x_mm: float, y_mm: float, s_mm: float, font: ImageFont.FreeTypeFont) -> None:
    x, y, s = px(x_mm), px(y_mm), px(s_mm)
    draw.rounded_rectangle([x, y, x + s, y + s], radius=max(2, round(s * 0.18)), fill=L.NAVY)
    mark = "in"
    bbox = font.getbbox(mark)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = x + (s - tw) / 2 - bbox[0]
    ty = y + (s - th) / 2 - bbox[1]
    draw.text((tx, ty), mark, font=font, fill=L.WHITE)


def render_front_card(fonts: dict) -> Image.Image:
    img = Image.new("RGB", (round(px(L.CARD_W)), round(px(L.CARD_H))), L.WHITE)
    d = ImageDraw.Draw(img)
    f = L.FRONT
    draw_text(d, f["name"]["text"], f["name"]["x"], f["name"]["y"], fonts["name"], L.NAVY)
    draw_text(d, f["surname"]["text"], f["surname"]["x"], f["surname"]["y"], fonts["surname"], L.NAVY)
    r = f["rule"]
    d.rectangle(
        [px(r["x"]), px(r["y"]), px(r["x"] + r["w"]), px(r["y"] + r["h"])],
        fill=L.RED,
    )
    draw_text(d, f["invite"]["text"], f["invite"]["x"], f["invite"]["y"], fonts["invite"], L.MUTED)
    return img


def render_back_card(fonts: dict, qr: Image.Image) -> Image.Image:
    img = Image.new("RGB", (round(px(L.CARD_W)), round(px(L.CARD_H))), L.WHITE)
    d = ImageDraw.Draw(img)
    b = L.BACK
    pad = b["pad"]
    d.rounded_rectangle(
        [px(pad["x"]), px(pad["y"]), px(pad["x"] + pad["w"]), px(pad["y"] + pad["h"])],
        radius=round(px(2)),
        fill=L.WHITE,
        outline=(236, 238, 241),
        width=max(1, round(px(0.15))),
    )
    q = b["qr"]
    qr_fit = qr.resize((round(px(q["w"])), round(px(q["h"]))), Image.Resampling.LANCZOS)
    img.paste(qr_fit, (round(px(q["x"])), round(px(q["y"]))))
    cap = b["caption"]
    draw_text(
        d,
        cap["text"],
        cap["x"],
        cap["y"],
        fonts["caption"],
        L.MUTED,
        box_w_mm=cap["w"],
        align="center",
    )
    icon_phone(d, b["icon_phone"]["x"], b["icon_phone"]["y"], b["icon_phone"]["w"])
    icon_email(d, b["icon_email"]["x"], b["icon_email"]["y"], b["icon_email"]["w"])
    icon_linkedin(d, b["icon_linkedin"]["x"], b["icon_linkedin"]["y"], b["icon_linkedin"]["w"], fonts["li"])
    draw_text(d, b["phone"]["text"], b["phone"]["x"], b["phone"]["y"], fonts["value"], L.NAVY)
    draw_text(d, b["email"]["text"], b["email"]["x"], b["email"]["y"], fonts["email"], L.NAVY)
    draw_text(d, b["linkedin"]["text"], b["linkedin"]["x"], b["linkedin"]["y"], fonts["handle"], L.NAVY)
    return img


def impose(card: Image.Image, positions: list[tuple[int, int, float, float]], label: str) -> Image.Image:
    sheet = Image.new("RGB", (round(px(L.A4_W)), round(px(L.A4_H))), L.WHITE)
    d = ImageDraw.Draw(sheet)
    for _col, _row, x, y in positions:
        sheet.paste(card, (round(px(x)), round(px(y))))
        crop_marks(d, x, y)
    caption_font = load_font("Inter-Regular.ttf", 6)
    draw_text(
        d,
        label,
        L.MARGIN_L,
        291.0,
        caption_font,
        L.MARK,
    )
    return sheet


def save_pdf(png_path: Path, pdf_path: Path) -> None:
    layout_fun = img2pdf.get_layout_fun((img2pdf.mm_to_pt(L.A4_W), img2pdf.mm_to_pt(L.A4_H)))
    pdf_path.write_bytes(img2pdf.convert(str(png_path), layout_fun=layout_fun))


def prepare_qr() -> Image.Image:
    src = Image.open(ASSETS / "qrcode.jpg").convert("RGB")
    # Flatten to hard black/white so texture in the JPEG does not muddy modules.
    gray = src.convert("L")
    bw = gray.point(lambda p: 255 if p > 180 else 0, mode="L").convert("RGB")
    # Restore the red SCAN ME disc from the original (colour would be lost in the threshold).
    src_px = src.load()
    bw_px = bw.load()
    w, h = src.size
    for y in range(h):
        for x in range(w):
            r, g, b = src_px[x, y]
            if r > 160 and g < 130 and b < 130 and r - g > 40:
                bw_px[x, y] = (228, 69, 58)
            elif r > 200 and g > 200 and b > 200:
                bw_px[x, y] = (255, 255, 255)
    return bw


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    fonts = {
        "name": load_font("Poppins-ExtraBold.ttf", 28),
        "surname": load_font("Poppins-Medium.ttf", 13),
        "invite": load_font("Inter-Regular.ttf", 9),
        "caption": load_font("Inter-Regular.ttf", 5.5),
        "value": load_font("Inter-Medium.ttf", 8),
        "email": load_font("Inter-Medium.ttf", 7),
        "handle": load_font("Inter-Medium.ttf", 6.5),
        "li": load_font("Poppins-ExtraBold.ttf", 6),
    }
    qr = prepare_qr()
    front_card = render_front_card(fonts)
    back_card = render_back_card(fonts, qr)

    front_sheet = impose(
        front_card,
        L.front_cards(),
        "FRONT  ·  Option 1  ·  10-up  ·  print at 100%  ·  then flip on the LONG edge",
    )
    back_sheet = impose(
        back_card,
        L.back_cards(),
        "BACK  ·  columns swapped for long-edge flip  ·  print at 100%",
    )

    out = OUTPUT / "v1.4"
    out.mkdir(exist_ok=True)
    front_png = out / "option1-front-a4.png"
    back_png = out / "option1-back-a4.png"
    front_sheet.save(front_png, dpi=(DPI, DPI))
    back_sheet.save(back_png, dpi=(DPI, DPI))
    save_pdf(front_png, out / "option1-front-a4.pdf")
    save_pdf(back_png, out / "option1-back-a4.pdf")
    front_card.save(out / "option1-front-card.png", dpi=(DPI, DPI))
    back_card.save(out / "option1-back-card.png", dpi=(DPI, DPI))
    for name in (
        "option1-front-a4.png",
        "option1-back-a4.png",
        "option1-front-a4.pdf",
        "option1-back-a4.pdf",
        "option1-front-card.png",
        "option1-back-card.png",
    ):
        dest = OUTPUT / name
        try:
            dest.write_bytes((out / name).read_bytes())
        except OSError as exc:
            print(f"Could not replace {dest.name} ({exc}). New file is in {out / name}")
    print(f"Wrote files in {out}")


if __name__ == "__main__":
    main()
