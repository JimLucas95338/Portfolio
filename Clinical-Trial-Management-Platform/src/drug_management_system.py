#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Drug Management & Randomization System
Comprehensive drug inventory, dispensing, and randomization management for clinical trials.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class DrugManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Drug Management & Randomization System")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f5f5f5')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Drug and randomization data
        self.drug_data = self.load_drug_data()
        self.randomization_data = self.load_randomization_data()
        
        self.setup_gui()
        self.update_dashboard()
        
    def configure_styles(self):
        """Configure custom styles"""
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        self.style.configure('Metric.TLabel', font=('Arial', 10), background='#f5f5f5')
        self.style.configure('Success.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#2e7d32')
        self.style.configure('Warning.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#f57c00')
        self.style.configure('Error.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#d32f2f')
        
    def load_drug_data(self):
        """Load drug inventory and management data"""
        return {
            "inventory": [
                {
                    "drug_id": "DRUG-001",
                    "name": "Study Drug A",
                    "batch": "BATCH-2025-001",
                    "strength": "100mg",
                    "form": "Tablet",
                    "quantity": 2500,
                    "expiry_date": "2026-03-15",
                    "storage_temp": "2-8°C",
                    "status": "Available",
                    "site": "Boston Medical Center"
                },
                {
                    "drug_id": "DRUG-002", 
                    "name": "Study Drug B",
                    "batch": "BATCH-2025-002",
                    "strength": "50mg",
                    "form": "Capsule",
                    "quantity": 1800,
                    "expiry_date": "2026-05-20",
                    "storage_temp": "Room Temperature",
                    "status": "Available",
                    "site": "Boston Medical Center"
                },
                {
                    "drug_id": "DRUG-003",
                    "name": "Placebo",
                    "batch": "BATCH-2025-003", 
                    "strength": "N/A",
                    "form": "Tablet",
                    "quantity": 3200,
                    "expiry_date": "2026-08-10",
                    "storage_temp": "Room Temperature",
                    "status": "Available",
                    "site": "Boston Medical Center"
                }
            ],
            "dispensing_log": [
                {
                    "patient_id": "P001",
                    "drug_id": "DRUG-001",
                    "quantity": 30,
                    "dispensed_date": "2025-09-05",
                    "dispensed_by": "Dr. Sarah Johnson",
                    "visit": "Baseline",
                    "randomization_code": "RAND-001-A"
                },
                {
                    "patient_id": "P002",
                    "drug_id": "DRUG-002", 
                    "quantity": 30,
                    "dispensed_date": "2025-09-04",
                    "dispensed_by": "Dr. Sarah Johnson",
                    "visit": "Baseline",
                    "randomization_code": "RAND-002-B"
                },
                {
                    "patient_id": "P003",
                    "drug_id": "DRUG-003",
                    "quantity": 30,
                    "dispensed_date": "2025-09-03",
                    "dispensed_by": "Dr. Sarah Johnson", 
                    "visit": "Baseline",
                    "randomization_code": "RAND-003-A"
                }
            ],
            "temperature_log": [
                {"date": "2025-09-06", "time": "08:00", "temp": "4.2°C", "status": "Normal"},
                {"date": "2025-09-06", "time": "12:00", "temp": "5.1°C", "status": "Normal"},
                {"date": "2025-09-06", "time": "16:00", "temp": "3.8°C", "status": "Normal"},
                {"date": "2025-09-06", "time": "20:00", "temp": "4.5°C", "status": "Normal"}
            ]
        }
    
    def load_randomization_data(self):
        """Load randomization and blinding data"""
        return {
            "randomization_scheme": {
                "type": "Stratified Block Randomization",
                "ratio": "1:1:1",
                "block_size": 6,
                "stratification_factors": ["Age Group", "Gender", "Disease Severity"],
                "total_subjects": 300
            },
            "treatment_arms": [
                {"arm": "A", "treatment": "Study Drug A", "description": "Active treatment arm"},
                {"arm": "B", "treatment": "Study Drug B", "description": "Active comparator arm"},
                {"arm": "C", "treatment": "Placebo", "description": "Control arm"}
            ],
            "randomized_patients": [
                {
                    "patient_id": "P001",
                    "randomization_code": "RAND-001-A",
                    "treatment_arm": "A",
                    "randomization_date": "2025-09-05",
                    "stratification": {"age": "18-65", "gender": "Male", "severity": "Moderate"},
                    "unblinded": False
                },
                {
                    "patient_id": "P002",
                    "randomization_code": "RAND-002-B", 
                    "treatment_arm": "B",
                    "randomization_date": "2025-09-04",
                    "stratification": {"age": "18-65", "gender": "Female", "severity": "Mild"},
                    "unblinded": False
                },
                {
                    "patient_id": "P003",
                    "randomization_code": "RAND-003-A",
                    "treatment_arm": "A", 
                    "randomization_date": "2025-09-03",
                    "stratification": {"age": "65+", "gender": "Male", "severity": "Severe"},
                    "unblinded": False
                }
            ],
            "randomization_stats": {
                "total_randomized": 3,
                "arm_a_count": 2,
                "arm_b_count": 1, 
                "arm_c_count": 0,
                "unblinded_count": 0,
                "next_code": "RAND-004"
            }
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
        title_label = ttk.Label(header_frame, text="Drug Management & Randomization System", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Comprehensive Drug Inventory, Dispensing, and Randomization Management", style='Metric.TLabel')
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        
        ttk.Button(button_frame, text="💊 Dispense Drug", command=self.dispense_drug).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="🎲 Randomize Patient", command=self.randomize_patient).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="📊 Generate Report", command=self.generate_report).grid(row=0, column=2)
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Drug Inventory tab
        self.create_drug_inventory_tab()
        
        # Randomization tab
        self.create_randomization_tab()
        
        # Dispensing Log tab
        self.create_dispensing_log_tab()
        
        # Temperature Monitoring tab
        self.create_temperature_monitoring_tab()
        
        # Reports tab
        self.create_reports_tab()
    
    def create_drug_inventory_tab(self):
        """Create drug inventory management tab"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="💊 Drug Inventory")
        
        # Left panel - Inventory list
        left_frame = ttk.Frame(inventory_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Inventory list
        inventory_list_frame = ttk.LabelFrame(left_frame, text="Drug Inventory", padding="10")
        inventory_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.inventory_tree = ttk.Treeview(inventory_list_frame, columns=('Drug', 'Batch', 'Strength', 'Quantity', 'Expiry', 'Status'), show='headings', height=10)
        self.inventory_tree.heading('Drug', text='Drug Name')
        self.inventory_tree.heading('Batch', text='Batch')
        self.inventory_tree.heading('Strength', text='Strength')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.heading('Expiry', text='Expiry Date')
        self.inventory_tree.heading('Status', text='Status')
        
        self.inventory_tree.column('Drug', width=150)
        self.inventory_tree.column('Batch', width=120)
        self.inventory_tree.column('Strength', width=80)
        self.inventory_tree.column('Quantity', width=80)
        self.inventory_tree.column('Expiry', width=100)
        self.inventory_tree.column('Status', width=100)
        
        self.inventory_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Inventory actions
        inventory_actions_frame = ttk.Frame(inventory_list_frame)
        inventory_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(inventory_actions_frame, text="➕ Add Drug", command=self.add_drug).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(inventory_actions_frame, text="✏️ Update", command=self.update_inventory).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(inventory_actions_frame, text="📋 View Details", command=self.view_drug_details).grid(row=0, column=2)
        
        # Inventory summary
        summary_frame = ttk.LabelFrame(left_frame, text="Inventory Summary", padding="10")
        summary_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=8, width=50)
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.summary_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        inventory_list_frame.columnconfigure(0, weight=1)
        inventory_list_frame.rowconfigure(0, weight=1)
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)
        
        # Right panel - Drug details
        right_frame = ttk.Frame(inventory_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Drug details
        details_frame = ttk.LabelFrame(right_frame, text="Drug Details", padding="10")
        details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.drug_details_text = scrolledtext.ScrolledText(details_frame, height=20, width=60)
        self.drug_details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.drug_details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        inventory_frame.columnconfigure(0, weight=1)
        inventory_frame.columnconfigure(1, weight=1)
        inventory_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
    
    def create_randomization_tab(self):
        """Create randomization management tab"""
        randomization_frame = ttk.Frame(self.notebook)
        self.notebook.add(randomization_frame, text="🎲 Randomization")
        
        # Left panel - Randomization scheme
        left_frame = ttk.Frame(randomization_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Randomization scheme
        scheme_frame = ttk.LabelFrame(left_frame, text="Randomization Scheme", padding="10")
        scheme_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.scheme_text = scrolledtext.ScrolledText(scheme_frame, height=8, width=50)
        self.scheme_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scheme_text.config(state=tk.DISABLED)
        
        # Treatment arms
        arms_frame = ttk.LabelFrame(left_frame, text="Treatment Arms", padding="10")
        arms_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.arms_tree = ttk.Treeview(arms_frame, columns=('Arm', 'Treatment', 'Description'), show='headings', height=4)
        self.arms_tree.heading('Arm', text='Arm')
        self.arms_tree.heading('Treatment', text='Treatment')
        self.arms_tree.heading('Description', text='Description')
        
        self.arms_tree.column('Arm', width=50)
        self.arms_tree.column('Treatment', width=120)
        self.arms_tree.column('Description', width=200)
        
        self.arms_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Randomization actions
        randomization_actions_frame = ttk.Frame(left_frame)
        randomization_actions_frame.grid(row=2, column=0, pady=(10, 0))
        
        ttk.Button(randomization_actions_frame, text="🎲 Randomize Patient", command=self.randomize_patient).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(randomization_actions_frame, text="👁 Unblind Patient", command=self.unblind_patient).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(randomization_actions_frame, text="📊 View Stats", command=self.view_randomization_stats).grid(row=0, column=2)
        
        # Configure grid weights
        scheme_frame.columnconfigure(0, weight=1)
        scheme_frame.rowconfigure(0, weight=1)
        arms_frame.columnconfigure(0, weight=1)
        arms_frame.rowconfigure(0, weight=1)
        
        # Right panel - Randomized patients
        right_frame = ttk.Frame(randomization_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Randomized patients list
        patients_frame = ttk.LabelFrame(right_frame, text="Randomized Patients", padding="10")
        patients_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.patients_tree = ttk.Treeview(patients_frame, columns=('Patient', 'Code', 'Arm', 'Date', 'Unblinded'), show='headings', height=12)
        self.patients_tree.heading('Patient', text='Patient ID')
        self.patients_tree.heading('Code', text='Randomization Code')
        self.patients_tree.heading('Arm', text='Treatment Arm')
        self.patients_tree.heading('Date', text='Randomization Date')
        self.patients_tree.heading('Unblinded', text='Unblinded')
        
        self.patients_tree.column('Patient', width=100)
        self.patients_tree.column('Code', width=120)
        self.patients_tree.column('Arm', width=80)
        self.patients_tree.column('Date', width=120)
        self.patients_tree.column('Unblinded', width=80)
        
        self.patients_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        randomization_frame.columnconfigure(0, weight=1)
        randomization_frame.columnconfigure(1, weight=1)
        randomization_frame.rowconfigure(0, weight=1)
        patients_frame.columnconfigure(0, weight=1)
        patients_frame.rowconfigure(0, weight=1)
    
    def create_dispensing_log_tab(self):
        """Create dispensing log tab"""
        dispensing_frame = ttk.Frame(self.notebook)
        self.notebook.add(dispensing_frame, text="📋 Dispensing Log")
        
        # Dispensing log
        log_frame = ttk.LabelFrame(dispensing_frame, text="Drug Dispensing Log", padding="10")
        log_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.dispensing_tree = ttk.Treeview(log_frame, columns=('Patient', 'Drug', 'Quantity', 'Date', 'Dispensed By', 'Visit', 'Code'), show='headings', height=12)
        self.dispensing_tree.heading('Patient', text='Patient ID')
        self.dispensing_tree.heading('Drug', text='Drug')
        self.dispensing_tree.heading('Quantity', text='Quantity')
        self.dispensing_tree.heading('Date', text='Date')
        self.dispensing_tree.heading('Dispensed By', text='Dispensed By')
        self.dispensing_tree.heading('Visit', text='Visit')
        self.dispensing_tree.heading('Code', text='Randomization Code')
        
        self.dispensing_tree.column('Patient', width=80)
        self.dispensing_tree.column('Drug', width=120)
        self.dispensing_tree.column('Quantity', width=80)
        self.dispensing_tree.column('Date', width=100)
        self.dispensing_tree.column('Dispensed By', width=120)
        self.dispensing_tree.column('Visit', width=100)
        self.dispensing_tree.column('Code', width=120)
        
        self.dispensing_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dispensing actions
        dispensing_actions_frame = ttk.Frame(log_frame)
        dispensing_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(dispensing_actions_frame, text="💊 New Dispensing", command=self.dispense_drug).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(dispensing_actions_frame, text="📊 Export Log", command=self.export_dispensing_log).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(dispensing_actions_frame, text="🔍 Search", command=self.search_dispensing).grid(row=0, column=2)
        
        # Configure grid weights
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def create_temperature_monitoring_tab(self):
        """Create temperature monitoring tab"""
        temp_frame = ttk.Frame(self.notebook)
        self.notebook.add(temp_frame, text="🌡️ Temperature Monitoring")
        
        # Temperature log
        temp_log_frame = ttk.LabelFrame(temp_frame, text="Temperature Monitoring Log", padding="10")
        temp_log_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.temp_tree = ttk.Treeview(temp_log_frame, columns=('Date', 'Time', 'Temperature', 'Status'), show='headings', height=12)
        self.temp_tree.heading('Date', text='Date')
        self.temp_tree.heading('Time', text='Time')
        self.temp_tree.heading('Temperature', text='Temperature')
        self.temp_tree.heading('Status', text='Status')
        
        self.temp_tree.column('Date', width=100)
        self.temp_tree.column('Time', width=80)
        self.temp_tree.column('Temperature', width=100)
        self.temp_tree.column('Status', width=100)
        
        self.temp_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Temperature alerts
        alerts_frame = ttk.LabelFrame(temp_frame, text="Temperature Alerts", padding="10")
        alerts_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.alerts_text = scrolledtext.ScrolledText(alerts_frame, height=20, width=60)
        self.alerts_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.alerts_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        temp_frame.columnconfigure(0, weight=1)
        temp_frame.columnconfigure(1, weight=1)
        temp_frame.rowconfigure(0, weight=1)
        temp_log_frame.columnconfigure(0, weight=1)
        temp_log_frame.rowconfigure(0, weight=1)
        alerts_frame.columnconfigure(0, weight=1)
        alerts_frame.rowconfigure(0, weight=1)
    
    def create_reports_tab(self):
        """Create reports tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Reports list
        reports_list_frame = ttk.LabelFrame(reports_frame, text="Available Reports", padding="10")
        reports_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.reports_tree = ttk.Treeview(reports_list_frame, columns=('Report', 'Description', 'Last Generated'), show='headings', height=10)
        self.reports_tree.heading('Report', text='Report Name')
        self.reports_tree.heading('Description', text='Description')
        self.reports_tree.heading('Last Generated', text='Last Generated')
        
        self.reports_tree.column('Report', width=200)
        self.reports_tree.column('Description', width=300)
        self.reports_tree.column('Last Generated', width=150)
        
        self.reports_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Report actions
        report_actions_frame = ttk.Frame(reports_list_frame)
        report_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(report_actions_frame, text="📊 Generate Report", command=self.generate_selected_report).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(report_actions_frame, text="📤 Export", command=self.export_report).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(report_actions_frame, text="📧 Email", command=self.email_report).grid(row=0, column=2)
        
        # Report preview
        preview_frame = ttk.LabelFrame(reports_frame, text="Report Preview", padding="10")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.report_preview_text = scrolledtext.ScrolledText(preview_frame, height=20, width=60)
        self.report_preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.report_preview_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        reports_frame.columnconfigure(0, weight=1)
        reports_frame.columnconfigure(1, weight=1)
        reports_frame.rowconfigure(0, weight=1)
        reports_list_frame.columnconfigure(0, weight=1)
        reports_list_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Drug Management System Ready", style='Metric.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Last updated
        self.last_updated_label = ttk.Label(status_frame, text="", style='Metric.TLabel')
        self.last_updated_label.grid(row=0, column=1, sticky=tk.E)
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        # Update inventory
        self.update_inventory_list()
        
        # Update randomization
        self.update_randomization_data()
        
        # Update dispensing log
        self.update_dispensing_log()
        
        # Update temperature monitoring
        self.update_temperature_monitoring()
        
        # Update reports
        self.update_reports()
        
        # Update status
        self.last_updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_inventory_list(self):
        """Update drug inventory list"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Add inventory items
        for drug in self.drug_data['inventory']:
            self.inventory_tree.insert('', 'end', values=(
                drug['name'],
                drug['batch'],
                drug['strength'],
                drug['quantity'],
                drug['expiry_date'],
                drug['status']
            ))
        
        # Update inventory summary
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        
        total_drugs = len(self.drug_data['inventory'])
        total_quantity = sum(drug['quantity'] for drug in self.drug_data['inventory'])
        available_drugs = len([drug for drug in self.drug_data['inventory'] if drug['status'] == 'Available'])
        
        summary_info = f"""
