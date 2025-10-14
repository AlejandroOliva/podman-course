# Module 5: Volumes and Data Persistence

## 🎯 Module Objectives
- Understand the persistence problem in containers
- Know the types of storage
- Work with named volumes
- Use bind mounts effectively
- Share data between containers

---

## 📦 The Persistence Problem

### Containers are Ephemeral

By default, data inside a container is **lost when the container is deleted**:

```bash
# Create container and write data
podman run -it --name temp ubuntu bash
# Inside the container:
echo "Important data" > /data.txt
exit

# Delete container
podman rm temp

# Data is lost 😢
```

**Solution**: Use volumes to persist data outside the container.

---

## 🗂️ Types of Storage in Podman

### 1. **Volumes (Named Volumes)** - Recommended ⭐
- Completely managed by Podman
- Location: `/var/lib/containers/storage/volumes/`
- Best for production

### 2. **Bind Mounts**
- Map host directory to container
- Full control over location
- Useful for development

### 3. **tmpfs** (temporary memory)
- Data in RAM
- Lost when stopping container
- For very temporary data

---

## 📚 Named Volumes

### Create Volumes

```bash
# Create a volume
podman volume create my-volume

# Create with options
podman volume create --opt type=tmpfs my-temp-volume

# List volumes
podman volume ls

# Inspect volume
podman volume inspect my-volume
```

### Use Volumes

```bash
# Basic syntax
podman run -v VOLUME_NAME:/path/in/container image

# Practical example
podman run -d \
  --name postgres-db \
  -v postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:15
```

### Verify Persistence

```bash
# 1. Create container with volume
podman run -d \
  --name db1 \
  -v db-data:/data \
  -e POSTGRES_PASSWORD=pass \
  postgres:15

# 2. Write data
podman exec db1 psql -U postgres -c "CREATE DATABASE myapp;"

# 3. Delete container
podman rm -f db1

# 4. Create new container with same volume
podman run -d \
  --name db2 \
  -v db-data:/data \
  -e POSTGRES_PASSWORD=pass \
  postgres:15

# 5. Data persists! 🎉
podman exec db2 psql -U postgres -l
```

### Manage Volumes

```bash
# List volumes
podman volume ls

# View details
podman volume inspect my-volume

# Delete volume
podman volume rm my-volume

# Delete unused volumes
podman volume prune

# Delete all volumes (CAREFUL!)
podman volume rm $(podman volume ls -q)
```

---

## 🔗 Bind Mounts

### Syntax

```bash
podman run -v /host/path:/container/path[:options] image
```

### Bind Mount Options

- `:Z` - Private relabeling (SELinux)
- `:z` - Shared relabeling (SELinux)
- `:ro` - Read-only
- `:rw` - Read and write (default)

### Practical Examples

#### Web Development

```bash
# Mount local code in nginx container
podman run -d \
  --name web-dev \
  -v $(pwd)/html:/usr/share/nginx/html:Z \
  -p 8080:80 \
  nginx

# Edit files locally and they reflect immediately
```

#### Application Development

```bash
# Node.js application
podman run -it --rm \
  --name node-dev \
  -v $(pwd):/app:Z \
  -w /app \
  -p 3000:3000 \
  node:18 \
  bash

# Inside the container:
npm install
npm run dev
```

#### Read-only

```bash
# Configuration in read-only mode
podman run -d \
  --name app \
  -v $(pwd)/config.json:/app/config.json:ro,Z \
  my-app:latest
```

---

## 🔄 Share Data between Containers

### Method 1: Shared Volume

```bash
# Create volume
podman volume create shared-data

# Container that writes data
podman run -d \
  --name writer \
  -v shared-data:/data \
  alpine \
  sh -c "while true; do date >> /data/log.txt; sleep 5; done"

# Container that reads data
podman run -it \
  --name reader \
  -v shared-data:/data:ro \
  alpine \
  tail -f /data/log.txt
```

### Method 2: Volumes-from (containers)

```bash
# Create container with volume
podman run -d \
  --name data-container \
  -v /data \
  alpine \
  tail -f /dev/null

# Use volumes from first container
podman run -it \
  --volumes-from data-container \
  alpine \
  sh
```

---

## 💾 Practical Use Cases

### Case 1: PostgreSQL Database

```bash
# Create volume for data
podman volume create postgres_data

# Run PostgreSQL
podman run -d \
  --name postgres \
  -v postgres_data:/var/lib/postgresql/data \
  -e POSTGRES_DB=myapp \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  postgres:15

# Data persists between restarts
podman restart postgres

# Even if we delete and recreate
podman rm -f postgres
podman run -d --name postgres -v postgres_data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret123 postgres:15
```

---

### Case 2: Web Server with Content

