import logging
import openai
import os
from typing import Dict, Any, Optional
import json
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

# Add debug logging for imports
try:
    import ollama
    logger.info("✅ Ollama package imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import ollama: {e}")
    ollama = None

class ContentGenerator:
    def __init__(self):
        logger.info("🚀 Initializing ContentGenerator...")
        
        self.openai_client = None
        self.anthropic_client = None
        self.google_client = None
        self.ollama_client = None
        
        self.config = self._load_config()
        
        # Initialize OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=api_key)
                logger.info("✅ OpenAI initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI initialization failed: {e}")
        else:
            logger.warning("⚠️ OPENAI_API_KEY not found, using fallback")
        
        # Initialize Anthropic (Claude)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                self.anthropic_client = anthropic_key
                logger.info("✅ Anthropic Claude initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Anthropic initialization failed: {e}")
        
        # Initialize Google (Gemini)
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            try:
                self.google_client = google_key
                logger.info("✅ Google Gemini initialized successfully")
            except Exception as e:
                logger.warning(f"⚠️ Google Gemini initialization failed: {e}")
        
        # Initialize Ollama with better error handling
        logger.info("🔧 Attempting to initialize Ollama...")
        if ollama is None:
            logger.warning("⚠️ Ollama package not available")
        else:
            try:
                # Test if Ollama is running
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    self.ollama_client = True
                    models = response.json()
                    logger.info("✅ Ollama initialized successfully")
                    logger.info(f"📋 Available models: {[model['name'] for model in models.get('models', [])]}")
                else:
                    logger.warning(f"⚠️ Ollama not responding (status: {response.status_code})")
            except requests.exceptions.ConnectionError:
                logger.warning("⚠️ Ollama service not running on localhost:11434")
            except Exception as e:
                logger.warning(f"⚠️ Ollama initialization failed: {e}")
        
        logger.info("🏁 ContentGenerator initialization complete")

    def _load_config(self) -> Dict[str, Any]:
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai_config.json")
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Failed to load AI config: {e}")
            return {
                "openai": {"model": "gpt-3.5-turbo", "max_tokens": 2000, "temperature": 0.7},
                "anthropic": {"model": "claude-3-sonnet-20240229", "max_tokens": 2000},
                "google": {"model": "gemini-pro", "max_tokens": 2000},
                "ollama": {"model": "llama3.2:latest", "max_tokens": 2000, "temperature": 0.7},  # Make sure this is here
                "content_generation": {"default_prompt_template": "Write about {topic}"}
            }

    # Add Ollama generation method
    async def _generate_with_ollama(self, prompt: str, content_type: str, style: str, length: str) -> Dict[str, Any]:
        """Generate content using Ollama (local AI)"""
        try:
            logger.info(f"🚀 Attempting Ollama generation with model: {self.config['ollama']['model']}")
            logger.info(f"📝 Prompt: {prompt}")
            
            # Use the correct Ollama API call
            response = ollama.chat(
                model=self.config["ollama"]["model"],
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate a {length} {content_type} in {style} style about: {prompt}"
                    }
                ],
                options={
                    "temperature": self.config["ollama"]["temperature"],
                    "num_predict": self.config["ollama"]["max_tokens"]
                }
            )
            
            logger.info(f"✅ Ollama response received: {type(response)}")
            logger.info(f"📄 Response content: {response}")
            
            # Extract content from response
            if 'message' in response and 'content' in response['message']:
                content = response['message']['content']
            else:
                # Fallback if response format is different
                content = str(response)
            
            return {
                "content": content,
                "model_used": f"ollama-{self.config['ollama']['model']}",
                "tokens_used": len(content.split()),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"❌ Ollama generation failed: {e}")
            logger.error(f"🔍 Error type: {type(e)}")
            logger.error(f"📋 Error details: {str(e)}")
            import traceback
            logger.error(f"📚 Full traceback: {traceback.format_exc()}")
            
            return {
                "content": f"Ollama generation failed: {str(e)}",
                "model_used": "ollama",
                "tokens_used": 0,
                "status": "error"
            }

    # Add these missing methods:

    async def _generate_with_openai(self, prompt: str, content_type: str, style: str, length: str) -> Dict[str, Any]:
        """Generate content using OpenAI"""
        try:
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
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return {
                "content": f"OpenAI generation failed: {str(e)}",
                "model_used": "openai",
                "tokens_used": 0,
                "status": "error"
            }

    async def _generate_with_claude(self, prompt: str, content_type: str, style: str, length: str) -> Dict[str, Any]:
        """Generate content using Claude (Anthropic)"""
        try:
            headers = {
                "x-api-key": self.anthropic_client,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.config["anthropic"]["model"],
                "max_tokens": self.config["anthropic"]["max_tokens"],
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate a {length} {content_type} in {style} style about: {prompt}"
                    }
                ]
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["content"][0]["text"]
                return {
                    "content": content,
                    "model_used": "claude-3",
                    "tokens_used": result.get("usage", {}).get("output_tokens", 0),
                    "status": "success"
                }
            else:
                raise Exception(f"Claude API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Claude generation failed: {e}")
            return {
                "content": f"Claude generation failed: {str(e)}",
                "model_used": "claude-3",
                "tokens_used": 0,
                "status": "error"
            }

    async def _generate_with_gemini(self, prompt: str, content_type: str, style: str, length: str) -> Dict[str, Any]:
        """Generate content using Google Gemini"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config['google']['model']}:generateContent"
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": f"Generate a {length} {content_type} in {style} style about: {prompt}"
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": self.config["google"]["max_tokens"],
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                f"{url}?key={self.google_client}",
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "content": content,
                    "model_used": "gemini-pro",
                    "tokens_used": result.get("usageMetadata", {}).get("totalTokenCount", 0),
                    "status": "success"
                }
            else:
                raise Exception(f"Gemini API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return {
                "content": f"Gemini generation failed: {str(e)}",
                "model_used": "gemini-pro",
                "tokens_used": 0,
                "status": "error"
            }

    def _generate_fallback_content(self, prompt: str, content_type: str, style: str, length: str) -> str:
        """Generate realistic fallback content when AI models are not available"""
        try:
            # Extract key information from the prompt
            lines = prompt.strip().split('\n')
            title = ""
            description = ""
            target_audience = ""
            keywords = []
            
            for line in lines:
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                elif line.startswith("Description:"):
                    description = line.replace("Description:", "").strip()
                elif line.startswith("Target Audience:"):
                    target_audience = line.replace("Target Audience:", "").strip()
                elif line.startswith("Keywords:"):
                    keywords_text = line.replace("Keywords:", "").strip()
                    if keywords_text != "None":
                        keywords = [k.strip() for k in keywords_text.split(',')]
            
            # Generate realistic content based on the parameters
            if content_type == "blog_post":
                content = f"""# {title}

