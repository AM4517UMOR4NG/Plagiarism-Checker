"""
Text preprocessing and normalization module.
Implements optimal preprocessing strategies for plagiarism detection.
"""
import re
from typing import List


class TextPreprocessor:
    """Advanced text preprocessing for optimal similarity detection."""
    
    def __init__(self):
        # Common English stop words (minimal set for plagiarism detection)
        # We keep most words to preserve semantic meaning
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can'
        }
    
    def normalize(self, text: str, remove_stopwords: bool = False) -> str:
        """
        Normalize text for similarity comparison.
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stop words (use with caution)
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep sentence structure
        text = re.sub(r'[^\w\s.,!?;:\-\']', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove stop words if requested (be cautious - may affect semantic similarity)
        if remove_stopwords:
            words = text.split()
            words = [w for w in words if w not in self.stop_words]
            text = ' '.join(words)
        
        return text.strip()
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences for fragment-level analysis.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence tokenization
        # For production, consider using nltk or spaCy for better accuracy
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
            
        Returns:
            List of words
        """
        # Remove punctuation and split
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        return [w for w in words if w]
    
    def get_ngrams(self, text: str, n: int = 3) -> List[str]:
        """
        Generate character n-grams for fingerprinting.
        
        Args:
            text: Input text
            n: N-gram size
            
        Returns:
            List of n-grams
        """
        # Remove all whitespace for character n-grams
        text = re.sub(r'\s+', '', text.lower())
        
        if len(text) < n:
            return [text]
        
        return [text[i:i+n] for i in range(len(text) - n + 1)]
    
    def get_word_ngrams(self, text: str, n: int = 5) -> List[str]:
        """
        Generate word n-grams for phrase matching.
        
        Args:
            text: Input text
            n: Number of consecutive words
            
        Returns:
            List of word n-grams
        """
        words = self.tokenize_words(text)
        
        if len(words) < n:
            return [' '.join(words)]
        
        return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
