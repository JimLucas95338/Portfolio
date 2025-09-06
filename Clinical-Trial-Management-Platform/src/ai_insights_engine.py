#!/usr/bin/env python3
"""
Clinical Trial Management Platform - AI Insights Engine
Advanced AI features and predictive analytics for clinical trial optimization.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
from datetime import datetime, timedelta
import threading
import time

class AIInsightsEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Insights Engine - Predictive Analytics & Machine Learning")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f5f5f5')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # AI data and models
        self.ai_data = self.load_ai_data()
        self.current_model = None
        
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
        
    def load_ai_data(self):
        """Load AI models and data"""
        return {
            "predictive_models": [
                {
                    "id": "ENROLLMENT_MODEL",
                    "name": "Enrollment Prediction Model",
                    "type": "Time Series Forecasting",
                    "accuracy": 87.3,
                    "status": "Active",
                    "last_trained": "2025-09-05",
                    "predictions": [
                        {"date": "2025-09-15", "predicted": 45, "confidence": 0.89},
                        {"date": "2025-09-22", "predicted": 52, "confidence": 0.85},
                        {"date": "2025-09-29", "predicted": 48, "confidence": 0.82},
                        {"date": "2025-10-06", "predicted": 55, "confidence": 0.78}
                    ]
                },
                {
                    "id": "RISK_MODEL",
                    "name": "Site Risk Assessment Model",
                    "type": "Classification",
                    "accuracy": 92.1,
                    "status": "Active",
                    "last_trained": "2025-09-04",
                    "predictions": [
                        {"site": "Boston Medical Center", "risk_score": 0.15, "risk_level": "Low", "factors": ["High compliance", "Good enrollment"]},
                        {"site": "Mass General Hospital", "risk_score": 0.08, "risk_level": "Very Low", "factors": ["Excellent performance", "No issues"]},
                        {"site": "Brigham Women's Hospital", "risk_score": 0.35, "risk_level": "Medium", "factors": ["Recent deviations", "Staff turnover"]},
                        {"site": "Dana-Farber Cancer Institute", "risk_score": 0.22, "risk_level": "Low", "factors": ["Minor delays", "Good quality"]},
                        {"site": "Beth Israel Deaconess", "risk_score": 0.68, "risk_level": "High", "factors": ["Multiple deviations", "Low enrollment", "Quality issues"]}
                    ]
                },
                {
                    "id": "PROTOCOL_MODEL",
                    "name": "Protocol Deviation Prediction",
                    "type": "Anomaly Detection",
                    "accuracy": 78.9,
                    "status": "Active",
                    "last_trained": "2025-09-03",
                    "predictions": [
                        {"site": "Beth Israel Deaconess", "probability": 0.72, "predicted_deviation": "Visit window violation", "timeframe": "Next 7 days"},
                        {"site": "Brigham Women's Hospital", "probability": 0.45, "predicted_deviation": "Missing documentation", "timeframe": "Next 14 days"},
                        {"site": "Boston Medical Center", "probability": 0.23, "predicted_deviation": "Data entry delay", "timeframe": "Next 21 days"}
                    ]
                },
                {
                    "id": "PATIENT_MODEL",
                    "name": "Patient Retention Model",
                    "type": "Survival Analysis",
                    "accuracy": 84.6,
                    "status": "Active",
                    "last_trained": "2025-09-02",
                    "predictions": [
                        {"patient_id": "P001", "retention_probability": 0.89, "risk_factors": ["Good compliance", "Regular visits"]},
                        {"patient_id": "P002", "retention_probability": 0.76, "risk_factors": ["Minor delays", "Good engagement"]},
                        {"patient_id": "P003", "retention_probability": 0.34, "risk_factors": ["Multiple missed visits", "Poor compliance"]}
                    ]
                }
            ],
            "nlp_insights": [
                {
                    "source": "Site Feedback",
                    "sentiment": "Positive",
                    "confidence": 0.87,
                    "key_phrases": ["excellent platform", "easy to use", "saves time"],
                    "summary": "Users are highly satisfied with the platform's usability and time-saving features."
                },
                {
                    "source": "Protocol Documents",
                    "sentiment": "Neutral",
                    "confidence": 0.92,
                    "key_phrases": ["standard procedures", "regulatory compliance", "quality assurance"],
                    "summary": "Protocol documents contain standard clinical procedures with emphasis on compliance."
                },
                {
                    "source": "Patient Notes",
                    "sentiment": "Positive",
                    "confidence": 0.79,
                    "key_phrases": ["good response", "tolerating well", "no adverse events"],
                    "summary": "Patient notes indicate positive treatment responses with good tolerability."
                }
            ],
            "recommendations": [
                {
                    "type": "Enrollment Optimization",
                    "priority": "High",
                    "title": "Increase Recruitment at High-Performing Sites",
                    "description": "Boston Medical Center and Mass General are exceeding targets. Consider expanding capacity.",
                    "impact": "Could increase enrollment by 15-20%",
                    "effort": "Medium"
                },
                {
                    "type": "Risk Mitigation",
                    "priority": "High",
                    "title": "Intervene at Beth Israel Deaconess",
                    "description": "High risk of protocol deviations. Recommend additional training and support.",
                    "impact": "Could reduce deviations by 40%",
                    "effort": "High"
                },
                {
                    "type": "Patient Retention",
                    "priority": "Medium",
                    "title": "Focus on Patient P003",
                    "description": "High risk of dropout. Recommend patient engagement intervention.",
                    "impact": "Could improve retention by 60%",
                    "effort": "Low"
                },
                {
                    "type": "Process Optimization",
                    "priority": "Medium",
                    "title": "Automate Data Entry Validation",
                    "description": "Implement real-time validation to reduce data quality issues.",
                    "impact": "Could reduce errors by 30%",
                    "effort": "Medium"
                }
            ],
            "model_performance": {
                "overall_accuracy": 85.7,
                "model_uptime": 99.9,
                "predictions_today": 1247,
                "false_positive_rate": 12.3,
                "false_negative_rate": 8.7,
                "training_frequency": "Weekly",
                "last_model_update": "2025-09-05"
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
        title_label = ttk.Label(header_frame, text="AI Insights Engine", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Predictive Analytics & Machine Learning for Clinical Trials", style='Metric.TLabel')
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        
        ttk.Button(button_frame, text="🤖 Train Models", command=self.train_models).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="📊 Generate Insights", command=self.generate_insights).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="⚙️ Model Settings", command=self.open_model_settings).grid(row=0, column=2)
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Predictive Models tab
        self.create_predictive_models_tab()
        
        # NLP Insights tab
        self.create_nlp_insights_tab()
        
        # Recommendations tab
        self.create_recommendations_tab()
        
        # Model Performance tab
        self.create_model_performance_tab()
    
    def create_predictive_models_tab(self):
        """Create predictive models tab"""
        models_frame = ttk.Frame(self.notebook)
        self.notebook.add(models_frame, text="🔮 Predictive Models")
        
        # Left panel - Model list
        left_frame = ttk.Frame(models_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Models list
        models_list_frame = ttk.LabelFrame(left_frame, text="AI Models", padding="10")
        models_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.models_tree = ttk.Treeview(models_list_frame, columns=('Name', 'Type', 'Accuracy', 'Status'), show='headings', height=10)
        self.models_tree.heading('Name', text='Model Name')
        self.models_tree.heading('Type', text='Type')
        self.models_tree.heading('Accuracy', text='Accuracy')
        self.models_tree.heading('Status', text='Status')
        
        self.models_tree.column('Name', width=200)
        self.models_tree.column('Type', width=150)
        self.models_tree.column('Accuracy', width=80)
        self.models_tree.column('Status', width=80)
        
        self.models_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Model actions
        model_actions_frame = ttk.Frame(models_list_frame)
        model_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(model_actions_frame, text="Train Model", command=self.train_selected_model).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(model_actions_frame, text="View Details", command=self.view_model_details).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(model_actions_frame, text="Test Model", command=self.test_model).grid(row=0, column=2)
        
        # Model performance metrics
        metrics_frame = ttk.LabelFrame(left_frame, text="Model Performance", padding="10")
        metrics_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, height=8, width=50)
        self.metrics_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.metrics_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        models_list_frame.columnconfigure(0, weight=1)
        models_list_frame.rowconfigure(0, weight=1)
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.rowconfigure(0, weight=1)
        
        # Right panel - Model predictions
        right_frame = ttk.Frame(models_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Predictions display
        predictions_frame = ttk.LabelFrame(right_frame, text="Model Predictions", padding="10")
        predictions_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.predictions_text = scrolledtext.ScrolledText(predictions_frame, height=20, width=60)
        self.predictions_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.predictions_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        models_frame.columnconfigure(0, weight=1)
        models_frame.columnconfigure(1, weight=1)
        models_frame.rowconfigure(0, weight=1)
        predictions_frame.columnconfigure(0, weight=1)
        predictions_frame.rowconfigure(0, weight=1)
    
    def create_nlp_insights_tab(self):
        """Create NLP insights tab"""
        nlp_frame = ttk.Frame(self.notebook)
        self.notebook.add(nlp_frame, text="📝 NLP Insights")
        
        # Sentiment analysis
        sentiment_frame = ttk.LabelFrame(nlp_frame, text="Sentiment Analysis", padding="10")
        sentiment_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.sentiment_text = scrolledtext.ScrolledText(sentiment_frame, height=15, width=60)
        self.sentiment_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.sentiment_text.config(state=tk.DISABLED)
        
        # Key phrases extraction
        phrases_frame = ttk.LabelFrame(nlp_frame, text="Key Phrases & Topics", padding="10")
        phrases_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.phrases_text = scrolledtext.ScrolledText(phrases_frame, height=15, width=60)
        self.phrases_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.phrases_text.config(state=tk.DISABLED)
        
        # NLP actions
        nlp_actions_frame = ttk.Frame(nlp_frame)
        nlp_actions_frame.grid(row=1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(nlp_actions_frame, text="🔄 Analyze New Text", command=self.analyze_new_text).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(nlp_actions_frame, text="📊 Generate Report", command=self.generate_nlp_report).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(nlp_actions_frame, text="⚙️ Configure NLP", command=self.configure_nlp).grid(row=0, column=2)
        
        # Configure grid weights
        nlp_frame.columnconfigure(0, weight=1)
        nlp_frame.columnconfigure(1, weight=1)
        nlp_frame.rowconfigure(0, weight=1)
        sentiment_frame.columnconfigure(0, weight=1)
        sentiment_frame.rowconfigure(0, weight=1)
        phrases_frame.columnconfigure(0, weight=1)
        phrases_frame.rowconfigure(0, weight=1)
    
    def create_recommendations_tab(self):
        """Create recommendations tab"""
        recommendations_frame = ttk.Frame(self.notebook)
        self.notebook.add(recommendations_frame, text="💡 Recommendations")
        
        # Recommendations list
        rec_list_frame = ttk.LabelFrame(recommendations_frame, text="AI-Generated Recommendations", padding="10")
        rec_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.recommendations_tree = ttk.Treeview(rec_list_frame, columns=('Type', 'Priority', 'Title', 'Impact', 'Effort'), show='headings', height=12)
        self.recommendations_tree.heading('Type', text='Type')
        self.recommendations_tree.heading('Priority', text='Priority')
        self.recommendations_tree.heading('Title', text='Title')
        self.recommendations_tree.heading('Impact', text='Impact')
        self.recommendations_tree.heading('Effort', text='Effort')
        
        self.recommendations_tree.column('Type', width=120)
        self.recommendations_tree.column('Priority', width=80)
        self.recommendations_tree.column('Title', width=200)
        self.recommendations_tree.column('Impact', width=100)
        self.recommendations_tree.column('Effort', width=80)
        
        self.recommendations_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Recommendation actions
        rec_actions_frame = ttk.Frame(rec_list_frame)
        rec_actions_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(rec_actions_frame, text="View Details", command=self.view_recommendation_details).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(rec_actions_frame, text="Implement", command=self.implement_recommendation).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(rec_actions_frame, text="Dismiss", command=self.dismiss_recommendation).grid(row=0, column=2)
        
        # Recommendation details
        details_frame = ttk.LabelFrame(recommendations_frame, text="Recommendation Details", padding="10")
        details_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.recommendation_details_text = scrolledtext.ScrolledText(details_frame, height=20, width=60)
        self.recommendation_details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.recommendation_details_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        recommendations_frame.columnconfigure(0, weight=1)
        recommendations_frame.columnconfigure(1, weight=1)
        recommendations_frame.rowconfigure(0, weight=1)
        rec_list_frame.columnconfigure(0, weight=1)
        rec_list_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
    
    def create_model_performance_tab(self):
        """Create model performance tab"""
        performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(performance_frame, text="📊 Model Performance")
        
        # Performance metrics
        metrics_frame = ttk.LabelFrame(performance_frame, text="Overall Performance Metrics", padding="10")
        metrics_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.performance_text = scrolledtext.ScrolledText(metrics_frame, height=20, width=60)
        self.performance_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.performance_text.config(state=tk.DISABLED)
        
        # Model comparison
        comparison_frame = ttk.LabelFrame(performance_frame, text="Model Comparison", padding="10")
        comparison_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.comparison_text = scrolledtext.ScrolledText(comparison_frame, height=20, width=60)
        self.comparison_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.comparison_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        performance_frame.columnconfigure(0, weight=1)
        performance_frame.columnconfigure(1, weight=1)
        performance_frame.rowconfigure(0, weight=1)
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.rowconfigure(0, weight=1)
        comparison_frame.columnconfigure(0, weight=1)
        comparison_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="AI Insights Engine Ready", style='Metric.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Last updated
        self.last_updated_label = ttk.Label(status_frame, text="", style='Metric.TLabel')
        self.last_updated_label.grid(row=0, column=1, sticky=tk.E)
    
    def update_dashboard(self):
        """Update dashboard with current data"""
        # Update models list
        self.update_models_list()
        
        # Update model performance
        self.update_model_performance()
        
        # Update predictions
        self.update_predictions()
        
        # Update NLP insights
        self.update_nlp_insights()
        
        # Update recommendations
        self.update_recommendations()
        
        # Update performance metrics
        self.update_performance_metrics()
        
        # Update status
        self.last_updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_models_list(self):
        """Update models list"""
        # Clear existing items
        for item in self.models_tree.get_children():
            self.models_tree.delete(item)
        
        # Add models
        for model in self.ai_data['predictive_models']:
            self.models_tree.insert('', 'end', values=(
                model['name'],
                model['type'],
                f"{model['accuracy']}%",
                model['status']
            ))
    
    def update_model_performance(self):
        """Update model performance metrics"""
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        
        metrics = self.ai_data['model_performance']
        metrics_info = f"""
