"""
AI Content Optimization Dashboard - Main Application
==================================================

Professional dashboard application for the AI Content Optimization Platform.
Provides comprehensive content analysis, optimization recommendations,
and performance tracking in an intuitive user interface.

Key Features:
- Real-time content analysis and optimization
- Multi-platform content optimization
- Performance prediction and benchmarking
- A/B testing suggestions and tracking
- Team collaboration and content management
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from content_analyzer import ContentAnalyzer, ContentAnalysis
except ImportError:
    print("⚠️ Could not import content_analyzer. Running in demo mode.")
    
    # Create mock classes for demo
    class MockContentAnalysis:
        def __init__(self):
            self.content_id = "demo_001"
            self.platform = "blog"
            self.word_count = 1250
            self.flesch_score = 72.5
            self.readability_rating = "Fairly Easy"
            self.sentiment_label = "Positive"
            self.sentiment_polarity = 0.35
            self.predicted_engagement = 6.8
            self.performance_tier = "Good (Above Average)"
            self.optimization_score = 0.75
            self.improvement_areas = ["Social Media Optimization", "Emotional Engagement"]
            self.recommendations = [
                {
                    'category': 'Social Media Optimization',
                    'issue': 'Not enough hashtags (0)',
                    'recommendation': 'Add 3 relevant hashtags',
                    'priority': 'High',
                    'expected_impact': '+25-35% reach'
                }
            ]
    
    class MockContentAnalyzer:
        def analyze_content(self, content, title="", platform="blog"):
            return MockContentAnalysis()
        
        def get_platform_benchmark(self, platform):
            return {
                'average_engagement': 3.5,
                'good_engagement': 5.0,
                'excellent_engagement': 8.0
            }
    
    ContentAnalyzer = MockContentAnalyzer
    ContentAnalysis = MockContentAnalysis

class ContentOptimizationDashboard:
    """
    Main dashboard application for AI content optimization.
    
    Provides a comprehensive interface for content analysis,
    optimization recommendations, and performance tracking.
    """
    
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.setup_gui()
        
        # Application state
        self.current_analysis = None
        self.content_history = []
        self.saved_templates = []
        
        print("🚀 Content Optimization Dashboard initialized")
    
    def setup_gui(self):
        """Setup the main dashboard interface."""
        self.root = tk.Tk()
        self.root.title("AI Content Optimization Platform - Dashboard")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f8f9fa')
        
        # Configure styles
        self.setup_styles()
        
        # Create main layout
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
        # Initialize with welcome content
        self.show_welcome_content()
    
    def setup_styles(self):
        """Configure professional styling."""
        self.colors = {
            'primary': '#1a365d',
            'secondary': '#2d3748',
            'accent': '#3182ce',
            'success': '#38a169',
            'warning': '#d69e2e',
            'danger': '#e53e3e',
            'light': '#f7fafc',
            'white': '#ffffff',
            'gray_50': '#f9fafb',
            'gray_100': '#f7fafc',
            'gray_200': '#edf2f7',
            'gray_300': '#e2e8f0',
            'gray_500': '#a0aec0',
            'gray_600': '#718096',
            'gray_700': '#4a5568',
            'gray_800': '#2d3748'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Header.TLabel', 
                       background=self.colors['primary'], 
                       foreground='white',
                       font=('Arial', 12, 'bold'))
    
    def create_header(self):
        """Create application header with branding and navigation."""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo and title section
        title_section = tk.Frame(header_frame, bg=self.colors['primary'])
        title_section.pack(side='left', padx=20, pady=15)
        
        # Main title
        tk.Label(
            title_section,
            text="🚀 AI Content Optimization Platform",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg=self.colors['primary']
        ).pack(anchor='w')
        
        # Subtitle
        tk.Label(
            title_section,
            text="Intelligent Content Analysis & Performance Optimization",
            font=('Arial', 11),
            fg='#e2e8f0',
            bg=self.colors['primary']
        ).pack(anchor='w')
        
        # Action buttons section
        actions_section = tk.Frame(header_frame, bg=self.colors['primary'])
        actions_section.pack(side='right', padx=20, pady=15)
        
        tk.Button(
            actions_section,
            text="💾 Save Analysis",
            command=self.save_analysis,
            font=('Arial', 10),
            bg=self.colors['accent'],
            fg='white',
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        ).pack(side='right', padx=5)
        
        tk.Button(
            actions_section,
            text="📁 Load Content",
            command=self.load_content_file,
            font=('Arial', 10),
            bg=self.colors['gray_600'],
            fg='white',
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        ).pack(side='right', padx=5)
    
    def create_main_content(self):
        """Create the main content area with input and results sections."""
        # Create horizontal paned window for layout
        main_paned = ttk.PanedWindow(self.root, orient='horizontal')
        main_paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel: Content input and configuration
        self.create_input_panel(main_paned)
        
        # Right panel: Analysis results and recommendations
        self.create_results_panel(main_paned)
    
    def create_input_panel(self, parent):
        """Create the content input and configuration panel."""
        input_frame = tk.Frame(parent, bg=self.colors['white'], relief='ridge', bd=1)
        parent.add(input_frame, weight=1)
        
        # Panel header
        header = tk.Frame(input_frame, bg=self.colors['gray_100'], height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📝 Content Input & Configuration",
            font=('Arial', 14, 'bold'),
            bg=self.colors['gray_100'],
            fg=self.colors['gray_800']
        ).pack(side='left', padx=15, pady=15)
        
        # Content input section
        content_section = tk.Frame(input_frame, bg=self.colors['white'])
        content_section.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Platform selection
        platform_frame = tk.Frame(content_section, bg=self.colors['white'])
        platform_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            platform_frame,
            text="Target Platform:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white']
        ).pack(anchor='w')
        
        self.platform_var = tk.StringVar(value='blog')
        platform_combo = ttk.Combobox(
            platform_frame,
            textvariable=self.platform_var,
            values=['blog', 'social_media', 'email', 'video'],
            state='readonly',
            width=20,
            font=('Arial', 10)
        )
        platform_combo.pack(anchor='w', pady=(5, 0))
        platform_combo.bind('<<ComboboxSelected>>', self.on_platform_change)
        
        # Title input
        title_frame = tk.Frame(content_section, bg=self.colors['white'])
        title_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(
            title_frame,
            text="Title/Headline:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white']
        ).pack(anchor='w')
        
        self.title_entry = tk.Entry(
            title_frame,
            font=('Arial', 11),
            relief='solid',
            bd=1
        )
        self.title_entry.pack(fill='x', pady=(5, 0), ipady=5)
        self.title_entry.bind('<KeyRelease>', self.on_content_change)
        
        # Content input
        content_label_frame = tk.Frame(content_section, bg=self.colors['white'])
        content_label_frame.pack(fill='x', pady=(15, 0))
        
        tk.Label(
            content_label_frame,
            text="Content:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white']
        ).pack(side='left')
        
        tk.Label(
            content_label_frame,
            text="(Start typing for real-time analysis)",
            font=('Arial', 9),
            fg=self.colors['gray_500'],
            bg=self.colors['white']
        ).pack(side='left', padx=(10, 0))
        
        # Content text area
        self.content_text = scrolledtext.ScrolledText(
            content_section,
            wrap='word',
            font=('Arial', 11),
            relief='solid',
            bd=1,
            height=20
        )
        self.content_text.pack(fill='both', expand=True, pady=(5, 0))
        self.content_text.bind('<KeyRelease>', self.on_content_change)
        
        # Action buttons
        button_frame = tk.Frame(content_section, bg=self.colors['white'])
        button_frame.pack(fill='x', pady=(15, 0))
        
        self.analyze_button = tk.Button(
            button_frame,
            text="🔍 Analyze Content",
            command=self.analyze_content,
            font=('Arial', 12, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        self.analyze_button.pack(side='left')
        
        tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_content,
            font=('Arial', 11),
            bg=self.colors['gray_500'],
            fg='white',
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="📋 Paste Sample",
            command=self.paste_sample_content,
            font=('Arial', 11),
            bg=self.colors['gray_600'],
            fg='white',
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(10, 0))
    
    def create_results_panel(self, parent):
        """Create the analysis results and recommendations panel."""
        results_frame = tk.Frame(parent, bg=self.colors['white'], relief='ridge', bd=1)
        parent.add(results_frame, weight=1)
        
        # Panel header
        header = tk.Frame(results_frame, bg=self.colors['gray_100'], height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📊 Analysis Results & Recommendations",
            font=('Arial', 14, 'bold'),
            bg=self.colors['gray_100'],
            fg=self.colors['gray_800']
        ).pack(side='left', padx=15, pady=15)
        
        # Create notebook for tabbed results
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Overview tab
        self.overview_frame = tk.Frame(self.results_notebook, bg=self.colors['white'])
        self.results_notebook.add(self.overview_frame, text='📈 Overview')
        
        # Detailed Analysis tab
        self.analysis_frame = tk.Frame(self.results_notebook, bg=self.colors['white'])
        self.results_notebook.add(self.analysis_frame, text='🔍 Detailed Analysis')
        
        # Recommendations tab
        self.recommendations_frame = tk.Frame(self.results_notebook, bg=self.colors['white'])
        self.results_notebook.add(self.recommendations_frame, text='💡 Recommendations')
        
        # Benchmarks tab
        self.benchmarks_frame = tk.Frame(self.results_notebook, bg=self.colors['white'])
        self.results_notebook.add(self.benchmarks_frame, text='📊 Benchmarks')
    
    def create_status_bar(self):
        """Create status bar for application feedback."""
        self.status_bar = tk.Frame(self.root, bg=self.colors['gray_200'], height=30)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready for content analysis",
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_700']
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Word count indicator
        self.word_count_label = tk.Label(
            self.status_bar,
            text="Words: 0",
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_700']
        )
        self.word_count_label.pack(side='right', padx=10, pady=5)
    
    def show_welcome_content(self):
        """Display welcome content in the results area."""
        welcome_frame = tk.Frame(self.overview_frame, bg=self.colors['white'])
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        tk.Label(
            welcome_frame,
            text="🚀 Welcome to AI Content Optimization",
            font=('Arial', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=(0, 10))
        
        tk.Label(
            welcome_frame,
            text="Enter your content and get AI-powered optimization recommendations",
            font=('Arial', 12),
            bg=self.colors['white'],
            fg=self.colors['gray_600']
        ).pack(pady=(0, 20))
        
        # Feature highlights
        features_frame = tk.Frame(welcome_frame, bg=self.colors['white'])
        features_frame.pack(fill='x', pady=10)
        
        features = [
            "📝 Multi-platform content optimization",
            "🎯 AI-powered performance prediction", 
            "📊 Comprehensive readability analysis",
            "💡 Actionable improvement recommendations",
            "📈 Benchmark comparison and scoring"
        ]
        
        for feature in features:
            tk.Label(
                features_frame,
                text=feature,
                font=('Arial', 11),
                bg=self.colors['white'],
                fg=self.colors['gray_700']
            ).pack(anchor='w', pady=2)
    
    def on_platform_change(self, event=None):
        """Handle platform selection change."""
        platform = self.platform_var.get()
        self.update_status(f"Platform changed to: {platform}")
        
        # Auto-analyze if content exists
        if self.content_text.get('1.0', tk.END).strip():
            self.analyze_content()
    
    def on_content_change(self, event=None):
        """Handle content changes for real-time feedback."""
        content = self.content_text.get('1.0', tk.END).strip()
        word_count = len(content.split()) if content else 0
        
        self.word_count_label.config(text=f"Words: {word_count}")
        
        # Update status based on content length
        if word_count == 0:
            self.update_status("Ready for content analysis")
        elif word_count < 50:
            self.update_status("Add more content for better analysis")
        else:
            self.update_status(f"Content ready for analysis ({word_count} words)")
    
    def analyze_content(self):
        """Perform content analysis and display results."""
        content = self.content_text.get('1.0', tk.END).strip()
        title = self.title_entry.get().strip()
        platform = self.platform_var.get()
        
        if not content:
            messagebox.showwarning("Warning", "Please enter content to analyze.")
            return
        
        # Update UI state
        self.analyze_button.config(text="🔄 Analyzing...", state='disabled')
        self.update_status("Analyzing content...")
        
        # Perform analysis in background thread
        def analysis_thread():
            try:
                analysis = self.analyzer.analyze_content(content, title, platform)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.display_analysis_results(analysis))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_analysis_error(str(e)))
        
        thread = threading.Thread(target=analysis_thread)
        thread.daemon = True
        thread.start()
    
    def display_analysis_results(self, analysis):
        """Display comprehensive analysis results."""
        try:
            self.current_analysis = analysis
            
            # Add to history
            self.content_history.append({
                'timestamp': datetime.now(),
                'analysis': analysis,
                'content_preview': analysis.content[:100] + "..." if len(analysis.content) > 100 else analysis.content
            })
            
            # Update all result tabs
            self.update_overview_tab(analysis)
            self.update_analysis_tab(analysis)
            self.update_recommendations_tab(analysis)
            self.update_benchmarks_tab(analysis)
            
            # Update status
            self.update_status("Analysis complete - Review results and recommendations")
            
        except Exception as e:
            self.handle_analysis_error(f"Error displaying results: {e}")
        finally:
            # Reset analyze button
            self.analyze_button.config(text="🔍 Analyze Content", state='normal')
    
    def update_overview_tab(self, analysis):
        """Update the overview tab with key metrics."""
        # Clear existing content
        for widget in self.overview_frame.winfo_children():
            widget.destroy()
        
        # Main metrics grid
        metrics_frame = tk.Frame(self.overview_frame, bg=self.colors['white'])
        metrics_frame.pack(fill='x', padx=20, pady=20)
        
        # Performance score (large display)
        score_frame = tk.Frame(metrics_frame, bg=self.colors['gray_50'], relief='ridge', bd=1)
        score_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        tk.Label(
            score_frame,
            text="🎯 Predicted Engagement",
            font=('Arial', 14, 'bold'),
            bg=self.colors['gray_50']
        ).pack(pady=(15, 5))
        
        engagement_color = self.colors['success'] if analysis.predicted_engagement > 5.0 else self.colors['warning'] if analysis.predicted_engagement > 3.0 else self.colors['danger']
        tk.Label(
            score_frame,
            text=f"{analysis.predicted_engagement}%",
            font=('Arial', 24, 'bold'),
            fg=engagement_color,
            bg=self.colors['gray_50']
        ).pack()
        
        tk.Label(
            score_frame,
            text=analysis.performance_tier,
            font=('Arial', 12),
            fg=self.colors['gray_600'],
            bg=self.colors['gray_50']
        ).pack(pady=(0, 15))
        
        # Key metrics cards
        metrics = [
            ("📝 Word Count", str(analysis.word_count), "words"),
            ("📖 Readability", analysis.readability_rating, f"Flesch: {analysis.flesch_score}"),
            ("😊 Sentiment", analysis.sentiment_label, f"Score: {analysis.sentiment_polarity:+.2f}"),
            ("⚡ Optimization", f"{analysis.optimization_score:.0%}", f"{len(analysis.improvement_areas)} areas to improve")
        ]
        
        for i, (title, value, subtitle) in enumerate(metrics):
            row = (i // 2) + 1
            col = i % 2
            
            card = tk.Frame(metrics_frame, bg=self.colors['gray_50'], relief='ridge', bd=1)
            card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            tk.Label(card, text=title, font=('Arial', 11, 'bold'), bg=self.colors['gray_50']).pack(pady=(10, 5))
            tk.Label(card, text=value, font=('Arial', 14, 'bold'), bg=self.colors['gray_50'], fg=self.colors['accent']).pack()
            tk.Label(card, text=subtitle, font=('Arial', 9), bg=self.colors['gray_50'], fg=self.colors['gray_600']).pack(pady=(0, 10))
        
        # Configure grid weights
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
    
    def update_analysis_tab(self, analysis):
        """Update the detailed analysis tab."""
        # Clear existing content
        for widget in self.analysis_frame.winfo_children():
            widget.destroy()
        
        # Scrollable frame for detailed analysis
        canvas = tk.Canvas(self.analysis_frame, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(self.analysis_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Analysis sections
        sections = [
            ("📝 Content Structure", [
                f"Word Count: {analysis.word_count}",
                f"Sentence Count: {analysis.sentence_count}",
                f"Paragraph Count: {analysis.paragraph_count}",
                f"Avg Paragraph Length: {analysis.paragraph_length_avg} words",
                f"Avg Sentence Length: {analysis.sentence_length_avg} words"
            ]),
            ("📖 Readability Analysis", [
                f"Flesch Reading Ease: {analysis.flesch_score}",
                f"Grade Level: {analysis.grade_level}",
                f"Readability Rating: {analysis.readability_rating}",
                f"Target Audience: General readers"
            ]),
            ("😊 Sentiment & Tone", [
                f"Sentiment: {analysis.sentiment_label}",
                f"Polarity Score: {analysis.sentiment_polarity:+.3f}",
                f"Subjectivity: {analysis.sentiment_subjectivity:.3f}",
                f"Emotional Tone: {analysis.emotional_tone}"
            ]),
            ("🎯 Platform Optimization", [
                f"Target Platform: {analysis.platform.title()}",
                f"Optimization Score: {analysis.optimization_score:.0%}",
                f"Headline Quality: {analysis.headline_quality:.0%}",
                f"Areas for Improvement: {len(analysis.improvement_areas)}"
            ])
        ]
        
        for section_title, items in sections:
            # Section header
            section_frame = tk.Frame(scrollable_frame, bg=self.colors['white'])
            section_frame.pack(fill='x', padx=20, pady=(15, 5))
            
            tk.Label(
                section_frame,
                text=section_title,
                font=('Arial', 13, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['primary']
            ).pack(anchor='w')
            
            # Section content
            content_frame = tk.Frame(scrollable_frame, bg=self.colors['gray_50'], relief='ridge', bd=1)
            content_frame.pack(fill='x', padx=20, pady=(0, 10))
            
            for item in items:
                tk.Label(
                    content_frame,
                    text=f"• {item}",
                    font=('Arial', 10),
                    bg=self.colors['gray_50'],
                    fg=self.colors['gray_700']
                ).pack(anchor='w', padx=15, pady=2)
    
    def update_recommendations_tab(self, analysis):
        """Update the recommendations tab."""
        # Clear existing content
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()
        
        if not analysis.recommendations:
            tk.Label(
                self.recommendations_frame,
                text="🎉 Great job! Your content is well-optimized.",
                font=('Arial', 14, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['success']
            ).pack(expand=True)
            return
        
        # Recommendations list
        rec_frame = tk.Frame(self.recommendations_frame, bg=self.colors['white'])
        rec_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            rec_frame,
            text=f"💡 {len(analysis.recommendations)} Optimization Recommendations",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(anchor='w', pady=(0, 15))
        
        for i, rec in enumerate(analysis.recommendations, 1):
            # Recommendation card
            card = tk.Frame(rec_frame, bg=self.colors['gray_50'], relief='ridge', bd=1)
            card.pack(fill='x', pady=5)
            
            # Header with priority
            header = tk.Frame(card, bg=self.colors['gray_50'])
            header.pack(fill='x', padx=15, pady=(10, 5))
            
            tk.Label(
                header,
                text=f"{i}. {rec['category']}",
                font=('Arial', 12, 'bold'),
                bg=self.colors['gray_50'],
                fg=self.colors['primary']
            ).pack(side='left')
            
            priority_color = self.colors['danger'] if rec['priority'] == 'High' else self.colors['warning'] if rec['priority'] == 'Medium' else self.colors['success']
            tk.Label(
                header,
                text=rec['priority'],
                font=('Arial', 9, 'bold'),
                bg=priority_color,
                fg='white',
                padx=8,
                pady=2
            ).pack(side='right')
            
            # Issue and recommendation
            tk.Label(
                card,
                text=f"Issue: {rec['issue']}",
                font=('Arial', 10),
                bg=self.colors['gray_50'],
                fg=self.colors['gray_700'],
                wraplength=600,
                justify='left'
            ).pack(anchor='w', padx=15)
            
            tk.Label(
                card,
                text=f"💡 {rec['recommendation']}",
                font=('Arial', 10, 'bold'),
                bg=self.colors['gray_50'],
                fg=self.colors['gray_800'],
                wraplength=600,
                justify='left'
            ).pack(anchor='w', padx=15, pady=(5, 0))
            
            tk.Label(
                card,
                text=f"Expected Impact: {rec['expected_impact']}",
                font=('Arial', 9),
                bg=self.colors['gray_50'],
                fg=self.colors['success'],
                wraplength=600,
                justify='left'
            ).pack(anchor='w', padx=15, pady=(5, 10))
    
    def update_benchmarks_tab(self, analysis):
        """Update the benchmarks comparison tab."""
        # Clear existing content
        for widget in self.benchmarks_frame.winfo_children():
            widget.destroy()
        
        # Get platform benchmarks
        benchmarks = self.analyzer.get_platform_benchmark(analysis.platform)
        
        bench_frame = tk.Frame(self.benchmarks_frame, bg=self.colors['white'])
        bench_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            bench_frame,
            text=f"📊 {analysis.platform.title()} Performance Benchmarks",
            font=('Arial', 14, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(anchor='w', pady=(0, 15))
        
        # Comparison data
        comparisons = [
            ("Your Content", analysis.predicted_engagement, self.colors['accent']),
            ("Average Content", benchmarks['average_engagement'], self.colors['gray_500']),
            ("Good Content", benchmarks['good_engagement'], self.colors['warning']),
            ("Excellent Content", benchmarks['excellent_engagement'], self.colors['success'])
        ]
        
        for label, value, color in comparisons:
            comp_frame = tk.Frame(bench_frame, bg=self.colors['gray_50'], relief='ridge', bd=1)
            comp_frame.pack(fill='x', pady=2)
            
            tk.Label(
                comp_frame,
                text=label,
                font=('Arial', 11, 'bold'),
                bg=self.colors['gray_50']
            ).pack(side='left', padx=15, pady=10)
            
            tk.Label(
                comp_frame,
                text=f"{value}%",
                font=('Arial', 11, 'bold'),
                fg=color,
                bg=self.colors['gray_50']
            ).pack(side='right', padx=15, pady=10)
    
    def paste_sample_content(self):
        """Paste sample content for demonstration."""
        sample_content = """
