# 🚀 Cara Menjalankan Aplikasi Plagiarism Checker

## ⚡ Cara Tercepat (RECOMMENDED)

### **Option 1: Gunakan Script Otomatis**

```powershell
# Di folder CheckTurnitin
.\START.ps1
```

Script ini akan otomatis:
- ✅ Setup virtual environment (jika belum ada)
- ✅ Install dependencies
- ✅ Start Backend di terminal baru
- ✅ Start Frontend di terminal baru
- ✅ Buka browser otomatis

**Selesai! Tunggu beberapa detik dan aplikasi siap digunakan.**

---

### **Option 2: Manual Step-by-Step**

#### **Terminal 1: Backend**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

#### **Terminal 2: Frontend** (Terminal BARU)
```powershell
cd frontend
npm run dev
```

#### **Akses Aplikasi:**
Buka browser → **http://localhost:3000**

---

## 🧪 Test Algoritma

Untuk memverifikasi algoritma berjalan dengan baik:

```powershell
cd worker
pip install -r requirements.txt
python test_algorithms.py
```

Expected output:
```
✅ ALL TESTS PASSED!
Algoritma plagiarism detection berhasil diimplementasikan
dan berfungsi dengan optimal!
```

---

## 📋 First Time Setup

### **Backend Setup:**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **Frontend Setup:**
```powershell
cd frontend
npm install
```

### **Worker Setup (Optional):**
```powershell
cd worker
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎮 Cara Menggunakan

1. **Upload Dokumen:**
   - Paste teks di text area, ATAU
   - Drag & drop file (PDF, DOCX, TXT)

2. **Klik "🚀 Check for Plagiarism"**

3. **Lihat Hasil:**
   - Overall Similarity Score
   - Risk Level (Low/Medium/High)
   - 4 Algoritma Breakdown:
     * Cosine Similarity (character-level)
     * N-gram Matching (fuzzy)
     * Lexical Similarity (word-level)
     * Semantic Similarity (BERT)
   - Matching Fragments
   - Processing Time

---

## 🔥 Mode Production (dengan Worker)

Untuk production dengan background processing:

### **1. Install & Start Redis:**

**Option A: Docker (Recommended)**
```powershell
docker run -d -p 6379:6379 redis:alpine
```

**Option B: Native Windows**
```powershell
choco install redis-64
redis-server
```

### **2. Start Backend:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

### **3. Start Worker:**
```powershell
cd worker
.\.venv\Scripts\Activate.ps1
$env:REDIS_URL="redis://localhost:6379/0"
python -m celery -A worker.app worker --loglevel=INFO --pool=solo
```

### **4. Start Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 🛠️ Troubleshooting

### **"Port 8000 already in use"**
```powershell
# Gunakan port lain
python -m uvicorn app.main:app --reload --port 8001

# Update frontend .env
# NEXT_PUBLIC_API_BASE=http://localhost:8001
```

### **"Module not found" di Backend**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **"Command not found: npm"**
Install Node.js dari: https://nodejs.org/

### **Frontend tidak connect ke Backend**
Check `frontend\.env`:
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### **Algoritma tidak jalan (masih mock data)**
- Mode Development: Algoritma SUDAH jalan otomatis ✅
- Mode Production: Pastikan Worker running dengan Redis

---

## 📊 Status Check

### **Backend:**
```
GET http://localhost:8000/health
```
Expected: `{"status": "healthy"}`

### **Frontend:**
```
http://localhost:3000
```
Expected: Landing page dengan upload form

### **Algoritma:**
```powershell
cd worker
python test_algorithms.py
```
Expected: All tests passed

---

## 🎯 Quick Reference

| Component | Command | URL |
|-----------|---------|-----|
| **Backend** | `uvicorn app.main:app --reload --port 8000` | http://localhost:8000 |
| **Frontend** | `npm run dev` | http://localhost:3000 |
| **Worker** | `celery -A worker.app worker --pool=solo` | - |
| **Redis** | `redis-server` | localhost:6379 |
| **Test** | `python test_algorithms.py` | - |

---

## 📝 Environment Variables

### **Backend** (`backend\.env`):
```env
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/plagiarism
JWT_SECRET=your-secret-key
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### **Frontend** (`frontend\.env`):
```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

---

## ⚙️ Recommended Workflow

### **Untuk Development/Testing:**
1. Run `.\START.ps1` ATAU
2. Backend + Frontend manual

### **Untuk Production:**
1. Setup Redis
2. Backend + Worker + Frontend

### **Untuk Testing Algoritma:**
```powershell
cd worker
python test_algorithms.py
```

---

## 💡 Tips

1. **First time running:**
   - Tunggu 1-2 menit saat pertama kali (download BERT model ~438MB)
   - Model akan di-cache untuk run selanjutnya

2. **Faster startup:**
   - Keep terminal backend/frontend tetap running
   - Reload otomatis saat edit code

3. **Performance:**
   - Development mode: 600-1000ms per dokumen
   - Production mode dengan caching: lebih cepat

4. **Memory usage:**
   - BERT model: ~1-2GB RAM
   - Tutup aplikasi lain jika RAM terbatas

---

## 🎉 Success Indicators

✅ Backend terminal shows:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

✅ Frontend terminal shows:
```
✓ Ready in 2.5s
○ Local:   http://localhost:3000
```

✅ Browser shows:
- Landing page dengan upload form
- Gradient background professional

✅ Test shows:
```
✅ ALL TESTS PASSED!
```

---

## 📞 Need Help?

1. **Check logs** di terminal backend/frontend
2. **Run tests**: `python test_algorithms.py`
3. **Verify setup**: 
   - Python 3.10+ installed
   - Node.js 18+ installed
   - All dependencies installed

---

**Quick Start:** `.\START.ps1`  
**Test Algoritma:** `cd worker && python test_algorithms.py`  
**Access App:** http://localhost:3000  

**Happy Checking! 🚀**
