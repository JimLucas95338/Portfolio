#!/usr/bin/env python3
"""
🏥 Value-Based Care Analytics Dashboard Launcher

Simple launcher script for the VBC Analytics GUI Dashboard.
This script handles the setup and launch of the dashboard application.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'scikit-learn', 'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_packages(packages):
    """Install missing packages"""
    if not packages:
        return
    
    print("🔧 Installing missing packages...")
    for package in packages:
        if package == 'tkinter':
            print("⚠️  tkinter is not available. Please install python3-tk:")
            print("   Ubuntu/Debian: sudo apt-get install python3-tk")
            print("   macOS: tkinter should be included with Python")
            print("   Windows: tkinter should be included with Python")
            continue
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def launch_dashboard():
    """Launch the Value-Based Care Dashboard"""
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path to the GUI application
        gui_path = os.path.join(script_dir, 'src', 'vbc_dashboard_gui.py')
        
        if not os.path.exists(gui_path):
            print(f"❌ Dashboard GUI not found at: {gui_path}")
            return False
        
        print("🏥 Launching Value-Based Care Analytics Dashboard...")
        print("📊 Loading sample data and initializing interface...")
        
        # Launch the GUI
        subprocess.run([sys.executable, gui_path])
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to launch dashboard: {str(e)}")
        return False

def main():
    """Main launcher function"""
    print("🏥 Value-Based Care Analytics Dashboard Launcher")
    print("=" * 55)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        
        response = input("Would you like to install missing packages? (y/n): ")
        if response.lower() in ['y', 'yes']:
            install_packages(missing_packages)
        else:
            print("❌ Cannot launch dashboard without required packages.")
            return
    else:
        print("✅ All dependencies are available")
    
    # Launch dashboard
    print("\n🚀 Starting dashboard...")
    success = launch_dashboard()
    
    if success:
        print("✅ Dashboard launched successfully!")
    else:
        print("❌ Failed to launch dashboard")

if __name__ == "__main__":
    main()