from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base

class ClusteringAnalysis(Base):
    __tablename__ = "clustering_analyses"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    params = Column(JSON)
    results = Column(JSON)
    total_texts = Column(Integer)
    metrics = Column(JSON)  # For storing silhouette score, etc.
