#!/usr/bin/env python3
"""
Simple Component Test - AI-Assisted Content Creation Platform
This script performs basic tests without requiring external dependencies.
"""

import os
import sys
from pathlib import Path

def test_file_existence():
    """Test if all required files exist"""
    print("🔍 Testing File Existence...")
    
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
        "frontend/tailwind.config.js",
        "frontend/src/App.tsx",
        "frontend/src/contexts/AuthContext.tsx",
        "frontend/src/services/api.ts",
        "requirements.txt",
        "setup.py",
        "README.md"
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} files:")
        for file in missing:
            print(f"   - {file}")
        return False
    
    print("✅ All required files exist!")
    return True

def test_directory_structure():
    """Test directory structure"""
    print("\n📁 Testing Directory Structure...")
    
    required_dirs = [
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
    
    missing = []
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")
            missing.append(dir_path)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} directories:")
        for dir in missing:
            print(f"   - {dir}/")
        return False
    
    print("✅ All required directories exist!")
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
        except SyntaxError as e:
            print(f"❌ {file_path} - Syntax Error: {e}")
            errors.append(f"{file_path}: {e}")
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            errors.append(f"{file_path}: {e}")
    
    if errors:
        print(f"\n⚠️  Found {len(errors)} syntax errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ All Python files have valid syntax!")
    return True

def test_configuration_files():
    """Test configuration files"""
    print("\n⚙️  Testing Configuration Files...")
    
    config_files = [
        "requirements.txt",
        "requirements-minimal.txt", 
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
    """Run all tests"""
    print("🚀 AI-Assisted Content Creation Platform - Simple Component Test")
    print("=" * 70)
    
    tests = [
        ("File Existence", test_file_existence),
        ("Directory Structure", test_directory_structure), 
        ("Python Syntax", test_python_syntax),
        ("Configuration Files", test_configuration_files)
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
        print("🎉 All components are structurally correct!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start backend: python -m uvicorn backend.main:app --reload")
        print("3. Start frontend: cd frontend && npm start")
        print("\n💡 For detailed testing, run: python test_components.py")
    else:
        print("⚠️  Some components need attention")
        print("💡 Check the errors above and fix missing files")
        print("\n📚 See component_status.md for detailed status")

if __name__ == "__main__":
    main() 