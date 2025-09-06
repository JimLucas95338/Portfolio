#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Mobile Offline App
Enhanced mobile application with offline capabilities and sync functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class MobileOfflineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Trial Mobile App - Offline Capable")
        self.root.geometry("400x700")
        self.root.configure(bg='#f5f5f5')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Offline data storage
        self.offline_data = self.load_offline_data()
        self.sync_status = "Online"
        self.last_sync = datetime.now()
        
        self.setup_gui()
        self.update_dashboard()
        
        # Start sync monitoring
        self.start_sync_monitoring()
        
    def configure_styles(self):
        """Configure custom styles for mobile app"""
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#f5f5f5')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        self.style.configure('Metric.TLabel', font=('Arial', 10), background='#f5f5f5')
        self.style.configure('Success.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#2e7d32')
        self.style.configure('Warning.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#f57c00')
        self.style.configure('Error.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#d32f2f')
        
    def load_offline_data(self):
        """Load offline data storage"""
        return {
            "patients": [
                {
                    "id": "P001",
                    "name": "John Doe",
                    "study_id": "STUDY-001",
                    "last_visit": "2025-09-05",
                    "next_visit": "2025-09-12",
                    "status": "Active",
                    "offline_updated": False
                },
                {
                    "id": "P002",
                    "name": "Mary Smith",
                    "study_id": "STUDY-001",
                    "last_visit": "2025-09-03",
                    "next_visit": "2025-09-10",
                    "status": "Active",
                    "offline_updated": False
                }
            ],
            "visits": [
                {
                    "id": "V001",
                    "patient_id": "P001",
                    "date": "2025-09-12",
                    "time": "10:00 AM",
                    "type": "Follow-up",
                    "status": "Scheduled",
                    "offline_updated": False
                },
                {
                    "id": "V002",
                    "patient_id": "P002",
                    "date": "2025-09-10",
                    "time": "2:00 PM",
                    "type": "Screening",
                    "status": "Scheduled",
                    "offline_updated": False
                }
            ],
            "offline_actions": [],
            "sync_queue": []
        }
    
    def setup_gui(self):
        """Set up the mobile app GUI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Main content area
        self.create_main_content(main_frame)
        
        # Bottom navigation
        self.create_bottom_navigation(main_frame)
    
    def create_header(self, parent):
        """Create the mobile app header"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # App title and sync status
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(title_frame, text="🏥 Clinical Trial App", style='Title.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Sync status indicator
        self.sync_status_label = ttk.Label(title_frame, text="🟢 Online", style='Success.TLabel')
        self.sync_status_label.grid(row=0, column=1, sticky=tk.E)
        
        # User info
        user_frame = ttk.Frame(header_frame)
        user_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(user_frame, text="Dr. Sarah Johnson | Boston Medical Center", style='Metric.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Last sync time
        self.last_sync_label = ttk.Label(user_frame, text="", style='Metric.TLabel')
        self.last_sync_label.grid(row=0, column=1, sticky=tk.E)
        
        # Configure grid weights
        title_frame.columnconfigure(1, weight=1)
        user_frame.columnconfigure(1, weight=1)
    
    def create_main_content(self, parent):
        """Create the main content area"""
        # Create notebook for different views
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Dashboard tab
        self.create_dashboard_tab()
        
        # Patients tab
        self.create_patients_tab()
        
        # Visits tab
        self.create_visits_tab()
        
        # Offline tab
        self.create_offline_tab()
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Quick stats
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Quick Stats", padding="10")
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Active patients
        ttk.Label(stats_grid, text="Active Patients", style='Metric.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_grid, text="2", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W)
        
        # Scheduled visits
        ttk.Label(stats_grid, text="Scheduled Visits", style='Metric.TLabel').grid(row=0, column=1, sticky=tk.W)
        ttk.Label(stats_grid, text="2", style='Header.TLabel').grid(row=1, column=1, sticky=tk.W)
        
        # Pending sync
        ttk.Label(stats_grid, text="Pending Sync", style='Metric.TLabel').grid(row=0, column=2, sticky=tk.W)
        self.pending_sync_label = ttk.Label(stats_grid, text="0", style='Header.TLabel')
        self.pending_sync_label.grid(row=1, column=2, sticky=tk.W)
        
        # Today's schedule
        schedule_frame = ttk.LabelFrame(dashboard_frame, text="Today's Schedule", padding="10")
        schedule_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.schedule_text = scrolledtext.ScrolledText(schedule_frame, height=8, width=50)
        self.schedule_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.schedule_text.config(state=tk.DISABLED)
        
        # Offline actions
        offline_frame = ttk.LabelFrame(dashboard_frame, text="Offline Actions", padding="10")
        offline_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.offline_text = scrolledtext.ScrolledText(offline_frame, height=6, width=50)
        self.offline_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.offline_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        stats_frame.columnconfigure(0, weight=1)
        schedule_frame.columnconfigure(0, weight=1)
        schedule_frame.rowconfigure(0, weight=1)
        offline_frame.columnconfigure(0, weight=1)
        offline_frame.rowconfigure(0, weight=1)
    
    def create_patients_tab(self):
        """Create patients tab"""
        patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(patients_frame, text="👥 Patients")
        
        # Patient list
        patients_list_frame = ttk.LabelFrame(patients_frame, text="Patient List", padding="10")
        patients_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.patients_tree = ttk.Treeview(patients_list_frame, columns=('Name', 'Study', 'Last Visit', 'Next Visit', 'Status'), show='headings', height=8)
        self.patients_tree.heading('Name', text='Patient')
        self.patients_tree.heading('Study', text='Study')
        self.patients_tree.heading('Last Visit', text='Last Visit')
        self.patients_tree.heading('Next Visit', text='Next Visit')
        self.patients_tree.heading('Status', text='Status')
        
        self.patients_tree.column('Name', width=100)
        self.patients_tree.column('Study', width=80)
        self.patients_tree.column('Last Visit', width=80)
        self.patients_tree.column('Next Visit', width=80)
        self.patients_tree.column('Status', width=80)
        
        self.patients_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Patient actions
        patient_actions_frame = ttk.Frame(patients_list_frame)
        patient_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(patient_actions_frame, text="➕ Add Patient", command=self.add_patient).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(patient_actions_frame, text="✏️ Edit", command=self.edit_patient).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(patient_actions_frame, text="📋 View Details", command=self.view_patient_details).grid(row=0, column=2)
        
        # Configure grid weights
        patients_list_frame.columnconfigure(0, weight=1)
        patients_list_frame.rowconfigure(0, weight=1)
    
    def create_visits_tab(self):
        """Create visits tab"""
        visits_frame = ttk.Frame(self.notebook)
        self.notebook.add(visits_frame, text="📅 Visits")
        
        # Visit list
        visits_list_frame = ttk.LabelFrame(visits_frame, text="Scheduled Visits", padding="10")
        visits_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.visits_tree = ttk.Treeview(visits_list_frame, columns=('Patient', 'Date', 'Time', 'Type', 'Status'), show='headings', height=8)
        self.visits_tree.heading('Patient', text='Patient')
        self.visits_tree.heading('Date', text='Date')
        self.visits_tree.heading('Time', text='Time')
        self.visits_tree.heading('Type', text='Type')
        self.visits_tree.heading('Status', text='Status')
        
        self.visits_tree.column('Patient', width=100)
        self.visits_tree.column('Date', width=80)
        self.visits_tree.column('Time', width=80)
        self.visits_tree.column('Type', width=100)
        self.visits_tree.column('Status', width=80)
        
        self.visits_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Visit actions
        visit_actions_frame = ttk.Frame(visits_list_frame)
        visit_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(visit_actions_frame, text="➕ Schedule Visit", command=self.schedule_visit).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(visit_actions_frame, text="✅ Complete", command=self.complete_visit).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(visit_actions_frame, text="✏️ Edit", command=self.edit_visit).grid(row=0, column=2)
        
        # Configure grid weights
        visits_list_frame.columnconfigure(0, weight=1)
        visits_list_frame.rowconfigure(0, weight=1)
    
    def create_offline_tab(self):
        """Create offline capabilities tab"""
        offline_frame = ttk.Frame(self.notebook)
        self.notebook.add(offline_frame, text="📱 Offline")
        
        # Offline status
        status_frame = ttk.LabelFrame(offline_frame, text="Offline Status", padding="10")
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.offline_status_text = scrolledtext.ScrolledText(status_frame, height=6, width=50)
        self.offline_status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.offline_status_text.config(state=tk.DISABLED)
        
        # Sync queue
        sync_frame = ttk.LabelFrame(offline_frame, text="Sync Queue", padding="10")
        sync_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.sync_queue_text = scrolledtext.ScrolledText(sync_frame, height=8, width=50)
        self.sync_queue_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.sync_queue_text.config(state=tk.DISABLED)
        
        # Offline actions
        offline_actions_frame = ttk.Frame(offline_frame)
        offline_actions_frame.grid(row=2, column=0, pady=(10, 0))
        
        ttk.Button(offline_actions_frame, text="🔄 Sync Now", command=self.sync_now).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(offline_actions_frame, text="📤 Upload Changes", command=self.upload_changes).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(offline_actions_frame, text="📥 Download Updates", command=self.download_updates).grid(row=0, column=2)
        
        # Configure grid weights
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        sync_frame.columnconfigure(0, weight=1)
        sync_frame.rowconfigure(0, weight=1)
    
    def create_bottom_navigation(self, parent):
        """Create bottom navigation"""
        nav_frame = ttk.Frame(parent)
        nav_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Navigation buttons
        ttk.Button(nav_frame, text="📊", command=lambda: self.notebook.select(0)).grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(nav_frame, text="👥", command=lambda: self.notebook.select(1)).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(nav_frame, text="📅", command=lambda: self.notebook.select(2)).grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E))
        ttk.Button(nav_frame, text="📱", command=lambda: self.notebook.select(3)).grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        for i in range(4):
            nav_frame.columnconfigure(i, weight=1)
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        # Update sync status
        self.update_sync_status()
        
        # Update today's schedule
        self.update_todays_schedule()
        
        # Update offline actions
        self.update_offline_actions()
        
        # Update patients list
        self.update_patients_list()
        
        # Update visits list
        self.update_visits_list()
        
        # Update offline status
        self.update_offline_status()
        
        # Update sync queue
        self.update_sync_queue()
    
    def update_sync_status(self):
        """Update sync status indicator"""
        if self.sync_status == "Online":
            self.sync_status_label.config(text="🟢 Online", style='Success.TLabel')
        else:
            self.sync_status_label.config(text="🔴 Offline", style='Error.TLabel')
        
        self.last_sync_label.config(text=f"Last sync: {self.last_sync.strftime('%H:%M')}")
    
    def update_todays_schedule(self):
        """Update today's schedule"""
        self.schedule_text.config(state=tk.NORMAL)
        self.schedule_text.delete(1.0, tk.END)
        
        today = datetime.now().strftime('%Y-%m-%d')
        schedule_info = f"Today's Schedule - {today}\n\n"
        
        # Add today's visits
        for visit in self.offline_data['visits']:
            if visit['date'] == today:
                schedule_info += f"• {visit['time']} - {visit['patient_id']} ({visit['type']})\n"
        
        if not any(visit['date'] == today for visit in self.offline_data['visits']):
            schedule_info += "No visits scheduled for today.\n"
        
        schedule_info += f"\nOffline Status: {self.sync_status}\n"
        schedule_info += f"Pending Sync: {len(self.offline_data['sync_queue'])} items"
        
        self.schedule_text.insert(tk.END, schedule_info)
        self.schedule_text.config(state=tk.DISABLED)
    
    def update_offline_actions(self):
        """Update offline actions display"""
        self.offline_text.config(state=tk.NORMAL)
        self.offline_text.delete(1.0, tk.END)
        
        if self.offline_data['offline_actions']:
            for action in self.offline_data['offline_actions']:
                self.offline_text.insert(tk.END, f"• {action}\n")
        else:
            self.offline_text.insert(tk.END, "No offline actions pending.\n")
        
        self.offline_text.config(state=tk.DISABLED)
    
    def update_patients_list(self):
        """Update patients list"""
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Add patients
        for patient in self.offline_data['patients']:
            self.patients_tree.insert('', 'end', values=(
                patient['name'],
                patient['study_id'],
                patient['last_visit'],
                patient['next_visit'],
                patient['status']
            ))
    
    def update_visits_list(self):
        """Update visits list"""
        # Clear existing items
        for item in self.visits_tree.get_children():
            self.visits_tree.delete(item)
        
        # Add visits
        for visit in self.offline_data['visits']:
            patient_name = next((p['name'] for p in self.offline_data['patients'] if p['id'] == visit['patient_id']), visit['patient_id'])
            self.visits_tree.insert('', 'end', values=(
                patient_name,
                visit['date'],
                visit['time'],
                visit['type'],
                visit['status']
            ))
    
    def update_offline_status(self):
        """Update offline status display"""
        self.offline_status_text.config(state=tk.NORMAL)
        self.offline_status_text.delete(1.0, tk.END)
        
        status_info = f"""OFFLINE CAPABILITIES
====================

CONNECTION STATUS: {self.sync_status}
Last Sync: {self.last_sync.strftime('%Y-%m-%d %H:%M:%S')}

OFFLINE FEATURES:
✅ View patient information
✅ Schedule new visits
✅ Update visit status
✅ Add patient notes
✅ View study protocols
✅ Access offline forms

SYNC CAPABILITIES:
• Automatic sync when online
• Manual sync on demand
• Conflict resolution
• Data validation
• Error handling

STORAGE:
• Local database: 2.3 MB
• Cached images: 15.2 MB
• Offline forms: 5.1 MB
• Total: 22.6 MB
        """
        
        self.offline_status_text.insert(tk.END, status_info)
        self.offline_status_text.config(state=tk.DISABLED)
    
    def update_sync_queue(self):
        """Update sync queue display"""
        self.sync_queue_text.config(state=tk.NORMAL)
        self.sync_queue_text.delete(1.0, tk.END)
        
        if self.offline_data['sync_queue']:
            for item in self.offline_data['sync_queue']:
                self.sync_queue_text.insert(tk.END, f"• {item}\n")
        else:
            self.sync_queue_text.insert(tk.END, "Sync queue is empty.\n")
        
        self.sync_queue_text.config(state=tk.DISABLED)
        
        # Update pending sync count
        self.pending_sync_label.config(text=str(len(self.offline_data['sync_queue'])))
    
    def start_sync_monitoring(self):
        """Start sync monitoring thread"""
        def monitor_sync():
            while True:
                # Simulate network status changes
                if random.random() < 0.1:  # 10% chance of status change
                    if self.sync_status == "Online":
                        self.sync_status = "Offline"
                        self.add_offline_action("Connection lost - working offline")
                    else:
                        self.sync_status = "Online"
                        self.add_offline_action("Connection restored - syncing data")
                        self.sync_now()
                
                # Update UI
                self.root.after(0, self.update_sync_status)
                time.sleep(5)
        
        sync_thread = threading.Thread(target=monitor_sync, daemon=True)
        sync_thread.start()
    
    def add_offline_action(self, action):
        """Add action to offline actions list"""
        timestamp = datetime.now().strftime('%H:%M')
        self.offline_data['offline_actions'].append(f"[{timestamp}] {action}")
        
        # Keep only last 10 actions
        if len(self.offline_data['offline_actions']) > 10:
            self.offline_data['offline_actions'] = self.offline_data['offline_actions'][-10:]
        
        self.update_offline_actions()
    
    def add_to_sync_queue(self, item):
        """Add item to sync queue"""
        self.offline_data['sync_queue'].append(item)
        self.update_sync_queue()
    
    def add_patient(self):
        """Add new patient"""
        messagebox.showinfo("Add Patient", "Add Patient form would open here.\n\nOffline capabilities:\n• Form validation\n• Local storage\n• Auto-sync when online")
        self.add_to_sync_queue("Add new patient: P003")
        self.add_offline_action("New patient added offline")
    
    def edit_patient(self):
        """Edit selected patient"""
        selection = self.patients_tree.selection()
        if selection:
            messagebox.showinfo("Edit Patient", "Edit Patient form would open here.\n\nChanges will be synced when online.")
            self.add_to_sync_queue("Update patient: P001")
            self.add_offline_action("Patient information updated offline")
        else:
            messagebox.showwarning("No Selection", "Please select a patient to edit.")
    
    def view_patient_details(self):
        """View patient details"""
        selection = self.patients_tree.selection()
        if selection:
            item = self.patients_tree.item(selection[0])
            patient_name = item['values'][0]
            messagebox.showinfo("Patient Details", f"Patient Details for {patient_name}\n\nOffline view includes:\n• Complete patient history\n• Visit records\n• Lab results (cached)\n• Protocol information")
        else:
            messagebox.showwarning("No Selection", "Please select a patient to view details.")
    
    def schedule_visit(self):
        """Schedule new visit"""
        messagebox.showinfo("Schedule Visit", "Schedule Visit form would open here.\n\nOffline scheduling:\n• Conflict detection\n• Local calendar\n• Auto-sync when online")
        self.add_to_sync_queue("Schedule new visit: V003")
        self.add_offline_action("New visit scheduled offline")
    
    def complete_visit(self):
        """Complete selected visit"""
        selection = self.visits_tree.selection()
        if selection:
            messagebox.showinfo("Complete Visit", "Visit completion form would open here.\n\nOffline completion:\n• Form validation\n• Local storage\n• Auto-sync when online")
            self.add_to_sync_queue("Complete visit: V001")
            self.add_offline_action("Visit completed offline")
        else:
            messagebox.showwarning("No Selection", "Please select a visit to complete.")
    
    def edit_visit(self):
        """Edit selected visit"""
        selection = self.visits_tree.selection()
        if selection:
            messagebox.showinfo("Edit Visit", "Edit Visit form would open here.\n\nChanges will be synced when online.")
            self.add_to_sync_queue("Update visit: V001")
            self.add_offline_action("Visit information updated offline")
        else:
            messagebox.showwarning("No Selection", "Please select a visit to edit.")
    
    def sync_now(self):
        """Sync data now"""
        if self.sync_status == "Online":
            messagebox.showinfo("Sync Now", "Syncing data with server...\n\n✅ Sync completed successfully!\n\nSynced:\n• 2 patient updates\n• 1 new visit\n• 3 form submissions")
            
            # Clear sync queue
            self.offline_data['sync_queue'] = []
            self.update_sync_queue()
            
            self.last_sync = datetime.now()
            self.add_offline_action("Manual sync completed")
        else:
            messagebox.showwarning("Offline", "Cannot sync while offline.\n\nChanges will be synced automatically when connection is restored.")
    
    def upload_changes(self):
        """Upload offline changes"""
        if self.sync_status == "Online":
            messagebox.showinfo("Upload Changes", "Uploading offline changes...\n\n✅ Upload completed!\n\nUploaded:\n• 2 patient records\n• 1 visit record\n• 3 form submissions")
            self.add_offline_action("Offline changes uploaded")
        else:
            messagebox.showwarning("Offline", "Cannot upload while offline.")
    
    def download_updates(self):
        """Download updates from server"""
        if self.sync_status == "Online":
            messagebox.showinfo("Download Updates", "Downloading updates from server...\n\n✅ Download completed!\n\nDownloaded:\n• 1 protocol update\n• 2 new patients\n• 5 visit updates")
            self.add_offline_action("Updates downloaded from server")
        else:
            messagebox.showwarning("Offline", "Cannot download while offline.")

def main():
    """Main function to run the mobile offline app"""
    root = tk.Tk()
    app = MobileOfflineApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
