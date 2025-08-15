#!/usr/bin/env python3
"""
Simple test script to isolate OpenAI client initialization issues
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing OpenAI client initialization...")
print(f"Python version: {os.sys.version}")
print(f"Current working directory: {os.getcwd()}")

# Check environment variables
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key found: {'Yes' if api_key and api_key != 'your_openai_api_key_here' else 'No'}")

# Test 1: Basic import
try:
    from openai import OpenAI
    print("✅ OpenAI import successful")
except ImportError as e:
    print(f"❌ OpenAI import failed: {e}")
    exit(1)

# Test 2: Simple client creation
try:
    if api_key and api_key != 'your_openai_api_key_here':
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client creation successful")
        
        # Test 3: Simple API call
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print("✅ OpenAI API call successful")
            print(f"Response: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ OpenAI API call failed: {e}")
    else:
        print("⚠️  No valid API key found, skipping API test")
        
except Exception as e:
    print(f"❌ OpenAI client creation failed: {e}")
    
    # Test 4: Check for proxy-related environment variables
    proxy_vars = [var for var in os.environ if 'proxy' in var.lower() or 'PROXY' in var]
    if proxy_vars:
        print(f"⚠️  Proxy-related environment variables found: {proxy_vars}")
    
    # Test 5: Try with minimal configuration
    try:
        print("Trying minimal client creation...")
        client = OpenAI()
        print("✅ OpenAI client creation with minimal config successful")
    except Exception as e2:
        print(f"❌ Minimal client creation also failed: {e2}")

print("\nTest completed!")
