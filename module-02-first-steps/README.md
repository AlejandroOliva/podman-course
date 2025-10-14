# Module 2: First Steps with Podman

## 🎯 Module Objectives
- Run your first container
- Learn essential basic commands
- Understand the container lifecycle
- Manage containers (list, stop, delete)

---

## 🚀 Your First Container

Let's run our first container with a simple image:

```bash
podman run hello-world
```

### What just happened?

1. Podman searched for the `hello-world` image locally
2. Since it didn't find it, it downloaded it from Docker Hub
3. Created a container from that image
4. Ran the container
5. The container displayed a message and terminated

---

## 📋 Essential Basic Commands

### 1. `podman run` - Run Containers

Basic syntax:
```bash
podman run [options] IMAGE [command]
```

#### Examples:

```bash
# Run Ubuntu and enter its shell (interactive)
podman run -it ubuntu bash

# Run Alpine Linux
podman run -it alpine sh

# Run an nginx web server
podman run -d -p 8080:80 nginx
```

#### Important options:

- `-it`: Interactive mode with terminal
  - `-i`: Keeps STDIN open
  - `-t`: Allocates a pseudo-TTY (terminal)
- `-d`: Run in background (detached)
- `-p`: Map ports (host:container)
- `--name`: Give a name to the container
- `--rm`: Remove container when it exits
- `-v`: Mount volumes

---

### 2. `podman ps` - List Containers

```bash
# List running containers
podman ps

# List ALL containers (including stopped ones)
podman ps -a

# View only IDs
podman ps -q

# Custom format
podman ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```

**Typical output:**
```
CONTAINER ID  IMAGE                           COMMAND    CREATED       STATUS       PORTS       NAMES
9c8f7b123456  docker.io/library/nginx:latest  nginx      2 minutes ago Up 2 minutes 0.0.0.0:8080->80/tcp  my-nginx
```

---

### 3. `podman stop` - Stop Containers

```bash
# Stop a container by name
podman stop my-nginx

# Stop a container by ID
podman stop 9c8f7b123456

# Stop multiple containers
podman stop container1 container2 container3

# Stop all running containers
podman stop $(podman ps -q)
```

---

### 4. `podman start` - Start Containers

```bash
# Start a stopped container
podman start my-nginx

# Start and attach to container (see output)
podman start -a my-nginx

# Start in interactive mode
podman start -ai my-container
```

---

### 5. `podman rm` - Remove Containers

```bash
# Remove a stopped container
podman rm my-nginx

# Force removal (even if running)
podman rm -f my-nginx

# Remove multiple containers
podman rm container1 container2

# Remove all stopped containers
podman container prune

# Remove ALL containers (careful!)
podman rm -f $(podman ps -aq)
```

---

### 6. `podman logs` - View Logs

```bash
# View logs of a container
podman logs my-nginx

# Follow logs in real-time (like tail -f)
podman logs -f my-nginx

# View last 50 lines
podman logs --tail 50 my-nginx

# View logs with timestamps
podman logs -t my-nginx
```

---

### 7. `podman exec` - Execute Commands in Container

```bash
# Execute a command
podman exec my-nginx ls -la /usr/share/nginx/html

# Open an interactive shell in a running container
podman exec -it my-nginx bash

# Execute as another user
podman exec -u nginx my-nginx whoami
```

---

### 8. `podman inspect` - Inspect Details

```bash
# View all information about a container
podman inspect my-nginx

# Get only the container's IP
podman inspect -f '{{.NetworkSettings.IPAddress}}' my-nginx

# View environment variables
podman inspect -f '{{.Config.Env}}' my-nginx
```

---

## 🔄 Container Lifecycle

```
[CREATED] --start--> [RUNNING] --stop--> [STOPPED] --rm--> [REMOVED]
    ↑                    |                   |
    |                    |                   |
    +------restart-------+--------start------+
```

### States:

