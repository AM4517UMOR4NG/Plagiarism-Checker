"""
Multi-algorithm similarity detection module.
Implements state-of-the-art algorithms for plagiarism detection.
"""
from typing import List, Tuple, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer


class SimilarityDetector:
    """
    Advanced multi-algorithm similarity detection.
    Combines lexical, syntactic, and semantic approaches for optimal accuracy.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """
        Initialize similarity detector with pre-trained models.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.semantic_model = None
        self.model_name = model_name
        self._model_loaded = False
    
    def _load_semantic_model(self):
        """Lazy load semantic model to save memory."""
        if not self._model_loaded:
            self.semantic_model = SentenceTransformer(self.model_name)
            self._model_loaded = True
    
    def cosine_similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate TF-IDF based cosine similarity.
        Optimal for lexical matching and document-level comparison.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            # Use TF-IDF with character n-grams for better matching
            vectorizer = TfidfVectorizer(
                analyzer='char',
                ngram_range=(3, 5),  # Character tri-grams to 5-grams
                min_df=1,
                max_features=5000
            )
            
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error in cosine_similarity_score: {e}")
            return 0.0
    
    def ngram_similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate n-gram based similarity using Ratcliff-Obershelp algorithm.
        Excellent for detecting paraphrasing and moderate changes.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            # Use partial ratio for substring matching
            partial_score = fuzz.partial_ratio(text1, text2) / 100.0
            
            # Use token sort ratio for word-order independent matching
            token_score = fuzz.token_sort_ratio(text1, text2) / 100.0
            
            # Combine both scores with weights
            return (partial_score * 0.6 + token_score * 0.4)
        except Exception as e:
            print(f"Error in ngram_similarity_score: {e}")
            return 0.0
    
    def lexical_similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate lexical similarity using word-level TF-IDF.
        Good for detecting copy-paste with minor modifications.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            # Word-level TF-IDF with word n-grams
            vectorizer = TfidfVectorizer(
                analyzer='word',
                ngram_range=(1, 3),  # Unigrams to trigrams
                min_df=1,
                max_features=3000,
                token_pattern=r'\b\w+\b'
            )
            
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error in lexical_similarity_score: {e}")
            return 0.0
    
    def semantic_similarity_score(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity using Sentence Transformers.
        Best for detecting paraphrasing and meaning-preserving rewrites.
        Uses state-of-the-art BERT-based embeddings.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            # Load model on first use
            self._load_semantic_model()
            
            # Generate embeddings
            embeddings = self.semantic_model.encode([text1, text2], convert_to_tensor=True)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                embeddings[0:1].cpu().numpy(),
                embeddings[1:2].cpu().numpy()
            )[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error in semantic_similarity_score: {e}")
            return 0.0
    
    def combined_similarity_score(
        self,
        text1: str,
        text2: str,
        weights: Dict[str, float] = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate weighted combined similarity across all algorithms.
        Provides the most robust and accurate plagiarism detection.
        
        Args:
            text1: First text
            text2: Second text
            weights: Optional custom weights for each algorithm
            
        Returns:
            Tuple of (overall_score, individual_scores)
        """
        # Default weights optimized for plagiarism detection
        if weights is None:
            weights = {
                'cosine': 0.25,    # Character-level matching
                'ngram': 0.25,     # Fuzzy string matching
                'lexical': 0.25,   # Word-level matching
                'semantic': 0.25   # Meaning-based matching
            }
        
        # Calculate all similarity scores
        scores = {
            'cosine': self.cosine_similarity_score(text1, text2),
            'ngram': self.ngram_similarity_score(text1, text2),
            'lexical': self.lexical_similarity_score(text1, text2),
            'semantic': self.semantic_similarity_score(text1, text2)
        }
        
        # Calculate weighted average
        overall = sum(scores[k] * weights[k] for k in weights.keys())
        
        return overall, scores
    
    def find_matching_fragments(
        self,
        query_text: str,
        corpus_texts: List[str],
        threshold: float = 0.7,
        fragment_size: int = 100
    ) -> List[Dict]:
        """
        Find specific text fragments that match between query and corpus.
        
        Args:
            query_text: Text to check for plagiarism
            corpus_texts: List of reference texts
            threshold: Minimum similarity threshold
            fragment_size: Size of text fragments to compare
            
        Returns:
            List of matching fragments with scores and sources
        """
        matches = []
        
        # Split query into fragments (sentences or fixed-size chunks)
        query_sentences = self._split_into_fragments(query_text, fragment_size)
        
        for i, corpus_text in enumerate(corpus_texts):
            corpus_sentences = self._split_into_fragments(corpus_text, fragment_size)
            
            for q_frag in query_sentences:
                for c_frag in corpus_sentences:
                    # Quick filter with n-gram similarity
                    quick_score = self.ngram_similarity_score(q_frag, c_frag)
                    
                    if quick_score >= threshold * 0.8:  # Pre-filter
                        # More accurate scoring
                        score, _ = self.combined_similarity_score(q_frag, c_frag)
                        
                        if score >= threshold:
                            matches.append({
                                'text': q_frag,
                                'score': round(score, 3),
                                'source': f"Source {i + 1}",
                                'matched_text': c_frag
                            })
        
        # Sort by score and remove duplicates
        matches = sorted(matches, key=lambda x: x['score'], reverse=True)
        return matches[:10]  # Return top 10 matches
    
    def _split_into_fragments(self, text: str, size: int) -> List[str]:
        """Split text into fragments of approximately equal size."""
        # Simple sentence-based splitting
        import re
        sentences = re.split(r'[.!?]+', text)
        fragments = []
        current = []
        current_len = 0
        
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            
            current.append(sent)
            current_len += len(sent)
            
            if current_len >= size:
                fragments.append('. '.join(current))
                current = []
                current_len = 0
        
        if current:
            fragments.append('. '.join(current))
        
        return [f for f in fragments if len(f) > 20]
