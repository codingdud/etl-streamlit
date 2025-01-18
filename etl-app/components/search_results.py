import streamlit as st
from components.col1_component import display_file_info
from components.col2_component import load_data_button

def show_search_results():
    # Only show results if they exist in session state
    results = st.session_state.get('search_results', [])
    if results:
        st.write(f"Found {len(results)} results:")
        for result in results:
            col1, col2 = st.columns([3, 1])
            with col1:
                display_file_info(result)    
            with col2:
                load_data_button(result)
    else:
        st.info("No search results to display. Please perform a search.")
