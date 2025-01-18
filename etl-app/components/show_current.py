import streamlit as st
import pandas as pd

def show_current_data_preview(df,current_num_rows):
    with st.sidebar:
        # Option to show/hide DataFrame structure
        st.write(f"Total rows: {len(df)}")
        show_structure = st.checkbox("Show Structure", value=False)
        if show_structure:
            st.write("### DataFrame Structure")
            st.write(df.dtypes)
        
    # Main content area
    st.write("### Current Data Preview")
    st.dataframe(df.head(current_num_rows))
