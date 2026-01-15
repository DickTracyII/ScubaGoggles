#!/usr/bin/env python3
"""
ScubaGoggles UI Launcher
Simple script to start the Streamlit configuration interface
"""

import subprocess
import shlex
import sys
from pathlib import Path
import argparse


def launch_ui(arguments: argparse.Namespace):
    """Launch the ScubaGoggles UI"""

    # Determine which app to run
    app_to_run = Path(__file__).parent / 'scubaconfigapp.py'

    if not app_to_run:
        print("❌ No UI application found!")
        print("Please ensure the UI modules are properly installed.")
        sys.exit(1)

    # Check if streamlit is available
    try:
        import streamlit

        print("🤿 Starting ScubaGoggles Configuration UI...")
        print(f"📱 Using: {app_to_run.name}")
        print("🌐 Opening in your default browser...")

        # Launch Streamlit
        cmd = f"""{sys.executable} -m streamlit run {str(app_to_run)} --server.port {arguments.port}"""
        subprocess.run(shlex.split(cmd))

    except ImportError:
        print("❌ Streamlit is not installed!")
        print("📦 Please reinstall ScubaGoggles with the optional UI dependencies:")
        print("    pip install scubagoggles[ui]")
        print("📦 Or install streamlit directly:")
        print("    pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 ScubaGoggles UI stopped by user")
    except Exception as e:
        print(f"❌ Error starting UI: {e}")
        sys.exit(1)

