"""
modeling.py

Functions and classes for training, evaluating,
and comparing customer churn prediction models.
"""

# =====================================================
# Imports
# =====================================================

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

# Optional XGBoost
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


# =====================================================
# Functions
# =====================================================

def prepare_train_test(
    X,
    y,
    test_size=0.2,
    random_state=42
):
    """
    Split dataset into training and testing sets.
    """

    return train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )


def scale_features(X_train, X_test):
    """
    Scale numerical features.
    """

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler


def evaluate_predictions(y_true, y_pred):
    """
    Calculate common classification metrics.
    """

    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1 Score": f1_score(y_true, y_pred)
    }


def save_model(model, filepath):
    """
    Save trained model.
    """

    joblib.dump(model, filepath)


def load_model(filepath):
    """
    Load trained model.
    """

    return joblib.load(filepath)


# =====================================================
# Base Model Trainer Class
# =====================================================

class ModelTrainer:
    """
    Parent class for machine learning models.
    """

    def __init__(self):
        self.model = None

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):

        predictions = self.predict(X_test)

        metrics = evaluate_predictions(
            y_test,
            predictions
        )

        return metrics


# =====================================================
# Logistic Regression
# =====================================================

class LogisticRegressionTrainer(ModelTrainer):

    def __init__(
        self,
        max_iter=1000,
        random_state=42
    ):

        super().__init__()

        self.model = LogisticRegression(
            max_iter=max_iter,
            random_state=random_state
        )


# =====================================================
# Random Forest
# =====================================================

class RandomForestTrainer(ModelTrainer):

    def __init__(
        self,
        n_estimators=200,
        max_depth=10,
        random_state=42
    ):

        super().__init__()

        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )


# =====================================================
# Gradient Boosting
# =====================================================

class GradientBoostingTrainer(ModelTrainer):

    def __init__(
        self,
        random_state=42
    ):

        super().__init__()

        self.model = GradientBoostingClassifier(
            random_state=random_state
        )


# =====================================================
# XGBoost
# =====================================================

class XGBoostTrainer(ModelTrainer):

    def __init__(
        self,
        random_state=42
    ):

        if not XGBOOST_AVAILABLE:
            raise ImportError(
                "XGBoost is not installed."
            )

        super().__init__()

        self.model = XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=random_state
        )


# =====================================================
# Model Comparison Class
# =====================================================

class ModelComparer:
    """
    Compare multiple models.
    """

    def __init__(self):
        self.results = []

    def add_result(self, model_name, metrics):

        row = {
            "Model": model_name,
            "Accuracy": metrics["Accuracy"],
            "Precision": metrics["Precision"],
            "Recall": metrics["Recall"],
            "F1 Score": metrics["F1 Score"]
        }

        self.results.append(row)

    def get_results(self):
        return pd.DataFrame(self.results)