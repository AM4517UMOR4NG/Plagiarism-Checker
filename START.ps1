# Quick Start Script untuk Plagiarism Checker
# Mode: Development (tanpa Redis)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Plagiarism Checker - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend venv exists
if (-not (Test-Path "backend\.venv")) {
    Write-Host "[1/4] Creating backend virtual environment..." -ForegroundColor Yellow
    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    cd ..
    Write-Host "✅ Backend environment created!" -ForegroundColor Green
} else {
    Write-Host "✅ Backend environment exists" -ForegroundColor Green
}

# Check if frontend node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[2/4] Installing frontend dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install
    cd ..
    Write-Host "✅ Frontend dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "✅ Frontend dependencies exist" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/4] Starting Backend Server..." -ForegroundColor Yellow
Write-Host "Opening new terminal for backend..." -ForegroundColor Gray

# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 3

Write-Host "[4/4] Starting Frontend Server..." -ForegroundColor Yellow
Write-Host "Opening new terminal for frontend..." -ForegroundColor Gray

# Start frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ Application Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open frontend in browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Tekan Ctrl+C di terminal backend/frontend untuk stop server" -ForegroundColor Yellow
