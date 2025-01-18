import pandas as pd

class DataTransformer:
    @staticmethod
    def get_available_transformations():
        return {
            "Drop NA": "drop_na",
            "Fill NA": "fill_na",
            "Convert to Datetime": "to_datetime",
            "Convert to Numeric": "to_numeric",
            "Convert Binary/Categorical to Numeric": "to_numeric_category",  # New transformation
            "Drop Duplicates": "drop_duplicates",
            "Add New Column": "add_new_column",
            "Drop Column": "drop_column"
        }
    
    def transform_data(self, df, transformation, column=None, **kwargs):
        if hasattr(self, transformation):
            transform_func = getattr(self, transformation)
            return transform_func(df, column, **kwargs)
        return df
    
    def drop_na(self, df, column=None, **kwargs):
        return df.dropna(subset=[column] if column else None)
    
    def fill_na(self, df, column=None, fill_method=None, value=None, **kwargs):
        if column:
            if fill_method == "average":
                avg_value = df[column].mean()
                df[column] = df[column].fillna(avg_value)
            elif fill_method == "sum":
                sum_value = df[column].sum()
                df[column] = df[column].fillna(sum_value)
            elif fill_method == "row_value":
                df[column] = df[column].fillna(value)
            else:
                df[column] = df[column].fillna(value)
        else:
            df = df.fillna(value)
        return df

    def to_datetime(self, df, column, **kwargs):
        df[column] = pd.to_datetime(df[column], errors='coerce')
        return df
    
    def to_numeric(self, df, column, **kwargs):
        df[column] = pd.to_numeric(df[column], errors='coerce')
        return df

    def to_numeric_category(self, df, column, **kwargs):
        """Converts binary, ordinal, or nominal categorical data to numeric dynamically."""
        if not column or column not in df.columns:
            raise ValueError("A valid column name must be specified.")

        # Retrieve user-defined mapping, if provided
        mapping = kwargs.get("mapping")

        # Automatically generate mapping if not provided
        if not mapping:
            unique_values = df[column].dropna().unique()  # Exclude NaN values
            unique_values = sorted(unique_values)  # Ensure consistency in ordering
            
            # Detect the type of data
            if len(unique_values) == 2:  # Binary
                mapping = {unique_values[0]: 0, unique_values[1]: 1}
            else:
                # Determine if ordinal by checking for user-defined ordering in kwargs
                order = kwargs.get("order")
                if order:
                    # Ensure the provided order matches the unique values
                    if set(order) != set(unique_values):
                        raise ValueError("Provided order does not match unique column values.")
                    mapping = {category: idx for idx, category in enumerate(order, start=1)}
                else:
                    # Default to nominal mapping
                    mapping = {category: idx for idx, category in enumerate(unique_values)}

        # Apply the mapping
        df[column] = df[column].map(mapping)
        return df
    
    def drop_duplicates(self, df, column=None, **kwargs):
        return df.drop_duplicates(subset=[column] if column else None)
    
    def add_new_column(self, df, new_column_name, operation, column1=None, column2=None):
        if operation == "concat":
            df[new_column_name] = df[column1].astype(str) + df[column2].astype(str)
        elif operation == "concat_with_string":
            df[new_column_name] = df[column1].astype(str) + column2
        return df
    
    def drop_column(self, df, column=None, **kwargs):
        """Drops the specified column from the DataFrame."""
        if column and column in df.columns:
            df = df.drop(columns=[column])
        return df
