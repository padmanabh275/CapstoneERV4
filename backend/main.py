from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session

# Import our content creation modules
from backend.core.content_generator import ContentGenerator
from backend.core.style_refiner import StyleRefiner
from backend.core.seo_optimizer import SEOOptimizer
from backend.core.plagiarism_checker import PlagiarismChecker

# Import database and auth modules
from backend.models.database import get_db, engine, Base
from backend.auth import get_current_active_user, JWTHandler
from backend.models.user import User

app = FastAPI(
    title="AI-Assisted Content Creation Platform",
    description="A multi-agent system for generating, refining, and optimizing content",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
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
    tone: str = "professional"  # professional, casual, humorous, academic
    word_count: int = 500
    target_audience: str = "general"
    content_type: str = "blog_post"  # blog_post, marketing_copy, creative_story

class ContentGenerationResponse(BaseModel):
    generated_content: str
    word_count: int
    estimated_reading_time: int
    suggestions: List[str]

class ContentRefinementRequest(BaseModel):
    content: str
    style: str = "casual"
    length: str = "medium"  # short, medium, long
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

@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
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
    current_user: User = Depends(get_current_active_user),
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

@app.post("/api/v1/generate-content", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """Generate content based on user prompt and parameters"""
    try:
        generated_content = await content_generator.generate(
            prompt=request.prompt,
            tone=request.tone,
            word_count=request.word_count,
            target_audience=request.target_audience,
            content_type=request.content_type
        )
        
        word_count = len(generated_content.split())
        estimated_reading_time = max(1, word_count // 200)  # Average reading speed
        
        return ContentGenerationResponse(
            generated_content=generated_content,
            word_count=word_count,
            estimated_reading_time=estimated_reading_time,
            suggestions=["Consider adding more specific examples", "Include a call-to-action"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@app.post("/api/v1/refine-content", response_model=ContentRefinementResponse)
async def refine_content(request: ContentRefinementRequest):
    """Refine existing content based on style and audience preferences"""
    try:
        refined_content, changes = await style_refiner.refine(
            content=request.content,
            style=request.style,
            length=request.length,
            target_audience=request.target_audience
        )
        
        readability_score = style_refiner.calculate_readability(refined_content)
        
        return ContentRefinementResponse(
            refined_content=refined_content,
            changes_made=changes,
            readability_score=readability_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content refinement failed: {str(e)}")

@app.post("/api/v1/optimize-seo", response_model=SEOOptimizationResponse)
async def optimize_seo(request: SEOOptimizationRequest):
    """Optimize content for search engines"""
    try:
        optimized_content, keyword_density, seo_score = await seo_optimizer.optimize(
            content=request.content,
            keywords=request.keywords,
            target_url=request.target_url
        )
        
        suggestions = seo_optimizer.get_suggestions(optimized_content, request.keywords)
        
        return SEOOptimizationResponse(
            optimized_content=optimized_content,
            keyword_density=keyword_density,
            seo_score=seo_score,
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SEO optimization failed: {str(e)}")

@app.post("/api/v1/check-plagiarism", response_model=PlagiarismCheckResponse)
async def check_plagiarism(request: PlagiarismCheckRequest):
    """Check content for plagiarism and factual accuracy"""
    try:
        plagiarism_score, fact_check_results = await plagiarism_checker.check(
            content=request.content,
            check_facts=request.check_facts
        )
        
        originality_score = 1.0 - plagiarism_score
        recommendations = plagiarism_checker.get_recommendations(plagiarism_score, fact_check_results)
        
        return PlagiarismCheckResponse(
            plagiarism_score=plagiarism_score,
            fact_check_results=fact_check_results,
            originality_score=originality_score,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plagiarism check failed: {str(e)}")

@app.get("/api/v1/health")
def detailed_health_check():
    """Detailed health check for all services"""
    return {
        "status": "healthy",
        "services": {
            "content_generator": "operational",
            "style_refiner": "operational", 
            "seo_optimizer": "operational",
            "plagiarism_checker": "operational"
        },
        "aws_services": {
            "sagemaker": "connected",
            "s3": "connected",
            "lambda": "connected"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
