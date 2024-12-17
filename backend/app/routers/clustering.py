from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.clustering import ClusteringRequest, ClusteringResponse, ModelInfo
from ..services.clustering import get_available_models, perform_clustering

router = APIRouter()

@router.get("/models", response_model=List[ModelInfo])
async def list_models():
    return get_available_models()

@router.post("/cluster", response_model=ClusteringResponse)
async def create_clustering(request: ClusteringRequest):
    try:
        return await perform_clustering(request)
    except Exception as e:
        # Enhanced error handling with debug info
        error_msg = f"Clustering failed: {str(e)}\n"
        if hasattr(e, '__cause__'):
            error_msg += f"Cause: {str(e.__cause__)}\n"
        if hasattr(e, '__context__'):
            error_msg += f"Context: {str(e.__context__)}\n"
        raise HTTPException(status_code=500, detail=error_msg)
