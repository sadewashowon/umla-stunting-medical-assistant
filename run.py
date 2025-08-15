#!/usr/bin/env python3
"""
Stunting Medical Assistant Launcher
Simple script to run the application with proper configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import openai
        import yaml
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_config():
    """Check if configuration files exist"""
    config_file = Path("config.yaml")
    env_file = Path(".env")
    
    if not config_file.exists():
        print("⚠️  config.yaml not found, creating default...")
        # The app will create this automatically
    
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("📝 Please copy env_example.txt to .env and configure your settings")
        print("   cp env_example.txt .env")
        return False
    
    print("✅ Configuration files found")
    return True

def main():
    """Main launcher function"""
    print("🍼 Stunting Medical Assistant")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check configuration
    check_config()
    
    print("\n🚀 Starting application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 40)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

