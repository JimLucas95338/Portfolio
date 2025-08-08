"""
Point-of-Care EHR Integration Demo
=================================

Pearl Health-style EHR workflow integration demonstrating how clinical signals
and decision support can be embedded directly into provider workflows.

Key Features:
- In-workflow clinical decision support
- Real-time patient risk assessment
- Care gap alerts at point of care
- Seamless integration with existing EHR systems
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class PointOfCareIntegration:
    """
    Pearl Health-style point-of-care EHR integration system.
    
    Demonstrates how clinical signals and decision support can be embedded
    seamlessly into provider workflows without disrupting existing processes.
    """
    
    def __init__(self):
        self.fhir_base = "https://hapi.fhir.org/baseR4"
        
        # Clinical decision support rules (Pearl Health style)
        self.decision_support_rules = {
            'preventive_care': {
                'annual_wellness_visit': {
                    'condition': 'days_since_last_visit > 365',
                    'alert': 'Patient due for Annual Wellness Visit',
                    'action': 'Schedule AWV within 30 days',
                    'priority': 'medium'
                },
                'cancer_screening': {
                    'condition': 'age >= 50 and no_recent_screening',
                    'alert': 'Colorectal cancer screening overdue',
                    'action': 'Order FIT test or schedule colonoscopy',
                    'priority': 'high'
                }
            },
            'chronic_care': {
                'diabetes_management': {
                    'condition': 'diabetes and last_a1c > 8.0',
                    'alert': 'Diabetes poorly controlled (A1C > 8%)',
                    'action': 'Consider medication adjustment or endocrine referral',
                    'priority': 'high'
                },
                'blood_pressure': {
                    'condition': 'hypertension and last_bp > 140/90',
                    'alert': 'Blood pressure above target',
                    'action': 'Review medications and lifestyle counseling',
                    'priority': 'medium'
                }
            },
            'care_coordination': {
                'post_discharge': {
                    'condition': 'recent_discharge and no_followup',
                    'alert': 'Post-discharge follow-up needed',
                    'action': 'Schedule within 7 days of discharge',
                    'priority': 'urgent'
                },
                'medication_reconciliation': {
                    'condition': 'recent_med_changes and no_reconciliation',
                    'alert': 'Medication reconciliation needed',
                    'action': 'Review and reconcile medications',
                    'priority': 'high'
                }
            }
        }
        
        # Risk scoring factors (simplified)
        self.risk_factors = {
            'age_75_plus': 2.0,
            'multiple_chronic_conditions': 1.8,
            'recent_hospitalization': 2.5,
            'medication_non_adherence': 1.6,
            'social_determinants': 1.4
        }
    
    def assess_patient_risk(self, patient_data: Dict) -> Dict:
        """
        Perform real-time risk assessment using Pearl Health methodology.
        
        Args:
            patient_data: Current patient data from EHR
            
        Returns:
            Risk assessment with scores and recommendations
        """
        base_risk = 1.0
        risk_factors_present = []
        
        # Age-based risk
        age = patient_data.get('age', 0)
        if age >= 75:
            base_risk *= self.risk_factors['age_75_plus']
            risk_factors_present.append('Age 75+')
        
        # Chronic conditions
        chronic_conditions = patient_data.get('chronic_conditions', [])
        if len(chronic_conditions) >= 3:
            base_risk *= self.risk_factors['multiple_chronic_conditions']
            risk_factors_present.append('Multiple chronic conditions')
        
        # Recent utilization
        if patient_data.get('recent_hospitalization', False):
            base_risk *= self.risk_factors['recent_hospitalization']
            risk_factors_present.append('Recent hospitalization')
        
        # Medication adherence
        med_adherence = patient_data.get('medication_adherence', 1.0)
        if med_adherence < 0.8:
            base_risk *= self.risk_factors['medication_non_adherence']
            risk_factors_present.append('Medication non-adherence')
        
        # Social determinants
        if patient_data.get('social_risk_factors', 0) > 2:
            base_risk *= self.risk_factors['social_determinants']
            risk_factors_present.append('Social determinants of health')
        
        # Convert to 0-100 scale
        risk_score = min((base_risk - 1) * 25, 100)
        
        # Determine risk level
        if risk_score >= 75:
            risk_level = 'High'
            risk_color = 'red'
        elif risk_score >= 50:
            risk_level = 'Medium'
            risk_color = 'orange'
        else:
            risk_level = 'Low'
            risk_color = 'green'
        
        return {
            'risk_score': round(risk_score, 1),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'risk_factors': risk_factors_present,
            'requires_intervention': risk_score >= 50
        }
    
    def generate_clinical_alerts(self, patient_data: Dict) -> List[Dict]:
        """
        Generate Pearl Health-style clinical alerts for point-of-care display.
        
        Args:
            patient_data: Current patient data
            
        Returns:
            List of clinical alerts with priorities and actions
        """
        alerts = []
        
        # Check each decision support rule
        for category, rules in self.decision_support_rules.items():
            for rule_name, rule_config in rules.items():
                alert = self._evaluate_rule(patient_data, rule_name, rule_config)
                if alert:
                    alert['category'] = category
                    alerts.append(alert)
        
        # Sort by priority (urgent, high, medium, low)
        priority_order = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
        alerts.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return alerts
    
    def _evaluate_rule(self, patient_data: Dict, rule_name: str, rule_config: Dict) -> Optional[Dict]:
        """Evaluate a specific clinical decision support rule."""
        
        # Simplified rule evaluation (in real implementation, would use proper rule engine)
        triggered = False
        
        if rule_name == 'annual_wellness_visit':
            last_visit = patient_data.get('days_since_last_visit', 0)
            triggered = last_visit > 365
            
        elif rule_name == 'cancer_screening':
            age = patient_data.get('age', 0)
            last_screening = patient_data.get('days_since_cancer_screening', 999)
            triggered = age >= 50 and last_screening > 365
            
        elif rule_name == 'diabetes_management':
            has_diabetes = 'diabetes' in patient_data.get('chronic_conditions', [])
            last_a1c = patient_data.get('last_a1c', 0)
            triggered = has_diabetes and last_a1c > 8.0
            
        elif rule_name == 'blood_pressure':
            has_htn = 'hypertension' in patient_data.get('chronic_conditions', [])
            last_bp_systolic = patient_data.get('last_bp_systolic', 0)
            triggered = has_htn and last_bp_systolic > 140
            
        elif rule_name == 'post_discharge':
            recent_discharge = patient_data.get('recent_discharge', False)
            has_followup = patient_data.get('post_discharge_followup', True)
            triggered = recent_discharge and not has_followup
            
        elif rule_name == 'medication_reconciliation':
            recent_changes = patient_data.get('recent_medication_changes', False)
            reconciled = patient_data.get('medications_reconciled', True)
            triggered = recent_changes and not reconciled
        
        if triggered:
            return {
                'rule_name': rule_name,
                'alert_text': rule_config['alert'],
                'recommended_action': rule_config['action'],
                'priority': rule_config['priority'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        
        return None
    
    def generate_care_recommendations(self, patient_data: Dict, risk_assessment: Dict) -> List[Dict]:
        """
        Generate Pearl Health-style care recommendations based on risk and alerts.
        
        Args:
            patient_data: Patient clinical data
            risk_assessment: Risk assessment results
            
        Returns:
            List of prioritized care recommendations
        """
        recommendations = []
        
        # Risk-based recommendations
        if risk_assessment['risk_level'] == 'High':
            recommendations.append({
                'type': 'care_management',
                'recommendation': 'Enroll in intensive care management program',
                'rationale': f"High risk score ({risk_assessment['risk_score']}) with multiple risk factors",
                'timeline': 'Within 48 hours',
                'care_team_role': 'Care Manager'
            })
        
        # Condition-specific recommendations
        chronic_conditions = patient_data.get('chronic_conditions', [])
        
        if 'diabetes' in chronic_conditions:
            recommendations.append({
                'type': 'diabetes_care',
                'recommendation': 'Comprehensive diabetes care review',
                'rationale': 'Patient has diabetes - ensure optimal management',
                'timeline': 'Next visit',
                'care_team_role': 'PCP + Diabetes Educator'
            })
        
        if 'heart_failure' in chronic_conditions:
            recommendations.append({
                'type': 'heart_failure_mgmt',
                'recommendation': 'Heart failure medication optimization',
                'rationale': 'Evidence-based heart failure management',
                'timeline': 'Within 2 weeks',
                'care_team_role': 'Cardiologist + PCP'
            })
        
        # Preventive care recommendations
        age = patient_data.get('age', 0)
        if age >= 65:
            recommendations.append({
                'type': 'preventive_care',
                'recommendation': 'Annual wellness visit and Medicare health screening',
                'rationale': 'Medicare beneficiary - comprehensive preventive care',
                'timeline': 'Schedule within 30 days',
                'care_team_role': 'PCP + Care Coordinator'
            })
        
        return recommendations[:5]  # Limit to top 5
    
    def create_workflow_summary(self, patient_data: Dict) -> Dict:
        """
        Create Pearl Health-style workflow summary for provider review.
        
        Args:
            patient_data: Complete patient data
            
        Returns:
            Workflow summary with key insights and next steps
        """
        risk_assessment = self.assess_patient_risk(patient_data)
        alerts = self.generate_clinical_alerts(patient_data)
        recommendations = self.generate_care_recommendations(patient_data, risk_assessment)
        
        # Count alerts by priority
        alert_counts = {'urgent': 0, 'high': 0, 'medium': 0, 'low': 0}
        for alert in alerts:
            alert_counts[alert['priority']] += 1
        
        return {
            'patient_summary': {
                'name': patient_data.get('name', 'Unknown Patient'),
                'age': patient_data.get('age', 0),
                'chronic_conditions': len(patient_data.get('chronic_conditions', [])),
                'last_visit': patient_data.get('days_since_last_visit', 0)
            },
            'risk_assessment': risk_assessment,
            'alert_summary': {
                'total_alerts': len(alerts),
                'urgent': alert_counts['urgent'],
                'high': alert_counts['high'],
                'medium': alert_counts['medium'],
                'low': alert_counts['low']
            },
            'active_alerts': alerts[:3],  # Top 3 alerts
            'care_recommendations': recommendations[:3],  # Top 3 recommendations
            'workflow_status': 'needs_attention' if len(alerts) > 0 or risk_assessment['risk_level'] == 'High' else 'routine'
        }

class PointOfCareGUI:
    """GUI demonstration of Pearl Health-style EHR integration."""
    
    def __init__(self):
        self.integration_engine = PointOfCareIntegration()
        self.setup_gui()
        
        # Sample patient data for demonstration
        self.sample_patients = [
            {
                'name': 'Mary Johnson, 78',
                'age': 78,
                'chronic_conditions': ['diabetes', 'hypertension', 'heart_failure'],
                'recent_hospitalization': True,
                'days_since_last_visit': 45,
                'days_since_cancer_screening': 400,
                'last_a1c': 8.5,
                'last_bp_systolic': 155,
                'medication_adherence': 0.7,
                'social_risk_factors': 3,
                'recent_discharge': True,
                'post_discharge_followup': False
            },
            {
                'name': 'Robert Chen, 65',
                'age': 65,
                'chronic_conditions': ['diabetes'],
                'recent_hospitalization': False,
                'days_since_last_visit': 120,
                'days_since_cancer_screening': 200,
                'last_a1c': 7.2,
                'last_bp_systolic': 125,
                'medication_adherence': 0.9,
                'social_risk_factors': 1,
                'recent_discharge': False,
                'post_discharge_followup': True
            },
            {
                'name': 'Sarah Williams, 55',
                'age': 55,
                'chronic_conditions': ['hypertension'],
                'recent_hospitalization': False,
                'days_since_last_visit': 400,
                'days_since_cancer_screening': 800,
                'last_a1c': 6.0,
                'last_bp_systolic': 148,
                'medication_adherence': 0.85,
                'social_risk_factors': 0,
                'recent_discharge': False,
                'post_discharge_followup': True
            }
        ]
        
        self.current_patient_index = 0
        self.load_patient()
    
    def setup_gui(self):
        """Setup the Pearl Health-style EHR integration GUI."""
        self.root = tk.Tk()
        self.root.title("Pearl Health - Point-of-Care Integration Demo")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f8f9fa')
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c5282', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🏥 Pearl Health EHR Integration", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2c5282').pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Patient selection
        patient_frame = tk.Frame(main_frame, bg='#ffffff', relief='ridge', bd=1)
        patient_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(patient_frame, text="Select Patient:", font=('Arial', 12, 'bold'), 
                bg='#ffffff').pack(side='left', padx=10, pady=10)
        
        self.patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(patient_frame, textvariable=self.patient_var, 
                                   values=[p['name'] for p in self.sample_patients],
                                   state='readonly', width=30)
        patient_combo.pack(side='left', padx=10, pady=10)
        patient_combo.bind('<<ComboboxSelected>>', self.on_patient_change)
        
        tk.Button(patient_frame, text="Refresh Analysis", command=self.load_patient,
                 bg='#4299e1', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Risk Assessment Tab
        self.risk_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.risk_frame, text='Risk Assessment')
        
        # Clinical Alerts Tab
        self.alerts_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.alerts_frame, text='Clinical Alerts')
        
        # Care Recommendations Tab
        self.recommendations_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.recommendations_frame, text='Care Recommendations')
        
        # Workflow Summary Tab
        self.workflow_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.workflow_frame, text='Workflow Summary')
    
    def on_patient_change(self, event):
        """Handle patient selection change."""
        selected_name = self.patient_var.get()
        for i, patient in enumerate(self.sample_patients):
            if patient['name'] == selected_name:
                self.current_patient_index = i
                break
        self.load_patient()
    
    def load_patient(self):
        """Load and analyze current patient data."""
        patient_data = self.sample_patients[self.current_patient_index]
        self.patient_var.set(patient_data['name'])
        
        # Generate analysis
        self.workflow_summary = self.integration_engine.create_workflow_summary(patient_data)
        
        # Update all tabs
        self.update_risk_tab()
        self.update_alerts_tab()
        self.update_recommendations_tab()
        self.update_workflow_tab()
    
    def update_risk_tab(self):
        """Update risk assessment display."""
        # Clear existing content
        for widget in self.risk_frame.winfo_children():
            widget.destroy()
        
        risk_data = self.workflow_summary['risk_assessment']
        
        # Risk score display
        risk_header = tk.Frame(self.risk_frame, bg='#ffffff')
        risk_header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(risk_header, text="Patient Risk Assessment", 
                font=('Arial', 14, 'bold'), bg='#ffffff').pack(side='left')
        
        # Risk score badge
        risk_color = risk_data['risk_color']
        risk_badge = tk.Label(risk_header, text=f"{risk_data['risk_level']} Risk ({risk_data['risk_score']})", 
                             font=('Arial', 12, 'bold'), fg='white', bg=risk_color, padx=10, pady=5)
        risk_badge.pack(side='right')
        
        # Risk factors
        factors_frame = tk.Frame(self.risk_frame, bg='#ffffff')
        factors_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(factors_frame, text="Contributing Risk Factors:", 
                font=('Arial', 12, 'bold'), bg='#ffffff').pack(anchor='w')
        
        if risk_data['risk_factors']:
            for factor in risk_data['risk_factors']:
                tk.Label(factors_frame, text=f"• {factor}", 
                        font=('Arial', 10), bg='#ffffff', fg='#e53e3e').pack(anchor='w', padx=20)
        else:
            tk.Label(factors_frame, text="• No significant risk factors identified", 
                    font=('Arial', 10), bg='#ffffff', fg='#38a169').pack(anchor='w', padx=20)
    
    def update_alerts_tab(self):
        """Update clinical alerts display."""
        # Clear existing content
        for widget in self.alerts_frame.winfo_children():
            widget.destroy()
        
        alerts = self.workflow_summary['active_alerts']
        
        # Alerts header
        alerts_header = tk.Frame(self.alerts_frame, bg='#ffffff')
        alerts_header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(alerts_header, text="Active Clinical Alerts", 
                font=('Arial', 14, 'bold'), bg='#ffffff').pack(side='left')
        
        alert_count = self.workflow_summary['alert_summary']['total_alerts']
        tk.Label(alerts_header, text=f"({alert_count} total)", 
                font=('Arial', 12), bg='#ffffff', fg='#666').pack(side='left', padx=10)
        
        # Alert list
        alerts_list = tk.Frame(self.alerts_frame, bg='#ffffff')
        alerts_list.pack(fill='both', expand=True, padx=20, pady=10)
        
        if alerts:
            for i, alert in enumerate(alerts):
                alert_item = tk.Frame(alerts_list, bg='#fff5f5', relief='ridge', bd=1)
                alert_item.pack(fill='x', pady=5)
                
                # Priority badge
                priority_colors = {'urgent': '#e53e3e', 'high': '#f56500', 'medium': '#d69e2e', 'low': '#38a169'}
                priority_color = priority_colors.get(alert['priority'], '#666')
                
                tk.Label(alert_item, text=alert['priority'].upper(), 
                        font=('Arial', 9, 'bold'), fg='white', bg=priority_color, 
                        padx=8, pady=2).pack(side='left', padx=10, pady=10)
                
                # Alert content
                content_frame = tk.Frame(alert_item, bg='#fff5f5')
                content_frame.pack(side='left', fill='x', expand=True, padx=10, pady=10)
                
                tk.Label(content_frame, text=alert['alert_text'], 
                        font=('Arial', 11, 'bold'), bg='#fff5f5').pack(anchor='w')
                tk.Label(content_frame, text=f"Action: {alert['recommended_action']}", 
                        font=('Arial', 10), bg='#fff5f5', fg='#666').pack(anchor='w')
        else:
            tk.Label(alerts_list, text="✅ No active clinical alerts", 
                    font=('Arial', 12), bg='#ffffff', fg='#38a169').pack(pady=50)
    
    def update_recommendations_tab(self):
        """Update care recommendations display."""
        # Clear existing content
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()
        
        recommendations = self.workflow_summary['care_recommendations']
        
        # Recommendations header
        rec_header = tk.Frame(self.recommendations_frame, bg='#ffffff')
        rec_header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(rec_header, text="Care Recommendations", 
                font=('Arial', 14, 'bold'), bg='#ffffff').pack(side='left')
        
        # Recommendations list
        rec_list = tk.Frame(self.recommendations_frame, bg='#ffffff')
        rec_list.pack(fill='both', expand=True, padx=20, pady=10)
        
        for i, rec in enumerate(recommendations):
            rec_item = tk.Frame(rec_list, bg='#f7fafc', relief='ridge', bd=1)
            rec_item.pack(fill='x', pady=8)
            
            # Recommendation content
            tk.Label(rec_item, text=f"{i+1}. {rec['recommendation']}", 
                    font=('Arial', 11, 'bold'), bg='#f7fafc').pack(anchor='w', padx=15, pady=5)
            tk.Label(rec_item, text=f"Rationale: {rec['rationale']}", 
                    font=('Arial', 10), bg='#f7fafc', fg='#666').pack(anchor='w', padx=15)
            tk.Label(rec_item, text=f"Timeline: {rec['timeline']} | Care Team: {rec['care_team_role']}", 
                    font=('Arial', 9), bg='#f7fafc', fg='#4a5568').pack(anchor='w', padx=15, pady=5)
    
    def update_workflow_tab(self):
        """Update workflow summary display."""
        # Clear existing content
        for widget in self.workflow_frame.winfo_children():
            widget.destroy()
        
        summary = self.workflow_summary
        
        # Workflow header
        workflow_header = tk.Frame(self.workflow_frame, bg='#ffffff')
        workflow_header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(workflow_header, text="Workflow Summary", 
                font=('Arial', 14, 'bold'), bg='#ffffff').pack(side='left')
        
        status = summary['workflow_status']
        status_color = '#e53e3e' if status == 'needs_attention' else '#38a169'
        tk.Label(workflow_header, text=status.replace('_', ' ').title(), 
                font=('Arial', 12, 'bold'), fg=status_color, bg='#ffffff').pack(side='right')
        
        # Summary grid
        grid_frame = tk.Frame(self.workflow_frame, bg='#ffffff')
        grid_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Patient info
        patient_info = summary['patient_summary']
        info_frame = tk.LabelFrame(grid_frame, text="Patient Information", 
                                  font=('Arial', 11, 'bold'), bg='#ffffff')
        info_frame.pack(fill='x', pady=10)
        
        tk.Label(info_frame, text=f"Age: {patient_info['age']} years", 
                font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Chronic Conditions: {patient_info['chronic_conditions']}", 
                font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=10, pady=2)
        tk.Label(info_frame, text=f"Days Since Last Visit: {patient_info['last_visit']}", 
                font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=10, pady=2)
        
        # Alert summary
        alert_summary = summary['alert_summary']
        alert_frame = tk.LabelFrame(grid_frame, text="Alert Summary", 
                                   font=('Arial', 11, 'bold'), bg='#ffffff')
        alert_frame.pack(fill='x', pady=10)
        
        tk.Label(alert_frame, text=f"Total Alerts: {alert_summary['total_alerts']}", 
                font=('Arial', 10), bg='#ffffff').pack(anchor='w', padx=10, pady=2)
        if alert_summary['urgent'] > 0:
            tk.Label(alert_frame, text=f"Urgent: {alert_summary['urgent']}", 
                    font=('Arial', 10, 'bold'), bg='#ffffff', fg='#e53e3e').pack(anchor='w', padx=10, pady=2)
        if alert_summary['high'] > 0:
            tk.Label(alert_frame, text=f"High Priority: {alert_summary['high']}", 
                    font=('Arial', 10), bg='#ffffff', fg='#f56500').pack(anchor='w', padx=10, pady=2)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

# Example usage and demonstration
if __name__ == "__main__":
    print("🏥 Pearl Health Point-of-Care EHR Integration Demo")
    print("=" * 55)
    print("Launching interactive demonstration...")
    print("This shows how Pearl Health-style clinical signals")
    print("can be embedded seamlessly into provider workflows.")
    print("=" * 55)
    
    # Launch the GUI
    app = PointOfCareGUI()
    app.run()
