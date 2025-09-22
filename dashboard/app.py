"""
Fintech Fraud Detection Dashboard - Real Data Version
AI-powered transaction monitoring system with actual fraud detection

Developer: Kevin Shalu
Portfolio Project: AI Product Manager - Fintech Specialization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from data_processor import FraudDataProcessor
    REAL_DATA_AVAILABLE = True
except ImportError:
    REAL_DATA_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System | Kevin Shalu - Real Data",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(90deg, #1f4e79 0%, #2e7db8 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-high { color: #ff4444; font-weight: bold; }
    .risk-medium { color: #ffaa00; font-weight: bold; }
    .risk-low { color: #44ff44; font-weight: bold; }
    .portfolio-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .real-data-badge {
        background: #28a745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_fraud_data(sample_size):
    """Load and process fraud data with caching"""
    processor = FraudDataProcessor()
    if processor.load_data(sample_size):
        df = processor.detect_anomalies()
        stats = processor.get_fraud_stats()
        return df, stats, processor
    return None, None, None

def main():
    # Portfolio header
    st.markdown("""
    <div class="portfolio-header">
        <h1>🏦 Fintech Fraud Detection System</h1>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p><strong>AI Product Manager Portfolio Project</strong> | Developer: Kevin Shalu | 
                <a href="https://github.com/kevinshalu/fintech-fraud-detector" style="color: #ffffff;">GitHub Repository</a></p>
                <p>Real-time AI-powered transaction monitoring with actual fraud detection</p>
            </div>
            <div class="real-data-badge">REAL DATA ANALYSIS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("🔧 System Controls")
    
    if REAL_DATA_AVAILABLE:
        st.sidebar.success("✅ Real fraud dataset loaded")
        sample_size = st.sidebar.slider("Sample Size (for performance)", 500, 2000, 1000)
        risk_threshold = st.sidebar.slider("Risk Alert Threshold", 0, 100, 70)
        
        # Load real data
        with st.spinner("Loading real fraud data..."):
            df, stats, processor = load_fraud_data(sample_size)
        
        if df is not None:
            # Main dashboard
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Transactions", f"{stats['total_transactions']:,}", "Real Data")
            with col2:
                st.metric("Actual Fraud", stats['actual_fraud'], f"{stats['actual_fraud_rate']:.3f}%")
            with col3:
                st.metric("Predicted Alerts", stats['predicted_fraud'], f"{stats['predicted_fraud_rate']:.2f}%")
            with col4:
                st.metric("Avg Transaction", f"${stats['avg_amount']:.2f}", "Real Data")
            
            st.markdown("---")
            
            # Transaction analysis
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📊 Transaction Analysis - Real Data")
                
                # High-risk transactions
                high_risk = df[df['Risk_Score'] >= risk_threshold].sort_values('Risk_Score', ascending=False)
                
                if len(high_risk) > 0:
                    st.write(f"**🚨 {len(high_risk)} High-Risk Transactions Detected**")
                    
                    # Display top risky transactions
                    display_cols = ['Time', 'Amount', 'Risk_Score', 'Class', 'Predicted_Fraud']
                    risk_display = high_risk[display_cols].head(10).copy()
                    risk_display['Actual_Status'] = risk_display['Class'].map({0: 'Legitimate', 1: 'FRAUD'})
                    risk_display['AI_Prediction'] = risk_display['Predicted_Fraud'].map({0: 'Normal', 1: 'Suspicious'})
                    
                    st.dataframe(
                        risk_display[['Time', 'Amount', 'Risk_Score', 'Actual_Status', 'AI_Prediction']], 
                        use_container_width=True
                    )
                else:
                    st.success("✅ No high-risk transactions detected")
            
            with col2:
                st.subheader("🎯 Model Performance")
                
                # Confusion matrix analysis
                actual_fraud = df['Class'].sum()
                predicted_fraud = df['Predicted_Fraud'].sum()
                
                # True positives (correctly identified fraud)
                true_positives = len(df[(df['Class'] == 1) & (df['Predicted_Fraud'] == 1)])
                false_positives = len(df[(df['Class'] == 0) & (df['Predicted_Fraud'] == 1)])
                false_negatives = len(df[(df['Class'] == 1) & (df['Predicted_Fraud'] == 0)])
                
                if actual_fraud > 0:
                    precision = true_positives / max(predicted_fraud, 1) * 100
                    recall = true_positives / actual_fraud * 100
                    
                    st.metric("Precision", f"{precision:.1f}%", "True Fraud / Predicted")
                    st.metric("Recall", f"{recall:.1f}%", "Detected / Total Fraud")
                    st.metric("False Positives", false_positives, "Normal flagged as fraud")
                else:
                    st.info("No actual fraud in sample")
                
                # Risk score distribution
                fig_risk = px.histogram(df, x='Risk_Score', nbins=20, 
                                      title="Risk Score Distribution")
                fig_risk.update_layout(height=250)
                st.plotly_chart(fig_risk, use_container_width=True)
            
            # Advanced analytics
            st.markdown("---")
            st.subheader("📈 Advanced Fraud Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Amount vs Risk Score
                fig_amount = px.scatter(df, x='Amount', y='Risk_Score', 
                                      color='Class', 
                                      color_discrete_map={0: 'blue', 1: 'red'},
                                      title="Transaction Amount vs Risk Score",
                                      labels={'Class': 'Actual Status'})
                fig_amount.update_layout(height=400)
                st.plotly_chart(fig_amount, use_container_width=True)
            
            with col2:
                # Time analysis
                df['Hour'] = (df['Time'] / 3600) % 24
                hourly_fraud = df.groupby('Hour').agg({
                    'Class': 'mean',
                    'Risk_Score': 'mean'
                }).reset_index()
                
                fig_time = px.line(hourly_fraud, x='Hour', y='Class', 
                                 title="Fraud Rate by Hour of Day")
                fig_time.update_layout(height=400, yaxis_title="Fraud Rate")
                st.plotly_chart(fig_time, use_container_width=True)
            
            # Compliance section
            st.markdown("---")
            st.subheader("📋 Compliance Dashboard")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("**PCI-DSS Compliance**\n✅ Data anonymized (V1-V28)")
                st.info("**Model Performance**\n📊 Real-time anomaly detection")
            
            with col2:
                st.info("**BSA/AML Monitoring**\n✅ Transaction pattern analysis")
                st.info("**Data Quality**\n📈 284K+ transaction dataset")
            
            with col3:
                st.info("**SOX Audit Trail**\n✅ ML model decisions logged")
                st.info("**Risk Management**\n⚠️ Configurable thresholds")
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Generate SAR Report", type="primary"):
                    sar_data = high_risk[high_risk['Risk_Score'] >= 80]
                    if len(sar_data) > 0:
                        st.success(f"✅ SAR Report: {len(sar_data)} high-risk transactions")
                        st.download_button(
                            "⬇️ Download SAR Report",
                            sar_data.to_csv(index=False),
                            f"sar_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                            "text/csv"
                        )
                    else:
                        st.info("No transactions meet SAR threshold (Risk Score ≥ 80)")
            
            with col2:
                if st.button("📊 Export Analysis"):
                    st.download_button(
                        "⬇️ Download Full Analysis",
                        df.to_csv(index=False),
                        f"fraud_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        "text/csv"
                    )
            
            with col3:
                if st.button("🔄 Refresh Model"):
                    st.cache_data.clear()
                    st.rerun()
            
        else:
            st.error("❌ Failed to load fraud dataset. Check data/raw/creditcard.csv exists.")
    
    else:
        st.error("❌ Data processor not available. Check src/data_processor.py")
    
    # Portfolio context
    st.markdown("---")
    st.markdown("""
    ### 💼 Portfolio Project Context - Day 2 Complete
    
    **Real Fraud Detection Capabilities:**
    - ✅ **Dataset Integration:** 284K+ real credit card transactions
    - ✅ **ML Implementation:** Isolation Forest anomaly detection
    - ✅ **Performance Metrics:** Precision, Recall, False Positive tracking
    - ✅ **Business Intelligence:** Risk scoring, temporal analysis, compliance reporting
    
    **AI Product Manager Skills Demonstrated:**
    - **Data Strategy:** Real-world dataset integration and preprocessing
    - **Model Selection:** Unsupervised learning for imbalanced fraud detection
    - **Business Metrics:** Precision/Recall optimization for financial use case
    - **Compliance Integration:** PCI-DSS, BSA/AML, SOX requirements
    
    **Development Progress:** Day 2 of 9 | **Next:** Advanced feature engineering and model optimization
    """)

if __name__ == "__main__":
    main()