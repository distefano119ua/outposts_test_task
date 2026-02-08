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
