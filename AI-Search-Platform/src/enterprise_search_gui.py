"""
Enterprise Search GUI - Professional AI Search Interface
=======================================================

Enterprise-grade search interface built on the Advanced RAG Engine,
designed for professional users, teams, and enterprise environments.

Key Features:
- Modern, intuitive search interface with real-time results
- Source attribution and confidence indicators
- Search history and saved queries
- Advanced filtering and result organization
- Multi-user support with role-based access
- Integration with enterprise systems
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
from dataclasses import asdict
import webbrowser
from urllib.parse import quote

# Import our RAG engine
from rag_engine import AdvancedRAGEngine, RAGResponse, SearchResult

class EnterpriseSearchGUI:
    """
    Professional search interface for enterprise AI search platform.
    
    Provides a comprehensive user experience for AI-powered search with:
    - Real-time search with instant results
    - Professional UI with confidence indicators
    - Search history and query management
    - Source attribution and fact-checking status
    - Advanced filtering and result organization
    """
    
    def __init__(self):
        self.rag_engine = AdvancedRAGEngine()
        
        # Application state (initialize before GUI setup)
        self.current_user = "enterprise_user"
        self.search_history = []
        self.saved_queries = []
        self.current_results = None
        
        self.setup_gui()
        
        # Load sample data
        self.load_sample_knowledge_base()
        
        print("🚀 Enterprise Search GUI initialized")
    
    def setup_gui(self):
        """Setup the professional enterprise search interface."""
        self.root = tk.Tk()
        self.root.title("Enterprise AI Search Platform")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')
        
        # Configure styles
        self.setup_styles()
        
        # Create main layout
        self.create_header()
        self.create_search_section()
        self.create_main_content_area()
        self.create_status_bar()
        
        # Initialize with welcome message
        self.show_welcome_message()
    
    def setup_styles(self):
        """Configure professional styling."""
        self.colors = {
            'primary': '#2c5282',
            'secondary': '#4a5568',
            'success': '#38a169',
            'warning': '#d69e2e',
            'danger': '#e53e3e',
            'light': '#f7fafc',
            'white': '#ffffff',
            'gray_100': '#f7fafc',
            'gray_200': '#edf2f7',
            'gray_300': '#e2e8f0',
            'gray_600': '#718096',
            'gray_800': '#2d3748'
        }
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Header.TFrame', background=self.colors['primary'])
        style.configure('Search.TFrame', background=self.colors['white'])
        style.configure('Results.TFrame', background=self.colors['gray_100'])
    
    def create_header(self):
        """Create application header with branding and navigation."""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(side='left', padx=20, pady=15)
        
        tk.Label(
            title_frame,
            text="🔍 Enterprise AI Search",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg=self.colors['primary']
        ).pack(side='left')
        
        tk.Label(
            title_frame,
            text="Intelligent Information Discovery",
            font=('Arial', 10),
            fg='#e2e8f0',
            bg=self.colors['primary']
        ).pack(side='left', padx=(10, 0))
        
        # User info and actions
        user_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        user_frame.pack(side='right', padx=20, pady=15)
        
        tk.Label(
            user_frame,
            text=f"Welcome, {self.current_user}",
            font=('Arial', 10),
            fg='white',
            bg=self.colors['primary']
        ).pack(side='right')
    
    def create_search_section(self):
        """Create the main search input section."""
        search_container = tk.Frame(self.root, bg=self.colors['white'], height=120)
        search_container.pack(fill='x', padx=20, pady=10)
        search_container.pack_propagate(False)
        
        # Search input frame
        search_frame = tk.Frame(search_container, bg=self.colors['white'])
        search_frame.pack(fill='x', pady=20)
        
        # Search label
        tk.Label(
            search_frame,
            text="Ask anything - I'll search across your enterprise knowledge base",
            font=('Arial', 12),
            fg=self.colors['gray_600'],
            bg=self.colors['white']
        ).pack(anchor='w')
        
        # Search input container
        input_container = tk.Frame(search_frame, bg=self.colors['white'])
        input_container.pack(fill='x', pady=(10, 0))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            input_container,
            textvariable=self.search_var,
            font=('Arial', 14),
            relief='solid',
            bd=1
        )
        self.search_entry.pack(side='left', fill='x', expand=True, ipady=8)
        self.search_entry.bind('<Return>', self.on_search)
        self.search_entry.bind('<KeyRelease>', self.on_search_input_change)
        
        # Search button
        self.search_button = tk.Button(
            input_container,
            text="🔍 Search",
            command=self.on_search,
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        self.search_button.pack(side='right', padx=(10, 0))
        
        # Quick actions
        actions_frame = tk.Frame(search_frame, bg=self.colors['white'])
        actions_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(
            actions_frame,
            text="📖 Search History",
            command=self.show_search_history,
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_800'],
            padx=10,
            pady=4,
            relief='flat',
            cursor='hand2'
        ).pack(side='left')
        
        tk.Button(
            actions_frame,
            text="⭐ Saved Queries",
            command=self.show_saved_queries,
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_800'],
            padx=10,
            pady=4,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(10, 0))
        
        tk.Button(
            actions_frame,
            text="⚙️ Advanced Search",
            command=self.show_advanced_search,
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_800'],
            padx=10,
            pady=4,
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=(10, 0))
    
    def create_main_content_area(self):
        """Create the main content area for results and information."""
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Results tab
        self.results_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.results_frame, text='🔍 Search Results')
        
        # Analytics tab
        self.analytics_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.analytics_frame, text='📊 Search Analytics')
        
        # History tab
        self.history_frame = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.history_frame, text='📖 Search History')
        
        # Setup individual tabs
        self.setup_results_tab()
        self.setup_analytics_tab()
        self.setup_history_tab()
    
    def setup_results_tab(self):
        """Setup the search results display tab."""
        # Results container with scrollbar
        results_container = tk.Frame(self.results_frame, bg=self.colors['white'])
        results_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Scrollable results area
        canvas = tk.Canvas(results_container, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(results_container, orient='vertical', command=canvas.yview)
        
        self.scrollable_results = tk.Frame(canvas, bg=self.colors['white'])
        self.scrollable_results.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_results, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind mouse wheel to canvas
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def setup_analytics_tab(self):
        """Setup the search analytics tab."""
        analytics_container = tk.Frame(self.analytics_frame, bg=self.colors['white'])
        analytics_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            analytics_container,
            text="📊 Search Performance Analytics",
            font=('Arial', 16, 'bold'),
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 20))
        
        # Metrics grid
        metrics_frame = tk.Frame(analytics_container, bg=self.colors['white'])
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        self.metrics_labels = {}
        metrics = [
            ('Total Queries', 'queries_processed'),
            ('Avg Response Time', 'avg_response_time'),
            ('Avg Confidence', 'avg_confidence'),
            ('Cache Hit Rate', 'cache_hit_rate')
        ]
        
        for i, (label, key) in enumerate(metrics):
            row = i // 2
            col = i % 2
            
            metric_card = tk.Frame(metrics_frame, bg=self.colors['gray_100'], relief='solid', bd=1)
            metric_card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            tk.Label(
                metric_card,
                text=label,
                font=('Arial', 10),
                bg=self.colors['gray_100']
            ).pack(pady=(10, 0))
            
            value_label = tk.Label(
                metric_card,
                text="0",
                font=('Arial', 16, 'bold'),
                bg=self.colors['gray_100'],
                fg=self.colors['primary']
            )
            value_label.pack(pady=(0, 10))
            
            self.metrics_labels[key] = value_label
        
        # Configure grid weights
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
    
    def setup_history_tab(self):
        """Setup the search history tab."""
        history_container = tk.Frame(self.history_frame, bg=self.colors['white'])
        history_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            history_container,
            text="📖 Recent Search History",
            font=('Arial', 16, 'bold'),
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 20))
        
        # History list
        self.history_listbox = tk.Listbox(
            history_container,
            font=('Arial', 10),
            height=15,
            relief='solid',
            bd=1
        )
        self.history_listbox.pack(fill='both', expand=True)
        self.history_listbox.bind('<Double-Button-1>', self.on_history_select)
    
    def create_status_bar(self):
        """Create status bar for application feedback."""
        self.status_bar = tk.Frame(self.root, bg=self.colors['gray_200'], height=30)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready for search",
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_600']
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Performance indicator
        self.performance_label = tk.Label(
            self.status_bar,
            text="",
            font=('Arial', 9),
            bg=self.colors['gray_200'],
            fg=self.colors['gray_600']
        )
        self.performance_label.pack(side='right', padx=10, pady=5)
    
    def show_welcome_message(self):
        """Display welcome message in results area."""
        welcome_frame = tk.Frame(self.scrollable_results, bg=self.colors['white'])
        welcome_frame.pack(fill='x', pady=20)
        
        tk.Label(
            welcome_frame,
            text="🔍 Welcome to Enterprise AI Search",
            font=('Arial', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=(0, 10))
        
        tk.Label(
            welcome_frame,
            text="Ask any question and I'll search across your enterprise knowledge base using advanced AI.",
            font=('Arial', 12),
            bg=self.colors['white'],
            fg=self.colors['gray_600']
        ).pack(pady=(0, 20))
        
        # Sample queries
        samples_frame = tk.Frame(welcome_frame, bg=self.colors['white'])
        samples_frame.pack(fill='x')
        
        tk.Label(
            samples_frame,
            text="Try these sample queries:",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white']
        ).pack(anchor='w', pady=(0, 10))
        
        sample_queries = [
            "What is machine learning and how does it work?",
            "How can I implement natural language processing?",
            "What are the benefits of vector databases?",
            "Compare different AI search technologies"
        ]
        
        for query in sample_queries:
            query_button = tk.Button(
                samples_frame,
                text=f"💡 {query}",
                command=lambda q=query: self.run_sample_query(q),
                font=('Arial', 10),
                bg=self.colors['gray_100'],
                fg=self.colors['gray_800'],
                relief='flat',
                cursor='hand2',
                anchor='w'
            )
            query_button.pack(fill='x', pady=2)
    
    def run_sample_query(self, query: str):
        """Run a sample query."""
        self.search_var.set(query)
        self.on_search()
    
    def on_search_input_change(self, event=None):
        """Handle search input changes for real-time suggestions."""
        query = self.search_var.get()
        
        if len(query) > 3:
            self.update_status(f"Ready to search: '{query[:30]}...'")
        else:
            self.update_status("Ready for search")
    
    def on_search(self, event=None):
        """Handle search request."""
        query = self.search_var.get().strip()
        
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
        
        # Update UI state
        self.search_button.config(text="🔄 Searching...", state='disabled')
        self.update_status("Searching...")
        
        # Perform search in background thread
        def search_thread():
            try:
                # Create new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Perform search
                response = loop.run_until_complete(
                    self.rag_engine.search(query, user_id=self.current_user)
                )
                
                # Update UI in main thread
                self.root.after(0, lambda: self.handle_search_response(query, response))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_search_error(str(e)))
            finally:
                loop.close()
        
        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()
    
    def handle_search_response(self, query: str, response: RAGResponse):
        """Handle successful search response."""
        try:
            # Update current results
            self.current_results = response
            
            # Add to search history
            self.search_history.append({
                'query': query,
                'timestamp': datetime.now(),
                'results_count': len(response.source_results),
                'confidence': response.confidence_score
            })
            
            # Display results
            self.display_search_results(query, response)
            
            # Update analytics
            self.update_analytics()
            
            # Update history
            self.update_history_display()
            
            # Update status
            processing_time = response.processing_time_ms
            self.update_status(f"Search completed in {processing_time:.1f}ms")
            self.performance_label.config(text=f"⚡ {processing_time:.1f}ms | 🎯 {response.confidence_score:.2f}")
            
        except Exception as e:
            self.handle_search_error(f"Error displaying results: {e}")
        finally:
            # Reset search button
            self.search_button.config(text="🔍 Search", state='normal')
    
    def handle_search_error(self, error_message: str):
        """Handle search errors."""
        self.update_status(f"Search error: {error_message}")
        messagebox.showerror("Search Error", f"An error occurred during search:\n{error_message}")
        self.search_button.config(text="🔍 Search", state='normal')
    
    def display_search_results(self, query: str, response: RAGResponse):
        """Display search results in the UI."""
        # Clear existing results
        for widget in self.scrollable_results.winfo_children():
            widget.destroy()
        
        # Query and response summary
        header_frame = tk.Frame(self.scrollable_results, bg=self.colors['white'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            header_frame,
            text=f"🔍 Search Results for: \"{query}\"",
            font=('Arial', 16, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(anchor='w')
        
        # Response metadata
        metadata_frame = tk.Frame(header_frame, bg=self.colors['white'])
        metadata_frame.pack(fill='x', pady=(10, 0))
        
        metadata_info = [
            f"🎯 Intent: {response.query_intent}",
            f"📊 Confidence: {response.confidence_score:.2f}",
            f"⚡ Response time: {response.processing_time_ms:.1f}ms",
            f"📚 Sources: {len(response.source_results)}"
        ]
        
        for info in metadata_info:
            tk.Label(
                metadata_frame,
                text=info,
                font=('Arial', 10),
                bg=self.colors['white'],
                fg=self.colors['gray_600']
            ).pack(side='left', padx=(0, 20))
        
        # Synthesized answer
        if response.synthesized_answer:
            answer_frame = tk.Frame(self.scrollable_results, bg=self.colors['gray_100'], relief='solid', bd=1)
            answer_frame.pack(fill='x', pady=(0, 20))
            
            tk.Label(
                answer_frame,
                text="🤖 AI-Generated Answer",
                font=('Arial', 12, 'bold'),
                bg=self.colors['gray_100'],
                fg=self.colors['primary']
            ).pack(anchor='w', padx=15, pady=(15, 5))
            
            # Answer text
            answer_text = scrolledtext.ScrolledText(
                answer_frame,
                height=6,
                wrap='word',
                font=('Arial', 11),
                relief='flat',
                bg=self.colors['gray_100']
            )
            answer_text.pack(fill='x', padx=15, pady=(0, 10))
            answer_text.insert('1.0', response.synthesized_answer)
            answer_text.config(state='disabled')
            
            # Fact-check status
            if response.fact_check_status != "disabled":
                fact_check_color = self.colors['success'] if response.fact_check_status == 'verified' else self.colors['warning']
                tk.Label(
                    answer_frame,
                    text=f"✓ Fact-check: {response.fact_check_status}",
                    font=('Arial', 9),
                    bg=self.colors['gray_100'],
                    fg=fact_check_color
                ).pack(anchor='w', padx=15, pady=(0, 15))
        
        # Source results
        if response.source_results:
            sources_label = tk.Label(
                self.scrollable_results,
                text=f"📚 Source Documents ({len(response.source_results)} results)",
                font=('Arial', 14, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['primary']
            )
            sources_label.pack(anchor='w', pady=(0, 10))
            
            for i, result in enumerate(response.source_results[:5], 1):  # Show top 5
                self.create_result_card(result, i)
        
        # Follow-up questions
        if response.follow_up_questions:
            followup_frame = tk.Frame(self.scrollable_results, bg=self.colors['white'])
            followup_frame.pack(fill='x', pady=(20, 0))
            
            tk.Label(
                followup_frame,
                text="💡 Suggested Follow-up Questions",
                font=('Arial', 12, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['primary']
            ).pack(anchor='w', pady=(0, 10))
            
            for question in response.follow_up_questions:
                question_button = tk.Button(
                    followup_frame,
                    text=f"❓ {question}",
                    command=lambda q=question: self.run_sample_query(q),
                    font=('Arial', 10),
                    bg=self.colors['gray_100'],
                    fg=self.colors['gray_800'],
                    relief='flat',
                    cursor='hand2',
                    anchor='w'
                )
                question_button.pack(fill='x', pady=2)
    
    def create_result_card(self, result: SearchResult, index: int):
        """Create a result card for a search result."""
        card_frame = tk.Frame(self.scrollable_results, bg=self.colors['white'], relief='solid', bd=1)
        card_frame.pack(fill='x', pady=5)
        
        # Header with source and relevance
        header_frame = tk.Frame(card_frame, bg=self.colors['white'])
        header_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        tk.Label(
            header_frame,
            text=f"{index}. {result.source}",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(side='left')
        
        # Confidence badge
        confidence_color = self.colors['success'] if result.confidence_score > 0.8 else self.colors['warning'] if result.confidence_score > 0.6 else self.colors['danger']
        confidence_badge = tk.Label(
            header_frame,
            text=f"🎯 {result.confidence_score:.2f}",
            font=('Arial', 9, 'bold'),
            bg=confidence_color,
            fg='white',
            padx=8,
            pady=2
        )
        confidence_badge.pack(side='right')
        
        # Content preview
        content_frame = tk.Frame(card_frame, bg=self.colors['white'])
        content_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        content_text = result.content[:300] + "..." if len(result.content) > 300 else result.content
        tk.Label(
            content_frame,
            text=content_text,
            font=('Arial', 10),
            bg=self.colors['white'],
            fg=self.colors['gray_800'],
            wraplength=800,
            justify='left'
        ).pack(anchor='w')
        
        # Metadata
        if result.metadata:
            metadata_frame = tk.Frame(card_frame, bg=self.colors['gray_100'])
            metadata_frame.pack(fill='x', padx=15, pady=(0, 15))
            
            metadata_text = " | ".join([
                f"Section: {result.metadata.get('section', 'N/A')}",
                f"Type: {result.metadata.get('source_type', 'N/A')}",
                f"Updated: {result.metadata.get('last_updated', 'N/A')}"
            ])
            
            tk.Label(
                metadata_frame,
                text=metadata_text,
                font=('Arial', 8),
                bg=self.colors['gray_100'],
                fg=self.colors['gray_600']
            ).pack(anchor='w', padx=10, pady=5)
    
    def update_analytics(self):
        """Update analytics display."""
        metrics = self.rag_engine.get_performance_metrics()
        
        for key, label in self.metrics_labels.items():
            value = metrics.get(key, 0)
            
            if key == 'avg_response_time':
                display_value = f"{value:.1f}ms"
            elif key == 'avg_confidence':
                display_value = f"{value:.3f}"
            else:
                display_value = str(int(value))
            
            label.config(text=display_value)
    
    def update_history_display(self):
        """Update search history display."""
        self.history_listbox.delete(0, tk.END)
        
        for entry in reversed(self.search_history[-20:]):  # Show last 20
            timestamp = entry['timestamp'].strftime('%H:%M:%S')
            display_text = f"[{timestamp}] {entry['query']} (Confidence: {entry['confidence']:.2f})"
            self.history_listbox.insert(0, display_text)
    
    def on_history_select(self, event):
        """Handle selection from search history."""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            history_entry = self.search_history[-(index+1)]  # Reverse index
            self.search_var.set(history_entry['query'])
    
    def show_search_history(self):
        """Show search history in a popup."""
        self.notebook.select(self.history_frame)
    
    def show_saved_queries(self):
        """Show saved queries dialog."""
        messagebox.showinfo("Saved Queries", "Saved queries feature would be implemented here.")
    
    def show_advanced_search(self):
        """Show advanced search options."""
        messagebox.showinfo("Advanced Search", "Advanced search filters would be implemented here.")
    
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def load_sample_knowledge_base(self):
        """Load sample documents into the knowledge base."""
        sample_docs = [
            {
                'content': 'Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. AI systems can perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation. The field encompasses various subfields including machine learning, natural language processing, computer vision, and robotics.',
                'source': 'AI_Introduction.pdf',
                'source_type': 'document',
                'section': 'Fundamentals',
                'last_updated': '2024-01-15',
                'chunk_id': 'ai_intro_001'
            },
            {
                'content': 'Machine Learning (ML) is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. ML algorithms build mathematical models based on training data to make predictions or decisions. Common types include supervised learning (using labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through interaction with an environment).',
                'source': 'ML_Fundamentals.pdf',
                'source_type': 'document',
                'section': 'Machine Learning',
                'last_updated': '2024-01-20',
                'chunk_id': 'ml_fund_001'
            },
            {
                'content': 'Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language in a valuable way. NLP combines computational linguistics with machine learning and deep learning models to process and analyze large amounts of natural language data. Applications include sentiment analysis, machine translation, chatbots, and text summarization.',
                'source': 'NLP_Guide.pdf',
                'source_type': 'document',
                'section': 'Natural Language Processing',
                'last_updated': '2024-01-25',
                'chunk_id': 'nlp_guide_001'
            },
            {
                'content': 'Vector databases are specialized database systems designed to store and query high-dimensional vector data efficiently. They are crucial for AI applications like semantic search, recommendation systems, and similarity matching. Vector databases use advanced indexing techniques like HNSW (Hierarchical Navigable Small World) and FAISS to enable fast approximate nearest neighbor searches across millions or billions of vectors.',
                'source': 'Vector_DB_Technology.pdf',
                'source_type': 'document',
                'section': 'Database Technology',
                'last_updated': '2024-01-30',
                'chunk_id': 'vector_db_001'
            },
            {
                'content': 'RAG (Retrieval-Augmented Generation) is an AI framework that combines the strengths of retrieval-based and generative models. RAG systems first retrieve relevant information from a knowledge base or document collection, then use this retrieved context to generate more accurate and contextually relevant responses. This approach helps reduce hallucinations and provides more factual, up-to-date information in AI-generated content.',
                'source': 'RAG_Architecture.pdf',
                'source_type': 'document',
                'section': 'AI Architecture',
                'last_updated': '2024-02-01',
                'chunk_id': 'rag_arch_001'
            }
        ]
        
        # Add documents to knowledge base
        added_count = self.rag_engine.add_documents(sample_docs)
        self.update_status(f"Loaded {added_count} documents into knowledge base")
    
    def run(self):
        """Start the GUI application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

# Example usage and demonstration
if __name__ == "__main__":
    print("🔍 Enterprise AI Search Platform")
    print("=" * 50)
    print("Launching professional search interface...")
    print("Features:")
    print("- Advanced RAG-powered search")
    print("- Real-time results with confidence scoring")
    print("- Source attribution and fact-checking")
    print("- Search history and analytics")
    print("- Professional enterprise UI")
    print("=" * 50)
    
    # Launch the GUI application
    app = EnterpriseSearchGUI()
    app.run()
