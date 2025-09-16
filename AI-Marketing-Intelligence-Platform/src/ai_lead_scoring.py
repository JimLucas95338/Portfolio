#!/usr/bin/env python3
"""
AI Lead Scoring Engine
Advanced machine learning model for B2B lead qualification and scoring
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AILeadScoringEngine:
    """
    Advanced AI-powered lead scoring engine that analyzes multiple data points
    to predict lead quality and conversion probability.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the AI Lead Scoring Engine
        
        Args:
            model_path: Path to pre-trained model file
        """
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.scoring_model = None
        self.conversion_model = None
        self.feature_importance = None
        self.model_metrics = {}
        
        if model_path:
            self.load_model(model_path)
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and engineer features for the ML models
        
        Args:
            df: Raw lead data DataFrame
            
        Returns:
            Processed DataFrame with engineered features
        """
        logger.info("Preparing features for lead scoring")
        
        # Create a copy to avoid modifying original data
        processed_df = df.copy()
        
        # Encode categorical variables
        categorical_columns = ['industry', 'company_size', 'job_title', 'lead_source']
        for col in categorical_columns:
            if col in processed_df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    processed_df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(processed_df[col].astype(str))
                else:
                    # Handle unseen categories
                    processed_df[f'{col}_encoded'] = processed_df[col].astype(str).map(
                        dict(zip(self.label_encoders[col].classes_, self.label_encoders[col].transform(self.label_encoders[col].classes_)))
                    ).fillna(-1)
        
        # Engineer behavioral features
        processed_df['engagement_score'] = (
            processed_df['website_visits'] * 0.3 +
            processed_df['page_views'] * 0.2 +
            processed_df['time_on_site'] / 100 * 0.3 +
            processed_df['email_opens'] * 0.2
        )
        
        # Calculate intent signals
        processed_df['intent_score'] = (
            processed_df['form_submissions'] * 0.5 +
            processed_df['email_opens'] * 0.3 +
            (processed_df['time_on_site'] > 300).astype(int) * 0.2
        )
        
        # Company profile score
        company_size_weights = {'Startup': 1, 'SMB': 2, 'Mid-market': 3, 'Enterprise': 4}
        processed_df['company_profile_score'] = processed_df['company_size'].map(company_size_weights).fillna(1)
        
        # Job title hierarchy
        job_title_weights = {
            'CEO': 5, 'CTO': 4, 'VP Marketing': 4, 'VP Sales': 4,
            'Director Sales': 3, 'Director Marketing': 3, 'Manager': 2,
            'Analyst': 1, 'Coordinator': 1
        }
        processed_df['job_title_score'] = processed_df['job_title'].map(job_title_weights).fillna(1)
        
        # Industry attractiveness (based on historical conversion rates)
        industry_weights = {
            'Technology': 1.2, 'Healthcare': 1.1, 'Finance': 1.0,
            'Manufacturing': 0.9, 'Retail': 0.8, 'Education': 0.7
        }
        processed_df['industry_score'] = processed_df['industry'].map(industry_weights).fillna(1.0)
        
        # Recency of activity
        if 'last_activity' in processed_df.columns:
            processed_df['days_since_activity'] = (
                datetime.now() - pd.to_datetime(processed_df['last_activity'])
            ).dt.days
            processed_df['activity_recency_score'] = np.exp(-processed_df['days_since_activity'] / 30)
        else:
            processed_df['activity_recency_score'] = 1.0
        
        # Website engagement velocity
        processed_df['engagement_velocity'] = (
            processed_df['website_visits'] / (processed_df['days_since_activity'] + 1)
        )
        
        # Content depth (pages per visit)
        processed_df['content_depth'] = (
            processed_df['page_views'] / (processed_df['website_visits'] + 1)
        )
        
        logger.info(f"Engineered {len(processed_df.columns)} features")
        return processed_df
    
    def train_scoring_model(self, df: pd.DataFrame, target_column: str = 'qualified') -> Dict:
        """
        Train the lead scoring model
        
        Args:
            df: Training data with features and target
            target_column: Name of the target column
            
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Training lead scoring model")
        
        # Prepare features
        processed_df = self.prepare_features(df)
        
        # Select features for training
        feature_columns = [
            'engagement_score', 'intent_score', 'company_profile_score',
            'job_title_score', 'industry_score', 'activity_recency_score',
            'engagement_velocity', 'content_depth'
        ]
        
        # Add encoded categorical features
        categorical_columns = ['industry_encoded', 'company_size_encoded', 'job_title_encoded']
        feature_columns.extend([col for col in categorical_columns if col in processed_df.columns])
        
        # Prepare training data
        X = processed_df[feature_columns].fillna(0)
        y = processed_df[target_column] if target_column in processed_df.columns else self._create_synthetic_target(processed_df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.scoring_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        self.scoring_model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.scoring_model.predict(X_test_scaled)
        y_pred_proba = self.scoring_model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': self.scoring_model.score(X_test_scaled, y_test),
            'auc_score': roc_auc_score(y_test, y_pred_proba),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        # Feature importance
        self.feature_importance = dict(zip(feature_columns, self.scoring_model.feature_importances_))
        
        self.model_metrics = metrics
        logger.info(f"Model training completed. AUC Score: {metrics['auc_score']:.3f}")
        
        return metrics
    
    def train_conversion_model(self, df: pd.DataFrame, target_column: str = 'conversion_probability') -> Dict:
        """
        Train the conversion probability model
        
        Args:
            df: Training data with features and target
            target_column: Name of the target column
            
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Training conversion probability model")
        
        # Prepare features
        processed_df = self.prepare_features(df)
        
        # Select features for training
        feature_columns = [
            'engagement_score', 'intent_score', 'company_profile_score',
            'job_title_score', 'industry_score', 'activity_recency_score',
            'engagement_velocity', 'content_depth'
        ]
        
        # Add encoded categorical features
        categorical_columns = ['industry_encoded', 'company_size_encoded', 'job_title_encoded']
        feature_columns.extend([col for col in categorical_columns if col in processed_df.columns])
        
        # Prepare training data
        X = processed_df[feature_columns].fillna(0)
        y = processed_df[target_column] if target_column in processed_df.columns else self._create_synthetic_conversion_target(processed_df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.conversion_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.conversion_model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.conversion_model.predict(X_test_scaled)
        
        # Calculate metrics
        metrics = {
            'r2_score': self.conversion_model.score(X_test_scaled, y_test),
            'mse': np.mean((y_test - y_pred) ** 2),
            'mae': np.mean(np.abs(y_test - y_pred))
        }
        
        logger.info(f"Conversion model training completed. R² Score: {metrics['r2_score']:.3f}")
        
        return metrics
    
    def score_lead(self, lead_data: Dict) -> Dict:
        """
        Score a single lead using the trained model
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Dictionary with lead score and insights
        """
        if not self.scoring_model:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Convert to DataFrame
        df = pd.DataFrame([lead_data])
        
        # Prepare features
        processed_df = self.prepare_features(df)
        
        # Select features
        feature_columns = [
            'engagement_score', 'intent_score', 'company_profile_score',
            'job_title_score', 'industry_score', 'activity_recency_score',
            'engagement_velocity', 'content_depth'
        ]
        
        # Add encoded categorical features
        categorical_columns = ['industry_encoded', 'company_size_encoded', 'job_title_encoded']
        feature_columns.extend([col for col in categorical_columns if col in processed_df.columns])
        
        # Prepare input
        X = processed_df[feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Get predictions
        qualification_probability = self.scoring_model.predict_proba(X_scaled)[0, 1]
        lead_score = int(qualification_probability * 100)
        
        # Get conversion probability if model is available
        conversion_probability = 0.0
        if self.conversion_model:
            conversion_probability = self.conversion_model.predict(X_scaled)[0]
            conversion_probability = max(0.0, min(1.0, conversion_probability))
        
        # Generate insights
        insights = self._generate_insights(lead_data, processed_df.iloc[0])
        
        return {
            'lead_score': lead_score,
            'qualification_probability': qualification_probability,
            'conversion_probability': conversion_probability,
            'insights': insights,
            'feature_contributions': self._get_feature_contributions(X.iloc[0], feature_columns),
            'recommendations': self._get_recommendations(lead_score, insights)
        }
    
    def batch_score_leads(self, leads_data: List[Dict]) -> List[Dict]:
        """
        Score multiple leads in batch
        
        Args:
            leads_data: List of lead dictionaries
            
        Returns:
            List of scoring results
        """
        logger.info(f"Batch scoring {len(leads_data)} leads")
        
        results = []
        for lead_data in leads_data:
            try:
                result = self.score_lead(lead_data)
                results.append(result)
            except Exception as e:
                logger.error(f"Error scoring lead: {e}")
                results.append({
                    'lead_score': 0,
                    'qualification_probability': 0.0,
                    'conversion_probability': 0.0,
                    'insights': ['Error in scoring'],
                    'feature_contributions': {},
                    'recommendations': ['Manual review required']
                })
        
        return results
    
    def _create_synthetic_target(self, df: pd.DataFrame) -> pd.Series:
        """Create synthetic target variable for demonstration"""
        # Create qualification based on multiple factors
        qualification_score = (
            df['engagement_score'] * 0.3 +
            df['intent_score'] * 0.4 +
            df['company_profile_score'] * 0.2 +
            df['job_title_score'] * 0.1
        )
        
        # Normalize and create binary target
        qualification_score = (qualification_score - qualification_score.min()) / (qualification_score.max() - qualification_score.min())
        return (qualification_score > 0.6).astype(int)
    
    def _create_synthetic_conversion_target(self, df: pd.DataFrame) -> pd.Series:
        """Create synthetic conversion target for demonstration"""
        # Create conversion probability based on multiple factors
        conversion_score = (
            df['engagement_score'] * 0.25 +
            df['intent_score'] * 0.35 +
            df['company_profile_score'] * 0.2 +
            df['industry_score'] * 0.2
        )
        
        # Normalize to 0-1 range
        conversion_score = (conversion_score - conversion_score.min()) / (conversion_score.max() - conversion_score.min())
        return conversion_score
    
    def _generate_insights(self, lead_data: Dict, processed_lead: pd.Series) -> List[str]:
        """Generate insights about the lead"""
        insights = []
        
        # Engagement insights
        if processed_lead['engagement_score'] > 0.7:
            insights.append("High website engagement indicates strong interest")
        elif processed_lead['engagement_score'] < 0.3:
            insights.append("Low engagement suggests need for nurturing")
        
        # Intent insights
        if processed_lead['intent_score'] > 0.6:
            insights.append("Strong intent signals detected")
        elif processed_lead['intent_score'] < 0.3:
            insights.append("Limited intent signals - consider lead nurturing")
        
        # Company profile insights
        if processed_lead['company_profile_score'] >= 3:
            insights.append("Enterprise-level company with high potential")
        elif processed_lead['company_profile_score'] <= 1:
            insights.append("Small company - evaluate fit and budget")
        
        # Job title insights
        if processed_lead['job_title_score'] >= 4:
            insights.append("Decision-maker identified - high priority")
        elif processed_lead['job_title_score'] <= 2:
            insights.append("Non-decision maker - may need champion")
        
        # Industry insights
        if processed_lead['industry_score'] > 1.0:
            insights.append("Attractive industry with high conversion potential")
        
        return insights
    
    def _get_feature_contributions(self, features: pd.Series, feature_columns: List[str]) -> Dict:
        """Get feature contributions to the score"""
        contributions = {}
        for col in feature_columns:
            if col in features.index:
                contributions[col] = float(features[col])
        return contributions
    
    def _get_recommendations(self, lead_score: int, insights: List[str]) -> List[str]:
        """Generate recommendations based on lead score"""
        recommendations = []
        
        if lead_score >= 80:
            recommendations.extend([
                "Immediate follow-up within 1 hour",
                "Assign to top-performing sales rep",
                "Prepare enterprise-level proposal"
            ])
        elif lead_score >= 60:
            recommendations.extend([
                "Follow-up within 4 hours",
                "Send personalized content",
                "Schedule demo call"
            ])
        elif lead_score >= 40:
            recommendations.extend([
                "Add to nurturing campaign",
                "Send educational content",
                "Follow-up in 24-48 hours"
            ])
        else:
            recommendations.extend([
                "Long-term nurturing required",
                "Focus on awareness content",
                "Re-engage in 1-2 weeks"
            ])
        
        return recommendations
    
    def save_model(self, model_path: str):
        """Save the trained model and preprocessing objects"""
        model_data = {
            'scoring_model': self.scoring_model,
            'conversion_model': self.conversion_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_importance': self.feature_importance,
            'model_metrics': self.model_metrics
        }
        joblib.dump(model_data, model_path)
        logger.info(f"Model saved to {model_path}")
    
    def load_model(self, model_path: str):
        """Load a pre-trained model and preprocessing objects"""
        model_data = joblib.load(model_path)
        self.scoring_model = model_data['scoring_model']
        self.conversion_model = model_data.get('conversion_model')
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_importance = model_data.get('feature_importance')
        self.model_metrics = model_data.get('model_metrics', {})
        logger.info(f"Model loaded from {model_path}")
    
    def get_model_performance(self) -> Dict:
        """Get model performance metrics"""
        return self.model_metrics
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance scores"""
        return self.feature_importance or {}


def main():
    """Demo function to test the AI Lead Scoring Engine"""
    
    # Create sample data
    sample_data = pd.DataFrame({
        'company': ['TechCorp', 'HealthTech', 'FinanceFirst', 'ManufacturingPro', 'RetailMax'],
        'industry': ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail'],
        'company_size': ['Mid-market', 'Enterprise', 'SMB', 'Mid-market', 'Enterprise'],
        'job_title': ['VP Marketing', 'CTO', 'Director Sales', 'CEO', 'VP Marketing'],
        'website_visits': [15, 8, 12, 6, 20],
        'page_views': [45, 32, 28, 18, 65],
        'time_on_site': [450, 320, 280, 180, 650],
        'email_opens': [3, 5, 2, 1, 7],
        'form_submissions': [1, 2, 0, 1, 3],
        'last_activity': pd.date_range('2024-12-01', periods=5, freq='D')
    })
    
    # Initialize and train the engine
    engine = AILeadScoringEngine()
    
    print("Training AI Lead Scoring Engine...")
    scoring_metrics = engine.train_scoring_model(sample_data)
    conversion_metrics = engine.train_conversion_model(sample_data)
    
    print(f"\nScoring Model Performance:")
    print(f"AUC Score: {scoring_metrics['auc_score']:.3f}")
    print(f"Accuracy: {scoring_metrics['accuracy']:.3f}")
    
    print(f"\nConversion Model Performance:")
    print(f"R² Score: {conversion_metrics['r2_score']:.3f}")
    print(f"MAE: {conversion_metrics['mae']:.3f}")
    
    # Test scoring
    print(f"\nFeature Importance:")
    for feature, importance in engine.get_feature_importance().items():
        print(f"{feature}: {importance:.3f}")
    
    # Score a sample lead
    sample_lead = {
        'company': 'DemoCorp',
        'industry': 'Technology',
        'company_size': 'Mid-market',
        'job_title': 'VP Marketing',
        'website_visits': 12,
        'page_views': 35,
        'time_on_site': 400,
        'email_opens': 4,
        'form_submissions': 1,
        'last_activity': datetime.now() - timedelta(days=1)
    }
    
    print(f"\nScoring Sample Lead:")
    result = engine.score_lead(sample_lead)
    print(f"Lead Score: {result['lead_score']}")
    print(f"Qualification Probability: {result['qualification_probability']:.3f}")
    print(f"Conversion Probability: {result['conversion_probability']:.3f}")
    print(f"Insights: {result['insights']}")
    print(f"Recommendations: {result['recommendations']}")


if __name__ == "__main__":
    main()
