"""
AI Content Optimization Platform - Launch Script
===============================================

Main launcher for the AI Content Optimization Platform.
Provides options to run different components of the platform:
- Dashboard Application (GUI)
- Content Analyzer (CLI)
- Demo Mode with Sample Content

Usage:
    python launch_optimizer.py [--mode=dashboard|analyzer|demo]
    python launch_optimizer.py --help
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def print_banner():
    """Display the platform banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║      🚀 AI CONTENT OPTIMIZATION PLATFORM 🚀                  ║
    ║                                                              ║
    ║  Intelligent Content Analysis & Performance Optimization     ║
    ║                                                              ║
    ║  Features:                                                   ║
    ║  • Real-time content analysis and optimization               ║
    ║  • Multi-platform content recommendations                    ║
    ║  • AI-powered performance prediction                         ║
    ║  • Professional dashboard interface                          ║
    ║  • Comprehensive analytics and reporting                     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'tkinter',
        'pandas', 
        'numpy',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing in simulation mode...")
        print("💡 For full functionality, install: pip install pandas numpy matplotlib seaborn")
        return False
    else:
        print("✅ All dependencies available!")
        return True

def launch_dashboard():
    """Launch the main dashboard application."""
    print("\n🚀 Launching AI Content Optimization Dashboard...")
    print("📊 Starting professional content analysis interface...")
    
    try:
        # Import and run dashboard
        from src.dashboard_app import ContentOptimizationDashboard
        
        print("✅ Dashboard modules loaded successfully")
        print("🎯 Opening dashboard window...")
        
        app = ContentOptimizationDashboard()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importing dashboard: {e}")
        print("🔧 Running in fallback mode...")
        run_fallback_demo()
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        print("💡 Try running: python src/dashboard_app.py directly")

def launch_analyzer():
    """Launch the content analyzer in CLI mode."""
    print("\n🔍 Launching Content Analyzer (CLI Mode)...")
    
    try:
        from src.content_analyzer import ContentAnalyzer
        
        analyzer = ContentAnalyzer()
        print("✅ Content analyzer initialized")
        
        # Interactive analysis
        print("\n📝 Enter content for analysis (press Enter twice to finish):")
        content_lines = []
        while True:
            line = input()
            if line == "" and content_lines:
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines)
        
        if content.strip():
            print("\n🔍 Analyzing content...")
            analysis = analyzer.analyze_content(content, platform="blog")
            
            print(f"\n📊 Analysis Results:")
            print(f"  Word Count: {analysis.word_count}")
            print(f"  Readability: {analysis.readability_rating} (Score: {analysis.flesch_score})")
            print(f"  Sentiment: {analysis.sentiment_label} ({analysis.sentiment_polarity:+.2f})")
            print(f"  Predicted Engagement: {analysis.predicted_engagement}%")
            print(f"  Performance Tier: {analysis.performance_tier}")
            print(f"  Optimization Score: {analysis.optimization_score:.0%}")
            
            if analysis.recommendations:
                print(f"\n💡 Optimization Recommendations:")
                for i, rec in enumerate(analysis.recommendations, 1):
                    print(f"  {i}. {rec['category']}: {rec['recommendation']}")
        else:
            print("❌ No content provided for analysis")
    
    except ImportError:
        print("❌ Content analyzer not available")
        run_fallback_demo()
    except Exception as e:
        print(f"❌ Error running analyzer: {e}")

