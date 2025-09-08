#!/usr/bin/env python3
"""
Clinical Trial Management Platform v2.0 - Demo Launcher
Launches the enhanced platform with all v2.0 features and improvements.
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

class V2DemoLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Trial Management Platform v2.0 - Demo Launcher")
        self.root.geometry("800x700")
        self.root.configure(bg='#f5f5f5')
        
        # Make window resizable
        self.root.resizable(True, True)
        
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the demo launcher GUI"""
        # Header
        header_frame = ttk.Frame(self.root, padding="20")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🏥 Clinical Trial Management Platform", font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        version_label = ttk.Label(header_frame, text="v2.0 - Advanced Analytics & AI-Powered Insights", font=('Arial', 12))
        version_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Features overview
        features_frame = ttk.LabelFrame(self.root, text="🚀 v2.0 New Features", padding="15")
        features_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        
        features_text = """
✅ Advanced Analytics Dashboard - Real-time insights with user feedback integration
✅ Integration Manager - Seamless connection with external systems (EDC, CTMS, LIMS, EMR)
✅ Mobile Offline App - Full functionality without internet connectivity
✅ AI Insights Engine - Predictive analytics and machine learning models
✅ Drug Management & Randomization - Complete drug inventory and randomization system
✅ Enhanced Reporting - Advanced export capabilities and performance metrics
✅ Real-time Monitoring - System performance and user analytics
        """
        
        features_label = ttk.Label(features_frame, text=features_text, justify=tk.LEFT)
        features_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Demo applications
        apps_frame = ttk.LabelFrame(self.root, text="📱 Demo Applications", padding="15")
        apps_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        
        # Configure grid weights for proper resizing
        self.root.rowconfigure(2, weight=1)
        apps_frame.columnconfigure(0, weight=1)
        
        # Main dashboard
        main_frame = ttk.Frame(apps_frame)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(main_frame, text="Main Site Coordinator Dashboard", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(main_frame, text="Core platform with patient management, visit scheduling, and compliance monitoring").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(main_frame, text="🚀 Launch", command=self.launch_main_dashboard).grid(row=0, column=1, rowspan=2, padx=(20, 0))
        
        # Analytics dashboard
        analytics_frame = ttk.Frame(apps_frame)
        analytics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(analytics_frame, text="Advanced Analytics Dashboard", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(analytics_frame, text="Real-time insights, user feedback integration, and performance metrics").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(analytics_frame, text="📊 Launch", command=self.launch_analytics).grid(row=0, column=1, rowspan=2, padx=(20, 0))
        
        # Integration manager
        integration_frame = ttk.Frame(apps_frame)
        integration_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(integration_frame, text="Integration Manager", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(integration_frame, text="Connect with external systems like EDC, CTMS, LIMS, and EMR").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(integration_frame, text="🔗 Launch", command=self.launch_integration).grid(row=0, column=1, rowspan=2, padx=(20, 0))
        
        # Mobile offline app
        mobile_frame = ttk.Frame(apps_frame)
        mobile_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(mobile_frame, text="Mobile Offline App", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(mobile_frame, text="Mobile-first design with offline capabilities and automatic sync").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(mobile_frame, text="📱 Launch", command=self.launch_mobile).grid(row=0, column=1, rowspan=2, padx=(20, 0))
        
        # AI insights engine
        ai_frame = ttk.Frame(apps_frame)
        ai_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(ai_frame, text="AI Insights Engine", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(ai_frame, text="Predictive analytics, machine learning models, and intelligent recommendations").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(ai_frame, text="🤖 Launch", command=self.launch_ai_engine).grid(row=0, column=1, rowspan=2, padx=(20, 0))
        
        # Drug management system
        drug_frame = ttk.Frame(apps_frame)
        drug_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(drug_frame, text="Drug Management & Randomization", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(drug_frame, text="Drug inventory, dispensing, randomization, and temperature monitoring").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(drug_frame, text="💊 Launch", command=self.launch_drug_management).grid(row=0, column=1, rowspan=2, padx=(20, 0))
        
        # Launch all button
        launch_all_frame = ttk.Frame(self.root)
        launch_all_frame.grid(row=3, column=0, pady=20, sticky=(tk.W, tk.E))
        
        ttk.Button(launch_all_frame, text="🚀 Launch All Applications", command=self.launch_all, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(launch_all_frame, text="📚 View Documentation", command=self.view_documentation).pack(side=tk.LEFT)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)  # Header - fixed size
        self.root.rowconfigure(1, weight=0)  # Features - fixed size
        self.root.rowconfigure(2, weight=1)  # Apps - expandable
        self.root.rowconfigure(3, weight=0)  # Buttons - fixed size
        
        header_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(0, weight=1)
        apps_frame.columnconfigure(0, weight=1)
        
        for frame in [main_frame, analytics_frame, integration_frame, mobile_frame, ai_frame, drug_frame]:
            frame.columnconfigure(0, weight=1)
    
    def launch_main_dashboard(self):
        """Launch the main site coordinator dashboard"""
        try:
            subprocess.Popen([sys.executable, "src/clinical_trial_gui.py"])
            messagebox.showinfo("Launching", "Main Site Coordinator Dashboard is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch main dashboard: {e}")
    
    def launch_analytics(self):
        """Launch the analytics dashboard"""
        try:
            subprocess.Popen([sys.executable, "src/analytics_dashboard.py"])
            messagebox.showinfo("Launching", "Advanced Analytics Dashboard is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch analytics dashboard: {e}")
    
    def launch_integration(self):
        """Launch the integration manager"""
        try:
            subprocess.Popen([sys.executable, "src/integration_manager.py"])
            messagebox.showinfo("Launching", "Integration Manager is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch integration manager: {e}")
    
    def launch_mobile(self):
        """Launch the mobile offline app"""
        try:
            subprocess.Popen([sys.executable, "src/mobile_offline_app.py"])
            messagebox.showinfo("Launching", "Mobile Offline App is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch mobile app: {e}")
    
    def launch_ai_engine(self):
        """Launch the AI insights engine"""
        try:
            subprocess.Popen([sys.executable, "src/ai_insights_engine.py"])
            messagebox.showinfo("Launching", "AI Insights Engine is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch AI engine: {e}")
    
    def launch_drug_management(self):
        """Launch the drug management system"""
        try:
            subprocess.Popen([sys.executable, "src/drug_management_system.py"])
            messagebox.showinfo("Launching", "Drug Management & Randomization System is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch drug management system: {e}")
    
    def launch_all(self):
        """Launch all applications"""
        try:
            # Launch all applications with a small delay
            subprocess.Popen([sys.executable, "src/clinical_trial_gui.py"])
            subprocess.Popen([sys.executable, "src/analytics_dashboard.py"])
            subprocess.Popen([sys.executable, "src/integration_manager.py"])
            subprocess.Popen([sys.executable, "src/mobile_offline_app.py"])
            subprocess.Popen([sys.executable, "src/ai_insights_engine.py"])
            subprocess.Popen([sys.executable, "src/drug_management_system.py"])
            
            messagebox.showinfo("Launching All", "All v2.0 applications are starting...\n\nThis may take a moment to load all modules.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch applications: {e}")
    
    def view_documentation(self):
        """View project documentation"""
        messagebox.showinfo("Documentation", "Project Documentation:\n\n• README.md - Complete project overview\n• docs/product-requirements.md - Detailed PRD\n• docs/executive-summary.md - Business case\n• mockups/ - Design mockups and wireframes\n\nAll documentation is available in the project directory.")

def main():
    """Main function to run the v2.0 demo launcher"""
    root = tk.Tk()
    app = V2DemoLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
