#!/usr/bin/env python3
"""
Start Backend Server
Simple script to start the backend with error handling
"""

import sys
import os
import uvicorn

def main():
    """Start the backend server"""
    print("🚀 Starting AI-Assisted Content Creation Platform Backend...")
    print("=" * 60)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Import the app
        print("📦 Importing backend app...")
        from backend.main import app
        print("✅ Backend app imported successfully")
        
        # Start the server
        print("🌐 Starting server on http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/")
        print("\n💡 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for now
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install fastapi uvicorn sqlalchemy python-jose[cryptography] bcrypt")
        return 1
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        print("💡 Check the error message above")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 