{description}

## Introduction

In today's rapidly evolving business landscape, {title.lower()} has become a cornerstone of modern organizational success. This comprehensive guide explores the key aspects and implications for {target_audience.lower()}.

## Key Benefits

The implementation of {title.lower()} offers numerous advantages:

- **Enhanced Efficiency**: Streamlined processes and automated workflows
- **Improved Decision Making**: Data-driven insights and analytics
- **Cost Reduction**: Optimized resource allocation and reduced operational costs
- **Competitive Advantage**: Staying ahead in an increasingly digital marketplace

## Implementation Strategies

For {target_audience.lower()}, successful adoption requires:

1. **Strategic Planning**: Aligning technology with business objectives
2. **Change Management**: Ensuring smooth organizational transition
3. **Continuous Learning**: Staying updated with latest developments
4. **Performance Monitoring**: Tracking key metrics and outcomes

## Future Outlook

As technology continues to advance, {title.lower()} will play an even more critical role in shaping business success. Organizations that embrace these changes early will be best positioned for long-term growth and sustainability.

## Conclusion

{title} represents a fundamental shift in how businesses operate and compete. By understanding and leveraging these technologies, {target_audience.lower()} can unlock new opportunities and drive sustainable success.

*Keywords: {', '.join(keywords) if keywords else 'business, technology, innovation'}*
"""
            else:
                content = f"""# {title}

