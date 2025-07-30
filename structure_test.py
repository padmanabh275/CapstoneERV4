#!/usr/bin/env python3
"""
Structure Test - No Dependencies Required
Tests only file structure and basic Python syntax.
"""

import os
import sys
from pathlib import Path

def test_structure():
    """Test project structure"""
    print("🏗️  Testing Project Structure...")
    
    # Test directories
    dirs = [
        "backend",
        "backend/models",
        "backend/auth", 
        "backend/core",
        "frontend",
        "frontend/src",
        "frontend/src/contexts",
        "frontend/src/services",
        "logs",
        "uploads",
        "exports",
        "temp",
        "data"
    ]
    
    missing_dirs = []
    for dir_path in dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")
            missing_dirs.append(dir_path)
    
    # Test critical files
    files = [
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
        "frontend/tailwind.config.js",
        "frontend/src/App.tsx",
        "frontend/src/contexts/AuthContext.tsx",
        "frontend/src/services/api.ts",
        "requirements.txt",
        "setup.py",
        "README.md"
    ]
    
    missing_files = []
    for file_path in files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_dirs or missing_files:
        print(f"\n⚠️  Missing {len(missing_dirs)} directories and {len(missing_files)} files")
        return False
    
    print("✅ All required structure exists!")
    return True

def test_python_syntax():
    """Test Python syntax without importing"""
    print("\n🐍 Testing Python Syntax...")
    
    python_files = [
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
        "setup.py"
    ]
    
    errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, file_path, 'exec')
            print(f"✅ {file_path}")
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            errors.append(f"{file_path}: {e}")
    
    if errors:
        print(f"\n⚠️  Found {len(errors)} syntax errors")
        return False
    
    print("✅ All Python files have valid syntax!")
    return True

def test_config_files():
    """Test configuration files"""
    print("\n⚙️  Testing Configuration Files...")
    
    config_files = [
        "requirements.txt",
        "requirements-minimal.txt",
        "requirements-simple.txt",
        "env.example",
        "docker-compose.yml",
        "Dockerfile",
        "frontend/package.json",
        "frontend/tailwind.config.js"
    ]
    
    for file_path in config_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            return False
    
    print("✅ All configuration files exist!")
    return True

def main():
    """Run structure tests"""
    print("🚀 AI-Assisted Content Creation Platform - Structure Test")
    print("=" * 60)
    
    tests = [
        ("Project Structure", test_structure),
        ("Python Syntax", test_python_syntax),
        ("Configuration Files", test_config_files)
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
    print("\n" + "=" * 60)
    print("📊 STRUCTURE TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All structure tests passed!")
        print("\n📋 Next steps:")
        print("1. Try installing dependencies: pip install -r requirements-simple.txt")
        print("2. If that fails: pip install fastapi uvicorn sqlalchemy")
        print("3. Start backend: python -m uvicorn backend.main:app --reload")
    else:
        print("⚠️  Some structure issues found")
        print("💡 Check the errors above")

if __name__ == "__main__":
    main() 