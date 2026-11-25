# Deployment Manual

Single source of truth for configuring, deploying, operating, and verifying the
ai-fashion-discovery application. Updated with every phase that introduces a
deployment change.

**Deployment status is truthful:** an item is marked complete only when there is
evidence the action succeeded, not merely because code or configuration was
written.

## 1. Deployment Architecture

| Layer | Hosting | Builds from | Root dir | Responsibility | Communication |
|-------|---------|-------------|----------|----------------|---------------|
| Frontend | Vercel | GitHub repo → `frontend/` | `frontend/` | Next.js App Router UI; browser calls backend directly | HTTPS to backend `/health` + APIs (`NEXT_PUBLIC_API_BASE_URL`) |
| Backend | Render Web Service (native Python runtime) | GitHub repo → `backend/` | `backend/` | FastAPI API, intent understanding, catalogue search/ranking, preference persistence | Bound to `0.0.0.0:$PORT`; health at `/health` |
| Database | Render managed PostgreSQL | n/a | n/a | Product catalogue, sessions, interactions, wishlists, comparisons | Internal URL preferred (same region); external URL otherwise |

- Frontend and backend are deployed independently; a frontend-only change does not trigger a backend rebuild on either platform.
- No Redis, no microservices, no dedicated vector database at MVP. PostgreSQL provides search/filtering.
- LLM API keys are backend-only; never exposed to frontend or browser.

## 2. Prerequisites and Accounts

### Accounts you (the project owner) must create

| Account | Purpose | Status |
|---------|---------|--------|
| GitHub | Source control; repo `kAbhi/ai-fashion-discovery` already exists | Exists (remote `origin` configured) |
| Vercel | Frontend hosting; connect GitHub, import `frontend/` as project root | Not created |
| Render | Backend Web Service + managed PostgreSQL; connect GitHub, import `backend/` as root dir | Not created |

### Tools you need locally

| Tool | Version | Verified here |
|------|---------|---------------|
| Node | >= 22 < 23 | v22.14.0 ✅ |
| npm | bundled | 10.9.2 ✅ |
| Python | >= 3.12 < 3.14 | 3.13.2 ✅ |
| PostgreSQL | 14+ | 14.17 via Homebrew ✅ |
| Docker / Docker Compose | optional | NOT installed (see §9) |


## 3. One-Time Manual Setup

These are actions only you can perform in hosting dashboards.

### 3.1 GitHub

1. Ensure repository `kAbhi/ai-fashion-discovery` is accessible to the accounts you will connect to Vercel and Render.
2. Push this phase's commit (see §10) so both platforms have code to build.

### 3.2 Vercel (frontend)

