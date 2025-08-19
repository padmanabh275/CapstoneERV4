import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add debug logging for imports
print("🔍 Environment Variables Check:")
print(f"OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not Set'}")
print(f"ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not Set'}")
print(f"GOOGLE_API_KEY: {'✅ Set' if os.getenv('GOOGLE_API_KEY') else '❌ Not Set'}")

# Add Ollama debugging
print("\n🖥️ Ollama Integration Check:")
try:
    import ollama
    print("✅ Ollama package imported successfully")
    
    # Test Ollama connection
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama service is running")
            print(f"📋 Available models: {[model['name'] for model in models.get('models', [])]}")
        else:
            print(f"⚠️ Ollama service responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Ollama service not running on localhost:11434")
    except Exception as e:
        print(f"⚠️ Ollama connection test failed: {e}")
        
except ImportError as e:
    print(f"❌ Failed to import ollama: {e}")
    print("💡 Try running: pip install ollama")
except Exception as e:
    print(f"⚠️ Ollama check failed: {e}")

print("\n🚀 Starting FastAPI application...")

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from sqlalchemy.orm import Session
from datetime import datetime

# Import our content creation modules
from core.content_generator import ContentGenerator
from core.style_refiner import StyleRefiner
from core.seo_optimizer import SEOOptimizer
from core.plagiarism_checker import PlagiarismChecker

# Import database and auth modules
from models.database import get_db, engine, Base
from auth import JWTHandler
from models.user import User
from models.content import Content
from auth.dependencies import get_current_user

app = FastAPI(
    title="AI Content Creation Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize our agents
content_generator = ContentGenerator()
style_refiner = StyleRefiner()
seo_optimizer = SEOOptimizer()
plagiarism_checker = PlagiarismChecker()

# Pydantic models for API requests/responses
class ContentGenerationRequest(BaseModel):
    prompt: str
    tone: str = "professional"
    word_count: int = 500
    target_audience: str = "general"
    content_type: str = "blog_post"

class ContentGenerationResponse(BaseModel):
    generated_content: str
    word_count: int
    estimated_reading_time: int
    suggestions: List[str]

class ContentRefinementRequest(BaseModel):
    content: str
    style: str = "casual"
    length: str = "medium"
    target_audience: str = "general"

class ContentRefinementResponse(BaseModel):
    refined_content: str
    changes_made: List[str]
    readability_score: float

class SEOOptimizationRequest(BaseModel):
    content: str
    keywords: List[str]
    target_url: Optional[str] = None

class SEOOptimizationResponse(BaseModel):
    optimized_content: str
    keyword_density: dict
    seo_score: float
    suggestions: List[str]

class PlagiarismCheckRequest(BaseModel):
    content: str
    check_facts: bool = True

class PlagiarismCheckResponse(BaseModel):
    plagiarism_score: float
    fact_check_results: List[dict]
    originality_score: float
    recommendations: List[str]

# Authentication models
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    full_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# Pydantic models for API responses
class ContentRequest(BaseModel):
    title: str
    content_type: str
    description: str
    target_audience: str
    tone: str
    word_count: int
    keywords: Optional[List[str]] = []

class ContentResponse(BaseModel):
    id: str
    title: str
    content: str
    content_type: str
    user_id: str
    status: str
    word_count: int
    content_metadata: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

@app.get("/")
def health_check():
    return {
        "status": "AI-Assisted Content Creation Platform API is running.",
        "version": "1.0.0",
        "agents": ["content_generator", "style_refiner", "seo_optimizer", "plagiarism_checker"]
    }

# Authentication endpoints
@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(request: UserLogin, db: Session = Depends(get_db)):
    """User login endpoint"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not user.verify_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = JWTHandler.create_access_token(data={"sub": user.username})
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified
        }
    )

@app.post("/api/v1/auth/register", response_model=TokenResponse)
async def register(request: UserRegister, db: Session = Depends(get_db)):
    """User registration endpoint"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == request.email) | (User.username == request.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user
    user = User(
        email=request.email,
        username=request.username,
        full_name=request.full_name
    )
    user.set_password(request.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate access token
    access_token = JWTHandler.create_access_token(data={"sub": user.username})
    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified
        }
    )

