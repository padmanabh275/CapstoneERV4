#!/usr/bin/env python3
"""
Test JWT Configuration
"""
import os
import sys
from datetime import datetime, timedelta

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.auth.jwt_handler import JWTHandler
    print("✅ JWT Handler imported successfully")
except ImportError as e:
    print(f"❌ Failed to import JWT Handler: {e}")
    sys.exit(1)

def test_jwt_configuration():
    """Test JWT configuration and functionality"""
    print("\n🔐 Testing JWT Configuration...")
    
    # Test 1: Check environment variables
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")
    expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    
    print(f"📋 Configuration:")
    print(f"   SECRET_KEY: {'✅ Set' if secret_key else '❌ Not set'}")
    print(f"   ALGORITHM: {algorithm}")
    print(f"   ACCESS_TOKEN_EXPIRE_MINUTES: {expire_minutes}")
    
    if not secret_key:
        print("⚠️  Warning: SECRET_KEY not set. Using default.")
    
    # Test 2: Create a test token
    try:
        test_data = {"sub": "testuser", "username": "testuser"}
        token = JWTHandler.create_access_token(test_data)
        print(f"✅ Token created successfully: {token[:50]}...")
        
        # Test 3: Verify the token
        payload = JWTHandler.verify_token(token)
        print(f"✅ Token verified successfully")
        print(f"   Payload: {payload}")
        
        # Test 4: Test password hashing
        test_password = "testpassword123"
        hashed = JWTHandler.hash_password(test_password)
        print(f"✅ Password hashed successfully")
        
        # Test 5: Test password verification
        is_valid = JWTHandler.verify_password(test_password, hashed)
        print(f"✅ Password verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        print("\n🎉 All JWT tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ JWT test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_jwt_configuration()
    sys.exit(0 if success else 1) 