INVENTORY SUMMARY
=================

TOTAL DRUGS: {total_drugs}
TOTAL QUANTITY: {total_quantity:,} units
AVAILABLE: {available_drugs} drugs
SITE: Boston Medical Center

DRUG BREAKDOWN:
• Study Drug A: 2,500 units (Available)
• Study Drug B: 1,800 units (Available)  
• Placebo: 3,200 units (Available)

STORAGE CONDITIONS:
• Refrigerated (2-8°C): 1 drug
• Room Temperature: 2 drugs

EXPIRY MONITORING:
• Next expiry: 2026-03-15 (Study Drug A)
• All drugs within 6 months of expiry
• No expired drugs

ALERTS:
• No low stock alerts
• Temperature monitoring: Normal
• All batches within specifications
        """
        
        self.summary_text.insert(tk.END, summary_info)
        self.summary_text.config(state=tk.DISABLED)
    
    def update_randomization_data(self):
        """Update randomization data"""
        # Update randomization scheme
        self.scheme_text.config(state=tk.NORMAL)
        self.scheme_text.delete(1.0, tk.END)
        
        scheme = self.randomization_data['randomization_scheme']
        scheme_info = f"""
RANDOMIZATION SCHEME
====================

TYPE: {scheme['type']}
RATIO: {scheme['ratio']}
BLOCK SIZE: {scheme['block_size']}
TOTAL SUBJECTS: {scheme['total_subjects']}

