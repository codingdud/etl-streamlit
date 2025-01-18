# File: components/col1_component.py
import streamlit as st

def display_file_info(result):
    """Display the file name and URL in the first column."""
    st.write(f"**{result['name']}**")
    st.write(result['url'])
