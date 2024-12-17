from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ClusteringRequest(BaseModel):
    model_id: str
    texts: List[str]
    params: Optional[Dict] = None

class ClusterResult(BaseModel):
    id: int
    summary: str
    texts: List[str]
    size: int
    percentage: float
    keywords: List[str]
    representative_text: str

class ClusteringResponse(BaseModel):
    clusters: List[ClusterResult]
    total_texts: int
    model_used: str
    created_at: datetime

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
