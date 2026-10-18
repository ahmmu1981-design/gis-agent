# Deployment notes

This project is designed for local development on macOS and production deployment on Linux-compatible Docker hosts.

## Prerequisites

- Docker and Docker Compose
- ArcGIS Experience Builder Developer Edition installation in a target environment
- Portal OAuth client registration
- ArcGIS Enterprise feature services defined in the approved catalog
- Local or remote Ollama endpoint

## Reverse proxy guidance

Place the FastAPI API behind a TLS-terminating reverse proxy such as NGINX or Traefik. Secure WebSockets with TLS and WebSocket upgrade support in the proxy configuration.

## Backup and upgrade guidance

- Back up the approved catalog and environment configuration before updates.
- Keep a versioned copy of the catalog JSON.
- Use pinned dependency versions in the backend requirements file.
- Validate the app against a staging ArcGIS server before moving to production.
