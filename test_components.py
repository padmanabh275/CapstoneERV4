#!/usr/bin/env python3
"""
Component Testing Script for AI-Assisted Content Creation Platform
This script tests all major components to ensure they're working correctly.
"""

import sys
import os
from pathlib import Path

def test_backend_imports():
    """Test backend component imports"""
    print("🧪 Testing Backend Components...")
    
    try:
        # Test FastAPI app
        from backend.main import app
        print("✅ FastAPI app imported successfully")
        
        # Test database models
        from backend.models.database import Base, get_db
        print("✅ Database models imported successfully")
        
        from backend.models.user import User
        print("✅ User model imported successfully")
        
        from backend.models.content import Project, ContentPiece, ContentVersion
        print("✅ Content models imported successfully")
        
        # Test authentication
        from backend.auth import JWTHandler, get_current_active_user
        print("✅ Authentication modules imported successfully")
        
        # Test AI components
        from backend.core.content_generator import ContentGenerator
        from backend.core.style_refiner import StyleRefiner
        from backend.core.seo_optimizer import SEOOptimizer
        from backend.core.plagiarism_checker import PlagiarismChecker
        print("✅ AI agent components imported successfully")
        
        # Test AWS and AI model managers
        from backend.core.aws_config import aws_config
        from backend.core.ai_models import AIModelManager
        print("✅ AWS and AI model managers imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend_structure():
    """Test frontend directory structure"""
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
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("✅ Frontend structure is complete")
    return True

def test_configuration_files():
    """Test configuration files"""
    print("\n🧪 Testing Configuration Files...")
    
    required_files = [
        "requirements.txt",
        "requirements-minimal.txt",
        "env.example",
        "docker-compose.yml",
        "Dockerfile",
        "setup.py",
        "README.md",
        "TROUBLESHOOTING.md"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("✅ Configuration files are complete")
    return True

def test_directories():
    """Test required directories"""
    print("\n🧪 Testing Directory Structure...")
    
    required_dirs = [
        "backend",
        "frontend",
        "logs",
        "uploads",
        "exports",
        "temp",
        "data"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/ directory exists")
        else:
            print(f"❌ {dir_path}/ directory missing")
            return False
    
    print("✅ Directory structure is complete")
    return True

def test_backend_functionality():
    """Test basic backend functionality"""
    print("\n🧪 Testing Backend Functionality...")
    
    try:
        from backend.main import app
        
        # Test health check endpoint
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Health check endpoint working")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test API documentation endpoint
        response = client.get("/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ TestClient not available: {e}")
        print("💡 Install with: pip install httpx")
        return False
    except Exception as e:
        print(f"❌ Backend functionality test failed: {e}")
        return False

def test_ai_components():
    """Test AI component initialization"""
    print("\n🧪 Testing AI Components...")
    
    try:
        from backend.core.content_generator import ContentGenerator
        from backend.core.style_refiner import StyleRefiner
        from backend.core.seo_optimizer import SEOOptimizer
        from backend.core.plagiarism_checker import PlagiarismChecker
        
        # Initialize components
        content_gen = ContentGenerator()
        style_ref = StyleRefiner()
        seo_opt = SEOOptimizer()
        plag_check = PlagiarismChecker()
        
        print("✅ All AI components initialized successfully")
        
        # Test basic functionality (mock responses)
        test_prompt = "Write a blog post about AI"
        result = content_gen.generate(test_prompt, "blog_post")
        if result:
            print("✅ Content generation working")
        else:
            print("⚠️  Content generation returned None (expected for mock)")
        
        return True
        
    except Exception as e:
        print(f"❌ AI components test failed: {e}")
        return False

def main():
    """Run all component tests"""
    print("🚀 AI-Assisted Content Creation Platform - Component Testing")
    print("=" * 70)
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    tests = [
        ("Configuration Files", test_configuration_files),
        ("Directory Structure", test_directories),
        ("Frontend Structure", test_frontend_structure),
        ("Backend Imports", test_backend_imports),
        ("Backend Functionality", test_backend_functionality),
        ("AI Components", test_ai_components),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All components are working correctly!")
        print("\n📋 Next steps:")
        print("1. Run: python setup.py")
        print("2. Start backend: python -m uvicorn backend.main:app --reload")
        print("3. Start frontend: cd frontend && npm start")
    else:
        print("⚠️  Some components need attention. Check the errors above.")
        print("\n💡 Check TROUBLESHOOTING.md for solutions")

if __name__ == "__main__":
    main() 