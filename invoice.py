# invoice.py

import streamlit as st
from database import session, Invoice
from utils.ui_helpers import show_table, show_success, show_error, download_button
import os

def view_invoices():
    """
    Provides view invoice.
    """
    st.header("View Invoices")
    invoices = session.query(Invoice).all()
    data = [{
        "ID": invoice.id,
        "Job ID": invoice.job_id,
        "Amount": invoice.amount,
        "PDF Path": invoice.pdf_path
    } for invoice in invoices]
    show_table(data)

    for invoice in invoices:
        if st.button(f"Download Invoice {invoice.id}"):
            if os.path.exists(invoice.pdf_path):
                with open(invoice.pdf_path, "rb") as file:
                    btn = download_button(
                        label="Download PDF",
                        data=file.read(),
                        file_name=os.path.basename(invoice.pdf_path)
                    )
            else:
                show_error("Invoice PDF not found.")

def invoice_management():
    """
    Provides manage invoice.
    """
    st.sidebar.subheader("Invoice Management")
    action = st.sidebar.selectbox("Action", ["View Invoices"])

    if action == "View Invoices":
        view_invoices()