def run_demo_mode():
    """Run demonstration mode with sample content."""
    print("\n🎭 Launching Demo Mode...")
    print("📚 Loading sample content and analysis...")
    
    # Sample content for demo
    sample_content = {
        "title": "How AI is Revolutionizing Content Marketing in 2024",
        "content": """
        Artificial intelligence is transforming the content marketing landscape in unprecedented ways. 
        From automated content generation to personalized recommendations, AI tools are helping 
        marketers create more engaging and effective content than ever before.
        
        The integration of machine learning algorithms enables real-time content optimization, 
        predictive performance analysis, and audience-specific personalization at scale. 
        Companies leveraging AI for content marketing are seeing 40% higher engagement rates 
        and 60% more efficient content production workflows.
        
        Key benefits include automated A/B testing, sentiment analysis, readability optimization, 
        and cross-platform content adaptation. The future of content marketing is AI-powered, 
        data-driven, and results-focused.
        
        Are you ready to transform your content strategy with artificial intelligence?
        """,
        "platform": "blog"
    }
    
    try:
        from src.content_analyzer import ContentAnalyzer
        
        analyzer = ContentAnalyzer()
        analysis = analyzer.analyze_content(
            sample_content["content"], 
            sample_content["title"], 
            sample_content["platform"]
        )
        
        print(f"\n📊 DEMO ANALYSIS RESULTS")
        print("=" * 50)
        print(f"Title: {sample_content['title']}")
        print(f"Platform: {sample_content['platform'].title()}")
        print(f"Content Length: {analysis.word_count} words")
        print()
        print(f"📈 Performance Metrics:")
        print(f"  • Predicted Engagement: {analysis.predicted_engagement}%")
        print(f"  • Performance Tier: {analysis.performance_tier}")
        print(f"  • Readability: {analysis.readability_rating} (Flesch: {analysis.flesch_score})")
        print(f"  • Sentiment: {analysis.sentiment_label} ({analysis.sentiment_polarity:+.2f})")
        print(f"  • Optimization Score: {analysis.optimization_score:.0%}")
        
        if analysis.recommendations:
            print(f"\n💡 AI Recommendations:")
            for i, rec in enumerate(analysis.recommendations, 1):
                print(f"  {i}. {rec['category']} ({rec['priority']} Priority)")
                print(f"     Issue: {rec['issue']}")
                print(f"     💡 {rec['recommendation']}")
                print(f"     📈 Impact: {rec['expected_impact']}")
                print()
        else:
            print(f"\n🎉 Content is well-optimized! No major improvements needed.")
        
        print("\n" + "=" * 50)
        print("🚀 Demo completed successfully!")
        print("💡 To analyze your own content, use --mode=dashboard or --mode=analyzer")
        
    except ImportError:
        print("📦 Running simulation demo...")
        run_fallback_demo()

def run_fallback_demo():
    """Run a fallback demo when dependencies aren't available."""
    print("\n🔧 SIMULATION MODE - AI Content Optimization Platform")
    print("=" * 60)
    print("📝 Sample Analysis Results (Simulated):")
    print()
    print("Content: 'How AI is Revolutionizing Content Marketing in 2024'")
    print("Platform: Blog")
    print("Word Count: 145 words")
    print()
    print("📊 Performance Prediction:")
    print("  • Engagement Rate: 6.8% (Good - Above Average)")
    print("  • Readability: Fairly Easy (Flesch Score: 72.5)")
    print("  • Sentiment: Positive (+0.35)")
    print("  • Optimization Score: 85%")
    print()
    print("💡 AI Recommendations:")
    print("  1. Content Length (Medium Priority)")
    print("     • Expand content to 800-1200 words for better SEO")
    print("     • Expected impact: +15-25% engagement")
    print()
    print("  2. Call-to-Action (High Priority)")
    print("     • Add clear next steps for readers")
    print("     • Expected impact: +20-30% conversions")
    print()
    print("✅ Analysis complete! Content shows strong potential.")
    print("💡 Install full dependencies for complete functionality.")

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="AI Content Optimization Platform Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_optimizer.py                    # Interactive mode
  python launch_optimizer.py --mode=dashboard  # Launch GUI dashboard
  python launch_optimizer.py --mode=analyzer   # Launch CLI analyzer
  python launch_optimizer.py --mode=demo       # Run demonstration
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['dashboard', 'analyzer', 'demo'],
        help='Launch mode: dashboard (GUI), analyzer (CLI), or demo'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check dependencies
    deps_available = check_dependencies()
    
    # Determine launch mode
    if args.mode:
        mode = args.mode
    else:
        print("\n🎯 Select Launch Mode:")
        print("1. Dashboard (GUI) - Full interactive interface")
        print("2. Analyzer (CLI) - Command line analysis")  
        print("3. Demo - Sample content analysis")
        print("4. Exit")
        
        while True:
            choice = input("\nEnter choice (1-4): ").strip()
            if choice == '1':
                mode = 'dashboard'
                break
            elif choice == '2':
                mode = 'analyzer'
                break
            elif choice == '3':
                mode = 'demo'
                break
            elif choice == '4':
                print("👋 Goodbye!")
                return
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    # Launch selected mode
    try:
        if mode == 'dashboard':
            launch_dashboard()
        elif mode == 'analyzer':
            launch_analyzer()
        elif mode == 'demo':
            run_demo_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using AI Content Optimization Platform!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check the installation and try again.")

if __name__ == "__main__":
    main()
