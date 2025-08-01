import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data(filepath):
    """Load and preprocess the patient readmission dataset."""
    df = pd.read_csv(filepath)
    
    # Encode categorical variables
    le_gender = LabelEncoder()
    le_diagnosis = LabelEncoder()
    le_insurance = LabelEncoder()
    le_discharge = LabelEncoder()
    
    X = df.copy()
    X['Gender'] = le_gender.fit_transform(X['Gender'])
    X['Diagnosis'] = le_diagnosis.fit_transform(X['Diagnosis'])
    X['InsuranceType'] = le_insurance.fit_transform(X['InsuranceType'])
    X['DischargeDisposition'] = le_discharge.fit_transform(X['DischargeDisposition'])
    
    # Create target variable
    y = (X['Readmitted'] == 'Yes').astype(int)
    X = X.drop(['PatientID', 'Readmitted'], axis=1)
    
    return X, y, df

def train_model(X_train, y_train, random_state=42):
    """Train a Random Forest model for readmission prediction."""
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance and return metrics."""
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    results = {
        'classification_report': classification_report(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
        'predictions': y_pred,
        'probabilities': y_pred_proba
    }
    return results

def plot_feature_importance(model, feature_names):
    """Plot feature importance from the trained model."""
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(8,6))
    sns.barplot(x='importance', y='feature', data=feature_importance.head(10))
    plt.title('Top 10 Feature Importance')
    plt.show()
    
    return feature_importance

def detect_bias(model, X_test, y_test, original_df, test_indices):
    """Detect potential bias in model predictions across demographic groups."""
    bias_results = {}
    
    # Age bias analysis
    age_groups = pd.cut(original_df.iloc[test_indices]['Age'], 
                        bins=[0, 65, 80, 100], 
                        labels=['<65', '65-80', '>80'])
    
    for age_group in age_groups.unique():
        mask = age_groups == age_group
        if mask.sum() > 0:
            group_pred = model.predict(X_test[mask])
            group_actual = y_test[mask]
            accuracy = (group_pred == group_actual).mean()
            bias_results[f'age_{age_group}'] = accuracy
    
    # Gender bias analysis
    for gender in ['Male', 'Female']:
        gender_mask = original_df.iloc[test_indices]['Gender'] == gender
        if gender_mask.sum() > 0:
            gender_pred = model.predict(X_test[gender_mask])
            gender_actual = y_test[gender_mask]
            accuracy = (gender_pred == gender_actual).mean()
            bias_results[f'gender_{gender}'] = accuracy
    
    return bias_results 