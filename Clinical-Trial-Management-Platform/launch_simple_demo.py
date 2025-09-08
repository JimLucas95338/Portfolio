#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Simple Demo Launcher
Shows only the essential tabs for new users (progressive disclosure simulation)
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

class SimpleDemoLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Trial Management Platform - Simple Demo")
        self.root.geometry("600x500")
        self.root.configure(bg='#f5f5f5')
        
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the simple demo launcher GUI"""
        # Header
        header_frame = ttk.Frame(self.root, padding="20")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🏥 Clinical Trial Management Platform", font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(header_frame, text="Simple Demo - Progressive Disclosure", font=('Arial', 12))
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Demo levels
        demo_frame = ttk.LabelFrame(self.root, text="🎯 Demo Levels", padding="15")
        demo_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        
        # Level 1 - New User
        level1_frame = ttk.Frame(demo_frame)
        level1_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(level1_frame, text="👶 New Site Coordinator (Day 1)", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(level1_frame, text="• Dashboard with today's priorities\n• Patient list for their studies\n• Today's scheduled visits", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(level1_frame, text="🚀 Launch Basic Dashboard", command=self.launch_basic_dashboard).grid(row=2, column=0, pady=(10, 0))
        
        # Level 2 - After 1 Week
        level2_frame = ttk.Frame(demo_frame)
        level2_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(level2_frame, text="📚 After 1 Week Training", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(level2_frame, text="• + Compliance tracking\n• + Document management", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(level2_frame, text="🚀 Launch Intermediate Dashboard", command=self.launch_intermediate_dashboard).grid(row=2, column=0, pady=(10, 0))
        
        # Level 3 - Experienced User
        level3_frame = ttk.Frame(demo_frame)
        level3_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(level3_frame, text="💼 Experienced Coordinator", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(level3_frame, text="• + Drug management\n• + Advanced features", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(level3_frame, text="🚀 Launch Full Dashboard", command=self.launch_full_dashboard).grid(row=2, column=0, pady=(10, 0))
        
        # Level 4 - Full Platform
        level4_frame = ttk.Frame(demo_frame)
        level4_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(level4_frame, text="🏆 Full Platform v2.0", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(level4_frame, text="• AI-powered insights\n• Advanced analytics\n• Integration manager", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        ttk.Button(level4_frame, text="🚀 Launch Full Platform", command=self.launch_full_platform).grid(row=2, column=0, pady=(10, 0))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(self.root, text="📋 Demo Instructions", padding="15")
        instructions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        
        instructions_text = """
🎯 Demo Flow:
1. Start with "New Site Coordinator" - shows only 3 essential tabs
2. Progress to "After 1 Week" - adds compliance and documents
3. Show "Experienced Coordinator" - includes drug management
4. End with "Full Platform" - demonstrates all v2.0 features

💡 Key Message: "We manage complexity through progressive disclosure"
        """
        
        ttk.Label(instructions_frame, text=instructions_text, font=('Arial', 10), justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        demo_frame.columnconfigure(0, weight=1)
        instructions_frame.columnconfigure(0, weight=1)
    
    def launch_basic_dashboard(self):
        """Launch basic dashboard (3 tabs only)"""
        messagebox.showinfo("Basic Dashboard", "Launching basic dashboard with only:\n• Dashboard\n• Patients\n• Scheduling\n\nPerfect for new users!")
        subprocess.Popen([sys.executable, "src/clinical_trial_gui_simple.py"])
    
    def launch_intermediate_dashboard(self):
        """Launch intermediate dashboard (5 tabs)"""
        messagebox.showinfo("Intermediate Dashboard", "Launching intermediate dashboard with:\n• Dashboard\n• Patients\n• Scheduling\n• Compliance\n• Documents\n\nAfter 1 week of training!")
        # Create a modified version for intermediate users
        subprocess.Popen([sys.executable, "src/clinical_trial_gui_simple.py", "intermediate"])
    
    def launch_full_dashboard(self):
        """Launch full dashboard (all 6 tabs)"""
        messagebox.showinfo("Full Dashboard", "Launching full dashboard with all 6 tabs:\n• Dashboard\n• Patients\n• Scheduling\n• Compliance\n• Documents\n• Drug Management\n\nFor experienced users!")
        # Create a modified version for experienced users
        subprocess.Popen([sys.executable, "src/clinical_trial_gui_simple.py", "experienced"])
    
    def launch_full_platform(self):
        """Launch full v2.0 platform"""
        messagebox.showinfo("Full Platform", "Launching the complete v2.0 platform with:\n• All dashboard features\n• AI-powered insights\n• Advanced analytics\n• Integration manager\n• Mobile offline app")
        subprocess.Popen([sys.executable, "launch_v2_demo.py"])

def main():
    root = tk.Tk()
    app = SimpleDemoLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