@app.get("/api/v1/auth/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }

@app.put("/api/v1/auth/profile")
async def update_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    for field, value in profile_data.items():
        if hasattr(current_user, field) and field not in ['id', 'created_at', 'updated_at']:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }

@app.post("/api/v1/content/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate AI content based on user parameters"""
    try:
        # Extract parameters from request
        title = request.title
        content_type = request.content_type
        description = request.description
        target_audience = request.target_audience
        tone = request.tone
        word_count = request.word_count
        keywords = request.keywords
        
        # Initialize content generator
        content_generator = ContentGenerator()
        
        # Create a comprehensive prompt
        prompt = f"""
        Title: {title}
        Content Type: {content_type}
        Description: {description}
        Target Audience: {target_audience}
        Tone: {tone}
        Word Count: {word_count}
        Keywords: {', '.join(keywords) if keywords else 'None'}
        
        Please generate content based on these specifications.
        """
        
        # Generate content using AI
        result = await content_generator.generate_content(
            prompt=prompt,
            content_type=content_type,
            style=tone,
            length="long" if word_count > 1000 else "medium" if word_count > 500 else "short"
        )
        
        # Extract the actual content from the result
        if result["status"] == "success":
            generated_content = result["content"]
        else:
            generated_content = f"Content generation failed: {result.get('content', 'Unknown error')}"
        
        # Save to database
        db_content = Content(
            title=title,
            content=generated_content,
            content_type=content_type,
            user_id=current_user.id,
            status="completed" if result["status"] == "success" else "failed",
            word_count=word_count,
            content_metadata={
                "target_audience": target_audience,
                "tone": tone,
                "keywords": keywords,
                "description": description,
                "generation_status": result["status"],
                "model_used": result.get("model_used", "unknown")
            }
        )
        
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        
        return db_content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/content/projects", response_model=List[ContentResponse])
async def get_user_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all content projects for the current user"""
    projects = db.query(Content).filter(Content.user_id == current_user.id).all()
    return projects

@app.get("/api/v1/content/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific content by ID"""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content

# Content generation endpoints
@app.post("/api/v1/content/generate-advanced", response_model=ContentGenerationResponse)
async def generate_advanced_content(request: ContentGenerationRequest):
    """Generate content using advanced parameters"""
    try:
        result = await content_generator.generate_content(
            prompt=request.prompt,
            content_type=request.content_type,
            style=request.tone,
            length="long" if request.word_count > 1000 else "medium" if request.word_count > 500 else "short"
        )
        
        if result["status"] == "success":
            content = result["content"]
            word_count = len(content.split())
            reading_time = max(1, word_count // 200)  # Average reading speed
            
            return ContentGenerationResponse(
                generated_content=content,
                word_count=word_count,
                estimated_reading_time=reading_time,
                suggestions=["Consider adding more specific examples", "Include relevant statistics"]
            )
        else:
            raise HTTPException(status_code=500, detail="Content generation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/content/refine", response_model=ContentRefinementResponse)
async def refine_content(request: ContentRefinementRequest):
    """Refine existing content"""
    try:
        result = await style_refiner.refine_content(
            content=request.content,
            style=request.style,
            target_audience=request.target_audience
        )
        
        return ContentRefinementResponse(
            refined_content=result["refined_content"],
            changes_made=result["changes_made"],
            readability_score=result["readability_score"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/content/optimize-seo", response_model=SEOOptimizationResponse)
async def optimize_seo(request: SEOOptimizationRequest):
    """Optimize content for SEO"""
    try:
        result = await seo_optimizer.optimize_content(
            content=request.content,
            keywords=request.keywords,
            target_url=request.target_url
        )
        
        return SEOOptimizationResponse(
            optimized_content=result["optimized_content"],
            keyword_density=result["keyword_density"],
            seo_score=result["seo_score"],
            suggestions=result["suggestions"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/content/check-plagiarism", response_model=PlagiarismCheckResponse)
async def check_plagiarism(request: PlagiarismCheckRequest):
    """Check content for plagiarism"""
    try:
        result = await plagiarism_checker.check_content(
            content=request.content,
            check_facts=request.check_facts
        )
        
        return PlagiarismCheckResponse(
            plagiarism_score=result["plagiarism_score"],
            fact_check_results=result["fact_check_results"],
            originality_score=result["originality_score"],
            recommendations=result["recommendations"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
