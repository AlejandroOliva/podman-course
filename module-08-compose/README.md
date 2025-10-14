# Module 8: Podman Compose

## 🎯 Module Objectives
- Understand what Podman Compose is
- Install and configure Podman Compose
- Create docker-compose.yml files for Podman
- Manage multi-container applications
- Migrate from Docker Compose to Podman

---

## 📦 What is Podman Compose?

**Podman Compose** is a tool that allows you to use `docker-compose.yml` files with Podman. It's compatible with Docker Compose and facilitates managing multi-container applications.

### Alternatives

1. **podman-compose**: Python implementation of docker-compose for Podman
2. **podman generate/play kube**: Native to Podman, uses Kubernetes YAML
3. **docker-compose** directly (configuring Podman socket)

---

## 🔧 Installing Podman Compose

### On Ubuntu/Debian

```bash
# Install pip if not installed
sudo apt install python3-pip

# Install podman-compose
pip3 install podman-compose

# Verify installation
podman-compose version

# Add to PATH if necessary
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### On Fedora/RHEL

```bash
# Install from repositories
sudo dnf install podman-compose

# Or with pip
pip3 install podman-compose

# Verify
podman-compose version
```

### On macOS

```bash
# With Homebrew
brew install podman-compose

# Or with pip
pip3 install podman-compose
```

---

## 📝 docker-compose.yml Structure

### Basic File

```yaml
version: '3'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  app:
    image: python:3.11-slim
    command: python app.py
    volumes:
      - ./app:/app
    working_dir: /app
```

### Main Sections

- **version**: Specification version (3, 3.8, 3.9)
- **services**: Container definitions
- **networks**: Custom networks
- **volumes**: Named volumes
- **configs**: Configurations
- **secrets**: Sensitive data

---

## 🚀 Podman Compose Commands

### Basic Commands

```bash
# Start services
podman-compose up

# Start in background
podman-compose up -d

# View logs
podman-compose logs

# Follow logs in real-time
podman-compose logs -f

# View service status
podman-compose ps

# Stop services
podman-compose stop

# Stop and remove containers
podman-compose down

# Stop, remove, and delete volumes
podman-compose down -v

# Rebuild images
podman-compose build

# Rebuild and start
podman-compose up --build

# Execute command in service
podman-compose exec service command

# Scale service
podman-compose up -d --scale web=3
```

---

## 🎯 Practical Examples

### Example 1: Simple Web Application

**File structure:**
```
project/
├── docker-compose.yml
├── html/
│   └── index.html
└── app/
    ├── app.py
    └── requirements.txt
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    container_name: web-server
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:Z
    depends_on:
      - app
    networks:
      - frontend

  app:
    image: python:3.11-slim
    container_name: python-app
    command: python -m http.server 8000
    working_dir: /app
    volumes:
      - ./app:/app:Z
    networks:
      - frontend

networks:
  frontend:
    driver: bridge
```

**Run:**
```bash
# Create content
mkdir -p html app
echo "<h1>Hello Podman Compose</h1>" > html/index.html
echo "print('App running')" > app/app.py

# Start
podman-compose up -d

# View logs
podman-compose logs -f

# Verify
curl http://localhost:8080

# Stop
podman-compose down
```

---

### Example 2: LAMP Stack (Linux, Apache, MySQL, PHP)

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: mysql-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: myapp
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - backend

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: phpmyadmin
    restart: always
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpassword
    depends_on:
      - db
    networks:
      - backend
      - frontend

  web:
    image: php:8.2-apache
    container_name: web-server
    restart: always
    ports:
      - "8080:80"
    volumes:
      - ./www:/var/www/html:Z
    depends_on:
      - db
    networks:
      - frontend
      - backend

volumes:
  db-data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

**Run:**
```bash
# Create web directory
mkdir -p www
cat > www/index.php << 'EOF'
<?php
$host = 'db';
$user = 'user';
$pass = 'password';
$db = 'myapp';

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully to MySQL!<br>";
echo "PHP Version: " . phpversion();
?>
EOF

# Start stack
podman-compose up -d

# Access at:
# - Application: http://localhost:8080
# - phpMyAdmin: http://localhost:8081
```

---

### Example 3: MERN Application (MongoDB, Express, React, Node)

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6
    container_name: mongodb
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: adminpass
    volumes:
      - mongo-data:/data/db
    networks:
      - mern-network

  backend:
    build: ./backend
    container_name: backend-api
    restart: always
    environment:
      PORT: 5000
      MONGODB_URI: mongodb://admin:adminpass@mongodb:27017/
      NODE_ENV: development
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app:Z
      - /app/node_modules
    networks:
      - mern-network

  frontend:
    build: ./frontend
    container_name: frontend-react
    restart: always
    environment:
      REACT_APP_API_URL: http://localhost:5000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app:Z
      - /app/node_modules
    networks:
      - mern-network

volumes:
  mongo-data:

networks:
  mern-network:
    driver: bridge
```

**backend/Containerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

**frontend/Containerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

---

