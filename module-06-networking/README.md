# Module 6: Networking in Podman

## 🎯 Module Objectives
- Understand container networking concepts
- Know the types of networks in Podman
- Create and manage custom networks
- Connect containers to each other
- Expose services to the outside

---

## 🌐 Basic Network Concepts

### Why do we need networks?

- **Isolation**: Separate traffic between applications
- **Communication**: Allow containers to talk to each other
- **Security**: Control what can communicate with what
- **Organization**: Group related services

---

## 📡 Types of Networks in Podman

### 1. **Bridge** (Default)
- Private virtual network
- Containers can communicate with each other
- Isolated from outside (unless you expose ports)

### 2. **Host**
- Uses host network directly
- No isolation
- Better performance

### 3. **None**
- No network
- Completely isolated container

### 4. **Container**
- Share another container's network

---

## 🔧 Network Management

### Basic Commands

```bash
# List networks
podman network ls

# View network details
podman network inspect podman

# Create network
podman network create my-network

# Delete network
podman network rm my-network

# Delete unused networks
podman network prune
```

---

## 🏗️ Create Custom Networks

### Basic Network

```bash
# Create network with default configuration
podman network create app-network

# Verify
podman network inspect app-network
```

### Network with Specific Configuration

```bash
# Network with custom subnet
podman network create \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  my-custom-network

# Network with multiple subnets (IPv4 and IPv6)
podman network create \
  --subnet 172.21.0.0/16 \
  --subnet 2001:db8::/64 \
  my-dual-network
```

### Advanced Options

```bash
# Network with custom DNS
podman network create \
  --subnet 172.22.0.0/16 \
  --dns 8.8.8.8 \
  --dns 8.8.4.4 \
  my-dns-network

# Network with IP range
podman network create \
  --subnet 172.23.0.0/16 \
  --ip-range 172.23.5.0/24 \
  --gateway 172.23.5.254 \
  my-range-network
```

---

## 🔌 Connect Containers to Networks

### When Creating Container

```bash
# Use custom network
podman run -d \
  --name web \
  --network my-network \
  nginx

# Without network
podman run -d \
  --name isolated \
  --network none \
  alpine

# Host network
podman run -d \
  --name app-host \
  --network host \
  nginx
```

### Connect/Disconnect Dynamically

```bash
# Create container
podman run -d --name app nginx

# Connect to existing network
podman network connect my-network app

# Container can be on multiple networks
podman network connect another-network app

# Disconnect from network
podman network disconnect my-network app
```

---

## 💬 Communication between Containers

### Automatic DNS Resolution

In custom networks, containers can communicate using their names:

```bash
# Create network
podman network create app-net

# Create database
podman run -d \
  --name database \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Create application that connects to DB
podman run -d \
  --name backend \
  --network app-net \
  -e DB_HOST=database \
  -e DB_PASSWORD=secret \
  my-backend:latest

# Backend can connect to "database" directly
```

### Practical Example: Complete Web Application

```bash
# 1. Create network
podman network create webapp

# 2. Database
podman run -d \
  --name postgres \
  --network webapp \
  -e POSTGRES_DB=myapp \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=pass123 \
  postgres:15

# 3. Backend API
podman run -d \
  --name api \
  --network webapp \
  -e DATABASE_URL=postgresql://admin:pass123@postgres:5432/myapp \
  my-api:latest

# 4. Frontend
podman run -d \
  --name frontend \
  --network webapp \
  -e API_URL=http://api:8000 \
  -p 8080:80 \
  my-frontend:latest

# Only frontend is accessible from outside (port 8080)
# Postgres and API are isolated in the internal network
```

---

## 🔍 Inspect Networks

### View Containers on a Network

```bash
# View network details
podman network inspect my-network

# View only connected containers
podman network inspect -f '{{range .Containers}}{{.Name}} {{end}}' my-network
```

### View Container Networks

```bash
# Inspect container
podman inspect -f '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}} {{end}}' my-container

# View container IP
podman inspect -f '{{.NetworkSettings.IPAddress}}' my-container

# View all IPs (all networks)
podman inspect -f '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}}: {{$conf.IPAddress}} {{end}}' my-container
```

---

## 🚪 Advanced Port Mapping

### Complete Syntax

```bash
-p [HOST_IP:]HOST_PORT:CONTAINER_PORT[/PROTOCOL]
```

### Examples

```bash
# Basic: Host:Container
podman run -d -p 8080:80 nginx

# Specific IP
podman run -d -p 127.0.0.1:8080:80 nginx

# Multiple ports
podman run -d \
  -p 8080:80 \
  -p 8443:443 \
  nginx

# Random port on host
podman run -d -p 80 nginx

# UDP protocol
podman run -d -p 5000:5000/udp my-app

# Port range
podman run -d -p 8080-8090:8080-8090 my-app
```

### View Mapped Ports

```bash
# View ports of a container
podman port my-container

# View all mapped ports
podman ps --format "table {{.Names}}\t{{.Ports}}"
```

---

## 🏢 Practical Use Cases

### Case 1: Microservices

