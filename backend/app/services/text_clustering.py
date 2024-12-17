from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from typing import List, Dict, Any
import numpy as np
from collections import Counter

class TextClusteringService:
    def __init__(self):
        # Initialize TF-IDF vectorizer for text embeddings
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            max_df=0.95,
            min_df=2
        )

        # Initialize clustering models with simplified IDs
        self.models = {
            "kmeans": lambda n_clusters: KMeans(n_clusters=n_clusters, random_state=42),
            "agglomerative": lambda n_clusters: AgglomerativeClustering(n_clusters=n_clusters),
            "dbscan": lambda: DBSCAN(eps=0.3, min_samples=2)
        }

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Convert texts to embeddings using TF-IDF"""
        return self.vectorizer.fit_transform(texts).toarray()

    def get_cluster_summary(self, texts: List[str]) -> str:
        """Generate one-sentence summary for a cluster using frequency analysis"""
        return texts[0] if texts else ""

    def get_cluster_keywords(self, texts: List[str], top_k: int = 5) -> List[str]:
        """Extract key terms from cluster texts using TF-IDF features"""
        if not texts:
            return []

        # Get feature names and their TF-IDF scores
        tfidf = self.vectorizer.transform([' '.join(texts)])
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        sorted_indices = np.argsort(tfidf.toarray()[0])[::-1]

        # Return top k keywords
        return feature_names[sorted_indices][:top_k].tolist()

    def cluster_texts(
        self,
        texts: List[str],
        model_id: str,
        params: Dict[str, Any] = None
    ) -> Dict:
        """Perform clustering analysis on texts"""
        if not texts:
            raise ValueError("No texts provided for clustering")

        # Get embeddings
        embeddings = self.get_embeddings(texts)

        # Determine number of clusters if not specified
        params = params or {}
        n_clusters = params.get('num_clusters', min(len(texts) // 5 + 1, 20))

        # Get clustering model
        if model_id not in self.models:
            raise ValueError(f"Unknown model: {model_id}")

        if model_id == "dbscan":
            model = self.models[model_id]()
        else:
            model = self.models[model_id](n_clusters)

        # Perform clustering
        labels = model.fit_predict(embeddings)

        # Calculate metrics
        metrics = {}
        if len(set(labels)) > 1:  # Only calculate if we have more than one cluster
            metrics["silhouette_score"] = float(silhouette_score(embeddings, labels))
            metrics["davies_bouldin_score"] = float(davies_bouldin_score(embeddings, labels))

        # Organize results by cluster
        clusters = []
        unique_labels = sorted(set(labels))
        total_texts = len(texts)

        for label in unique_labels:
            if label == -1:  # Skip noise points from DBSCAN
                continue

            cluster_texts = [t for i, t in enumerate(texts) if labels[i] == label]
            cluster_size = len(cluster_texts)

            clusters.append({
                "id": int(label),
                "texts": cluster_texts,
                "size": cluster_size,
                "percentage": cluster_size / total_texts * 100,
                "summary": self.get_cluster_summary(cluster_texts),
                "keywords": self.get_cluster_keywords(cluster_texts),
                "representative_text": cluster_texts[0] if cluster_texts else ""
            })

        return {
            "clusters": clusters,
            "total_texts": total_texts,
            "metrics": metrics
        }
