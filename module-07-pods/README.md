# Module 7: Pods - Podman's Unique Feature

## 🎯 Module Objectives
- Understand what Pods are
- Know the advantages of using Pods
- Create and manage Pods
- Work with containers inside Pods
- Generate Kubernetes files from Pods

---

## 🎪 What are Pods?

A **Pod** is a group of one or more containers that:
- Share the same network namespace
- Share the same IPC (inter-process communication)
- Can share volumes
- Are managed as a single unit

### Kubernetes Concept

Pods are the fundamental concept in Kubernetes. Podman brings this functionality to the local level, without needing a cluster.

```
┌─────────────────────────────────────┐
│            POD                      │
│  ┌─────────────┐  ┌──────────────┐ │
│  │ Container   │  │ Container    │ │
│  │   Nginx     │  │   App        │ │
│  └─────────────┘  └──────────────┘ │
│         ↑                ↑          │
│         └────────┬───────┘          │
│            Shared network           │
│         (localhost between them)    │
└─────────────────────────────────────┘
```

---

## 🌟 Advantages of using Pods

1. **Communication via localhost**: Containers communicate via `localhost`
2. **Unified management**: Start/stop/delete all containers at once
3. **Kubernetes compatibility**: Easy migration to K8s
4. **Organization**: Group related services
5. **Sidecars**: Implement patterns like logging, monitoring

---

## 🚀 Create and Manage Pods

### Basic Commands

```bash
# Create an empty Pod
podman pod create --name my-pod

# Create Pod with mapped port
podman pod create --name web-pod -p 8080:80

# List Pods
podman pod ls

# View containers in a Pod
podman pod ps -a

# Inspect Pod
podman pod inspect my-pod

# Stop Pod (stops all containers)
podman pod stop my-pod

# Start Pod
podman pod start my-pod

# Restart Pod
podman pod restart my-pod

# Delete Pod (deletes all containers)
podman pod rm my-pod

# Force delete Pod
podman pod rm -f my-pod
```

---

## 🏗️ Working with Containers in Pods

### Add Containers to a Pod

```bash
# 1. Create Pod
podman pod create --name app-pod -p 8080:80

# 2. Add nginx container
podman run -d \
  --pod app-pod \
  --name webserver \
  nginx:alpine

# 3. Add application container
podman run -d \
  --pod app-pod \
  --name app \
  my-application:latest

# Containers can communicate via localhost
```

### Example: Web App + Redis

```bash
# Create Pod
podman pod create --name webapp-pod -p 8080:5000

# Add Redis
podman run -d \
  --pod webapp-pod \
  --name redis \
  redis:alpine

# Add Flask app that uses Redis
podman run -d \
  --pod webapp-pod \
  --name flask-app \
  -e REDIS_HOST=localhost \
  my-flask-app:latest

# Flask can connect to Redis using "localhost:6379"
```

---

## 🎯 Practical Examples

### Example 1: Complete Web Stack

```bash
# Create Pod with necessary ports
podman pod create --name webstack \
  -p 8080:80 \
  -p 8443:443

# Database
podman run -d \
  --pod webstack \
  --name db \
  -e POSTGRES_PASSWORD=secret \
  postgres:15-alpine

# Backend API
podman run -d \
  --pod webstack \
  --name api \
  -e DB_HOST=localhost \
  -e DB_PASSWORD=secret \
  my-backend:latest

# Frontend Nginx
podman run -d \
  --pod webstack \
  --name web \
  -e API_URL=http://localhost:8000 \
  my-frontend:latest

# View all Pod containers
podman ps --filter pod=webstack
```

---

### Example 2: Application with Log Sidecar

```bash
# Create Pod
podman pod create --name app-with-logs -p 8080:8080

# Shared volume for logs
podman volume create logs-shared

# Main application
podman run -d \
  --pod app-with-logs \
  --name app \
  -v logs-shared:/var/log/app \
  my-application:latest

# Sidecar to process logs
podman run -d \
  --pod app-with-logs \
  --name log-processor \
  -v logs-shared:/logs:ro \
  alpine \
  sh -c "tail -f /logs/app.log | grep ERROR"

# Sidecar to export metrics
podman run -d \
  --pod app-with-logs \
  --name metrics \
  -v logs-shared:/logs:ro \
  prometheus-exporter:latest
```

