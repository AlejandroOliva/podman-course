# Module 9: Practical Exercises and Projects

## 🎯 Module Objectives
- Apply all acquired knowledge
- Solve progressive exercises
- Complete real projects
- Prepare to use Podman in production

---

## 📚 Progressive Exercises

### 🟢 Beginner Level

#### Exercise 1: Your First Application

**Objective**: Create and run a simple web server

**Tasks**:
1. Run a container with nginx
2. Map port 8080 on host to port 80 in container
3. Verify it works by accessing with curl
4. View the container logs
5. Stop and remove the container

<details>
<summary>💡 View Solution</summary>

```bash
# 1. Run nginx
podman run -d --name my-nginx -p 8080:80 nginx

# 2. Verify
curl http://localhost:8080

# 3. View logs
podman logs my-nginx

# 4. Stop and remove
podman stop my-nginx
podman rm my-nginx
```
</details>

---

#### Exercise 2: Customize Web Content

**Objective**: Serve your own HTML content

**Tasks**:
1. Create a directory with an `index.html` file
2. Run nginx mounting your directory
3. Modify the HTML and verify changes in real-time

<details>
<summary>💡 View Solution</summary>

```bash
# 1. Create content
mkdir -p my-web
cat > my-web/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My First Web with Podman</title>
</head>
<body>
    <h1>Hello from Podman!</h1>
    <p>This is my first web page in a container.</p>
</body>
</html>
EOF

# 2. Run nginx
podman run -d --name web -p 8080:80 \
  -v $(pwd)/my-web:/usr/share/nginx/html:Z \
  nginx

# 3. Verify
curl http://localhost:8080

# 4. Edit and verify changes
echo "<p>New content</p>" >> my-web/index.html
curl http://localhost:8080
```
</details>

---

#### Exercise 3: Persistent Database

**Objective**: Create a database that persists data

**Tasks**:
1. Create a volume for PostgreSQL
2. Run PostgreSQL using that volume
3. Connect and create a database
4. Delete the container
5. Create a new container and verify data persists

<details>
<summary>💡 View Solution</summary>

```bash
# 1. Create volume
podman volume create pgdata

# 2. Run PostgreSQL
podman run -d --name postgres \
  -e POSTGRES_PASSWORD=mypassword \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# 3. Wait for startup
sleep 5

# 4. Create database
podman exec -it postgres psql -U postgres -c "CREATE DATABASE myapp;"
podman exec -it postgres psql -U postgres -c "\l"

# 5. Delete container
podman rm -f postgres

# 6. Create new container with same volume
podman run -d --name postgres-new \
  -e POSTGRES_PASSWORD=mypassword \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# 7. Verify DB exists
sleep 5
podman exec -it postgres-new psql -U postgres -c "\l"
```
</details>

---

### 🟡 Intermediate Level

#### Exercise 4: Application with Database

**Objective**: Connect a web application with a database

**Tasks**:
1. Create a custom network
2. Run PostgreSQL on that network
3. Run an application that connects to the DB
4. Verify communication between containers

<details>
<summary>💡 View Solution</summary>

```bash
# 1. Create network
podman network create app-network

# 2. Run PostgreSQL
podman run -d --name db \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  postgres:15-alpine

# 3. Run Python app that connects to DB
cat > app.py << 'EOF'
import psycopg2
import time

time.sleep(3)  # Wait for DB to be ready

try:
    conn = psycopg2.connect(
        host="db",
        database="myapp",
        user="postgres",
        password="secret"
    )
    print("✅ Successful connection to PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
EOF

cat > requirements.txt << 'EOF'
psycopg2-binary
EOF

cat > Containerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
EOF

# 4. Build and run app
podman build -t my-app .
podman run --rm --network app-network my-app
```
</details>

---

#### Exercise 5: Create Your First Image

**Objective**: Build a custom image

**Tasks**:
1. Create a simple application (web server)
2. Write a Containerfile
3. Build the image
4. Run a container from your image
5. Upload the image to a registry (optional)

<details>
<summary>💡 View Solution</summary>

```bash
# 1. Create Flask application
cat > app.py << 'EOF'
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from my custom image!",
        "version": os.getenv("APP_VERSION", "1.0"),
        "author": "Your Name"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

cat > requirements.txt << 'EOF'
Flask==3.0.0
EOF

# 2. Create Containerfile
cat > Containerfile << 'EOF'
FROM python:3.11-slim

# Metadata
LABEL maintainer="your@email.com"
LABEL version="1.0"

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Switch to non-root user
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]
EOF

# 3. Build image
podman build -t my-first-image:1.0 .

# 4. Run container
podman run -d --name my-app -p 5000:5000 \
  -e APP_VERSION=1.0 \
  my-first-image:1.0

# 5. Test
curl http://localhost:5000
curl http://localhost:5000/health

# 6. View created images
podman images | grep my-first-image
```
</details>

