# app/certificate_utils.py

import fitz  # PyMuPDF
import os
from datetime import datetime

def generate_certificate(name: str) -> str:
    # Dynamically resolve path relative to this file
    template_path = os.path.join(os.path.dirname(__file__), "Certificate_Template_Blank.pdf")
    output_dir = "certificates"
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.now().strftime("%B %d, %Y")
    output_path = os.path.join(output_dir, f"certificate_{name.replace(' ', '_')}.pdf")

    doc = fitz.open(template_path)
    page = doc[0]

    # Insert data at reasonable positions (may tweak visually)
    page.insert_text((320, 305), name, fontsize=22, fontname="helv", fill=(0, 0, 0))
    page.insert_text((400, 410), date_str, fontsize=14, fontname="helv", fill=(0, 0, 0))
    page.insert_text((190, 440), "Muhammad Aktar", fontsize=14, fontname="helv", fill=(0, 0, 0))

    doc.save(output_path)
    doc.close()

    return output_path
