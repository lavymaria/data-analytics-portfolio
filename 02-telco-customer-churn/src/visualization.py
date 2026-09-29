# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    confusion_matrix,
    RocCurveDisplay
)


class ClassificationVisualizer:
    """
    Visualization utilities for classification models.
    """

    @staticmethod
    def plot_confusion_matrix(
        model,
        X_test,
        y_test,
        title="Confusion Matrix"
    ):

        predictions = model.predict(X_test)

        cm = confusion_matrix(
            y_test,
            predictions
        )

        plt.figure(figsize=(6, 4))

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues"
        )

        plt.title(title)
        plt.xlabel("Predicted")
        plt.ylabel("Actual")

        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_roc_curve(
        model,
        X_test,
        y_test,
        title="ROC Curve"
    ):

        RocCurveDisplay.from_estimator(
            model,
            X_test,
            y_test
        )

        plt.title(title)

        plt.tight_layout()
        plt.show()


    @staticmethod
    def model_comparison_chart(
        comparison_df,
        metrics=None
    ):

        if metrics is None:

            metrics = [
                "Accuracy",
                "Precision",
                "Recall",
                "F1 Score",
                "ROC-AUC"
            ]

        comparison_df.set_index(
            "Model"
        )[metrics].plot(
            kind="bar",
            figsize=(10, 6)
        )

        plt.title(
            "Model Performance Comparison"
        )

        plt.ylabel("Score")

        plt.tight_layout()

        plt.show()


"""
Visualization Module
--------------------
Reusable plots for EDA, model evaluation,
and business reporting.
"""

import matplotlib.pyplot as plt
import seaborn as sns


class EDAVisualizer:

    @staticmethod
    def plot_target_distribution(
        df,
        target_column
    ):

        plt.figure(figsize=(6,4))

        sns.countplot(
            data=df,
            x=target_column
        )

        plt.title(
            f"{target_column} Distribution"
        )

        plt.show()

    @staticmethod
    def plot_numeric_distribution(
        df,
        column
    ):

        plt.figure(figsize=(8,5))

        sns.histplot(
            df[column],
            kde=True
        )

        plt.title(column)
        plt.show()

    @staticmethod
    def correlation_heatmap(df):

        plt.figure(figsize=(12,8))

        sns.heatmap(
            df.corr(numeric_only=True),
            cmap="coolwarm",
            annot=False
        )

        plt.title(
            "Correlation Matrix"
        )

        plt.show()


class ModelVisualizer:

    @staticmethod
    def plot_feature_importance(
        feature_importance_df,
        top_n=10
    ):
        top_features = (
            feature_importance_df
            .sort_values(
                by="Importance",
                ascending=False
            )
            .head(top_n)
        )

        plt.figure(figsize=(10,6))

        sns.barplot(
            data=top_features,
            x="Importance",
            y="Feature"
        )

        plt.title(
            "Top Feature Importance"
        )

        plt.show()

    @staticmethod
    def plot_model_comparison(
        comparison_df,
        metric="Recall"
    ):

        plt.figure(figsize=(10,5))

        sns.barplot(
            data=comparison_df,
            x="Model",
            y=metric
        )

        plt.title(
            f"Model Comparison ({metric})"
        )

        plt.xticks(rotation=45)

        plt.show()


class BusinessVisualizer:

    @staticmethod
    def plot_risk_segments(
        segment_df,
        segment_column,
        target_column
    ):

        risk_data = (
            segment_df
            .groupby(segment_column)[target_column]
            .mean()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        plt.figure(figsize=(10,5))

        sns.barplot(
            data=risk_data,
            x=segment_column,
            y=target_column
        )

        plt.title(
            f"Churn Rate by {segment_column}"
        )

        plt.xticks(rotation=45)

        plt.show()

    @staticmethod
    def plot_business_impact(
        impact_df
    ):

        plt.figure(figsize=(8,5))

        sns.barplot(
            data=impact_df,
            x="Category",
            y="Value"
        )

        plt.title(
            "Estimated Business Impact"
        )

        plt.show()
