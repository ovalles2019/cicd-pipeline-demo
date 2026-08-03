# Modern CI/CD Pipeline Demo

Learn and showcase a production-style CI/CD pipeline: commit → lint → build → test → registry → QA → Staging → Production.

A tiny FastAPI app is the *artifact*. The real product is the pipeline around it.

```text
 Developer ──commit──► GitHub
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
       Source          Build            Test
      (linting)   (image + unit +     (integration)
                   coverage ≥80%)
                          │
                          ▼
                       Release
                  (ship image → GHCR)
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
             QA       Staging     Production
```

## Pipeline stages (map to the diagram)

| Diagram stage | What runs here | Job name |
|---------------|----------------|----------|
| **Source** | Branch protection + Ruff lint/format | `lint` |
| **Build** | Docker image build + unit tests + **coverage gate 80%** | `build-image`, `unit-tests`, `coverage` |
| **Test** | Integration tests | `integration-tests` |
| **Release** | Push image to **GHCR** (registry) | `release` |
| **Deploy** | Promote through **QA → Staging → Production** | `deploy-qa`, `deploy-staging`, `deploy-production` |

On pull requests, only Source → Build → Test run (no release/deploy).
On `main`, the full path runs. Staging and Production wait for **manual approval** via GitHub Environments.

## Quick start (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# quality gates (same checks CI runs)
ruff check app tests
ruff format --check app tests
pytest tests/unit --cov=app --cov-fail-under=80
pytest tests/integration -v

# run the API
uvicorn app.main:app --reload --port 8000
# → http://127.0.0.1:8000/health
# → http://127.0.0.1:8000/docs
```

## Repo layout

```text
app/                  # FastAPI service (the deployable)
tests/unit/           # Build-stage unit tests
tests/integration/    # Test-stage integration flows
.github/workflows/    # CI/CD pipeline definition
docs/                 # Branch protection + deploy wiring
Dockerfile            # Container image
render.yaml           # QA / Staging / Production on Render
```

## GitHub setup (show-ready)

1. **Create the repo** and push this project.
2. **Branch protection** on `main` — require the status checks listed in [`docs/branch-protection.md`](docs/branch-protection.md).
3. **Environments** `qa`, `staging`, `production` — require reviewers on staging + production ([`docs/deploy.md`](docs/deploy.md)).
4. *(Optional)* Wire **Render** deploy hooks so promotions hit real services.

Without Render secrets, deploy jobs still run and *simulate* promotion — good for learning the flow in Actions.

## What this demonstrates on a resume / portfolio

- Quality gates that **fail the pipeline** (lint, coverage threshold)
- Build once, promote the same artifact through environments
- Container registry as the release boundary (GHCR)
- Environment protection / human approval before production
- Infrastructure-as-code for the target envs (`render.yaml`)

## API surface

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | Liveness + environment + version |
| `GET` | `/version` | App metadata |
| `GET/POST` | `/api/items` | Tiny CRUD used by tests |

## License

MIT — use freely for learning and portfolio demos.
