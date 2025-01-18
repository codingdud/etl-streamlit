import streamlit as st
from services.search_service import SearchService
from constants import SUPPORTED_EXTENSIONS

def show_search_inputs():
    search_service = SearchService()
    # Input fields for search
    query = st.text_input("Enter your search query:")
    file_types = st.sidebar.multiselect("Select file types:", options=SUPPORTED_EXTENSIONS if SUPPORTED_EXTENSIONS else ['.csv', '.xlsx', '.xml'])

    if st.button("Search"):
        with st.spinner("Searching for files..."):  # Spinner for the search operation
            try:
                results = search_service.search_files(query, file_types)
                if results:
                    st.session_state.search_results = results  # Store results in session state
                    st.success(f"Found {len(results)} results.")
                else:
                    st.session_state.search_results = []  # Clear results if none found
                    st.warning("No files found matching your criteria.")
            except Exception as e:
                st.error(f"Error during search: {str(e)}")
