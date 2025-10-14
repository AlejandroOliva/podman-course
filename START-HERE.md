# 🎓 Welcome to the Podman Course!

## 👋 Hello, Student

This is a complete Podman course designed to take you from zero to an advanced level. The course is structured in progressive modules with theory, practical examples, and exercises.

---

## 📁 Course Structure

```
podman-tutorial/
├── README.md                          # Main course index
├── START-HERE.md                      # This file (you are here!)
├── QUICK-GUIDE.md                     # Quick command reference
├── ADDITIONAL-RESOURCES.md            # External links and resources
│
├── module-01-introduction/            # What is Podman?
├── module-02-first-steps/             # Basic commands
├── module-03-images/                  # Creating and managing images
├── module-04-container-management/    # Advanced management
├── module-05-volumes/                 # Data persistence
├── module-06-networking/              # Networks and connectivity
├── module-07-pods/                    # Pods (unique feature)
├── module-08-compose/                 # Podman Compose
├── module-09-exercises/               # Practical exercises
│
└── examples/                          # Ready-to-use examples
    ├── 01-simple-web/
    ├── 02-python-flask/
    └── 03-compose-stack/
```

---

## 🚀 How to Start

### Step 1: Verify you have Podman installed

```bash
podman --version
```

If you don't have it installed, go to **[Module 1](module-01-introduction/README.md)** where installation is explained.

### Step 2: Read the main README

```bash
cat README.md
# or open in your favorite editor
```

### Step 3: Start with Module 1

```bash
cd module-01-introduction
cat README.md
```

### Step 4: Practice with each module

Read the theory, run the examples, and do the exercises.

---

## 📚 Recommended Learning Path

### 🟢 For Beginners (Week 1-2)

1. **Module 1**: Introduction to Podman
   - Basic concepts
   - Installation
   - First verifications

2. **Module 2**: First Steps
   - Your first container
   - Essential commands
   - Basic management

3. **Module 3**: Working with Images
   - Downloading images
   - Creating your own images
   - Containerfiles

**Practice**: Complete **Example 1: Simple Web** in `examples/01-simple-web/`

---

### 🟡 For Intermediate Level (Week 3-4)

4. **Module 4**: Advanced Container Management
   - Environment variables
   - Ports and networks
   - Debugging

5. **Module 5**: Volumes and Persistence
   - Storage types
   - Named volumes
   - Bind mounts

6. **Module 6**: Networking in Podman
   - Network types
   - Connecting containers
   - Use cases

**Practice**: Complete **Example 2: Python Flask** in `examples/02-python-flask/`

---

### 🔴 For Advanced Level (Week 5-6)

7. **Module 7**: Pods
   - Pod concept
   - Managing Pods
   - Generate Kubernetes YAML

8. **Module 8**: Podman Compose
   - Multi-container applications
   - docker-compose.yml
   - Complete stacks

9. **Module 9**: Practical Exercises
   - Progressive exercises
   - Complete projects
   - Automation

**Practice**: Complete **Example 3: Complete Stack** in `examples/03-compose-stack/`

---

## 🎯 Suggested Study Plans

### Option 1: Intensive (2 weeks)
- **Duration**: 2-3 hours daily
- **Day 1-3**: Modules 1-3
- **Day 4-6**: Modules 4-6
- **Day 7-9**: Modules 7-8
- **Day 10-14**: Module 9 + Projects

### Option 2: Moderate (1 month)
- **Duration**: 1-1.5 hours daily
- **Week 1**: Modules 1-2
- **Week 2**: Modules 3-4
- **Week 3**: Modules 5-6
- **Week 4**: Modules 7-9

### Option 3: Relaxed (2 months)
- **Duration**: 3-4 hours weekly
- **2 modules per week**
- **Weekends for practice**

---

## 📖 Reference Guides

### During the Course

- **[QUICK-GUIDE.md](QUICK-GUIDE.md)**: Essential commands to copy/paste
- **Module documentation**: Each module has its complete README.md

### After the Course

- **[ADDITIONAL-RESOURCES.md](ADDITIONAL-RESOURCES.md)**: Links, books, videos, communities

---

## 💻 Requirements

### Prior Knowledge
- ✅ Basic Linux terminal usage
- ✅ Basic networking concepts (IP, ports)
- ✅ Optional: Docker knowledge (helps but not necessary)

### System
- 💾 At least 10GB free space
- 🖥️ Linux, macOS, or Windows with WSL2
- 📦 Podman installed (explained in Module 1)

---

## 🎮 Included Practical Examples

### Example 1: Simple Web Server
**Level**: Beginner  
**Time**: 10 minutes  
**Location**: `examples/01-simple-web/`

An nginx server with custom HTML. Perfect for understanding bind mounts and ports.

```bash
cd examples/01-simple-web
./run.sh
```

---

### Example 2: REST API with Flask
**Level**: Intermediate  
**Time**: 20 minutes  
**Location**: `examples/02-python-flask/`

Build and run a REST API with Python Flask. Learn to create custom images.

```bash
cd examples/02-python-flask
./build-and-run.sh
```

---

### Example 3: Complete Stack (Frontend + Backend + DB)
**Level**: Advanced  
**Time**: 30 minutes  
**Location**: `examples/03-compose-stack/`

Complete stack with PostgreSQL, Flask API, and web frontend using Podman Compose.

```bash
cd examples/03-compose-stack
podman-compose up -d
```

---

## 🏆 Upon Completing the Course

You will be able to:

- ✅ Manage containers with Podman professionally
- ✅ Create your own optimized and secure images
- ✅ Design multi-container architectures
- ✅ Work with Pods in Kubernetes style
- ✅ Deploy complete applications with Compose
- ✅ Solve common problems
- ✅ Apply security best practices
- ✅ Prepare applications for production

---

## 💡 Tips for Success

1. **🔬 Experiment**: Don't be afraid to try and make mistakes
2. **📝 Take notes**: Write down important commands and concepts
3. **🎯 Practice**: Run every example in the course
4. **❓ Ask questions**: Use community resources if you have doubts
5. **🔄 Repeat**: Some concepts require repeated practice
6. **🚀 Projects**: Apply what you learned in your own projects

---

## 🆘 Need Help?

### Within the Course
- Each module has detailed examples
- Exercises include commented solutions
- Quick guide has reference commands

### Community
- Podman GitHub Discussions
- Stack Overflow (tag: podman)
- Reddit r/podman
- See ADDITIONAL-RESOURCES.md for more

---

## 🎊 You're Ready!

You have everything you need to start your journey with Podman. The course is designed to be progressive and practical.

### Your First Step

```bash
# Navigate to the course
cd module-01-introduction
cat README.md

# Or open the file in your favorite editor
```

---

## 📞 Course Information

- **Level**: From zero to advanced
- **Estimated duration**: 2-8 weeks (depending on pace)
- **Modules**: 9 complete modules
- **Practical examples**: 3 projects + multiple exercises
- **Language**: English 🇬🇧🇺🇸

---

## ⭐ Final Note

This course is 100% practical. Don't just read, **run the commands**, **try the examples**, and **complete the exercises**. The only way to learn Podman is by using it.

**Good luck and enjoy learning Podman! 🚀🐳**

---

*"The expert in anything was once a beginner." - Helen Hayes*

---

### 👉 [Start with Module 1: Introduction to Podman](module-01-introduction/README.md)
