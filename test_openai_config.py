#!/usr/bin/env python3
"""
Test OpenAI Configuration
"""
import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")

def test_openai_configuration():
    """Test OpenAI configuration"""
    print("\n🤖 Testing OpenAI Configuration...")
    
    # Get OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    print(f"📋 Configuration:")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_api_key and openai_api_key != 'your-openai-api-key' else '❌ Not set'}")
    
    if not openai_api_key or openai_api_key == 'your-openai-api-key':
        print("\n❌ OpenAI API key not configured!")
        print("📝 To get your OpenAI API key:")
        print("   1. Go to https://platform.openai.com/")
        print("   2. Sign up/Login to your account")
        print("   3. Go to API Keys section")
        print("   4. Create a new API key")
        print("   5. Copy the key (starts with 'sk-')")
        print("   6. Update your .env file with the key")
        return False
    
    # Test if the key looks valid
    if not openai_api_key.startswith('sk-'):
        print("⚠️  Warning: API key doesn't start with 'sk-'. This might not be a valid OpenAI key.")
    
    print(f"✅ OpenAI API key configured: {openai_api_key[:10]}...")
    
    # Test OpenAI connection (optional - requires internet)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ OpenAI API connection successful!")
        print(f"   Response: {response.choices[0].message.content}")
        return True
        
    except ImportError:
        print("⚠️  OpenAI library not installed. Run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        print("   This might be due to:")
        print("   - Invalid API key")
        print("   - No internet connection")
        print("   - API rate limits")
        return False

if __name__ == "__main__":
    success = test_openai_configuration()
    sys.exit(0 if success else 1) 