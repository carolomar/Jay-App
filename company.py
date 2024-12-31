# company.py

import streamlit as st
from database import session, Company
from utils.ui_helpers import input_text, show_table, show_success, show_error

def add_company():
    """
    Provides a form to add a new company to the database.
    """
    st.header("Add New Company")
    name = input_text("Company Name")
    location = input_text("Location")
    payment_terms = input_text("Payment Terms")
    contact_info = input_text("Contact Information")

    if st.button("Add Company"):
        if name:
            new_company = Company(
                name=name,
                location=location,
                payment_terms=payment_terms,
                contact_info=contact_info
            )
            session.add(new_company)
            session.commit()
            show_success("Company added successfully!")
        else:
            show_error("Company name is required.")

def view_companies():
    """
    Provides a form to view company.
    """
    st.header("View Companies")
    companies = session.query(Company).all()
    data = [{
        "ID": company.id,
        "Name": company.name,
        "Location": company.location,
        "Payment Terms": company.payment_terms,
        "Contact Info": company.contact_info
    } for company in companies]
    show_table(data)

def update_company():
    """
    Provides a form to update a new company to the database.
    """
    st.header("Update Company")
    companies = session.query(Company).all()
    company_names = [company.name for company in companies]
    selected = st.selectbox("Select Company to Update", company_names)
    company = session.query(Company).filter_by(name=selected).first()

    if company:
        name = input_text("Company Name", company.name)
        location = input_text("Location", company.location)
        payment_terms = input_text("Payment Terms", company.payment_terms)
        contact_info = input_text("Contact Information", company.contact_info)

        if st.button("Update Company"):
            company.name = name
            company.location = location
            company.payment_terms = payment_terms
            company.contact_info = contact_info
            session.commit()
            show_success("Company updated successfully!")
    else:
        show_error("Company not found.")

def delete_company():
    """
    Provides a form to delete a new company to the database.
    """
    st.header("Delete Company")
    companies = session.query(Company).all()
    company_names = [company.name for company in companies]
    selected = st.selectbox("Select Company to Delete", company_names)

    if st.button("Delete Company"):
        company = session.query(Company).filter_by(name=selected).first()
        if company:
            session.delete(company)
            session.commit()
            show_success("Company deleted successfully!")
        else:
            show_error("Company not found.")

def company_crud():
    """
    Provides a form to choose company.
    """
    st.sidebar.subheader("Company Management")
    action = st.sidebar.selectbox("Action", ["Add Company", "View Companies", "Update Company", "Delete Company"])

    if action == "Add Company":
        add_company()
    elif action == "View Companies":
        view_companies()
    elif action == "Update Company":
        update_company()
    elif action == "Delete Company":
        delete_company()
