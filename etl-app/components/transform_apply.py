import streamlit as st
import pandas as pd
from data.data_transformer import DataTransformer

def show_transformations_and_apply(df, transformed_num_rows):
    # Initialize the DataTransformer
    transformer = DataTransformer()

    # Sidebar elements for transformation options
    st.sidebar.write("### Available Transformations")

    # Retrieve available transformations from the transformer
    transformations = transformer.get_available_transformations()
    selected_transform = st.sidebar.selectbox(
        "Select transformation",
        list(transformations.keys())
    )

    # Options for column selection
    columns = df.columns.tolist()
    selected_column = st.sidebar.selectbox(
        "Select column to transform (if applicable)",
        ["None"] + columns
    )

    # Configuration for specific transformations
    fill_value = None
    if selected_transform == "Fill NA":
        if selected_column != "None":
            fill_value = st.sidebar.number_input("Fill value", value=0)

    # Separate option for dropping a column
    column_to_drop = None
    if selected_transform == "Drop Column":
        column_to_drop = st.sidebar.selectbox("Select column to drop", columns)
        if selected_transform == "Drop Column" and column_to_drop!="None":
            # Start with the most recent `current_df`
            if 'current_df' in st.session_state:
                base_df = st.session_state['current_df'].copy()
            else:
                base_df = df.copy()  # Fallback to the provided DataFrame
            base_df = transformer.drop_column(base_df, column=column_to_drop)
            # Display the transformed DataFrame
            st.write("### Transformed Data Preview")
            st.dataframe(base_df.head(transformed_num_rows))
            st.write(f"Total rows: {len(base_df)}")

    # Option to filter data by a specific value
    filter_column = st.sidebar.selectbox("Select column to filter", ["None"] + columns)
    if filter_column != "None":
        filter_value = st.sidebar.text_input(f"Enter value to filter {filter_column}")
        if filter_value:
            # Filter the DataFrame and display the result
            df = df[df[filter_column].astype(str).str.contains(filter_value, na=False)]
            st.success(f"Filtered to {len(df)} rows based on {filter_column} containing '{filter_value}'.")

    # Apply the selected transformation when the button is clicked
    if st.sidebar.button("Apply Transformation"):
        try:
            # Start with the most recent `current_df`
            if 'current_df' in st.session_state:
                base_df = st.session_state['current_df'].copy()
            else:
                base_df = df.copy()  # Fallback to the provided DataFrame

            # Handle dropping a column
            if selected_transform == "Drop Column" and column_to_drop:
                base_df = transformer.drop_column(base_df, column=column_to_drop)
            else:
                kwargs = {'value': fill_value} if selected_transform == "Fill NA" else {}
                column = None if selected_column == "None" else selected_column

                # Apply the selected transformation
                base_df = transformer.transform_data(
                    base_df,
                    transformations[selected_transform],
                    column=column,
                    **kwargs
                )

            # Update session state with the transformed DataFrame
            st.session_state['transformed_df'] = base_df
            st.toast("Transformation applied successfully!", icon='😍')

            # Display the transformed DataFrame
            st.write("### Transformed Data Preview")
            st.dataframe(base_df.head(transformed_num_rows))
            st.write(f"Total rows: {len(base_df)}")
        except Exception as e:
            st.error(f"Error applying transformation: {str(e)}")

    # Button to save the transformations and make them permanent
    if st.button("Save Transformations"):
        if 'transformed_df' in st.session_state:
            st.session_state['current_df'] = st.session_state['transformed_df'].copy()
            st.toast("Transformations saved successfully!", icon='😍')
