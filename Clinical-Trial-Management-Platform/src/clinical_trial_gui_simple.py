#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Simplified Site Coordinator Dashboard
Progressive disclosure version - only shows essential tabs for new users
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class SimpleClinicalTrialDashboard:
    def __init__(self, root, user_level="new"):
        self.root = root
        self.root.title("Clinical Trial Management Platform - Site Coordinator Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f5f5')
        
        self.user_level = user_level  # "new", "intermediate", "experienced"
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Sample data
        self.studies = self.load_sample_data()
        self.current_study = None
        
        self.setup_gui()
        self.update_dashboard()
        
    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        self.style.configure('Metric.TLabel', font=('Arial', 10), background='#f5f5f5')
        self.style.configure('Success.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#2e7d32')
        self.style.configure('Warning.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#f57c00')
        self.style.configure('Error.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#d32f2f')
        
    def load_sample_data(self):
        """Load sample clinical trial data"""
        return {
            "studies": [
                {
                    "id": "STUDY-001",
                    "title": "Phase III Oncology Study - Novel Immunotherapy",
                    "sponsor": "BioPharma Innovations",
                    "phase": "Phase III",
                    "status": "Active",
                    "protocol_version": "2.1",
                    "enrollment_target": 300,
                    "enrollment_current": 245,
                    "sites": 12,
                    "start_date": "2024-03-15",
                    "estimated_completion": "2025-12-31",
                    "last_visit": "2025-09-01",
                    "next_visit": "2025-09-08",
                    "compliance_score": 91.2,
                    "data_quality": 95.7
                }
            ],
            "patients": [
                {
                    "id": "P001",
                    "study_id": "STUDY-001",
                    "initials": "J.D.",
                    "age": 45,
                    "gender": "Male",
                    "enrollment_date": "2024-04-15",
                    "last_visit": "2025-09-01",
                    "next_visit": "2025-09-08",
                    "visit_status": "Completed",
                    "compliance": "Excellent"
                },
                {
                    "id": "P002",
                    "study_id": "STUDY-001",
                    "initials": "M.S.",
                    "age": 52,
                    "gender": "Female",
                    "enrollment_date": "2024-05-20",
                    "last_visit": "2025-08-28",
                    "next_visit": "2025-09-05",
                    "visit_status": "Scheduled",
                    "compliance": "Good"
                },
                {
                    "id": "P003",
                    "study_id": "STUDY-001",
                    "initials": "R.K.",
                    "age": 38,
                    "gender": "Male",
                    "enrollment_date": "2024-06-10",
                    "last_visit": "2025-09-01",
                    "next_visit": "2025-09-08",
                    "visit_status": "Overdue",
                    "compliance": "Fair"
                }
            ],
            "alerts": [
                {
                    "id": "A001",
                    "type": "Protocol Deviation",
                    "severity": "High",
                    "study_id": "STUDY-001",
                    "description": "Visit window exceeded for Patient P003",
                    "date": "2025-09-06",
                    "status": "Open"
                },
                {
                    "id": "A002",
                    "type": "Data Query",
                    "severity": "Medium",
                    "study_id": "STUDY-002",
                    "description": "Missing lab values for Patient P002",
                    "date": "2025-09-05",
                    "status": "In Progress"
                }
            ]
        }
    
    def setup_gui(self):
        """Set up the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Main content area
        self.create_main_content(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="Clinical Trial Management Platform", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # User level indicator
        level_text = {
            "new": "👶 New User Experience",
            "intermediate": "📚 Intermediate User", 
            "experienced": "💼 Experienced User"
        }
        level_label = ttk.Label(header_frame, text=level_text.get(self.user_level, "User"), style='Header.TLabel')
        level_label.grid(row=0, column=1, sticky=tk.E)
        
        # Study selector
        study_frame = ttk.Frame(header_frame)
        study_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(study_frame, text="Select Study:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.study_var = tk.StringVar()
        self.study_combo = ttk.Combobox(study_frame, textvariable=self.study_var, state='readonly', width=50)
        self.study_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.study_combo.bind('<<ComboboxSelected>>', self.on_study_selected)
        
        ttk.Button(study_frame, text="🔄 Refresh", command=self.refresh_data).grid(row=0, column=2)
        
        study_frame.columnconfigure(1, weight=1)
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create tabs based on user level
        self.create_tabs()
    
    def create_tabs(self):
        """Create tabs based on user level"""
        # Always show Dashboard
        self.create_dashboard_tab()
        
        # Always show Patients
        self.create_patient_tab()
        
        # Always show Scheduling
        self.create_scheduling_tab()
        
        # Show additional tabs based on user level
        if self.user_level in ["intermediate", "experienced"]:
            self.create_compliance_tab()
            self.create_documents_tab()
        
        if self.user_level == "experienced":
            self.create_drug_management_tab()
    
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Left panel - Study overview
        left_frame = ttk.Frame(dashboard_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Study overview
        overview_frame = ttk.LabelFrame(left_frame, text="Study Overview", padding="10")
        overview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.study_info_text = scrolledtext.ScrolledText(overview_frame, height=15, width=50)
        self.study_info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.study_info_text.config(state=tk.DISABLED)
        
        # Metrics
        metrics_frame = ttk.LabelFrame(left_frame, text="Key Metrics", padding="10")
        metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.enrollment_label = ttk.Label(metrics_frame, text="Enrollment: 0/0 (0%)", style='Metric.TLabel')
        self.enrollment_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.enrollment_progress = ttk.Progressbar(metrics_frame, length=200, mode='determinate')
        self.enrollment_progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.compliance_label = ttk.Label(metrics_frame, text="Compliance Score: 0%", style='Metric.TLabel')
        self.compliance_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.data_quality_label = ttk.Label(metrics_frame, text="Data Quality: 0%", style='Metric.TLabel')
        self.data_quality_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        # Right panel - Alerts and activities
        right_frame = ttk.Frame(dashboard_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Alerts
        alerts_frame = ttk.LabelFrame(right_frame, text="Alerts & Notifications", padding="10")
        alerts_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=('Type', 'Severity', 'Description', 'Date'), show='headings', height=8)
        self.alerts_tree.heading('Type', text='Type')
        self.alerts_tree.heading('Severity', text='Severity')
        self.alerts_tree.heading('Description', text='Description')
        self.alerts_tree.heading('Date', text='Date')
        
        self.alerts_tree.column('Type', width=100)
        self.alerts_tree.column('Severity', width=80)
        self.alerts_tree.column('Description', width=200)
        self.alerts_tree.column('Date', width=100)
        
        self.alerts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Recent activities
        activities_frame = ttk.LabelFrame(right_frame, text="Recent Activities", padding="10")
        activities_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.activities_text = scrolledtext.ScrolledText(activities_frame, height=8, width=50)
        self.activities_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.activities_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.columnconfigure(1, weight=1)
        dashboard_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        overview_frame.columnconfigure(0, weight=1)
        overview_frame.rowconfigure(0, weight=1)
        metrics_frame.columnconfigure(0, weight=1)
        alerts_frame.columnconfigure(0, weight=1)
        alerts_frame.rowconfigure(0, weight=1)
        activities_frame.columnconfigure(0, weight=1)
        activities_frame.rowconfigure(0, weight=1)
    
    def create_patient_tab(self):
        """Create the patient management tab"""
        patient_frame = ttk.Frame(self.notebook)
        self.notebook.add(patient_frame, text="👥 Patients")
        
        # Patient list
        self.patient_tree = ttk.Treeview(patient_frame, columns=('ID', 'Initials', 'Age', 'Gender', 'Enrollment', 'Last Visit', 'Next Visit', 'Status'), show='headings', height=15)
        self.patient_tree.heading('ID', text='Patient ID')
        self.patient_tree.heading('Initials', text='Initials')
        self.patient_tree.heading('Age', text='Age')
        self.patient_tree.heading('Gender', text='Gender')
        self.patient_tree.heading('Enrollment', text='Enrollment Date')
        self.patient_tree.heading('Last Visit', text='Last Visit')
        self.patient_tree.heading('Next Visit', text='Next Visit')
        self.patient_tree.heading('Status', text='Status')
        
        self.patient_tree.column('ID', width=80)
        self.patient_tree.column('Initials', width=80)
        self.patient_tree.column('Age', width=60)
        self.patient_tree.column('Gender', width=80)
        self.patient_tree.column('Enrollment', width=120)
        self.patient_tree.column('Last Visit', width=100)
        self.patient_tree.column('Next Visit', width=100)
        self.patient_tree.column('Status', width=100)
        
        self.patient_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights
        patient_frame.columnconfigure(0, weight=1)
        patient_frame.rowconfigure(0, weight=1)
    
    def create_scheduling_tab(self):
        """Create the scheduling tab"""
        scheduling_frame = ttk.Frame(self.notebook)
        self.notebook.add(scheduling_frame, text="📅 Scheduling")
        
        # Today's schedule
        schedule_frame = ttk.LabelFrame(scheduling_frame, text="Today's Schedule", padding="10")
        schedule_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        schedule_text = """
TODAY'S SCHEDULED VISITS
========================

9:00 AM - Patient P001 (J.D.)
         Visit Type: Follow-up
         Duration: 60 minutes
         Status: Confirmed

11:00 AM - Patient P002 (M.S.)
          Visit Type: Baseline
          Duration: 90 minutes
          Status: Confirmed

2:00 PM - Patient P003 (R.K.)
         Visit Type: Follow-up
         Duration: 60 minutes
         Status: Pending Confirmation

UPCOMING VISITS
===============

Tomorrow (Sep 7):
- 10:00 AM - Patient P001 (J.D.) - Lab Collection
- 3:00 PM - Patient P002 (M.S.) - Follow-up

This Week:
- Sep 8: Patient P001 (J.D.) - Follow-up
- Sep 9: Patient P002 (M.S.) - Follow-up
- Sep 10: Patient P003 (R.K.) - Follow-up
        """
        
        schedule_display = scrolledtext.ScrolledText(schedule_frame, height=20, width=60)
        schedule_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        schedule_display.insert(tk.END, schedule_text)
        schedule_display.config(state=tk.DISABLED)
        
        # Configure grid weights
        scheduling_frame.columnconfigure(0, weight=1)
        scheduling_frame.rowconfigure(0, weight=1)
        schedule_frame.columnconfigure(0, weight=1)
        schedule_frame.rowconfigure(0, weight=1)
    
    def create_compliance_tab(self):
        """Create the compliance tab (intermediate+ users only)"""
        compliance_frame = ttk.Frame(self.notebook)
        self.notebook.add(compliance_frame, text="✅ Compliance")
        
        compliance_text = """
PROTOCOL COMPLIANCE DASHBOARD
=============================

Overall Compliance Score: 91.2%

PROTOCOL ADHERENCE:
- Visit windows: 95% compliance
- Data collection: 89% compliance
- Safety reporting: 98% compliance
- Documentation: 87% compliance

RECENT DEVIATIONS:
- Patient P003: Visit window exceeded (Sep 6)
- Patient P002: Missing lab values (Sep 5)
- Patient P001: Late data entry (Sep 4)

COMPLIANCE ACTIONS:
- Review protocol deviations
- Update training materials
- Schedule monitor visit
- Complete data queries
        """
        
        compliance_display = scrolledtext.ScrolledText(compliance_frame, height=20, width=60)
        compliance_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        compliance_display.insert(tk.END, compliance_text)
        compliance_display.config(state=tk.DISABLED)
        
        # Configure grid weights
        compliance_frame.columnconfigure(0, weight=1)
        compliance_frame.rowconfigure(0, weight=1)
    
    def create_documents_tab(self):
        """Create the documents tab (intermediate+ users only)"""
        documents_frame = ttk.Frame(self.notebook)
        self.notebook.add(documents_frame, text="📄 Documents")
        
        documents_text = """
STUDY DOCUMENTS
===============

PROTOCOL DOCUMENTS:
- Protocol v2.1 (Current)
- Informed Consent v1.3 (Current)
- Case Report Form v1.0 (Draft)

SITE DOCUMENTS:
- Site Manual v1.2 (Current)
- Investigator Brochure v3.0 (Current)
- Safety Report v1.0 (Submitted)

TRAINING MATERIALS:
- GCP Training Certificate (Valid)
- Protocol Training (Completed)
- Safety Training (Completed)

RECENT UPDATES:
- Protocol updated to v2.1 (Aug 15)
- Informed Consent updated (Aug 20)
- Site Manual updated (Aug 25)
        """
        
        documents_display = scrolledtext.ScrolledText(documents_frame, height=20, width=60)
        documents_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        documents_display.insert(tk.END, documents_text)
        documents_display.config(state=tk.DISABLED)
        
        # Configure grid weights
        documents_frame.columnconfigure(0, weight=1)
        documents_frame.rowconfigure(0, weight=1)
    
    def create_drug_management_tab(self):
        """Create the drug management tab (experienced users only)"""
        drug_frame = ttk.Frame(self.notebook)
        self.notebook.add(drug_frame, text="💊 Drug Management")
        
        drug_text = """
DRUG MANAGEMENT DASHBOARD
=========================

CURRENT INVENTORY:
- Study Drug A: 150 units (Batch BATCH-2025-001)
- Study Drug B: 80 units (Batch BATCH-2025-002)
- Placebo: 200 units (Batch BATCH-2025-003)

PENDING REQUESTS:
- Study Drug A: 100 units (Approved)
- Study Drug B: 50 units (Pending)
- Placebo: 75 units (Shipped)

ALERTS:
- Study Drug B: Low stock (80 units)
- All drugs within expiry dates
- Temperature monitoring: Normal

RECENT ACTIVITIES:
- Sep 5: Received Study Drug A shipment
- Sep 4: Updated Study Drug B inventory
- Sep 3: Requested Placebo shipment
        """
        
        drug_display = scrolledtext.ScrolledText(drug_frame, height=20, width=60)
        drug_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        drug_display.insert(tk.END, drug_text)
        drug_display.config(state=tk.DISABLED)
        
        # Configure grid weights
        drug_frame.columnconfigure(0, weight=1)
        drug_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready", style='Metric.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.last_updated_label = ttk.Label(status_frame, text="Last updated: Never", style='Metric.TLabel')
        self.last_updated_label.grid(row=0, column=1, sticky=tk.E)
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        # Update study selector
        study_options = [f"{study['id']} - {study['title']}" for study in self.studies['studies']]
        self.study_combo['values'] = study_options
        if study_options and not self.study_var.get():
            self.study_combo.current(0)
            self.on_study_selected()
        
        # Update study overview
        self.update_study_overview()
        
        # Update metrics
        self.update_enrollment_metrics()
        self.update_compliance_metrics()
        
        # Update alerts
        self.update_alerts()
        
        # Update activities
        self.update_activities()
        
        # Update patient list
        self.update_patient_list()
        
        # Update status
        self.last_updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_study_overview(self):
        """Update study overview information"""
        if not self.current_study:
            return
        
        self.study_info_text.config(state=tk.NORMAL)
        self.study_info_text.delete(1.0, tk.END)
        
        study = self.current_study
        info_text = f"""Study ID: {study['id']}
Title: {study['title']}
Sponsor: {study['sponsor']}
Phase: {study['phase']}
Status: {study['status']}
Protocol Version: {study['protocol_version']}

Enrollment Progress:
• Target: {study['enrollment_target']} patients
• Current: {study['enrollment_current']} patients
• Progress: {(study['enrollment_current']/study['enrollment_target']*100):.1f}%

Study Timeline:
• Start Date: {study['start_date']}
• Estimated Completion: {study['estimated_completion']}
• Last Visit: {study['last_visit']}
• Next Visit: {study['next_visit']}

Performance Metrics:
• Compliance Score: {study['compliance_score']}%
• Data Quality: {study['data_quality']}%
• Active Sites: {study['sites']}"""
        
        self.study_info_text.insert(tk.END, info_text)
        self.study_info_text.config(state=tk.DISABLED)
    
    def update_enrollment_metrics(self):
        """Update enrollment metrics"""
        if not self.current_study:
            return
        
        study = self.current_study
        progress = (study['enrollment_current'] / study['enrollment_target']) * 100
        
        self.enrollment_label.config(text=f"Enrollment: {study['enrollment_current']}/{study['enrollment_target']} ({progress:.1f}%)")
        self.enrollment_progress['value'] = progress
    
    def update_compliance_metrics(self):
        """Update compliance metrics"""
        if not self.current_study:
            return
        
        study = self.current_study
        
        self.compliance_label.config(text=f"Compliance Score: {study['compliance_score']}%", style='Success.TLabel' if study['compliance_score'] >= 95 else 'Warning.TLabel')
        self.data_quality_label.config(text=f"Data Quality: {study['data_quality']}%", style='Success.TLabel' if study['data_quality'] >= 95 else 'Warning.TLabel')
    
    def update_alerts(self):
        """Update alerts list"""
        # Clear existing items
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        
        # Add alerts
        for alert in self.studies['alerts']:
            self.alerts_tree.insert('', 'end', values=(
                alert['type'],
                alert['severity'],
                alert['description'],
                alert['date']
            ))
    
    def update_activities(self):
        """Update recent activities"""
        self.activities_text.config(state=tk.NORMAL)
        self.activities_text.delete(1.0, tk.END)
        
        activities = [
            "Sep 6, 2025 09:15 - Patient P001 visit completed",
            "Sep 6, 2025 08:30 - Daily dashboard refresh",
            "Sep 5, 2025 16:20 - Data query resolved for P002",
            "Sep 5, 2025 14:10 - Visit scheduled for P001 on Sep 12",
            "Sep 5, 2025 11:30 - Study documents updated to v2.1",
            "Sep 4, 2025 15:45 - Site monitoring visit completed",
            "Sep 4, 2025 09:15 - Enrollment target reached for Site 12"
        ]
        
        for activity in activities:
            self.activities_text.insert(tk.END, activity + "\n")
        
        self.activities_text.config(state=tk.DISABLED)
    
    def update_patient_list(self):
        """Update patient list"""
        # Clear existing items
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        # Add patients
        for patient in self.studies['patients']:
            self.patient_tree.insert('', 'end', values=(
                patient['id'],
                patient['initials'],
                patient['age'],
                patient['gender'],
                patient['enrollment_date'],
                patient['last_visit'],
                patient['next_visit'],
                patient['visit_status']
            ))
    
    def on_study_selected(self, event=None):
        """Handle study selection"""
        selection = self.study_var.get()
        if selection:
            study_id = selection.split(' - ')[0]
            self.current_study = next((s for s in self.studies['studies'] if s['id'] == study_id), None)
            self.update_dashboard()
    
    def refresh_data(self):
        """Refresh all data"""
        self.status_label.config(text="Refreshing data...")
        self.update_dashboard()
        self.status_label.config(text="Ready")

def main():
    import sys
    
    # Get user level from command line argument
    user_level = "new"  # default
    if len(sys.argv) > 1:
        user_level = sys.argv[1]
    
    root = tk.Tk()
    app = SimpleClinicalTrialDashboard(root, user_level=user_level)
    root.mainloop()

if __name__ == "__main__":
    main()
