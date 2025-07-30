#!/usr/bin/env python3
"""
Minimal Test - Works with basic dependencies only
"""

import sys
import os

def test_minimal_imports():
    """Test minimal imports that should work"""
    print("🧪 Testing Minimal Imports...")
    
    # Test basic Python
    try:
        import json
        import logging
        print("✅ Basic Python modules OK")
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return False
    
    # Test FastAPI (core)
    try:
        import fastapi
        print("✅ FastAPI OK")
    except ImportError:
        print("❌ FastAPI not installed - run: pip install fastapi")
        return False
    
    # Test SQLAlchemy (core)
    try:
        import sqlalchemy
        print("✅ SQLAlchemy OK")
    except ImportError:
        print("❌ SQLAlchemy not installed - run: pip install sqlalchemy")
        return False
    
    # Test JWT (authentication)
    try:
        import jwt
        print("✅ JWT OK")
    except ImportError:
        print("❌ JWT not installed - run: pip install python-jose[cryptography]")
        return False
    
    # Test bcrypt (password hashing)
    try:
        import bcrypt
        print("✅ bcrypt OK")
    except ImportError:
        print("❌ bcrypt not installed - run: pip install bcrypt")
        return False
    
    print("✅ All minimal imports successful!")
    return True

def test_backend_basic():
    """Test basic backend functionality"""
    print("\n🧪 Testing Basic Backend...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Test basic imports
        from backend.main import app
        print("✅ Backend app imported")
        
        # Test database models (using SQLite fallback)
        try:
            from backend.models.database import Base, get_db
            print("✅ PostgreSQL database models OK")
        except:
            # Try SQLite fallback
            from backend.models.database_sqlite import Base, get_db
            print("✅ SQLite database models OK (fallback)")
        
        # Test auth modules
        from backend.auth import JWTHandler, get_current_active_user
        print("✅ Auth modules OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def main():
    """Run minimal tests"""
    print("🚀 Minimal Component Test")
    print("=" * 50)
    
    if not test_minimal_imports():
        print("\n❌ Minimal imports failed")
        print("💡 Install core dependencies:")
        print("   pip install fastapi sqlalchemy python-jose[cryptography] bcrypt")
        return
    
    if not test_backend_basic():
        print("\n❌ Backend test failed")
        print("💡 Check the error messages above")
        return
    
    print("\n🎉 Minimal test passed!")
    print("\n📋 Next steps:")
    print("1. Start backend: python -m uvicorn backend.main:app --reload")
    print("2. Access API docs: http://localhost:8000/docs")
    print("3. Test endpoints: http://localhost:8000/")

if __name__ == "__main__":
    main() 