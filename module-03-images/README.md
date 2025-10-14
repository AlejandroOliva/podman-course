# Module 3: Working with Images

## 🎯 Module Objectives
- Understand what container images are
- Search for and download images
- Create your own images
- Manage local images
- Understand image layers

---

## 🖼️ What are Images?

A **container image** is an immutable template that contains:
- File system
- Applications and dependencies
- Environment variables
- Execution configuration

**Analogy**: If a container is a running process, the image is the program installed on disk.

### Image Structure

Images are formed by **layers**:
```
┌─────────────────────────┐
│   Layer 3: App + code   │
├─────────────────────────┤
│   Layer 2: Dependencies │
├─────────────────────────┤
│   Layer 1: Base system  │
└─────────────────────────┘
```

Each layer is read-only and reused between images.

---

## 🔍 Searching for Images

### Search in registries

```bash
# Search for images on Docker Hub
podman search nginx

# Search and limit results
podman search --limit 5 python

# Search only official images
podman search --filter is-official=true nginx

# View more details
podman search --list-tags nginx | head -20
```

### Common registries

- **Docker Hub**: docker.io (default)
- **Red Hat**: registry.redhat.io
- **Quay.io**: quay.io
- **GitHub**: ghcr.io

---

## ⬇️ Downloading Images

### `podman pull` Command

```bash
# Download an image (latest by default)
podman pull nginx

# Download a specific version
podman pull nginx:1.25

# Download from a specific registry
podman pull docker.io/library/nginx:alpine

# Download all versions of an image
podman pull --all-tags alpine
```

### Anatomy of an image name

```
[registry/][user/]name[:tag]
```

Examples:
- `nginx` → docker.io/library/nginx:latest
- `nginx:alpine` → docker.io/library/nginx:alpine
- `quay.io/podman/hello` → image from quay.io

---

## 📋 Listing Images

```bash
# List all local images
podman images

# Short format
podman images -q

# View images with more details
podman images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# View history of an image (its layers)
podman history nginx
```

**Typical output:**
```
REPOSITORY                TAG         IMAGE ID      CREATED       SIZE
docker.io/library/nginx   latest      605c77e624dd  2 weeks ago   141 MB
docker.io/library/alpine  latest      c059bfaa849c  3 weeks ago   5.59 MB
```

---

## 🏗️ Creating Your Own Images

### Method 1: Using Containerfile/Dockerfile

A **Containerfile** (or Dockerfile) is a text file with instructions to build an image.

#### Basic Example: Python Application

Create `Containerfile`:

```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Port the application exposes
EXPOSE 8000

# Default command
CMD ["python", "app.py"]
```

#### Build the image

```bash
# Basic syntax
podman build -t my-app:1.0 .

# With multiple tags
podman build -t my-app:1.0 -t my-app:latest .

# Specify the Containerfile
podman build -f Containerfile -t my-app .
```

---

## 📝 Containerfile Instructions

### Main Instructions

#### `FROM` - Base Image
```dockerfile
FROM ubuntu:22.04
FROM python:3.11-alpine
FROM scratch  # Empty image
```

#### `RUN` - Execute Commands
```dockerfile
# Install packages
RUN apt-get update && apt-get install -y curl

# Multiple commands (best practice)
RUN apt-get update && \
    apt-get install -y \
        curl \
        vim \
        git && \
    rm -rf /var/lib/apt/lists/*
```

#### `COPY` vs `ADD`
```dockerfile
# Copy files (recommended)
COPY file.txt /destination/
COPY src/ /app/

# ADD has extra functions (decompress, URLs)
ADD file.tar.gz /destination/  # Automatically decompresses
```

#### `WORKDIR` - Working Directory
```dockerfile
WORKDIR /app
# All following commands execute in /app
```

#### `ENV` - Environment Variables
```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV PATH="/app/bin:${PATH}"
```

#### `EXPOSE` - Document Ports
```dockerfile
EXPOSE 80
EXPOSE 443
EXPOSE 8080/tcp
```

#### `CMD` vs `ENTRYPOINT`

**CMD** - Default command (can be overridden):
```dockerfile
CMD ["python", "app.py"]
CMD ["nginx", "-g", "daemon off;"]
```

**ENTRYPOINT** - Main command (always executes):
```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]  # Only this can be overridden
```

#### `USER` - Execution User
```dockerfile
# Create non-root user
RUN useradd -m appuser
USER appuser
```

#### `ARG` - Build Arguments
```dockerfile
ARG VERSION=1.0
ARG BUILD_DATE
RUN echo "Building version ${VERSION}"
```

---

## 🎯 Complete Practical Examples

