#!/usr/bin/env python3
"""Generate a QR code and a one-page flyer PDF for the ECVP 2026 Scheduler.

Outputs (in the project root):
  - ecvp-scheduler-qr.png   the QR code on its own
  - ECVP_2026_Scheduler_QR.pdf   A4 flyer with title, QR code, and the link

Run from the project root:  python3 scripts/make_qr_pdf.py
"""
import json
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
URL = "https://markwgreenlee.github.io/ecvp-2026-scheduler"
TITLE = "ECVP 2026 Scheduler"
SUBTITLE = "European Conference on Visual Perception"
DATELINE = "August 23–27, 2026 · Bournemouth, UK"
QR_PNG = ROOT / "ecvp-scheduler-qr.png"
PDF_OUT = ROOT / "ECVP_2026_Scheduler_QR.pdf"

DESCRIPTION = (
    "Search and organise the entire ECVP 2026 programme on your phone. "
    "Build a personal schedule and export it to your calendar — no app "
    "store, no account, no sign-up."
)

# Counted from the programme rather than hardcoded: the organisers' corrected
# exports change the total (622 -> 614 on 2026-08-06), and a stale figure on a
# flyer published by the conference is not something we can quietly fix later.
ENTRY_COUNT = len(json.loads((ROOT / "assets" / "ecvp-data.json").read_text()))

FEATURES = [
    f"All {ENTRY_COUNT} keynotes, symposia, talks, posters & socials — full-text search",
    "Filter by day (Sun–Thu) and type",
    "Tap any card for the full abstract, authors and affiliations",
    "Build your own schedule and export it to Google Calendar",
    "Works offline after the first load — add it to your home screen",
]

NAVY = (22 / 255, 50 / 255, 79 / 255)   # #16324f
GREY = (0.42, 0.42, 0.42)
DARK = (0.20, 0.20, 0.20)


def make_qr():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=20, border=2)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#16324f", back_color="white")
    img.save(QR_PNG)
    print(f"wrote {QR_PNG.name} ({img.size[0]}x{img.size[1]})")


def _wrap(c, text, font, size, max_width):
    """Greedy word-wrap `text` to lines no wider than `max_width` points."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if c.stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def make_pdf():
    c = canvas.Canvas(str(PDF_OUT), pagesize=A4)
    w, h = A4
    y = h - 34 * mm

    # Title
    c.setFillColorRGB(*NAVY)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(w / 2, y, TITLE)

    # Subtitle + dateline
    y -= 11 * mm
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 15)
    c.drawCentredString(w / 2, y, SUBTITLE)
    y -= 8 * mm
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, y, DATELINE)

    # Divider rule
    y -= 8 * mm
    c.setStrokeColorRGB(*NAVY)
    c.setLineWidth(1)
    c.line(w / 2 - 40 * mm, y, w / 2 + 40 * mm, y)

    # Description (wrapped, centred)
    y -= 11 * mm
    c.setFillColorRGB(*DARK)
    c.setFont("Helvetica", 12.5)
    for line in _wrap(c, DESCRIPTION, "Helvetica", 12.5, 140 * mm):
        c.drawCentredString(w / 2, y, line)
        y -= 6.6 * mm

    # Feature bullets (left-aligned within a centred column)
    y -= 4 * mm
    bullet_x = w / 2 - 68 * mm
    text_x = bullet_x + 5 * mm
    c.setFont("Helvetica", 11.5)
    for feat in FEATURES:
        c.setFillColorRGB(*NAVY)
        c.drawString(bullet_x, y, "•")
        c.setFillColorRGB(*DARK)
        for i, line in enumerate(_wrap(c, feat, "Helvetica", 11.5, 128 * mm)):
            c.drawString(text_x, y, line)
            y -= 5.8 * mm
        y -= 1.4 * mm

    # Prompt
    y -= 4 * mm
    c.setFillColorRGB(*NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, y, "Scan to open the schedule app")

    # QR code (centred)
    qr_size = 72 * mm
    qr_x = (w - qr_size) / 2
    y -= 8 * mm
    qr_y = y - qr_size
    c.drawImage(ImageReader(str(QR_PNG)), qr_x, qr_y, qr_size, qr_size,
                preserveAspectRatio=True, mask="auto")
    c.linkURL(URL, (qr_x, qr_y, qr_x + qr_size, qr_y + qr_size), relative=0)

    # Link
    c.setFillColorRGB(*NAVY)
    c.setFont("Helvetica-Bold", 14)
    link_y = qr_y - 12 * mm
    c.drawCentredString(w / 2, link_y, URL)

    # Footer note
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(
        w / 2, link_y - 10 * mm,
        "No app store needed — opens in any phone browser and works offline.",
    )
    c.drawCentredString(
        w / 2, link_y - 16 * mm,
        "On iPhone use Safari, on Android use Chrome, then 'Add to Home Screen'.",
    )

    c.showPage()
    c.save()
    print(f"wrote {PDF_OUT.name}")


if __name__ == "__main__":
    make_qr()
    make_pdf()
