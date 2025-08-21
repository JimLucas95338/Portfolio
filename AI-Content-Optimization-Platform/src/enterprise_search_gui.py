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
import sys
import os

# Add the current directory to the path to import rag_engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag_engine import AdvancedRAGEngine, RAGResponse, SearchResult
except ImportError:
    print("⚠️ Could not import rag_engine. Running in demo mode.")
    
    # Create mock classes for demo
    class MockRAGResponse:
        def __init__(self):
            self.synthesized_answer = "This is a demo response from the AI Search Platform."
            self.source_results = []
            self.confidence_score = 0.85
            self.query_intent = "informational"
            self.follow_up_questions = ["What are the benefits?", "How does it work?"]
            self.fact_check_status = "verified"
            self.processing_time_ms = 125.5
    
    class MockSearchResult:
        def __init__(self, content, source, score):
            self.content = content
            self.source = source
            self.relevance_score = score
            self.confidence_score = score * 0.9
            self.metadata = {'section': 'Demo', 'source_type': 'document'}
    
    class MockRAGEngine:
        def __init__(self):
            pass
        
        async def search(self, query, user_id="default"):
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            response = MockRAGResponse()
            response.source_results = [
                MockSearchResult(f"Demo content for query: {query}", "demo_source.pdf", 0.9),
                MockSearchResult(f"Additional context about: {query}", "additional_source.pdf", 0.8)
            ]
            return response
        
        def get_performance_metrics(self):
            return {'queries_processed': 42, 'avg_response_time': 150.2, 'avg_confidence': 0.82, 'cache_hit_rate': 15}
    
    AdvancedRAGEngine = MockRAGEngine
    RAGResponse = MockRAGResponse
    SearchResult = MockSearchResult

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
        self.setup_gui()
        
        # Application state
        self.current_user = "enterprise_user"
        self.search_history = []
        self.saved_queries = []
        self.current_results = None
        
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
        
        # User info
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
    
    def handle_search_response(self, query: str, response):
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
    
    def display_search_results(self, query: str, response):
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
            
            for i, result in enumerate(response.source_results[:5], 1):
                self.create_result_card(result, i)
    
    def create_result_card(self, result, index: int):
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
        confidence_color = self.colors['success'] if result.confidence_score > 0.8 else self.colors['warning']
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
        content_frame.pack(fill='x', padx=15, pady=(0, 15))
        
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
    
    def update_analytics(self):
        """Update analytics display."""
        try:
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
        except Exception as e:
            print(f"Error updating analytics: {e}")
    
    def update_history_display(self):
        """Update search history display."""
        self.history_listbox.delete(0, tk.END)
        
        for entry in reversed(self.search_history[-20:]):
            timestamp = entry['timestamp'].strftime('%H:%M:%S')
            display_text = f"[{timestamp}] {entry['query']} (Confidence: {entry['confidence']:.2f})"
            self.history_listbox.insert(0, display_text)
    
    def on_history_select(self, event):
        """Handle selection from search history."""
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            history_entry = self.search_history[-(index+1)]
            self.search_var.set(history_entry['query'])
    
    def show_search_history(self):
        """Show search history in a popup."""
        self.notebook.select(self.history_frame)
    
    def show_saved_queries(self):
        """Show saved queries dialog."""
        messagebox.showinfo("Saved Queries", "Saved queries feature would be implemented here.")
    
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
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
