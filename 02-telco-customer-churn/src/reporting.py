"""
Reporting Module
----------------
Business insights and executive reporting.
"""

import pandas as pd


class BusinessReportGenerator:

    @staticmethod
    def create_model_summary(
        comparison_df
    ):
        """
        Return best model.
        """

        best_model = (
            comparison_df
            .sort_values(
                by=["Recall", "F1 Score"],
                ascending=False
            )
            .iloc[0]
        )

        return best_model

    @staticmethod
    def generate_executive_summary():

        summary = pd.DataFrame({
            "Area": [
                "Customer Retention",
                "Contract Strategy",
                "Customer Success",
                "Marketing"
            ],
            "Recommendation": [
                "Target high-risk customers",
                "Promote long-term contracts",
                "Early intervention",
                "Personalized offers"
            ]
        })

        return summary

    @staticmethod
    def generate_business_recommendations():

        recommendations = pd.DataFrame({
            "Recommendation":[
                "Promote annual contracts",
                "Launch onboarding program",
                "Target high-risk accounts",
                "Review pricing strategy"
            ],
            "Expected Impact":[
                "Lower churn",
                "Improve retention",
                "Increase customer value",
                "Reduce churn drivers"
            ]
        })

        return recommendations

    @staticmethod
    def calculate_business_impact(
        customers_at_risk,
        retention_rate,
        average_customer_value
    ):

        retained_customers = (
            customers_at_risk
            * retention_rate
        )

        estimated_savings = (
            retained_customers
            * average_customer_value
        )

        return {
            "Customers At Risk":
            customers_at_risk,

            "Retention Rate":
            retention_rate,

            "Retained Customers":
            retained_customers,

            "Estimated Savings":
            estimated_savings
        }

    @staticmethod
    def create_risk_profile(
        df,
        group_column,
        target_column="churn"
    ):

        risk_profile = (
            df.groupby(group_column)
            [target_column]
            .mean()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        return risk_profile

    @staticmethod
    def export_report(
        executive_summary,
        recommendations,
        file_path
    ):

        with pd.ExcelWriter(
            file_path
        ) as writer:

            executive_summary.to_excel(
                writer,
                sheet_name="Executive Summary",
                index=False
            )

            recommendations.to_excel(
                writer,
                sheet_name="Recommendations",
                index=False
            )
