#!/bin/bash
# Linux/Mac startup script for Resume Ranker

echo "========================================"
echo "     Resume Ranker - Startup Script"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed or not in PATH"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

echo "Checking Docker installation..."
docker --version
echo ""

echo "Building and starting services..."
echo "This may take a few minutes on first run..."
echo ""

# Start Docker Compose
docker-compose up --build

echo ""
echo "========================================"
echo "Services are running!"
echo ""
echo "Frontend:  http://localhost:8501"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop services"
echo "========================================"
