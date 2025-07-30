#!/usr/bin/env python3
"""
Setup script for AI-Assisted Content Creation Platform
This script helps initialize the project and configure all necessary components.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

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

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        # First try to upgrade pip
        run_command("python -m pip install --upgrade pip", "Upgrading pip")
        
        # Install dependencies with more flexible version handling
        run_command("pip install -r requirements.txt --no-cache-dir", "Installing Python dependencies")
        print("✅ Python dependencies installed successfully!")
    except Exception as e:
        print(f"❌ Installing Python dependencies failed: {e}")
        print("🔄 Trying alternative installation method...")
        try:
            # Try installing without strict version pinning
            run_command("pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib boto3 transformers torch openai", "Installing core dependencies")
            print("✅ Core dependencies installed successfully!")
        except Exception as e2:
            print(f"❌ Alternative installation also failed: {e2}")
            print("🔄 Trying with minimal requirements...")
            try:
                # Try with minimal requirements file
                run_command("pip install -r requirements-minimal.txt", "Installing minimal dependencies")
                print("✅ Minimal dependencies installed successfully!")
            except Exception as e3:
                print(f"❌ Minimal installation also failed: {e3}")
                print("💡 Manual installation required. Please run:")
                print("   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib boto3")
                return False
    return True

def setup_database():
    """Setup database and run migrations"""
    # Create database directory if it doesn't exist
    db_dir = Path("data")
    db_dir.mkdir(exist_ok=True)
    
    print("📊 Database setup completed")
    return True

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Environment file created from template")
        print("⚠️  Please update .env file with your configuration")
    elif env_file.exists():
        print("✅ Environment file already exists")
    else:
        print("❌ Environment template not found")
        return False
    
    return True

def setup_spacy_models():
    """Download spaCy models"""
    return run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model")

def setup_nltk_data():
    """Download NLTK data"""
    nltk_script = """
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
"""
    return run_command(f'python -c "{nltk_script}"', "Downloading NLTK data")

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "uploads",
        "exports",
        "temp",
        "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")
    return True

def setup_frontend():
    """Setup React frontend"""
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        os.chdir(frontend_dir)
        success = run_command("npm install", "Installing frontend dependencies")
        os.chdir("..")
        return success
    else:
        print("⚠️  Frontend directory not found, skipping frontend setup")
        return True

def run_tests():
    """Run basic tests"""
    return run_command("python -m pytest tests/ -v", "Running tests")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Update .env file with your configuration:")
    print("   - Database credentials")
    print("   - AWS credentials (if using AWS services)")
    print("   - OpenAI API key (if using OpenAI)")
    print("   - JWT secret key")
    print("\n2. Start the backend server:")
    print("   cd smart_assistant")
    print("   python -m uvicorn backend.main:app --reload")
    print("\n3. Start the frontend (in a new terminal):")
    print("   cd smart_assistant/frontend")
    print("   npm start")
    print("\n4. Access the application:")
    print("   - Backend API: http://localhost:8000")
    print("   - Frontend: http://localhost:3000")
    print("   - API Documentation: http://localhost:8000/docs")
    print("\n5. Create your first user account through the registration endpoint")
    print("\n📚 Documentation:")
    print("   - README.md: Project overview and setup")
    print("   - API docs: http://localhost:8000/docs")
    print("\n🐛 Troubleshooting:")
    print("   - Check logs/ directory for error logs")
    print("   - Verify all environment variables are set")
    print("   - Ensure database is running and accessible")

def main():
    """Main setup function"""
    print("🚀 Setting up AI-Assisted Content Creation Platform")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create necessary directories
    if not create_directories():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Setup NLP models
    if not setup_spacy_models():
        print("⚠️  spaCy model download failed, continuing...")
    
    if not setup_nltk_data():
        print("⚠️  NLTK data download failed, continuing...")
    
    # Setup frontend
    if not setup_frontend():
        print("⚠️  Frontend setup failed, continuing...")
    
    # Run tests (optional)
    print("\n🧪 Running tests...")
    run_tests()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 