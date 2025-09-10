"""
Clinical Signals Engine - Signal-Action Framework
=================================================

This module implements a clinical signals engine providing predictive alerts 
and workflow automation for value-based care providers.

Key Features:
- Urgency scoring algorithms for patient prioritization
- Signal-action framework for care team workflows
- Predictive alerts for ED visits, readmissions, and care gaps
- Provider panel management optimization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class ClinicalSignalsEngine:
    """
    Clinical Signals Engine for proactive care management.
    
    This engine identifies high-risk patients and recommends specific actions
    to improve outcomes and reduce costs in value-based care settings.
    """
    
    def __init__(self):
        self.signal_thresholds = {
            'high_risk_ed': 0.7,
            'readmission_risk': 0.6,
            'care_gap_urgent': 0.8,
            'chronic_care_mgmt': 0.5
        }
        
        # Clinical signal categories
        self.signal_categories = {
            'preventive': ['annual_wellness_visit', 'cancer_screening', 'vaccination'],
            'acute': ['post_discharge_followup', 'ed_visit_prevention', 'urgent_referral'],
            'predictive': ['readmission_risk', 'ed_risk', 'deterioration_risk'],
            'chronic': ['diabetes_care', 'hypertension_mgmt', 'medication_adherence']
        }
    
    def calculate_urgency_score(self, patient_data: Dict) -> float:
        """
        Calculate urgency score for patient prioritization.
        
        Args:
            patient_data: Dictionary containing patient clinical and demographic data
            
        Returns:
            Urgency score between 0-100 (higher = more urgent)
        """
        score_components = {}
        
        # Clinical risk factors (40% weight)
        clinical_score = 0
        if patient_data.get('num_chronic_conditions', 0) >= 3:
            clinical_score += 25
        if patient_data.get('recent_ed_visits', 0) >= 2:
            clinical_score += 20
        if patient_data.get('recent_hospitalizations', 0) >= 1:
            clinical_score += 15
        
        score_components['clinical'] = min(clinical_score, 40)
        
        # Social determinants (20% weight)
        social_score = 0
        if patient_data.get('transportation_barriers', False):
            social_score += 5
        if patient_data.get('food_insecurity', False):
            social_score += 5
        if patient_data.get('medication_adherence', 0) < 0.8:
            social_score += 10
        
        score_components['social'] = min(social_score, 20)
        
        # Care gaps (25% weight)
        care_gap_score = 0
        overdue_screenings = patient_data.get('overdue_screenings', 0)
        care_gap_score += min(overdue_screenings * 5, 15)
        
        days_since_pcp_visit = patient_data.get('days_since_pcp_visit', 0)
        if days_since_pcp_visit > 365:
            care_gap_score += 10
        
        score_components['care_gaps'] = min(care_gap_score, 25)
        
        # Utilization patterns (15% weight)
        utilization_score = 0
        if patient_data.get('total_cost_last_year', 0) > 10000:
            utilization_score += 8
        if patient_data.get('specialist_visits', 0) > 6:
            utilization_score += 7
        
        score_components['utilization'] = min(utilization_score, 15)
        
        total_score = sum(score_components.values())
        
        return min(total_score, 100)
    
    def generate_clinical_signals(self, patient_panel: pd.DataFrame) -> pd.DataFrame:
        """
        Generate clinical signals for entire patient panel.
        
        Args:
            patient_panel: DataFrame containing patient data
            
        Returns:
            DataFrame with patients, urgency scores, and recommended actions
        """
        signals_data = []
        
        for _, patient in patient_panel.iterrows():
            patient_dict = patient.to_dict()
            urgency_score = self.calculate_urgency_score(patient_dict)
            
            # Determine signal category and recommended actions
            signals = self._identify_patient_signals(patient_dict, urgency_score)
            
            signals_data.append({
                'patient_id': patient_dict.get('patient_id'),
                'patient_name': patient_dict.get('patient_name', 'Unknown'),
                'urgency_score': urgency_score,
                'risk_level': self._get_risk_level(urgency_score),
                'primary_signal': signals['primary'],
                'signal_category': signals['category'],
                'recommended_action': signals['action'],
                'action_priority': signals['priority'],
                'care_team_role': signals['care_team'],
                'target_completion': signals['timeline']
            })
        
        return pd.DataFrame(signals_data).sort_values('urgency_score', ascending=False)
    
    def _identify_patient_signals(self, patient_data: Dict, urgency_score: float) -> Dict:
        """Identify specific signals and recommended actions for a patient."""
        
        # High urgency patients (score > 70)
        if urgency_score > 70:
            if patient_data.get('recent_discharge', False):
                return {
                    'primary': 'High-Risk Post-Discharge',
                    'category': 'acute',
                    'action': 'Schedule 72-hour post-discharge call and 7-day follow-up visit',
                    'priority': 'Urgent - 24 hours',
                    'care_team': 'Care Manager + PCP',
                    'timeline': 'Within 24 hours'
                }
            elif patient_data.get('recent_ed_visits', 0) >= 2:
                return {
                    'primary': 'Frequent ED User',
                    'category': 'predictive',
                    'action': 'Initiate chronic care management and care plan review',
                    'priority': 'High - 48 hours',
                    'care_team': 'Care Manager',
                    'timeline': 'Within 48 hours'
                }
        
        # Medium urgency (score 40-70)
        elif urgency_score > 40:
            if patient_data.get('overdue_screenings', 0) > 2:
                return {
                    'primary': 'Multiple Care Gaps',
                    'category': 'preventive',
                    'action': 'Schedule comprehensive wellness visit and screening catch-up',
                    'priority': 'Medium - 1 week',
                    'care_team': 'PCP + Care Coordinator',
                    'timeline': 'Within 7 days'
                }
            elif patient_data.get('medication_adherence', 1) < 0.8:
                return {
                    'primary': 'Medication Non-Adherence',
                    'category': 'chronic',
                    'action': 'Medication therapy management and adherence counseling',
                    'priority': 'Medium - 1 week',
                    'care_team': 'Pharmacist + Care Manager',
                    'timeline': 'Within 7 days'
                }
        
        # Lower urgency patients
        else:
            return {
                'primary': 'Routine Care Management',
                'category': 'preventive',
                'action': 'Annual wellness visit and routine screening reminder',
                'priority': 'Routine - 30 days',
                'care_team': 'Care Coordinator',
                'timeline': 'Within 30 days'
            }
        
        # Default case
        return {
            'primary': 'Assessment Needed',
            'category': 'general',
            'action': 'Comprehensive assessment and risk stratification',
            'priority': 'Medium - 1 week',
            'care_team': 'Care Manager',
            'timeline': 'Within 7 days'
        }
    
    def _get_risk_level(self, urgency_score: float) -> str:
        """Convert urgency score to risk level categories."""
        if urgency_score >= 70:
            return "High Risk"
        elif urgency_score >= 40:
            return "Medium Risk"
        elif urgency_score >= 20:
            return "Low Risk"
        else:
            return "Stable"
    
    def prioritize_patient_panel(self, provider_panel: pd.DataFrame, max_patients: int = 20) -> pd.DataFrame:
        """
        Prioritize patients for proactive outreach.
        
        Args:
            provider_panel: DataFrame with provider's patient panel
            max_patients: Maximum number of patients to prioritize for action
            
        Returns:
            DataFrame with top priority patients and recommended actions
        """
        # Generate signals for all patients
        signals_df = self.generate_clinical_signals(provider_panel)
        
        # Apply clinical filtering
        priority_patients = signals_df[
            (signals_df['urgency_score'] >= 30) |  # Minimum threshold
            (signals_df['signal_category'].isin(['acute', 'predictive']))  # Critical categories
        ].head(max_patients)
        
        # Add workflow integration recommendations
        priority_patients['workflow_integration'] = priority_patients.apply(
            lambda row: self._get_workflow_recommendation(row), axis=1
        )
        
        return priority_patients
    
    def _get_workflow_recommendation(self, patient_row: pd.Series) -> str:
        """Generate workflow integration recommendations for EHR systems."""
        category = patient_row['signal_category']
        priority = patient_row['action_priority']
        
        if 'Urgent' in priority:
            return "Add to provider's urgent task list + immediate alert"
        elif category == 'acute':
            return "Schedule in next available appointment slot"
        elif category == 'preventive':
            return "Add to outreach campaign + patient portal message"
        else:
            return "Add to monthly care management review"
    
    def generate_provider_dashboard_data(self, provider_panel: pd.DataFrame) -> Dict:
        """
        Generate provider dashboard data.
        
        Args:
            provider_panel: DataFrame containing provider's patient panel
            
        Returns:
            Dictionary with dashboard metrics and patient lists
        """
        signals_df = self.generate_clinical_signals(provider_panel)
        
        dashboard_data = {
            'panel_overview': {
                'total_patients': len(provider_panel),
                'high_risk_patients': len(signals_df[signals_df['risk_level'] == 'High Risk']),
                'patients_needing_action': len(signals_df[signals_df['urgency_score'] >= 30]),
                'average_risk_score': signals_df['urgency_score'].mean()
            },
            'signal_breakdown': {
                'acute_signals': len(signals_df[signals_df['signal_category'] == 'acute']),
                'predictive_signals': len(signals_df[signals_df['signal_category'] == 'predictive']),
                'preventive_signals': len(signals_df[signals_df['signal_category'] == 'preventive']),
                'chronic_signals': len(signals_df[signals_df['signal_category'] == 'chronic'])
            },
            'action_priorities': {
                'urgent_24h': len(signals_df[signals_df['action_priority'].str.contains('Urgent', na=False)]),
                'high_48h': len(signals_df[signals_df['action_priority'].str.contains('High', na=False)]),
                'medium_1week': len(signals_df[signals_df['action_priority'].str.contains('Medium', na=False)]),
                'routine_30days': len(signals_df[signals_df['action_priority'].str.contains('Routine', na=False)])
            },
            'top_priority_patients': signals_df.head(10).to_dict('records')
        }
        
        return dashboard_data

# Example usage and demonstration
if __name__ == "__main__":
    # Create sample patient panel data
    np.random.seed(42)
    
    sample_patients = []
    for i in range(100):
        patient = {
            'patient_id': f'PAT_{i+1:03d}',
            'patient_name': f'Patient {i+1}',
            'age': np.random.randint(18, 95),
            'num_chronic_conditions': np.random.poisson(1.5),
            'recent_ed_visits': np.random.poisson(0.5),
            'recent_hospitalizations': np.random.poisson(0.2),
            'transportation_barriers': np.random.choice([True, False], p=[0.2, 0.8]),
            'food_insecurity': np.random.choice([True, False], p=[0.15, 0.85]),
            'medication_adherence': np.random.beta(8, 2),  # Skewed toward good adherence
            'overdue_screenings': np.random.poisson(1),
            'days_since_pcp_visit': np.random.exponential(200),
            'total_cost_last_year': np.random.lognormal(8, 1),
            'specialist_visits': np.random.poisson(2),
            'recent_discharge': np.random.choice([True, False], p=[0.1, 0.9])
        }
        sample_patients.append(patient)
    
    patient_panel_df = pd.DataFrame(sample_patients)
    
    # Initialize the Clinical Signals Engine
    signals_engine = ClinicalSignalsEngine()
    
    print("🎯 Clinical Signals Engine Demo")
    print("=" * 60)
    
    # Generate clinical signals
    signals_results = signals_engine.generate_clinical_signals(patient_panel_df)
    
    print(f"\nTop 10 Priority Patients:")
    print("-" * 60)
    for _, patient in signals_results.head(10).iterrows():
        print(f"Patient: {patient['patient_name']}")
        print(f"  Urgency Score: {patient['urgency_score']:.1f} ({patient['risk_level']})")
        print(f"  Signal: {patient['primary_signal']}")
        print(f"  Action: {patient['recommended_action']}")
        print(f"  Priority: {patient['action_priority']}")
        print(f"  Care Team: {patient['care_team_role']}")
        print()
    
    # Generate provider dashboard
    dashboard_data = signals_engine.generate_provider_dashboard_data(patient_panel_df)
    
    print("\n📊 Provider Dashboard Summary:")
    print("-" * 60)
    overview = dashboard_data['panel_overview']
    print(f"Total Patients: {overview['total_patients']}")
    print(f"High Risk Patients: {overview['high_risk_patients']}")
    print(f"Patients Needing Action: {overview['patients_needing_action']}")
    print(f"Average Risk Score: {overview['average_risk_score']:.1f}")
    
    print(f"\n🚨 Action Priorities:")
    priorities = dashboard_data['action_priorities']
    print(f"  Urgent (24h): {priorities['urgent_24h']} patients")
    print(f"  High (48h): {priorities['high_48h']} patients")
    print(f"  Medium (1 week): {priorities['medium_1week']} patients")
    print(f"  Routine (30 days): {priorities['routine_30days']} patients")
    
    print("\n" + "=" * 60)
    print("Clinical Signals Engine Demo Complete! 🎉")
    print("This demonstrates clinical signal-action framework")
    print("for proactive population health management.")