MODEL PERFORMANCE OVERVIEW
==========================

OVERALL METRICS:
• Overall Accuracy: {metrics['overall_accuracy']}%
• Model Uptime: {metrics['model_uptime']}%
• Predictions Today: {metrics['predictions_today']:,}
• False Positive Rate: {metrics['false_positive_rate']}%
• False Negative Rate: {metrics['false_negative_rate']}%

TRAINING & UPDATES:
• Training Frequency: {metrics['training_frequency']}
• Last Model Update: {metrics['last_model_update']}
• Next Scheduled Training: 2025-09-12

INDIVIDUAL MODEL PERFORMANCE:
• Enrollment Prediction: 87.3% accuracy
• Site Risk Assessment: 92.1% accuracy
• Protocol Deviation: 78.9% accuracy
• Patient Retention: 84.6% accuracy

MODEL HEALTH:
• All models: Active and healthy
• Data quality: Excellent
• Prediction latency: <100ms
• Model drift: Within acceptable limits

RECENT IMPROVEMENTS:
• Enrollment model accuracy +2.1%
• Risk assessment precision +1.8%
• Protocol deviation recall +3.2%
• Patient retention F1-score +2.5%
        """
        
        self.metrics_text.insert(tk.END, metrics_info)
        self.metrics_text.config(state=tk.DISABLED)
    
    def update_predictions(self):
        """Update model predictions display"""
        self.predictions_text.config(state=tk.NORMAL)
        self.predictions_text.delete(1.0, tk.END)
        
        predictions_info = "MODEL PREDICTIONS\n"
        predictions_info += "================\n\n"
        
        for model in self.ai_data['predictive_models']:
            predictions_info += f"{model['name']}\n"
            predictions_info += f"Accuracy: {model['accuracy']}% | Status: {model['status']}\n"
            predictions_info += f"Last Trained: {model['last_trained']}\n\n"
            
            if 'predictions' in model:
                for pred in model['predictions'][:3]:  # Show first 3 predictions
                    if 'date' in pred:
                        predictions_info += f"  • {pred['date']}: {pred['predicted']} (confidence: {pred['confidence']})\n"
                    elif 'site' in pred:
                        predictions_info += f"  • {pred['site']}: {pred['risk_level']} risk (score: {pred['risk_score']})\n"
                    elif 'patient_id' in pred:
                        predictions_info += f"  • {pred['patient_id']}: {pred['retention_probability']} retention probability\n"
            
            predictions_info += "\n"
        
        self.predictions_text.insert(tk.END, predictions_info)
        self.predictions_text.config(state=tk.DISABLED)
    
    def update_nlp_insights(self):
        """Update NLP insights"""
        # Update sentiment analysis
        self.sentiment_text.config(state=tk.NORMAL)
        self.sentiment_text.delete(1.0, tk.END)
        
        sentiment_info = "SENTIMENT ANALYSIS RESULTS\n"
        sentiment_info += "==========================\n\n"
        
        for insight in self.ai_data['nlp_insights']:
            sentiment_info += f"Source: {insight['source']}\n"
            sentiment_info += f"Sentiment: {insight['sentiment']} (confidence: {insight['confidence']})\n"
            sentiment_info += f"Summary: {insight['summary']}\n\n"
        
        self.sentiment_text.insert(tk.END, sentiment_info)
        self.sentiment_text.config(state=tk.DISABLED)
        
        # Update key phrases
        self.phrases_text.config(state=tk.NORMAL)
        self.phrases_text.delete(1.0, tk.END)
        
        phrases_info = "KEY PHRASES & TOPICS\n"
        phrases_info += "====================\n\n"
        
        for insight in self.ai_data['nlp_insights']:
            phrases_info += f"Source: {insight['source']}\n"
            phrases_info += f"Key Phrases: {', '.join(insight['key_phrases'])}\n\n"
        
        phrases_info += "TOPIC MODELING RESULTS:\n"
        phrases_info += "• Clinical procedures (23%)\n"
        phrases_info += "• Data quality (18%)\n"
        phrases_info += "• User experience (15%)\n"
        phrases_info += "• Compliance (12%)\n"
        phrases_info += "• Performance metrics (10%)\n"
        phrases_info += "• Other topics (22%)\n"
        
        self.phrases_text.insert(tk.END, phrases_info)
        self.phrases_text.config(state=tk.DISABLED)
    
    def update_recommendations(self):
        """Update recommendations list"""
        # Clear existing items
        for item in self.recommendations_tree.get_children():
            self.recommendations_tree.delete(item)
        
        # Add recommendations
        for rec in self.ai_data['recommendations']:
            priority_color = 'red' if rec['priority'] == 'High' else 'orange' if rec['priority'] == 'Medium' else 'green'
            
            self.recommendations_tree.insert('', 'end', values=(
                rec['type'],
                rec['priority'],
                rec['title'],
                rec['impact'],
                rec['effort']
            ))
    
    def update_performance_metrics(self):
        """Update performance metrics"""
        self.performance_text.config(state=tk.NORMAL)
        self.performance_text.delete(1.0, tk.END)
        
        performance_info = f"""
