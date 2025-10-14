# Example 3: Complete Stack with Compose

Complete stack with frontend, backend, and database using Podman Compose.

## Components

- **PostgreSQL**: Database
- **Backend**: Flask REST API
- **Frontend**: Web page with nginx

## Structure

```
03-compose-stack/
├── docker-compose.yml
├── backend/
│   ├── Containerfile
│   ├── app.py
│   └── requirements.txt
└── frontend/
    └── index.html
```

## How to Use

```bash
# Start the entire stack
podman-compose up -d

# View logs
podman-compose logs -f

# View status
podman-compose ps

# Test backend
curl http://localhost:5000
curl http://localhost:5000/api/data

# Access frontend
# Open http://localhost:8080

# Stop everything
podman-compose down

# Stop and remove volumes
podman-compose down -v
```

## URLs

- Frontend: http://localhost:8080
- Backend API: http://localhost:5000
- PostgreSQL: localhost:5432
