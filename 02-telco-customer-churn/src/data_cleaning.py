# src/data_cleaning.py

import pandas as pd


# ==================================================
# UTILITY FUNCTIONS
# ==================================================

def dataset_summary(df):
    """
    Return basic dataset information.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist()
    }


def data_type_summary(df):
    """
    Return datatype information for all columns.
    """

    return pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.values
    })


def check_duplicates(df):
    """
    Count duplicate records.
    """

    return df.duplicated().sum()


def missing_value_summary(df):
    """
    Return missing value counts and percentages.
    """

    missing_count = df.isnull().sum()

    missing_percent = (
        missing_count / len(df) * 100
    ).round(2)

    return pd.DataFrame({
        "Missing Count": missing_count,
        "Missing Percentage": missing_percent
    }).sort_values(
        by="Missing Percentage",
        ascending=False
    )


# ==================================================
# DATA CLEANER CLASS
# ==================================================

class DataCleaner:
    """
    Collection of cleaning methods that can be
    chained together.
    """

    def __init__(self, df):
        self.df = df.copy()

    def standardize_column_names(self):
        """
        Convert column names to snake_case.
        """

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return self

    def remove_duplicates(self):
        """
        Remove duplicate rows.
        """

        self.df = self.df.drop_duplicates()

        return self

    def convert_total_charges(self):
        """
        Example method for Telco dataset.
        Convert TotalCharges to numeric.
        """

        if "totalcharges" in self.df.columns:
            self.df["totalcharges"] = pd.to_numeric(
                self.df["totalcharges"],
                errors="coerce"
            )

        if "TotalCharges" in self.df.columns:
            self.df["TotalCharges"] = pd.to_numeric(
                self.df["TotalCharges"],
                errors="coerce"
            )

        return self

    def drop_missing_rows(self):
        """
        Drop rows with missing values.
        """

        self.df = self.df.dropna()

        return self

    def fill_missing_values(self, value=0):
        """
        Fill missing values with a specified value.
        """

        self.df = self.df.fillna(value)

        return self

    def get_dataframe(self):
        """
        Return cleaned dataframe.
        """

        return self.df