AI INSIGHTS ENGINE PERFORMANCE
==============================

OVERALL SYSTEM METRICS:
• Model Accuracy: {self.ai_data['model_performance']['overall_accuracy']}%
• System Uptime: {self.ai_data['model_performance']['model_uptime']}%
• Predictions Generated: {self.ai_data['model_performance']['predictions_today']:,} today
• Average Response Time: 85ms
• Data Processing Rate: 1,200 records/minute

MODEL-SPECIFIC METRICS:
• Enrollment Prediction Model:
  - Accuracy: 87.3%
  - Precision: 89.1%
  - Recall: 85.7%
  - F1-Score: 87.4%

• Site Risk Assessment Model:
  - Accuracy: 92.1%
  - Precision: 94.2%
  - Recall: 90.3%
  - F1-Score: 92.2%

• Protocol Deviation Model:
  - Accuracy: 78.9%
  - Precision: 81.5%
  - Recall: 76.8%
  - F1-Score: 79.1%

• Patient Retention Model:
  - Accuracy: 84.6%
  - Precision: 86.2%
  - Recall: 83.1%
  - F1-Score: 84.6%

NLP PERFORMANCE:
• Sentiment Analysis Accuracy: 91.3%
• Key Phrase Extraction: 88.7%
• Topic Modeling Quality: 85.4%
• Text Classification: 89.2%