{description}

This {content_type} explores the critical aspects of {title.lower()} and its relevance for {target_audience.lower()}. Through detailed examination and expert insights, we provide comprehensive coverage of this important topic.

## Key Points

- Understanding the fundamentals of {title.lower()}
- Identifying opportunities for {target_audience.lower()}
- Implementing effective strategies and solutions
- Measuring success and optimizing performance

## Summary

{title} represents a significant opportunity for {target_audience.lower()} to enhance their capabilities and achieve competitive advantages. By embracing these developments, organizations can position themselves for long-term success and growth.

*Keywords: {', '.join(keywords) if keywords else 'strategy, implementation, success'}*
"""

            return content
            
        except Exception as e:
            logger.error(f"Fallback content generation failed: {e}")
            return f"Content generation is currently unavailable. Please try again later or contact support.\n\nRequested content: {title} ({content_type})"

    async def generate_content(self, prompt: str, content_type: str = "article", 
                             style: str = "professional", length: str = "medium",
                             preferred_model: str = "auto") -> Dict[str, Any]:
        """Generate content using multiple AI models with fallback"""
        
        # Try preferred model first
        if preferred_model != "auto":
            if preferred_model == "ollama" and self.ollama_client:
                result = await self._generate_with_ollama(prompt, content_type, style, length)
                if result["status"] == "success":
                    return result
            elif preferred_model == "openai" and self.openai_client:
                result = await self._generate_with_openai(prompt, content_type, style, length)
                if result["status"] == "success":
                    return result
            elif preferred_model == "claude" and self.anthropic_client:
                result = await self._generate_with_claude(prompt, content_type, style, length)
                if result["status"] == "success":
                    return result
            elif preferred_model == "gemini" and self.google_client:
                result = await self._generate_with_gemini(prompt, content_type, style, length)
                if result["status"] == "success":
                    return result
        
        # Fallback to available models in order (add Ollama first since it's free!)
        if self.ollama_client:  # Try Ollama first
            result = await self._generate_with_ollama(prompt, content_type, style, length)
            if result["status"] == "success":
                return result
        
        if self.openai_client:
            result = await self._generate_with_openai(prompt, content_type, style, length)
            if result["status"] == "success":
                return result
        
        if self.anthropic_client:
            result = await self._generate_with_claude(prompt, content_type, style, length)
            if result["status"] == "success":
                return result
        
        if self.google_client:
            result = await self._generate_with_gemini(prompt, content_type, style, length)
            if result["status"] == "success":
                return result
        
        # If all AI models fail, use fallback
        logger.warning("All AI models failed, using fallback")
        fallback_content = self._generate_fallback_content(prompt, content_type, style, length)
        return {
            "content": fallback_content,
            "model_used": "fallback",
            "tokens_used": 0,
            "status": "success"
        }

    async def generate_multiple_variants(self, prompt: str, count: int = 3, 
                                       models: list = None) -> Dict[str, Any]:
        """Generate multiple content variants using different models"""
        if models is None:
            models = ["ollama", "openai", "claude", "gemini"]
        
        variants = []
        for i, model in enumerate(models[:count]):
            try:
                variant = await self.generate_content(
                    prompt=prompt,
                    content_type="variant",
                    style="professional",
                    length="medium",
                    preferred_model=model
                )
                variants.append(variant)
            except Exception as e:
                logger.warning(f"Failed to generate variant with {model}: {e}")
        
        return {
            "variants": variants,
            "total_variants": len(variants),
            "status": "success" if variants else "error"
        } 