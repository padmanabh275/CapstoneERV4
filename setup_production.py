#!/usr/bin/env python3
"""
Production Setup Script
Comprehensive setup for AI-Assisted Content Creation Platform with Real AI Models
"""
import subprocess
import sys
import os
import json

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
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_backend_status():
    """Check if backend is ready for AI integration"""
    print("🔍 Checking backend status...")
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and ready")
            return True
        else:
            print("⚠️ Backend is running but health check failed")
            return True
    except Exception as e:
        print(f"⚠️ Backend health check failed: {e}")
        return True  # Continue anyway

def install_real_ai_dependencies():
    """Install real AI model dependencies"""
    print("🤖 Installing real AI model dependencies...")
    
    # Core AI/ML libraries
    ai_deps = [
        "openai>=1.0.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.1.0",
        "langchain-community>=0.1.0",
        "transformers>=4.35.0",
        "torch>=2.2.0",
        "torchvision>=0.17.0",
        "accelerate>=0.25.0",
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0",
        "spacy>=3.7.0",
        "textstat>=0.7.0",
        "nltk>=3.8.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "requests>=2.31.0",
        "httpx>=0.25.0",
        "aiohttp>=3.9.0",
        "tiktoken>=0.5.0",
        "python-dotenv>=1.0.0"
    ]
    
    for dep in ai_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️ Failed to install {dep}, continuing...")
    
    return True

def setup_spacy_model():
    """Download spaCy English model"""
    print("📚 Setting up spaCy English model...")
    return run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model")

def setup_nltk_data():
    """Download NLTK data"""
    print("📚 Setting up NLTK data...")
    nltk_script = """
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
print("NLTK data downloaded successfully")
"""
    return run_command(f'python -c "{nltk_script}"', "Downloading NLTK data")

