#!/usr/bin/env python3
"""
Quick Component Test for AI-Assisted Content Creation Platform
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """Test basic imports without dependencies"""
    print("🧪 Testing Basic Imports...")
    
    try:
        # Test if we can import basic Python modules
        import json
        import logging
        print("✅ Basic Python modules imported")
        
        # Test if we can import FastAPI
        import fastapi
        print("✅ FastAPI imported")
        
        # Test if we can import SQLAlchemy
        import sqlalchemy
        print("✅ SQLAlchemy imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        "backend/main.py",
        "backend/models/database.py",
        "backend/models/user.py",
        "backend/models/content.py",
        "backend/auth/jwt_handler.py",
        "backend/auth/dependencies.py",
        "backend/core/content_generator.py",
        "backend/core/style_refiner.py",
        "backend/core/seo_optimizer.py",
        "backend/core/plagiarism_checker.py",
        "backend/core/ai_models.py",
        "backend/core/aws_config.py",
        "frontend/package.json",
        "requirements.txt",
        "setup.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files")
        return False
    
    print("✅ All required files exist")
    return True

def test_backend_structure():
    """Test backend module structure"""
    print("\n🧪 Testing Backend Structure...")
    
    try:
        # Test if we can import the main app
        sys.path.insert(0, os.getcwd())
        
        # Test basic imports
        from backend.main import app
        print("✅ FastAPI app imported")
        
        # Test database models
        from backend.models.database import Base, get_db
        print("✅ Database models imported")
        
        # Test auth modules
        from backend.auth import JWTHandler, get_current_active_user
        print("✅ Auth modules imported")
        
        # Test AI components
        from backend.core.content_generator import ContentGenerator
        from backend.core.style_refiner import StyleRefiner
        from backend.core.seo_optimizer import SEOOptimizer
        from backend.core.plagiarism_checker import PlagiarismChecker
        print("✅ AI components imported")
        
        # Test AWS and AI models
        from backend.core.aws_config import aws_config
        from backend.core.ai_models import AIModelManager
        print("✅ AWS and AI models imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend_structure():
    """Test frontend structure"""
    print("\n🧪 Testing Frontend Structure...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    required_files = [
        "package.json",
        "tailwind.config.js",
        "src/App.tsx",
        "src/contexts/AuthContext.tsx",
        "src/services/api.ts"
    ]
    
    for file_path in required_files:
        if (frontend_dir / file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            return False
    
    print("✅ Frontend structure complete")
    return True

def main():
    """Run quick tests"""
    print("🚀 Quick Component Test")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("File Structure", test_file_structure),
        ("Backend Structure", test_backend_structure),
        ("Frontend Structure", test_frontend_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 QUICK TEST RESULTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All components are ready!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start backend: python -m uvicorn backend.main:app --reload")
        print("3. Start frontend: cd frontend && npm start")
    else:
        print("⚠️  Some components need attention")
        print("💡 Check the errors above and fix missing files")

if __name__ == "__main__":
    main() 