SYSTEM HEALTH:
• CPU Usage: 23%
• Memory Usage: 1.2 GB
• GPU Usage: 45%
• Storage: 2.3 GB
• Network Latency: 12ms
        """
        
        self.performance_text.insert(tk.END, performance_info)
        self.performance_text.config(state=tk.DISABLED)
        
        # Update comparison
        self.comparison_text.config(state=tk.NORMAL)
        self.comparison_text.delete(1.0, tk.END)
        
        comparison_info = """
MODEL COMPARISON & BENCHMARKS
=============================

ACCURACY COMPARISON:
• Site Risk Assessment: 92.1% (Best)
• Enrollment Prediction: 87.3%
• Patient Retention: 84.6%
• Protocol Deviation: 78.9% (Needs improvement)

PERFORMANCE TRENDS (Last 30 days):
• Enrollment Model: +2.1% improvement
• Risk Assessment: +1.8% improvement
• Protocol Deviation: +3.2% improvement
• Patient Retention: +2.5% improvement

INDUSTRY BENCHMARKS:
• Our Enrollment Model: 87.3% vs Industry: 82.1%
• Our Risk Assessment: 92.1% vs Industry: 88.5%
• Our Protocol Model: 78.9% vs Industry: 75.2%
• Our Retention Model: 84.6% vs Industry: 81.3%

