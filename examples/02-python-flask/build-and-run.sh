#!/bin/bash

echo "🔨 Building Flask image..."

# Build image
podman build -t flask-app:latest .

echo "✅ Image built!"
echo ""
echo "🚀 Running container..."

# Stop container if exists
podman stop flask-app 2>/dev/null
podman rm flask-app 2>/dev/null

# Run container
podman run -d \
  --name flask-app \
  -p 5000:5000 \
  flask-app:latest

echo "✅ Application started!"
echo "📍 Access at: http://localhost:5000"
echo ""
echo "🧪 Test the endpoints:"
echo "  curl http://localhost:5000"
echo "  curl http://localhost:5000/api/hello"
echo "  curl http://localhost:5000/api/time"
echo ""
echo "📋 View logs: podman logs -f flask-app"
