# Enterprise Conversational GIS Agent

This repository contains a modular, Docker-ready enterprise GIS application scaffold that integrates an ArcGIS Experience Builder custom widget with a FastAPI backend, approved GIS tool layer restrictions, and an Ollama-based model provider. The code is intentionally built to be portable across Linux containers and macOS development hosts without hard-coding OS-specific behavior.

## Current environment status

A real ArcGIS Experience Builder Developer Edition installation was not found on this machine. The repository therefore contains the supported project structure and widget scaffolding, along with explicit configuration guidance for the required host installation and Portal registration step. The backend and tests are implemented and verified locally in this environment, while the Experience Builder integration remains a deployment-ready scaffold pending the actual Developer Edition installation.

## Architecture

Browser -> Experience Builder app -> custom widget -> authenticated FastAPI backend -> GIS tools -> approved catalog -> ArcGIS Enterprise FeatureServer -> GeoJSON -> map results

## Key requirements

- Python 3.11 runtime for containers.
- FastAPI backend with typed Pydantic models.
- Approved ArcGIS catalog allowlist enforced server side.
- Ollama provider with environment-based configuration.
- Simple OAuth/session scaffolding and authorization checks.
- Docker Compose for backend, Redis, and Ollama.

## Experience Builder Developer Edition

The source files in `experience-builder/custom-widgets/conversational-gis` are structured for ArcGIS Experience Builder Developer Edition conventions, but the actual Developer Edition installation itself is not bundled in this repository. Place this widget into the proper custom widget directory of your Experience Builder installation and rebuild it using the version's supported workflow.

Typical deployment path:

1. Install ArcGIS Experience Builder Developer Edition for the target version.
2. Copy the folder `experience-builder/custom-widgets/conversational-gis` into the Developer Edition widget directory.
3. Register the widget with your Experience Builder app.
4. Configure the backend URL and map widget association in the widget settings.
5. Publish or preview the app and confirm the widget connects to the FastAPI backend.

## Running locally

```bash
cd enterprise-gis-agent/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd ..
python -m pytest backend/tests -q
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## Docker Compose

```bash
cd enterprise-gis-agent
docker compose -f deploy/compose.yaml up --build
```

## Environment variables

See `.env.example` for required placeholders.

## Catalog administration

The allowlist is defined in `backend/catalog.json`. Add or update approved service entries there and validate them at startup. No arbitrary layer or service path is allowed outside the catalog.

## Security notes

- The frontend never stores Portal access tokens in browser storage.
- The backend must enforce all layer allowlist checks independently of the LLM.
- The model provider remains an external inference layer; do not allow direct arbitrary HTTP access beyond the configured catalog tools.
- Production deployments must use a secure session secret, HTTPS, and an authorized OAuth registration in the org Portal.

## Known limitation

This machine does not contain a live ArcGIS Enterprise Portal or Experience Builder installation; therefore the final integration with real Portal OAuth, feature queries, and the native map widget must be completed in the target enterprise environment.
