# File: pages/search_page.py
import streamlit as st
from components.search_inputs import show_search_inputs
from components.search_results import show_search_results

def show_search_page():
    st.title("Search & Extract Data Files")
    
    show_search_inputs()  # Get search inputs from the sidebar
    show_search_results()  # Display search results
