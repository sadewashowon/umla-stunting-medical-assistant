#!/usr/bin/env python3
"""
Minimal test script to isolate OpenAI client initialization issues
"""

import os
import sys

print("🔍 Starting minimal OpenAI test...")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

# Step 1: Check environment
print("\n📋 Step 1: Environment check")
print(f"OPENAI_API_KEY exists: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

# Step 2: Try import
print("\n📦 Step 2: Import test")
try:
    from openai import OpenAI
    print("✅ OpenAI import successful")
except ImportError as e:
    print(f"❌ OpenAI import failed: {e}")
    sys.exit(1)

# Step 3: Check OpenAI version
print("\n🔢 Step 3: Version check")
try:
    import openai
    print(f"✅ OpenAI package version: {openai.__version__}")
except Exception as e:
    print(f"❌ Version check failed: {e}")

# Step 4: Try minimal client creation
print("\n🚀 Step 4: Minimal client creation")
try:
    client = OpenAI()
    print("✅ Minimal client creation successful")
except Exception as e:
    print(f"❌ Minimal client creation failed: {e}")
    print(f"Error type: {type(e).__name__}")
    print(f"Error details: {str(e)}")

# Step 5: Try with API key
print("\n🔑 Step 5: Client with API key")
api_key = os.getenv('OPENAI_API_KEY')
if api_key and api_key != 'your_openai_api_key_here':
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Client with API key successful")
        
        # Step 6: Try simple API call
        print("\n📡 Step 6: Simple API call")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print("✅ API call successful")
            print(f"Response: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ API call failed: {e}")
            print(f"Error type: {type(e).__name__}")
    except Exception as e:
        print(f"❌ Client with API key failed: {e}")
        print(f"Error type: {type(e).__name__}")
else:
    print("⚠️  No valid API key found, skipping API key test")

print("\n✅ Test completed!")

