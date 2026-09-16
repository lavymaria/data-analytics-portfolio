"""
eda.py

Reusable Exploratory Data Analysis utilities for analytics projects.

Author: Lavender Wakasa
Project: Telco Customer Churn Analysis
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


class EDAAnalyzer:
    """
    Reusable EDA toolkit.
    """

    def __init__(self, dataframe):
        self.df = dataframe

    # ==========================================================
    # DATASET OVERVIEW
    # ==========================================================

    def dataset_summary(self):
        """
        Generate high-level dataset summary.
        """

        summary = {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "missing_values": self.df.isnull().sum().sum(),
            "duplicates": self.df.duplicated().sum()
        }

        return summary

    def numerical_summary(self):
        """
        Return descriptive statistics for numeric columns.
        """

        return self.df.describe().T

    def categorical_summary(self):
        """
        Return descriptive summary for categorical columns.
        """

        return self.df.describe(include="object").T

    # ==========================================================
    # UNIVARIATE ANALYSIS
    # ==========================================================

    def plot_count(self, column, figsize=(8, 4)):
        """
        Plot countplot for categorical features.
        """

        plt.figure(figsize=figsize)

        sns.countplot(
            data=self.df,
            x=column
        )

        plt.title(f"{column.title()} Distribution")
        plt.tight_layout()
        plt.show()

    def category_percentages(self, column):
        """
        Return category percentages.
        """

        return round(
            self.df[column]
            .value_counts(normalize=True)
            * 100,
            2
        )

    def plot_histogram(
        self,
        column,
        bins=30,
        figsize=(8, 4)
    ):
        """
        Histogram with KDE.
        """

        plt.figure(figsize=figsize)

        sns.histplot(
            self.df[column],
            kde=True,
            bins=bins
        )

        plt.title(f"{column.title()} Distribution")
        plt.tight_layout()
        plt.show()

    def plot_boxplot(
        self,
        column,
        figsize=(8, 4)
    ):
        """
        Boxplot for outlier detection.
        """

        plt.figure(figsize=figsize)

        sns.boxplot(
            x=self.df[column]
        )

        plt.title(f"{column.title()} Boxplot")
        plt.tight_layout()
        plt.show()

    # ==========================================================
    # TARGET ANALYSIS
    # ==========================================================

    def target_distribution(self, target):
        """
        Return target counts and percentages.
        """

        counts = self.df[target].value_counts()

        percentages = round(
            self.df[target]
            .value_counts(normalize=True)
            * 100,
            2
        )

        return pd.DataFrame({
            "count": counts,
            "percentage": percentages
        })

    # ==========================================================
    # BIVARIATE ANALYSIS
    # ==========================================================

    def churn_rate(self, column, target="churn"):
        """
        Calculate churn rate by category.
        """

        return round(
            pd.crosstab(
                self.df[column],
                self.df[target],
                normalize="index"
            ) * 100,
            2
        )

    def plot_churn_by_category(
        self,
        column,
        target="churn",
        figsize=(8, 4)
    ):
        """
        Countplot segmented by target.
        """

        plt.figure(figsize=figsize)

        sns.countplot(
            data=self.df,
            x=column,
            hue=target
        )

        plt.title(f"{target.title()} by {column.title()}")
        plt.xticks(rotation=30)

        plt.tight_layout()
        plt.show()

    def plot_churn_boxplot(
        self,
        numerical_column,
        target="churn",
        figsize=(8, 4)
    ):
        """
        Boxplot of numeric feature against churn.
        """

        plt.figure(figsize=figsize)

        sns.boxplot(
            data=self.df,
            x=target,
            y=numerical_column
        )

        plt.title(
            f"{target.title()} vs {numerical_column.title()}"
        )

        plt.tight_layout()
        plt.show()

    # ==========================================================
    # CORRELATION ANALYSIS
    # ==========================================================

    def correlation_matrix(self):
        """
        Return correlation matrix.
        """

        numeric_df = self.df.select_dtypes(
            include=np.number
        )

        return numeric_df.corr()

    def plot_correlation_heatmap(
        self,
        figsize=(8, 6)
    ):
        """
        Correlation heatmap.
        """

        corr = self.correlation_matrix()

        plt.figure(figsize=figsize)

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f"
        )

        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.show()

    # ==========================================================
    # OUTLIER ANALYSIS
    # ==========================================================

    def outlier_summary(self, column):
        """
        IQR-based outlier summary.
        """

        q1 = self.df[column].quantile(0.25)
        q3 = self.df[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = self.df[
            (self.df[column] < lower_bound)
            | (self.df[column] > upper_bound)
        ]

        return {
            "column": column,
            "outlier_count": len(outliers),
            "outlier_percentage":
                round(
                    len(outliers)
                    / len(self.df)
                    * 100,
                    2
                )
        }

    # ==========================================================
    # FEATURE TYPE UTILITIES
    # ==========================================================

    def numerical_columns(self):
        """
        Return numeric columns.
        """

        return self.df.select_dtypes(
            include=np.number
        ).columns.tolist()

    def categorical_columns(self):
        """
        Return categorical columns.
        """

        return self.df.select_dtypes(
            exclude=np.number
        ).columns.tolist()