from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from typing import List, Dict, Any
import numpy as np
from collections import Counter
import jieba

class TextClusteringService:
    def __init__(self):
        # Initialize TF-IDF vectorizer for text embeddings
        self.vectorizer = TfidfVectorizer(
            max_features=5000,  # Increased for better Chinese character coverage
            stop_words=None,    # No stop words for Chinese
            max_df=1.0,        # Allow terms that appear in all documents
            min_df=0.0,        # Allow all terms, even those appearing once
            token_pattern=r'(?u)\b\w+\b',  # Allow single characters for Chinese
            analyzer=lambda x: list(jieba.cut(x))  # Use jieba for Chinese tokenization
        )

        # Initialize clustering models with simplified IDs
        self.models = {
            "kmeans": lambda n_clusters: KMeans(n_clusters=n_clusters, random_state=42),
            "agglomerative": lambda n_clusters: AgglomerativeClustering(n_clusters=n_clusters),
            "dbscan": lambda: DBSCAN(eps=0.3, min_samples=2)
        }

    def preprocess_chinese_text(self, texts: List[str]) -> List[str]:
        """Preprocess Chinese texts with minimal cleaning to preserve meaningful content"""
        processed_texts = []
        for text in texts:
            # Remove only basic punctuation while preserving Chinese punctuation
            text = ''.join(char for char in text if not (char.isspace() and char not in '，。！？；：'))
            # Tokenize with jieba and join with spaces
            tokens = jieba.cut(text)
            # Preserve all tokens, including single characters
            processed_text = ' '.join(token for token in tokens)
            processed_texts.append(processed_text)
        return processed_texts

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Convert texts to embeddings using TF-IDF with Chinese preprocessing"""
        processed_texts = self.preprocess_chinese_text(texts)
        # Fit vectorizer first to build vocabulary
        self.vectorizer.fit(processed_texts)
        # Then transform texts to get embeddings
        return self.vectorizer.transform(processed_texts).toarray()

    def get_cluster_summary(self, texts: List[str]) -> str:
        """Generate one-sentence summary for a cluster using frequency analysis of Chinese text"""
        if not texts:
            return ""

        # Process texts with jieba
        processed_texts = [list(jieba.cut(text)) for text in texts]

        # Get word frequencies from all processed texts
        word_freq = Counter([word for text in processed_texts for word in text])

        # Filter meaningful words (length > 1) and get top keywords
        keywords = [word for word, freq in word_freq.most_common(10)
                   if len(word.strip()) > 1]

        # Use most representative text as example
        example_text = texts[0][:50] + "..." if len(texts[0]) > 50 else texts[0]

        # Create summary combining keywords and example
        return f"主要话题：{'、'.join(keywords[:3])}。示例：{example_text}"

    def get_cluster_keywords(self, texts: List[str], top_k: int = 5) -> List[str]:
        """Extract key terms from cluster texts using TF-IDF features and jieba tokenization"""
        if not texts:
            return []

        # Combine texts and tokenize
        combined_text = " ".join(texts)
        words = list(jieba.cut(combined_text))

        # Get word frequencies and filter meaningful words
        word_freq = Counter(words)
        keywords = [word for word, _ in word_freq.most_common(top_k * 2)
                   if len(word.strip()) > 1]  # Filter single characters

        # Return top k keywords
        return keywords[:top_k]

    def cluster_texts(
        self,
        texts: List[str],
        model_id: str,
        params: Dict[str, Any] = None
    ) -> Dict:
        """Perform clustering analysis on texts"""
        if not texts:
            raise ValueError("No texts provided for clustering")

        if len(texts) < 2:
            raise ValueError("At least 2 texts are required for clustering")

        # Get embeddings
        embeddings = self.get_embeddings(texts)

        # Determine number of clusters if not specified
        params = params or {}
        n_clusters = params.get('num_clusters', min(2, len(texts)))  # At least 2 clusters for small datasets

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
