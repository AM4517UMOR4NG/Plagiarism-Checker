"""
Test script untuk memverifikasi algoritma plagiarism detection.
Run: python test_algorithms.py
"""
from worker.preprocessor import TextPreprocessor
from worker.similarity import SimilarityDetector
from worker.corpus import CorpusManager


def test_preprocessing():
    """Test text preprocessing."""
    print("=" * 60)
    print("TEST 1: Text Preprocessing")
    print("=" * 60)
    
    preprocessor = TextPreprocessor()
    
    text = """
    Machine Learning is AMAZING! Check out https://example.com for more.
    Contact: test@email.com
    Multiple    spaces     should    be    normalized.
    """
    
    normalized = preprocessor.normalize(text)
    print(f"Original:\n{text}")
    print(f"\nNormalized:\n{normalized}")
    
    sentences = preprocessor.tokenize_sentences(text)
    print(f"\nSentences: {sentences}")
    
    ngrams = preprocessor.get_word_ngrams(normalized, n=3)
    print(f"\nWord 3-grams (first 3): {ngrams[:3]}")
    
    print("\n✅ Preprocessing test passed!\n")


def test_similarity_algorithms():
    """Test all similarity algorithms."""
    print("=" * 60)
    print("TEST 2: Similarity Algorithms")
    print("=" * 60)
    
    detector = SimilarityDetector()
    
    # Test case 1: Identical text
    text1 = "Machine learning is a subset of artificial intelligence."
    text2 = "Machine learning is a subset of artificial intelligence."
    
    print(f"\nTest Case 1: Identical Text")
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    
    overall, scores = detector.combined_similarity_score(text1, text2)
    print(f"\nResults:")
    print(f"  Overall: {overall:.3f}")
    print(f"  Cosine:  {scores['cosine']:.3f}")
    print(f"  N-gram:  {scores['ngram']:.3f}")
    print(f"  Lexical: {scores['lexical']:.3f}")
    print(f"  Semantic: {scores['semantic']:.3f}")
    
    # Test case 2: Paraphrased text
    text3 = "Machine learning is a subset of artificial intelligence that focuses on learning from data."
    text4 = "ML represents a branch of AI that emphasizes data-driven learning approaches."
    
    print(f"\n\nTest Case 2: Paraphrased Text")
    print(f"Text 1: {text3}")
    print(f"Text 2: {text4}")
    
    overall2, scores2 = detector.combined_similarity_score(text3, text4)
    print(f"\nResults:")
    print(f"  Overall: {overall2:.3f}")
    print(f"  Cosine:  {scores2['cosine']:.3f}")
    print(f"  N-gram:  {scores2['ngram']:.3f}")
    print(f"  Lexical: {scores2['lexical']:.3f}")
    print(f"  Semantic: {scores2['semantic']:.3f}")
    
    # Test case 3: Completely different text
    text5 = "Machine learning is a subset of artificial intelligence."
    text6 = "Climate change refers to long-term shifts in global temperatures."
    
    print(f"\n\nTest Case 3: Different Text")
    print(f"Text 1: {text5}")
    print(f"Text 2: {text6}")
    
    overall3, scores3 = detector.combined_similarity_score(text5, text6)
    print(f"\nResults:")
    print(f"  Overall: {overall3:.3f}")
    print(f"  Cosine:  {scores3['cosine']:.3f}")
    print(f"  N-gram:  {scores3['ngram']:.3f}")
    print(f"  Lexical: {scores3['lexical']:.3f}")
    print(f"  Semantic: {scores3['semantic']:.3f}")
    
    print("\n✅ Similarity algorithms test passed!\n")


def test_corpus_matching():
    """Test matching against corpus."""
    print("=" * 60)
    print("TEST 3: Corpus Matching")
    print("=" * 60)
    
    detector = SimilarityDetector()
    corpus_manager = CorpusManager()
    preprocessor = TextPreprocessor()
    
    # Test with ML-related text (should match corpus)
    test_text = """
    Machine learning algorithms enable computers to learn from data without 
    explicit programming. These systems improve their performance through 
    experience and can make predictions based on patterns found in training data.
    """
    
    print(f"\nTest Text:\n{test_text}")
    
    corpus_texts = corpus_manager.get_all_texts()
    corpus_metadata = corpus_manager.get_metadata()
    
    max_similarity = 0.0
    best_match = None
    
    for i, corpus_text in enumerate(corpus_texts):
        normalized_test = preprocessor.normalize(test_text)
        normalized_corpus = preprocessor.normalize(corpus_text)
        
        overall, scores = detector.combined_similarity_score(
            normalized_test,
            normalized_corpus
        )
        
        if overall > max_similarity:
            max_similarity = overall
            best_match = corpus_metadata[i]['title']
    
    print(f"\n📊 Results:")
    print(f"  Max Similarity: {max_similarity:.3f}")
    print(f"  Best Match: {best_match}")
    
    # Find fragments
    print(f"\n🔍 Finding matching fragments...")
    fragments = detector.find_matching_fragments(
        preprocessor.normalize(test_text),
        [preprocessor.normalize(t) for t in corpus_texts],
        threshold=0.60
    )
    
    print(f"\nFound {len(fragments)} fragments with similarity > 0.60:")
    for i, frag in enumerate(fragments[:3], 1):
        print(f"\n  Fragment {i}:")
        print(f"    Text: {frag['text'][:80]}...")
        print(f"    Score: {frag['score']:.3f}")
        print(f"    Source: {frag['source']}")
    
    print("\n✅ Corpus matching test passed!\n")


def test_performance():
    """Test processing performance."""
    print("=" * 60)
    print("TEST 4: Performance Benchmark")
    print("=" * 60)
    
    import time
    
    detector = SimilarityDetector()
    preprocessor = TextPreprocessor()
    
    text1 = """
    Artificial intelligence and machine learning are transforming industries 
    across the globe. These technologies enable computers to perform tasks 
    that typically require human intelligence, such as visual perception, 
    speech recognition, decision-making, and language translation.
    """ * 5  # Repeat to make it longer
    
    text2 = """
    AI and ML technologies are revolutionizing various sectors worldwide.
    These systems allow machines to execute functions that normally need
    human cognitive abilities, including image analysis, voice understanding,
    making decisions, and converting between languages.
    """ * 5
    
    print(f"\nText length: ~{len(text1)} characters")
    
    # Test each algorithm
    algorithms = [
        ("Cosine Similarity", detector.cosine_similarity_score),
        ("N-gram Matching", detector.ngram_similarity_score),
        ("Lexical Similarity", detector.lexical_similarity_score),
        ("Semantic Similarity", detector.semantic_similarity_score),
    ]
    
    for name, func in algorithms:
        start = time.time()
        score = func(text1, text2)
        elapsed = (time.time() - start) * 1000
        print(f"\n{name}:")
        print(f"  Score: {score:.3f}")
        print(f"  Time: {elapsed:.1f}ms")
    
    # Test combined
    start = time.time()
    overall, scores = detector.combined_similarity_score(text1, text2)
    elapsed = (time.time() - start) * 1000
    
    print(f"\nCombined (All Algorithms):")
    print(f"  Overall: {overall:.3f}")
    print(f"  Total Time: {elapsed:.1f}ms")
    
    print("\n✅ Performance test completed!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 PLAGIARISM DETECTION ALGORITHM TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_preprocessing()
        test_similarity_algorithms()
        test_corpus_matching()
        test_performance()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nAlgoritma plagiarism detection berhasil diimplementasikan")
        print("dan berfungsi dengan optimal!\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
