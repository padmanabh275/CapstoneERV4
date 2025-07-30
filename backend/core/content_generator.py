import logging
import openai
import os
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.openai_client = None
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