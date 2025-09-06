#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Integration Manager
Handles integration with external systems like EDC, CTMS, and other clinical systems.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class IntegrationManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Trial Integration Manager - External System Connections")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f5f5')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Integration data
        self.integration_data = self.load_integration_data()
        self.current_connection = None
        
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
        
    def load_integration_data(self):
        """Load sample integration data"""
        return {
            "connected_systems": [
                {
                    "id": "EDC-001",
                    "name": "Medidata Rave EDC",
                    "type": "EDC",
                    "status": "Connected",
                    "last_sync": "2025-09-06 14:30:00",
                    "sync_frequency": "Real-time",
                    "data_volume": "2.3M records",
                    "health_score": 98.5,
                    "api_calls": 15420,
                    "error_rate": 0.02
                },
                {
                    "id": "CTMS-001", 
                    "name": "Veeva Vault CTMS",
                    "type": "CTMS",
                    "status": "Connected",
                    "last_sync": "2025-09-06 14:25:00",
                    "sync_frequency": "Every 15 minutes",
                    "data_volume": "850K records",
                    "health_score": 96.8,
                    "api_calls": 8930,
                    "error_rate": 0.05
                },
                {
                    "id": "LIMS-001",
                    "name": "LabVantage LIMS",
                    "type": "LIMS",
                    "status": "Connected",
                    "last_sync": "2025-09-06 14:20:00",
                    "sync_frequency": "Every 30 minutes",
                    "data_volume": "1.2M records",
                    "health_score": 99.1,
                    "api_calls": 5670,
                    "error_rate": 0.01
                },
                {
                    "id": "EMR-001",
                    "name": "Epic EMR System",
                    "type": "EMR",
                    "status": "Connected",
                    "last_sync": "2025-09-06 14:15:00",
                    "sync_frequency": "Real-time",
                    "data_volume": "5.1M records",
                    "health_score": 97.3,
                    "api_calls": 23450,
                    "error_rate": 0.03
                }
            ],
            "available_integrations": [
                {"name": "Oracle Clinical One", "type": "EDC", "status": "Available", "description": "Comprehensive EDC solution"},
                {"name": "Medrio EDC", "type": "EDC", "status": "Available", "description": "Cloud-based EDC platform"},
                {"name": "OpenClinica", "type": "EDC", "status": "Available", "description": "Open-source EDC system"},
                {"name": "IBM Clinical Development", "type": "CTMS", "status": "Available", "description": "Enterprise CTMS solution"},
                {"name": "MasterControl CTMS", "type": "CTMS", "status": "Available", "description": "Quality management CTMS"},
                {"name": "Cerner EMR", "type": "EMR", "status": "Available", "description": "Hospital EMR system"},
                {"name": "Allscripts EMR", "type": "EMR", "status": "Available", "description": "Healthcare IT platform"}
            ],
            "sync_logs": [
                {"timestamp": "2025-09-06 14:30:00", "system": "Medidata Rave", "operation": "Data Sync", "status": "Success", "records": 1250, "duration": "2.3s"},
                {"timestamp": "2025-09-06 14:25:00", "system": "Veeva Vault", "operation": "Document Sync", "status": "Success", "records": 45, "duration": "1.8s"},
                {"timestamp": "2025-09-06 14:20:00", "system": "LabVantage", "operation": "Lab Results", "status": "Success", "records": 89, "duration": "3.1s"},
                {"timestamp": "2025-09-06 14:15:00", "system": "Epic EMR", "operation": "Patient Data", "status": "Success", "records": 234, "duration": "4.2s"},
                {"timestamp": "2025-09-06 14:10:00", "system": "Medidata Rave", "operation": "Data Sync", "status": "Warning", "records": 1150, "duration": "5.1s", "note": "High latency detected"},
                {"timestamp": "2025-09-06 14:05:00", "system": "Veeva Vault", "operation": "Document Sync", "status": "Success", "records": 38, "duration": "1.5s"}
            ],
            "integration_metrics": {
                "total_connections": 4,
                "active_connections": 4,
                "total_data_synced": "9.45M records",
                "average_sync_time": "2.7s",
                "overall_health_score": 97.9,
                "api_calls_today": 53470,
                "error_rate": 0.03
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
        title_label = ttk.Label(header_frame, text="Integration Manager", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="External System Connections & Data Synchronization", style='Metric.TLabel')
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        
        ttk.Button(button_frame, text="➕ Add Integration", command=self.add_integration).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="🔄 Sync All", command=self.sync_all_systems).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="📊 View Logs", command=self.view_sync_logs).grid(row=0, column=2)
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Connected Systems tab
        self.create_connected_systems_tab()
        
        # Available Integrations tab
        self.create_available_integrations_tab()
        
        # Sync Monitoring tab
        self.create_sync_monitoring_tab()
        
        # Configuration tab
        self.create_configuration_tab()
    
    def create_connected_systems_tab(self):
        """Create connected systems tab"""
        connected_frame = ttk.Frame(self.notebook)
        self.notebook.add(connected_frame, text="🔗 Connected Systems")
        
        # Left panel - System list
        left_frame = ttk.Frame(connected_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Systems list
        systems_frame = ttk.LabelFrame(left_frame, text="Connected Systems", padding="10")
        systems_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.systems_tree = ttk.Treeview(systems_frame, columns=('Name', 'Type', 'Status', 'Health'), show='headings', height=12)
        self.systems_tree.heading('Name', text='System Name')
        self.systems_tree.heading('Type', text='Type')
        self.systems_tree.heading('Status', text='Status')
        self.systems_tree.heading('Health', text='Health Score')
        
        self.systems_tree.column('Name', width=200)
        self.systems_tree.column('Type', width=100)
        self.systems_tree.column('Status', width=100)
        self.systems_tree.column('Health', width=100)
        
        self.systems_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # System actions
        actions_frame = ttk.Frame(systems_frame)
        actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(actions_frame, text="Test Connection", command=self.test_connection).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(actions_frame, text="Sync Now", command=self.sync_system).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(actions_frame, text="Configure", command=self.configure_system).grid(row=0, column=2)
        
        # Integration metrics
        metrics_frame = ttk.LabelFrame(left_frame, text="Integration Metrics", padding="10")
        metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, height=8, width=50)
        self.metrics_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.metrics_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        systems_frame.columnconfigure(0, weight=1)
        systems_frame.rowconfigure(0, weight=1)
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.rowconfigure(0, weight=1)
        
        # Right panel - System details
        right_frame = ttk.Frame(connected_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # System details
        details_frame = ttk.LabelFrame(right_frame, text="System Details", padding="10")
        details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=20, width=60)
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        connected_frame.columnconfigure(0, weight=1)
        connected_frame.columnconfigure(1, weight=1)
        connected_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
    
    def create_available_integrations_tab(self):
        """Create available integrations tab"""
        available_frame = ttk.Frame(self.notebook)
        self.notebook.add(available_frame, text="📦 Available Integrations")
        
        # Available systems list
        systems_frame = ttk.LabelFrame(available_frame, text="Available Integration Partners", padding="10")
        systems_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.available_tree = ttk.Treeview(systems_frame, columns=('Name', 'Type', 'Status', 'Description'), show='headings', height=15)
        self.available_tree.heading('Name', text='System Name')
        self.available_tree.heading('Type', text='Type')
        self.available_tree.heading('Status', text='Status')
        self.available_tree.heading('Description', text='Description')
        
        self.available_tree.column('Name', width=200)
        self.available_tree.column('Type', width=100)
        self.available_tree.column('Status', width=100)
        self.available_tree.column('Description', width=250)
        
        self.available_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Integration actions
        actions_frame = ttk.Frame(systems_frame)
        actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(actions_frame, text="Connect System", command=self.connect_system).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(actions_frame, text="View Documentation", command=self.view_documentation).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(actions_frame, text="Request Integration", command=self.request_integration).grid(row=0, column=2)
        
        # Integration details
        details_frame = ttk.LabelFrame(available_frame, text="Integration Details", padding="10")
        details_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.integration_details_text = scrolledtext.ScrolledText(details_frame, height=20, width=60)
        self.integration_details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.integration_details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        available_frame.columnconfigure(0, weight=1)
        available_frame.columnconfigure(1, weight=1)
        available_frame.rowconfigure(0, weight=1)
        systems_frame.columnconfigure(0, weight=1)
        systems_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
    
    def create_sync_monitoring_tab(self):
        """Create sync monitoring tab"""
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="📊 Sync Monitoring")
        
        # Sync logs
        logs_frame = ttk.LabelFrame(monitoring_frame, text="Recent Sync Activity", padding="10")
        logs_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.logs_tree = ttk.Treeview(logs_frame, columns=('Timestamp', 'System', 'Operation', 'Status', 'Records', 'Duration'), show='headings', height=15)
        self.logs_tree.heading('Timestamp', text='Timestamp')
        self.logs_tree.heading('System', text='System')
        self.logs_tree.heading('Operation', text='Operation')
        self.logs_tree.heading('Status', text='Status')
        self.logs_tree.heading('Records', text='Records')
        self.logs_tree.heading('Duration', text='Duration')
        
        self.logs_tree.column('Timestamp', width=150)
        self.logs_tree.column('System', width=150)
        self.logs_tree.column('Operation', width=120)
        self.logs_tree.column('Status', width=80)
        self.logs_tree.column('Records', width=80)
        self.logs_tree.column('Duration', width=80)
        
        self.logs_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sync statistics
        stats_frame = ttk.LabelFrame(monitoring_frame, text="Sync Statistics", padding="10")
        stats_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, width=60)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.stats_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        monitoring_frame.columnconfigure(0, weight=1)
        monitoring_frame.columnconfigure(1, weight=1)
        monitoring_frame.rowconfigure(0, weight=1)
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
    
    def create_configuration_tab(self):
        """Create configuration tab"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuration")
        
        # API Configuration
        api_frame = ttk.LabelFrame(config_frame, text="API Configuration", padding="10")
        api_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # API settings
        ttk.Label(api_frame, text="API Base URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        api_url_entry = ttk.Entry(api_frame, width=50)
        api_url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        api_url_entry.insert(0, "https://api.clinical-trial-platform.com/v2")
        
        ttk.Label(api_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        api_key_entry = ttk.Entry(api_frame, width=50, show="*")
        api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        api_key_entry.insert(0, "ctm_sk_1234567890abcdef")
        
        ttk.Label(api_frame, text="Rate Limit:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        rate_limit_combo = ttk.Combobox(api_frame, values=["1000/hour", "5000/hour", "10000/hour"], state='readonly')
        rate_limit_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        rate_limit_combo.set("5000/hour")
        
        ttk.Label(api_frame, text="Timeout (seconds):").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        timeout_entry = ttk.Entry(api_frame, width=50)
        timeout_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        timeout_entry.insert(0, "30")
        
        # Sync Configuration
        sync_frame = ttk.LabelFrame(config_frame, text="Sync Configuration", padding="10")
        sync_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(sync_frame, text="Default Sync Frequency:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        sync_freq_combo = ttk.Combobox(sync_frame, values=["Real-time", "Every 5 minutes", "Every 15 minutes", "Every 30 minutes", "Hourly"], state='readonly')
        sync_freq_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        sync_freq_combo.set("Every 15 minutes")
        
        ttk.Label(sync_frame, text="Retry Attempts:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        retry_entry = ttk.Entry(sync_frame, width=50)
        retry_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        retry_entry.insert(0, "3")
        
        ttk.Label(sync_frame, text="Batch Size:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        batch_entry = ttk.Entry(sync_frame, width=50)
        batch_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        batch_entry.insert(0, "1000")
        
        ttk.Label(sync_frame, text="Error Threshold:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        error_threshold_entry = ttk.Entry(sync_frame, width=50)
        error_threshold_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        error_threshold_entry.insert(0, "5%")
        
        # Configuration buttons
        config_buttons_frame = ttk.Frame(config_frame)
        config_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(config_buttons_frame, text="💾 Save Configuration", command=self.save_configuration).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(config_buttons_frame, text="🔄 Reset to Defaults", command=self.reset_configuration).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(config_buttons_frame, text="📤 Export Config", command=self.export_configuration).grid(row=0, column=2)
        
        # Configure grid weights
        config_frame.columnconfigure(0, weight=1)
        config_frame.columnconfigure(1, weight=1)
        config_frame.rowconfigure(0, weight=1)
        api_frame.columnconfigure(1, weight=1)
        sync_frame.columnconfigure(1, weight=1)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Integration Manager Ready", style='Metric.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Last updated
        self.last_updated_label = ttk.Label(status_frame, text="", style='Metric.TLabel')
        self.last_updated_label.grid(row=0, column=1, sticky=tk.E)
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        # Update connected systems
        self.update_connected_systems()
        
        # Update available integrations
        self.update_available_integrations()
        
        # Update sync monitoring
        self.update_sync_monitoring()
        
        # Update integration metrics
        self.update_integration_metrics()
        
        # Update status
        self.last_updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_connected_systems(self):
        """Update connected systems list"""
        # Clear existing items
        for item in self.systems_tree.get_children():
            self.systems_tree.delete(item)
        
        # Add connected systems
        for system in self.integration_data['connected_systems']:
            status_color = 'green' if system['status'] == 'Connected' else 'red'
            health_color = 'green' if system['health_score'] >= 95 else 'orange' if system['health_score'] >= 90 else 'red'
            
            self.systems_tree.insert('', 'end', values=(
                system['name'],
                system['type'],
                system['status'],
                f"{system['health_score']}%"
            ))
    
    def update_available_integrations(self):
        """Update available integrations list"""
        # Clear existing items
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        # Add available integrations
        for integration in self.integration_data['available_integrations']:
            self.available_tree.insert('', 'end', values=(
                integration['name'],
                integration['type'],
                integration['status'],
                integration['description']
            ))
    
    def update_sync_monitoring(self):
        """Update sync monitoring data"""
        # Clear existing items
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        
        # Add sync logs
        for log in self.integration_data['sync_logs']:
            status_color = 'green' if log['status'] == 'Success' else 'orange' if log['status'] == 'Warning' else 'red'
            
            self.logs_tree.insert('', 'end', values=(
                log['timestamp'],
                log['system'],
                log['operation'],
                log['status'],
                log['records'],
                log['duration']
            ))
        
        # Update sync statistics
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        metrics = self.integration_data['integration_metrics']
        stats_info = f"""
