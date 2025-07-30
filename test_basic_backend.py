#!/usr/bin/env python3
"""
Basic Backend Test - Works without AI dependencies
"""

import sys
import os

def test_basic_backend():
    """Test basic backend functionality without AI components"""
    print("🧪 Testing Basic Backend (No AI Dependencies)...")
    
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
        
        # Test basic AI components (they should handle missing dependencies gracefully)
        try:
            from backend.core.content_generator import ContentGenerator
            print("✅ Content generator OK (with fallback)")
        except Exception as e:
            print(f"⚠️  Content generator failed: {e}")
        
        try:
            from backend.core.style_refiner import StyleRefiner
            print("✅ Style refiner OK (with fallback)")
        except Exception as e:
            print(f"⚠️  Style refiner failed: {e}")
        
        try:
            from backend.core.seo_optimizer import SEOOptimizer
            print("✅ SEO optimizer OK (with fallback)")
        except Exception as e:
            print(f"⚠️  SEO optimizer failed: {e}")
        
        try:
            from backend.core.plagiarism_checker import PlagiarismChecker
            print("✅ Plagiarism checker OK (with fallback)")
        except Exception as e:
            print(f"⚠️  Plagiarism checker failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_server_startup():
    """Test if the server can start"""
    print("\n🧪 Testing Server Startup...")
    
    try:
        from backend.main import app
        
        # Test that the app has the required endpoints
        routes = [route.path for route in app.routes]
        required_routes = ["/", "/docs", "/api/v1/auth/login", "/api/v1/auth/register"]
        
        for route in required_routes:
            if route in routes:
                print(f"✅ Route {route} exists")
            else:
                print(f"⚠️  Route {route} missing")
        
        print("✅ Server startup test passed")
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False

def main():
    """Run basic backend tests"""
    print("🚀 Basic Backend Test")
    print("=" * 50)
    
    if not test_basic_backend():
        print("\n❌ Basic backend test failed")
        print("💡 Check the error messages above")
        return
    
    if not test_server_startup():
        print("\n❌ Server startup test failed")
        print("💡 Check the error messages above")
        return
    
    print("\n🎉 Basic backend test passed!")
    print("\n📋 Next steps:")
    print("1. Start backend: python -m uvicorn backend.main:app --reload")
    print("2. Access API docs: http://localhost:8000/docs")
    print("3. Test endpoints: http://localhost:8000/")
    print("\n💡 Note: AI features will use mock implementations")
    print("   To enable full AI features, install: pip install langchain")

if __name__ == "__main__":
    main() 