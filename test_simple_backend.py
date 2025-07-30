#!/usr/bin/env python3
"""
Simple Backend Test - Only tests core functionality
"""

import sys
import os

def test_core_imports():
    """Test only core imports that should always work"""
    print("🧪 Testing Core Imports...")
    
    try:
        import fastapi
        print("✅ FastAPI OK")
    except ImportError:
        print("❌ FastAPI not installed")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn OK")
    except ImportError:
        print("❌ Uvicorn not installed")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy OK")
    except ImportError:
        print("❌ SQLAlchemy not installed")
        return False
    
    try:
        import jwt
        print("✅ JWT OK")
    except ImportError:
        print("❌ JWT not installed")
        return False
    
    try:
        import bcrypt
        print("✅ bcrypt OK")
    except ImportError:
        print("❌ bcrypt not installed")
        return False
    
    print("✅ All core imports successful!")
    return True

def test_backend_app():
    """Test if the backend app can be imported"""
    print("\n🧪 Testing Backend App...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Test basic app import
        from backend.main import app
        print("✅ Backend app imported successfully")
        
        # Test that app has basic structure
        if hasattr(app, 'routes'):
            print("✅ App has routes")
        else:
            print("❌ App missing routes")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backend app test failed: {e}")
        return False

def test_database_models():
    """Test database models with SQLite fallback"""
    print("\n🧪 Testing Database Models...")
    
    try:
        # Try SQLite fallback first
        from backend.models.database_sqlite import Base, get_db
        print("✅ SQLite database models OK")
        return True
    except Exception as e:
        print(f"❌ Database models failed: {e}")
        return False

def test_auth_modules():
    """Test authentication modules"""
    print("\n🧪 Testing Auth Modules...")
    
    try:
        from backend.auth import JWTHandler, get_current_active_user
        print("✅ Auth modules OK")
        return True
    except Exception as e:
        print(f"❌ Auth modules failed: {e}")
        return False

def main():
    """Run simple backend tests"""
    print("🚀 Simple Backend Test")
    print("=" * 50)
    
    if not test_core_imports():
        print("\n❌ Core imports failed")
        print("💡 Install core dependencies:")
        print("   pip install fastapi uvicorn sqlalchemy python-jose[cryptography] bcrypt")
        return
    
    if not test_backend_app():
        print("\n❌ Backend app test failed")
        return
    
    if not test_database_models():
        print("\n❌ Database models test failed")
        return
    
    if not test_auth_modules():
        print("\n❌ Auth modules test failed")
        return
    
    print("\n🎉 Simple backend test passed!")
    print("\n📋 Next steps:")
    print("1. Start backend: python -m uvicorn backend.main:app --reload")
    print("2. Access API docs: http://localhost:8000/docs")
    print("3. Test endpoints: http://localhost:8000/")
    print("\n💡 Note: AI features will use mock implementations")

if __name__ == "__main__":
    main() 