### Example 4: Microservices with Redis and PostgreSQL

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: postgres-db
    restart: always
    environment:
      POSTGRES_DB: microservices
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis-cache
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  auth-service:
    build: ./services/auth
    container_name: auth-service
    restart: always
    environment:
      DATABASE_URL: postgresql://admin:secret123@postgres:5432/microservices
      REDIS_URL: redis://redis:6379
      JWT_SECRET: supersecret
    ports:
      - "8001:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend-network

  user-service:
    build: ./services/users
    container_name: user-service
    restart: always
    environment:
      DATABASE_URL: postgresql://admin:secret123@postgres:5432/microservices
      AUTH_SERVICE_URL: http://auth-service:8000
    ports:
      - "8002:8000"
    depends_on:
      - postgres
      - auth-service
    networks:
      - backend-network

  api-gateway:
    build: ./services/gateway
    container_name: api-gateway
    restart: always
    environment:
      AUTH_SERVICE: http://auth-service:8000
      USER_SERVICE: http://user-service:8000
    ports:
      - "8080:8080"
    depends_on:
      - auth-service
      - user-service
    networks:
      - backend-network
      - frontend-network

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:Z
      - ./nginx/ssl:/etc/nginx/ssl:Z
    depends_on:
      - api-gateway
    networks:
      - frontend-network

volumes:
  postgres-data:
  redis-data:

networks:
  backend-network:
    driver: bridge
  frontend-network:
    driver: bridge
```

---

## 🔧 Advanced Options

### Environment Variables

**Method 1: In docker-compose.yml**
```yaml
services:
  app:
    image: myapp:latest
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DEBUG=false
```

**Method 2: .env File**

**.env:**
```env
NODE_ENV=production
PORT=3000
DB_HOST=postgres
DB_PASSWORD=secret123
```

**docker-compose.yml:**
```yaml
services:
  app:
    image: myapp:latest
    environment:
      - NODE_ENV=${NODE_ENV}
      - PORT=${PORT}
      - DB_HOST=${DB_HOST}
      - DB_PASSWORD=${DB_PASSWORD}
```

**Method 3: External File**
```yaml
services:
  app:
    image: myapp:latest
    env_file:
      - ./config/common.env
      - ./config/production.env
```

---

### Build Context

```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Containerfile
      args:
        - VERSION=1.0
        - BUILD_DATE=2024-01-15
    image: my-app:latest
```

---

### Healthchecks

```yaml
services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

### Dependencies and Order

```yaml
services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
```

---

### Resource Limits

```yaml
services:
  app:
    image: myapp:latest
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 🔄 Migration from Docker Compose to Podman

### Step 1: Verify Compatibility

Most docker-compose.yml files work without changes, but verify:

```bash
# Validate syntax
podman-compose config

# See which services would be created
podman-compose config --services
```

### Step 2: Adjust Volumes (SELinux)

If using SELinux, add `:Z` or `:z`:

```yaml
# Before
volumes:
  - ./app:/app

# After
volumes:
  - ./app:/app:Z
```

### Step 3: Alias for Docker Compose (Optional)

```bash
# Add to ~/.bashrc
alias docker-compose='podman-compose'

# Or create script
cat > /usr/local/bin/docker-compose << 'EOF'
#!/bin/bash
podman-compose "$@"
EOF
chmod +x /usr/local/bin/docker-compose
```

---

## 🛠️ Troubleshooting

### View Detailed Logs

```bash
# Logs from all services
podman-compose logs

# Logs from specific service
podman-compose logs service

# Last N lines
podman-compose logs --tail=100 service

# In real-time
podman-compose logs -f
```

### View Resulting Configuration

```bash
# View processed configuration
podman-compose config

# View only environment variables
podman-compose config | grep environment -A 10
```

### Recreate Services

```bash
# Recreate specific service
podman-compose up -d --force-recreate service

# Recreate all
podman-compose up -d --force-recreate
```

---

## 🎓 Module Summary

You have learned:
- ✅ What Podman Compose is and how to install it
- ✅ docker-compose.yml file structure
- ✅ Essential podman-compose commands
- ✅ Practical examples (LAMP, MERN, Microservices)
- ✅ Environment variables and configuration
- ✅ Healthchecks and dependencies
- ✅ Migration from Docker Compose to Podman
- ✅ Troubleshooting and debugging

---

## 📊 Cheat Sheet

```bash
# Main commands
podman-compose up -d                # Start services
podman-compose ps                   # View status
podman-compose logs -f              # View logs
podman-compose stop                 # Stop
podman-compose down                 # Stop and remove
podman-compose down -v              # + delete volumes
podman-compose build                # Build images
podman-compose up --build           # Rebuild and start
podman-compose exec service bash    # Enter container
podman-compose restart service      # Restart service

# Utilities
podman-compose config               # View configuration
podman-compose images               # View images
podman-compose top                  # View processes
```

---

## ➡️ Next Step

**[Module 9: Practical Exercises](../module-09-exercises/README.md)**

---

## 💡 Final Exercise

Create a complete stack with docker-compose.yml that includes:
1. Database (PostgreSQL or MySQL)
2. Backend API (Node.js, Python, or your preference)
3. Web frontend
4. Redis for cache
5. Nginx as reverse proxy
6. Volumes for persistence
7. Separate networks (frontend/backend)
8. Configured healthchecks
9. Environment variables in .env file
