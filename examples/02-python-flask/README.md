# Example 2: Flask Application

Simple REST API with Python Flask.

## Files

- `app.py`: Flask application
- `requirements.txt`: Python dependencies
- `Containerfile`: Image definition
- `build-and-run.sh`: Script to build and run

## How to Use

```bash
# Build and run
bash build-and-run.sh

# Test the API
curl http://localhost:5000
curl http://localhost:5000/api/hello
curl http://localhost:5000/api/time

# View logs
podman logs -f flask-app

# Stop
podman stop flask-app
podman rm flask-app
```

## Endpoints

- `GET /` - API information
- `GET /api/hello` - Greeting
- `GET /api/time` - Current time
- `GET /health` - Health check
