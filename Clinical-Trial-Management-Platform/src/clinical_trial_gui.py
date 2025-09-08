#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Site Coordinator Dashboard
A comprehensive GUI application for managing clinical trial operations at research sites.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class ClinicalTrialDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Trial Management Platform - Site Coordinator Dashboard")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f5f5')
        
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
                    "enrollment_target": 300,
                    "enrollment_current": 187,
                    "sites": 25,
                    "start_date": "2024-03-15",
                    "estimated_completion": "2025-12-31",
                    "protocol_version": "v2.1",
                    "last_visit": "2025-09-05",
                    "next_visit": "2025-09-12",
                    "compliance_score": 94.5,
                    "data_quality": 98.2
                },
                {
                    "id": "STUDY-002", 
                    "title": "Cardiovascular Outcomes Study",
                    "sponsor": "CardioMed Solutions",
                    "phase": "Phase IV",
                    "status": "Active",
                    "enrollment_target": 500,
                    "enrollment_current": 423,
                    "sites": 40,
                    "start_date": "2023-11-01",
                    "estimated_completion": "2025-06-30",
                    "protocol_version": "v1.3",
                    "last_visit": "2025-09-03",
                    "next_visit": "2025-09-10",
                    "compliance_score": 97.8,
                    "data_quality": 99.1
                },
                {
                    "id": "STUDY-003",
                    "title": "Rare Disease Treatment Study",
                    "sponsor": "RareDx Therapeutics",
                    "phase": "Phase II",
                    "status": "Recruiting",
                    "enrollment_target": 80,
                    "enrollment_current": 23,
                    "sites": 12,
                    "start_date": "2025-01-15",
                    "estimated_completion": "2026-08-31",
                    "protocol_version": "v1.0",
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
                    "last_visit": "2025-09-05",
                    "next_visit": "2025-09-12",
                    "visit_status": "Scheduled",
                    "compliance": "Good"
                },
                {
                    "id": "P002",
                    "study_id": "STUDY-001", 
                    "initials": "M.S.",
                    "age": 52,
                    "gender": "Female",
                    "enrollment_date": "2024-05-20",
                    "last_visit": "2025-09-03",
                    "next_visit": "2025-09-10",
                    "visit_status": "Completed",
                    "compliance": "Excellent"
                },
                {
                    "id": "P003",
                    "study_id": "STUDY-002",
                    "initials": "R.K.",
                    "age": 38,
                    "gender": "Male",
                    "enrollment_date": "2024-01-10",
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
                },
                {
                    "id": "A003",
                    "type": "Enrollment Alert",
                    "severity": "Low",
                    "study_id": "STUDY-003",
                    "description": "Enrollment below target for Site 12",
                    "date": "2025-09-04",
                    "status": "Open"
                }
            ],
            "drug_requests": [
                {
                    "id": "DR-001",
                    "drug_name": "Study Drug A",
                    "quantity": 100,
                    "requested_by": "Dr. Sarah Johnson",
                    "request_date": "2025-09-03",
                    "status": "Approved",
                    "received_date": "2025-09-05",
                    "batch_number": "BATCH-2025-001",
                    "expiry_date": "2026-03-15"
                },
                {
                    "id": "DR-002",
                    "drug_name": "Study Drug B",
                    "quantity": 50,
                    "requested_by": "Dr. Sarah Johnson",
                    "request_date": "2025-09-02",
                    "status": "Pending",
                    "received_date": None,
                    "batch_number": None,
                    "expiry_date": None
                },
                {
                    "id": "DR-003",
                    "drug_name": "Placebo",
                    "quantity": 75,
                    "requested_by": "Dr. Sarah Johnson",
                    "request_date": "2025-09-01",
                    "status": "Shipped",
                    "received_date": None,
                    "batch_number": "BATCH-2025-003",
                    "expiry_date": "2026-08-10"
                }
            ],
            "drug_inventory": [
                {
                    "drug_name": "Study Drug A",
                    "current_stock": 150,
                    "batch_number": "BATCH-2025-001",
                    "expiry_date": "2026-03-15",
                    "storage_location": "Refrigerator A",
                    "last_updated": "2025-09-05"
                },
                {
                    "drug_name": "Study Drug B",
                    "current_stock": 80,
                    "batch_number": "BATCH-2025-002",
                    "expiry_date": "2026-05-20",
                    "storage_location": "Room Temperature Storage",
                    "last_updated": "2025-09-04"
                },
                {
                    "drug_name": "Placebo",
                    "current_stock": 200,
                    "batch_number": "BATCH-2025-003",
                    "expiry_date": "2026-08-10",
                    "storage_location": "Room Temperature Storage",
                    "last_updated": "2025-09-03"
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
        
        # User info
        user_label = ttk.Label(header_frame, text="Site Coordinator: Dr. Sarah Johnson | Site: Boston Medical Center", style='Metric.TLabel')
        user_label.grid(row=1, column=0, sticky=tk.W)
        
        # Study selector
        study_frame = ttk.Frame(header_frame)
        study_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        
        ttk.Label(study_frame, text="Active Study:", style='Header.TLabel').grid(row=0, column=0, padx=(0, 5))
        
        self.study_var = tk.StringVar()
        self.study_combo = ttk.Combobox(study_frame, textvariable=self.study_var, width=40, state='readonly')
        self.study_combo.grid(row=0, column=1)
        self.study_combo.bind('<<ComboboxSelected>>', self.on_study_selected)
        
        # Refresh button
        refresh_btn = ttk.Button(study_frame, text="Refresh", command=self.refresh_data)
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Dashboard tab
        self.create_dashboard_tab()
        
        # Patient Management tab
        self.create_patient_tab()
        
        # Visit Scheduling tab
        self.create_scheduling_tab()
        
        # Compliance tab
        self.create_compliance_tab()
        
        # Documents tab
        self.create_documents_tab()
        
        # Drug Management tab
        self.create_drug_management_tab()
    
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Left panel - Key metrics
        left_frame = ttk.Frame(dashboard_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Study overview
        self.create_study_overview(left_frame)
        
        # Enrollment metrics
        self.create_enrollment_metrics(left_frame)
        
        # Compliance metrics
        self.create_compliance_metrics(left_frame)
        
        # Right panel - Alerts and activities
        right_frame = ttk.Frame(dashboard_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Alerts
        self.create_alerts_panel(right_frame)
        
        # Recent activities
        self.create_activities_panel(right_frame)
        
        # Configure grid weights
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.columnconfigure(1, weight=1)
        dashboard_frame.rowconfigure(0, weight=1)
    
    def create_study_overview(self, parent):
        """Create study overview section"""
        overview_frame = ttk.LabelFrame(parent, text="Study Overview", padding="10")
        overview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.study_info_text = scrolledtext.ScrolledText(overview_frame, height=8, width=50)
        self.study_info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.study_info_text.config(state=tk.DISABLED)
    
    def create_enrollment_metrics(self, parent):
        """Create enrollment metrics section"""
        enrollment_frame = ttk.LabelFrame(parent, text="Enrollment Metrics", padding="10")
        enrollment_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Enrollment progress
        self.enrollment_label = ttk.Label(enrollment_frame, text="", style='Metric.TLabel')
        self.enrollment_label.grid(row=0, column=0, sticky=tk.W)
        
        # Progress bar
        self.enrollment_progress = ttk.Progressbar(enrollment_frame, length=300, mode='determinate')
        self.enrollment_progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Enrollment by site
        self.site_enrollment_label = ttk.Label(enrollment_frame, text="", style='Metric.TLabel')
        self.site_enrollment_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
    def create_compliance_metrics(self, parent):
        """Create compliance metrics section"""
        compliance_frame = ttk.LabelFrame(parent, text="Compliance Metrics", padding="10")
        compliance_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Compliance score
        self.compliance_label = ttk.Label(compliance_frame, text="", style='Metric.TLabel')
        self.compliance_label.grid(row=0, column=0, sticky=tk.W)
        
        # Data quality
        self.data_quality_label = ttk.Label(compliance_frame, text="", style='Metric.TLabel')
        self.data_quality_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Protocol adherence
        self.protocol_label = ttk.Label(compliance_frame, text="", style='Metric.TLabel')
        self.protocol_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
    
    def create_alerts_panel(self, parent):
        """Create alerts panel"""
        alerts_frame = ttk.LabelFrame(parent, text="Alerts & Notifications", padding="10")
        alerts_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Alerts list
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=('Type', 'Severity', 'Description', 'Date'), show='headings', height=8)
        self.alerts_tree.heading('Type', text='Type')
        self.alerts_tree.heading('Severity', text='Severity')
        self.alerts_tree.heading('Description', text='Description')
        self.alerts_tree.heading('Date', text='Date')
        
        self.alerts_tree.column('Type', width=120)
        self.alerts_tree.column('Severity', width=80)
        self.alerts_tree.column('Description', width=200)
        self.alerts_tree.column('Date', width=100)
        
        self.alerts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for alerts
        alerts_scrollbar = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, command=self.alerts_tree.yview)
        alerts_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.alerts_tree.configure(yscrollcommand=alerts_scrollbar.set)
        
        # Alert actions
        alert_actions_frame = ttk.Frame(alerts_frame)
        alert_actions_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(alert_actions_frame, text="View Details", command=self.view_alert_details).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(alert_actions_frame, text="Mark Resolved", command=self.mark_alert_resolved).grid(row=0, column=1)
        
        # Configure grid weights
        alerts_frame.columnconfigure(0, weight=1)
        alerts_frame.rowconfigure(0, weight=1)
    
    def create_activities_panel(self, parent):
        """Create recent activities panel"""
        activities_frame = ttk.LabelFrame(parent, text="Recent Activities", padding="10")
        activities_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.activities_text = scrolledtext.ScrolledText(activities_frame, height=8, width=50)
        self.activities_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.activities_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        activities_frame.columnconfigure(0, weight=1)
        activities_frame.rowconfigure(0, weight=1)
    
    def create_patient_tab(self):
        """Create patient management tab"""
        patient_frame = ttk.Frame(self.notebook)
        self.notebook.add(patient_frame, text="Patient Management")
        
        # Patient list
        patient_list_frame = ttk.LabelFrame(patient_frame, text="Patient List", padding="10")
        patient_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Patient treeview
        self.patient_tree = ttk.Treeview(patient_list_frame, columns=('ID', 'Initials', 'Age', 'Gender', 'Enrollment', 'Last Visit', 'Next Visit', 'Status'), show='headings', height=15)
        
        for col in ('ID', 'Initials', 'Age', 'Gender', 'Enrollment', 'Last Visit', 'Next Visit', 'Status'):
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=100)
        
        self.patient_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Patient actions
        patient_actions_frame = ttk.Frame(patient_list_frame)
        patient_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(patient_actions_frame, text="Add Patient", command=self.add_patient).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(patient_actions_frame, text="Edit Patient", command=self.edit_patient).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(patient_actions_frame, text="Schedule Visit", command=self.schedule_visit).grid(row=0, column=2)
        
        # Patient details
        patient_details_frame = ttk.LabelFrame(patient_frame, text="Patient Details", padding="10")
        patient_details_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.patient_details_text = scrolledtext.ScrolledText(patient_details_frame, height=15, width=50)
        self.patient_details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.patient_details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        patient_frame.columnconfigure(0, weight=1)
        patient_frame.columnconfigure(1, weight=1)
        patient_frame.rowconfigure(0, weight=1)
        patient_list_frame.columnconfigure(0, weight=1)
        patient_list_frame.rowconfigure(0, weight=1)
        patient_details_frame.columnconfigure(0, weight=1)
        patient_details_frame.rowconfigure(0, weight=1)
    
    def create_scheduling_tab(self):
        """Create visit scheduling tab"""
        scheduling_frame = ttk.Frame(self.notebook)
        self.notebook.add(scheduling_frame, text="Visit Scheduling")
        
        # Calendar view placeholder
        calendar_frame = ttk.LabelFrame(scheduling_frame, text="Visit Calendar", padding="10")
        calendar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        calendar_text = scrolledtext.ScrolledText(calendar_frame, height=20, width=60)
        calendar_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        calendar_text.insert(tk.END, "Visit Calendar View\n\n")
        calendar_text.insert(tk.END, "September 2025\n")
        calendar_text.insert(tk.END, "Mon  Tue  Wed  Thu  Fri  Sat  Sun\n")
        calendar_text.insert(tk.END, " 1    2    3    4    5    6    7\n")
        calendar_text.insert(tk.END, " 8    9   10   11   12   13   14\n")
        calendar_text.insert(tk.END, "15   16   17   18   19   20   21\n")
        calendar_text.insert(tk.END, "22   23   24   25   26   27   28\n")
        calendar_text.insert(tk.END, "29   30\n\n")
        calendar_text.insert(tk.END, "Scheduled Visits:\n")
        calendar_text.insert(tk.END, "Sep 10: Patient P001 - Follow-up Visit\n")
        calendar_text.insert(tk.END, "Sep 12: Patient P002 - Screening Visit\n")
        calendar_text.insert(tk.END, "Sep 15: Patient P003 - End of Study Visit\n")
        calendar_text.config(state=tk.DISABLED)
        
        # Scheduling controls
        controls_frame = ttk.LabelFrame(scheduling_frame, text="Scheduling Controls", padding="10")
        controls_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(controls_frame, text="Patient:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        patient_combo = ttk.Combobox(controls_frame, values=["P001 - J.D.", "P002 - M.S.", "P003 - R.K."], state='readonly')
        patient_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(controls_frame, text="Visit Type:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        visit_combo = ttk.Combobox(controls_frame, values=["Screening", "Baseline", "Follow-up", "End of Study"], state='readonly')
        visit_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(controls_frame, text="Date:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        date_entry = ttk.Entry(controls_frame)
        date_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(controls_frame, text="Time:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        time_entry = ttk.Entry(controls_frame)
        time_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(controls_frame, text="Schedule Visit", command=self.schedule_new_visit).grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        # Configure grid weights
        scheduling_frame.columnconfigure(0, weight=2)
        scheduling_frame.columnconfigure(1, weight=1)
        scheduling_frame.rowconfigure(0, weight=1)
        calendar_frame.columnconfigure(0, weight=1)
        calendar_frame.rowconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)
    
    def create_compliance_tab(self):
        """Create compliance monitoring tab"""
        compliance_frame = ttk.Frame(self.notebook)
        self.notebook.add(compliance_frame, text="Compliance")
        
        # Protocol adherence
        protocol_frame = ttk.LabelFrame(compliance_frame, text="Protocol Adherence", padding="10")
        protocol_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        protocol_text = scrolledtext.ScrolledText(protocol_frame, height=15, width=50)
        protocol_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        protocol_text.insert(tk.END, "Protocol Compliance Summary\n\n")
        protocol_text.insert(tk.END, "Overall Compliance Score: 94.5%\n\n")
        protocol_text.insert(tk.END, "Key Metrics:\n")
        protocol_text.insert(tk.END, "• Visit Window Compliance: 96.2%\n")
        protocol_text.insert(tk.END, "• Protocol Deviation Rate: 3.8%\n")
        protocol_text.insert(tk.END, "• Data Entry Timeliness: 98.1%\n")
        protocol_text.insert(tk.END, "• Documentation Completeness: 95.3%\n\n")
        protocol_text.insert(tk.END, "Recent Deviations:\n")
        protocol_text.insert(tk.END, "• Sep 5: Visit window exceeded for P003\n")
        protocol_text.insert(tk.END, "• Sep 3: Missing informed consent for P001\n")
        protocol_text.insert(tk.END, "• Sep 1: Protocol violation - incorrect dosing\n")
        protocol_text.config(state=tk.DISABLED)
        
        # Data quality
        data_quality_frame = ttk.LabelFrame(compliance_frame, text="Data Quality", padding="10")
        data_quality_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        data_quality_text = scrolledtext.ScrolledText(data_quality_frame, height=15, width=50)
        data_quality_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_quality_text.insert(tk.END, "Data Quality Metrics\n\n")
        data_quality_text.insert(tk.END, "Overall Data Quality: 98.2%\n\n")
        data_quality_text.insert(tk.END, "Quality Indicators:\n")
        data_quality_text.insert(tk.END, "• Missing Data Rate: 1.8%\n")
        data_quality_text.insert(tk.END, "• Query Resolution Time: 2.3 days\n")
        data_quality_text.insert(tk.END, "• Data Entry Accuracy: 99.1%\n")
        data_quality_text.insert(tk.END, "• Source Data Verification: 97.5%\n\n")
        data_quality_text.insert(tk.END, "Open Queries:\n")
        data_quality_text.insert(tk.END, "• P002: Missing lab values (2 days)\n")
        data_quality_text.insert(tk.END, "• P001: Incomplete adverse event form\n")
        data_quality_text.insert(tk.END, "• P003: Data discrepancy in visit notes\n")
        data_quality_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        compliance_frame.columnconfigure(0, weight=1)
        compliance_frame.columnconfigure(1, weight=1)
        compliance_frame.rowconfigure(0, weight=1)
        protocol_frame.columnconfigure(0, weight=1)
        protocol_frame.rowconfigure(0, weight=1)
        data_quality_frame.columnconfigure(0, weight=1)
        data_quality_frame.rowconfigure(0, weight=1)
    
    def create_documents_tab(self):
        """Create document management tab"""
        documents_frame = ttk.Frame(self.notebook)
        self.notebook.add(documents_frame, text="Documents")
        
        # Document list
        doc_list_frame = ttk.LabelFrame(documents_frame, text="Study Documents", padding="10")
        doc_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Document treeview
        self.doc_tree = ttk.Treeview(doc_list_frame, columns=('Name', 'Type', 'Version', 'Status', 'Date'), show='headings', height=15)
        
        for col in ('Name', 'Type', 'Version', 'Status', 'Date'):
            self.doc_tree.heading(col, text=col)
            self.doc_tree.column(col, width=120)
        
        self.doc_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Document actions
        doc_actions_frame = ttk.Frame(doc_list_frame)
        doc_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(doc_actions_frame, text="Upload Document", command=self.upload_document).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(doc_actions_frame, text="Download", command=self.download_document).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(doc_actions_frame, text="View", command=self.view_document).grid(row=0, column=2)
        
        # Document details
        doc_details_frame = ttk.LabelFrame(documents_frame, text="Document Details", padding="10")
        doc_details_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.doc_details_text = scrolledtext.ScrolledText(doc_details_frame, height=15, width=50)
        self.doc_details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.doc_details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        documents_frame.columnconfigure(0, weight=1)
        documents_frame.columnconfigure(1, weight=1)
        documents_frame.rowconfigure(0, weight=1)
        doc_list_frame.columnconfigure(0, weight=1)
        doc_list_frame.rowconfigure(0, weight=1)
        doc_details_frame.columnconfigure(0, weight=1)
        doc_details_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready", style='Metric.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Last updated
        self.last_updated_label = ttk.Label(status_frame, text="", style='Metric.TLabel')
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
        
        # Update enrollment metrics
        self.update_enrollment_metrics()
        
        # Update compliance metrics
        self.update_compliance_metrics()
        
        # Update alerts
        self.update_alerts()
        
        # Update activities
        self.update_activities()
        
        # Update patient list
        self.update_patient_list()
        
        # Update document list
        self.update_document_list()
        
        # Update drug management
        self.update_drug_requests()
        self.update_drug_inventory()
        
        # Update status
        self.last_updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_study_overview(self):
        """Update study overview section"""
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
        
        self.site_enrollment_label.config(text=f"Average per site: {study['enrollment_current']/study['sites']:.1f} patients")
    
    def update_compliance_metrics(self):
        """Update compliance metrics"""
        if not self.current_study:
            return
        
        study = self.current_study
        
        self.compliance_label.config(text=f"Compliance Score: {study['compliance_score']}%", style='Success.TLabel' if study['compliance_score'] >= 95 else 'Warning.TLabel')
        self.data_quality_label.config(text=f"Data Quality: {study['data_quality']}%", style='Success.TLabel' if study['data_quality'] >= 95 else 'Warning.TLabel')
        self.protocol_label.config(text=f"Protocol Adherence: {study['compliance_score']}%", style='Success.TLabel' if study['compliance_score'] >= 95 else 'Warning.TLabel')
    
    def update_alerts(self):
        """Update alerts list"""
        # Clear existing items
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        
        # Add alerts
        for alert in self.studies['alerts']:
            severity_color = 'red' if alert['severity'] == 'High' else 'orange' if alert['severity'] == 'Medium' else 'green'
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
            "Sep 6, 2025 14:30 - Patient P001 visit completed",
            "Sep 6, 2025 12:15 - Protocol deviation alert for P003",
            "Sep 6, 2025 10:45 - New patient P004 enrolled in STUDY-001",
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
            status_color = 'green' if patient['visit_status'] == 'Completed' else 'orange' if patient['visit_status'] == 'Scheduled' else 'red'
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
    
    def update_document_list(self):
        """Update document list"""
        # Clear existing items
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)
        
        # Sample documents
        documents = [
            ("Protocol v2.1", "Protocol", "2.1", "Approved", "2025-08-15"),
            ("Informed Consent", "Consent", "1.3", "Current", "2025-08-20"),
            ("Case Report Form", "CRF", "1.0", "Draft", "2025-09-01"),
            ("Site Manual", "Manual", "1.2", "Current", "2025-08-25"),
            ("Safety Report", "Safety", "1.0", "Submitted", "2025-09-05")
        ]
        
        for doc in documents:
            self.doc_tree.insert('', 'end', values=doc)
    
    def create_drug_management_tab(self):
        """Create drug management tab"""
        drug_frame = ttk.Frame(self.notebook)
        self.notebook.add(drug_frame, text="💊 Drug Management")
        
        # Left panel - Drug requests
        left_frame = ttk.Frame(drug_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Drug requests
        requests_frame = ttk.LabelFrame(left_frame, text="Drug Requests", padding="10")
        requests_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.drug_requests_tree = ttk.Treeview(requests_frame, columns=('Drug', 'Quantity', 'Requested By', 'Date', 'Status'), show='headings', height=8)
        self.drug_requests_tree.heading('Drug', text='Drug Name')
        self.drug_requests_tree.heading('Quantity', text='Quantity')
        self.drug_requests_tree.heading('Requested By', text='Requested By')
        self.drug_requests_tree.heading('Date', text='Request Date')
        self.drug_requests_tree.heading('Status', text='Status')
        
        self.drug_requests_tree.column('Drug', width=120)
        self.drug_requests_tree.column('Quantity', width=80)
        self.drug_requests_tree.column('Requested By', width=120)
        self.drug_requests_tree.column('Date', width=100)
        self.drug_requests_tree.column('Status', width=100)
        
        self.drug_requests_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Drug request actions
        request_actions_frame = ttk.Frame(requests_frame)
        request_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(request_actions_frame, text="➕ New Request", command=self.new_drug_request).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(request_actions_frame, text="✅ Mark Received", command=self.mark_drug_received).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(request_actions_frame, text="📋 View Details", command=self.view_drug_request_details).grid(row=0, column=2)
        
        # Current inventory
        inventory_frame = ttk.LabelFrame(left_frame, text="Current Inventory", padding="10")
        inventory_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.inventory_text = scrolledtext.ScrolledText(inventory_frame, height=8, width=50)
        self.inventory_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.inventory_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        requests_frame.columnconfigure(0, weight=1)
        requests_frame.rowconfigure(0, weight=1)
        inventory_frame.columnconfigure(0, weight=1)
        inventory_frame.rowconfigure(0, weight=1)
        
        # Right panel - Drug details and actions
        right_frame = ttk.Frame(drug_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Drug details
        details_frame = ttk.LabelFrame(right_frame, text="Drug Request Details", padding="10")
        details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.drug_details_text = scrolledtext.ScrolledText(details_frame, height=20, width=60)
        self.drug_details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.drug_details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        drug_frame.columnconfigure(0, weight=1)
        drug_frame.columnconfigure(1, weight=1)
        drug_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
    
    def update_drug_requests(self):
        """Update drug requests list"""
        # Clear existing items
        for item in self.drug_requests_tree.get_children():
            self.drug_requests_tree.delete(item)
        
        # Add drug requests
        for request in self.studies['drug_requests']:
            status_color = 'green' if request['status'] == 'Approved' else 'orange' if request['status'] == 'Pending' else 'blue' if request['status'] == 'Shipped' else 'red'
            self.drug_requests_tree.insert('', 'end', values=(
                request['drug_name'],
                request['quantity'],
                request['requested_by'],
                request['request_date'],
                request['status']
            ))
    
    def update_drug_inventory(self):
        """Update drug inventory display"""
        self.inventory_text.config(state=tk.NORMAL)
        self.inventory_text.delete(1.0, tk.END)
        
        inventory_info = "CURRENT DRUG INVENTORY\n"
        inventory_info += "=====================\n\n"
        
        for drug in self.studies['drug_inventory']:
            inventory_info += f"Drug: {drug['drug_name']}\n"
            inventory_info += f"Current Stock: {drug['current_stock']} units\n"
            inventory_info += f"Batch: {drug['batch_number']}\n"
            inventory_info += f"Expiry: {drug['expiry_date']}\n"
            inventory_info += f"Storage: {drug['storage_location']}\n"
            inventory_info += f"Last Updated: {drug['last_updated']}\n\n"
        
        inventory_info += "ALERTS:\n"
        inventory_info += "• Study Drug B: Low stock (80 units)\n"
        inventory_info += "• All drugs within expiry dates\n"
        inventory_info += "• Temperature monitoring: Normal\n"
        
        self.inventory_text.insert(tk.END, inventory_info)
        self.inventory_text.config(state=tk.DISABLED)
    
    def new_drug_request(self):
        """Create new drug request"""
        messagebox.showinfo("New Drug Request", "Drug Request Form would open here.\n\nRequired Information:\n• Drug name and strength\n• Requested quantity\n• Justification for request\n• Urgency level\n• Expected delivery date\n• Storage requirements")
    
    def mark_drug_received(self):
        """Mark selected drug request as received"""
        selection = self.drug_requests_tree.selection()
        if selection:
            item = self.drug_requests_tree.item(selection[0])
            drug_name = item['values'][0]
            messagebox.showinfo("Mark Received", f"Marking {drug_name} as received...\n\nReceived Information:\n• Batch number verification\n• Expiry date confirmation\n• Storage location assignment\n• Quality control check\n• Inventory update")
        else:
            messagebox.showwarning("No Selection", "Please select a drug request to mark as received.")
    
    def view_drug_request_details(self):
        """View detailed drug request information"""
        selection = self.drug_requests_tree.selection()
        if selection:
            item = self.drug_requests_tree.item(selection[0])
            drug_name = item['values'][0]
            status = item['values'][4]
            
            # Find the full request details
            request = next((r for r in self.studies['drug_requests'] if r['drug_name'] == drug_name), None)
            
            if request:
                self.drug_details_text.config(state=tk.NORMAL)
                self.drug_details_text.delete(1.0, tk.END)
                
                details = f"""DRUG REQUEST DETAILS
====================

Request ID: {request['id']}
Drug Name: {request['drug_name']}
Quantity: {request['quantity']} units
Requested By: {request['requested_by']}
Request Date: {request['request_date']}
Status: {request['status']}

DELIVERY INFORMATION:
Received Date: {request['received_date'] or 'Not yet received'}
Batch Number: {request['batch_number'] or 'Not assigned'}
Expiry Date: {request['expiry_date'] or 'Not assigned'}

NEXT STEPS:
"""
                if request['status'] == 'Pending':
                    details += "• Awaiting sponsor approval\n• Monitor request status\n• Prepare storage location"
                elif request['status'] == 'Approved':
                    details += "• Drug shipment in progress\n• Monitor delivery status\n• Prepare for receipt"
                elif request['status'] == 'Shipped':
                    details += "• Drug shipment en route\n• Prepare for receipt\n• Verify batch information"
                elif request['status'] == 'Received':
                    details += "• Drug received and stored\n• Update inventory records\n• Begin dispensing process"
                
                self.drug_details_text.insert(tk.END, details)
                self.drug_details_text.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("No Selection", "Please select a drug request to view details.")
    
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
        self.root.update()
        
        # Simulate data refresh
        time.sleep(1)
        
        self.update_dashboard()
        self.status_label.config(text="Data refreshed successfully")
    
    def view_alert_details(self):
        """View alert details"""
        selection = self.alerts_tree.selection()
        if selection:
            item = self.alerts_tree.item(selection[0])
            alert_type = item['values'][0]
            description = item['values'][2]
            messagebox.showinfo("Alert Details", f"Type: {alert_type}\n\nDescription: {description}")
    
    def mark_alert_resolved(self):
        """Mark selected alert as resolved"""
        selection = self.alerts_tree.selection()
        if selection:
            messagebox.showinfo("Alert Resolved", "Alert has been marked as resolved.")
            self.refresh_data()
    
    def add_patient(self):
        """Add new patient"""
        messagebox.showinfo("Add Patient", "Add Patient dialog would open here.")
    
    def edit_patient(self):
        """Edit selected patient"""
        selection = self.patient_tree.selection()
        if selection:
            messagebox.showinfo("Edit Patient", "Edit Patient dialog would open here.")
    
    def schedule_visit(self):
        """Schedule visit for selected patient"""
        selection = self.patient_tree.selection()
        if selection:
            messagebox.showinfo("Schedule Visit", "Schedule Visit dialog would open here.")
    
    def schedule_new_visit(self):
        """Schedule new visit"""
        messagebox.showinfo("Visit Scheduled", "New visit has been scheduled successfully.")
    
    def upload_document(self):
        """Upload new document"""
        messagebox.showinfo("Upload Document", "Document upload dialog would open here.")
    
    def download_document(self):
        """Download selected document"""
        selection = self.doc_tree.selection()
        if selection:
            messagebox.showinfo("Download Document", "Document download would start here.")
    
    def view_document(self):
        """View selected document"""
        selection = self.doc_tree.selection()
        if selection:
            messagebox.showinfo("View Document", "Document viewer would open here.")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = ClinicalTrialDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