```bash
# Network for microservices
podman network create microservices

# User service
podman run -d \
  --name user-service \
  --network microservices \
  user-service:latest

# Product service
podman run -d \
  --name product-service \
  --network microservices \
  product-service:latest

# Order service (connects with other services)
podman run -d \
  --name order-service \
  --network microservices \
  -e USER_SERVICE_URL=http://user-service:8000 \
  -e PRODUCT_SERVICE_URL=http://product-service:8000 \
  order-service:latest

# API Gateway (single entry point)
podman run -d \
  --name gateway \
  --network microservices \
  -p 8080:8080 \
  -e USER_SERVICE=http://user-service:8000 \
  -e PRODUCT_SERVICE=http://product-service:8000 \
  -e ORDER_SERVICE=http://order-service:8000 \
  api-gateway:latest
```

---

### Case 2: Development with Frontend and Backend

```bash
# Development network
podman network create dev-network

# Database
podman run -d \
  --name dev-db \
  --network dev-network \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=devpass \
  postgres:15

# Backend in development mode
podman run -d \
  --name dev-backend \
  --network dev-network \
  -v $(pwd)/backend:/app:Z \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://postgres:devpass@dev-db:5432/devdb \
  -e FLASK_ENV=development \
  python:3.11

# Frontend in development mode
podman run -d \
  --name dev-frontend \
  --network dev-network \
  -v $(pwd)/frontend:/app:Z \
  -p 3000:3000 \
  -e REACT_APP_API_URL=http://localhost:5000 \
  node:18
```

---

### Case 3: Testing Environment

```bash
# Isolated test network
podman network create test-network

# Test services
podman run -d --name test-db --network test-network postgres:15-alpine
podman run -d --name test-redis --network test-network redis:alpine
podman run -d --name test-api --network test-network my-api:test

# Run tests
podman run --rm \
  --network test-network \
  -e API_URL=http://test-api:8000 \
  my-tests:latest

# Cleanup
podman stop test-db test-redis test-api
podman rm test-db test-redis test-api
podman network rm test-network
```

---

### Case 4: Reverse Proxy

```bash
# Network for applications
podman network create apps

# Application 1
podman run -d \
  --name app1 \
  --network apps \
  my-app:v1

# Application 2
podman run -d \
  --name app2 \
  --network apps \
  my-app:v2

# Nginx as reverse proxy
cat > nginx.conf << 'EOF'
events {}
http {
    upstream app1 {
        server app1:8000;
    }
    upstream app2 {
        server app2:8000;
    }
    server {
        listen 80;
        location /app1/ {
            proxy_pass http://app1/;
        }
        location /app2/ {
            proxy_pass http://app2/;
        }
    }
}
EOF

podman run -d \
  --name proxy \
  --network apps \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:Z \
  -p 8080:80 \
  nginx
```

---

## 🔒 Security and Isolation

### Separate Networks by Environment

```bash
# Production network
podman network create --subnet 172.30.0.0/16 prod-network

# Staging network
podman network create --subnet 172.31.0.0/16 staging-network

# Development network
podman network create --subnet 172.32.0.0/16 dev-network

# Containers on different networks are completely isolated
```

### Containers without Network

```bash
# For maximum isolation
podman run -d \
  --name isolated-service \
  --network none \
  my-app:latest

# Useful for data processing without network need
```

---

## 🛠️ Network Troubleshooting

### Verify Connectivity

```bash
# Ping between containers
podman exec container1 ping -c 3 container2

# Verify DNS
podman exec container1 nslookup container2

# View routes
podman exec container ip route

# View network interfaces
podman exec container ip addr
```

### Debugging Tools

```bash
# Container with network tools
podman run -it --rm \
  --network my-network \
  nicolaka/netshoot

# From there you can use: ping, nslookup, curl, tcpdump, etc.
```

### View Network Logs

```bash
# View network events
podman events --filter type=network

# View container connections
podman exec container netstat -tulpn
```

---

## 📊 Network Mode Comparison

| Mode | Isolation | Performance | Use | External Access |
|------|-----------|-------------|-----|-----------------|
| **bridge** | High | Good | Default, normal apps | Via port mapping |
| **host** | None | Excellent | High performance | Direct |
| **none** | Total | N/A | Maximum security | None |
| **container** | Shared | Good | Pods, sidecars | Depends |

---

## 🎓 Module Summary

You have learned:
- ✅ Basic networking concepts in containers
- ✅ Types of networks in Podman
- ✅ Create and manage custom networks
- ✅ Connect containers to each other
- ✅ Automatic DNS resolution
- ✅ Advanced port mapping
- ✅ Practical use cases (microservices, development, etc.)
- ✅ Security and isolation
- ✅ Network troubleshooting

---

## 📊 Cheat Sheet

```bash
# Network management
podman network create name
podman network ls
podman network inspect name
podman network rm name
podman network prune

# Use networks
podman run --network name image
podman run --network host image
podman run --network none image

# Connect/Disconnect
podman network connect network container
podman network disconnect network container

# Ports
podman run -p 8080:80 image
podman port container

# Troubleshooting
podman exec container ping another-container
podman exec container ip addr
```

---

## ➡️ Next Step

**[Module 7: Pods - Podman's Unique Feature](../module-07-pods/README.md)**

---

## 💡 Practical Exercise

Create a 3-tier architecture:
1. Backend network with: PostgreSQL + Redis
2. Frontend network with: Web application
3. DMZ network with: Nginx as reverse proxy
4. Only Nginx should be accessible from outside
5. Verify that layers can communicate correctly
