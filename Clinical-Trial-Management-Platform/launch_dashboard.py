#!/usr/bin/env python3
"""
Clinical Trial Management Platform - Launch Script
Launches the site coordinator dashboard application.
"""

import sys
import os
import subprocess

def main():
    """Launch the Clinical Trial Management Platform dashboard"""
    print("🏥 Clinical Trial Management Platform")
    print("=" * 50)
    print("Launching Site Coordinator Dashboard...")
    print()
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gui_path = os.path.join(script_dir, "src", "clinical_trial_gui.py")
    
    # Check if the GUI file exists
    if not os.path.exists(gui_path):
        print("❌ Error: GUI application not found!")
        print(f"Expected location: {gui_path}")
        return 1
    
    try:
        # Launch the GUI application
        print("🚀 Starting Clinical Trial Dashboard...")
        print("📊 Features available:")
        print("   • Study Overview & Metrics")
        print("   • Patient Management")
        print("   • Visit Scheduling")
        print("   • Compliance Monitoring")
        print("   • Document Management")
        print()
        print("💡 Tip: Use the tabs to navigate between different sections")
        print("🔄 Click 'Refresh' to update data in real-time")
        print()
        
        # Run the GUI application
        subprocess.run([sys.executable, gui_path], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
