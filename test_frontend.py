#!/usr/bin/env python3
"""
Frontend Test Script
Test the React frontend functionality
"""

import subprocess
import sys
import os
import time
import requests

def check_node_installed():
    """Check if Node.js is installed"""
    print("🔍 Checking Node.js installation...")
    try:
        result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except Exception:
        print("❌ Node.js not found")
        return False

def check_npm_installed():
    """Check if npm is installed"""
    print("🔍 Checking npm installation...")
    try:
        result = subprocess.run("npm --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm version: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except Exception:
        print("❌ npm not found")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return False
    
    try:
        result = subprocess.run("npm install", shell=True, cwd=frontend_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend dependencies installed")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_frontend_build():
    """Test if frontend can be built"""
    print("🏗️  Testing frontend build...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    try:
        result = subprocess.run("npm run build", shell=True, cwd=frontend_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend build successful")
            return True
        else:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Frontend build failed: {e}")
        return False

def test_backend_connection():
    """Test if frontend can connect to backend"""
    print("🔗 Testing backend connection...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend connection successful")
            return True
        else:
            print(f"❌ Backend connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def start_frontend_dev_server():
    """Start the frontend development server"""
    print("🚀 Starting frontend development server...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("🔗 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop the frontend server")
    print("=" * 60)
    
    try:
        subprocess.run("npm start", shell=True, cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main test function"""
    print("🎨 AI-Assisted Content Creation Platform - Frontend Test")
    print("=" * 60)
    
    # Check prerequisites
    if not check_node_installed():
        print("\n❌ Node.js is required but not installed")
        print("💡 Please install Node.js from: https://nodejs.org/")
        return 1
    
    if not check_npm_installed():
        print("\n❌ npm is required but not installed")
        print("💡 Please install npm (usually comes with Node.js)")
        return 1
    
    # Test backend connection
    if not test_backend_connection():
        print("\n❌ Backend is not running")
        print("💡 Please start the backend first:")
        print("   cd smart_assistant && python start_backend.py")
        return 1
    
    # Install dependencies
    if not install_frontend_dependencies():
        print("\n❌ Failed to install frontend dependencies")
        return 1
    
    # Test build
    if not test_frontend_build():
        print("\n❌ Frontend build failed")
        return 1
    
    print("\n🎉 Frontend test passed!")
    print("\n📋 Starting development server...")
    
    # Start development server
    start_frontend_dev_server()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 