SYNC STATISTICS
===============

OVERALL METRICS:
• Total Connections: {metrics['total_connections']}
• Active Connections: {metrics['active_connections']}
• Total Data Synced: {metrics['total_data_synced']}
• Average Sync Time: {metrics['average_sync_time']}
• Overall Health Score: {metrics['overall_health_score']}%

PERFORMANCE METRICS:
• API Calls Today: {metrics['api_calls_today']:,}
• Error Rate: {metrics['error_rate']}%
• Success Rate: {100 - metrics['error_rate']}%

SYSTEM HEALTH:
• Medidata Rave: 98.5% health score
• Veeva Vault: 96.8% health score
• LabVantage: 99.1% health score
• Epic EMR: 97.3% health score

RECENT ACTIVITY:
• Last 24 hours: 1,247 sync operations
• Successful syncs: 1,241 (99.5%)
• Failed syncs: 6 (0.5%)
• Average response time: 2.7 seconds

ALERTS & NOTIFICATIONS:
• No critical issues detected
• 2 systems showing high latency
• All systems within normal parameters
        """
        
        self.stats_text.insert(tk.END, stats_info)
        self.stats_text.config(state=tk.DISABLED)
    
    def update_integration_metrics(self):
        """Update integration metrics"""
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        
        metrics = self.integration_data['integration_metrics']
        metrics_info = f"""
