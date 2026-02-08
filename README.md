# Outposts Logs Service

This project is a small service-oriented system for collecting, processing, exporting, and forwarding nginx logs.

It consists of two services:
- **nginx** — a mock nginx log provider
- **logs** — a log processing and exporting service

The system is designed to demonstrate:
- service-to-service communication
- log parsing and normalization
- flexible exporting (CSV / JSON)
- integration with GitHub via REST API
- Docker-based development workflow
---

## Build and run the project using Makefile

The project uses a `Makefile` to simplify building Docker images and running all services.
All commands must be executed from the **project root directory**.

---

### Prerequisites

Make sure the following tools are installed on your system:

- Docker
- Docker Compose
- Make

Verify installation:

```bash
docker --version
docker compose version
make --version
```
---
## GitHub configuration

To enable exporting logs to GitHub, you must provide your own GitHub credentials.

Before running the project, update the environment variables with your personal data:

```env
GITHUB_TOKEN=""
GITHUB_REPO=""
```
---
## Build Docker images

To build Docker images for all services: `make build`

This command:
- builds Docker images for logs and nginx services
- does not start containers

---

## Start services

To start all services in detached mode: `make up`

This command:
- starts containers using Docker Compose
- runs services in the background

After startup, the services will be available at:
- Logs service Swagger UI:  
  http://localhost:8001/docs
- Nginx mock service:  
  http://localhost:8000/logs
