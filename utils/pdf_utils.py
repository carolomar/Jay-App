# utils/pdf_utils.py

from fpdf import FPDF
import os

def generate_invoice_pdf(invoice_details, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="Invoice", ln=True, align='C')

    # Invoice Details
    for key, value in invoice_details.items():
        pdf.cell(100, 10, txt=f"{key}:", border=0)
        pdf.cell(100, 10, txt=str(value), border=0, ln=True)

    pdf.output(output_path)
    return output_path