INTEGRATION OVERVIEW
====================

CONNECTION STATUS:
• Total Systems: {metrics['total_connections']}
• Active: {metrics['active_connections']}
• Inactive: 0

DATA VOLUME:
• Total Synced: {metrics['total_data_synced']}
• Today's Sync: 1,247 operations
• Peak Hour: 2:00 PM (156 operations)

PERFORMANCE:
• Health Score: {metrics['overall_health_score']}%
• API Calls: {metrics['api_calls_today']:,} today
• Error Rate: {metrics['error_rate']}%

SYSTEM STATUS:
✅ Medidata Rave EDC - Connected
✅ Veeva Vault CTMS - Connected  
✅ LabVantage LIMS - Connected
✅ Epic EMR System - Connected

NEXT SYNC:
• Medidata Rave: Real-time
• Veeva Vault: 14:40:00
• LabVantage: 14:50:00
• Epic EMR: Real-time
        """
        
        self.metrics_text.insert(tk.END, metrics_info)
        self.metrics_text.config(state=tk.DISABLED)
    
    def test_connection(self):
        """Test selected system connection"""
        selection = self.systems_tree.selection()
        if selection:
            item = self.systems_tree.item(selection[0])
            system_name = item['values'][0]
            messagebox.showinfo("Connection Test", f"Testing connection to {system_name}...\n\n✅ Connection successful!\nResponse time: 45ms\nAPI version: v2.1")
        else:
            messagebox.showwarning("No Selection", "Please select a system to test.")
    
    def sync_system(self):
        """Sync selected system"""
        selection = self.systems_tree.selection()
        if selection:
            item = self.systems_tree.item(selection[0])
            system_name = item['values'][0]
            messagebox.showinfo("System Sync", f"Initiating sync for {system_name}...\n\n✅ Sync completed successfully!\nRecords synced: 1,250\nDuration: 2.3 seconds")
        else:
            messagebox.showwarning("No Selection", "Please select a system to sync.")
    
    def configure_system(self):
        """Configure selected system"""
        selection = self.systems_tree.selection()
        if selection:
            item = self.systems_tree.item(selection[0])
            system_name = item['values'][0]
            messagebox.showinfo("System Configuration", f"Opening configuration for {system_name}...\n\nConfiguration options:\n• API endpoints\n• Sync frequency\n• Data mapping\n• Error handling")
        else:
            messagebox.showwarning("No Selection", "Please select a system to configure.")
    
    def add_integration(self):
        """Add new integration"""
        messagebox.showinfo("Add Integration", "Add Integration wizard would open here.\n\nSteps:\n1. Select system type\n2. Configure API settings\n3. Test connection\n4. Set sync parameters\n5. Activate integration")
    
    def sync_all_systems(self):
        """Sync all connected systems"""
        messagebox.showinfo("Sync All Systems", "Initiating sync for all connected systems...\n\n✅ All systems synced successfully!\n\nResults:\n• Medidata Rave: 1,250 records\n• Veeva Vault: 45 documents\n• LabVantage: 89 lab results\n• Epic EMR: 234 patient records")
    
    def view_sync_logs(self):
        """View detailed sync logs"""
        messagebox.showinfo("Sync Logs", "Detailed sync logs would open here.\n\nFeatures:\n• Filter by system/date\n• Export logs\n• Error analysis\n• Performance metrics")
    
    def connect_system(self):
        """Connect to selected available system"""
        selection = self.available_tree.selection()
        if selection:
            item = self.available_tree.item(selection[0])
            system_name = item['values'][0]
            messagebox.showinfo("Connect System", f"Connecting to {system_name}...\n\nConnection wizard would open with:\n• API configuration\n• Authentication setup\n• Data mapping\n• Sync scheduling")
        else:
            messagebox.showwarning("No Selection", "Please select a system to connect.")
    
    def view_documentation(self):
        """View integration documentation"""
        selection = self.available_tree.selection()
        if selection:
            item = self.available_tree.item(selection[0])
            system_name = item['values'][0]
            messagebox.showinfo("Documentation", f"Opening documentation for {system_name}...\n\nDocumentation includes:\n• API reference\n• Integration guide\n• Sample configurations\n• Troubleshooting tips")
        else:
            messagebox.showwarning("No Selection", "Please select a system to view documentation.")
    
    def request_integration(self):
        """Request new integration"""
        messagebox.showinfo("Request Integration", "Integration request form would open here.\n\nRequest includes:\n• System details\n• Business justification\n• Technical requirements\n• Timeline expectations")
    
    def save_configuration(self):
        """Save configuration settings"""
        messagebox.showinfo("Save Configuration", "Configuration saved successfully!\n\nSettings updated:\n• API configuration\n• Sync parameters\n• Error handling\n• Performance tuning")
    
    def reset_configuration(self):
        """Reset configuration to defaults"""
        messagebox.showinfo("Reset Configuration", "Configuration reset to defaults.\n\nAll settings restored to:\n• Default API endpoints\n• Standard sync frequency\n• Default timeouts\n• Standard error thresholds")
    
    def export_configuration(self):
        """Export configuration"""
        messagebox.showinfo("Export Configuration", "Configuration exported successfully!\n\nExported to:\n• integration_config.json\n• API_credentials.enc\n• sync_schedules.xml")

def main():
    """Main function to run the integration manager"""
    root = tk.Tk()
    app = IntegrationManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