---

### Example 3: Development Pod

```bash
# Pod for development with all tools
podman pod create --name devpod \
  -p 3000:3000 \
  -p 5000:5000 \
  -p 8080:8080

# Database for development
podman run -d \
  --pod devpod \
  --name dev-db \
  -e POSTGRES_PASSWORD=devpass \
  postgres:15-alpine

# Redis for cache
podman run -d \
  --pod devpod \
  --name dev-redis \
  redis:alpine

# Main development container
podman run -it \
  --pod devpod \
  --name dev-env \
  -v $(pwd):/workspace:Z \
  -w /workspace \
  python:3.11 \
  bash

# From dev-env you can access everything via localhost
```

---

### Example 4: Microservices in a Pod

```bash
# Pod for related microservices
podman pod create --name micro-pod -p 8080:8080

# Authentication service
podman run -d \
  --pod micro-pod \
  --name auth \
  auth-service:latest

# User service
podman run -d \
  --pod micro-pod \
  --name users \
  -e AUTH_URL=http://localhost:8001 \
  user-service:latest

# API Gateway
podman run -d \
  --pod micro-pod \
  --name gateway \
  -e AUTH_SERVICE=http://localhost:8001 \
  -e USER_SERVICE=http://localhost:8002 \
  gateway:latest
```

---

## 🔧 Advanced Pod Options

### Create Pod with Options

```bash
# Pod with custom hostname
podman pod create --name mypod --hostname my-application

# Pod with custom DNS
podman pod create --name mypod --dns 8.8.8.8 --dns 8.8.4.4

# Pod with custom network
podman network create my-network
podman pod create --name mypod --network my-network

# Pod with labels
podman pod create --name mypod \
  --label app=webapp \
  --label version=1.0 \
  --label env=production

# Pod sharing IPC and PID namespace
podman pod create --name mypod \
  --share ipc,net,uts
```

---

## 📦 Advanced Management

### View Detailed Status

```bash
# View Pods with custom format
podman pod ps --format "table {{.ID}}\t{{.Name}}\t{{.Status}}\t{{.Created}}"

# View all containers (includes infra)
podman ps -a --pod

# View only Pod IDs
podman pod ps -q

# Filter Pods by status
podman pod ps --filter status=running
```

### Pod Logs

```bash
# View logs from all Pod containers
podman pod logs my-pod

# Logs from specific container in Pod
podman logs webstack-app

# Follow logs in real-time
podman pod logs -f my-pod
```

### Statistics

```bash
# Stats of containers in a Pod
podman stats --pod=my-pod

# Stats of all Pods
podman pod stats
```

---

## 🔍 The Infra Container

Each Pod has a special **infra container** that:
- Maintains namespaces (network, IPC, etc.)
- Is created automatically
- Uses very few resources (image: `k8s.gcr.io/pause`)
- Is named `<pod-name>-infra`

```bash
# View the infra container
podman ps -a --filter label=io.podman.annotations.infra=true

# You shouldn't interact with it directly
```

---

## ☸️ Generate Kubernetes Files

### From Pod to Kubernetes YAML

```bash
# Generate YAML from a Pod
podman generate kube my-pod > my-pod.yaml

# Generate with Kubernetes service
podman generate kube --service my-pod > my-pod-service.yaml
```

**Example output (my-pod.yaml):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: app
    image: my-application:latest
    ports:
    - containerPort: 8080
      hostPort: 8080
  - name: redis
    image: redis:alpine
```

### From Kubernetes YAML to Pod

```bash
# Create Pod from Kubernetes file
podman play kube my-pod.yaml

# Delete Pod created from YAML
podman play kube --down my-pod.yaml

# Recreate (delete and create again)
podman play kube --replace my-pod.yaml
```

---

## 🎨 Complete Example: WordPress Application

```bash
# 1. Create Pod
podman pod create --name wordpress-pod \
  -p 8080:80 \
  --label app=wordpress

# 2. Add MySQL
podman run -d \
  --pod wordpress-pod \
  --name wp-db \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wpuser \
  -e MYSQL_PASSWORD=wppass \
  -v wp-db-data:/var/lib/mysql \
  mysql:8.0

