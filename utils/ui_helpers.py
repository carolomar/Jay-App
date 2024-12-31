# utils/ui_helpers.py

import streamlit as st

def input_text(label, default=''):
    return st.text_input(label, value=default)

def input_selectbox(label, options, index=0):
    return st.selectbox(label, options, index=index)

def input_date(label):
    return st.date_input(label)

def show_table(data):
    st.table(data)

def show_dataframe(df):
    st.dataframe(df)

def show_success(message):
    st.success(message)

def show_error(message):
    st.error(message)

def download_button(label, data, file_name):
    return st.download_button(label, data, file_name)
