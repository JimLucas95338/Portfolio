# Patient Readmission Prediction

## Overview
This project demonstrates the development of a machine learning model to predict patient readmission risk, with a focus on explainability, fairness, and ethical considerations in healthcare AI.

## Objectives
- Build a predictive model for patient readmission risk
- Ensure model interpretability and explainability
- Detect and address potential bias in predictions
- Provide actionable insights for healthcare providers

## Methodology
1. **Data Preprocessing**: Handle categorical variables, feature engineering
2. **Model Development**: Random Forest classifier with hyperparameter tuning
3. **Evaluation**: Performance metrics, confusion matrix, ROC-AUC
4. **Explainability**: Feature importance analysis, SHAP values
5. **Bias Detection**: Analyze predictions across demographic groups

## Ethical Considerations
- **Fairness**: Monitor for bias across age, gender, and other demographic factors
- **Transparency**: Ensure model decisions are explainable to clinicians
- **Privacy**: Use synthetic data to protect patient confidentiality
- **Impact**: Consider the consequences of false positives vs false negatives

## Project Structure
- `data/` – Synthetic patient dataset
- `notebooks/` – Jupyter notebooks for analysis and modeling
- `src/` – Utility functions and model code
- `docs/` – Documentation and reports

## Getting Started
1. Install required packages:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```
2. Run the main notebook: `notebooks/readmission_prediction_model.ipynb`
3. Review the utility functions in `src/model_utils.py`

## Key Features
- **Predictive Modeling**: Random Forest with 80%+ accuracy
- **Feature Importance**: Identifies key risk factors
- **Bias Detection**: Analyzes fairness across demographic groups
- **Explainable AI**: Provides interpretable results for clinicians

## Results
- Model achieves good performance on synthetic data
- Top risk factors: Length of stay, number of medications, age
- Bias analysis shows consistent performance across demographic groups
- Ready for validation on real-world data with proper safeguards 