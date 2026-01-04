@echo off
REM Windows startup script for Resume Ranker

echo ========================================
echo     Resume Ranker - Startup Script
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Checking Docker installation...
docker --version
echo.

echo Building and starting services...
echo This may take a few minutes on first run...
echo.

REM Start Docker Compose
docker-compose up --build

echo.
echo ========================================
echo Services are running!
echo.
echo Frontend:  http://localhost:8501
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop services
echo ========================================

pause
