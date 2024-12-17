from typing import List
from datetime import datetime
from ..schemas.clustering import (
    ModelInfo, ClusteringRequest, ClusteringResponse, ClusterResult
)
from .text_clustering import TextClusteringService

# Initialize the clustering service
clustering_service = TextClusteringService()

def get_available_models() -> List[ModelInfo]:
    """Returns list of available clustering models"""
    return [
        ModelInfo(
            id="kmeans",
            name="K-Means Clustering",
            description="Uses TF-IDF text vectorization with K-means clustering"
        ),
        ModelInfo(
            id="agglomerative",
            name="Agglomerative Clustering",
            description="Hierarchical clustering using TF-IDF text vectorization"
        ),
        ModelInfo(
            id="dbscan",
            name="DBSCAN Clustering",
            description="Density-based clustering using TF-IDF text vectorization"
        )
    ]

async def perform_clustering(request: ClusteringRequest) -> ClusteringResponse:
    """Performs clustering analysis on the input texts"""
    # Perform clustering
    results = clustering_service.cluster_texts(
        texts=request.texts,
        model_id=request.model_id,
        params=request.params
    )

    # Convert to response format
    clusters = [
        ClusterResult(
            id=c["id"],
            summary=c["summary"],
            texts=c["texts"],
            size=c["size"],
            percentage=c["percentage"],
            keywords=c["keywords"],
            representative_text=c["representative_text"]
        )
        for c in results["clusters"]
    ]

    return ClusteringResponse(
        clusters=clusters,
        total_texts=results["total_texts"],
        model_used=request.model_id,
        created_at=datetime.now()
    )
