import os
import streamlit as st
import pandas as pd
from data.data_transformer import DataTransformer
from constants import TEMP_DOWNLOAD_DIR
from services.file_service import FileService
from components.show_current import show_current_data_preview
from components.transform_apply import show_transformations_and_apply

def show_transform_page():
    st.title("Transform Data")

    # Check if there are any files in the TEMP_DOWNLOAD_DIR
    available_files = [
        file for file in os.listdir(TEMP_DOWNLOAD_DIR)
        if os.path.isfile(os.path.join(TEMP_DOWNLOAD_DIR, file))
    ]

    if not available_files:
        st.warning("No files found in the temp_downloads directory. Please load a file from the Search & Extract page first.")
        return

    # Let the user select a file to load
    selected_file = st.selectbox(
        "Select a file to load",
        available_files,
        index=available_files.index(st.session_state.get("last_selected_file", available_files[0])) if "last_selected_file" in st.session_state else 0
    )

    # Construct the file path
    filepath = os.path.join(TEMP_DOWNLOAD_DIR, selected_file)

    # Load the file only if it's new or not loaded yet
    if (
        "loaded_filepath" not in st.session_state or
        st.session_state.loaded_filepath != filepath
    ):
        file_service = FileService()
        try:
            # Load the file into a DataFrame
            df = file_service.load_file(filepath)
            st.session_state['current_df'] = df
            st.session_state['loaded_filepath'] = filepath
            st.session_state['last_selected_file'] = selected_file
            st.toast(f"File {selected_file} loaded successfully!", icon="😻")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return
    else:
        # Retrieve the existing DataFrame from session state
        df = st.session_state['current_df']

    # Proceed with transformations if a DataFrame is loaded
    transformer = DataTransformer()

    # Sidebar for the number of rows to display
    with st.sidebar:
        current_num_rows = st.number_input(
            "Number of rows to display",
            min_value=1,
            max_value=len(df),
            value=st.session_state.get("current_num_rows", 10),  # Default to 10 or saved value
            key="current_num_rows"  # Save the number of rows persistently
        )

    # Show current data preview and transformation options
    show_current_data_preview(df, current_num_rows)
    show_transformations_and_apply(df, current_num_rows)
