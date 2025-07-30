#!/usr/bin/env python3
"""
Dependency Installation Script
Installs dependencies step by step with error handling.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def install_core_dependencies():
    """Install core dependencies"""
    print("📦 Installing Core Dependencies...")
    
    # Core web framework
    if not run_command("pip install fastapi uvicorn", "Installing FastAPI and Uvicorn"):
        return False
    
    # Database
    if not run_command("pip install sqlalchemy", "Installing SQLAlchemy"):
        return False
    
    # Authentication
    if not run_command("pip install python-jose[cryptography] passlib[bcrypt] bcrypt", "Installing authentication packages"):
        return False
    
    # HTTP client
    if not run_command("pip install requests httpx", "Installing HTTP clients"):
        return False
    
    # Utilities
    if not run_command("pip install python-dotenv pydantic", "Installing utilities"):
        return False
    
    # Development
    if not run_command("pip install pytest", "Installing pytest"):
        return False
    
    return True

def install_optional_dependencies():
    """Install optional dependencies"""
    print("\n📦 Installing Optional Dependencies...")
    
    # PostgreSQL adapter (optional - can use SQLite instead)
    print("🔄 Installing PostgreSQL adapter...")
    if not run_command("pip install psycopg2-binary", "Installing PostgreSQL adapter"):
        print("⚠️  PostgreSQL adapter failed - will use SQLite instead")
    
    # AWS SDK
    print("🔄 Installing AWS SDK...")
    if not run_command("pip install boto3", "Installing AWS SDK"):
        print("⚠️  AWS SDK failed - AWS features will be disabled")
    
    # NLP libraries (optional)
    print("🔄 Installing NLP libraries...")
    if not run_command("pip install spacy nltk", "Installing NLP libraries"):
        print("⚠️  NLP libraries failed - some AI features will be limited")
    
    return True

def test_imports():
    """Test if core imports work"""
    print("\n🧪 Testing Core Imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError:
        print("❌ FastAPI import failed")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError:
        print("❌ Uvicorn import failed")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError:
        print("❌ SQLAlchemy import failed")
        return False
    
    try:
        import jwt
        print("✅ JWT imported successfully")
    except ImportError:
        print("❌ JWT import failed")
        return False
    
    print("✅ All core imports successful!")
    return True

def main():
    """Main installation function"""
    print("🚀 AI-Assisted Content Creation Platform - Dependency Installation")
    print("=" * 70)
    
    # Install core dependencies
    if not install_core_dependencies():
        print("❌ Core dependency installation failed")
        sys.exit(1)
    
    # Install optional dependencies
    install_optional_dependencies()
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🎉 Dependency Installation Complete!")
    print("=" * 70)
    print("\n📋 Next steps:")
    print("1. Test backend: python debug_imports.py")
    print("2. Start backend: python -m uvicorn backend.main:app --reload")
    print("3. Access API docs: http://localhost:8000/docs")
    print("\n💡 If you encounter issues:")
    print("   - Check TROUBLESHOOTING.md")
    print("   - Try: pip install --upgrade pip")
    print("   - Use virtual environment if needed")

if __name__ == "__main__":
    main() 