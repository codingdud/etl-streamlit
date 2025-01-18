import streamlit as st
import requests

class SearchService:
    def __init__(self):
        self.headers = {"Ocp-Apim-Subscription-Key": st.secrets["BING_API_KEY"]}
        self.endpoint = st.secrets["BING_ENDPOINT"]
        self.supported_extensions = st.secrets.get("SUPPORTED_EXTENSIONS", ["xml", "xlsx", "csv"])
    
    def search_files(self, query, file_types=None):
        if file_types is None:
            file_types = self.supported_extensions
            
        file_query = " OR ".join([f"filetype:{ft}" for ft in file_types])
        full_query = f"{query} ({file_query})"
        
        params = {
            "q": full_query,
            "count": 50,
            "responseFilter": "webPages"
        }
        
        try:
            response = requests.get(self.endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get("webPages", {}).get("value", [])
        except requests.exceptions.RequestException as e:
            st.error(f"Search API error: {str(e)}")
            return []