Artificial intelligence is transforming the way we create and optimize content. In this comprehensive guide, we'll explore how AI-powered tools can revolutionize your content strategy and boost engagement rates significantly.

Content optimization has never been more important. With millions of pieces of content published daily, standing out requires more than just good writing. It demands data-driven insights, strategic planning, and continuous improvement.

Our AI content optimization platform analyzes your content across multiple dimensions: readability, sentiment, structure, and engagement potential. Using advanced machine learning algorithms, we predict how your audience will respond before you hit publish.

Key benefits include:
- 40% average increase in engagement rates
- Real-time optimization recommendations
- Multi-platform content adaptation
- Performance prediction with 90% accuracy
- Comprehensive analytics and reporting

Ready to transform your content strategy? Start optimizing your content today and see the difference AI can make for your brand's success.
        """.strip()
        
        sample_title = "How AI Content Optimization Can Boost Your Engagement by 40%"
        
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert('1.0', sample_content)
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, sample_title)
        
        self.update_status("Sample content loaded - Click Analyze to see results")
    
    def clear_content(self):
        """Clear all content and reset the interface."""
        self.content_text.delete('1.0', tk.END)
        self.title_entry.delete(0, tk.END)
        self.current_analysis = None
        
        # Clear results tabs
        for frame in [self.overview_frame, self.analysis_frame, self.recommendations_frame, self.benchmarks_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        
        self.show_welcome_content()
        self.update_status("Content cleared - Ready for new analysis")
    
    def save_analysis(self):
        """Save current analysis results."""
        if not self.current_analysis:
            messagebox.showwarning("Warning", "No analysis to save. Please analyze content first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Analysis Results"
        )
        
        if filename:
            try:
                # Create saveable analysis data
                analysis_data = {
                    'timestamp': datetime.now().isoformat(),
                    'platform': self.current_analysis.platform,
                    'content_preview': self.current_analysis.content[:200] + "...",
                    'metrics': {
                        'word_count': self.current_analysis.word_count,
                        'predicted_engagement': self.current_analysis.predicted_engagement,
                        'readability_score': self.current_analysis.flesch_score,
                        'sentiment_polarity': self.current_analysis.sentiment_polarity,
                        'optimization_score': self.current_analysis.optimization_score
                    },
                    'recommendations': self.current_analysis.recommendations
                }
                
                with open(filename, 'w') as f:
                    json.dump(analysis_data, f, indent=2)
                
                messagebox.showinfo("Success", f"Analysis saved to {filename}")
                self.update_status(f"Analysis saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save analysis: {str(e)}")
    
    def load_content_file(self):
        """Load content from a file."""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Load Content File"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.content_text.delete('1.0', tk.END)
                self.content_text.insert('1.0', content)
                
                self.update_status(f"Content loaded from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def handle_analysis_error(self, error_message: str):
        """Handle analysis errors."""
        self.update_status(f"Analysis error: {error_message}")
        messagebox.showerror("Analysis Error", f"An error occurred during analysis:\n{error_message}")
        self.analyze_button.config(text="🔍 Analyze Content", state='normal')
    
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def run(self):
        """Start the dashboard application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

# Example usage and demonstration
if __name__ == "__main__":
    print("🚀 AI Content Optimization Dashboard")
    print("=" * 50)
    print("Launching comprehensive content optimization platform...")
    print("Features:")
    print("- Real-time content analysis and optimization")
    print("- Multi-platform content recommendations")
    print("- Performance prediction and benchmarking")
    print("- Professional dashboard interface")
    print("- Save and load content functionality")
    print("=" * 50)
    
    # Launch the dashboard application
    app = ContentOptimizationDashboard()
    app.run()
