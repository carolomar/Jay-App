# report.py

import streamlit as st
from database import session, Job, Invoice
from utils.ui_helpers import input_date, show_dataframe
import pandas as pd

def generate_report():
    """
    generate report.
    """
    st.header("Generate Reports")
    start_date = input_date("Start Date")
    end_date = input_date("End Date")

    jobs = session.query(Job).filter(Job.created_at >= start_date, Job.created_at <= end_date).all()
    invoices = session.query(Invoice).join(Job).filter(Job.created_at >= start_date, Job.created_at <= end_date).all()

    total_jobs = len(jobs)
    completed_jobs = len([job for job in jobs if job.status == 'complete'])
    pending_payments = len([invoice for invoice in invoices if invoice.amount > 0 and not invoice.pdf_path])
    revenue = sum(invoice.amount for invoice in invoices if invoice.amount)

    report_data = {
        "Total Jobs": [total_jobs],
        "Completed Jobs": [completed_jobs],
        "Pending Payments": [pending_payments],
        "Total Revenue": [revenue]
    }

    df = pd.DataFrame(report_data)
    show_dataframe(df)

def reporting():
    """
    choose report
    """
    st.sidebar.subheader("Reporting")
    action = st.sidebar.selectbox("Action", ["Generate Reports"])

    if action == "Generate Reports":
        generate_report()