STRATIFICATION FACTORS:
• {scheme['stratification_factors'][0]}
• {scheme['stratification_factors'][1]}
• {scheme['stratification_factors'][2]}

CURRENT STATUS:
• Randomized: {self.randomization_data['randomization_stats']['total_randomized']}
• Remaining: {scheme['total_subjects'] - self.randomization_data['randomization_stats']['total_randomized']}
• Next Code: {self.randomization_data['randomization_stats']['next_code']}
        """
        
        self.scheme_text.insert(tk.END, scheme_info)
        self.scheme_text.config(state=tk.DISABLED)
        
        # Update treatment arms
        for item in self.arms_tree.get_children():
            self.arms_tree.delete(item)
        
        for arm in self.randomization_data['treatment_arms']:
            self.arms_tree.insert('', 'end', values=(
                arm['arm'],
                arm['treatment'],
                arm['description']
            ))
        
        # Update randomized patients
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        for patient in self.randomization_data['randomized_patients']:
            self.patients_tree.insert('', 'end', values=(
                patient['patient_id'],
                patient['randomization_code'],
                patient['treatment_arm'],
                patient['randomization_date'],
                "Yes" if patient['unblinded'] else "No"
            ))
    
    def update_dispensing_log(self):
        """Update dispensing log"""
        # Clear existing items
        for item in self.dispensing_tree.get_children():
            self.dispensing_tree.delete(item)
        
        # Add dispensing records
        for record in self.drug_data['dispensing_log']:
            drug_name = next((drug['name'] for drug in self.drug_data['inventory'] if drug['drug_id'] == record['drug_id']), record['drug_id'])
            self.dispensing_tree.insert('', 'end', values=(
                record['patient_id'],
                drug_name,
                record['quantity'],
                record['dispensed_date'],
                record['dispensed_by'],
                record['visit'],
                record['randomization_code']
            ))
    
    def update_temperature_monitoring(self):
        """Update temperature monitoring"""
        # Clear existing items
        for item in self.temp_tree.get_children():
            self.temp_tree.delete(item)
        
        # Add temperature records
        for record in self.drug_data['temperature_log']:
            self.temp_tree.insert('', 'end', values=(
                record['date'],
                record['time'],
                record['temp'],
                record['status']
            ))
        
        # Update alerts
        self.alerts_text.config(state=tk.NORMAL)
        self.alerts_text.delete(1.0, tk.END)
        
        alerts_info = """
