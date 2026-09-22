# src/evaluation.py

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


class ClassificationEvaluator:
    """
    Utilities for evaluating classification models.
    """

    @staticmethod
    def evaluate_predictions(y_true, y_pred):
        """
        Calculate standard classification metrics.
        """

        return {
            "Accuracy": accuracy_score(y_true, y_pred),
            "Precision": precision_score(y_true, y_pred),
            "Recall": recall_score(y_true, y_pred),
            "F1 Score": f1_score(y_true, y_pred)
        }

    @staticmethod
    def evaluate_model(model, X_test, y_test):
        """
        Evaluate a trained model.
        """

        predictions = model.predict(X_test)

        results = (
            ClassificationEvaluator
            .evaluate_predictions(
                y_test,
                predictions
            )
        )

        results["ROC-AUC"] = roc_auc_score(
            y_test,
            predictions
        )

        return results

    @staticmethod
    def classification_report_text(
        model,
        X_test,
        y_test
    ):
        """
        Generate classification report.
        """

        predictions = model.predict(X_test)

        return classification_report(
            y_test,
            predictions
        )

    @staticmethod
    def compare_models(results_dict):
        """
        Compare multiple models.
        """

        return (
            pd.DataFrame(results_dict)
            .T
            .sort_values(
                by="F1 Score",
                ascending=False
            )
        )
