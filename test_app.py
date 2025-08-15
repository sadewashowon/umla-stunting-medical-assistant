#!/usr/bin/env python3
"""
Test script for Stunting Medical Assistant
Tests basic functionality without running the full Streamlit app
"""

import os
import sys
import sqlite3
from pathlib import Path

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        import auth_utils
        print("✅ auth_utils imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth_utils: {e}")
        return False
    
    try:
        import stunting_knowledge
        print("✅ stunting_knowledge imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import stunting_knowledge: {e}")
        return False
    
    try:
        import yaml
        print("✅ yaml imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import yaml: {e}")
        return False
    
    return True

def test_database():
    """Test database creation and basic operations"""
    print("\n🗄️  Testing database functionality...")
    
    try:
        # Test database initialization
        from auth_utils import init_auth_db, create_demo_user
        
        # Initialize database
        init_auth_db()
        print("✅ Database initialized successfully")
        
        # Test demo user creation
        success, message = create_demo_user()
        if success:
            print("✅ Demo user created successfully")
        else:
            print(f"ℹ️  Demo user status: {message}")
        
        # Test database connection
        conn = sqlite3.connect('stunting_assistant.db')
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        expected_tables = ['users', 'chat_history']
        for table in expected_tables:
            if table in table_names:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
                return False
        
        # Check demo user exists
        cursor.execute("SELECT username FROM users WHERE username = 'demo'")
        user = cursor.fetchone()
        if user:
            print("✅ Demo user found in database")
        else:
            print("❌ Demo user not found in database")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_knowledge_base():
    """Test the stunting knowledge base"""
    print("\n📚 Testing knowledge base...")
    
    try:
        from stunting_knowledge import get_knowledge_response, get_knowledge_summary
        
        # Test knowledge summary
        summary = get_knowledge_summary()
        if "Complete Stunting Knowledge Base" in summary:
            print("✅ Knowledge base summary generated")
        else:
            print("❌ Knowledge base summary failed")
            return False
        
        # Test response generation
        test_queries = [
            "What is stunting?",
            "How to prevent stunting?",
            "What causes stunting?",
            "Random unrelated question"
        ]
        
        for query in test_queries:
            response = get_knowledge_response(query)
            if response and len(response) > 50:
                print(f"✅ Query '{query[:20]}...' got response")
            else:
                print(f"❌ Query '{query[:20]}...' failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Knowledge base test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n⚙️  Testing configuration...")
    
    try:
        config_path = Path("config.yaml")
        if not config_path.exists():
            print("⚠️  config.yaml not found, will be created by app")
            return True
        
        with open(config_path, 'r') as file:
            import yaml
            config = yaml.safe_load(file)
        
        # Check required config sections
        required_sections = ['credentials', 'cookie', 'app']
        for section in required_sections:
            if section in config:
                print(f"✅ Config section '{section}' found")
            else:
                print(f"❌ Config section '{section}' missing")
                return False
        
        # Check demo user in credentials
        if 'demo' in config.get('credentials', {}).get('usernames', {}):
            print("✅ Demo user found in config")
        else:
            print("❌ Demo user missing from config")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def cleanup():
    """Clean up test artifacts"""
    print("\n🧹 Cleaning up test artifacts...")
    
    try:
        # Remove test database
        if os.path.exists('stunting_assistant.db'):
            os.remove('stunting_assistant.db')
            print("✅ Test database removed")
        
        # Remove any other test files
        test_files = ['test_log.txt', 'test_output.txt']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"✅ Test file '{file}' removed")
        
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

def main():
    """Run all tests"""
    print("🍼 Stunting Medical Assistant - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Database Operations", test_database),
        ("Knowledge Base", test_knowledge_base),
        ("Configuration", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the app, run:")
        print("   python run.py")
        print("   or")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   1. Install requirements: pip install -r requirements.txt")
        print("   2. Check file permissions")
        print("   3. Verify Python version (3.8+)")
    
    # Cleanup
    cleanup()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

