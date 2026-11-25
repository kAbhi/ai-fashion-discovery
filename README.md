# ai-fashion-discovery

AI-powered occasion-first fashion discovery platform — monorepo.

## Contents

- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Local setup](#local-setup)
- [Running the services](#running-the-services)
- [Running tests](#running-tests)
- [Linting and type checks](#linting-and-type-checks)
- [Environment variables](#environment-variables)
- [Deployment](#deployment)
- [License](#license)

## Project structure

```text
ai-fashion-discovery/
├── backend/           # FastAPI (Python 3.13), SQLAlchemy 2.x, Alembic, Pytest
├── frontend/          # Next.js App Router, TypeScript, Tailwind, Vitest
├── data/seed/         # Sample catalogue seed data (placeholder)
├── docs/              # Project documentation
├── prompts/           # Product requirements and phase specifications
├── docker/postgres/   # Local database initialisation scripts
├── docker-compose.yml # Local development stack (PostgreSQL + backend + frontend)
├── .env.example       # Environment variable template
├── DEPLOYMENT.md      # Deployment manual (Vercel frontend / Render backend)
├── .gitignore
└── README.md
```

## Requirements

| Tool | Version | Notes |
|------|---------|-------|
| Node | >= 22 < 23 | Pin via `.nvmrc` |
| Python | >= 3.12 < 3.14 | Pin via `backend/.python-version` (3.13 used) |
| PostgreSQL | 14+ | Local via Docker Compose or Homebrew |
| Docker | optional | Only needed if using Docker Compose |

### If Docker is unavailable
PostgreSQL 14 is installed via Homebrew on this machine. Create databases manually:

```bash
psql -d postgres -c "CREATE ROLE fashion LOGIN PASSWORD 'fashion';"
psql -d postgres -c "CREATE DATABASE fashion_discovery OWNER fashion;"
psql -d postgres -c "CREATE DATABASE fashion_discovery_test OWNER fashion;"
```

## Local setup

### 1. Clone and enter the repository

```bash
git clone https://github.com/kAbhi/ai-fashion-discovery.git
cd ai-fashion-discovery
```

### 2. Copy the environment template

```bash
cp .env.example .env
```

Edit `.env` if your local ports or credentials differ. For local development the defaults work out of the box with Docker Compose.

### 3. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

The venv must not be committed (`.venv/` is gitignored).

### 4. Frontend setup

```bash
cd ../frontend
npm install
```

## Running the services

### Option A — Docker Compose (recommended, reproduces production parity)

```bash
docker compose up --build
```

Then:
- Backend health: http://localhost:8000/health
- Frontend: http://localhost:3000

Stop with `docker compose down`.

### Option B — Manual (backend + frontend on localhost)

Terminal 1 — backend:

```bash
cd backend
source .venv/bin/activate
export DATABASE_URL=postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery
export CORS_ORIGINS=http://localhost:3000
export ENVIRONMENT=local
alembic upgrade head          # one-time schema setup; see below
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Terminal 2 — frontend:

```bash
cd frontend
export NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
npm run dev
```

Open http://localhost:3000 — the homepage renders and polls the backend health endpoint.

### Database migrations

Schema changes are version-controlled with Alembic (`backend/alembic/`). Never run destructive DDL outside a migration file.

```bash
cd backend
# Create a new migration after model changes
alembic revision -m "add products table" --autogenerate
# Apply to local dev database
alembic upgrade head
```

## Running tests

Backend (requires the `fashion_discovery_test` PostgreSQL database):

```bash
cd backend
source .venv/bin/activate
export DATABASE_URL=postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery
export TEST_DATABASE_URL=postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery_test
export ENVIRONMENT=test
export CORS_ORIGINS=http://localhost:3000
pytest -q
```

Frontend:

```bash
cd frontend
npm test           # vitest run
npm run typecheck  # tsc --noEmit
npm run lint       # eslint
npm run format:check
```

## Linting and type checks

Backend: `ruff check`, `ruff format --check`, `mypy` (configured in `backend/pyproject.toml`).

Frontend: `eslint`, `prettier --check`, `tsc --noEmit`.

## Environment variables

| Variable | Where | Secret? | Required | Purpose |
|----------|-------|---------|----------|---------|
| `DATABASE_URL` | backend `.env` / Render dashboard | Yes | Yes | PostgreSQL connection URL |
| `TEST_DATABASE_URL` | backend `.env` | Yes | No | Test database URL |
| `ENVIRONMENT` | backend `.env` | No | No | `local\|test\|preview\|production` |
| `LOG_LEVEL` | backend `.env` | No | No | Logging level |
| `CORS_ORIGINS` | backend `.env` / Render dashboard | No | Yes | Comma-separated allowed browser origins |
| `CORS_ORIGIN_REGEX` | backend `.env` | No | No | Preview origin pattern (optional) |
| `LLM_PROVIDER` | backend `.env` | No | No | LLM provider name |
| `LLM_API_KEY` | Render dashboard only | Yes | No | LLM API key (never committed) |
| `NEXT_PUBLIC_API_BASE_URL` | frontend `.env.local` / Vercel dashboard | No | Yes | Backend base URL for browser calls |

See `.env.example` for local placeholder values.

## Deployment

| Layer | Hosting | Builds from | Root directory |
|-------|---------|-------------|----------------|
| Frontend | Vercel | GitHub → `frontend/` | `frontend` |
| Backend | Render | GitHub → `backend/` | `backend` |
| Database | Render PostgreSQL | managed service | n/a |

`DEPLOYMENT.md` is the single source of truth for manual setup steps, environment variables, deployment commands, verification, and rollback procedures. Review it before first deployment.

### Deployment readiness (this phase)

- ✅ `render.yaml` prepared in code (hosting resources not yet created)
- ✅ `.env.example` documents every required variable
- ✅ Backend binds to `0.0.0.0` and honors the `PORT` environment variable
- ✅ Backend exposes `/health` for Render health checks
- ✅ Frontend reads `NEXT_PUBLIC_API_BASE_URL` only (no `NEXT_PUBLIC_*` secrets)
- ✅ Monorepo subdirectory builds are supported by both platforms
- ⚠️ GitHub, Vercel and Render accounts must be created by the project owner
- ⚠️ Production secrets must be entered in hosting dashboards (never committed)

## License

MIT
