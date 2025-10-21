import time
import os
from celery import Celery
from pydantic import BaseModel

from worker.extractors import DocumentExtractor
from worker.preprocessor import TextPreprocessor
from worker.similarity import SimilarityDetector
from worker.corpus import CorpusManager
from worker.ai_detector import AIDetector

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("plagiarism_checker", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# Initialize components (shared across workers)
preprocessor = TextPreprocessor()
detector = SimilarityDetector()
corpus_manager = CorpusManager()
ai_detector = AIDetector()


class UploadPayload(BaseModel):
    doc_id: str
    title: str | None = None
    user_id: str | None = None
    file_path: str | None = None
    text: str | None = None


@celery_app.task(name="worker.process_upload")
def process_upload(payload: dict):
    """
    Advanced plagiarism & AI detection pipeline using multi-algorithm approach.
    
    Pipeline:
    1. Extract text from document (PDF/DOCX/TXT)
    2. Preprocess and normalize text
    3. AI Detection - Check if text is AI-generated
    4. Plagiarism Detection - Compare against corpus using multiple algorithms
    5. Calculate overall similarity score
    6. Identify matching fragments
    7. Return comprehensive results with AI probability
    """
    start_time = time.time()
    data = UploadPayload(**payload)
    
    try:
        # Step 1: Extract text from document
        if data.file_path and os.path.exists(data.file_path):
            raw_text = DocumentExtractor.extract(data.file_path)
        elif data.text:
            raw_text = data.text
        else:
            return {
                "doc_id": data.doc_id,
                "title": data.title,
                "error": "No text or file provided",
                "summary": {"similarity": 0.0, "sources": [], "processing_time_ms": 0},
                "fragments": [],
                "explain": {"cosine": 0.0, "ngram": 0.0, "lexical": 0.0, "semantic": 0.0}
            }
        
        # Step 2: Preprocess text
        normalized_text = preprocessor.normalize(raw_text)
        
        if len(normalized_text) < 50:
            return {
                "doc_id": data.doc_id,
                "title": data.title,
                "error": "Text too short for analysis",
                "summary": {"similarity": 0.0, "sources": [], "processing_time_ms": 0},
                "fragments": [],
                "explain": {"cosine": 0.0, "ngram": 0.0, "lexical": 0.0, "semantic": 0.0}
            }
        
        # Step 3: Get reference corpus
        corpus_texts = corpus_manager.get_all_texts()
        corpus_metadata = corpus_manager.get_metadata()
        
        # Step 4: Calculate similarity scores against corpus
        max_similarity = 0.0
        all_scores = {"cosine": 0.0, "ngram": 0.0, "lexical": 0.0, "semantic": 0.0}
        
        for corpus_text in corpus_texts:
            normalized_corpus = preprocessor.normalize(corpus_text)
            overall_score, individual_scores = detector.combined_similarity_score(
                normalized_text,
                normalized_corpus
            )
            
            if overall_score > max_similarity:
                max_similarity = overall_score
                all_scores = individual_scores
        
        # Step 5: AI Detection - Check if text is AI-generated
        ai_probability, ai_scores = ai_detector.detect_ai_comprehensive(raw_text)
        ai_confidence = ai_detector.get_ai_confidence_level(ai_probability)
        
        # Step 6: Find matching fragments
        fragments = detector.find_matching_fragments(
            normalized_text,
            [preprocessor.normalize(t) for t in corpus_texts],
            threshold=0.65
        )
        
        # Map fragments to source metadata
        for fragment in fragments:
            try:
                source_idx = int(fragment['source'].split()[-1]) - 1
                if 0 <= source_idx < len(corpus_metadata):
                    fragment['source'] = corpus_metadata[source_idx]['title']
                    fragment['url'] = corpus_metadata[source_idx]['url']
            except (ValueError, IndexError):
                pass
        
        # Step 7: Prepare sources list
        sources = []
        if max_similarity > 0.3:  # Only include sources if similarity is significant
            for meta in corpus_metadata[:3]:  # Top 3 sources
                sources.append({
                    "title": meta['title'],
                    "url": meta['url']
                })
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        # Return comprehensive results with AI detection
        return {
            "doc_id": data.doc_id,
            "title": data.title or "Untitled Document",
            "summary": {
                "similarity": round(max_similarity, 3),
                "sources": sources,
                "processing_time_ms": processing_time,
            },
            "fragments": fragments[:5],  # Top 5 fragments
            "explain": {
                "cosine": round(all_scores['cosine'], 3),
                "ngram": round(all_scores['ngram'], 3),
                "lexical": round(all_scores['lexical'], 3),
                "semantic": round(all_scores['semantic'], 3),
            },
            "ai_detection": {
                "probability": ai_probability,
                "confidence": ai_confidence,
                "scores": ai_scores
            },
        }
    
    except Exception as e:
        # Error handling
        processing_time = int((time.time() - start_time) * 1000)
        return {
            "doc_id": data.doc_id,
            "title": data.title,
            "error": str(e),
            "summary": {
                "similarity": 0.0,
                "sources": [],
                "processing_time_ms": processing_time,
            },
            "fragments": [],
            "explain": {
                "cosine": 0.0,
                "ngram": 0.0,
                "lexical": 0.0,
                "semantic": 0.0,
            },
            "ai_detection": {
                "probability": 0.0,
                "confidence": "Error during detection",
                "scores": {
                    "perplexity": 0.0,
                    "burstiness": 0.0,
                    "patterns": 0.0,
                    "vocabulary": 0.0,
                    "roberta": 0.0
                }
            },
        }
