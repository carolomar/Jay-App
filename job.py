# job.py

import streamlit as st
from database import session, Job, Company, Invoice
from utils.ui_helpers import input_text, input_selectbox, show_table, show_success, show_error
from utils.pdf_utils import generate_invoice_pdf
import os

def add_job():
    """
    Provides a form to add a new job to the database.
    """
    st.header("Add New Job")
    companies = session.query(Company).all()
    company_names = [company.name for company in companies]
    selected_company = input_selectbox("Select Company", company_names)

    job_type = input_text("Job Type")
    status = input_selectbox("Status", ["pending", "in progress", "complete"])

    if st.button("Add Job"):
        company = session.query(Company).filter_by(name=selected_company).first()
        if company and job_type:
            new_job = Job(
                job_type=job_type,
                status=status,
                company=company
            )
            session.add(new_job)
            session.commit()
            show_success("Job added successfully!")
        else:
            show_error("Please provide all required fields.")

def view_jobs():
    """
    Provides a way to view job.
    """
    st.header("View Jobs")
    jobs = session.query(Job).all()
    data = [{
        "ID": job.id,
        "Job Type": job.job_type,
        "Status": job.status,
        "Company": job.company.name,
        "Created At": job.created_at
    } for job in jobs]
    show_table(data)

def update_job_status():
    """
    Provides a form to aupdate status to the database.
    """
    st.header("Update Job Status")
    jobs = session.query(Job).filter(Job.status != 'complete').all()
    job_list = [f"{job.id} - {job.job_type} ({job.company.name})" for job in jobs]
    selected = st.selectbox("Select Job", job_list)

    if selected:
        job_id = int(selected.split(" - ")[0])
        job = session.query(Job).filter_by(id=job_id).first()
        if job:
            new_status = input_selectbox("New Status", ["pending", "in progress", "complete"], index=["pending", "in progress", "complete"].index(job.status))
            if st.button("Update Status"):
                job.status = new_status
                session.commit()
                show_success("Job status updated successfully!")
                if new_status == "complete":
                    generate_and_save_invoice(job)
        else:
            show_error("Job not found.")

def generate_and_save_invoice(job):
    """
    Provides a form save invoice to the database.
    """
    st.info("Generating invoice...")
    invoice_details = {
        "Invoice ID": job.id,
        "Company": job.company.name,
        "Job Type": job.job_type,
        "Payment Terms": job.company.payment_terms,
        "Amount": 100.0  # Placeholder amount
    }
    pdf_path = os.path.join("invoices", f"invoice_{job.id}.pdf")
    os.makedirs("invoices", exist_ok=True)
    generate_invoice_pdf(invoice_details, pdf_path)

    new_invoice = Invoice(
        job=job,
        amount=invoice_details["Amount"],
        pdf_path=pdf_path
    )
    session.add(new_invoice)
    session.commit()
    st.success("Invoice generated and saved.")

def job_management():
    """
    Provides a way to manage jobs.
    """
    st.sidebar.subheader("Job Management")
    action = st.sidebar.selectbox("Action", ["Add Job", "View Jobs", "Update Job Status"])

    if action == "Add Job":
        add_job()
    elif action == "View Jobs":
        view_jobs()
    elif action == "Update Job Status":
        update_job_status()
