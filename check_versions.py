#!/usr/bin/env python3
"""
Check package versions and identify compatibility issues
"""

import sys
import pkg_resources

def check_package_versions():
    """Check installed package versions"""
    print("🔍 Checking package versions...")
    print(f"Python version: {sys.version}")
    print()
    
    # Check key packages
    key_packages = [
        'openai',
        'streamlit',
        'python-dotenv',
        'pandas',
        'streamlit-chat'
    ]
    
    for package in key_packages:
        try:
            version = pkg_resources.get_distribution(package).version
            print(f"✅ {package}: {version}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package}: Not installed")
    
    print()
    
    # Check for potential conflicts
    print("🔍 Checking for potential conflicts...")
    
    # Check if there are multiple openai packages
    openai_packages = [pkg for pkg in pkg_resources.working_set if 'openai' in pkg.project_name.lower()]
    if len(openai_packages) > 1:
        print(f"⚠️  Multiple OpenAI-related packages found: {[pkg.project_name for pkg in openai_packages]}")
    
    # Check for httpx (often used by OpenAI)
    try:
        httpx_version = pkg_resources.get_distribution('httpx').version
        print(f"✅ httpx: {httpx_version}")
    except pkg_resources.DistributionNotFound:
        print("❌ httpx: Not installed (might be needed for OpenAI)")
    
    # Check for requests (might conflict)
    try:
        requests_version = pkg_resources.get_distribution('requests').version
        print(f"✅ requests: {requests_version}")
    except pkg_resources.DistributionNotFound:
        print("ℹ️  requests: Not installed")
    
    print()
    print("🔍 Environment check completed!")

if __name__ == "__main__":
    check_package_versions()