1. Log in to [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **Add New → Project**, import `kAbhi/ai-fashion-discovery`.
3. **Important:** before deploying, open **Project Settings → Build and Development Settings → Root Directory** and set it to `frontend`.
4. Framework preset: Next.js (detected automatically).
5. Build command: `npm run build` (Vercel default for Next.js).
6. Output directory: `.next` (Vercel default).
7. Add environment variable:
   - `NEXT_PUBLIC_API_BASE_URL` = `https://<render-backend>.onrender.com` (production value; obtain after backend exists).
   - Mark as **Production** and **Preview** (browser-visible).
8. Do **not** add any `NEXT_PUBLIC_*` secrets; only `NEXT_PUBLIC_API_BASE_URL` should be browser-visible.
9. Enable automatic deployments from `main` (default). Preview deployments are automatic for branches/PRs.

### 3.3 Render (backend + database)

1. Log in to [Render Dashboard](https://dashboard.render.com).
2. **Database first:** click **New → PostgreSQL**, choose a plan:
   - MVP: Free (`0.1c-256mb`, 1 GB storage) is acceptable for evaluation but **expires 30 days after creation** and has no backups. For anything persistent, use a paid plan (`0.1c-256mb` paid or larger).
   - Region: choose the same region as the backend web service (enables internal URL / private networking).
   - Record the **External Database URL** and **Internal Database URL** from the database's **Info** page — you will enter the external URL (or internal if backend is same region) as `DATABASE_URL` on the web service.
3. **Backend:** click **New → Web Service**, connect GitHub repo `kAbhi/ai-fashion-discovery`.
4. **Root Directory:** set to `backend`.
5. Runtime: Python. Set `PYTHON_VERSION=3.13` (or add `backend/.python-version` with `3.13` — already committed).
6. Build command: `pip install -r requirements-dev.txt`
   - Prefer `pip install -r requirements.txt` in production once dev tooling is split; for MVP `requirements-dev.txt` installs everything including test tooling.
7. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. Health check path: `/health`
9. Add environment variables (see §4 table). `LLM_API_KEY` and `DATABASE_URL` are secret; toggle **Secret** on.
10. `DATABASE_URL` must use the `postgresql+psycopg://` driver form. Render's provided URL is `postgres://` or `postgresql://`; the backend config normalises `postgres://`/`postgresql://` → `postgresql+psycopg://` automatically, so you may paste Render's URL as-is.
11. CORS: set `CORS_ORIGINS=https://<your-vercel-frontend>.vercel.app` (production domain; obtain after frontend exists).
12. **Auto-deploy:** set to `commit` (default) or `checksPass` once CI exists.
13. **Pre-deploy command (migrations):** Render pre-deploy commands are available only on paid web services. On the free plan you must run `alembic upgrade head` as a one-off shell command after each schema-changing deploy. See §6.

### 3.4 Render build filter (monorepo)

To avoid unnecessary backend rebuilds when only frontend files change, configure the backend service **Build Filter**:
- Paths: `backend/**`
- Ignored paths: (leave empty)

Or rely on Render's automatic root-directory behaviour: with Root Directory `backend`, Render only redeploys when files under `backend/` change.

## 4. Environment Variables and Secrets

| Variable | Where configured | Secret? | Required | Purpose | Environments |
|----------|------------------|---------|----------|---------|--------------|
| `DATABASE_URL` | Render dashboard (backend) | Yes | Yes | PostgreSQL connection URL (Render provides internal/external URL) | preview, production |
| `TEST_DATABASE_URL` | backend `.env` (local only) | Yes | No | Test database URL | local |
| `ENVIRONMENT` | Render dashboard / `.env` | No | No | `local\|test\|preview\|production` | all |
| `LOG_LEVEL` | Render dashboard / `.env` | No | No | Logging level | all |
| `CORS_ORIGINS` | Render dashboard (backend) | No | Yes | Comma-separated allowed browser origins | preview, production |
| `CORS_ORIGIN_REGEX` | Render dashboard (backend) | No | No | Regex for Vercel Preview origins (preview backend only) | preview |
| `LLM_PROVIDER` | Render dashboard (backend) | No | No | LLM provider name | preview, production |
| `LLM_API_KEY` | Render dashboard (backend) | **Yes** | No | LLM API key | preview, production |
| `NEXT_PUBLIC_API_BASE_URL` | Vercel dashboard (frontend) | No | Yes | Backend base URL for browser calls | preview, production |

## 5. Deployment Instructions

### 5.1 Backend (Render)

1. Create the Render PostgreSQL database (§3.3) and note its External/Internal URL.
2. Create the Render Web Service with Root Directory `backend`.
3. Set build command `pip install -r requirements-dev.txt`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, health check path `/health`.
4. Enter environment variables (§4).
5. Trigger the first deploy; verify §8.

### 5.2 Frontend (Vercel)

1. Create the Vercel project with Root Directory `frontend`.
2. Enter `NEXT_PUBLIC_API_BASE_URL` = backend Render URL (§3.2).
3. Trigger the first deploy; verify §8.

### 5.3 Database migrations (Render)

Migrations are version-controlled in `backend/alembic/` via Alembic. Safe deployment strategy:

- **Paid Render plan with pre-deploy command support:** set pre-deploy command `alembic upgrade head` on the backend service. It runs once per instance after build, before deploy.
- **Free plan (no pre-deploy command):** after every deploy that includes schema changes, run a one-off migration in Render Shell (if available on your plan) or connect via `psql` using the database's external URL and run `alembic upgrade head` locally against the Render database. Never allow automatic destructive DDL; never drop tables or reset production data during deployment.

### 5.4 Rollback

- Render: use the **Rollback** button on the service's Deploys page to revert to the previous deploy.
- Vercel: use **Rollback** in the project's Deployments tab.
- Database: migrations are additive by design; if a migration must be reverted, create a new migration that undoes the change and deploy it normally.

## 6. Database and Migrations

- Primary database: PostgreSQL (Render managed in production; Docker Compose / Homebrew locally).
- Schema changes only via Alembic migration files in `backend/alembic/versions/`.
- `alembic/env.py` reads `DATABASE_URL` from the environment; `alembic.ini` intentionally has no hardcoded URL.
- Initial migration `0001_baseline` committed in this phase (empty schema; models added in later phases).
- Free Render Postgres databases expire 30 days after creation, have 1 GB storage, no backups, and no connection pooling. Upgrade to a paid plan before relying on production data.
- Backups: not available on free tier. On paid tiers, configure automated backups in Render dashboard and test restore periodically.

## 7. Environment Configuration

| Setting | Local | Preview | Production |
|---------|-------|---------|------------|
| Frontend URL | http://localhost:3000 | `https://<project>.vercel.app` (preview deployments) | `https://<project>.vercel.app` |
| Backend URL | http://localhost:8000 | `https://<backend>.onrender.com` | `https://<backend>.onrender.com` |
| Database | local Docker Compose / Homebrew PostgreSQL | Render Postgres (preview env) | Render Postgres (production env) |
| `CORS_ORIGINS` | `http://localhost:3000` | preview frontend URL | production frontend URL |
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | preview backend URL | production backend URL |
| `ENVIRONMENT` | `local` | `preview` | `production` |

- CORS on the backend is an explicit allow-list (`allow_origins`), never `*`. `CORS_ORIGIN_REGEX` supports Vercel Preview URLs on preview backends only.
- No localhost URLs in production builds; `NEXT_PUBLIC_API_BASE_URL` must be set per environment.

## 8. Verification and Smoke Tests

After each deployment:

| Check | Command / URL | Expected result |
|-------|---------------|-----------------|
| Backend availability | `curl -s https://<backend>.onrender.com/health` | HTTP 200, `{"status":"ok","database":"ok",...}` |
| Backend health (production) | Render dashboard → service → Health tab | Healthy |
| Database connectivity | included in `/health` response (`database: "ok"`) | OK |
| Frontend availability | `https://<frontend>.vercel.app` | Page loads, no console errors |
| Frontend → backend API | browser opens frontend; System Status shows "Connected" / "Reachable" | OK |
| CORS configuration | `curl -s -I -H 'Origin: https://<frontend>.vercel.app' https://<backend>.onrender.com/health` | `access-control-allow-origin` matches frontend URL |
| OpenAPI schema | `https://<backend>.onrender.com/openapi.json` | HTTP 200 (docs disabled in prod, JSON available) |
| Critical journey | open homepage, submit a shopping prompt (Phase 1+) | results grid renders |

Smoke test locally (already verified in this phase):

```bash
# backend
cd backend && source .venv/bin/activate
export DATABASE_URL=postgresql+psycopg://fashion:fashion@localhost:5432/fashion_discovery
export CORS_ORIGINS=http://localhost:3000
export ENVIRONMENT=local
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
curl -s http://localhost:8000/health   # → {"status":"ok","database":"ok"}

# frontend
cd frontend && export NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
npm run build                          # succeeds
npm run start &                        # then curl http://localhost:3000
```


## 9. Troubleshooting and Rollback

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Backend `/health` 503, `database: "unavailable"` | `DATABASE_URL` wrong or DB unreachable | Verify Render database URL; check `postgresql+psycopg://` driver form; confirm DB is in same region for internal URL |
| Frontend shows "Could not reach the backend API" | `NEXT_PUBLIC_API_BASE_URL` unset/wrong or CORS blocks frontend origin | Set `NEXT_PUBLIC_API_BASE_URL` in Vercel; add frontend URL to backend `CORS_ORIGINS` |
| Frontend build fails on Vercel | Missing `NEXT_PUBLIC_API_BASE_URL` at build or Node version mismatch | Set build-time env var; ensure Vercel uses Node 22 |
| Backend build fails on Render | `requirements-dev.txt` installs dev tools but a package lacks a wheel | Prefer `requirements.txt` for production builds; pin Python 3.13 via `.python-version` |
| Free Render backend spins down | Free plan spins down after 15 min idle; first request slow (~1 min) | Expected on free tier; upgrade to paid for always-on |
| Free Render Postgres expires | 30-day expiry, no backups | Upgrade to paid plan before day 30; export data before expiry |

Rollback: Render and Vercel both offer one-click rollback to the previous deploy from the dashboard. Database rollbacks require a new forward migration (never revert by dropping data).

## 10. Costs and Human Approvals

### Services that may incur charges

| Service | Free tier? | Notes | Approval needed? |
|---------|------------|-------|------------------|
| GitHub | Yes (public repo) | — | No |
| Vercel | Yes (hobby) | Frontend builds + bandwidth included | No for hobby; yes for Pro/team |
| Render Web Service | Yes (free, spins down after 15 min idle) | Pre-deploy commands not available on free; always-on requires paid | Yes for paid plan |
| Render PostgreSQL | Yes (free, 1 GB, expires 30 days, no backups) | Not suitable for persistent production data | Yes for paid plan |
| Custom domains / DNS | — | You configure and pay registrar directly | Yes |

### Manual actions requiring your approval (checklist in §11)

1. Create GitHub/Vercel/Render accounts or confirm existing access.
2. Create Render PostgreSQL (choose free vs paid plan).
3. Create Render Web Service and Vercel project; connect GitHub.
4. Enter production secrets (`DATABASE_URL`, `LLM_API_KEY`, `CORS_ORIGINS`, `NEXT_PUBLIC_API_BASE_URL`) in dashboards.
5. Approve production deployment after smoke tests pass.
6. Approve any paid plan upgrades.

## 11. Manual Action Checklist

| # | Action | Status | Notes |
|---|--------|--------|-------|
| 1 | Confirm GitHub access to `kAbhi/ai-fashion-discovery` | Not started | Remote `origin` already configured locally |
| 2 | Create Vercel account + connect GitHub | Not started | Required before frontend deploy |
| 3 | Create Render account + connect GitHub | Not started | Required before backend/database deploy |
| 4 | Create Render PostgreSQL database (choose plan) | Not started | Free expires after 30 days; note External URL |
| 5 | Create Render Web Service (root dir `backend`) | Not started | Build `pip install -r requirements-dev.txt`; start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`; health `/health` |
| 6 | Create Vercel project (root dir `frontend`) | Not started | Build `npm run build` |
| 7 | Configure `CORS_ORIGINS` on backend = frontend URL | Not started | Needs both frontend and backend URLs |
| 8 | Configure `NEXT_PUBLIC_API_BASE_URL` on frontend = backend URL | Not started | Needs backend URL |
| 9 | Enter `DATABASE_URL` and `LLM_API_KEY` as secrets | Not started | `LLM_API_KEY` only when Phase 2 adds LLM |
| 10 | Run smoke tests (§8) after first deploy | Not started | Backend `/health`, frontend page, CORS, DB connectivity |
| 11 | Approve production deployment | Not started | Do not mark complete until deployed app verified |

## 12. Phase Completion Notes — Phase 0

- What changed in DEPLOYMENT.md: initial full document created (all 12 sections).
- What you need to do next, in order: create Vercel and Render accounts; create Render PostgreSQL; create backend web service; create frontend project; configure environment variables; run smoke tests; approve production.
- What I completed automatically: repository scaffold, backend FastAPI + health endpoint + Alembic + tests, frontend Next.js + status page + tests, `docker-compose.yml`, `Dockerfile`s, `.env.example`, updated `README.md`, this `DEPLOYMENT.md`.
- What remains unverified or requires your intervention: Docker Compose cannot be tested locally (Docker not installed on this machine); hosting accounts/resources not created; no production deployment has been executed or verified.

| `POSTGRES_USER/PASSWORD/DB/PORT` | local `.env` / docker-compose | No (local only) | No | Local Docker Compose credentials | local |

- Never commit `.env`, `.env.local`, or any file containing real secrets.
- `.env.example` is committed with placeholder values only.
- `LLM_API_KEY` must never have the `NEXT_PUBLIC_` prefix.
