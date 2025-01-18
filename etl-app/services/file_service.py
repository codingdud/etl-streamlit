import os
import requests
import pandas as pd
from urllib.parse import urlparse
import streamlit as st  # Add this import statement
from constants import TEMP_DOWNLOAD_DIR

class FileService:
    def download_file(self, url):
        st.toast(f"Attempting to download file from URL: {url}")
        response = requests.get(url, stream=True, timeout=10)  # 10 seconds timeout
        st.toast(f"Status Code: {response.status_code}")
        response.raise_for_status()
        
        filename = os.path.basename(urlparse(url).path)
        st.toast(f"Filename determined from URL: {filename}")
        filepath = os.path.join(TEMP_DOWNLOAD_DIR, filename)
        
        st.toast(f"File will be saved to: {filepath}")
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        st.toast("File downloaded successfully")
        return filepath
    
    def load_file(self, filepath):
        st.toast(f"Attempting to load file: {filepath}")
        ext = os.path.splitext(filepath)[1].lower()
        st.toast(f"File extension: {ext}")
        
        try:
            if ext == '.csv':
                return pd.read_csv(filepath)
            elif ext in ['.xlsx', '.xls']:
                return pd.read_excel(filepath)
            elif ext == '.xml':
                return pd.read_xml(filepath)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            raise