# 3. Wait for MySQL to start
sleep 10

# 4. Add WordPress
podman run -d \
  --pod wordpress-pod \
  --name wordpress \
  -e WORDPRESS_DB_HOST=localhost \
  -e WORDPRESS_DB_USER=wpuser \
  -e WORDPRESS_DB_PASSWORD=wppass \
  -e WORDPRESS_DB_NAME=wordpress \
  -v wp-data:/var/www/html \
  wordpress:latest

# 5. Access http://localhost:8080

# 6. View status
podman pod ps
podman ps --pod

# 7. View logs
podman logs wordpress
podman logs wp-db

# 8. Generate YAML
podman generate kube wordpress-pod > wordpress-pod.yaml

# 9. Stop everything
podman pod stop wordpress-pod

# 10. Delete everything
podman pod rm -f wordpress-pod
```

---

## 🔄 Migration to Kubernetes

### Development Workflow

```bash
# 1. Develop locally with Pods
podman pod create --name myapp -p 8080:80
podman run -d --pod myapp --name web nginx
podman run -d --pod myapp --name api my-api:latest

# 2. Generate YAML for Kubernetes
podman generate kube myapp > myapp-k8s.yaml

# 3. Adjust YAML if necessary
vim myapp-k8s.yaml

# 4. Deploy in Kubernetes
kubectl apply -f myapp-k8s.yaml
```

---

## 🎭 Design Patterns with Pods

### 1. Sidecar Pattern
An auxiliary container that complements the main one:
- Logs, metrics, monitoring
- Proxy, SSL termination
- Data synchronization

```bash
podman pod create --name app-sidecar -p 8080:8080

# Main
podman run -d --pod app-sidecar --name app my-app:latest

# Log sidecar
podman run -d --pod app-sidecar --name logger log-collector:latest
```

### 2. Ambassador Pattern
Proxy that manages external connections:

```bash
podman pod create --name app-ambassador

# Application
podman run -d --pod app-ambassador --name app my-app:latest

# Ambassador (proxy to external services)
podman run -d --pod app-ambassador --name proxy ambassador-proxy:latest
```

### 3. Adapter Pattern
Normalizes output for external systems:

```bash
podman pod create --name app-adapter -p 9090:9090

# Application with proprietary format
podman run -d --pod app-adapter --name app legacy-app:latest

# Adapter (converts to Prometheus format)
podman run -d --pod app-adapter --name adapter metrics-adapter:latest
```

---

## 🛡️ Security in Pods

```bash
# Pod with non-root user
podman pod create --name secure-pod \
  --userns keep-id \
  -p 8080:8080

# Containers in Pod inherit security configuration
podman run -d --pod secure-pod --name app my-app:latest
```

---

## 🎓 Module Summary

You have learned:
- ✅ What Pods are and why they're unique in Podman
- ✅ Advantages of grouping containers in Pods
- ✅ Create and manage Pods
- ✅ Add containers to existing Pods
- ✅ Communication via localhost between containers
- ✅ Generate Kubernetes files from Pods
- ✅ Design patterns (Sidecar, Ambassador, Adapter)
- ✅ Migration from local Pods to Kubernetes

---

## 📊 Cheat Sheet

```bash
# Pod management
podman pod create --name name -p 8080:80
podman pod ls
podman pod ps
podman pod inspect name
podman pod start name
podman pod stop name
podman pod restart name
podman pod rm name

# Containers in Pods
podman run -d --pod name --name container image
podman ps --pod

# Kubernetes
podman generate kube pod > pod.yaml
podman play kube pod.yaml
podman play kube --down pod.yaml

# Logs and Stats
podman pod logs pod
podman pod stats
```

---

## ➡️ Next Step

**[Module 8: Podman Compose](../module-08-compose/README.md)**

---

## 💡 Practical Exercise

Create a Pod with:
1. A web application (Flask/Node/whatever you prefer)
2. Redis for cache
3. A sidecar that shows logs in real-time
4. Everything must communicate via localhost
5. Generate the Kubernetes YAML file
6. Verify it works by recreating it from YAML
