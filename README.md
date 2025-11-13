# 🔍  Plagiarism Checker

A production-grade plagiarism detection system with modern UI and advanced AI-powered similarity detection.

![Status](https://img.shields.io/badge/status-production%20ready-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)

## 🌟 Features

- **Modern UI**: Beautiful gradient design with professional results dashboard
- **Drag & Drop**: Easy file upload with drag-and-drop support
- **Real-time Analysis**: Live progress updates during document processing
- **Detailed Metrics**: Comprehensive similarity scores with visual progress bars
- **Multiple Algorithms**: Cosine, N-gram, Lexical, and Semantic matching
- **Fragment Detection**: Identifies specific matched content sections
- **Source Tracking**: Links to original sources when matches are found

## 📁 Project Structure

```
CheckTurnitin/
├── backend/          # FastAPI REST API
├── frontend/         # Next.js professional UI
├── worker/           # Celery background processing
└── infrastructure/   # Docker & deployment configs
```

## 🚀 Quick Start (Windows)

### Prerequisites
- Python 3.10+ 
- Node.js 18+
- (Optional) Redis for production processing

### 1. Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env

# Start API server
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

**Backend will be available at:** `http://localhost:8000`

### 2. Frontend Setup

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup environment
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env

# Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

### 3. Worker Setup (Optional - for real processing)

```powershell
# Navigate to worker
cd worker

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Set Redis URL
$env:REDIS_URL="redis://localhost:6379/0"

# Start worker
.\.venv\Scripts\python.exe -m celery -A worker.app worker --loglevel=INFO
```

**Note:** Worker requires Redis to be running. Without Redis, the app uses development fallback mode with mock results.

## 🎯 Usage

1. Open `http://localhost:3000` in your browser
2. Enter document title (optional)
3. Paste text or drag & drop a file (PDF, DOCX, TXT)
4. Click "🚀 Check for Plagiarism"
5. View detailed analysis results with:
   - Overall similarity score
   - Risk level indicator (Low/Medium/High)
   - Algorithm-specific metrics
   - Matched content fragments
   - Processing statistics

## 🔧 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/v1/upload` - Submit document for analysis
- `GET /api/v1/jobs/{job_id}` - Check analysis status
- `GET /api/v1/results/{job_id}` - Retrieve analysis results
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/register` - User registration

## 🎨 UI Features

### Upload Page
- Clean, modern design with gradient background
- Drag-and-drop file upload
- Real-time file size display
- Input validation and error handling
- Smooth animations and transitions

### Results Page
- Large, color-coded similarity score
- Risk level badges (Low/Medium/High)
- Progress bars for each algorithm
- Processing time and source count
- Matched fragment viewer
- Professional typography and spacing

## 🔐 Development vs Production

### Development Mode (Current)
- Uses mock data for instant results
- No external dependencies required
- Perfect for UI/UX testing
- Job IDs start with `dev_`

### Production Mode (With Redis + Worker)
- Real plagiarism detection algorithms
- Background job processing
- Database persistence
- Elasticsearch integration (planned)
- Vector similarity search (FAISS)

## 📦 Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- Celery - Distributed task queue
- SQLAlchemy - ORM
- Sentence Transformers - NLP embeddings
- FAISS - Vector similarity search

**Frontend:**
- Next.js 14 - React framework
- TypeScript - Type safety
- CSS-in-JS - Inline styling

**Infrastructure:**
- Redis - Message broker
- PostgreSQL - Database
- MinIO - Object storage
- Elasticsearch - Full-text search

## 🛠️ Configuration

**Backend** (`backend/.env`):
```env
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/plagiarism
JWT_SECRET=your-secret-key
```

**Frontend** (`frontend/.env`):
```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## 📝 Notes

- Development fallback allows testing without Redis/Celery
- Frontend auto-refreshes on code changes
- Backend hot-reloads with `--reload` flag
- All timestamps in UTC
- CORS enabled for local development

## 🔮 Roadmap

- [ ] User authentication & authorization
- [ ] Document history & management
- [ ] Export reports (PDF, DOCX)
- [ ] Batch processing
- [ ] API rate limiting
- [ ] Advanced NLP models
- [ ] Multi-language support
- [ ] Premium tier features

## 📄 License

This project is for educational and professional use.