### Example 1: Static Web Server

**Containerfile:**
```dockerfile
FROM nginx:alpine

# Copy HTML files
COPY ./html /usr/share/nginx/html

# Copy custom configuration (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
```

**Build and run:**
```bash
# Create directory with HTML
mkdir -p html
echo "<h1>My Website!</h1>" > html/index.html

# Build
podman build -t my-website .

# Run
podman run -d -p 8080:80 --name web my-website

# Test
curl http://localhost:8080
```

---

### Example 2: Node.js Application

**Structure:**
```
my-app/
├── Containerfile
├── package.json
├── package-lock.json
└── server.js
```

**server.js:**
```javascript
const http = require('http');
const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello from Node.js on Podman!\n');
});

server.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

**package.json:**
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "Example app",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  }
}
```

**Containerfile:**
```dockerfile
FROM node:18-alpine

# Create non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy code
COPY server.js ./

# Switch to non-root user
USER appuser

EXPOSE 3000

CMD ["npm", "start"]
```

**Build and run:**
```bash
podman build -t my-node-app:1.0 .
podman run -d -p 3000:3000 --name node-app my-node-app:1.0
curl http://localhost:3000
```

---

### Example 3: Python Application with Flask

**Structure:**
```
flask-app/
├── Containerfile
├── requirements.txt
└── app.py
```

**app.py:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask!", "status": "ok"})

@app.route('/info')
def info():
    return jsonify({
        "app": "Flask on Podman",
        "version": "1.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

**requirements.txt:**
```
Flask==3.0.0
```

**Containerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (better cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

**Build and run:**
```bash
podman build -t flask-app:1.0 .
podman run -d -p 5000:5000 --name flask flask-app:1.0
curl http://localhost:5000
curl http://localhost:5000/info
```

---

## 🗑️ Managing Images

### Remove images

```bash
# Remove an image
podman rmi nginx

# Remove by ID
podman rmi 605c77e624dd

# Force removal
podman rmi -f nginx

# Remove unused images
podman image prune

# Remove ALL unused images
podman image prune -a
```

### Tag images

```bash
# Create new tag
podman tag my-app:1.0 my-app:latest

# Tag for a registry
podman tag my-app:1.0 quay.io/myuser/my-app:1.0
```

### Inspect images

```bash
# View image details
podman inspect nginx

# View only size
podman inspect -f '{{.Size}}' nginx

# View layers
podman history nginx
```

### Save and load images

```bash
# Save image to file
podman save -o nginx.tar nginx

# Load image from file
podman load -i nginx.tar

# Export container (not image)
podman export container > container.tar
```

---

## 🎨 Best Practices for Images

### 1. **Use small base images**
```dockerfile
# ❌ Avoid
FROM ubuntu

# ✅ Better
FROM alpine
FROM python:3.11-slim
```

### 2. **Order instructions by change frequency**
```dockerfile
# Layers that change less, first
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # This changes more frequently
```

### 3. **Combine RUN commands**
```dockerfile
# ❌ Creates multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim

# ✅ Single layer
RUN apt-get update && \
    apt-get install -y curl vim && \
    rm -rf /var/lib/apt/lists/*
```

### 4. **Use .containerignore / .dockerignore**
```
# .containerignore
node_modules/
.git/
*.log
.env
Containerfile
```

### 5. **Don't run as root**
```dockerfile
RUN useradd -m appuser
USER appuser
```

### 6. **Multi-stage builds**
```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Stage 2: Runtime
FROM alpine:latest
COPY --from=builder /app/myapp /usr/local/bin/
CMD ["myapp"]
```

---

## 🎓 Module Summary

You have learned:
- ✅ What images are and how they work
- ✅ Search for and download images
- ✅ Create images with Containerfile
- ✅ Main Containerfile instructions
- ✅ Complete practical examples
- ✅ Manage local images
- ✅ Best practices

---

## 📊 Cheat Sheet

```bash
podman search image                # Search for images
podman pull image:tag              # Download image
podman images                      # List images
podman build -t name:tag .         # Build image
podman history image               # View layers
podman inspect image               # View details
podman rmi image                   # Remove image
podman tag image new-tag           # Tag
podman save -o file.tar image      # Export
podman load -i file.tar            # Import
```

---

## ➡️ Next Step

**[Module 4: Advanced Container Management](../module-04-container-management/README.md)**

---

## 💡 Practical Exercise

Create a simple web application with your favorite language and containerize it with Podman. The app should:
1. Respond on an HTTP port
2. Return information about the app (name, version)
3. Use an appropriate base image
4. Run as non-root user
