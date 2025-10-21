# 🧠 Algoritma Plagiarism Detection - Dokumentasi Teknis

## 📊 Ringkasan Implementasi

Sistem ini menggunakan **pendekatan multi-algorithm** untuk mencapai akurasi deteksi plagiarisme yang optimal. Setiap algoritma mendeteksi jenis plagiarisme yang berbeda, dan hasilnya dikombinasikan untuk memberikan skor keseluruhan yang komprehensif.

## 🎯 Algoritma yang Diimplementasikan

### 1. **TF-IDF + Cosine Similarity (Character-Level)**

**Tujuan:** Deteksi kesamaan leksikal berbasis karakter

**Cara Kerja:**
- Menggunakan **Term Frequency-Inverse Document Frequency (TF-IDF)** untuk mengubah teks menjadi vektor numerik
- Menggunakan **character n-grams (3-5)** untuk menangkap pola karakter
- Menghitung **cosine similarity** antara vektor dokumen

**Kelebihan:**
- ✅ Sangat efektif untuk mendeteksi copy-paste dengan perubahan kecil
- ✅ Tahan terhadap penggantian kata (word substitution)
- ✅ Menangkap pola struktural teks

**Kompleksitas:** O(n) untuk vektorisasi, O(1) untuk cosine similarity

---

### 2. **N-gram Fuzzy Matching (Ratcliff-Obershelp)**

**Tujuan:** Deteksi kesamaan dengan toleransi terhadap modifikasi teks

**Cara Kerja:**
- Menggunakan library **rapidfuzz** dengan algoritma Ratcliff-Obershelp
- Menggabungkan **partial ratio** (substring matching) dan **token sort ratio** (word-order independent)
- Weight: 60% partial ratio + 40% token sort ratio

**Kelebihan:**
- ✅ Mendeteksi parafrase ringan
- ✅ Toleran terhadap perubahan urutan kata
- ✅ Efektif untuk teks yang di-reword

**Kompleksitas:** O(n*m) rata-rata, dengan optimisasi internal

---

### 3. **Lexical Similarity (Word-Level TF-IDF)**

**Tujuan:** Analisis kesamaan berbasis kata dan frasa

**Cara Kerja:**
- TF-IDF dengan **word n-grams (1-3)**
- Menangkap unigrams, bigrams, dan trigrams
- Cosine similarity pada vektor kata

**Kelebihan:**
- ✅ Mendeteksi plagiarisme berbasis frasa
- ✅ Mempertahankan konteks kata
- ✅ Efektif untuk deteksi copy-paste dengan sinonim

**Kompleksitas:** O(n) untuk vektorisasi

---

### 4. **Semantic Similarity (BERT-based Embeddings)**

**Tujuan:** Deteksi kesamaan makna (parafrase canggih)

**Cara Kerja:**
- Menggunakan **Sentence Transformers** dengan model `all-mpnet-base-v2`
- Mengubah teks menjadi **dense vector embeddings (768 dimensi)**
- Model berbasis **MPNet** (Masked and Permuted Pre-training)
- Cosine similarity pada embeddings

**Kelebihan:**
- ✅ Mendeteksi parafrase yang kompleks
- ✅ Memahami makna semantik, bukan hanya kata-kata
- ✅ State-of-the-art untuk similarity detection
- ✅ Pre-trained pada 1 billion+ sentence pairs

**Model Details:**
- Architecture: MPNet (Microsoft)
- Parameters: 110M
- Embedding Dimension: 768
- Training Data: MS MARCO, Natural Questions, S2ORC, etc.

**Kompleksitas:** O(n) untuk encoding

---

## 🔬 Pendekatan Multi-Algorithm

### Weighted Combination

Skor akhir dihitung dengan **weighted average**:

```
Overall Score = 0.25×Cosine + 0.25×N-gram + 0.25×Lexical + 0.25×Semantic
```

**Rationale:**
- Equal weights memastikan deteksi seimbang untuk semua jenis plagiarisme
- Dapat di-tune berdasarkan kebutuhan spesifik
- Mengurangi false positives/negatives dari satu algoritma

### Fragment Detection

**Algoritma:**
1. Split dokumen menjadi fragments (~100 characters)
2. Pre-filter dengan n-gram similarity (threshold 80%)
3. Detailed scoring dengan multi-algorithm approach
4. Return top 10 matches dengan score tertinggi

**Optimisasi:**
- Two-stage filtering mengurangi komputasi
- Sentence-based segmentation untuk konteks yang lebih baik

---

## 📈 Performa dan Optimalisasi

### 1. **Text Preprocessing**
- Lowercase normalization
- URL dan email removal
- Whitespace normalization
- Optional stopword removal (with caution)

### 2. **Lazy Loading**
- Sentence Transformer model loaded on-demand
- Menghemat memory untuk workloads ringan

### 3. **Efficient Vectorization**
- Max features limit (3000-5000)
- Character dan word n-grams optimized
- Sparse matrix representation (scipy)

### 4. **Scalability**
- Celery untuk distributed processing
- Shared model instances across workers
- Redis untuk message queue

---

## 🎓 Akurasi dan Validitas

### Coverage Matrix

| Jenis Plagiarisme | Cosine | N-gram | Lexical | Semantic |
|-------------------|--------|--------|---------|----------|
| Copy-Paste Exact | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Copy-Paste Minor Edit | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Word Substitution | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Paraphrase Ringan | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Paraphrase Complex | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Structure Change | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### Threshold Recommendations

- **High Risk (>0.70):** Kemungkinan besar plagiarisme
- **Medium Risk (0.40-0.70):** Perlu review manual
- **Low Risk (<0.40):** Kemungkinan kecil plagiarisme

---

## 🚀 Kemampuan Produksi

### Current Features
✅ Multi-format support (PDF, DOCX, TXT)
✅ 4 algoritma state-of-the-art
✅ Fragment-level detection
✅ Distributed processing (Celery)
✅ Error handling & recovery

### Future Enhancements
- [ ] FAISS vector indexing untuk corpus besar
- [ ] Elasticsearch integration untuk full-text search
- [ ] Database persistence (PostgreSQL)
- [ ] Citation extraction dan referensi
- [ ] Multi-language support
- [ ] Fine-tuned models untuk domain spesifik

---

## 📚 Referensi Ilmiah

1. **TF-IDF & Cosine Similarity:**
   - Salton, G., & McGill, M. J. (1983). Introduction to Modern Information Retrieval

2. **Fuzzy String Matching:**
   - Ratcliff, J. W., & Metzener, D. E. (1988). Pattern Matching: The Gestalt Approach

3. **Sentence Transformers:**
   - Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks
   - Song, K., et al. (2020). MPNet: Masked and Permuted Pre-training for Language Understanding

4. **Plagiarism Detection:**
   - Potthast, M., et al. (2014). Overview of the 6th International Competition on Plagiarism Detection

---

## 💡 Kesimpulan

Implementasi ini menggunakan **pendekatan state-of-the-art** yang menggabungkan:
- ✅ **Classical NLP** (TF-IDF, N-grams)
- ✅ **Modern Deep Learning** (Transformer-based embeddings)
- ✅ **Fuzzy Matching** (Toleran terhadap variasi)

Kombinasi ini memberikan **akurasi tinggi** untuk berbagai jenis plagiarisme, dari copy-paste sederhana hingga parafrase kompleks.

**Status:** ✅ Production-Ready dengan optimasi untuk akurasi dan performa.
