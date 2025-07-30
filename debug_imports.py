#!/usr/bin/env python3
"""
Debug Import Issues - AI-Assisted Content Creation Platform
This script helps identify specific import problems.
"""

import sys
import os
from pathlib import Path

def debug_imports():
    """Debug import issues step by step"""
    print("🔍 Debugging Import Issues...")
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    # Test 1: Basic Python imports
    print("\n1. Testing basic Python imports...")
    try:
        import json
        import logging
        print("✅ Basic Python modules OK")
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return
    
    # Test 2: FastAPI import
    print("\n2. Testing FastAPI import...")
    try:
        import fastapi
        print("✅ FastAPI import OK")
    except ImportError as e:
        print(f"❌ FastAPI not installed: {e}")
        print("💡 Install with: pip install fastapi")
        return
    
    # Test 3: SQLAlchemy import
    print("\n3. Testing SQLAlchemy import...")
    try:
        import sqlalchemy
        print("✅ SQLAlchemy import OK")
    except ImportError as e:
        print(f"❌ SQLAlchemy not installed: {e}")
        print("💡 Install with: pip install sqlalchemy")
        return
    
    # Test 4: Backend main app
    print("\n4. Testing backend main app...")
    try:
        from backend.main import app
        print("✅ Backend main app OK")
    except Exception as e:
        print(f"❌ Backend main app failed: {e}")
        return
    
    # Test 5: Database models
    print("\n5. Testing database models...")
    try:
        from backend.models.database import Base, get_db
        print("✅ Database models OK")
    except Exception as e:
        print(f"❌ Database models failed: {e}")
        return
    
    # Test 6: User model
    print("\n6. Testing user model...")
    try:
        from backend.models.user import User
        print("✅ User model OK")
    except Exception as e:
        print(f"❌ User model failed: {e}")
        return
    
    # Test 7: Content models
    print("\n7. Testing content models...")
    try:
        from backend.models.content import Project, ContentPiece, ContentVersion
        print("✅ Content models OK")
    except Exception as e:
        print(f"❌ Content models failed: {e}")
        return
    
    # Test 8: Auth modules
    print("\n8. Testing auth modules...")
    try:
        from backend.auth import JWTHandler, get_current_active_user
        print("✅ Auth modules OK")
    except Exception as e:
        print(f"❌ Auth modules failed: {e}")
        return
    
    # Test 9: AI components
    print("\n9. Testing AI components...")
    try:
        from backend.core.content_generator import ContentGenerator
        print("✅ Content generator OK")
    except Exception as e:
        print(f"❌ Content generator failed: {e}")
        return
    
    try:
        from backend.core.style_refiner import StyleRefiner
        print("✅ Style refiner OK")
    except Exception as e:
        print(f"❌ Style refiner failed: {e}")
        return
    
    try:
        from backend.core.seo_optimizer import SEOOptimizer
        print("✅ SEO optimizer OK")
    except Exception as e:
        print(f"❌ SEO optimizer failed: {e}")
        return
    
    try:
        from backend.core.plagiarism_checker import PlagiarismChecker
        print("✅ Plagiarism checker OK")
    except Exception as e:
        print(f"❌ Plagiarism checker failed: {e}")
        return
    
    # Test 10: AWS and AI models
    print("\n10. Testing AWS and AI models...")
    try:
        from backend.core.aws_config import aws_config
        print("✅ AWS config OK")
    except Exception as e:
        print(f"❌ AWS config failed: {e}")
        return
    
    try:
        from backend.core.ai_models import AIModelManager
        print("✅ AI models OK")
    except Exception as e:
        print(f"❌ AI models failed: {e}")
        return
    
    print("\n🎉 All imports successful!")

def check_missing_dependencies():
    """Check for missing dependencies"""
    print("\n📦 Checking for missing dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "python-jose",
        "passlib",
        "bcrypt",
        "boto3",
        "transformers",
        "torch",
        "openai",
        "spacy",
        "nltk"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("💡 Install with: pip install -r requirements.txt")
    else:
        print("\n✅ All required packages are installed!")

def main():
    """Run debug tests"""
    print("🚀 Debug Import Issues")
    print("=" * 50)
    
    debug_imports()
    check_missing_dependencies()
    
    print("\n" + "=" * 50)
    print("📋 Next Steps:")
    print("1. If dependencies are missing: pip install -r requirements.txt")
    print("2. If imports still fail: Check the specific error messages above")
    print("3. Run simple test: python simple_test.py")

if __name__ == "__main__":
    main() 