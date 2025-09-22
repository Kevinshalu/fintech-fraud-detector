import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class FraudDataProcessor:
    def __init__(self):
        self.model = IsolationForest(contamination=0.002, random_state=42)
        self.df = None
    
    def load_data(self, sample_size=1000):
        """Load and sample the fraud dataset"""
        try:
            df_full = pd.read_csv('data/raw/creditcard.csv')
            # Sample for dashboard performance
            self.df = df_full.sample(n=min(sample_size, len(df_full)), random_state=42)
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def detect_anomalies(self):
        """Run fraud detection on current data"""
        if self.df is None:
            return None
            
        # Use features for anomaly detection
        features = ['Time', 'Amount'] + [f'V{i}' for i in range(1, 29)]
        X = self.df[features]
        
        # Predict anomalies
        anomalies = self.model.fit_predict(X)
        self.df['Predicted_Fraud'] = (anomalies == -1).astype(int)
        
        # Calculate risk scores
        scores = self.model.decision_function(X)
        self.df['Risk_Score'] = ((scores.max() - scores) / (scores.max() - scores.min()) * 100).astype(int)
        
        return self.df
    
    def get_fraud_stats(self):
        """Get fraud statistics"""
        if self.df is None:
            return {}
            
        actual_fraud_rate = (self.df['Class'].sum() / len(self.df)) * 100
        predicted_fraud_rate = (self.df['Predicted_Fraud'].sum() / len(self.df)) * 100
        
        return {
            'total_transactions': len(self.df),
            'actual_fraud': self.df['Class'].sum(),
            'predicted_fraud': self.df['Predicted_Fraud'].sum(),
            'actual_fraud_rate': actual_fraud_rate,
            'predicted_fraud_rate': predicted_fraud_rate,
            'avg_amount': self.df['Amount'].mean()
        }