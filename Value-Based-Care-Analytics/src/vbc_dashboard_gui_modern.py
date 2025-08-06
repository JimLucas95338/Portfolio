"""
🏥 Modern Value-Based Care Analytics Dashboard GUI

Ultra-modern desktop application with contemporary design, gradients, 
animations, and sleek interface for healthcare executives.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
from datetime import datetime, timedelta
import sys
import os
from threading import Thread
import time

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.risk_engine import HealthcareRiskEngine
from src.quality_tracker import QualityMeasureTracker

class ModernVBCDashboard:
    """
    Ultra-modern GUI application for Value-Based Care Analytics Platform
    with contemporary design and smooth animations
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Value-Based Care Analytics - Modern Dashboard")
        self.root.geometry("1800x1100")
        self.root.configure(bg='#0f0f0f')  # Dark background
        
        # Modern color palette
        self.colors = {
            'bg_primary': '#0f0f0f',       # Dark charcoal
            'bg_secondary': '#1a1a1a',     # Darker gray
            'bg_card': '#2d2d30',          # Card background
            'accent_blue': '#007acc',      # Microsoft blue
            'accent_green': '#00d084',     # Success green
            'accent_orange': '#ff8c00',    # Warning orange
            'accent_red': '#ff4757',       # Error red
            'text_primary': '#ffffff',     # White text
            'text_secondary': '#b0b0b0',   # Gray text
            'text_muted': '#808080',       # Muted text
            'border': '#404040',           # Border color
            'hover': '#404040'             # Hover color
        }
        
        # Initialize engines
        self.risk_engine = HealthcareRiskEngine()
        self.quality_tracker = QualityMeasureTracker()
        
        # Data storage
        self.claims_data = None
        self.quality_data = None
        self.provider_data = None
        self.predictions_data = None
        
        # UI components
        self.charts = {}
        self.status_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        
        # Set up modern styling
        self.setup_modern_styles()
        
        # Create modern interface
        self.create_modern_sidebar()
        self.create_modern_header()
        self.create_modern_main_content()
        self.create_modern_status_bar()
        
        # Load sample data
        self.load_sample_data()
        
        # Set initial view
        self.show_dashboard_view()
    
    def setup_modern_styles(self):
        """Configure ultra-modern GUI styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button styles
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_blue'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        style.map('Modern.TButton',
                 background=[('active', '#0066cc'), ('pressed', '#005bb5')])
        
        # Success button
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_green'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        # Warning button
        style.configure('Warning.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_orange'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat')
        
        # Modern notebook
        style.configure('Modern.TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       padding=[20, 12],
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_secondary'],
                       borderwidth=0)
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['hover'])],
                 foreground=[('selected', self.colors['text_primary'])])
    
    def create_modern_sidebar(self):
        """Create modern sidebar navigation"""
        self.sidebar = tk.Frame(self.root, bg=self.colors['bg_secondary'], width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo area
        logo_frame = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'], height=100)
        logo_frame.pack(fill=tk.X, padx=20, pady=20)
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, 
                             text="🏥 VBC Analytics",
                             font=('Segoe UI', 16, 'bold'),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'])
        logo_label.pack(anchor='w')
        
        subtitle_label = tk.Label(logo_frame,
                                 text="Modern Dashboard",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_muted'])
        subtitle_label.pack(anchor='w')
        
        # Navigation buttons
        nav_frame = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'])
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard_view),
            ("🤖 AI Analytics", self.show_analytics_view),
            ("📈 Charts", self.show_charts_view),
            ("🚨 Alerts", self.show_alerts_view),
            ("📋 Reports", self.show_reports_view),
            ("⚙️ Settings", self.show_settings_view)
        ]
        
        self.nav_buttons = {}
        for text, command in nav_buttons:
            btn = self.create_nav_button(nav_frame, text, command)
            btn.pack(fill=tk.X, pady=5)
            self.nav_buttons[text] = btn
    
    def create_nav_button(self, parent, text, command):
        """Create modern navigation button"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        
        btn = tk.Button(btn_frame,
                       text=text,
                       font=('Segoe UI', 11, 'bold'),
                       bg=self.colors['bg_secondary'],
                       fg=self.colors['text_secondary'],
                       activebackground=self.colors['accent_blue'],
                       activeforeground=self.colors['text_primary'],
                       relief='flat',
                       bd=0,
                       padx=20,
                       pady=15,
                       anchor='w',
                       command=lambda: self.nav_click(text, command))
        btn.pack(fill=tk.X)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.colors['hover'], fg=self.colors['text_primary'])
        
        def on_leave(e):
            if not hasattr(btn, 'active') or not btn.active:
                btn.config(bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.active = False
        
        return btn_frame
    
    def nav_click(self, text, command):
        """Handle navigation button click"""
        # Reset all buttons
        for btn_text, btn_frame in self.nav_buttons.items():
            btn = btn_frame.winfo_children()[0]
            btn.active = False
            btn.config(bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'])
        
        # Activate clicked button
        btn = self.nav_buttons[text].winfo_children()[0]
        btn.active = True
        btn.config(bg=self.colors['accent_blue'], fg=self.colors['text_primary'])
        
        # Execute command
        command()
    
    def create_modern_header(self):
        """Create modern header with search and actions"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_card'], height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Search area
        search_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        search_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        
        tk.Label(search_frame, text="🔍", 
                font=('Segoe UI', 16), 
                bg=self.colors['bg_card'], 
                fg=self.colors['text_muted']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=('Segoe UI', 11),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               insertbackground=self.colors['text_primary'],
                               relief='flat',
                               bd=0,
                               width=30)
        search_entry.pack(side=tk.LEFT, ipady=8)
        
        # Action buttons
        actions_frame = tk.Frame(header_frame, bg=self.colors['bg_card'])
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        
        ttk.Button(actions_frame, text="🔄 Refresh", 
                  style='Modern.TButton',
                  command=self.refresh_all_data).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions_frame, text="📊 Export", 
                  style='Success.TButton',
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions_frame, text="💾 Save", 
                  style='Warning.TButton',
                  command=self.save_data).pack(side=tk.LEFT, padx=5)
    
    def create_modern_main_content(self):
        """Create modern main content area"""
        self.main_content = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # This will be populated by different views
        self.current_view = None
    
    def create_modern_status_bar(self):
        """Create modern status bar"""
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        # Status with icon
        status_left = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
        status_left.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=10)
        
        tk.Label(status_left, text="●", 
                font=('Segoe UI', 12), 
                bg=self.colors['bg_secondary'], 
                fg=self.colors['accent_green']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = tk.Label(status_left,
                                    textvariable=self.status_var,
                                    font=('Segoe UI', 10),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'])
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        progress_frame = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
        progress_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           variable=self.progress_var,
                                           length=200,
                                           style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Time
        self.time_label = tk.Label(progress_frame,
                                  text="",
                                  font=('Segoe UI', 10),
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_muted'])
        self.time_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.update_time()
        self.update_status("Ready - Modern VBC Analytics Dashboard", 100)
    
    def show_dashboard_view(self):
        """Show modern dashboard view"""
        self.clear_main_content()
        
        dashboard_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(dashboard_frame,
                         text="Executive Dashboard",
                         font=('Segoe UI', 24, 'bold'),
                         bg=self.colors['bg_primary'],
                         fg=self.colors['text_primary'])
        header.pack(anchor='w', pady=(0, 30))
        
        # KPI Cards Grid
        self.create_modern_kpi_grid(dashboard_frame)
        
        # Charts Row
        charts_frame = tk.Frame(dashboard_frame, bg=self.colors['bg_primary'])
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.create_dashboard_charts(charts_frame)
    
    def create_modern_kpi_grid(self, parent):
        """Create modern KPI cards grid"""
        kpi_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        kpi_frame.pack(fill=tk.X, pady=(0, 30))
        
        # KPI data
        kpis = [
            ("Total Patients", "patients_count", "👥", self.colors['accent_blue'], "32"),
            ("Quality Score", "quality_score", "⭐", self.colors['accent_green'], "89.4%"),
            ("High Risk", "high_risk_count", "🚨", self.colors['accent_red'], "8"),
            ("Cost PMPM", "cost_pmpm", "💰", self.colors['accent_orange'], "$687"),
            ("Shared Savings", "shared_savings", "💵", self.colors['accent_green'], "$498K"),
            ("Quality Bonus", "quality_bonus", "🏆", self.colors['accent_blue'], "$169K")
        ]
        
        self.kpi_cards = {}
        
        for i, (name, key, icon, color, default_value) in enumerate(kpis):
            # Card container
            card = tk.Frame(kpi_frame, bg=self.colors['bg_card'], relief='flat', bd=0)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew", ipadx=20, ipady=20)
            
            # Icon with colored background
            icon_frame = tk.Frame(card, bg=color, width=60, height=60)
            icon_frame.pack(pady=(0, 15))
            icon_frame.pack_propagate(False)
            
            icon_label = tk.Label(icon_frame, text=icon, 
                                 font=('Segoe UI', 20), 
                                 bg=color, 
                                 fg='white')
            icon_label.pack(expand=True)
            
            # Value
            value_label = tk.Label(card, text=default_value,
                                  font=('Segoe UI', 18, 'bold'),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['text_primary'])
            value_label.pack()
            
            # Name
            name_label = tk.Label(card, text=name,
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_card'],
                                 fg=self.colors['text_muted'])
            name_label.pack(pady=(5, 0))
            
            # Change indicator
            change_label = tk.Label(card, text="↗ +2.3%",
                                   font=('Segoe UI', 9),
                                   bg=self.colors['bg_card'],
                                   fg=self.colors['accent_green'])
            change_label.pack()
            
            self.kpi_cards[key] = value_label
        
        # Configure grid weights
        for i in range(len(kpis)):
            kpi_frame.columnconfigure(i, weight=1)
    
    def create_dashboard_charts(self, parent):
        """Create dashboard charts section"""
        # Left chart
        left_chart = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        left_chart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_chart, text="Risk Distribution",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        # Right chart
        right_chart = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        right_chart.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(right_chart, text="Quality Trends",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        # Store for later use
        self.left_chart_frame = left_chart
        self.right_chart_frame = right_chart
    
    def show_analytics_view(self):
        """Show analytics view"""
        self.clear_main_content()
        
        analytics_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        analytics_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with action buttons
        header_frame = tk.Frame(analytics_frame, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame,
                text="AI Analytics",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Action buttons
        actions = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        actions.pack(side=tk.RIGHT)
        
        ttk.Button(actions, text="🤖 Run Risk Analysis", 
                  style='Modern.TButton',
                  command=self.run_risk_analysis).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions, text="⭐ Quality Analysis", 
                  style='Success.TButton',
                  command=self.run_quality_analysis).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions, text="💰 Financial Analysis", 
                  style='Warning.TButton',
                  command=self.run_financial_analysis).pack(side=tk.LEFT, padx=5)
        
        # Results area with modern tabs
        self.create_analytics_results(analytics_frame)
    
    def create_analytics_results(self, parent):
        """Create modern analytics results area"""
        results_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern notebook
        self.analytics_notebook = ttk.Notebook(results_frame, style='Modern.TNotebook')
        self.analytics_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Risk Analysis Tab
        risk_tab = tk.Frame(self.analytics_notebook, bg=self.colors['bg_card'])
        self.analytics_notebook.add(risk_tab, text="🎯 Risk Analysis")
        
        self.risk_text = tk.Text(risk_tab,
                                font=('Consolas', 11),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_primary'],
                                insertbackground=self.colors['text_primary'],
                                selectbackground=self.colors['accent_blue'],
                                relief='flat',
                                bd=0)
        
        risk_scroll = ttk.Scrollbar(risk_tab, orient=tk.VERTICAL, command=self.risk_text.yview)
        self.risk_text.configure(yscrollcommand=risk_scroll.set)
        
        self.risk_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        risk_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
        
        # Quality Analysis Tab
        quality_tab = tk.Frame(self.analytics_notebook, bg=self.colors['bg_card'])
        self.analytics_notebook.add(quality_tab, text="⭐ Quality Measures")
        
        # Create modern treeview
        self.create_modern_quality_tree(quality_tab)
        
        # Financial Analysis Tab
        financial_tab = tk.Frame(self.analytics_notebook, bg=self.colors['bg_card'])
        self.analytics_notebook.add(financial_tab, text="💰 Financial Performance")
        
        self.financial_text = tk.Text(financial_tab,
                                     font=('Consolas', 11),
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     insertbackground=self.colors['text_primary'],
                                     selectbackground=self.colors['accent_blue'],
                                     relief='flat',
                                     bd=0)
        
        financial_scroll = ttk.Scrollbar(financial_tab, orient=tk.VERTICAL, command=self.financial_text.yview)
        self.financial_text.configure(yscrollcommand=financial_scroll.set)
        
        self.financial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        financial_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
    
    def create_modern_quality_tree(self, parent):
        """Create modern quality measures treeview"""
        tree_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Search bar
        search_frame = tk.Frame(tree_frame, bg=self.colors['bg_card'])
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Search Quality Measures:", 
                font=('Segoe UI', 11), 
                bg=self.colors['bg_card'], 
                fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        self.quality_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, 
                               textvariable=self.quality_search_var,
                               font=('Segoe UI', 10),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               insertbackground=self.colors['text_primary'],
                               relief='flat',
                               bd=0)
        search_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True, ipady=5)
        
        # Modern treeview
        columns = ("Measure", "Performance", "Benchmark", "Score", "Status", "Trend")
        self.quality_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        column_config = {
            "Measure": 250,
            "Performance": 100,
            "Benchmark": 100,
            "Score": 80,
            "Status": 150,
            "Trend": 80
        }
        
        for col in columns:
            self.quality_tree.heading(col, text=col)
            self.quality_tree.column(col, width=column_config.get(col, 100))
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.quality_tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.quality_tree.xview)
        self.quality_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack
        self.quality_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_charts_view(self):
        """Show charts view"""
        self.clear_main_content()
        
        charts_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(charts_frame,
                text="Interactive Charts",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 30))
        
        # Chart controls
        controls_frame = tk.Frame(charts_frame, bg=self.colors['bg_card'])
        controls_frame.pack(fill=tk.X, pady=(0, 20), ipady=20)
        
        tk.Label(controls_frame, text="Select Chart Type:",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=20)
        
        chart_types = ["Risk Distribution", "Quality Trends", "Cost Analysis", "Provider Performance"]
        self.chart_var = tk.StringVar(value=chart_types[0])
        
        chart_combo = ttk.Combobox(controls_frame, 
                                  textvariable=self.chart_var,
                                  values=chart_types, 
                                  state="readonly")
        chart_combo.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(controls_frame, text="📊 Generate Chart", 
                  style='Modern.TButton',
                  command=self.generate_chart).pack(side=tk.LEFT, padx=10)
        
        # Chart display area
        self.chart_display = tk.Frame(charts_frame, bg=self.colors['bg_card'])
        self.chart_display.pack(fill=tk.BOTH, expand=True)
    
    def show_alerts_view(self):
        """Show alerts view"""
        self.clear_main_content()
        
        alerts_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        alerts_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(alerts_frame,
                text="🚨 Alerts & Notifications",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 30))
        
        # Alert cards
        self.create_alert_cards(alerts_frame)
    
    def create_alert_cards(self, parent):
        """Create modern alert cards"""
        alerts_data = [
            ("High Risk Patients", "8 patients require immediate attention", "🚨", self.colors['accent_red']),
            ("Quality Alert", "3 measures below benchmark", "⚠️", self.colors['accent_orange']),
            ("Cost Alert", "PMPM trending above target", "💰", self.colors['accent_orange']),
            ("Success", "Quality bonuses earned this quarter", "✅", self.colors['accent_green'])
        ]
        
        for i, (title, message, icon, color) in enumerate(alerts_data):
            alert_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
            alert_card.pack(fill=tk.X, pady=10, ipady=20, ipadx=20)
            
            # Icon
            icon_label = tk.Label(alert_card, text=icon,
                                 font=('Segoe UI', 20),
                                 bg=self.colors['bg_card'],
                                 fg=color)
            icon_label.pack(side=tk.LEFT, padx=(0, 20))
            
            # Content
            content_frame = tk.Frame(alert_card, bg=self.colors['bg_card'])
            content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            title_label = tk.Label(content_frame, text=title,
                                  font=('Segoe UI', 14, 'bold'),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['text_primary'])
            title_label.pack(anchor='w')
            
            message_label = tk.Label(content_frame, text=message,
                                    font=('Segoe UI', 10),
                                    bg=self.colors['bg_card'],
                                    fg=self.colors['text_muted'])
            message_label.pack(anchor='w')
            
            # Action button
            action_btn = ttk.Button(alert_card, text="View Details",
                                   style='Modern.TButton')
            action_btn.pack(side=tk.RIGHT, padx=20)
    
    def show_reports_view(self):
        """Show reports view"""
        self.clear_main_content()
        
        reports_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        reports_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(reports_frame,
                text="📋 Reports & Analytics",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 30))
        
        # Report cards grid
        self.create_report_cards(reports_frame)
    
    def create_report_cards(self, parent):
        """Create modern report cards"""
        reports_grid = tk.Frame(parent, bg=self.colors['bg_primary'])
        reports_grid.pack(fill=tk.X, pady=(0, 30))
        
        reports = [
            ("Executive Summary", "📊", "Comprehensive overview for leadership"),
            ("Risk Analysis", "🎯", "AI-powered patient risk assessment"),
            ("Quality Dashboard", "⭐", "HEDIS/CMS quality measures tracking"),
            ("Financial Performance", "💰", "Value-based care ROI analysis"),
            ("Provider Scorecards", "👨‍⚕️", "Individual provider performance"),
            ("Trends Analysis", "📈", "Historical and predictive insights")
        ]
        
        for i, (title, icon, description) in enumerate(reports):
            row, col = i // 3, i % 3
            
            report_card = tk.Frame(reports_grid, bg=self.colors['bg_card'], relief='flat', bd=0)
            report_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", ipadx=20, ipady=20)
            
            # Icon
            icon_label = tk.Label(report_card, text=icon,
                                 font=('Segoe UI', 24),
                                 bg=self.colors['bg_card'],
                                 fg=self.colors['accent_blue'])
            icon_label.pack(pady=(0, 10))
            
            # Title
            title_label = tk.Label(report_card, text=title,
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['text_primary'])
            title_label.pack()
            
            # Description
            desc_label = tk.Label(report_card, text=description,
                                 font=('Segoe UI', 9),
                                 bg=self.colors['bg_card'],
                                 fg=self.colors['text_muted'],
                                 wraplength=150)
            desc_label.pack(pady=(5, 15))
            
            # Generate button
            ttk.Button(report_card, text="Generate",
                      style='Modern.TButton',
                      command=lambda t=title: self.generate_report(t)).pack()
        
        # Configure grid
        for i in range(3):
            reports_grid.columnconfigure(i, weight=1)
    
    def show_settings_view(self):
        """Show settings view"""
        self.clear_main_content()
        
        settings_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(settings_frame,
                text="⚙️ Settings",
                font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(anchor='w', pady=(0, 30))
        
        # Settings content
        settings_content = tk.Frame(settings_frame, bg=self.colors['bg_card'])
        settings_content.pack(fill=tk.BOTH, expand=True, ipady=30)
        
        tk.Label(settings_content,
                text="Settings and Configuration",
                font=('Segoe UI', 16),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=50)
        
        tk.Label(settings_content,
                text="⚙️ Configuration options would be available here",
                font=('Segoe UI', 12),
                bg=self.colors['bg_card'],
                fg=self.colors['text_muted']).pack()
    
    def clear_main_content(self):
        """Clear main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_status(self, message, progress=None):
        """Update status bar"""
        self.status_var.set(message)
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update_idletasks()
    
    # Data and functionality methods (simplified for demo)
    def load_sample_data(self):
        """Load sample data"""
        try:
            self.update_status("Loading healthcare data...", 50)
            
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(os.path.dirname(script_dir), 'data')
            
            # Load data files
            claims_file = os.path.join(data_dir, 'synthetic_claims_data.csv')
            quality_file = os.path.join(data_dir, 'quality_measures_data.csv')
            provider_file = os.path.join(data_dir, 'provider_performance_data.csv')
            
            if os.path.exists(claims_file):
                self.claims_data = pd.read_csv(claims_file)
                
            if os.path.exists(quality_file):
                self.quality_data = pd.read_csv(quality_file)
                
            if os.path.exists(provider_file):
                self.provider_data = pd.read_csv(provider_file)
            
            self.update_status("Data loaded successfully", 100)
            
        except Exception as e:
            self.update_status(f"Error loading data: {str(e)}", 0)
    
    def refresh_all_data(self):
        """Refresh all data"""
        self.update_status("Refreshing data...", 0)
        self.load_sample_data()
    
    def run_risk_analysis(self):
        """Run risk analysis"""
        if self.claims_data is None:
            messagebox.showwarning("Warning", "Please load claims data first.")
            return
        
        self.update_status("Running AI risk analysis...", 50)
        
        try:
            # Train model and generate predictions
            training_metrics = self.risk_engine.train_risk_model(self.claims_data)
            self.predictions_data = self.risk_engine.predict_risk_scores(self.claims_data)
            
            # Display results
            self.risk_text.delete(1.0, tk.END)
            
            result_text = f"""🤖 MODERN AI RISK STRATIFICATION ANALYSIS
{'='*60}

📊 MODEL PERFORMANCE:
• R² Score: {training_metrics['r2_score']:.3f} (Excellent: >0.8)
• Training Samples: {training_metrics['training_samples']}
• Test Samples: {training_metrics['test_samples']}

🎯 RISK DISTRIBUTION:
"""
            
            # Add risk distribution
            risk_dist = self.predictions_data['predicted_risk_category'].value_counts()
            for category, count in risk_dist.items():
                percentage = (count / len(self.predictions_data)) * 100
                result_text += f"• {category}: {count} patients ({percentage:.1f}%)\n"
            
            self.risk_text.insert(1.0, result_text)
            self.update_status("Risk analysis completed", 100)
            
        except Exception as e:
            self.update_status(f"Risk analysis failed: {str(e)}", 0)
    
    def run_quality_analysis(self):
        """Run quality analysis"""
        if self.quality_data is None:
            messagebox.showwarning("Warning", "Please load quality data first.")
            return
        
        self.update_status("Analyzing quality measures...", 50)
        
        try:
            # Clear previous results
            for item in self.quality_tree.get_children():
                self.quality_tree.delete(item)
            
            # Process each quality measure
            for _, measure in self.quality_data.iterrows():
                measure_name = measure['measure_name'][:30] + "..." if len(measure['measure_name']) > 30 else measure['measure_name']
                performance = f"{measure['performance_rate']:.1f}%"
                benchmark = f"{measure['benchmark_rate']:.1f}%"
                score = f"{measure['quality_score']:.1f}%"
                
                # Determine status and trend
                if measure['performance_rate'] > measure['benchmark_rate']:
                    status = "✅ Above Benchmark"
                    trend = "📈"
                else:
                    status = "⚠️ Below Benchmark"
                    trend = "📉"
                
                # Insert into tree
                self.quality_tree.insert("", tk.END, values=(
                    measure_name, performance, benchmark, score, status, trend
                ))
            
            self.update_status("Quality analysis completed", 100)
            
        except Exception as e:
            self.update_status(f"Quality analysis failed: {str(e)}", 0)
    
    def run_financial_analysis(self):
        """Run financial analysis"""
        if self.provider_data is None:
            messagebox.showwarning("Warning", "Please load provider data first.")
            return
        
        self.update_status("Analyzing financial performance...", 50)
        
        try:
            # Calculate financial metrics
            total_revenue = self.provider_data['revenue_total'].sum()
            total_shared_savings = self.provider_data['shared_savings'].sum()
            total_quality_bonus = self.provider_data['quality_bonus'].sum()
            
            # Display results
            self.financial_text.delete(1.0, tk.END)
            
            result_text = f"""💰 MODERN FINANCIAL PERFORMANCE ANALYSIS
{'='*60}

📊 OVERALL PERFORMANCE:
• Total Revenue: ${total_revenue:,.0f}
• Shared Savings Earned: ${total_shared_savings:,.0f}
• Quality Bonuses: ${total_quality_bonus:,.0f}
• Total Value-Based Revenue: ${total_shared_savings + total_quality_bonus:,.0f}
"""
            
            self.financial_text.insert(1.0, result_text)
            self.update_status("Financial analysis completed", 100)
            
        except Exception as e:
            self.update_status(f"Financial analysis failed: {str(e)}", 0)
    
    def generate_chart(self):
        """Generate interactive chart"""
        chart_type = self.chart_var.get()
        
        # Clear previous chart
        for widget in self.chart_display.winfo_children():
            widget.destroy()
        
        tk.Label(self.chart_display,
                text=f"📊 {chart_type} Chart",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=50)
        
        tk.Label(self.chart_display,
                text="Chart visualization would be displayed here",
                font=('Segoe UI', 12),
                bg=self.colors['bg_card'],
                fg=self.colors['text_muted']).pack()
    
    def generate_report(self, report_type):
        """Generate report"""
        self.update_status(f"Generating {report_type} report...", 50)
        messagebox.showinfo("Report", f"{report_type} report generated successfully!")
        self.update_status("Report generated", 100)
    
    def export_data(self):
        """Export data"""
        messagebox.showinfo("Export", "Data export functionality")
    
    def save_data(self):
        """Save data"""
        messagebox.showinfo("Save", "Data save functionality")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernVBCDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()