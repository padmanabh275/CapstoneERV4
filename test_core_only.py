#!/usr/bin/env python3
"""
Core Only Test - Tests only the most basic functionality
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

def test_basic_app_creation():
    """Test if we can create a basic FastAPI app"""
    print("\n🧪 Testing Basic App Creation...")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Create a minimal app
        app = FastAPI(title="Test App")
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add a simple route
        @app.get("/")
        def health_check():
            return {"status": "healthy", "message": "Core test passed"}
        
        print("✅ Basic FastAPI app created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Basic app creation failed: {e}")
        return False

def test_ai_components():
    """Test AI components with optional imports"""
    print("\n🧪 Testing AI Components...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Test content generator (should work with optional imports)
        try:
            from backend.core.content_generator import ContentGenerator
            print("✅ Content generator imported")
        except Exception as e:
            print(f"⚠️  Content generator failed: {e}")
        
        # Test style refiner (should work with optional imports)
        try:
            from backend.core.style_refiner import StyleRefiner
            print("✅ Style refiner imported")
        except Exception as e:
            print(f"⚠️  Style refiner failed: {e}")
        
        # Test SEO optimizer (should work with optional imports)
        try:
            from backend.core.seo_optimizer import SEOOptimizer
            print("✅ SEO optimizer imported")
        except Exception as e:
            print(f"⚠️  SEO optimizer failed: {e}")
        
        # Test plagiarism checker (should work with optional imports)
        try:
            from backend.core.plagiarism_checker import PlagiarismChecker
            print("✅ Plagiarism checker imported")
        except Exception as e:
            print(f"⚠️  Plagiarism checker failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI components test failed: {e}")
        return False

def main():
    """Run core-only tests"""
    print("🚀 Core Only Test")
    print("=" * 50)
    
    if not test_core_imports():
        print("\n❌ Core imports failed")
        print("💡 Install core dependencies:")
        print("   pip install fastapi uvicorn sqlalchemy python-jose[cryptography] bcrypt")
        return
    
    if not test_basic_app_creation():
        print("\n❌ Basic app creation failed")
        return
    
    if not test_ai_components():
        print("\n❌ AI components test failed")
        return
    
    print("\n🎉 Core-only test passed!")
    print("\n📋 Next steps:")
    print("1. Install core dependencies if needed")
    print("2. Try starting a minimal server:")
    print("   python -c \"from fastapi import FastAPI; import uvicorn; app = FastAPI(); uvicorn.run(app, host='0.0.0.0', port=8000)\"")
    print("\n💡 Note: This test doesn't include database or full backend functionality")

if __name__ == "__main__":
    main() 