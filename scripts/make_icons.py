#!/usr/bin/env python3
"""Generate an original ECVP 2026 scheduler icon set (no third-party logo).

Draws a simple stylised eye (a vision/perception motif) on the ECVP navy, with
"ECVP" beneath it, then exports every size the app and PWA need. The artwork is
generated at 1024px and downscaled with Lanczos resampling.

Run from the project root:  python3 scripts/make_icons.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

NAVY = (22, 50, 79)        # #16324f  brand primary
BLUE = (43, 110, 166)      # #2b6ea6  ECVP gradient accent
WHITE = (255, 255, 255)
DARK = (10, 22, 36)

# path (relative to project root) -> square size in px
TARGETS = {
    "assets/icon.png": 1024,                    # Expo app icon
    "assets/adaptive-icon.png": 1024,           # Android adaptive foreground
    "assets/favicon.png": 48,                   # small favicon
    "public/icons/icon-192.png": 192,           # PWA / Android
    "public/icons/icon-512.png": 512,           # PWA / Android
    "public/icons/apple-touch-icon.png": 180,   # Safari iPhone home screen
}


def load_font(size):
    for path in (
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def render_master(n=1024):
    """Render the master 1024px icon."""
    img = Image.new("RGBA", (n, n), NAVY + (255,))
    d = ImageDraw.Draw(img)

    cx, cy = n // 2, int(n * 0.42)
    eye_w, eye_h = int(n * 0.72), int(n * 0.40)

    # White almond eye shape
    d.ellipse(
        [cx - eye_w // 2, cy - eye_h // 2, cx + eye_w // 2, cy + eye_h // 2],
        fill=WHITE,
    )

    # Iris (concentric rings)
    iris_r = int(eye_h * 0.46)
    d.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], fill=BLUE)
    ring_r = int(iris_r * 0.72)
    d.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], fill=NAVY)

    # Pupil
    pup_r = int(iris_r * 0.40)
    d.ellipse([cx - pup_r, cy - pup_r, cx + pup_r, cy + pup_r], fill=DARK)

    # Catch-light highlight
    hl_r = int(iris_r * 0.16)
    hx, hy = cx - int(iris_r * 0.30), cy - int(iris_r * 0.32)
    d.ellipse([hx - hl_r, hy - hl_r, hx + hl_r, hy + hl_r], fill=WHITE)

    # Eye outline
    d.ellipse(
        [cx - eye_w // 2, cy - eye_h // 2, cx + eye_w // 2, cy + eye_h // 2],
        outline=NAVY, width=int(n * 0.018),
    )

    # Wordmark
    font = load_font(int(n * 0.18))
    text = "ECVP"
    tb = d.textbbox((0, 0), text, font=font)
    tw = tb[2] - tb[0]
    d.text((cx - tw // 2 - tb[0], int(n * 0.70) - tb[1]), text, font=font, fill=WHITE)

    return img


def flatten(img, size, bg=WHITE):
    out = img.resize((size, size), Image.LANCZOS)
    base = Image.new("RGBA", (size, size), bg + (255,))
    base.alpha_composite(out)
    return base.convert("RGB")


def main():
    master = render_master(1024)
    for rel, size in TARGETS.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        # The icon already fills its background with navy, so flatten on navy.
        flatten(master, size, bg=NAVY).save(out, "PNG")
        print(f"wrote {rel} ({size}x{size})")


if __name__ == "__main__":
    main()
