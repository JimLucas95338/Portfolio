#!/usr/bin/env python3
"""
Portfolio Launcher - Jim Lucas
==============================

Interactive launcher for all portfolio projects.
Provides menu-driven access to launch specific projects or view documentation.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

class PortfolioLauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.projects = {
            '1': {
                'name': 'AI Search Platform',
                'path': 'AI-Search-Platform',
                'main_file': 'src/enterprise_search_gui.py',
                'description': 'Enterprise AI search with RAG architecture (June-Aug 2025)',
                'docs': 'docs/product-requirements.md'
            },
            '2': {
                'name': 'AI Content Optimization Platform',
                'path': 'AI-Content-Optimization-Platform',
                'main_file': 'src/dashboard_app.py',
                'description': 'AI-powered content optimization (Mar-May 2025)',
                'docs': 'docs/product-requirements.md'
            },
            '3': {
                'name': 'Value-Based Care Analytics',
                'path': 'Value-Based-Care-Analytics',
                'main_file': 'launch_dashboard.py',
                'description': 'Pearl Health-aligned population health (Dec 2024-Feb 2025)',
                'docs': 'docs/executive-summary.md'
            },
            '4': {
                'name': 'Digital Therapeutics Case Study',
                'path': 'Digital-Therapeutics-Case-Study',
                'main_file': 'mockups/dashboard_example.ipynb',
                'description': 'Digital therapeutics strategy (Sep-Nov 2024)',
                'docs': 'docs/executive-summary.md'
            },
            '5': {
                'name': 'FHIR API Integration Demo',
                'path': 'FHIR-API-Integration-Demo',
                'main_file': 'api/fhir_gui_demo.py',
                'description': 'Healthcare interoperability (Jun-Aug 2024)',
                'docs': 'docs/product-requirements.md'
            },
            '6': {
                'name': 'Healthcare Data Dashboard',
                'path': 'Healthcare-Data-Dashboard',
                'main_file': 'notebooks/healthcare_dashboard_example.ipynb',
                'description': 'Healthcare analytics foundation (Mar-May 2024)',
                'docs': 'docs/executive-summary.md'
            }
        }

    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print portfolio header."""
        print("=" * 70)
        print("🚀 JIM LUCAS - SENIOR AI PRODUCT MANAGER PORTFOLIO")
        print("   Healthcare & Life Sciences + AI Platforms")
        print("=" * 70)
        print()

    def print_menu(self):
        """Print main menu options."""
        print("📋 Available Projects:")
        print("-" * 50)
        
        for key, project in self.projects.items():
            status = self.get_project_status(project['path'])
            print(f"{key}. {project['name']} {status}")
            print(f"   {project['description']}")
            print()
        
        print("📖 Additional Options:")
        print("-" * 50)
        print("w. Open Portfolio Website (index.html)")
        print("p. View Full Portfolio Document")
        print("h. Help & Documentation")
        print("q. Quit")
        print()

    def get_project_status(self, project_path):
        """Get project status indicator."""
        project_dir = self.base_path / project_path
        if not project_dir.exists():
            return "❌"
        
        # Check for key files to determine completeness
        has_docs = (project_dir / "docs").exists() or (project_dir / "README.md").exists()
        has_src = (project_dir / "src").exists() or (project_dir / "api").exists()
        
        if has_docs and has_src:
            return "✅"
        elif has_docs or has_src:
            return "⚠️"
        else:
            return "📁"

    def launch_project(self, project_key):
        """Launch selected project."""
        if project_key not in self.projects:
            print("❌ Invalid project selection!")
            return False

        project = self.projects[project_key]
        project_path = self.base_path / project['path']
        main_file_path = project_path / project['main_file']

        print(f"🚀 Launching {project['name']}...")
        print(f"📂 Project Path: {project_path}")
        
        if not project_path.exists():
            print(f"❌ Project directory not found: {project_path}")
            return False

        try:
            if main_file_path.suffix == '.py':
                # Launch Python file
                print(f"🐍 Running Python script: {main_file_path}")
                os.chdir(project_path)
                subprocess.run([sys.executable, main_file_path], check=True)
                
            elif main_file_path.suffix == '.ipynb':
                # Launch Jupyter notebook
                print(f"📓 Opening Jupyter notebook: {main_file_path}")
                os.chdir(project_path)
                subprocess.run(['jupyter', 'notebook', main_file_path], check=True)
                
            elif main_file_path.suffix == '.html':
                # Open in browser
                print(f"🌐 Opening in browser: {main_file_path}")
                webbrowser.open(str(main_file_path))
                
            else:
                # Open project directory
                print(f"📁 Opening project directory: {project_path}")
                if os.name == 'nt':  # Windows
                    subprocess.run(['explorer', str(project_path)])
                elif os.name == 'posix':  # macOS/Linux
                    subprocess.run(['open', str(project_path)])

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Error launching project: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ Required software not found. Please ensure Python/Jupyter is installed.")
            return False

    def view_documentation(self, project_key):
        """View project documentation."""
        if project_key not in self.projects:
            return False

        project = self.projects[project_key]
        doc_path = self.base_path / project['path'] / project['docs']
        
        if doc_path.exists():
            print(f"📖 Opening documentation: {doc_path}")
            if os.name == 'nt':  # Windows
                subprocess.run(['start', str(doc_path)], shell=True)
            else:  # macOS/Linux
                subprocess.run(['open', str(doc_path)])
            return True
        else:
            print(f"❌ Documentation not found: {doc_path}")
            return False

    def open_portfolio_website(self):
        """Open the main portfolio website."""
        index_path = self.base_path / "index.html"
        if index_path.exists():
            print("🌐 Opening portfolio website...")
            webbrowser.open(str(index_path))
        else:
            print("❌ Portfolio website not found!")

    def view_full_portfolio(self):
        """View the full portfolio document."""
        portfolio_path = self.base_path / "Portfolio.md"
        if portfolio_path.exists():
            print("📄 Opening full portfolio document...")
            if os.name == 'nt':  # Windows
                subprocess.run(['start', str(portfolio_path)], shell=True)
            else:  # macOS/Linux
                subprocess.run(['open', str(portfolio_path)])
        else:
            print("❌ Portfolio document not found!")

    def show_help(self):
        """Show help information."""
        print("📚 PORTFOLIO LAUNCHER HELP")
        print("=" * 40)
        print()
        print("🎯 How to Use:")
        print("• Enter a number (1-6) to launch a project")
        print("• Enter 'w' to open the portfolio website")
        print("• Enter 'p' to view the full portfolio document")
        print("• Enter 'q' to quit")
        print()
        print("📁 Project Structure:")
        print("• Each project contains source code, documentation, and demos")
        print("• Status indicators: ✅ Complete, ⚠️ Partial, ❌ Missing, 📁 Basic")
        print()
        print("🔧 Requirements:")
        print("• Python 3.7+ for Python projects")
        print("• Jupyter Notebook for .ipynb files")
        print("• Modern web browser for HTML files")
        print()
        print("💡 Tips:")
        print("• Projects are ordered by recency (newest first)")
        print("• Each project includes detailed documentation")
        print("• Some projects may require additional dependencies")
        print()

    def run(self):
        """Main launcher loop."""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            try:
                choice = input("🎯 Select an option: ").strip().lower()
                
                if choice == 'q':
                    print("👋 Thanks for exploring my portfolio!")
                    break
                elif choice == 'w':
                    self.open_portfolio_website()
                elif choice == 'p':
                    self.view_full_portfolio()
                elif choice == 'h':
                    self.clear_screen()
                    self.show_help()
                    input("\nPress Enter to continue...")
                elif choice in self.projects:
                    self.launch_project(choice)
                    input("\nPress Enter to return to menu...")
                else:
                    print("❌ Invalid selection! Please try again.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                input("Press Enter to continue...")

def main():
    """Entry point for portfolio launcher."""
    try:
        launcher = PortfolioLauncher()
        launcher.run()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
