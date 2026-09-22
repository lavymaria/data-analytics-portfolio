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