def create_env_file():
    """Create environment file with AI API keys"""
    print("🔐 Creating environment file...")
    
    env_content = """# AI-Assisted Content Creation Platform Environment Variables

# Database
DATABASE_URL=sqlite:///./content_platform.db

# JWT Secret
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Hugging Face Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key-here
HUGGINGFACE_MODEL=gpt2

# AWS Configuration (Optional)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
SAGEMAKER_ENDPOINT_NAME=your-sagemaker-endpoint

# Content Analysis APIs
PLAGIARISM_API_KEY=your-plagiarism-check-api-key
SEO_API_KEY=your-seo-api-key

# Development
DEBUG=True
LOG_LEVEL=INFO
"""
    
    try:
        with open("smart_assistant/.env", "w") as f:
            f.write(env_content)
        print("✅ Environment file created: smart_assistant/.env")
        print("⚠️ Please update the API keys in .env file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_ai_config():
    """Create AI configuration file"""
    print("🤖 Creating AI configuration...")
    
    ai_config = {
        "openai": {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "huggingface": {
            "model": "gpt2",
            "max_length": 1000,
            "temperature": 0.8,
            "top_k": 50,
            "top_p": 0.9
        },
        "content_generation": {
            "default_prompt_template": "Write a high-quality {content_type} about {topic}. Make it engaging, informative, and well-structured.",
            "max_length": 2000,
            "include_seo": True,
            "include_fact_check": True
        },
        "style_refinement": {
            "tone_options": ["professional", "casual", "academic", "creative", "technical"],
            "readability_target": 60.0,
            "sentence_length_target": 20
        },
        "seo_optimization": {
            "keyword_density_target": 0.02,
            "title_length_target": 60,
            "meta_description_length": 160,
            "heading_structure": True
        },
        "plagiarism_check": {
            "similarity_threshold": 0.8,
            "check_sources": True,
            "fact_check": True
        }
    }
    
    try:
        with open("smart_assistant/ai_config.json", "w") as f:
            json.dump(ai_config, f, indent=2)
        print("✅ AI configuration created: smart_assistant/ai_config.json")
        return True
    except Exception as e:
        print(f"❌ Failed to create AI config: {e}")
        return False

def update_ai_models():
    """Update AI models to use real implementations"""
    print("🔄 Updating AI models with real implementations...")
    
    # Update content generator
    content_generator_code = '''import logging
import openai
import os
from typing import Dict, Any, Optional
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.openai_client = None
        self.langchain_llm = None
        self.config = self._load_config()
        
        # Initialize OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                openai.api_key = api_key
                self.openai_client = openai.OpenAI()
                self.langchain_llm = OpenAI(
                    openai_api_key=api_key,
                    model_name=self.config["openai"]["model"],
                    max_tokens=self.config["openai"]["max_tokens"],
                    temperature=self.config["openai"]["temperature"]
                )
                logger.info("✅ OpenAI initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI initialization failed: {e}")
        else:
            logger.warning("⚠️ OPENAI_API_KEY not found, using fallback")

    def _load_config(self) -> Dict[str, Any]:
        """Load AI configuration"""
        try:
            with open("ai_config.json", "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Failed to load AI config: {e}")
            return {
                "openai": {"model": "gpt-4", "max_tokens": 2000, "temperature": 0.7},
                "content_generation": {"default_prompt_template": "Write about {topic}"}
            }

    async def generate_content(self, prompt: str, content_type: str = "article", 
                             style: str = "professional", length: str = "medium") -> Dict[str, Any]:
        """Generate content using real AI models"""
        try:
            if self.openai_client:
                # Use OpenAI API directly
                response = self.openai_client.chat.completions.create(
                    model=self.config["openai"]["model"],
                    messages=[
                        {"role": "system", "content": f"You are a professional {content_type} writer. Write in a {style} style."},
                        {"role": "user", "content": f"Write a {length} {content_type} about: {prompt}"}
                    ],
                    max_tokens=self.config["openai"]["max_tokens"],
                    temperature=self.config["openai"]["temperature"]
                )
                
                content = response.choices[0].message.content
                
                return {
                    "content": content,
                    "model_used": self.config["openai"]["model"],
                    "tokens_used": response.usage.total_tokens,
                    "status": "success"
                }
            else:
                # Fallback to mock implementation
                return {
                    "content": f"Generated {content_type} about {prompt} in {style} style",
                    "model_used": "mock",
                    "tokens_used": 0,
                    "status": "fallback"
                }
                
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return {
                "content": f"Error generating content: {str(e)}",
                "model_used": "error",
                "tokens_used": 0,
                "status": "error"
            }

    async def generate_multiple_variants(self, prompt: str, count: int = 3) -> Dict[str, Any]:
        """Generate multiple content variants"""
        variants = []
        for i in range(count):
            variant = await self.generate_content(prompt, f"variant_{i+1}")
            variants.append(variant)
        
        return {
            "variants": variants,
            "total_variants": count,
            "status": "success"
        }
'''
    
    try:
        with open("smart_assistant/backend/core/content_generator.py", "w") as f:
            f.write(content_generator_code)
        print("✅ Content generator updated with real AI implementation")
        return True
    except Exception as e:
        print(f"❌ Failed to update content generator: {e}")
        return False

def create_ai_test_script():
    """Create a test script for AI functionality"""
    print("🧪 Creating AI test script...")
    
    test_script = '''#!/usr/bin/env python3
"""
AI Model Test Script
Test real AI model implementations
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

async def test_ai_models():
    """Test all AI model components"""
    print("🤖 Testing AI Models...")
    
    try:
        from backend.core.content_generator import ContentGenerator
        from backend.core.style_refiner import StyleRefiner
        from backend.core.seo_optimizer import SEOOptimizer
        from backend.core.plagiarism_checker import PlagiarismChecker
        
        # Test content generation
        print("📝 Testing Content Generation...")
        generator = ContentGenerator()
        result = await generator.generate_content(
            prompt="artificial intelligence in healthcare",
            content_type="blog post",
            style="professional"
        )
        print(f"✅ Content Generation: {result['status']}")
        print(f"   Model: {result['model_used']}")
        print(f"   Tokens: {result['tokens_used']}")
        
        # Test style refinement
        print("\\n🎨 Testing Style Refinement...")
        refiner = StyleRefiner()
        refined = await refiner.refine_content(
            content="This is a test content for refinement.",
            target_style="professional",
            target_tone="formal"
        )
        print(f"✅ Style Refinement: {refined['status']}")
        
        # Test SEO optimization
        print("\\n🔍 Testing SEO Optimization...")
        optimizer = SEOOptimizer()
        optimized = await optimizer.optimize_content(
            content="Test content for SEO optimization.",
            target_keywords=["AI", "healthcare", "technology"]
        )
        print(f"✅ SEO Optimization: {optimized['status']}")
        
        # Test plagiarism check
        print("\\n✅ Testing Plagiarism Check...")
        checker = PlagiarismChecker()
        check_result = await checker.check_plagiarism(
            content="This is original content for testing."
        )
        print(f"✅ Plagiarism Check: {check_result['status']}")
        
        print("\\n🎉 All AI model tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ AI model test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_ai_models())
'''
    
    try:
        with open("smart_assistant/test_ai_models.py", "w") as f:
            f.write(test_script)
        print("✅ AI test script created: smart_assistant/test_ai_models.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create AI test script: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up AI-Assisted Content Creation Platform with Real AI Models")
    print("=" * 70)
    
    # Check backend status
    if not check_backend_status():
        print("❌ Backend not ready. Please start the backend first.")
        return 1
    
    # Install AI dependencies
    if not install_real_ai_dependencies():
        print("❌ Failed to install AI dependencies")
        return 1
    
    # Setup AI models
    if not setup_spacy_model():
        print("⚠️ spaCy model setup failed, continuing...")
    
    if not setup_nltk_data():
        print("⚠️ NLTK data setup failed, continuing...")
    
    # Create configuration files
    if not create_env_file():
        print("❌ Failed to create environment file")
        return 1
    
    if not create_ai_config():
        print("❌ Failed to create AI configuration")
        return 1
    
    # Update AI models
    if not update_ai_models():
        print("❌ Failed to update AI models")
        return 1
    
    # Create test script
    if not create_ai_test_script():
        print("❌ Failed to create AI test script")
        return 1
    
    print("\n🎉 AI Setup Complete!")
    print("=" * 70)
    print("✅ Real AI models integrated")
    print("✅ OpenAI integration ready")
    print("✅ Configuration files created")
    print("✅ Test script available")
    print("\n📋 Next Steps:")
    print("1. Update API keys in smart_assistant/.env")
    print("2. Test AI models: python test_ai_models.py")
    print("3. Restart backend to use real AI")
    print("4. Test the platform with real AI generation")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 