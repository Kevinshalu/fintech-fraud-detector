"""
Fintech Fraud Detection Dashboard
AI-powered transaction monitoring system

Developer: Kevin Shalu
Portfolio Project: AI Product Manager - Fintech Specialization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System | Kevin Shalu",
    page_icon="🏦",
    layout="wide"
)

def main():
    # Header
    st.title("🏦 Fintech Fraud Detection System")
    st.markdown("**Developer: Kevin Shalu | AI Product Manager Portfolio Project**")
    st.markdown("Real-time AI-powered transaction monitoring with regulatory compliance")
    
    # Demo message
    st.info("📊 Demo Mode: This dashboard showcases fraud detection capabilities with sample data")
    
    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", "1,247")
    with col2:
        st.metric("Flagged Transactions", "23")
    with col3:
        st.metric("False Positive Rate", "2.1%")
    with col4:
        st.metric("Processing Time", "45ms")
    
    # Sample transaction data
    sample_data = {
        'Transaction ID': ['TXN001', 'TXN002', 'TXN003', 'TXN004'],
        'Amount': [100.50, 2500.00, 45.20, 15000.00],
        'Merchant': ['Coffee Shop', 'Electronics Store', 'Gas Station', 'Luxury Goods'],
        'Risk Score': [15, 45, 20, 95]
    }
    
    df = pd.DataFrame(sample_data)
    
    st.subheader("Recent Transactions")
    st.dataframe(df, use_container_width=True)
    
    # Simple chart
    st.subheader("Risk Score Distribution")
    fig = px.bar(df, x='Transaction ID', y='Risk Score', title="Transaction Risk Scores")
    st.plotly_chart(fig, use_container_width=True)
    
    # Compliance section
    st.subheader("Compliance Status")
    st.success("✅ PCI-DSS Compliant")
    st.success("✅ SOX Audit Trail Active") 
    st.success("✅ GDPR Privacy Controls Enabled")

if __name__ == "__main__":
    main()
