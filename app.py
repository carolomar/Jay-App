# app.py

import streamlit as st
from company import company_crud
from job import job_management
from invoice import invoice_management
from report import reporting
from database import init_db

# Initialize the database
init_db()

# Set Streamlit page configuration
st.set_page_config(page_title="Janitorial Company App", layout="wide")

def main():
    st.title("Janitorial Company Management App")

    # Sidebar Navigation
    menu = ["Home", "Companies", "Jobs", "Invoices", "Reports"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Home":
        st.subheader("Welcome to the Janitorial Company Management App")
        st.write("Use the sidebar to navigate through different sections.")
    elif choice == "Companies":
        company_crud()
    elif choice == "Jobs":
        job_management()
    elif choice == "Invoices":
        invoice_management()
    elif choice == "Reports":
        reporting()
    else:
        st.error("Invalid Selection")

if __name__ == "__main__":
    main()
