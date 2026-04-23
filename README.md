# Loan Recovery Performance Analysis Dashboard

## Objective
Analyze loan repayment behavior and identify factors affecting recovery rates to reduce defaults and improve financial performance. This professional, interactive dashboard visualizes key metrics (KPIs) and Risk Segmentation.

## Overview
High loan default rates present a significant problem in the banking sector. This project utilizes Data Analytics to uncover insights on customer reliability, helping prioritize high-risk segments. 

**This is a professional resume and GitHub-ready Data Analyst / Data Science portfolio project.**

## Features
- **Data Pipeline**: Synthetically generated, highly realistic Loan Data (`scripts/data_generator.py`) factoring in Income, Age, Debt-to-Income, etc.
- **Deep Data Analytics (12-Step Lifecycle)**: Included is a professional Jupyter Notebook (`notebooks/Loan_Recovery_Analysis.ipynb`) mapping out data cleaning, Exploratory Data Analysis (EDA), and Machine Learning (Logistic Regression).
- **Executive Summaries**: Slide outlines and Project reports stored in the `reports/` folder.
- **Interactive Dashboard** (Built with Python, Streamlit, Plotly):
  - **Overview Page:** KPIs (Recovery Rate, Default Rate) and dynamic interactive charts for Loan Portfolios.
  - **Risk Analysis Page:** Scatter charts, Heatmaps, and automated ML-ready Risk Segmentation.

## Key Insights Discovered
1. **Loan Type vs Recovery:** Personal Loans and Education loans show significantly higher default rates.
2. **Income vs Default:** Lower income combined with high loan amounts dramatically increases predictive default risk.
3. **Age Group Analysis:** Younger borrowers (under 30) represent higher risk due to shorter credit histories.

## How to Run This Project

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate the dataset (optional, already generated in `/data`):
   ```bash
   python scripts/data_generator.py
   ```
3. Run the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

*Built by a Data Analyst for the Banking Domain using Python, Pandas, and Streamlit.*
