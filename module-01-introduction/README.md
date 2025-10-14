# Module 1: Introduction to Podman

## 🎯 Module Objectives
- Understand what Podman is
- Know the differences with Docker
- Understand the advantages of using Podman
- Install Podman on your system

---

## What is Podman?

**Podman** (Pod Manager) is a tool for managing OCI (Open Container Initiative) containers and images. It's an alternative to Docker that offers unique features and important advantages.

### Main Features

1. **Daemonless**: Unlike Docker, Podman doesn't require a background service
2. **Rootless**: Can run containers without root privileges
3. **Docker compatible**: Commands are almost identical (`podman` ≈ `docker`)
4. **Native Pods**: Supports Kubernetes-style Pods
5. **Improved security**: Better isolation and permission control

---

## 🆚 Differences between Podman and Docker

| Feature | Podman | Docker |
|---------|--------|--------|
| **Architecture** | Daemonless | Requires daemon (dockerd) |
| **Permissions** | Can run rootless | Traditionally requires root |
| **Pods** | Native support | Not directly available |
| **Systemd** | Native integration | Limited |
| **Fork/Exec** | Direct execution | Through daemon |
| **Compatibility** | 100% compatible with Docker commands | N/A |

### Architecture Example

**Docker:**
```
User → Docker CLI → Docker Daemon → containerd → runc → Container
```

**Podman:**
```
User → Podman CLI → fork/exec → crun/runc → Container
```

---

## ✅ Advantages of Podman

### 1. **Security**
- Rootless execution
- No daemon running as root
- Smaller attack surface

### 2. **Simplicity**
- Simpler architecture without daemon
- Less overhead
- Direct child process of user

### 3. **Systemd Integration**
- Automatically generates systemd files
- Container management as system services
- Auto-start and recovery

### 4. **Compatibility**
- Alias: `alias docker=podman` works in most cases
- Uses the same images from Docker Hub
- Compatible with Dockerfiles

### 5. **Pods**
- Native support for Pods (container groups)
- Similar to Kubernetes
- Facilitates transition to K8s

---

## 🔧 Installing Podman

### On Ubuntu/Debian

```bash
# Update system
sudo apt update

# Install Podman
sudo apt install -y podman

# Verify installation
podman --version
```

### On Fedora/RHEL/CentOS

```bash
# Podman comes pre-installed on Fedora 33+
# If not installed:
sudo dnf install -y podman

# Verify installation
podman --version
```

### On macOS

```bash
# Using Homebrew
brew install podman

# Initialize Podman VM
podman machine init
podman machine start

# Verify installation
podman --version
```

### On Windows

```powershell
# Download installer from:
# https://github.com/containers/podman/releases

# Or use winget:
winget install -e --id RedHat.Podman

# Initialize VM
podman machine init
podman machine start
```

---

## ✅ Installation Verification

Run these commands to verify everything works:

```bash
# View version
podman --version

# View system information
podman info

# Test by running a simple container
podman run hello-world
```

If you see the "Hello from Docker!" message (or similar), Podman is working correctly! 🎉

---

## 🔍 Help Commands

```bash
# General help
podman --help

# Help for a specific command
podman run --help

# View all available commands
podman --help | grep Commands -A 100
```

---

## 📝 Important Notes

1. **Alias for Docker**: If coming from Docker, you can create an alias:
   ```bash
   echo "alias docker=podman" >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Rootless Mode**: For better security, use Podman without sudo whenever possible

3. **Compatibility**: Podman can use Docker Hub registries directly

---

## 🎓 Module Summary

You have learned:
- ✅ What Podman is and its main features
- ✅ Key differences with Docker
- ✅ Advantages of using Podman
- ✅ How to install and verify Podman

---

## ➡️ Next Step

**[Module 2: First Steps](../module-02-first-steps/README.md)**

---

## 💡 Self-Assessment Questions

1. What is the main architectural difference between Podman and Docker?
2. What does "rootless" mean and why is it important?
3. Can I use Docker Hub images with Podman?
4. What command do I use to verify that Podman is installed?

*(Answers are in the module content)*
