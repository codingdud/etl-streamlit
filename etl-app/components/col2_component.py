import streamlit as st
from services.file_service import FileService

file_service = FileService()

def load_data_button(result):
    """Create a button to load data and handle file downloading and loading."""
    if st.button("Load Data", key=f"load_{result['url']}"):
        with st.spinner("Downloading and loading file..."):  # Spinner for loading data
            try:
                # Uncomment the file download and load operations when ready
                filepath = file_service.download_file(result['url'])
                st.write(f"File downloaded to: {filepath}")

                # Simulate data loading for demonstration purposes
                df = file_service.load_file(filepath)
                st.session_state['current_df'] = df

                st.toast(f"Data loaded successfully from {result['url']}")
                # For demonstration, use a sample DataFrame preview
                st.dataframe(df.head())
                st.write(f"Total rows: {len(df)}")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
                st.write(f"Exception Details: {repr(e)}")