1. **Created**: Container created but not started
2. **Running**: Container is running
3. **Paused**: Container temporarily paused
4. **Stopped/Exited**: Container stopped
5. **Dead**: Container that couldn't stop correctly

---

## 💻 Practical Exercises

### Exercise 1: Basic Web Server

```bash
# 1. Run an nginx server
podman run -d --name my-web -p 8080:80 nginx

# 2. Verify it's running
podman ps

# 3. Open browser at http://localhost:8080
# Or use curl:
curl http://localhost:8080

# 4. View logs
podman logs my-web

# 5. Enter the container
podman exec -it my-web bash

# 6. Inside the container, view web files
ls -la /usr/share/nginx/html/

# 7. Exit the container
exit

# 8. Stop and remove
podman stop my-web
podman rm my-web
```

---

### Exercise 2: Interactive Container

```bash
# 1. Run Ubuntu interactively
podman run -it --name my-ubuntu ubuntu bash

# 2. Inside the container, install some packages
apt update
apt install -y curl vim

# 3. Create a file
echo "Hello from container" > /tmp/message.txt

# 4. Read the file
cat /tmp/message.txt

# 5. Exit (Ctrl+D or exit)
exit

# 6. Container stopped. Start it again
podman start my-ubuntu

# 7. Verify the file is still there
podman exec my-ubuntu cat /tmp/message.txt

# 8. Cleanup
podman rm -f my-ubuntu
```

---

### Exercise 3: Multiple Management

```bash
# 1. Create several containers
podman run -d --name web1 -p 8081:80 nginx
podman run -d --name web2 -p 8082:80 nginx
podman run -d --name web3 -p 8083:80 nginx

# 2. List them all
podman ps

# 3. Stop web2
podman stop web2

# 4. View all (including stopped)
podman ps -a

# 5. Restart web2
podman start web2

# 6. View logs of web1
podman logs web1

# 7. Stop all
podman stop web1 web2 web3

# 8. Remove all
podman rm web1 web2 web3

# Or all in one:
podman rm -f web1 web2 web3
```

---

## 🎨 Useful Options for `run` Command

### Custom name
```bash
podman run -d --name my-application nginx
```

### Auto-remove on exit
```bash
podman run --rm -it alpine sh
```

### Environment variables
```bash
podman run -e MY_VARIABLE="value" -e OTHER_VAR="123" alpine env
```

### Limit resources
```bash
# Limit memory to 512MB
podman run -m 512m nginx

# Limit CPU (50% of 1 core)
podman run --cpus="0.5" nginx
```

### Network mode
```bash
# Without network
podman run --network none alpine

# Host network
podman run --network host nginx
```

---

## 📝 Useful Cleanup Commands

```bash
# Remove stopped containers
podman container prune

# Remove unused images
podman image prune

# Clean everything (containers, images, volumes, unused networks)
podman system prune

# Clean EVERYTHING including used images
podman system prune -a --volumes
```

---

## 🎓 Module Summary

You have learned:
- ✅ How to run your first container
- ✅ Essential commands: run, ps, stop, start, rm
- ✅ How to view logs and inspect containers
- ✅ The container lifecycle
- ✅ Cleanup and management commands

---

## 📊 Command Cheat Sheet

```bash
podman run [options] image          # Create and run container
podman ps [-a]                      # List containers
podman stop container               # Stop container
podman start container              # Start container
podman restart container            # Restart container
podman rm container                 # Remove container
podman logs [-f] container          # View logs
podman exec -it container bash      # Enter container
podman inspect container            # View details
podman container prune              # Clean stopped containers
```

---

## ➡️ Next Step

**[Module 3: Working with Images](../module-03-images/README.md)**

---

## 💡 Self-Assessment Questions

1. What does the `-it` option do in `podman run`?
2. How do I list ALL containers, including stopped ones?
3. What's the difference between `podman stop` and `podman rm`?
4. How can I view logs in real-time from a container?
5. What command do I use to open a shell in a running container?