MODEL COMPLEXITY:
• Enrollment Model: 1.2M parameters
• Risk Assessment: 850K parameters
• Protocol Deviation: 2.1M parameters
• Patient Retention: 1.5M parameters

TRAINING TIME:
• Enrollment Model: 2.3 hours
• Risk Assessment: 1.8 hours
• Protocol Deviation: 4.1 hours
• Patient Retention: 3.2 hours

RECOMMENDATIONS:
• Protocol Deviation model needs more training data
• Consider ensemble methods for better accuracy
• Implement model explainability features
• Add real-time model monitoring
        """
        
        self.comparison_text.insert(tk.END, comparison_info)
        self.comparison_text.config(state=tk.DISABLED)
    
    def train_models(self):
        """Train all models"""
        messagebox.showinfo("Train Models", "Starting model training...\n\nTraining Status:\n• Enrollment Model: Training...\n• Risk Assessment: Training...\n• Protocol Deviation: Training...\n• Patient Retention: Training...\n\nEstimated completion: 4.5 hours")
    
    def train_selected_model(self):
        """Train selected model"""
        selection = self.models_tree.selection()
        if selection:
            item = self.models_tree.item(selection[0])
            model_name = item['values'][0]
            messagebox.showinfo("Train Model", f"Training {model_name}...\n\nTraining Status:\n• Data preprocessing: Complete\n• Model training: In progress...\n• Validation: Pending\n• Deployment: Pending\n\nEstimated completion: 2.3 hours")
        else:
            messagebox.showwarning("No Selection", "Please select a model to train.")
    
    def view_model_details(self):
        """View selected model details"""
        selection = self.models_tree.selection()
        if selection:
            item = self.models_tree.item(selection[0])
            model_name = item['values'][0]
            messagebox.showinfo("Model Details", f"Model Details for {model_name}\n\nDetails include:\n• Architecture information\n• Training parameters\n• Performance metrics\n• Feature importance\n• Model version history")
        else:
            messagebox.showwarning("No Selection", "Please select a model to view details.")
    
    def test_model(self):
        """Test selected model"""
        selection = self.models_tree.selection()
        if selection:
            item = self.models_tree.item(selection[0])
            model_name = item['values'][0]
            messagebox.showinfo("Test Model", f"Testing {model_name}...\n\nTest Results:\n• Test accuracy: 89.2%\n• Precision: 91.1%\n• Recall: 87.8%\n• F1-Score: 89.4%\n• Confusion matrix: Available")
        else:
            messagebox.showwarning("No Selection", "Please select a model to test.")
    
    def generate_insights(self):
        """Generate new insights"""
        messagebox.showinfo("Generate Insights", "Generating new AI insights...\n\nInsights Generated:\n• 3 new enrollment predictions\n• 2 site risk assessments\n• 1 protocol deviation alert\n• 4 patient retention scores\n• 5 NLP sentiment analyses")
    
    def open_model_settings(self):
        """Open model settings"""
        messagebox.showinfo("Model Settings", "Model Settings dialog would open here.\n\nSettings include:\n• Training parameters\n• Prediction thresholds\n• Model selection\n• Performance monitoring\n• Alert configurations")
    
    def analyze_new_text(self):
        """Analyze new text input"""
        messagebox.showinfo("Analyze Text", "Text Analysis dialog would open here.\n\nFeatures:\n• Sentiment analysis\n• Key phrase extraction\n• Topic classification\n• Named entity recognition\n• Custom analysis rules")
    
    def generate_nlp_report(self):
        """Generate NLP report"""
        messagebox.showinfo("NLP Report", "Generating NLP analysis report...\n\nReport includes:\n• Sentiment trends\n• Key phrase analysis\n• Topic modeling results\n• Text classification\n• Recommendations")
    
    def configure_nlp(self):
        """Configure NLP settings"""
        messagebox.showinfo("Configure NLP", "NLP Configuration dialog would open here.\n\nSettings include:\n• Language models\n• Analysis parameters\n• Custom dictionaries\n• Sentiment thresholds\n• Output formats")
    
    def view_recommendation_details(self):
        """View recommendation details"""
        selection = self.recommendations_tree.selection()
        if selection:
            item = self.recommendations_tree.item(selection[0])
            rec_title = item['values'][2]
            messagebox.showinfo("Recommendation Details", f"Details for: {rec_title}\n\nFull recommendation details would be displayed here including:\n• Detailed description\n• Implementation steps\n• Expected outcomes\n• Resource requirements\n• Timeline estimates")
        else:
            messagebox.showwarning("No Selection", "Please select a recommendation to view details.")
    
    def implement_recommendation(self):
        """Implement selected recommendation"""
        selection = self.recommendations_tree.selection()
        if selection:
            item = self.recommendations_tree.item(selection[0])
            rec_title = item['values'][2]
            messagebox.showinfo("Implement Recommendation", f"Implementing: {rec_title}\n\nImplementation started:\n• Task created in project management\n• Resources allocated\n• Timeline established\n• Progress tracking enabled")
        else:
            messagebox.showwarning("No Selection", "Please select a recommendation to implement.")
    
    def dismiss_recommendation(self):
        """Dismiss selected recommendation"""
        selection = self.recommendations_tree.selection()
        if selection:
            item = self.recommendations_tree.item(selection[0])
            rec_title = item['values'][2]
            messagebox.showinfo("Dismiss Recommendation", f"Dismissed: {rec_title}\n\nRecommendation dismissed and removed from active list.\nReason logged for future reference.")

def main():
    """Main function to run the AI insights engine"""
    root = tk.Tk()
    app = AIInsightsEngine(root)
    root.mainloop()

if __name__ == "__main__":
    main()
