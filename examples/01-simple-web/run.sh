#!/bin/bash

echo "🚀 Starting simple web server..."

# Stop container if it already exists
podman stop simple-web 2>/dev/null
podman rm simple-web 2>/dev/null

# Run nginx with mounted volume
podman run -d \
  --name simple-web \
  -p 8080:80 \
  -v $(pwd):/usr/share/nginx/html:Z \
  nginx:alpine

echo "✅ Web server started!"
echo "📍 Access at: http://localhost:8080"
echo ""
echo "To view logs: podman logs -f simple-web"
echo "To stop: podman stop simple-web && podman rm simple-web"
