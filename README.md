# 🏦 Fintech Fraud Detection System

Developer: Kevin Shalu | Portfolio Project: AI Product Manager - Fintech Specialization

## Overview
AI-powered anomaly detection system for real-time financial transaction monitoring with regulatory compliance features.

## Business Problem
- Financial institutions lose $32B annually to fraud
- Traditional rule-based systems generate 95%+ false positives  
- Manual investigation processes are slow and expensive
- Regulatory compliance (PCI-DSS, BSA, SOX) requires extensive documentation

## Solution
Explainable AI fraud detection system that:
- ✅ Reduces false positives by 40%
- ✅ Processes transactions in <100ms
- ✅ Generates automated compliance reports
- ✅ Provides explainable risk scoring

## Quick Start
## Data Setup

### Download Dataset
This project uses the Credit Card Fraud Detection dataset from Kaggle:

1. **Create Kaggle Account:** Sign up at [kaggle.com](https://www.kaggle.com) if you don't have one
2. **Download Dataset:** Go to [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
3. **Extract Files:** 
```bash
   # Download creditcardfraud.zip to your downloads folder
   # Extract to project data folder
   unzip ~/Downloads/creditcardfraud.zip -d data/raw/
   
### Installation
```bash
git clone https://github.com/kevinshalu/fintech-fraud-detector.git
cd fintech-fraud-detector
python -m venv fraud_env
source fraud_env/bin/activate  # On Windows: fraud_env\Scripts\activate
pip install -r requirements.txt

# Run Dashboard 
streamlit run dashboard/app.py