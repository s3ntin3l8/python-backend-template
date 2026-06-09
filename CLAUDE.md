# CLAUDE.md — FastAPI Backend Template

A FastAPI starter wired to the centralized CI/CD in
[`s3ntin3l8/.github`](https://github.com/s3ntin3l8/.github). If you are an AI agent or
developer working in a repo created from this template, read this first.

## First steps after creating a repo from this template

1. Rename the placeholders: `name = "project-name"` in `pyproject.toml`, the
   `# Project Name` title in `README.md`, and the `FastAPI(title=...)` in
   `app/main.py`.
2. `make install` — creates `.venv`, installs the project (editable, with the `dev`
   extra) and the pre-commit hooks.
3. Decide your CI coverage floor: `.github/workflows/ci-cd.yml` ships
   `coverage-fail-under: '0'` (a starter floor) — **ratchet it up** as you add real code.

## Commands (Makefile)

| Command | Does |
|---------|------|
| `make install` | Create venv, install `.[dev]`, install pre-commit + pre-push hooks. |
| `make dev` | Run the dev server with hot reload (`uvicorn app.main:app --reload`). |
| `make run` | Run the server without reload. |
| `make test` | Run the pytest suite. |
| `make lint` | `pre-commit run --all-files` (ruff + ruff-format + mypy + detect-secrets). |
| `make format` | Auto-fix formatting with ruff. |
| `make clean` | Remove venv and caches. |

## Layout

- `app/main.py` — FastAPI app + routes (`/`, `/health`).
- `app/core/` — `config.py` (pydantic-settings `settings`), `logging.py` (JSON
  formatter), `encryption.py` (optional Fernet field encryption, keyed by
  `DB_ENCRYPTION_KEY`), `date_utils.py` (ISO-8601/UTC helpers).
- `tests/` — pytest (`asyncio_mode=auto`); httpx `ASGITransport` for endpoint tests.
- `Dockerfile` — slim, non-root `uvicorn` image (built/pushed by CI).
- `.github/workflows/` — thin callers of the reusable workflows in `s3ntin3l8/.github`.

## CI/CD — uses centralized reusable workflows

Workflows here are **callers** of `s3ntin3l8/.github/.github/workflows/*.yml@main`:
`ci-cd.yml` (ci-python + docker-publish), `codeql.yml`, `dependency-review.yml`,
`release-please.yml`, `cleanup-ghcr.yml`.

**The #1 thing to get right:** a caller job that invokes a reusable workflow needing
write scopes **must declare a `permissions:` block** — the default `GITHUB_TOKEN` is
read-only and the run otherwise fails at startup with zero jobs. `build-docker` needs
`contents: read` + `packages: write` + `id-token: write`; `codeql` needs
`security-events: write`; `release-please` needs `contents: write` +
`pull-requests: write`. See the `s3ntin3l8/.github` README for the full table.

`ci-python` installs deps via `pip install -e ".[dev]"`, so keep dev tooling
(ruff/mypy/pytest/etc.) in the `[project.optional-dependencies] dev` group of
`pyproject.toml`. If your package isn't named `app`, pass `coverage-source:` to the
`test-python` caller.

## Conventions

- **Python 3.12+, async-first.** FastAPI + Pydantic v2 + `httpx`.
- **Conventional Commits** — Release Please cuts versions/changelogs from them.
- **Typing + lint enforced** by ruff and mypy (config in `pyproject.toml`); run
  `make lint` before pushing (the pre-push hook runs the full suite).
- **Secrets:** never commit real credentials; `detect-secrets` runs in pre-commit and
  CI against `.secrets.baseline` (regenerate with
  `detect-secrets scan > .secrets.baseline` after vetting new detections).
