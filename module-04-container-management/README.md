# Module 4: Advanced Container Management

## 🎯 Module Objectives
- Work with environment variables
- Map ports correctly
- Manage logs and debugging
- Limit resources
- Automatically restart containers

---

## 🔧 Environment Variables

Environment variables are fundamental for configuring applications without modifying code.

### Passing Environment Variables

```bash
# Single variable
podman run -e MY_VARIABLE="value" alpine env

# Multiple variables
podman run \
  -e DB_HOST="localhost" \
  -e DB_PORT="5432" \
  -e DB_NAME="myapp" \
  alpine env

# From a file
podman run --env-file variables.env alpine env
```

**File variables.env:**
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=secret123
```

### Practical Example: MySQL

```bash
podman run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=mypassword \
  -e MYSQL_DATABASE=myapp \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=password123 \
  -p 3306:3306 \
  mysql:8.0

# View configured variables
podman inspect mysql-db | grep -A 10 "Env"
```

---

## 🔌 Port Mapping

### Basic Syntax

```bash
-p [HOST_IP:]HOST_PORT:CONTAINER_PORT[/protocol]
```

### Mapping Examples

```bash
# Port 8080 on host → port 80 in container
podman run -d -p 8080:80 nginx

# Multiple ports
podman run -d \
  -p 8080:80 \
  -p 8443:443 \
  nginx

# Specific IP
podman run -d -p 127.0.0.1:8080:80 nginx

# Random port on host
podman run -d -p 80 nginx

# View assigned port
podman port container

# Specify UDP protocol
podman run -d -p 5000:5000/udp my-app
```

### View Mapped Ports

```bash
# View ports of a specific container
podman port my-container

# List containers with their ports
podman ps --format "table {{.Names}}\t{{.Ports}}"
```

---

## 📊 Logs and Debugging

### `podman logs` Command

```bash
# View all logs
podman logs my-container

# Follow logs in real-time
podman logs -f my-container

# Last N lines
podman logs --tail 100 my-container

# Logs since certain time
podman logs --since 10m my-container
podman logs --since "2024-01-01T00:00:00"

# Logs until certain time
podman logs --until "2024-01-01T23:59:59" my-container

# With timestamps
podman logs -t my-container

# Combine options
podman logs -f --tail 50 -t my-container
```

### Container Debugging

#### View processes inside container

```bash
# List processes
podman top my-container

# With custom format
podman top my-container -eo pid,comm,args
```

#### Real-time statistics

```bash
# Stats of all containers
podman stats

# Stats of specific container
podman stats my-container

# Without stream (single sample)
podman stats --no-stream

# Custom format
podman stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

#### Inspect container

```bash
# All information
podman inspect my-container

# Container IP
podman inspect -f '{{.NetworkSettings.IPAddress}}' my-container

# Container state
podman inspect -f '{{.State.Status}}' my-container

# Environment variables
podman inspect -f '{{.Config.Env}}' my-container
```

#### Copy files from/to container

```bash
# Copy from container to host
podman cp my-container:/path/file.txt ./local-file.txt

# Copy from host to container
podman cp ./local-file.txt my-container:/path/destination/

# Copy entire directory
podman cp my-container:/app/logs ./logs-backup
```

---

## 💾 Resource Limitation

### Limit Memory

```bash
# Limit to 512 MB
podman run -m 512m nginx

# Limit with swap
podman run -m 512m --memory-swap 1g nginx

# Without swap
podman run -m 512m --memory-swap 512m nginx

# Soft limit (reservation)
podman run --memory-reservation 256m nginx
```

### Limit CPU

```bash
# Use 1.5 CPUs
podman run --cpus="1.5" nginx

# Use specific CPUs (0 and 1)
podman run --cpuset-cpus="0,1" nginx

# CPU shares (relative weight)
podman run --cpu-shares=512 nginx

# Limit % usage (50%)
podman run --cpu-quota=50000 nginx
```

### Complete Example with Limits

```bash
podman run -d \
  --name limited-app \
  --memory="512m" \
  --memory-reservation="256m" \
  --cpus="1.0" \
  --pids-limit 100 \
  nginx

# View applied limits
podman inspect limited-app | grep -i memory
```

---

## 🔄 Restart Policies

### Restart Options

```bash
# no: Don't restart (default)
podman run --restart=no nginx

# on-failure: Restart only if it fails
podman run --restart=on-failure nginx

# always: Always restart
podman run -d --restart=always nginx

# unless-stopped: Restart unless manually stopped
podman run -d --restart=unless-stopped nginx

# on-failure with attempt limit
podman run --restart=on-failure:5 nginx
```

### Practical Example

```bash
# Server that restarts automatically
podman run -d \
  --name web-server \
  --restart=always \
  -p 8080:80 \
  nginx

# Simulate failure (stop nginx)
podman exec web-server killall nginx

# Verify it restarted
podman ps
podman logs web-server
```

