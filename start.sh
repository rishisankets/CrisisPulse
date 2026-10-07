#!/bin/bash

# CrisisPulse — Unified Local Development Runner
# Boots FastAPI backend and Vite frontend concurrently with clean exit handling

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "  🌍 CrisisPulse — Global Conflict & Response Tracker"
echo "=========================================================="

# Check Python Virtual Environment
if [ ! -d "backend/venv" ]; then
    echo "⚠️  backend/venv not detected. Creating virtualenv..."
    python3 -m venv backend/venv
    backend/venv/bin/pip install -r backend/requirements.txt
fi

# Cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down CrisisPulse services..."
    kill $(jobs -p) 2>/dev/null || true
    echo "✅ Shutdown complete."
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

echo "🚀 Starting FastAPI Backend on http://localhost:8000..."
backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend &
BACKEND_PID=$!

echo "⚡ Starting Vite Frontend on http://localhost:5173..."
npm --prefix frontend run dev &
FRONTEND_PID=$!

echo ""
echo "----------------------------------------------------------"
echo "  🌐 CrisisPulse Console:  http://localhost:5173"
echo "  📚 API Documentation:    http://localhost:8000/docs"
echo "----------------------------------------------------------"
echo "Press Ctrl+C to terminate both servers."
echo ""

wait
