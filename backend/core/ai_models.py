import os
import json
import logging
from typing import Dict, Any, Optional, List
import openai
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from .aws_config import aws_config

logger = logging.getLogger(__name__)

class AIModelManager:
    def __init__(self):
        self.openai_client = None
        self.huggingface_models = {}
        self.sagemaker_endpoints = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI model clients"""
        # Initialize OpenAI client
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            openai.api_key = openai_api_key
            self.openai_client = openai
            logger.info("OpenAI client initialized")
        
        # Initialize Hugging Face models
        self._load_huggingface_models()
        
        # Initialize SageMaker endpoints
        self._load_sagemaker_endpoints()
    
    def _load_huggingface_models(self):
        """Load Hugging Face models for local inference"""
        try:
            # Load text generation model
            model_name = os.getenv('HF_MODEL_NAME', 'gpt2')
            self.huggingface_models['text_generation'] = pipeline(
                'text-generation',
                model=model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info(f"Loaded Hugging Face model: {model_name}")
        except Exception as e:
            logger.warning(f"Failed to load Hugging Face models: {str(e)}")
    
    def _load_sagemaker_endpoints(self):
        """Load available SageMaker endpoints"""
        try:
            endpoints = aws_config.get_sagemaker_endpoints()
            for endpoint in endpoints:
                self.sagemaker_endpoints[endpoint['EndpointName']] = endpoint
            logger.info(f"Loaded {len(self.sagemaker_endpoints)} SageMaker endpoints")
        except Exception as e:
            logger.warning(f"Failed to load SageMaker endpoints: {str(e)}")
    
    def generate_text_openai(self, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1000) -> Optional[str]:
        """Generate text using OpenAI API"""
        if not self.openai_client:
            logger.error("OpenAI client not initialized")
            return None
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that generates high-quality content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None
    
    def generate_text_huggingface(self, prompt: str, max_length: int = 1000) -> Optional[str]:
        """Generate text using Hugging Face models"""
        if 'text_generation' not in self.huggingface_models:
            logger.error("Hugging Face text generation model not loaded")
            return None
        
        try:
            result = self.huggingface_models['text_generation'](
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            return result[0]['generated_text']
        except Exception as e:
            logger.error(f"Hugging Face generation error: {str(e)}")
            return None
    
    def generate_text_sagemaker(self, prompt: str, endpoint_name: str) -> Optional[str]:
        """Generate text using SageMaker endpoint"""
        if endpoint_name not in self.sagemaker_endpoints:
            logger.error(f"SageMaker endpoint {endpoint_name} not found")
            return None
        
        try:
            payload = {
                "prompt": prompt,
                "max_length": 1000,
                "temperature": 0.7
            }
            
            response = aws_config.invoke_sagemaker_endpoint(endpoint_name, payload)
            if response:
                return response.get('generated_text', '')
            return None
        except Exception as e:
            logger.error(f"SageMaker API error: {str(e)}")
            return None
    
    def generate_content(self, prompt: str, content_type: str, **kwargs) -> Optional[str]:
        """Generate content using the best available AI model"""
        # Try OpenAI first (if available)
        if self.openai_client:
            result = self.generate_text_openai(prompt, **kwargs)
            if result:
                return result
        
        # Try SageMaker endpoints
        for endpoint_name in self.sagemaker_endpoints:
            result = self.generate_text_sagemaker(prompt, endpoint_name)
            if result:
                return result
        
        # Fallback to Hugging Face
        if self.huggingface_models:
            result = self.generate_text_huggingface(prompt, **kwargs)
            if result:
                return result
        
        logger.error("No AI models available for text generation")
        return None
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            # Use OpenAI for sentiment analysis if available
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Analyze the sentiment of the following text and return a JSON with 'sentiment' (positive/negative/neutral) and 'confidence' (0-1)."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=100
                )
                return json.loads(response.choices[0].message.content)
            
            # Fallback to simple keyword-based analysis
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                return {"sentiment": "positive", "confidence": 0.7}
            elif negative_count > positive_count:
                return {"sentiment": "negative", "confidence": 0.7}
            else:
                return {"sentiment": "neutral", "confidence": 0.5}
                
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return {"sentiment": "neutral", "confidence": 0.5}
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        try:
            # Use OpenAI for keyword extraction if available
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Extract the most important keywords from the following text and return them as a JSON array."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=100
                )
                return json.loads(response.choices[0].message.content)
            
            # Fallback to simple keyword extraction
            import re
            words = re.findall(r'\b\w+\b', text.lower())
            # Remove common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            keywords = [word for word in words if word not in stop_words and len(word) > 3]
            return list(set(keywords))[:10]
            
        except Exception as e:
            logger.error(f"Keyword extraction error: {str(e)}")
            return []
    
    def summarize_text(self, text: str, max_length: int = 150) -> Optional[str]:
        """Summarize text"""
        try:
            if self.openai_client:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"Summarize the following text in {max_length} characters or less:"},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=max_length
                )
                return response.choices[0].message.content
            
            # Fallback to simple summarization
            sentences = text.split('.')
            if len(sentences) <= 2:
                return text
            
            # Take first and last sentence
            summary = sentences[0] + '. ' + sentences[-1] + '.'
            return summary[:max_length]
            
        except Exception as e:
            logger.error(f"Text summarization error: {str(e)}")
            return None

# Global AI model manager instance
ai_model_manager = AIModelManager() 