#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

THREATS_JSON = Path("/opt/SELFIX/data/clamav_threats.json")
REPORT_JSON = Path("/opt/SELFIX/data/scan_report.json")
REPORT_PDF = Path("/opt/SELFIX/reports/scan_report.pdf")


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "SELFIX Antivirus Threat Report", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


def generate_report():
    if not THREATS_JSON.exists():
        print("⚠️ No ClamAV threats found.")
        return

    threats = json.loads(THREATS_JSON.read_text())

    report_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_detected": len(threats),
        "threats": threats
    }

    # Save as JSON
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report_data, indent=2))

    # Generate PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for entry in threats:
        pdf.cell(0, 10, f"{entry['file']} → {entry['status']}", ln=True)

    REPORT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(REPORT_PDF))
    print(f"✅ PDF report saved: {REPORT_PDF}")


if __name__ == "__main__":
    generate_report()