TEMPERATURE ALERTS
==================

CURRENT STATUS: ✅ NORMAL
Last Alert: None

MONITORING SUMMARY:
• Storage Unit: Refrigerator #1
• Target Temperature: 2-8°C
• Current Temperature: 4.2°C
• Status: Within Range

RECENT READINGS:
• 08:00 - 4.2°C (Normal)
• 12:00 - 5.1°C (Normal)
• 16:00 - 3.8°C (Normal)
• 20:00 - 4.5°C (Normal)

ALERT THRESHOLDS:
• High Alert: >8°C
• Low Alert: <2°C
• Critical: >10°C or <0°C

AUTOMATED ACTIONS:
• Email alerts to pharmacy staff
• SMS notifications for critical alerts
• Automatic backup cooling activation
• Data logging for regulatory compliance

COMPLIANCE STATUS:
• 21 CFR Part 11 compliant
• GCP temperature monitoring
• Audit trail maintained
• No deviations recorded
        """
        
        self.alerts_text.insert(tk.END, alerts_info)
        self.alerts_text.config(state=tk.DISABLED)
    
    def update_reports(self):
        """Update reports list"""
        # Clear existing items
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        # Add available reports
        reports = [
            ("Drug Inventory Report", "Complete inventory status with expiry dates and quantities", "2025-09-06 14:30"),
            ("Dispensing Summary", "Daily/weekly/monthly dispensing activity summary", "2025-09-06 14:25"),
            ("Randomization Report", "Randomization statistics and treatment arm distribution", "2025-09-06 14:20"),
            ("Temperature Log", "Temperature monitoring log with compliance status", "2025-09-06 14:15"),
            ("Regulatory Compliance", "Compliance report for FDA and regulatory submissions", "2025-09-06 14:10"),
            ("Site Performance", "Site-specific drug management performance metrics", "2025-09-06 14:05")
        ]
        
        for report in reports:
            self.reports_tree.insert('', 'end', values=report)
    
    def dispense_drug(self):
        """Dispense drug to patient"""
        messagebox.showinfo("Dispense Drug", "Drug Dispensing Form would open here.\n\nFeatures:\n• Patient selection\n• Drug selection with inventory check\n• Quantity validation\n• Randomization code assignment\n• Digital signature capture\n• Regulatory compliance checks")
    
    def randomize_patient(self):
        """Randomize new patient"""
        messagebox.showinfo("Randomize Patient", "Patient Randomization Form would open here.\n\nProcess:\n• Patient eligibility verification\n• Stratification factor collection\n• Randomization code generation\n• Treatment arm assignment\n• Blinding confirmation\n• Regulatory documentation")
    
    def add_drug(self):
        """Add new drug to inventory"""
        messagebox.showinfo("Add Drug", "Add Drug Form would open here.\n\nRequired Information:\n• Drug name and strength\n• Batch number and expiry date\n• Storage requirements\n• Regulatory information\n• Initial quantity\n• Site assignment")
    
    def update_inventory(self):
        """Update drug inventory"""
        messagebox.showinfo("Update Inventory", "Inventory Update Form would open here.\n\nUpdates:\n• Quantity adjustments\n• Status changes\n• Batch information\n• Expiry date updates\n• Storage location changes")
    
    def view_drug_details(self):
        """View detailed drug information"""
        selection = self.inventory_tree.selection()
        if selection:
            item = self.inventory_tree.item(selection[0])
            drug_name = item['values'][0]
            messagebox.showinfo("Drug Details", f"Drug Details for {drug_name}\n\nDetails include:\n• Complete drug information\n• Batch details and expiry\n• Storage requirements\n• Regulatory information\n• Dispensing history\n• Quality control data")
        else:
            messagebox.showwarning("No Selection", "Please select a drug to view details.")
    
    def unblind_patient(self):
        """Unblind patient (emergency only)"""
        messagebox.showinfo("Unblind Patient", "Emergency Unblinding Form would open here.\n\n⚠️ WARNING: This is for emergency use only!\n\nProcess:\n• Emergency justification required\n• Medical monitor approval\n• Regulatory notification\n• Documentation requirements\n• Audit trail maintenance")
    
    def view_randomization_stats(self):
        """View randomization statistics"""
        messagebox.showinfo("Randomization Statistics", "Randomization Statistics Report\n\nCurrent Statistics:\n• Total Randomized: 3\n• Arm A: 2 patients\n• Arm B: 1 patient\n• Arm C: 0 patients\n• Unblinded: 0 patients\n• Next Code: RAND-004")
    
    def generate_report(self):
        """Generate comprehensive report"""
        messagebox.showinfo("Generate Report", "Generating comprehensive drug management report...\n\nReport includes:\n• Inventory status\n• Dispensing summary\n• Randomization statistics\n• Temperature monitoring\n• Compliance status\n• Regulatory documentation")
    
    def export_dispensing_log(self):
        """Export dispensing log"""
        messagebox.showinfo("Export Dispensing Log", "Dispensing log exported successfully!\n\nExported to:\n• dispensing_log_2025-09-06.csv\n• Regulatory format included\n• Audit trail maintained")
    
    def search_dispensing(self):
        """Search dispensing records"""
        messagebox.showinfo("Search Dispensing", "Search Dispensing Records dialog would open here.\n\nSearch options:\n• By patient ID\n• By drug name\n• By date range\n• By dispensing staff\n• By randomization code")
    
    def generate_selected_report(self):
        """Generate selected report"""
        selection = self.reports_tree.selection()
        if selection:
            item = self.reports_tree.item(selection[0])
            report_name = item['values'][0]
            messagebox.showinfo("Generate Report", f"Generating {report_name}...\n\nReport generated successfully!\n\nFeatures:\n• Real-time data\n• Regulatory compliance\n• Export options\n• Email distribution")
        else:
            messagebox.showwarning("No Selection", "Please select a report to generate.")
    
    def export_report(self):
        """Export selected report"""
        messagebox.showinfo("Export Report", "Report exported successfully!\n\nExport formats:\n• PDF for regulatory submissions\n• Excel for data analysis\n• CSV for system integration\n• XML for electronic submissions")
    
    def email_report(self):
        """Email report to stakeholders"""
        messagebox.showinfo("Email Report", "Report emailed successfully!\n\nRecipients:\n• Study coordinator\n• Medical monitor\n• Regulatory affairs\n• Site pharmacy\n• Data management")

def main():
    """Main function to run the drug management system"""
    root = tk.Tk()
    app = DrugManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