---

#### Exercise 6: Working with Pods

**Objective**: Create a Pod with multiple containers

**Tasks**:
1. Create a Pod
2. Add an application container
3. Add a Redis container
4. Verify they communicate via localhost
5. Generate the Kubernetes YAML file

<details>
<summary>💡 View Solution</summary>

```bash
# 1. Create Pod
podman pod create --name my-pod -p 5000:5000

# 2. Add Redis
podman run -d --pod my-pod --name redis redis:alpine

# 3. Create application that uses Redis
cat > app-redis.py << 'EOF'
from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def home():
    count = r.incr('visits')
    return jsonify({
        "message": "Application with Redis",
        "visits": count
    })

@app.route('/reset')
def reset():
    r.set('visits', 0)
    return jsonify({"message": "Counter reset"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

cat > requirements-redis.txt << 'EOF'
Flask==3.0.0
redis==5.0.0
EOF

cat > Containerfile.redis << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements-redis.txt requirements.txt
RUN pip install -r requirements.txt
COPY app-redis.py app.py
CMD ["python", "app.py"]
EOF

# 4. Build and run app
podman build -f Containerfile.redis -t app-redis .
podman run -d --pod my-pod --name app app-redis

# 5. Test
sleep 3
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000/reset

# 6. View Pod
podman pod ps
podman ps --pod

# 7. Generate Kubernetes YAML
podman generate kube my-pod > my-pod.yaml
cat my-pod.yaml
```
</details>

---

### 🔴 Advanced Level

#### Exercise 7: Complete Stack with Compose

**Objective**: Create a complete multi-container application

**Tasks**:
1. Create an application with frontend, backend, and database
2. Use docker-compose.yml
3. Configure separate networks
4. Add persistent volumes
5. Implement healthchecks

<details>
<summary>💡 View Solution</summary>

**File structure:**
```
project/
├── docker-compose.yml
├── backend/
│   ├── Containerfile
│   ├── app.py
│   └── requirements.txt
└── frontend/
    ├── Containerfile
    └── index.html
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: db
    restart: always
    environment:
      POSTGRES_DB: todoapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: cache
    restart: always
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  backend:
    build: ./backend
    container_name: api
    restart: always
    environment:
      DATABASE_URL: postgresql://admin:secret123@postgres:5432/todoapp
      REDIS_URL: redis://redis:6379
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
      - frontend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    container_name: web
    restart: always
    ports:
      - "8080:80"
    depends_on:
      - backend
    networks:
      - frontend

volumes:
  db-data:

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge
```

**backend/app.py:**
```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import redis
import os

app = Flask(__name__)
CORS(app)

db_url = os.getenv('DATABASE_URL')
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url, decode_responses=True)

def get_db():
    return psycopg2.connect(db_url)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    conn.close()
    return jsonify(todos)

@app.route('/api/stats')
def stats():
    visits = r.incr('api_calls')
    return jsonify({"total_calls": visits})

if __name__ == '__main__':
    # Create table if not exists
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200),
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()
    
    app.run(host='0.0.0.0', port=5000)
```

**backend/Containerfile:**
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

**backend/requirements.txt:**
```
Flask==3.0.0
Flask-CORS==4.0.0
psycopg2-binary==2.9.9
redis==5.0.0
```

**frontend/Containerfile:**
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
```

**frontend/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Todo App - Podman</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        button { padding: 10px 20px; margin: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>📝 Todo App with Podman</h1>
    <button onclick="getStats()">View Statistics</button>
    <div id="stats"></div>
    <div id="todos"></div>

    <script>
        async function getStats() {
            const response = await fetch('http://localhost:5000/api/stats');
            const data = await response.json();
            document.getElementById('stats').innerHTML = 
                `<p>Total API calls: ${data.total_calls}</p>`;
        }
    </script>
</body>
</html>
```

**Run:**
```bash
# Create structure
mkdir -p project/{backend,frontend}
# (create all files above)

cd project

# Start entire stack
podman-compose up -d

# View logs
podman-compose logs -f

# Test
curl http://localhost:5000/health
curl http://localhost:5000/api/stats
# Open http://localhost:8080 in browser

# Stop
podman-compose down
```
</details>

---

#### Exercise 8: CI/CD with Podman

**Objective**: Automate build and deployment

