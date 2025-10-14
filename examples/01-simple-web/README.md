# Example 1: Simple Web Server

This example shows how to create a simple web server with nginx.

## Files

- `index.html`: Example web page
- `run.sh`: Script to run the container

## How to Use

```bash
# Run
bash run.sh

# Access
# Open http://localhost:8080 in your browser
# Or use: curl http://localhost:8080

# Stop
podman stop simple-web
podman rm simple-web
```

## Modify Content

Simply edit `index.html` and changes will be reflected immediately (the directory is mounted in the container).
