from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class ContentType(enum.Enum):
    BLOG_POST = "blog_post"
    MARKETING_COPY = "marketing_copy"
    CREATIVE_STORY = "creative_story"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    ARTICLE = "article"

class ContentStatus(enum.Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    content_pieces = relationship("ContentPiece", back_populates="project")
    
    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}')>"

class ContentPiece(Base):
    __tablename__ = "content_pieces"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    # SEO and metadata
    seo_title = Column(String)
    seo_description = Column(Text)
    keywords = Column(JSON)  # Store as JSON array
    seo_score = Column(Integer, default=0)
    
    # Style and tone
    tone = Column(String)  # professional, casual, humorous, academic
    target_audience = Column(String)
    word_count = Column(Integer, default=0)
    
    # AI processing metadata
    ai_generated = Column(Boolean, default=False)
    plagiarism_score = Column(Integer, default=0)
    fact_check_score = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    author = relationship("User", back_populates="content_pieces")
    project = relationship("Project", back_populates="content_pieces")
    versions = relationship("ContentVersion", back_populates="content_piece")
    
    def __repr__(self):
        return f"<ContentPiece(id={self.id}, title='{self.title}', type={self.content_type.value})>"

class ContentVersion(Base):
    __tablename__ = "content_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    content_piece_id = Column(Integer, ForeignKey("content_pieces.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    changes_summary = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    content_piece = relationship("ContentPiece", back_populates="versions")
    created_by = relationship("User")
    
    def __repr__(self):
        return f"<ContentVersion(id={self.id}, piece_id={self.content_piece_id}, version={self.version_number})>" 