**Tasks**:
1. Create a script that builds images
2. Add automated tests
3. Implement image versioning
4. Create deployment script

<details>
<summary>💡 View Solution</summary>

**build.sh:**
```bash
#!/bin/bash
set -e

VERSION=${1:-"latest"}
IMAGE_NAME="my-app"

echo "🔨 Building image ${IMAGE_NAME}:${VERSION}..."

# Build image
podman build -t ${IMAGE_NAME}:${VERSION} .

# Tag as latest
podman tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:latest

# Run tests
echo "🧪 Running tests..."
podman run --rm ${IMAGE_NAME}:${VERSION} pytest

# Security scan (optional, requires additional tools)
# podman run --rm -v /var/run/podman/podman.sock:/var/run/docker.sock \
#   aquasec/trivy image ${IMAGE_NAME}:${VERSION}

echo "✅ Build complete: ${IMAGE_NAME}:${VERSION}"
```

**deploy.sh:**
```bash
#!/bin/bash
set -e

VERSION=${1:-"latest"}
CONTAINER_NAME="my-app-prod"

echo "🚀 Deploying ${CONTAINER_NAME}..."

# Stop previous container if exists
podman stop ${CONTAINER_NAME} 2>/dev/null || true
podman rm ${CONTAINER_NAME} 2>/dev/null || true

# Deploy new version
podman run -d \
  --name ${CONTAINER_NAME} \
  --restart=always \
  -p 8080:8080 \
  -v app-data:/data \
  -e ENV=production \
  my-app:${VERSION}

# Healthcheck
echo "⏳ Waiting for application to be ready..."
for i in {1..30}; do
  if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Application deployed successfully!"
    exit 0
  fi
  sleep 1
done

echo "❌ Error: Application didn't respond"
exit 1
```

**Use:**
```bash
chmod +x build.sh deploy.sh

# Build version 1.0
./build.sh 1.0

# Deploy
./deploy.sh 1.0
```
</details>

---

## 🏆 Complete Projects

### Project 1: Blog System

**Description**: Complete blog with admin, database, and cache

**Components**:
- PostgreSQL: Database
- Redis: Cache
- Backend: REST API (Python/Node)
- Frontend: Web interface
- Nginx: Reverse proxy

**Features**:
- CRUD of posts
- User authentication
- Comments
- Search with cache
- Admin panel

---

### Project 2: Monitoring with ELK Stack

**Description**: Centralized logging system

**Components**:
- Elasticsearch: Log storage
- Logstash: Log processing
- Kibana: Visualization
- Filebeat: Log collection

---

### Project 3: E-commerce

**Description**: Complete online store

**Components**:
- Product database (PostgreSQL)
- Session database (Redis)
- Product service
- Cart service
- Payment service
- Frontend

---

## 🎓 Module Summary

You have completed:
- ✅ Exercises from beginner to advanced
- ✅ Real practical projects
- ✅ Application of all course concepts
- ✅ Automation with scripts
- ✅ CI/CD best practices

---

## 🎉 Congratulations!

You have completed the **Complete Podman Course**. Now you have the skills to:

- 🐳 Manage containers with Podman
- 🏗️ Create your own images
- 🎪 Work with Pods
- 🌐 Configure complex networks
- 💾 Handle data persistence
- 🚀 Deploy multi-container applications
- ☸️ Prepare applications for Kubernetes

---

## 📚 Additional Resources

### Official Documentation
- [Podman Documentation](https://docs.podman.io/)
- [Podman GitHub](https://github.com/containers/podman)
- [Podman Desktop](https://podman-desktop.io/)

### Community
- [Podman Discussions](https://github.com/containers/podman/discussions)
- [Reddit r/podman](https://www.reddit.com/r/podman/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/podman)

### Complementary Courses
- Kubernetes Basics
- Container Security
- DevOps with Containers

---

## 🎯 Next Steps

1. **Practice regularly**: Use Podman in your personal projects
2. **Contribute**: Participate in open source projects
3. **Learn Kubernetes**: Continue with orchestration
4. **Deepen security**: Study best practices
5. **Share knowledge**: Teach others

---

## 💬 Feedback

If this course was helpful:
- ⭐ Share it with others
- 💡 Suggest improvements
- 🐛 Report errors
- ✍️ Contribute with more exercises

---

**Thank you for completing this course! 🚀**

*"Practice makes perfect. Keep experimenting with Podman and you'll go far."*

---

## 📝 Certificate of Completion

You have successfully completed:
- ✅ 9 theoretical modules
- ✅ 8+ practical exercises
- ✅ Real projects

**Continue learning and building amazing things with Podman!** 🎊
