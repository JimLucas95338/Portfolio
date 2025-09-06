#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Analytics Dashboard
Advanced analytics and reporting module based on user feedback and market needs.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class AnalyticsDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Trial Analytics Dashboard - Advanced Reporting")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f5f5f5')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Sample analytics data
        self.analytics_data = self.load_analytics_data()
        self.current_study = None
        
        self.setup_gui()
        self.update_dashboard()
        
    def configure_styles(self):
        """Configure custom styles for the analytics dashboard"""
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f5f5f5')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f5f5f5')
        self.style.configure('Metric.TLabel', font=('Arial', 10), background='#f5f5f5')
        self.style.configure('Success.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#2e7d32')
        self.style.configure('Warning.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#f57c00')
        self.style.configure('Error.TLabel', font=('Arial', 10), background='#f5f5f5', foreground='#d32f2f')
        
    def load_analytics_data(self):
        """Load sample analytics data"""
        return {
            "study_performance": {
                "enrollment_trends": [
                    {"month": "Jan 2025", "target": 50, "actual": 45, "sites": 5},
                    {"month": "Feb 2025", "target": 100, "actual": 87, "sites": 8},
                    {"month": "Mar 2025", "target": 150, "actual": 134, "sites": 12},
                    {"month": "Apr 2025", "target": 200, "actual": 187, "sites": 18},
                    {"month": "May 2025", "target": 250, "actual": 223, "sites": 22},
                    {"month": "Jun 2025", "target": 300, "actual": 267, "sites": 25}
                ],
                "site_performance": [
                    {"site_id": "SITE-001", "name": "Boston Medical Center", "enrollment": 23, "compliance": 96.5, "quality": 98.2, "efficiency": 94.1},
                    {"site_id": "SITE-002", "name": "Mass General Hospital", "enrollment": 19, "compliance": 98.1, "quality": 99.0, "efficiency": 96.3},
                    {"site_id": "SITE-003", "name": "Brigham Women's Hospital", "enrollment": 17, "compliance": 94.8, "quality": 97.5, "efficiency": 92.7},
                    {"site_id": "SITE-004", "name": "Dana-Farber Cancer Institute", "enrollment": 21, "compliance": 97.2, "quality": 98.8, "efficiency": 95.4},
                    {"site_id": "SITE-005", "name": "Beth Israel Deaconess", "enrollment": 15, "compliance": 93.1, "quality": 96.2, "efficiency": 89.8}
                ],
                "predictive_insights": [
                    {"metric": "Enrollment Completion", "prediction": "On Track", "confidence": 87, "timeline": "Dec 2025"},
                    {"metric": "Site Activation Risk", "prediction": "Low Risk", "confidence": 92, "timeline": "Ongoing"},
                    {"metric": "Protocol Deviation", "prediction": "Moderate Risk", "confidence": 78, "timeline": "Next 30 days"},
                    {"metric": "Data Quality", "prediction": "Excellent", "confidence": 95, "timeline": "Ongoing"}
                ]
            },
            "user_analytics": {
                "feature_adoption": [
                    {"feature": "Patient Management", "adoption_rate": 94, "satisfaction": 4.6, "usage_trend": "Increasing"},
                    {"feature": "Visit Scheduling", "adoption_rate": 87, "satisfaction": 4.3, "usage_trend": "Stable"},
                    {"feature": "Compliance Monitoring", "adoption_rate": 91, "satisfaction": 4.5, "usage_trend": "Increasing"},
                    {"feature": "Document Management", "adoption_rate": 78, "satisfaction": 4.1, "usage_trend": "Increasing"},
                    {"feature": "Analytics Dashboard", "adoption_rate": 65, "satisfaction": 4.4, "usage_trend": "Rapidly Increasing"}
                ],
                "user_feedback": [
                    {"date": "2025-09-05", "user": "Dr. Sarah Johnson", "site": "Boston Medical Center", "rating": 5, "feedback": "The new analytics dashboard is incredibly helpful for tracking study progress. The predictive insights are spot-on."},
                    {"date": "2025-09-04", "user": "Mike Chen", "site": "Mass General", "rating": 4, "feedback": "Love the export functionality. Makes reporting to sponsors much easier. Would like to see more customization options."},
                    {"date": "2025-09-03", "user": "Dr. Lisa Rodriguez", "site": "Brigham Women's", "rating": 5, "feedback": "The mobile app improvements are fantastic. Can now complete most tasks on my phone during patient visits."},
                    {"date": "2025-09-02", "user": "Jennifer Park", "site": "Dana-Farber", "rating": 4, "feedback": "Integration with our EDC system is working well. Data sync is much faster than before."},
                    {"date": "2025-09-01", "user": "Dr. Robert Kim", "site": "Beth Israel", "rating": 5, "feedback": "The AI-powered alerts are saving us hours of manual monitoring. Very impressed with the accuracy."}
                ]
            },
            "system_metrics": {
                "performance": {
                    "avg_response_time": 180,  # ms
                    "uptime": 99.8,
                    "error_rate": 0.02,
                    "user_satisfaction": 4.5
                },
                "usage_patterns": {
                    "peak_hours": "9:00 AM - 11:00 AM, 2:00 PM - 4:00 PM",
                    "most_used_features": ["Patient Management", "Visit Scheduling", "Compliance Monitoring"],
                    "mobile_usage": 68,
                    "desktop_usage": 32
                }
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
        title_label = ttk.Label(header_frame, text="Clinical Trial Analytics Dashboard", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Version info
        version_label = ttk.Label(header_frame, text="v2.0 - Advanced Analytics & Reporting", style='Metric.TLabel')
        version_label.grid(row=1, column=0, sticky=tk.W)
        
        # Export and refresh buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        
        ttk.Button(button_frame, text="📊 Export Report", command=self.export_report).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="🔄 Refresh Data", command=self.refresh_data).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="⚙️ Settings", command=self.open_settings).grid(row=0, column=2)
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Analytics Overview tab
        self.create_analytics_overview_tab()
        
        # Study Performance tab
        self.create_study_performance_tab()
        
        # User Analytics tab
        self.create_user_analytics_tab()
        
        # Predictive Insights tab
        self.create_predictive_insights_tab()
        
        # System Metrics tab
        self.create_system_metrics_tab()
    
    def create_analytics_overview_tab(self):
        """Create the analytics overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Analytics Overview")
        
        # Left panel - Key metrics
        left_frame = ttk.Frame(overview_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Key performance indicators
        self.create_kpi_section(left_frame)
        
        # Recent insights
        self.create_insights_section(left_frame)
        
        # Right panel - Charts and trends
        right_frame = ttk.Frame(overview_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Enrollment trends
        self.create_enrollment_trends(right_frame)
        
        # Site performance
        self.create_site_performance(right_frame)
        
        # Configure grid weights
        overview_frame.columnconfigure(0, weight=1)
        overview_frame.columnconfigure(1, weight=1)
        overview_frame.rowconfigure(0, weight=1)
    
    def create_kpi_section(self, parent):
        """Create KPI section"""
        kpi_frame = ttk.LabelFrame(parent, text="Key Performance Indicators", padding="10")
        kpi_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # KPI metrics
        metrics = [
            ("Overall Study Progress", "89%", "On Track"),
            ("Site Activation Rate", "96%", "Excellent"),
            ("Data Quality Score", "98.2%", "Outstanding"),
            ("User Satisfaction", "4.5/5.0", "High"),
            ("System Uptime", "99.8%", "Excellent"),
            ("Mobile Usage", "68%", "Growing")
        ]
        
        for i, (label, value, status) in enumerate(metrics):
            metric_frame = ttk.Frame(kpi_frame)
            metric_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)
            
            ttk.Label(metric_frame, text=label, style='Metric.TLabel').grid(row=0, column=0, sticky=tk.W)
            ttk.Label(metric_frame, text=value, style='Header.TLabel').grid(row=0, column=1, sticky=tk.E)
            ttk.Label(metric_frame, text=status, style='Success.TLabel').grid(row=1, column=0, columnspan=2, sticky=tk.W)
    
    def create_insights_section(self, parent):
        """Create insights section"""
        insights_frame = ttk.LabelFrame(parent, text="Recent Insights", padding="10")
        insights_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.insights_text = scrolledtext.ScrolledText(insights_frame, height=15, width=50)
        self.insights_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.insights_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        insights_frame.columnconfigure(0, weight=1)
        insights_frame.rowconfigure(0, weight=1)
    
    def create_enrollment_trends(self, parent):
        """Create enrollment trends section"""
        trends_frame = ttk.LabelFrame(parent, text="Enrollment Trends", padding="10")
        trends_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Enrollment data table
        self.enrollment_tree = ttk.Treeview(trends_frame, columns=('Month', 'Target', 'Actual', 'Sites'), show='headings', height=8)
        self.enrollment_tree.heading('Month', text='Month')
        self.enrollment_tree.heading('Target', text='Target')
        self.enrollment_tree.heading('Actual', text='Actual')
        self.enrollment_tree.heading('Sites', text='Active Sites')
        
        self.enrollment_tree.column('Month', width=120)
        self.enrollment_tree.column('Target', width=80)
        self.enrollment_tree.column('Actual', width=80)
        self.enrollment_tree.column('Sites', width=100)
        
        self.enrollment_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        trends_frame.columnconfigure(0, weight=1)
        trends_frame.rowconfigure(0, weight=1)
    
    def create_site_performance(self, parent):
        """Create site performance section"""
        performance_frame = ttk.LabelFrame(parent, text="Site Performance Ranking", padding="10")
        performance_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Site performance table
        self.site_tree = ttk.Treeview(performance_frame, columns=('Site', 'Enrollment', 'Compliance', 'Quality', 'Efficiency'), show='headings', height=8)
        self.site_tree.heading('Site', text='Site')
        self.site_tree.heading('Enrollment', text='Enrollment')
        self.site_tree.heading('Compliance', text='Compliance')
        self.site_tree.heading('Quality', text='Quality')
        self.site_tree.heading('Efficiency', text='Efficiency')
        
        self.site_tree.column('Site', width=200)
        self.site_tree.column('Enrollment', width=80)
        self.site_tree.column('Compliance', width=80)
        self.site_tree.column('Quality', width=80)
        self.site_tree.column('Efficiency', width=80)
        
        self.site_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        performance_frame.columnconfigure(0, weight=1)
        performance_frame.rowconfigure(0, weight=1)
    
    def create_study_performance_tab(self):
        """Create study performance tab"""
        performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(performance_frame, text="📈 Study Performance")
        
        # Performance metrics
        metrics_frame = ttk.LabelFrame(performance_frame, text="Performance Metrics", padding="10")
        metrics_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.performance_text = scrolledtext.ScrolledText(metrics_frame, height=20, width=60)
        self.performance_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.performance_text.config(state=tk.DISABLED)
        
        # Benchmarking
        benchmark_frame = ttk.LabelFrame(performance_frame, text="Industry Benchmarking", padding="10")
        benchmark_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.benchmark_text = scrolledtext.ScrolledText(benchmark_frame, height=20, width=60)
        self.benchmark_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.benchmark_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        performance_frame.columnconfigure(0, weight=1)
        performance_frame.columnconfigure(1, weight=1)
        performance_frame.rowconfigure(0, weight=1)
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.rowconfigure(0, weight=1)
        benchmark_frame.columnconfigure(0, weight=1)
        benchmark_frame.rowconfigure(0, weight=1)
    
    def create_user_analytics_tab(self):
        """Create user analytics tab"""
        user_frame = ttk.Frame(self.notebook)
        self.notebook.add(user_frame, text="👥 User Analytics")
        
        # Feature adoption
        adoption_frame = ttk.LabelFrame(user_frame, text="Feature Adoption & Satisfaction", padding="10")
        adoption_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.adoption_tree = ttk.Treeview(adoption_frame, columns=('Feature', 'Adoption', 'Satisfaction', 'Trend'), show='headings', height=10)
        self.adoption_tree.heading('Feature', text='Feature')
        self.adoption_tree.heading('Adoption', text='Adoption Rate')
        self.adoption_tree.heading('Satisfaction', text='Satisfaction')
        self.adoption_tree.heading('Trend', text='Usage Trend')
        
        self.adoption_tree.column('Feature', width=150)
        self.adoption_tree.column('Adoption', width=100)
        self.adoption_tree.column('Satisfaction', width=100)
        self.adoption_tree.column('Trend', width=120)
        
        self.adoption_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # User feedback
        feedback_frame = ttk.LabelFrame(user_frame, text="Recent User Feedback", padding="10")
        feedback_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.feedback_text = scrolledtext.ScrolledText(feedback_frame, height=20, width=60)
        self.feedback_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.feedback_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        user_frame.columnconfigure(0, weight=1)
        user_frame.columnconfigure(1, weight=1)
        user_frame.rowconfigure(0, weight=1)
        adoption_frame.columnconfigure(0, weight=1)
        adoption_frame.rowconfigure(0, weight=1)
        feedback_frame.columnconfigure(0, weight=1)
        feedback_frame.rowconfigure(0, weight=1)
    
    def create_predictive_insights_tab(self):
        """Create predictive insights tab"""
        insights_frame = ttk.Frame(self.notebook)
        self.notebook.add(insights_frame, text="🔮 Predictive Insights")
        
        # AI predictions
        predictions_frame = ttk.LabelFrame(insights_frame, text="AI-Powered Predictions", padding="10")
        predictions_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.predictions_tree = ttk.Treeview(predictions_frame, columns=('Metric', 'Prediction', 'Confidence', 'Timeline'), show='headings', height=10)
        self.predictions_tree.heading('Metric', text='Metric')
        self.predictions_tree.heading('Prediction', text='Prediction')
        self.predictions_tree.heading('Confidence', text='Confidence')
        self.predictions_tree.heading('Timeline', text='Timeline')
        
        self.predictions_tree.column('Metric', width=150)
        self.predictions_tree.column('Prediction', width=120)
        self.predictions_tree.column('Confidence', width=100)
        self.predictions_tree.column('Timeline', width=120)
        
        self.predictions_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Recommendations
        recommendations_frame = ttk.LabelFrame(insights_frame, text="Actionable Recommendations", padding="10")
        recommendations_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.recommendations_text = scrolledtext.ScrolledText(recommendations_frame, height=20, width=60)
        self.recommendations_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.recommendations_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        insights_frame.columnconfigure(0, weight=1)
        insights_frame.columnconfigure(1, weight=1)
        insights_frame.rowconfigure(0, weight=1)
        predictions_frame.columnconfigure(0, weight=1)
        predictions_frame.rowconfigure(0, weight=1)
        recommendations_frame.columnconfigure(0, weight=1)
        recommendations_frame.rowconfigure(0, weight=1)
    
    def create_system_metrics_tab(self):
        """Create system metrics tab"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="⚙️ System Metrics")
        
        # Performance metrics
        perf_frame = ttk.LabelFrame(system_frame, text="System Performance", padding="10")
        perf_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.system_text = scrolledtext.ScrolledText(perf_frame, height=20, width=60)
        self.system_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.system_text.config(state=tk.DISABLED)
        
        # Usage patterns
        usage_frame = ttk.LabelFrame(system_frame, text="Usage Patterns", padding="10")
        usage_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.usage_text = scrolledtext.ScrolledText(usage_frame, height=20, width=60)
        self.usage_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.usage_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        system_frame.columnconfigure(0, weight=1)
        system_frame.columnconfigure(1, weight=1)
        system_frame.rowconfigure(0, weight=1)
        perf_frame.columnconfigure(0, weight=1)
        perf_frame.rowconfigure(0, weight=1)
        usage_frame.columnconfigure(0, weight=1)
        usage_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Analytics Dashboard Ready", style='Metric.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Last updated
        self.last_updated_label = ttk.Label(status_frame, text="", style='Metric.TLabel')
        self.last_updated_label.grid(row=0, column=1, sticky=tk.E)
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        # Update insights
        self.update_insights()
        
        # Update enrollment trends
        self.update_enrollment_trends()
        
        # Update site performance
        self.update_site_performance()
        
        # Update study performance
        self.update_study_performance()
        
        # Update user analytics
        self.update_user_analytics()
        
        # Update predictive insights
        self.update_predictive_insights()
        
        # Update system metrics
        self.update_system_metrics()
        
        # Update status
        self.last_updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_insights(self):
        """Update insights section"""
        self.insights_text.config(state=tk.NORMAL)
        self.insights_text.delete(1.0, tk.END)
        
        insights = [
            "📈 ENROLLMENT TREND: Study is 89% on track for completion by December 2025",
            "🏆 TOP PERFORMING SITE: Mass General Hospital with 98.1% compliance score",
            "📱 MOBILE ADOPTION: 68% of users now prefer mobile interface for daily tasks",
            "🤖 AI ACCURACY: Predictive analytics showing 87% accuracy in enrollment forecasting",
            "⭐ USER SATISFACTION: Overall satisfaction increased to 4.5/5.0 after v2.0 release",
            "🔧 SYSTEM PERFORMANCE: 99.8% uptime with 180ms average response time",
            "📊 DATA QUALITY: 98.2% accuracy rate with automated validation improvements",
            "🚀 FEATURE ADOPTION: Analytics Dashboard showing 65% adoption with rapid growth",
            "💡 RECOMMENDATION: Consider expanding AI insights to protocol deviation prediction",
            "📈 GROWTH OPPORTUNITY: 23% of sites could benefit from additional training"
        ]
        
        for insight in insights:
            self.insights_text.insert(tk.END, insight + "\n\n")
        
        self.insights_text.config(state=tk.DISABLED)
    
    def update_enrollment_trends(self):
        """Update enrollment trends table"""
        # Clear existing items
        for item in self.enrollment_tree.get_children():
            self.enrollment_tree.delete(item)
        
        # Add enrollment data
        for trend in self.analytics_data['study_performance']['enrollment_trends']:
            self.enrollment_tree.insert('', 'end', values=(
                trend['month'],
                trend['target'],
                trend['actual'],
                trend['sites']
            ))
    
    def update_site_performance(self):
        """Update site performance table"""
        # Clear existing items
        for item in self.site_tree.get_children():
            self.site_tree.delete(item)
        
        # Add site performance data
        for site in self.analytics_data['study_performance']['site_performance']:
            self.site_tree.insert('', 'end', values=(
                site['name'],
                site['enrollment'],
                f"{site['compliance']}%",
                f"{site['quality']}%",
                f"{site['efficiency']}%"
            ))
    
    def update_study_performance(self):
        """Update study performance section"""
        self.performance_text.config(state=tk.NORMAL)
        self.performance_text.delete(1.0, tk.END)
        
        performance_data = """
STUDY PERFORMANCE ANALYSIS
==========================

OVERALL METRICS:
• Study Progress: 89% on track
• Enrollment Rate: 89% of target achieved
• Site Activation: 96% of planned sites active
• Data Quality: 98.2% accuracy rate
• Protocol Compliance: 95.1% adherence rate

MONTHLY TRENDS:
• January: 90% of target (45/50 patients)
• February: 87% of target (87/100 patients)
• March: 89% of target (134/150 patients)
• April: 94% of target (187/200 patients)
• May: 89% of target (223/250 patients)
• June: 89% of target (267/300 patients)

SITE PERFORMANCE RANKING:
1. Mass General Hospital - 98.1% compliance
2. Dana-Farber Cancer Institute - 97.2% compliance
3. Boston Medical Center - 96.5% compliance
4. Brigham Women's Hospital - 94.8% compliance
5. Beth Israel Deaconess - 93.1% compliance

KEY ACHIEVEMENTS:
• Reduced protocol deviations by 45%
• Improved data entry accuracy by 23%
• Decreased query resolution time by 60%
• Increased site satisfaction to 4.5/5.0

AREAS FOR IMPROVEMENT:
• Site 5 (Beth Israel) needs additional support
• Protocol deviation risk in next 30 days
• Consider expanding to additional sites
        """
        
        self.performance_text.insert(tk.END, performance_data)
        self.performance_text.config(state=tk.DISABLED)
    
    def update_user_analytics(self):
        """Update user analytics"""
        # Update feature adoption table
        for item in self.adoption_tree.get_children():
            self.adoption_tree.delete(item)
        
        for feature in self.analytics_data['user_analytics']['feature_adoption']:
            self.adoption_tree.insert('', 'end', values=(
                feature['feature'],
                f"{feature['adoption_rate']}%",
                f"{feature['satisfaction']}/5.0",
                feature['usage_trend']
            ))
        
        # Update user feedback
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        
        for feedback in self.analytics_data['user_analytics']['user_feedback']:
            self.feedback_text.insert(tk.END, f"Date: {feedback['date']}\n")
            self.feedback_text.insert(tk.END, f"User: {feedback['user']} ({feedback['site']})\n")
            self.feedback_text.insert(tk.END, f"Rating: {'⭐' * feedback['rating']} ({feedback['rating']}/5)\n")
            self.feedback_text.insert(tk.END, f"Feedback: {feedback['feedback']}\n")
            self.feedback_text.insert(tk.END, "-" * 60 + "\n\n")
        
        self.feedback_text.config(state=tk.DISABLED)
    
    def update_predictive_insights(self):
        """Update predictive insights"""
        # Update predictions table
        for item in self.predictions_tree.get_children():
            self.predictions_tree.delete(item)
        
        for prediction in self.analytics_data['study_performance']['predictive_insights']:
            self.predictions_tree.insert('', 'end', values=(
                prediction['metric'],
                prediction['prediction'],
                f"{prediction['confidence']}%",
                prediction['timeline']
            ))
        
        # Update recommendations
        self.recommendations_text.config(state=tk.NORMAL)
        self.recommendations_text.delete(1.0, tk.END)
        
        recommendations = """
ACTIONABLE RECOMMENDATIONS
==========================

IMMEDIATE ACTIONS (Next 7 days):
• Provide additional training to Beth Israel site staff
• Review protocol deviation patterns for Site 3
• Implement mobile app training for remaining 32% of users

SHORT-TERM ACTIONS (Next 30 days):
• Expand AI insights to protocol deviation prediction
• Add custom reporting templates for sponsor requests
• Implement advanced data visualization features

MEDIUM-TERM ACTIONS (Next 90 days):
• Develop integration with additional EDC systems
• Create automated compliance reporting workflows
• Launch predictive analytics for site performance

STRATEGIC INITIATIVES (Next 6 months):
• Expand platform to support Phase I/II studies
• Develop machine learning models for patient recruitment
• Create industry benchmarking capabilities

RISK MITIGATION:
• Monitor Site 5 performance closely
• Prepare contingency plans for enrollment shortfalls
• Implement additional data validation rules

OPPORTUNITY AREAS:
• 23% of sites could benefit from advanced training
• Mobile usage growth indicates need for enhanced mobile features
• High user satisfaction suggests expansion opportunities
        """
        
        self.recommendations_text.insert(tk.END, recommendations)
        self.recommendations_text.config(state=tk.DISABLED)
    
    def update_system_metrics(self):
        """Update system metrics"""
        # Update system performance
        self.system_text.config(state=tk.NORMAL)
        self.system_text.delete(1.0, tk.END)
        
        perf_data = self.analytics_data['system_metrics']['performance']
        system_info = f"""
SYSTEM PERFORMANCE METRICS
==========================

RESPONSE TIME:
• Average Response Time: {perf_data['avg_response_time']}ms
• 95th Percentile: 250ms
• 99th Percentile: 400ms

AVAILABILITY:
• System Uptime: {perf_data['uptime']}%
• Planned Maintenance: 0.1%
• Unplanned Downtime: 0.1%

ERROR RATES:
• Overall Error Rate: {perf_data['error_rate']}%
• API Error Rate: 0.01%
• Database Error Rate: 0.01%

USER EXPERIENCE:
• User Satisfaction: {perf_data['user_satisfaction']}/5.0
• Page Load Time: 1.2s average
• Mobile Performance: 1.5s average

SCALABILITY:
• Concurrent Users: 2,500 (peak)
• Database Connections: 150 (active)
• API Requests: 50,000/day

SECURITY:
• Security Incidents: 0
• Failed Login Attempts: 12/day
• Data Breaches: 0
        """
        
        self.system_text.insert(tk.END, system_info)
        self.system_text.config(state=tk.DISABLED)
        
        # Update usage patterns
        self.usage_text.config(state=tk.NORMAL)
        self.usage_text.delete(1.0, tk.END)
        
        usage_data = self.analytics_data['system_metrics']['usage_patterns']
        usage_info = f"""
USAGE PATTERNS & ANALYTICS
==========================

PEAK USAGE HOURS:
{usage_data['peak_hours']}

MOST USED FEATURES:
1. {usage_data['most_used_features'][0]}
2. {usage_data['most_used_features'][1]}
3. {usage_data['most_used_features'][2]}

DEVICE USAGE:
• Mobile: {usage_data['mobile_usage']}%
• Desktop: {usage_data['desktop_usage']}%

USER BEHAVIOR:
• Average Session Duration: 23 minutes
• Pages per Session: 8.5
• Bounce Rate: 12%

GEOGRAPHIC DISTRIBUTION:
• North America: 65%
• Europe: 25%
• Asia-Pacific: 10%

FEATURE ADOPTION TRENDS:
• Patient Management: 94% adoption
• Visit Scheduling: 87% adoption
• Compliance Monitoring: 91% adoption
• Analytics Dashboard: 65% adoption (growing)
        """
        
        self.usage_text.insert(tk.END, usage_info)
        self.usage_text.config(state=tk.DISABLED)
    
    def export_report(self):
        """Export analytics report"""
        messagebox.showinfo("Export Report", "Analytics report exported successfully!\n\nReport includes:\n• Study performance metrics\n• User analytics and feedback\n• Predictive insights\n• System performance data\n• Actionable recommendations")
    
    def refresh_data(self):
        """Refresh analytics data"""
        self.status_label.config(text="Refreshing analytics data...")
        self.root.update()
        
        # Simulate data refresh
        time.sleep(1)
        
        self.update_dashboard()
        self.status_label.config(text="Analytics data refreshed successfully")
    
    def open_settings(self):
        """Open analytics settings"""
        messagebox.showinfo("Analytics Settings", "Analytics settings dialog would open here.\n\nSettings include:\n• Report customization\n• Data refresh intervals\n• Alert thresholds\n• Export preferences")

def main():
    """Main function to run the analytics dashboard"""
    root = tk.Tk()
    app = AnalyticsDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
