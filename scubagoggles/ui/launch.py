#!/usr/bin/env python3
"""
ScubaGoggles UI Launcher
Simple script to start the Streamlit configuration interface
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the ScubaGoggles UI"""
    
    # Determine which app to run
    ui_dir = Path(__file__).parent
    
    # Try the enhanced app first, fall back to basic app
    app_files = [
        ui_dir / "scubaconfigapp.py",
        ui_dir / "config_generator.py"
    ]
    
    app_to_run = None
    for app_file in app_files:
        if app_file.exists():
            app_to_run = app_file
            break
    
    if not app_to_run:
        print("❌ No UI application found!")
        print("Please ensure the UI modules are properly installed.")
        sys.exit(1)
    
    # Check if streamlit is available
    try:
        import streamlit
        print(f"🤿 Starting ScubaGoggles Configuration UI...")
        print(f"📱 Using: {app_to_run.name}")
        print(f"🌐 Opening in your default browser...")
        
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(app_to_run),
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ]
        
        subprocess.run(cmd)
        
    except ImportError:
        print("❌ Streamlit is not installed!")
        print("📦 Please install UI requirements:")
        print("    pip install -r requirements-ui.txt")
        print("📦 Or install streamlit directly:")
        print("    pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 ScubaGoggles UI stopped by user")
    except Exception as e:
        print(f"❌ Error starting UI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()