"""
AI-Generated Text Detection Module.
Implements multiple methods to detect if text is written by AI (ChatGPT, Claude, etc.)

Methods:
1. Perplexity Analysis - Lower perplexity indicates AI-generated text
2. Burstiness Score - AI text has lower burstiness (more uniform)
3. Linguistic Pattern Detection - AI has specific patterns
4. RoBERTa-based Classification - Deep learning classifier
"""
import re
import math
import numpy as np
from typing import Dict, List, Tuple
from collections import Counter
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class AIDetector:
    """
    Multi-method AI detection system.
    Combines statistical analysis and deep learning for robust detection.
    """
    
    def __init__(self):
        """Initialize AI detector with models."""
        self.roberta_model = None
        self.roberta_tokenizer = None
        self._model_loaded = False
        
        # AI writing patterns (common in GPT outputs)
        self.ai_patterns = {
            'hedging': [
                r'\b(however|moreover|furthermore|nevertheless|nonetheless)\b',
                r'\b(it is important to note|it should be noted|it is worth noting)\b',
                r'\b(in conclusion|to summarize|in summary)\b',
            ],
            'formal_transitions': [
                r'\b(firstly|secondly|thirdly|finally)\b',
                r'\b(on the one hand|on the other hand)\b',
                r'\b(in addition|additionally|furthermore)\b',
            ],
            'ai_phrases': [
                r'\b(as an AI|I am an AI|as a language model)\b',
                r'\b(I don\'t have personal|I cannot provide personal)\b',
                r'\b(it\'s important to|it is crucial to)\b',
                r'\b(delve into|dive into|explore the nuances)\b',
            ]
        }
    
    def _load_roberta_model(self):
        """Lazy load RoBERTa model for AI detection."""
        if not self._model_loaded:
            try:
                # Using RoBERTa fine-tuned for AI detection
                model_name = "roberta-base-openai-detector"
                # Fallback to general RoBERTa if specific model not available
                try:
                    self.roberta_tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.roberta_model = AutoModelForSequenceClassification.from_pretrained(model_name)
                except:
                    # Use distilroberta as lightweight alternative
                    self.roberta_tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")
                    self.roberta_model = AutoModelForSequenceClassification.from_pretrained(
                        "distilroberta-base",
                        num_labels=2
                    )
                
                self.roberta_model.eval()
                self._model_loaded = True
            except Exception as e:
                print(f"Warning: Could not load RoBERTa model: {e}")
                self._model_loaded = False
    
    def calculate_perplexity(self, text: str) -> float:
        """
        Calculate perplexity score.
        Lower perplexity = more predictable = more likely AI-generated.
        
        Args:
            text: Input text
            
        Returns:
            Perplexity score (lower = more AI-like)
        """
        if not text or len(text.strip()) < 10:
            return 100.0  # High perplexity for very short text
        
        # Tokenize into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        if len(words) < 5:
            return 100.0
        
        # Calculate word frequencies
        word_freq = Counter(words)
        total_words = len(words)
        
        # Calculate entropy (simplified perplexity)
        entropy = 0.0
        for word, count in word_freq.items():
            prob = count / total_words
            entropy -= prob * math.log2(prob)
        
        # Perplexity = 2^entropy
        perplexity = 2 ** entropy
        
        # Normalize to 0-100 scale (lower = more AI-like)
        # AI text typically has perplexity 20-40
        # Human text typically has perplexity 50-100+
        normalized = min(100, max(0, perplexity))
        
        return normalized
    
    def calculate_burstiness(self, text: str) -> float:
        """
        Calculate burstiness score.
        AI text has lower burstiness (more uniform sentence lengths).
        Human text has higher burstiness (varied sentence lengths).
        
        Args:
            text: Input text
            
        Returns:
            Burstiness score (0-1, lower = more AI-like)
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return 0.5  # Neutral for very short text
        
        # Calculate sentence lengths
        lengths = [len(s.split()) for s in sentences]
        
        if len(lengths) < 2:
            return 0.5
        
        # Calculate variance and mean
        mean_length = np.mean(lengths)
        variance = np.var(lengths)
        
        if mean_length == 0:
            return 0.5
        
        # Burstiness = (variance - mean) / (variance + mean)
        # Ranges from -1 to 1, normalize to 0-1
        burstiness = (variance - mean_length) / (variance + mean_length)
        normalized = (burstiness + 1) / 2  # Convert to 0-1 scale
        
        # AI typically has burstiness < 0.3
        # Human typically has burstiness > 0.5
        return normalized
    
    def detect_ai_patterns(self, text: str) -> Dict[str, float]:
        """
        Detect linguistic patterns common in AI-generated text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of pattern scores
        """
        text_lower = text.lower()
        word_count = len(text.split())
        
        if word_count == 0:
            return {'hedging': 0.0, 'formal_transitions': 0.0, 'ai_phrases': 0.0}
        
        scores = {}
        
        for pattern_type, patterns in self.ai_patterns.items():
            matches = 0
            for pattern in patterns:
                matches += len(re.findall(pattern, text_lower, re.IGNORECASE))
            
            # Normalize by text length (matches per 100 words)
            score = (matches / word_count) * 100
            scores[pattern_type] = min(1.0, score)  # Cap at 1.0
        
        return scores
    
    def roberta_classify(self, text: str) -> float:
        """
        Use RoBERTa model to classify if text is AI-generated.
        
        Args:
            text: Input text
            
        Returns:
            Probability that text is AI-generated (0-1)
        """
        try:
            self._load_roberta_model()
            
            if not self._model_loaded or self.roberta_model is None:
                return 0.5  # Neutral if model not available
            
            # Tokenize
            inputs = self.roberta_tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            # Get prediction
            with torch.no_grad():
                outputs = self.roberta_model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)
                
                # Assuming label 1 is "AI-generated"
                ai_prob = probs[0][1].item()
            
            return ai_prob
            
        except Exception as e:
            print(f"Error in RoBERTa classification: {e}")
            return 0.5  # Neutral on error
    
    def analyze_vocabulary_diversity(self, text: str) -> float:
        """
        Analyze vocabulary diversity (Type-Token Ratio).
        AI text often has higher vocabulary diversity.
        
        Args:
            text: Input text
            
        Returns:
            Diversity score (0-1, higher = more diverse)
        """
        words = re.findall(r'\b\w+\b', text.lower())
        
        if len(words) < 10:
            return 0.5
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # Type-Token Ratio
        ttr = unique_words / total_words
        
        # AI typically has TTR 0.6-0.8
        # Human typically has TTR 0.4-0.6
        return ttr
    
    def detect_ai_comprehensive(self, text: str) -> Tuple[float, Dict[str, float]]:
        """
        Comprehensive AI detection using all methods.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (overall_ai_probability, individual_scores)
        """
        if not text or len(text.strip()) < 50:
            return 0.0, {
                'perplexity': 0.0,
                'burstiness': 0.0,
                'patterns': 0.0,
                'roberta': 0.0,
                'vocabulary': 0.0
            }
        
        # Calculate all metrics
        perplexity = self.calculate_perplexity(text)
        burstiness = self.calculate_burstiness(text)
        patterns = self.detect_ai_patterns(text)
        vocabulary = self.analyze_vocabulary_diversity(text)
        
        # Perplexity score (invert: lower perplexity = higher AI probability)
        perplexity_score = max(0, (100 - perplexity) / 100)
        
        # Burstiness score (invert: lower burstiness = higher AI probability)
        burstiness_score = 1 - burstiness
        
        # Pattern score (average of all pattern types)
        pattern_score = np.mean(list(patterns.values()))
        
        # Vocabulary score (higher diversity = higher AI probability)
        vocab_score = vocabulary
        
        # RoBERTa score (if available)
        roberta_score = self.roberta_classify(text)
        
        # Weighted combination
        # RoBERTa gets highest weight as it's most accurate
        weights = {
            'perplexity': 0.15,
            'burstiness': 0.15,
            'patterns': 0.15,
            'vocabulary': 0.15,
            'roberta': 0.40  # Highest weight for deep learning model
        }
        
        overall_score = (
            perplexity_score * weights['perplexity'] +
            burstiness_score * weights['burstiness'] +
            pattern_score * weights['patterns'] +
            vocab_score * weights['vocabulary'] +
            roberta_score * weights['roberta']
        )
        
        individual_scores = {
            'perplexity': round(perplexity_score, 3),
            'burstiness': round(burstiness_score, 3),
            'patterns': round(pattern_score, 3),
            'vocabulary': round(vocab_score, 3),
            'roberta': round(roberta_score, 3)
        }
        
        return round(overall_score, 3), individual_scores
    
    def get_ai_confidence_level(self, ai_probability: float) -> str:
        """
        Get confidence level for AI detection.
        
        Args:
            ai_probability: AI probability (0-1)
            
        Returns:
            Confidence level string
        """
        if ai_probability >= 0.80:
            return "Very High - Likely AI-generated"
        elif ai_probability >= 0.60:
            return "High - Probably AI-generated"
        elif ai_probability >= 0.40:
            return "Medium - Possibly AI-generated"
        elif ai_probability >= 0.20:
            return "Low - Probably human-written"
        else:
            return "Very Low - Likely human-written"
