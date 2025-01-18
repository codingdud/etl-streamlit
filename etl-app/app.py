import os
import streamlit as st
from utils.logger import setup_logging
from screens.search_page import show_search_page
from screens.transform_page import show_transform_page
from screens.math_solve import show_math_solver

# Create logger for this module
logger = setup_logging(__name__)

# Initialize application settings
def init_app():
    """
    Initialize application settings and perform pre-flight checks.
    """
    # Check for required secrets
    required_secrets = ['BING_API_KEY', 'BING_ENDPOINT']
    for secret in required_secrets:
        if secret not in st.secrets:
            logger.error(f"Missing required secret: {secret}")
            st.error(f"Missing required secret: {secret}")
            st.stop()
    
    # Create temp directory
    temp_dir = st.secrets.get('TEMP_DOWNLOAD_DIR', 'temp_downloads')
    try:
        os.makedirs(temp_dir, exist_ok=True)
        logger.info(f"Temporary download directory created: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to create temporary download directory: {e}")
        st.error(f"Failed to create temporary download directory: {e}")
        st.stop()

# Main application
def main():
    try:
        # Configure Streamlit page
        st.set_page_config(page_title="File ETL App", layout="wide")
        logger.info("Streamlit page configuration set")

        # Initialize app settings
        init_app()

        # Navigation sidebar
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Select Page", ["Search & Extract", "Transform", "AI"])
        logger.info(f"Page selected: {page}")

        # Route to appropriate page based on selection
        if page == "Search & Extract":
            logger.info("Navigating to Search & Extract page")
            show_search_page()
        elif page == "Transform":
            logger.info("Navigating to Transform page")
            show_transform_page()
        else:
            logger.info("Navigating to AI page")
            show_math_solver()

    except Exception as e:
        # Log any unexpected errors
        logger.exception("An unexpected error occurred in the main application")
        st.error(f"An unexpected error occurred: {e}")

# Entry point of the application
if __name__ == "__main__":
    main()