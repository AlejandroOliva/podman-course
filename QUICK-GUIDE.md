# 📖 Podman Quick Guide

## Essential Commands

### Containers

```bash
# Run container
podman run -d --name my-container -p 8080:80 nginx

# List running containers
podman ps

# List all containers
podman ps -a

# Stop container
podman stop my-container

# Start container
podman start my-container

# Remove container
podman rm my-container

# View logs
podman logs -f my-container

# Enter a container
podman exec -it my-container bash
```

### Images

```bash
# Search for images
podman search nginx

# Pull image
podman pull nginx:alpine

# List images
podman images

# Build image
podman build -t my-image:1.0 .

# Remove image
podman rmi my-image:1.0

# View image history
podman history my-image
```

### Volumes

```bash
# Create volume
podman volume create my-volume

# List volumes
podman volume ls

# Inspect volume
podman volume inspect my-volume

# Use volume
podman run -v my-volume:/data nginx

# Use bind mount
podman run -v $(pwd):/app:Z nginx

# Remove volume
podman volume rm my-volume
```

### Networks

```bash
# Create network
podman network create my-network

# List networks
podman network ls

# Use custom network
podman run --network my-network nginx

# Connect container to network
podman network connect my-network my-container

# Remove network
podman network rm my-network
```

### Pods

```bash
# Create Pod
podman pod create --name my-pod -p 8080:80

# List Pods
podman pod ls

# Add container to Pod
podman run -d --pod my-pod nginx

# Stop Pod
podman pod stop my-pod

# Remove Pod
podman pod rm my-pod

# Generate Kubernetes YAML
podman generate kube my-pod > pod.yaml

# Create Pod from YAML
podman play kube pod.yaml
```

### Podman Compose

```bash
# Start services
podman-compose up -d

# View logs
podman-compose logs -f

# Stop services
podman-compose down

# Rebuild
podman-compose up --build

# View status
podman-compose ps
```

### Cleanup

```bash
# Remove stopped containers
podman container prune

# Remove unused images
podman image prune

# Remove unused volumes
podman volume prune

# Remove unused networks
podman network prune

# Clean everything
podman system prune -a --volumes
```

### System Information

```bash
# Podman information
podman info

# Version
podman version

# Disk usage
podman system df

# View events in real-time
podman events
```

## Common `podman run` Options

```bash
podman run \
  -d \                              # Run in background
  --name my-container \             # Container name
  -p 8080:80 \                      # Map ports
  -e VAR=value \                    # Environment variable
  -v volume:/path \                 # Mount volume
  --network my-network \            # Use custom network
  --restart=always \                # Restart policy
  -m 512m \                         # Limit memory
  --cpus="1.0" \                    # Limit CPU
  --rm \                            # Remove on exit
  nginx:alpine                      # Image to use
```

## Quick Example: Web Application

```bash
# 1. Create network
podman network create app-net

# 2. Database
podman run -d \
  --name db \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15-alpine

# 3. Application
podman run -d \
  --name app \
  --network app-net \
  -e DB_HOST=db \
  -p 8080:8080 \
  my-app:latest
```

## Troubleshooting

```bash
# View detailed logs
podman logs --tail 100 -f container

# Inspect container
podman inspect container

# View processes in container
podman top container

# View statistics
podman stats container

# Run command in container
podman exec container command

# Copy files
podman cp container:/path/file ./local
podman cp ./local container:/path/
```

## Resources

- **Official Documentation**: https://docs.podman.io/
- **GitHub**: https://github.com/containers/podman
- **Complete Tutorial**: See modules in this repository

## Tips

1. **Alias for Docker**: `alias docker=podman`
2. **Rootless**: Run without `sudo` whenever possible
3. **SELinux**: Use `:Z` in volumes for systems with SELinux
4. **Logs**: Use `-f` to follow logs in real-time
5. **Cleanup**: Clean regularly with `podman system prune`

---

**Happy learning with Podman! 🚀**
