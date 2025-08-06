"""
🎯 Risk Stratification Engine for Value-Based Care

This module implements AI-powered patient risk scoring algorithms
used to identify high-risk patients for proactive care management.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib

class HealthcareRiskEngine:
    """
    Advanced risk stratification engine for healthcare organizations
    implementing value-based care models.
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.encoders = {}
        self.risk_thresholds = {
            'low': 1.0,
            'medium': 2.0,
            'high': 3.0
        }
        
    def prepare_features(self, df):
        """
        Prepare features for risk prediction model
        
        Args:
            df (DataFrame): Patient data with clinical and demographic features
            
        Returns:
            DataFrame: Processed features ready for modeling
        """
        features_df = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['gender', 'chronic_conditions']
        for col in categorical_cols:
            if col in features_df.columns:
                if col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                    features_df[col + '_encoded'] = self.encoders[col].fit_transform(features_df[col].astype(str))
                else:
                    features_df[col + '_encoded'] = self.encoders[col].transform(features_df[col].astype(str))
        
        # Create derived features
        features_df['age_risk_factor'] = np.where(features_df['age'] > 65, 1.5, 1.0)
        features_df['chronic_condition_count'] = features_df['chronic_conditions'].str.count(',') + 1
        features_df['chronic_condition_count'] = np.where(
            features_df['chronic_conditions'] == 'None', 
            0, 
            features_df['chronic_condition_count']
        )
        
        # High-cost condition flags
        high_cost_conditions = ['Cancer', 'Heart Failure', 'ESRD', 'COPD', 'CKD']
        for condition in high_cost_conditions:
            features_df[f'has_{condition.lower().replace(" ", "_")}'] = (
                features_df['chronic_conditions'].str.contains(condition, case=False, na=False).astype(int)
            )
        
        return features_df
    
    def train_risk_model(self, df, target_col='cost_amount'):
        """
        Train the risk prediction model
        
        Args:
            df (DataFrame): Training data
            target_col (str): Target variable for prediction
            
        Returns:
            dict: Training metrics and model performance
        """
        # Prepare features
        features_df = self.prepare_features(df)
        
        # Select feature columns
        feature_cols = [
            'age', 'gender_encoded', 'chronic_condition_count', 'age_risk_factor',
            'has_cancer', 'has_heart_failure', 'has_esrd', 'has_copd', 'has_ckd'
        ]
        
        # Filter existing columns
        available_cols = [col for col in feature_cols if col in features_df.columns]
        
        X = features_df[available_cols]
        y = features_df[target_col]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = dict(zip(available_cols, self.model.feature_importances_))
        
        return {
            'mse': mse,
            'r2_score': r2,
            'feature_importance': feature_importance,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_risk_scores(self, df):
        """
        Predict risk scores for new patients
        
        Args:
            df (DataFrame): Patient data for prediction
            
        Returns:
            DataFrame: Original data with predicted risk scores and categories
        """
        features_df = self.prepare_features(df)
        
        feature_cols = [
            'age', 'gender_encoded', 'chronic_condition_count', 'age_risk_factor',
            'has_cancer', 'has_heart_failure', 'has_esrd', 'has_copd', 'has_ckd'
        ]
        
        available_cols = [col for col in feature_cols if col in features_df.columns]
        X = features_df[available_cols]
        
        # Predict cost (proxy for risk)
        predicted_cost = self.model.predict(X)
        
        # Convert to risk scores (normalized)
        risk_scores = (predicted_cost - predicted_cost.min()) / (predicted_cost.max() - predicted_cost.min()) * 4 + 0.5
        
        # Assign risk categories
        risk_categories = []
        for score in risk_scores:
            if score >= self.risk_thresholds['high']:
                risk_categories.append('High Risk')
            elif score >= self.risk_thresholds['medium']:
                risk_categories.append('Medium Risk')
            elif score >= self.risk_thresholds['low']:
                risk_categories.append('Low Risk')
            else:
                risk_categories.append('Very Low Risk')
        
        # Add predictions to dataframe
        result_df = df.copy()
        result_df['predicted_risk_score'] = risk_scores
        result_df['predicted_risk_category'] = risk_categories
        result_df['predicted_annual_cost'] = predicted_cost
        
        return result_df
    
    def get_care_recommendations(self, patient_risk_score, chronic_conditions):
        """
        Generate care management recommendations based on risk score
        
        Args:
            patient_risk_score (float): Patient's risk score
            chronic_conditions (str): Patient's chronic conditions
            
        Returns:
            dict: Care recommendations and intervention strategies
        """
        recommendations = {
            'care_level': '',
            'interventions': [],
            'monitoring_frequency': '',
            'care_team': []
        }
        
        if patient_risk_score >= 3.0:
            recommendations['care_level'] = 'Intensive Care Management'
            recommendations['interventions'] = [
                'Weekly nurse check-ins',
                'Medication adherence monitoring',
                'Emergency action plan development',
                'Specialist referral coordination'
            ]
            recommendations['monitoring_frequency'] = 'Weekly'
            recommendations['care_team'] = ['Care Manager', 'Nurse Navigator', 'Pharmacist', 'Specialist']
            
        elif patient_risk_score >= 2.0:
            recommendations['care_level'] = 'Enhanced Care Coordination'
            recommendations['interventions'] = [
                'Bi-weekly care coordination calls',
                'Care plan optimization',
                'Preventive care scheduling',
                'Disease-specific education'
            ]
            recommendations['monitoring_frequency'] = 'Bi-weekly'
            recommendations['care_team'] = ['Care Coordinator', 'Clinical Pharmacist']
            
        elif patient_risk_score >= 1.0:
            recommendations['care_level'] = 'Standard Care with Monitoring'
            recommendations['interventions'] = [
                'Monthly wellness checks',
                'Preventive care reminders',
                'Health education materials'
            ]
            recommendations['monitoring_frequency'] = 'Monthly'
            recommendations['care_team'] = ['Primary Care Provider']
            
        else:
            recommendations['care_level'] = 'Standard Preventive Care'
            recommendations['interventions'] = [
                'Annual wellness visits',
                'Preventive screening reminders',
                'Health promotion programs'
            ]
            recommendations['monitoring_frequency'] = 'Annually'
            recommendations['care_team'] = ['Primary Care Provider']
        
        # Add condition-specific recommendations
        if 'Diabetes' in chronic_conditions:
            recommendations['interventions'].extend([
                'HbA1c monitoring every 3 months',
                'Diabetic eye exam annually',
                'Foot care education'
            ])
        
        if 'Heart Failure' in chronic_conditions:
            recommendations['interventions'].extend([
                'Daily weight monitoring',
                'Sodium restriction counseling',
                'Cardiology follow-up'
            ])
        
        if 'COPD' in chronic_conditions:
            recommendations['interventions'].extend([
                'Spirometry monitoring',
                'Smoking cessation support',
                'Pulmonary rehabilitation'
            ])
        
        return recommendations
    
    def save_model(self, filepath):
        """Save the trained model and encoders"""
        model_data = {
            'model': self.model,
            'encoders': self.encoders,
            'risk_thresholds': self.risk_thresholds
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """Load a pre-trained model and encoders"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.encoders = model_data['encoders']
        self.risk_thresholds = model_data['risk_thresholds']

# Example usage and testing
if __name__ == "__main__":
    # Demo with sample data
    sample_data = pd.DataFrame({
        'patient_id': ['P001', 'P002', 'P003'],
        'age': [67, 45, 72],
        'gender': ['F', 'M', 'F'],
        'chronic_conditions': ['Diabetes,Hypertension', 'Hypertension', 'COPD,Heart Failure'],
        'cost_amount': [1250, 180, 2450]
    })
    
    # Initialize and train risk engine
    risk_engine = HealthcareRiskEngine()
    
    print("🤖 Healthcare Risk Engine Initialized")
    print("=" * 50)
    
    # Train model
    metrics = risk_engine.train_risk_model(sample_data)
    print(f"✅ Model Training Complete")
    print(f"📊 R² Score: {metrics['r2_score']:.3f}")
    print(f"📈 Training Samples: {metrics['training_samples']}")
    
    # Generate predictions
    predictions = risk_engine.predict_risk_scores(sample_data)
    print(f"\\n🎯 Risk Predictions Generated")
    
    # Show sample recommendations
    for _, patient in predictions.iterrows():
        recs = risk_engine.get_care_recommendations(
            patient['predicted_risk_score'], 
            patient['chronic_conditions']
        )
        print(f"\\n👤 {patient['patient_id']} ({patient['predicted_risk_category']}):")
        print(f"   📋 Care Level: {recs['care_level']}")
        print(f"   ⏰ Monitoring: {recs['monitoring_frequency']}")
        print(f"   👥 Care Team: {', '.join(recs['care_team'])}")