import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(page_title="Loan Recovery Dashboard", layout="wide", page_icon="🏦")

# Title and Description
st.title("🏦 Loan Recovery Performance Dashboard")
st.markdown("Analyze loan repayment behavior and identify factors affecting recovery rates to reduce defaults and improve financial performance.")

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('loan_recovery_dataset.csv')
        # Clean duplicate/null values just for the dashboard to show clean data
        df.drop_duplicates(inplace=True)
        if 'Customer_Age' in df.columns:
            df['Customer_Age'] = df['Customer_Age'].fillna(df['Customer_Age'].median())
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Dataset not found. Please run `python scripts/data_generator.py` first to generate the dataset.")
    st.stop()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview Page", "Risk Analysis Page"])

if page == "Overview Page":
    st.header("Overview KPIs")
    
    # Calculate KPIs
    total_loans = len(df)
    total_disbursed = df['Loan_Amount'].sum()
    total_recovered = df['Recovery_Amount'].sum()
    recovery_rate = (total_recovered / total_disbursed) * 100
    
    default_count = len(df[df['Recovery_Status'] == 'Default'])
    default_rate = (default_count / total_loans) * 100
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Loans", f"{total_loans:,}")
    with col2:
        st.metric("Total Disbursed", f"₹{total_disbursed / 1e7:,.2f} Cr")
    with col3:
        st.metric("Total Recovered", f"₹{total_recovered / 1e7:,.2f} Cr")
    with col4:
        st.metric("Default Rate", f"{default_rate:.2f}%")
        
    st.markdown("---")
    
    # Overview Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Donut Chart for Loan Status
        fig_status = px.pie(
            df, names='Recovery_Status', title="Portfolio Status (Recovered vs Default)",
            color='Recovery_Status', color_discrete_map={'Recovered': '#2ecc71', 'Default': '#e74c3c'},
            hole=0.4
        )
        st.plotly_chart(fig_status, width='stretch')
        
    with col_chart2:
        # Bar Chart for Loan Volume by Type
        type_counts = df['Loan_Type'].value_counts().reset_index()
        type_counts.columns = ['Loan_Type', 'Count']
        fig_type = px.bar(
            type_counts, x='Loan_Type', y='Count', title="Loan Volume by Type",
            color='Loan_Type', color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_type, width='stretch')
        
    # Recovery Rate by Loan Type
    st.subheader("Recovery Analysis by Loan Type")
    rec_type = df.groupby('Loan_Type').apply(
        lambda x: (x['Recovery_Amount'].sum() / x['Loan_Amount'].sum()) * 100
    ).reset_index(name='Recovery_Rate_Pct').sort_values('Recovery_Rate_Pct', ascending=False)
    
    fig_rec = px.bar(
        rec_type, x='Loan_Type', y='Recovery_Rate_Pct', title="Average Recovery Rate (%) by Loan Portfolio",
        text=rec_type['Recovery_Rate_Pct'].apply(lambda x: f"{x:.1f}%"),
        color='Recovery_Rate_Pct', color_continuous_scale='Viridis'
    )
    fig_rec.update_traces(textposition='outside')
    fig_rec.update_layout(yaxis_range=[0, 110])
    st.plotly_chart(fig_rec, width='stretch')

elif page == "Risk Analysis Page":
    st.header("Risk Segmentation & Predictive Factors")
    
    # 1. Income vs Loan Amount with Status
    st.subheader("Income vs. Loan Amount by Default Status")
    fig_scatter = px.scatter(
        df, x='Income', y='Loan_Amount', color='Recovery_Status',
        color_discrete_map={'Recovered': '#2ecc71', 'Default': '#e74c3c'},
        opacity=0.6, title="Borrower Income vs Disbursement mapping Defaults"
    )
    st.plotly_chart(fig_scatter, width='stretch')
    
    # 2. Risk Segments
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Automated Risk Segmentation")
        risk_counts = df['Risk_Segment'].value_counts().reset_index()
        risk_counts.columns = ['Risk_Segment', 'Count']
        fig_risk = px.pie(
            risk_counts, names='Risk_Segment', values='Count', hole=0.3,
            color='Risk_Segment', color_discrete_map={'Low Risk': '#2ecc71', 'Medium Risk': '#f1c40f', 'High Risk': '#e74c3c'},
            title="Portfolio Risk Exposure"
        )
        st.plotly_chart(fig_risk, width='stretch')

    with col2:
        st.subheader("Default Probability by Risk Segment")
        risk_default = df.groupby('Risk_Segment').apply(
            lambda x: (x['Recovery_Status'] == 'Default').mean() * 100
        ).reset_index(name='Default_Rate_Pct')
        
        fig_risk_bar = px.bar(
            risk_default, x='Risk_Segment', y='Default_Rate_Pct',
            color='Risk_Segment', color_discrete_map={'Low Risk': '#2ecc71', 'Medium Risk': '#f1c40f', 'High Risk': '#e74c3c'},
            text=risk_default['Default_Rate_Pct'].apply(lambda x: f"{x:.1f}%")
        )
        fig_risk_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_risk_bar, width='stretch')
        
    st.subheader("Correlation Heatmap")
    st.markdown("Understanding which numerical features are highly correlated with Recovery Amounts and Default occurrences.")
    
    # Encode Default as numeric for correlation
    df_corr = df.copy()
    df_corr['Is_Default'] = (df_corr['Recovery_Status'] == 'Default').astype(int)
    num_cols = df_corr.select_dtypes(include=[np.number]).columns.tolist()
    
    corr_matrix = df_corr[num_cols].corr()
    fig_corr = px.imshow(
        corr_matrix, text_auto=".2f", aspect="auto", 
        color_continuous_scale="RdBu_r", title="Feature Correlation Heatmap"
    )
    st.plotly_chart(fig_corr, width='stretch')