---

## 🏷️ Names and Labels

### Container Names

```bash
# Custom name
podman run -d --name my-application nginx

# Without name (automatically generated)
podman run -d nginx
```

### Labels

```bash
# Add labels
podman run -d \
  --label "environment=production" \
  --label "version=1.0" \
  --label "team=backend" \
  nginx

# Filter containers by label
podman ps -a --filter "label=environment=production"

# View container labels
podman inspect -f '{{.Config.Labels}}' my-container
```

---

## 🚪 Network Modes

### Network Types

```bash
# Default network (bridge)
podman run -d nginx

# Without network
podman run -d --network=none nginx

# Host network (use host network directly)
podman run -d --network=host nginx

# Custom network
podman network create my-network
podman run -d --network=my-network nginx
```

### Example: Communication between Containers

```bash
# Create custom network
podman network create app-network

# Create database
podman run -d \
  --name postgres-db \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Create application that connects to DB
podman run -d \
  --name my-app \
  --network app-network \
  -e DB_HOST=postgres-db \
  -e DB_PASSWORD=secret \
  -p 8080:8080 \
  my-application:latest

# App can access DB using the name "postgres-db"
```

---

## ⏱️ Healthchecks

### Define Healthcheck in Containerfile

```dockerfile
FROM nginx:alpine

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1
```

### Healthcheck at runtime

```bash
podman run -d \
  --name web-with-health \
  --health-cmd "curl -f http://localhost/ || exit 1" \
  --health-interval 30s \
  --health-timeout 3s \
  --health-retries 3 \
  nginx

# View health status
podman inspect --format='{{.State.Health.Status}}' web-with-health
```

---

## 🎯 Practical Use Cases

### Case 1: Web Application with Database

```bash
# 1. Create network
podman network create webapp-net

# 2. PostgreSQL database
podman run -d \
  --name postgres \
  --network webapp-net \
  -e POSTGRES_DB=myapp \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# 3. Web application
podman run -d \
  --name webapp \
  --network webapp-net \
  -e DB_HOST=postgres \
  -e DB_USER=admin \
  -e DB_PASSWORD=secret123 \
  -e DB_NAME=myapp \
  -p 8080:8080 \
  --restart=always \
  my-webapp:latest

# 4. Verify
podman ps
podman logs webapp
```

---

### Case 2: Development Server

```bash
# Development container with local volume
podman run -it \
  --name dev-container \
  --rm \
  -v $(pwd):/workspace:Z \
  -w /workspace \
  -p 3000:3000 \
  -p 5000:5000 \
  -e NODE_ENV=development \
  node:18 \
  bash

# Inside container you can develop
# Changes reflect on your local system
```

---

### Case 3: Microservices

```bash
# Network for microservices
podman network create microservices

# Authentication service
podman run -d \
  --name auth-service \
  --network microservices \
  -e JWT_SECRET=supersecret \
  -p 8001:8000 \
  auth-service:latest

# User service
podman run -d \
  --name user-service \
  --network microservices \
  -e AUTH_URL=http://auth-service:8000 \
  -p 8002:8000 \
  user-service:latest

# API Gateway
podman run -d \
  --name api-gateway \
  --network microservices \
  -e AUTH_SERVICE=http://auth-service:8000 \
  -e USER_SERVICE=http://user-service:8000 \
  -p 8080:8080 \
  api-gateway:latest
```

---

## 🧹 Maintenance

### Clean up resources

```bash
# Remove stopped containers
podman container prune

# Remove containers stopped more than 24h ago
podman container prune --filter "until=24h"

# View disk usage
podman system df

# Clean everything
podman system prune -a --volumes
```

### Real-time events

```bash
# View Podman events
podman events

# Filter events
podman events --filter container=my-container
podman events --filter event=start
```

---

## 🎓 Module Summary

You have learned:
- ✅ Use environment variables effectively
- ✅ Map ports correctly
- ✅ Debug containers with logs and stats
- ✅ Limit resources (CPU, memory)
- ✅ Configure restart policies
- ✅ Work with networks and communication between containers
- ✅ Practical use cases

---

## 📊 Cheat Sheet

```bash
# Environment variables
podman run -e VAR=value image
podman run --env-file file.env image

# Ports
podman run -p 8080:80 image
podman port container

# Logs
podman logs -f --tail 100 container

# Resources
podman run -m 512m --cpus="1.0" image

# Restart
podman run --restart=always image

# Networks
podman network create my-network
podman run --network my-network image

# Stats
podman stats container
podman top container
```

---

## ➡️ Next Step

**[Module 5: Volumes and Persistence](../module-05-volumes/README.md)**

---

## 💡 Practical Exercise

Create a complete stack with:
1. PostgreSQL database with persistent data
2. Backend API that connects to the DB
3. Everything on a custom network
4. With appropriate resource limits
5. Automatic restart configured
