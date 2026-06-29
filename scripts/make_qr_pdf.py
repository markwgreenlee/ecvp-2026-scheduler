#!/usr/bin/env python3
"""Generate a QR code and a one-page flyer PDF for the ECVP 2026 Scheduler.

Outputs (in the project root):
  - ecvp-scheduler-qr.png   the QR code on its own
  - ECVP_2026_Scheduler_QR.pdf   A4 flyer with title, QR code, and the link

Run from the project root:  python3 scripts/make_qr_pdf.py
"""
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

NAVY = (22 / 255, 50 / 255, 79 / 255)   # #16324f
GREY = (0.42, 0.42, 0.42)


def make_qr():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=20, border=2)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#16324f", back_color="white")
    img.save(QR_PNG)
    print(f"wrote {QR_PNG.name} ({img.size[0]}x{img.size[1]})")


def make_pdf():
    c = canvas.Canvas(str(PDF_OUT), pagesize=A4)
    w, h = A4

    # Title
    c.setFillColorRGB(*NAVY)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(w / 2, h - 45 * mm, TITLE)

    # Subtitle + dateline
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica", 15)
    c.drawCentredString(w / 2, h - 56 * mm, SUBTITLE)
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h - 64 * mm, DATELINE)

    # Prompt
    c.setFillColorRGB(*NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, h - 82 * mm, "Scan to open the schedule app")

    # QR code (centred)
    qr_size = 95 * mm
    qr_x = (w - qr_size) / 2
    qr_y = h - 82 * mm - 12 * mm - qr_size
    c.drawImage(ImageReader(str(QR_PNG)), qr_x, qr_y, qr_size, qr_size,
                preserveAspectRatio=True, mask="auto")

    # Link
    c.setFillColorRGB(*NAVY)
    c.setFont("Helvetica-Bold", 14)
    link_y = qr_y - 14 * mm
    c.drawCentredString(w / 2, link_y, URL)
    c.linkURL(URL, (qr_x, qr_y, qr_x + qr_size, qr_y + qr_size), relative=0)

    # Footer note
    c.setFillColorRGB(*GREY)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(
        w / 2, link_y - 12 * mm,
        "No app store needed — opens in any phone browser and works offline.",
    )
    c.drawCentredString(
        w / 2, link_y - 18 * mm,
        "On iPhone use Safari, on Android use Chrome, then 'Add to Home Screen'.",
    )

    c.showPage()
    c.save()
    print(f"wrote {PDF_OUT.name}")


if __name__ == "__main__":
    make_qr()
    make_pdf()
