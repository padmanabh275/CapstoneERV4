#!/usr/bin/env python3
"""
Start Frontend Server
Script to set up and start the React frontend
"""

import subprocess
import sys
import os

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

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
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    print(f"📦 Installing frontend dependencies in {frontend_dir}...")
    
    # Install dependencies
    if not run_command("npm install", "Installing npm dependencies", cwd=frontend_dir):
        return False
    
    return True

def start_frontend():
    """Start the frontend development server"""
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    print("🚀 Starting React frontend...")
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("🔗 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop the frontend server")
    print("=" * 60)
    
    try:
        # Start the development server
        subprocess.run("npm start", shell=True, cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main function to set up and start frontend"""
    print("🎨 AI-Assisted Content Creation Platform - Frontend Setup")
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
    
    # Install dependencies
    if not install_frontend_dependencies():
        print("\n❌ Failed to install frontend dependencies")
        return 1
    
    # Start frontend
    start_frontend()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 