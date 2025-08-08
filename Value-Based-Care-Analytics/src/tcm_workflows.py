"""
Transitional Care Management (TCM) Workflows
============================================

Pearl Health-style post-discharge care coordination and transitional care management.
Focuses on reducing readmissions and improving care transitions.

Key Features:
- Post-discharge follow-up scheduling
- Care transition risk assessment
- Provider workflow automation
- Readmission prevention protocols
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class TransitionalCareManager:
    """
    Pearl Health-style Transitional Care Management system.
    
    Automates post-discharge workflows to reduce readmissions and improve
    care coordination between hospital and primary care settings.
    """
    
    def __init__(self):
        self.tcm_protocols = {
            'high_risk': {
                'contact_timeline': '24_hours',
                'followup_timeline': '7_days',
                'care_team': ['PCP', 'Care_Manager', 'Pharmacist'],
                'interventions': ['medication_reconciliation', 'home_visit', 'care_plan_update']
            },
            'medium_risk': {
                'contact_timeline': '48_hours',
                'followup_timeline': '14_days',
                'care_team': ['PCP', 'Care_Manager'],
                'interventions': ['phone_call', 'medication_review', 'followup_scheduling']
            },
            'low_risk': {
                'contact_timeline': '72_hours',
                'followup_timeline': '30_days',
                'care_team': ['Care_Coordinator'],
                'interventions': ['phone_call', 'routine_followup']
            }
        }
        
        # Risk factors for readmission (Pearl Health methodology)
        self.readmission_risk_factors = {
            'clinical': {
                'heart_failure': 3.2,
                'copd': 2.8,
                'diabetes_complications': 2.1,
                'sepsis': 2.9,
                'pneumonia': 1.8,
                'stroke': 2.3
            },
            'social': {
                'lives_alone': 1.5,
                'transportation_barriers': 1.8,
                'medication_costs': 2.0,
                'health_literacy_low': 1.6
            },
            'utilization': {
                'frequent_ed_user': 2.5,
                'multiple_readmissions': 3.0,
                'long_length_of_stay': 1.7,
                'multiple_comorbidities': 2.2
            }
        }
    
    def assess_discharge_risk(self, patient_data: Dict) -> Dict:
        """
        Assess patient's risk for readmission using Pearl Health risk factors.
        
        Args:
            patient_data: Dictionary containing patient clinical and social data
            
        Returns:
            Dictionary with risk score, level, and recommended interventions
        """
        risk_score = 1.0  # Base risk
        risk_factors_present = []
        
        # Clinical risk factors
        for condition, multiplier in self.readmission_risk_factors['clinical'].items():
            if patient_data.get(condition, False):
                risk_score *= multiplier
                risk_factors_present.append(f"Clinical: {condition}")
        
        # Social determinants
        for factor, multiplier in self.readmission_risk_factors['social'].items():
            if patient_data.get(factor, False):
                risk_score *= multiplier
                risk_factors_present.append(f"Social: {factor}")
        
        # Utilization patterns
        for pattern, multiplier in self.readmission_risk_factors['utilization'].items():
            if patient_data.get(pattern, False):
                risk_score *= multiplier
                risk_factors_present.append(f"Utilization: {pattern}")
        
        # Additional risk factors
        age = patient_data.get('age', 65)
        if age >= 75:
            risk_score *= 1.3
            risk_factors_present.append("Demographic: Age 75+")
        
        # Length of stay impact
        los = patient_data.get('length_of_stay', 3)
        if los >= 7:
            risk_score *= 1.4
            risk_factors_present.append("Clinical: Extended LOS")
        
        # Determine risk level
        if risk_score >= 8.0:
            risk_level = 'high_risk'
        elif risk_score >= 4.0:
            risk_level = 'medium_risk'
        else:
            risk_level = 'low_risk'
        
        return {
            'risk_score': min(risk_score, 20.0),  # Cap at 20
            'risk_level': risk_level,
            'risk_factors': risk_factors_present,
            'recommended_protocol': self.tcm_protocols[risk_level]
        }
    
    def create_tcm_workflow(self, patient_data: Dict, discharge_date: datetime) -> Dict:
        """
        Create personalized TCM workflow based on patient risk assessment.
        
        Args:
            patient_data: Patient clinical and demographic data
            discharge_date: Date of hospital discharge
            
        Returns:
            Dictionary with complete TCM workflow and timeline
        """
        risk_assessment = self.assess_discharge_risk(patient_data)
        protocol = risk_assessment['recommended_protocol']
        
        # Calculate key dates
        contact_hours = 24 if protocol['contact_timeline'] == '24_hours' else \
                       48 if protocol['contact_timeline'] == '48_hours' else 72
        
        followup_days = 7 if protocol['followup_timeline'] == '7_days' else \
                       14 if protocol['followup_timeline'] == '14_days' else 30
        
        contact_date = discharge_date + timedelta(hours=contact_hours)
        followup_date = discharge_date + timedelta(days=followup_days)
        
        workflow = {
            'patient_id': patient_data.get('patient_id'),
            'patient_name': patient_data.get('patient_name'),
            'discharge_date': discharge_date.strftime('%Y-%m-%d'),
            'risk_assessment': risk_assessment,
            'workflow_timeline': {
                'initial_contact': {
                    'due_date': contact_date.strftime('%Y-%m-%d %H:%M'),
                    'responsible_party': protocol['care_team'][0],
                    'contact_method': 'phone_call',
                    'objectives': ['assess_status', 'medication_review', 'schedule_followup'],
                    'status': 'pending'
                },
                'followup_visit': {
                    'due_date': followup_date.strftime('%Y-%m-%d'),
                    'responsible_party': 'PCP',
                    'visit_type': 'office_visit' if risk_assessment['risk_level'] != 'low_risk' else 'telehealth',
                    'objectives': ['physical_exam', 'medication_reconciliation', 'care_plan_review'],
                    'status': 'pending'
                }
            },
            'interventions': self._generate_interventions(risk_assessment, patient_data),
            'care_team_assignments': self._assign_care_team(protocol['care_team'], risk_assessment),
            'success_metrics': {
                'target_contact_completion': '100%',
                'target_followup_completion': '85%',
                'target_readmission_reduction': '25%'
            }
        }
        
        return workflow
    
    def _generate_interventions(self, risk_assessment: Dict, patient_data: Dict) -> List[Dict]:
        """Generate specific interventions based on risk factors."""
        interventions = []
        risk_factors = risk_assessment['risk_factors']
        
        # Medication-related interventions
        if any('medication' in factor.lower() for factor in risk_factors):
            interventions.append({
                'intervention': 'Comprehensive Medication Reconciliation',
                'responsible': 'Pharmacist',
                'timeline': 'Within 48 hours',
                'objectives': ['identify_discrepancies', 'assess_adherence', 'cost_counseling']
            })
        
        # Social support interventions
        if any('social' in factor.lower() for factor in risk_factors):
            interventions.append({
                'intervention': 'Social Services Coordination',
                'responsible': 'Care Manager',
                'timeline': 'Within 72 hours',
                'objectives': ['transportation_assistance', 'meal_support', 'home_safety']
            })
        
        # High-risk clinical interventions
        if risk_assessment['risk_level'] == 'high_risk':
            interventions.append({
                'intervention': 'Home Health Assessment',
                'responsible': 'Home Health Nurse',
                'timeline': 'Within 48 hours',
                'objectives': ['clinical_assessment', 'medication_setup', 'caregiver_education']
            })
        
        # Chronic disease management
        chronic_conditions = ['heart_failure', 'copd', 'diabetes_complications']
        if any(patient_data.get(condition, False) for condition in chronic_conditions):
            interventions.append({
                'intervention': 'Chronic Care Management Enrollment',
                'responsible': 'Care Manager',
                'timeline': 'Within 7 days',
                'objectives': ['care_plan_update', 'self_management_education', 'monitoring_setup']
            })
        
        return interventions
    
    def _assign_care_team(self, care_team_roles: List[str], risk_assessment: Dict) -> Dict:
        """Assign specific responsibilities to care team members."""
        assignments = {}
        
        for role in care_team_roles:
            if role == 'PCP':
                assignments['Primary Care Provider'] = {
                    'responsibilities': ['clinical_oversight', 'followup_visit', 'care_plan_management'],
                    'contact_schedule': 'As needed for clinical issues'
                }
            elif role == 'Care_Manager':
                assignments['Care Manager'] = {
                    'responsibilities': ['care_coordination', 'barrier_identification', 'resource_connection'],
                    'contact_schedule': 'Weekly for first month'
                }
            elif role == 'Pharmacist':
                assignments['Clinical Pharmacist'] = {
                    'responsibilities': ['medication_reconciliation', 'adherence_counseling', 'drug_interaction_review'],
                    'contact_schedule': 'Within 48 hours, then as needed'
                }
            elif role == 'Care_Coordinator':
                assignments['Care Coordinator'] = {
                    'responsibilities': ['appointment_scheduling', 'reminder_calls', 'basic_health_education'],
                    'contact_schedule': 'Per protocol timeline'
                }
        
        return assignments
    
    def generate_tcm_dashboard_data(self, tcm_workflows: List[Dict]) -> Dict:
        """
        Generate dashboard data for TCM program performance monitoring.
        
        Args:
            tcm_workflows: List of TCM workflow dictionaries
            
        Returns:
            Dictionary with performance metrics and insights
        """
        total_workflows = len(tcm_workflows)
        
        if total_workflows == 0:
            return {'error': 'No TCM workflows to analyze'}
        
        # Risk distribution
        risk_distribution = {'high_risk': 0, 'medium_risk': 0, 'low_risk': 0}
        contact_completion = 0
        followup_completion = 0
        
        for workflow in tcm_workflows:
            risk_level = workflow['risk_assessment']['risk_level']
            risk_distribution[risk_level] += 1
            
            # Check completion status (simulated)
            if workflow['workflow_timeline']['initial_contact']['status'] == 'completed':
                contact_completion += 1
            if workflow['workflow_timeline']['followup_visit']['status'] == 'completed':
                followup_completion += 1
        
        dashboard_data = {
            'program_overview': {
                'total_patients': total_workflows,
                'high_risk_patients': risk_distribution['high_risk'],
                'medium_risk_patients': risk_distribution['medium_risk'],
                'low_risk_patients': risk_distribution['low_risk']
            },
            'performance_metrics': {
                'contact_completion_rate': round(contact_completion / total_workflows * 100, 1),
                'followup_completion_rate': round(followup_completion / total_workflows * 100, 1),
                'average_risk_score': round(np.mean([w['risk_assessment']['risk_score'] for w in tcm_workflows]), 2),
                'workflows_requiring_urgent_attention': len([w for w in tcm_workflows if w['risk_assessment']['risk_level'] == 'high_risk'])
            },
            'care_team_utilization': {
                'pcp_assignments': sum(1 for w in tcm_workflows if 'Primary Care Provider' in w['care_team_assignments']),
                'care_manager_assignments': sum(1 for w in tcm_workflows if 'Care Manager' in w['care_team_assignments']),
                'pharmacist_assignments': sum(1 for w in tcm_workflows if 'Clinical Pharmacist' in w['care_team_assignments'])
            },
            'risk_factor_analysis': {
                'top_risk_factors': self._analyze_risk_factors(tcm_workflows),
                'intervention_recommendations': self._generate_population_interventions(tcm_workflows)
            }
        }
        
        return dashboard_data
    
    def _analyze_risk_factors(self, workflows: List[Dict]) -> List[Dict]:
        """Analyze most common risk factors across the population."""
        risk_factor_counts = {}
        
        for workflow in workflows:
            for factor in workflow['risk_assessment']['risk_factors']:
                risk_factor_counts[factor] = risk_factor_counts.get(factor, 0) + 1
        
        # Sort by frequency
        sorted_factors = sorted(risk_factor_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'risk_factor': factor, 'frequency': count, 'percentage': round(count/len(workflows)*100, 1)}
            for factor, count in sorted_factors[:10]
        ]
    
    def _generate_population_interventions(self, workflows: List[Dict]) -> List[str]:
        """Generate population-level intervention recommendations."""
        recommendations = []
        total_workflows = len(workflows)
        
        # Analyze risk distribution
        high_risk_count = sum(1 for w in workflows if w['risk_assessment']['risk_level'] == 'high_risk')
        high_risk_percentage = high_risk_count / total_workflows * 100
        
        if high_risk_percentage > 30:
            recommendations.append("Consider expanding care management team - high percentage of high-risk patients")
        
        # Analyze common risk factors
        risk_factors = self._analyze_risk_factors(workflows)
        top_factor = risk_factors[0] if risk_factors else None
        
        if top_factor and top_factor['percentage'] > 40:
            if 'medication' in top_factor['risk_factor'].lower():
                recommendations.append("Implement pharmacy partnership for medication management")
            elif 'social' in top_factor['risk_factor'].lower():
                recommendations.append("Strengthen social services coordination and community partnerships")
            elif 'transportation' in top_factor['risk_factor'].lower():
                recommendations.append("Explore telehealth options and transportation assistance programs")
        
        return recommendations

# Example usage and demonstration
if __name__ == "__main__":
    # Create sample discharge patients
    np.random.seed(42)
    
    sample_discharges = []
    for i in range(50):
        patient = {
            'patient_id': f'DISCH_{i+1:03d}',
            'patient_name': f'Discharge Patient {i+1}',
            'age': np.random.randint(45, 95),
            'length_of_stay': np.random.poisson(5) + 1,
            
            # Clinical conditions (Pearl Health risk factors)
            'heart_failure': np.random.choice([True, False], p=[0.2, 0.8]),
            'copd': np.random.choice([True, False], p=[0.15, 0.85]),
            'diabetes_complications': np.random.choice([True, False], p=[0.25, 0.75]),
            'sepsis': np.random.choice([True, False], p=[0.1, 0.9]),
            'pneumonia': np.random.choice([True, False], p=[0.18, 0.82]),
            
            # Social determinants
            'lives_alone': np.random.choice([True, False], p=[0.3, 0.7]),
            'transportation_barriers': np.random.choice([True, False], p=[0.25, 0.75]),
            'medication_costs': np.random.choice([True, False], p=[0.2, 0.8]),
            'health_literacy_low': np.random.choice([True, False], p=[0.3, 0.7]),
            
            # Utilization patterns
            'frequent_ed_user': np.random.choice([True, False], p=[0.15, 0.85]),
            'multiple_readmissions': np.random.choice([True, False], p=[0.1, 0.9]),
            'multiple_comorbidities': np.random.choice([True, False], p=[0.4, 0.6])
        }
        sample_discharges.append(patient)
    
    # Initialize TCM system
    tcm_manager = TransitionalCareManager()
    
    print("🏥 Pearl Health-Style Transitional Care Management Demo")
    print("=" * 65)
    
    # Create TCM workflows for sample patients
    tcm_workflows = []
    discharge_date = datetime.now() - timedelta(days=1)  # Yesterday's discharges
    
    for patient in sample_discharges:
        workflow = tcm_manager.create_tcm_workflow(patient, discharge_date)
        # Simulate some completed workflows
        if np.random.random() > 0.3:
            workflow['workflow_timeline']['initial_contact']['status'] = 'completed'
        if np.random.random() > 0.5:
            workflow['workflow_timeline']['followup_visit']['status'] = 'completed'
        
        tcm_workflows.append(workflow)
    
    # Show sample high-risk patient workflow
    high_risk_workflows = [w for w in tcm_workflows if w['risk_assessment']['risk_level'] == 'high_risk']
    
    if high_risk_workflows:
        sample_workflow = high_risk_workflows[0]
        print(f"\n📋 Sample High-Risk TCM Workflow:")
        print("-" * 45)
        print(f"Patient: {sample_workflow['patient_name']}")
        print(f"Risk Score: {sample_workflow['risk_assessment']['risk_score']:.2f}")
        print(f"Risk Factors: {len(sample_workflow['risk_assessment']['risk_factors'])}")
        print(f"Care Team: {list(sample_workflow['care_team_assignments'].keys())}")
        print(f"Interventions: {len(sample_workflow['interventions'])}")
        
        print(f"\nWorkflow Timeline:")
        timeline = sample_workflow['workflow_timeline']
        print(f"  Initial Contact: {timeline['initial_contact']['due_date']} ({timeline['initial_contact']['status']})")
        print(f"  Follow-up Visit: {timeline['followup_visit']['due_date']} ({timeline['followup_visit']['status']})")
    
    # Generate dashboard data
    dashboard_data = tcm_manager.generate_tcm_dashboard_data(tcm_workflows)
    
    print(f"\n📊 TCM Program Dashboard:")
    print("-" * 45)
    overview = dashboard_data['program_overview']
    metrics = dashboard_data['performance_metrics']
    
    print(f"Total Patients: {overview['total_patients']}")
    print(f"  High Risk: {overview['high_risk_patients']}")
    print(f"  Medium Risk: {overview['medium_risk_patients']}")
    print(f"  Low Risk: {overview['low_risk_patients']}")
    
    print(f"\nPerformance Metrics:")
    print(f"  Contact Completion: {metrics['contact_completion_rate']}%")
    print(f"  Follow-up Completion: {metrics['followup_completion_rate']}%")
    print(f"  Average Risk Score: {metrics['average_risk_score']}")
    
    print(f"\nTop Risk Factors:")
    for factor in dashboard_data['risk_factor_analysis']['top_risk_factors'][:5]:
        print(f"  {factor['risk_factor']}: {factor['frequency']} patients ({factor['percentage']}%)")
    
    print("\n" + "=" * 65)
    print("Transitional Care Management Demo Complete! 🎉")
    print("This demonstrates Pearl Health-style post-discharge care coordination")
