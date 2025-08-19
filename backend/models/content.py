from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database import Base  # Fixed: use absolute import from models
import uuid

class Content(Base):
    __tablename__ = "content"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="draft")
    word_count = Column(Integer, default=0)
    content_metadata = Column(JSON, default={})  # Changed from 'metadata' to 'content_metadata'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="content")
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', type='{self.content_type}')>" 