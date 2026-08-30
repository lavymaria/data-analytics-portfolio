# Exploring the Relationship Between Internet Usage, Education, and Economic Growth in Africa (2000–2024)

## Project Overview

This project investigates whether internet penetration and secondary school enrollment help explain economic growth across African countries between 2000 and 2024.

Using data from the World Bank, the analysis combines exploratory data analysis (EDA), correlation analysis, and multiple linear regression to assess the relationship between:

- GDP Growth
- Internet Usage
- Secondary School Enrollment

The project aims to answer the following research question:

> To what extent do internet usage and secondary school enrollment explain variations in GDP growth across African countries?

Based on a final dataset of 1,109 observations, the findings suggest that educational attainment is a much stronger predictor of economic growth than internet usage alone.



## Project Structure

```text
world-bank-project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_statistical_analysis.ipynb
│
├── reports/
│   └── Project_Report.pdf
│
├── visuals/
│   ├── gdp_distribution.png
│   ├── correlation_heatmap.png
│   ├── actual_vs_predicted.png
│   └── residual_distribution.png
│
└── README.md
```



## Dataset

The dataset contains:

- 1,134 observations
- Multiple African countries
- Annual data from 2000 to 2024

### Variables

| Variable | Description |
|-----------|------------|
| GDP_Growth | Annual GDP growth rate |
| Internet_Usage | Percentage of individuals using the internet |
| Secondary_Enrollment | Gross secondary school enrollment rate |
| Country | Country name |
| Country_Code | Country identifier |
| Year | Observation year |

Data quality checks revealed only 25 missing values in Secondary Enrollment. After removing incomplete records, 1,109 observations were retained for analysis.



## Tools & Technologies

- Python
- Pandas
- NumPy
- Seaborn
- Matplotlib
- Statsmodels
- Jupyter Notebook
- VS Code



## Exploratory Data Analysis

The EDA phase focused on understanding:

- Variable distributions
- Time-series trends
- Country-level comparisons
- Outliers and anomalies

### Key Findings

- GDP Growth displayed substantial variation across countries and years.
- Internet usage increased steadily across Africa over the study period.
- Secondary school enrollment showed sustained growth in many countries.
- Countries such as Libya, Algeria, and South Africa recorded high enrollment levels.
- Seychelles, Morocco, and Mauritius recorded among the highest average GDP growth rates.



## Correlation Analysis

Pearson correlation coefficients were calculated to measure the strength of relationships between variables.

| Variables | Correlation (r) |
|------------|------------|
| GDP Growth vs Secondary Enrollment | 0.607 |
| GDP Growth vs Internet Usage | -0.122 |
| Internet Usage vs Secondary Enrollment | -0.107 |

### Interpretation

- Secondary enrollment exhibited a moderately strong positive relationship with GDP growth.
- Internet usage showed only a weak relationship with GDP growth.
- Education emerged as the strongest contributor among the variables studied.



## Regression Analysis

The following multiple linear regression model was estimated:

GDP Growth = β₀ + β₁(Internet Usage) + β₂(Secondary Enrollment)

### Model Performance

- R² = 0.372
- Model statistically significant (p < 0.001)

This indicates that approximately 37.2% of the variation in GDP growth can be explained by internet usage and secondary enrollment. 

### Regression Results

| Variable | Coefficient | P-value |
|-----------|------------|----------|
| Secondary Enrollment | 0.490 | < 0.001 |
| Internet Usage | -0.179 | 0.017 |

### Interpretation

**Secondary Enrollment**

- Strong positive predictor of GDP growth.
- A one-point increase in enrollment is associated with approximately a 0.49-point increase in GDP growth.

**Internet Usage**

- Statistically significant but weak negative coefficient.
- Likely reflects omitted variables, structural differences between countries, or limitations in the dataset rather than a causal effect.



## Model Diagnostics

Model evaluation included:

- Actual vs Predicted GDP Growth
- Residual Distribution Analysis

### Findings

- Predictions aligned reasonably well with moderate GDP growth observations.
- The model underestimated extreme high-growth cases.
- Residuals were approximately normally distributed with slight positive skewness.
- Some outliers remained, indicating additional explanatory variables may improve predictive performance. 



## Key Insights

✅ Secondary education is strongly associated with economic growth.

✅ Educational attainment is a stronger predictor of GDP growth than internet access.

✅ Internet connectivity alone does not fully explain economic performance.

✅ Human capital development remains a critical factor for long-term economic progress.

✅ Additional variables such as governance, investment, trade, and political stability would likely improve future models.



## Skills Demonstrated

- Data Cleaning and Preparation
- Exploratory Data Analysis (EDA)
- Statistical Analysis
- Correlation Analysis
- Multiple Linear Regression
- Data Visualization
- Economic Data Interpretation
- Python for Data Analytics





## Future Improvements

Potential enhancements for future iterations include:

- Incorporating inflation indicators
- Foreign direct investment (FDI) data
- Governance and political stability metrics
- Infrastructure expenditure
- Panel data regression techniques
- Machine learning forecasting models



## Author

Lavender Wakasa: Data Analyst and Predictictive Analysis Expert

Created as part of a portfolio demonstrating practical skills in:

- Data Analysis
- Statistical Modelling
- Economic Research
- Python Programming
- Data Storytelling