```bash
# Directory structure
mkdir -p website/html
echo "<h1>My Website</h1>" > website/html/index.html

# Run nginx with bind mount
podman run -d \
  --name web \
  -v $(pwd)/website/html:/usr/share/nginx/html:Z \
  -p 8080:80 \
  nginx

# Edit content locally
echo "<p>Updated content</p>" >> website/html/index.html

# Changes reflect immediately
curl http://localhost:8080
```

---

### Case 3: Application with Persistent Logs

```bash
# Create volume for logs
podman volume create app-logs

# Run application
podman run -d \
  --name my-app \
  -v app-logs:/var/log/app \
  my-application:latest

# View logs from host
podman run --rm \
  -v app-logs:/logs:ro \
  alpine \
  cat /logs/app.log
```

---

### Case 4: Data Backup

```bash
# Volume with important data
podman volume create important-data

# Container using that data
podman run -d --name app -v important-data:/data alpine tail -f /dev/null

# Create backup
podman run --rm \
  -v important-data:/source:ro \
  -v $(pwd):/backup:Z \
  alpine \
  tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /source .

# Restore backup
podman run --rm \
  -v important-data:/target \
  -v $(pwd):/backup:Z \
  alpine \
  sh -c "cd /target && tar xzf /backup/backup-20240115.tar.gz"
```

---

### Case 5: Multiple Volumes

```bash
# Application with separate data, config, and logs
podman run -d \
  --name complete-app \
  -v app-data:/var/lib/app \
  -v app-config:/etc/app:ro \
  -v app-logs:/var/log/app \
  -v $(pwd)/code:/opt/app:Z \
  my-app:latest
```

---

## 🎨 Containerfile with Volumes

### Define VOLUME in Containerfile

```dockerfile
FROM nginx:alpine

# Declare mount point
VOLUME /usr/share/nginx/html

# If no volume is specified when running,
# Podman will create an anonymous volume
```

### Complete Example

```dockerfile
FROM postgres:15

# Declare volumes
VOLUME /var/lib/postgresql/data
VOLUME /var/log/postgresql

# Environment variables
ENV POSTGRES_DB=myapp
ENV POSTGRES_USER=admin

EXPOSE 5432
```

---

## ⚙️ Advanced Options

### Temporary Volumes (tmpfs)

```bash
# Data in RAM (doesn't persist)
podman run -d \
  --name temp-app \
  --tmpfs /tmp:rw,size=100m,mode=1777 \
  nginx

# Useful for temporary data that doesn't need to persist
```

### Volumes with Drivers

```bash
# Local volume with specific options
podman volume create \
  --opt type=tmpfs \
  --opt device=tmpfs \
  --opt o=size=100m \
  my-tmpfs-volume
```

### Permissions and Ownership

```bash
# Change owner inside container
podman run --rm \
  -v my-volume:/data \
  alpine \
  chown -R 1000:1000 /data

# Use volume with specific user
podman run -d \
  --name app \
  --user 1000:1000 \
  -v data:/app/data \
  my-app:latest
```

---

## 🛡️ SELinux and Volumes

On systems with SELinux (Fedora, RHEL, CentOS):

```bash
# :Z - Private relabeling (recommended)
# Only this container can access
podman run -v $(pwd)/data:/data:Z alpine

# :z - Shared relabeling
# Multiple containers can access
podman run -v $(pwd)/data:/data:z alpine

# Without options, there may be permission errors
```

---

## 📊 Inspection and Monitoring

### View container volumes

```bash
# Inspect mounts
podman inspect -f '{{.Mounts}}' my-container

# Readable format
podman inspect -f '{{range .Mounts}}{{.Type}} {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' my-container
```

### Disk usage

```bash
# View Podman disk usage
podman system df

# Detailed with volumes
podman system df -v

# View specific volume size
du -sh /var/lib/containers/storage/volumes/my-volume/
```

---

## 🎓 Module Summary

You have learned:
- ✅ Why we need persistence in containers
- ✅ Differences between volumes, bind mounts, and tmpfs
- ✅ Create and manage named volumes
- ✅ Use bind mounts for development
- ✅ Share data between containers
- ✅ Practical use cases and backups
- ✅ Advanced options and SELinux

---

## 📊 Cheat Sheet

```bash
# Volumes
podman volume create name
podman volume ls
podman volume inspect name
podman volume rm name
podman volume prune

# Use volumes
podman run -v name:/path image
podman run -v /host:/container:Z image

# Backup
podman run --rm -v vol:/data:ro -v $(pwd):/backup:Z \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore
podman run --rm -v vol:/data -v $(pwd):/backup:Z \
  alpine sh -c "cd /data && tar xzf /backup/backup.tar.gz"
```

---

## ➡️ Next Step

**[Module 6: Networking in Podman](../module-06-networking/README.md)**

---

## 💡 Practical Exercise

1. Create a volume for a database
2. Run PostgreSQL using that volume
3. Create a database and tables
4. Delete the container
5. Create a new container with the same volume
6. Verify that the data persists
7. Make a backup of the volume to a .tar.gz file
