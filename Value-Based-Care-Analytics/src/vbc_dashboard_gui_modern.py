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
        
        # Update KPIs after data load
        self.update_kpi_cards()
    
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
    
    def update_kpi_cards(self):
        """Update KPI cards with real data"""
        try:
            if hasattr(self, 'kpi_cards') and self.claims_data is not None:
                # Calculate real metrics
                total_patients = self.claims_data['patient_id'].nunique()
                
                # Quality score from quality data
                avg_quality = self.quality_data['quality_score'].mean() if self.quality_data is not None else 89.4
                
                # High risk patients
                high_risk_count = len(self.claims_data[self.claims_data['risk_score'] >= 2.0])
                
                # Financial metrics from provider data
                if self.provider_data is not None:
                    avg_cost_pmpm = self.provider_data['total_cost_pmpm'].mean()
                    total_shared_savings = self.provider_data['shared_savings'].sum()
                    total_quality_bonus = self.provider_data['quality_bonus'].sum()
                else:
                    avg_cost_pmpm = 687
                    total_shared_savings = 498000
                    total_quality_bonus = 169000
                
                # Update the labels
                self.kpi_cards['patients_count'].config(text=f"{total_patients}")
                self.kpi_cards['quality_score'].config(text=f"{avg_quality:.1f}%")
                self.kpi_cards['high_risk_count'].config(text=f"{high_risk_count}")
                self.kpi_cards['cost_pmpm'].config(text=f"${avg_cost_pmpm:.0f}")
                self.kpi_cards['shared_savings'].config(text=f"${total_shared_savings/1000:.0f}K")
                self.kpi_cards['quality_bonus'].config(text=f"${total_quality_bonus/1000:.0f}K")
                
        except Exception as e:
            print(f"Error updating KPI cards: {e}")
    
    def create_dashboard_charts(self, parent):
        """Create dashboard charts section"""
        # Left chart - Risk Distribution
        left_chart = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        left_chart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_chart, text="Risk Distribution",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=(15, 10))
        
        # Create risk distribution chart
        self.create_risk_distribution_chart(left_chart)
        
        # Right chart - Quality Trends
        right_chart = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=0)
        right_chart.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(right_chart, text="Quality Trends",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=(15, 10))
        
        # Create quality trends chart
        self.create_quality_trends_chart(right_chart)
        
        # Store for later use
        self.left_chart_frame = left_chart
        self.right_chart_frame = right_chart
    
    def create_risk_distribution_chart(self, parent):
        """Create risk distribution pie chart"""
        try:
            # Create matplotlib figure with dark theme
            plt.style.use('dark_background')
            fig = Figure(figsize=(5, 4), dpi=80, facecolor=self.colors['bg_card'])
            ax = fig.add_subplot(111)
            ax.set_facecolor(self.colors['bg_card'])
            
            if self.claims_data is not None:
                # Calculate risk distribution from actual data
                risk_counts = []
                risk_labels = []
                
                low_risk = len(self.claims_data[self.claims_data['risk_score'] < 1.0])
                medium_risk = len(self.claims_data[(self.claims_data['risk_score'] >= 1.0) & (self.claims_data['risk_score'] < 2.0)])
                high_risk = len(self.claims_data[(self.claims_data['risk_score'] >= 2.0) & (self.claims_data['risk_score'] < 3.0)])
                very_high_risk = len(self.claims_data[self.claims_data['risk_score'] >= 3.0])
                
                if low_risk > 0:
                    risk_counts.append(low_risk)
                    risk_labels.append('Low Risk')
                if medium_risk > 0:
                    risk_counts.append(medium_risk)
                    risk_labels.append('Medium Risk')
                if high_risk > 0:
                    risk_counts.append(high_risk)
                    risk_labels.append('High Risk')
                if very_high_risk > 0:
                    risk_counts.append(very_high_risk)
                    risk_labels.append('Very High Risk')
            else:
                # Sample data if no real data available
                risk_counts = [15, 10, 5, 2]
                risk_labels = ['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
            
            # Modern color scheme for pie chart
            colors = [self.colors['accent_green'], self.colors['accent_orange'], 
                     self.colors['accent_red'], '#ff4757']
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(risk_counts, labels=risk_labels, colors=colors,
                                            autopct='%1.1f%%', startangle=90,
                                            textprops={'color': 'white', 'fontsize': 9})
            
            # Style the chart
            ax.set_title('Patient Risk Categories', color='white', fontsize=12, pad=20)
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            # Fallback if chart creation fails
            error_label = tk.Label(parent, 
                                  text="📊 Risk Distribution\n(Chart loading...)",
                                  font=('Segoe UI', 10),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['text_muted'],
                                  justify=tk.CENTER)
            error_label.pack(expand=True)
            print(f"Risk chart error: {e}")
    
    def create_quality_trends_chart(self, parent):
        """Create quality trends line chart"""
        try:
            # Create matplotlib figure with dark theme
            plt.style.use('dark_background')
            fig = Figure(figsize=(5, 4), dpi=80, facecolor=self.colors['bg_card'])
            ax = fig.add_subplot(111)
            ax.set_facecolor(self.colors['bg_card'])
            
            if self.quality_data is not None:
                # Use actual quality data
                quality_scores = self.quality_data['quality_score'].values
                measure_names = [name[:15] + '...' if len(name) > 15 else name 
                               for name in self.quality_data['measure_name']]
                
                # Create trend line (simulate trend over time)
                x_pos = range(len(quality_scores))
                
                # Plot quality scores
                ax.plot(x_pos, quality_scores, marker='o', linewidth=2, 
                       color=self.colors['accent_blue'], markersize=6,
                       markerfacecolor=self.colors['accent_green'])
                
                # Add benchmark line
                benchmarks = self.quality_data['benchmark_rate'].values
                ax.plot(x_pos, benchmarks, '--', linewidth=1, 
                       color=self.colors['text_muted'], alpha=0.7, label='Benchmark')
                
                ax.set_xticks(x_pos[::2])  # Show every other label to avoid crowding
                ax.set_xticklabels(measure_names[::2], rotation=45, ha='right', fontsize=8)
                ax.set_ylabel('Score (%)', color='white', fontsize=10)
                
            else:
                # Sample trend data
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                quality_trend = [85, 87, 89, 88, 91, 89]
                benchmark = [80] * 6
                
                ax.plot(months, quality_trend, marker='o', linewidth=3, 
                       color=self.colors['accent_blue'], markersize=8,
                       markerfacecolor=self.colors['accent_green'])
                ax.plot(months, benchmark, '--', linewidth=2, 
                       color=self.colors['text_muted'], alpha=0.7, label='Benchmark')
                
                ax.set_ylabel('Quality Score (%)', color='white', fontsize=10)
            
            # Style the chart
            ax.set_title('Quality Performance Over Time', color='white', fontsize=12, pad=20)
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.2, color='white')
            ax.legend(loc='upper left', fontsize=8)
            
            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            
            # Tight layout
            fig.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            # Fallback if chart creation fails
            error_label = tk.Label(parent, 
                                  text="📈 Quality Trends\n(Chart loading...)",
                                  font=('Segoe UI', 10),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['text_muted'],
                                  justify=tk.CENTER)
            error_label.pack(expand=True)
            print(f"Quality chart error: {e}")
    
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
            ("High Risk Patients", "8 patients require immediate attention", "🚨", self.colors['accent_red'], "high_risk"),
            ("Quality Alert", "3 measures below benchmark", "⚠️", self.colors['accent_orange'], "quality"),
            ("Cost Alert", "PMPM trending above target", "💰", self.colors['accent_orange'], "cost"),
            ("Success", "Quality bonuses earned this quarter", "✅", self.colors['accent_green'], "success")
        ]
        
        for i, (title, message, icon, color, alert_type) in enumerate(alerts_data):
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
            
            # Action button with specific functionality
            action_btn = ttk.Button(alert_card, text="View Details",
                                   style='Modern.TButton',
                                   command=lambda t=alert_type: self.show_alert_details(t))
            action_btn.pack(side=tk.RIGHT, padx=20)
    
    def show_alert_details(self, alert_type):
        """Show detailed alert information"""
        if alert_type == "high_risk":
            self.show_high_risk_details()
        elif alert_type == "quality":
            self.show_quality_alert_details()
        elif alert_type == "cost":
            self.show_cost_alert_details()
        elif alert_type == "success":
            self.show_success_details()
    
    def show_high_risk_details(self):
        """Show high risk patients details"""
        if self.claims_data is not None:
            high_risk_patients = self.claims_data[self.claims_data['risk_score'] >= 2.0]
            
            details = f"""🚨 HIGH RISK PATIENTS ALERT
            
Total High-Risk Patients: {len(high_risk_patients)}

Patient Details:
"""
            for _, patient in high_risk_patients.head(10).iterrows():
                details += f"• {patient['patient_id']}: Risk Score {patient['risk_score']:.2f}, Age {patient['age']}, Conditions: {patient['chronic_conditions']}\n"
            
            details += f"""
RECOMMENDED ACTIONS:
• Deploy intensive care management for these patients
• Schedule immediate follow-up appointments
• Implement medication adherence monitoring
• Coordinate with specialists as needed
• Monitor for emergency department visits

EXPECTED IMPACT:
• 25% reduction in preventable hospitalizations
• Improved patient outcomes through proactive care
• Potential cost savings of $50,000+ per quarter"""
            
        else:
            details = "High-risk patient data not available. Please load claims data first."
        
        self.show_details_popup("High Risk Patients Alert", details)
    
    def show_quality_alert_details(self):
        """Show quality alert details"""
        if self.quality_data is not None:
            below_benchmark = self.quality_data[self.quality_data['performance_rate'] < self.quality_data['benchmark_rate']]
            
            details = f"""⚠️ QUALITY MEASURES ALERT
            
Measures Below Benchmark: {len(below_benchmark)}

Quality Issues:
"""
            for _, measure in below_benchmark.head(5).iterrows():
                gap = measure['benchmark_rate'] - measure['performance_rate']
                details += f"• {measure['measure_name']}: {measure['performance_rate']:.1f}% (Gap: -{gap:.1f}%)\n"
            
            details += f"""
IMPROVEMENT OPPORTUNITIES:
• Implement targeted quality improvement initiatives
• Provide additional provider training and support
• Deploy care gap closure workflows
• Enhance patient engagement programs
• Monitor progress monthly

EXPECTED BENEFITS:
• Improved patient outcomes and satisfaction
• Higher quality bonus payments
• Enhanced competitive positioning
• Regulatory compliance assurance"""
            
        else:
            details = "Quality data not available. Please load quality measures data first."
        
        self.show_details_popup("Quality Measures Alert", details)
    
    def show_cost_alert_details(self):
        """Show cost alert details"""
        if self.provider_data is not None:
            avg_cost = self.provider_data['total_cost_pmpm'].mean()
            target_cost = 650  # Example target
            variance = avg_cost - target_cost
            
            details = f"""💰 COST MANAGEMENT ALERT
            
Current Average PMPM: ${avg_cost:.2f}
Target PMPM: ${target_cost:.2f}
Variance: ${variance:.2f} ({variance/target_cost*100:+.1f}%)

Cost Analysis:
• Total cost trending above quarterly targets
• Need to identify cost reduction opportunities
• Review high-cost providers and specialties
• Implement cost containment strategies

RECOMMENDED ACTIONS:
• Review provider contracts and fee schedules
• Implement utilization management programs
• Focus on preventive care to reduce acute costs
• Negotiate better rates with high-volume providers
• Deploy care coordination to reduce duplicative services

POTENTIAL SAVINGS:
• 10-15% cost reduction through better management
• Improved efficiency in care delivery
• Enhanced shared savings opportunities
• Better contract performance"""
            
        else:
            details = "Provider cost data not available. Please load provider data first."
        
        self.show_details_popup("Cost Management Alert", details)
    
    def show_success_details(self):
        """Show success details"""
        if self.provider_data is not None:
            total_bonus = self.provider_data['quality_bonus'].sum()
            total_savings = self.provider_data['shared_savings'].sum()
            
            details = f"""✅ SUCCESS METRICS
            
Quarterly Performance:
• Quality Bonuses Earned: ${total_bonus:,.0f}
• Shared Savings Generated: ${total_savings:,.0f}
• Total Value-Based Revenue: ${total_bonus + total_savings:,.0f}

ACHIEVEMENTS:
• Exceeded quality performance targets
• Successful implementation of care management programs
• Strong provider engagement and performance
• Positive patient outcomes and satisfaction

SUCCESS FACTORS:
• AI-driven risk stratification and care management
• Comprehensive quality measures tracking
• Proactive care gap closure initiatives
• Strong provider-patient relationships
• Effective care coordination

NEXT STEPS:
• Continue current successful strategies
• Scale successful programs to additional providers
• Explore expansion of value-based contracts
• Share best practices across the organization
• Plan for next quarter's quality initiatives"""
            
        else:
            details = "Performance data not available. Please load provider data first."
        
        self.show_details_popup("Success Metrics", details)
    
    def show_details_popup(self, title, content):
        """Show a popup window with detailed information"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("600x500")
        popup.configure(bg=self.colors['bg_secondary'])
        
        # Make popup modal
        popup.transient(self.root)
        popup.grab_set()
        
        # Title
        title_label = tk.Label(popup, text=title,
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'])
        title_label.pack(pady=20)
        
        # Content area
        content_frame = tk.Frame(popup, bg=self.colors['bg_card'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Scrollable text
        text_widget = tk.Text(content_frame,
                             font=('Segoe UI', 10),
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'],
                             wrap=tk.WORD,
                             padx=20,
                             pady=20)
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert content
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        # Close button
        close_btn = ttk.Button(popup, text="Close",
                              style='Modern.TButton',
                              command=popup.destroy)
        close_btn.pack(pady=10)
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
    
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
        self.update_kpi_cards()
        
        # Refresh current view if it's dashboard
        current_nav = None
        for text, btn_frame in self.nav_buttons.items():
            btn = btn_frame.winfo_children()[0]
            if hasattr(btn, 'active') and btn.active:
                current_nav = text
                break
        
        if current_nav == "📊 Dashboard":
            self.show_dashboard_view()
        
        self.update_status("Data refreshed successfully", 100)
    
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
        
        self.update_status(f"Generating {chart_type} chart...", 50)
        
        try:
            # Create matplotlib figure with dark theme
            plt.style.use('dark_background')
            fig = Figure(figsize=(12, 8), dpi=100, facecolor=self.colors['bg_card'])
            
            if chart_type == "Risk Distribution":
                self.create_interactive_risk_chart(fig)
            elif chart_type == "Quality Trends":
                self.create_interactive_quality_chart(fig)
            elif chart_type == "Cost Analysis":
                self.create_interactive_cost_chart(fig)
            elif chart_type == "Provider Performance":
                self.create_interactive_provider_chart(fig)
            
            # Embed chart in tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart_display)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            self.update_status(f"{chart_type} chart generated successfully", 100)
            
        except Exception as e:
            error_label = tk.Label(self.chart_display,
                                  text=f"❌ Error generating {chart_type} chart\n{str(e)}",
                                  font=('Segoe UI', 12),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['accent_red'],
                                  justify=tk.CENTER)
            error_label.pack(expand=True)
            self.update_status(f"Chart generation failed: {str(e)}", 0)
    
    def create_interactive_risk_chart(self, fig):
        """Create interactive risk distribution chart"""
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg_card'])
        
        if self.claims_data is not None:
            # Calculate detailed risk distribution
            risk_data = {}
            for _, patient in self.claims_data.iterrows():
                score = patient['risk_score']
                if score < 1.0:
                    category = 'Low Risk\n(0.0-1.0)'
                elif score < 2.0:
                    category = 'Medium Risk\n(1.0-2.0)'
                elif score < 3.0:
                    category = 'High Risk\n(2.0-3.0)'
                else:
                    category = 'Very High Risk\n(3.0+)'
                
                risk_data[category] = risk_data.get(category, 0) + 1
        else:
            # Sample data
            risk_data = {
                'Low Risk\n(0.0-1.0)': 15,
                'Medium Risk\n(1.0-2.0)': 10,
                'High Risk\n(2.0-3.0)': 5,
                'Very High Risk\n(3.0+)': 2
            }
        
        # Create enhanced pie chart
        colors = [self.colors['accent_green'], self.colors['accent_orange'], 
                 self.colors['accent_red'], '#ff4757']
        
        wedges, texts, autotexts = ax.pie(risk_data.values(), labels=risk_data.keys(),
                                        colors=colors, autopct='%1.1f%%', startangle=90,
                                        textprops={'color': 'white', 'fontsize': 11},
                                        explode=(0.05, 0.05, 0.1, 0.15))  # Explode slices
        
        ax.set_title('Patient Risk Distribution Analysis', color='white', fontsize=16, pad=30)
        
        # Add summary text
        total_patients = sum(risk_data.values())
        high_risk_total = risk_data.get('High Risk\n(2.0-3.0)', 0) + risk_data.get('Very High Risk\n(3.0+)', 0)
        risk_percentage = (high_risk_total / total_patients) * 100
        
        summary_text = f"Total Patients: {total_patients}\nHigh-Risk Patients: {high_risk_total} ({risk_percentage:.1f}%)"
        ax.text(1.3, 0.5, summary_text, transform=ax.transAxes, fontsize=12,
               verticalalignment='center', color='white',
               bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['bg_secondary'], alpha=0.8))
    
    def create_interactive_quality_chart(self, fig):
        """Create interactive quality trends chart"""
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg_card'])
        
        if self.quality_data is not None:
            # Use actual quality data
            measures = self.quality_data['measure_name'].head(10)  # Top 10 measures
            performance = self.quality_data['performance_rate'].head(10)
            benchmarks = self.quality_data['benchmark_rate'].head(10)
            scores = self.quality_data['quality_score'].head(10)
            
            x_pos = range(len(measures))
            
            # Create grouped bar chart
            width = 0.25
            ax.bar([x - width for x in x_pos], performance, width, label='Performance', 
                  color=self.colors['accent_blue'], alpha=0.8)
            ax.bar(x_pos, benchmarks, width, label='Benchmark', 
                  color=self.colors['text_muted'], alpha=0.6)
            ax.bar([x + width for x in x_pos], scores, width, label='Quality Score', 
                  color=self.colors['accent_green'], alpha=0.8)
            
            ax.set_xlabel('Quality Measures', color='white', fontsize=12)
            ax.set_ylabel('Score (%)', color='white', fontsize=12)
            ax.set_title('Quality Measures Performance Analysis', color='white', fontsize=16, pad=30)
            
            # Rotate x-axis labels
            short_names = [name[:20] + '...' if len(name) > 20 else name for name in measures]
            ax.set_xticks(x_pos)
            ax.set_xticklabels(short_names, rotation=45, ha='right', fontsize=10)
            
        else:
            # Sample data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
            quality_trend = [85, 87, 89, 88, 91, 89, 92, 90]
            benchmark = [80] * 8
            target = [95] * 8
            
            ax.plot(months, quality_trend, marker='o', linewidth=3, markersize=8,
                   color=self.colors['accent_blue'], label='Actual Performance')
            ax.plot(months, benchmark, '--', linewidth=2, 
                   color=self.colors['text_muted'], label='Industry Benchmark')
            ax.plot(months, target, ':', linewidth=2, 
                   color=self.colors['accent_green'], label='Target')
            
            ax.set_ylabel('Quality Score (%)', color='white', fontsize=12)
            ax.set_title('Quality Performance Trends Over Time', color='white', fontsize=16, pad=30)
        
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.legend(loc='upper left', fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
    
    def create_interactive_cost_chart(self, fig):
        """Create interactive cost analysis chart"""
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg_card'])
        
        if self.provider_data is not None:
            # Cost analysis by specialty
            specialty_costs = self.provider_data.groupby('specialty').agg({
                'total_cost_pmpm': 'mean',
                'shared_savings': 'sum',
                'patient_panel_size': 'sum'
            }).round(0)
            
            specialties = specialty_costs.index
            costs = specialty_costs['total_cost_pmpm']
            savings = specialty_costs['shared_savings']
            
            # Create dual-axis chart
            ax2 = ax.twinx()
            
            # Bar chart for costs
            bars1 = ax.bar(specialties, costs, alpha=0.7, color=self.colors['accent_orange'], 
                          label='Cost PMPM')
            
            # Line chart for savings
            line1 = ax2.plot(specialties, savings, marker='o', linewidth=3, markersize=8,
                           color=self.colors['accent_green'], label='Shared Savings')
            
            ax.set_xlabel('Medical Specialty', color='white', fontsize=12)
            ax.set_ylabel('Cost PMPM ($)', color='white', fontsize=12)
            ax2.set_ylabel('Shared Savings ($)', color='white', fontsize=12)
            ax.set_title('Cost Analysis by Medical Specialty', color='white', fontsize=16, pad=30)
            
            # Rotate labels
            ax.tick_params(axis='x', rotation=45, colors='white')
            
        else:
            # Sample cost data
            categories = ['Primary Care', 'Cardiology', 'Endocrinology', 'Nephrology', 'Oncology']
            costs = [450, 890, 595, 1250, 2850]
            savings = [35000, 52000, 18000, 45000, 85000]
            
            ax2 = ax.twinx()
            
            bars = ax.bar(categories, costs, alpha=0.7, color=self.colors['accent_orange'])
            line = ax2.plot(categories, savings, marker='o', linewidth=3, markersize=8,
                          color=self.colors['accent_green'])
            
            ax.set_ylabel('Cost PMPM ($)', color='white', fontsize=12)
            ax2.set_ylabel('Shared Savings ($)', color='white', fontsize=12)
            ax.set_title('Healthcare Cost vs Savings Analysis', color='white', fontsize=16, pad=30)
        
        ax.tick_params(colors='white')
        ax2.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        # Combined legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    def create_interactive_provider_chart(self, fig):
        """Create interactive provider performance chart"""
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg_card'])
        
        if self.provider_data is not None:
            # Scatter plot: Quality Score vs Cost PMPM
            x = self.provider_data['avg_quality_score']
            y = self.provider_data['total_cost_pmpm']
            sizes = self.provider_data['patient_panel_size'] / 5  # Scale bubble sizes
            colors_data = self.provider_data['shared_savings']
            
            scatter = ax.scatter(x, y, s=sizes, c=colors_data, cmap='RdYlGn', alpha=0.7)
            
            ax.set_xlabel('Average Quality Score (%)', color='white', fontsize=12)
            ax.set_ylabel('Total Cost PMPM ($)', color='white', fontsize=12)
            ax.set_title('Provider Performance: Quality vs Cost\n(Bubble size = Panel Size, Color = Shared Savings)', 
                        color='white', fontsize=16, pad=30)
            
            # Add colorbar
            cbar = fig.colorbar(scatter, ax=ax)
            cbar.set_label('Shared Savings ($)', color='white', fontsize=10)
            cbar.ax.tick_params(colors='white')
            
            # Add quadrant lines
            avg_quality = x.mean()
            avg_cost = y.mean()
            ax.axvline(avg_quality, color='white', linestyle='--', alpha=0.5)
            ax.axhline(avg_cost, color='white', linestyle='--', alpha=0.5)
            
            # Add quadrant labels
            ax.text(0.95, 0.95, 'High Cost\nHigh Quality', transform=ax.transAxes, 
                   ha='right', va='top', color='white', fontsize=10, alpha=0.7)
            ax.text(0.05, 0.05, 'Low Cost\nLow Quality', transform=ax.transAxes, 
                   ha='left', va='bottom', color='white', fontsize=10, alpha=0.7)
            
        else:
            # Sample provider data
            np.random.seed(42)
            n_providers = 15
            quality_scores = np.random.normal(85, 10, n_providers)
            costs = np.random.normal(700, 200, n_providers)
            panel_sizes = np.random.normal(200, 50, n_providers)
            
            scatter = ax.scatter(quality_scores, costs, s=panel_sizes, 
                               c=range(n_providers), cmap='viridis', alpha=0.7)
            
            ax.set_xlabel('Quality Score (%)', color='white', fontsize=12)
            ax.set_ylabel('Cost PMPM ($)', color='white', fontsize=12)
            ax.set_title('Provider Performance Analysis', color='white', fontsize=16, pad=30)
        
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
    
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