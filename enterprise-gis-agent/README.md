# Enterprise Conversational GIS Agent

This repository contains an enterprise GIS application scaffold integrating an ArcGIS Experience Builder custom widget, FastAPI backend, approved layer catalog, GeoAgent, and Ollama. The container runtime is Linux-based and suitable for Docker-compatible hosts; development is also supported on macOS.

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

## Agent integration

The agent is initialized with the public `geoagent.create_agent` factory and `GeoAgentConfig` API. The selected release is GeoAgent `1.9.0`; its declared minimum Strands version is `1.37`, and the resolved lock installs Strands `1.61.1` with Ollama client `0.6.3`. Ollama is configured using `GeoAgentConfig(provider="ollama", model=..., ollama_host=..., temperature=0.0)`. GeoAgent resolves and constructs its supported Strands Ollama model internally.

GIS tools use GeoAgent's `@geo_tool` decorator and the documented `create_agent(..., tools=...)` registration mechanism. The bound query tool checks the approved catalog, operation and group restrictions, validates structured filters, restricts output fields, and captures returned GeoJSON in a request-scoped `ResultCapture`. The API returns GeoAgent's answer separately from the captured features. Application code does not instantiate Strands `Agent` or call an Ollama client directly.

GeoAgent and Strands require Python 3.11 or newer. `backend/requirements.txt` pins direct dependencies and explicitly declares `GeoAgent[ollama,browser]==1.9.0`; `backend/requirements.lock` pins the resolved dependency set for Python 3.11.

## Running locally

```bash
cd enterprise-gis-agent
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -r backend/requirements.lock
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

This machine does not contain a live ArcGIS Enterprise Portal or Experience Builder installation; therefore integration with real Portal OAuth, feature queries, and the native map widget must be completed in the target enterprise environment. The current ArcGIS client query method remains a development placeholder. The OAuth endpoints and WebSocket module are also scaffolding, not verified production authentication or streaming implementations.

## Architecture verification

- GeoAgent `1.9.0`, Strands Agents `1.61.1`, Ollama client `0.6.3` installed under Python 3.11.17.
- GeoAgent public entry point: `geoagent.create_agent`, with `GeoAgentContext` and `GeoAgentConfig`.
- Ollama configuration: GeoAgent provider `ollama`, configured host/model, temperature `0.0`; model construction occurs inside GeoAgent's resolver.
- GIS tool registration: custom `@geo_tool` function passed to `create_agent` via `tools`.
- Actual result capture: `backend/app/agent/tools.py` validates and records GIS tool results in a request-scoped collector; response assembly returns answer and GeoJSON independently.
- Regression coverage includes a simulated Strands-format tool call through GeoAgent's real `chat()` loop, tool authorization, actual output preservation, and concurrent request isolation.
