"""
Feature Engineering Module
--------------------------
Reusable feature engineering functions for the
Telco Customer Churn project.
"""

from dataclasses import dataclass
import pandas as pd


# =====================================================
# Helper Functions
# =====================================================

def _count_yes_values(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    """
    Count the number of 'Yes' values across specified columns.
    """
    return df[columns].eq("Yes").sum(axis=1)


def _create_tenure_labels(
    series: pd.Series,
    bins: list[int],
    labels: list[str]
) -> pd.Series:
    """
    Convert numerical tenure into customer lifecycle groups.
    """
    return pd.cut(
        series,
        bins=bins,
        labels=labels,
        include_lowest=True
    )


def _create_quantile_bands(
    series: pd.Series,
    labels: list[str]
) -> pd.Series:
    """
    Create quantile-based categorical bands.
    """
    return pd.qcut(
        series,
        q=len(labels),
        labels=labels
    )


# =====================================================
# Main Feature Engineering Class
# =====================================================

@dataclass
class FeatureEngineer:
    """
    Encapsulates all feature engineering operations.
    """

    tenure_bins: list = None
    tenure_labels: list = None

    def __post_init__(self):

        if self.tenure_bins is None:
            self.tenure_bins = [0, 12, 24, 48, 72]

        if self.tenure_labels is None:
            self.tenure_labels = [
                "new",
                "developing",
                "established",
                "loyal"
            ]

    # -------------------------------------------------
    # Customer Lifecycle Features
    # -------------------------------------------------

    def create_tenure_group(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df = df.copy()

        df["tenure_group"] = _create_tenure_labels(
            df["tenure"],
            self.tenure_bins,
            self.tenure_labels
        )

        return df

    # -------------------------------------------------
    # Pricing Features
    # -------------------------------------------------

    def create_charge_band(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df = df.copy()

        df["charge_band"] = _create_quantile_bands(
            df["monthlycharges"],
            ["low", "medium", "high", "premium"]
        )

        return df

    def create_charge_per_month_feature(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df = df.copy()

        df["charge_per_month_tenure"] = (
            df["totalcharges"] /
            (df["tenure"] + 1)
        )

        return df

    # -------------------------------------------------
    # Service Features
    # -------------------------------------------------

    def create_service_count(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df = df.copy()

        service_cols = [
            "onlinesecurity",
            "onlinebackup",
            "deviceprotection",
            "techsupport",
            "streamingtv",
            "streamingmovies"
        ]

        df["num_additional_services"] = (
            _count_yes_values(
                df,
                service_cols
            )
        )

        return df

    # -------------------------------------------------
    # Encoding
    # -------------------------------------------------

    
    def encode_features(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        return pd.get_dummies(
            df,
            drop_first=True
        )

    


    # -------------------------------------------------
    # Workflow Method
    # -------------------------------------------------

    def transform(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Run the complete feature engineering pipeline.
        """

        df = self.create_tenure_group(df)
        df = self.create_charge_band(df)
        df = self.create_charge_per_month_feature(df)
        df = self.create_service_count(df)

        return df
