# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

AI-powered New Zealand self-driving trip planner (Chinese-language UI). Single Python/FastAPI backend serves both the REST API and the vanilla HTML/CSS/JS frontend as static files. No database — file-based storage only. The LLM backend is DeepSeek (`deepseek-chat` model via the OpenAI-compatible SDK).

### Running the dev server

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Opens at `http://localhost:8000`. The frontend is auto-served from `frontend/`.

### Environment variables

The app requires `DEEPSEEK_API_KEY` (injected as a Cursor secret or written to `.env` at the project root). Optional: `DEEPSEEK_TIMEOUT_SECONDS`, `DEEPSEEK_RETRY_MAX`, `DEEPSEEK_RETRY_BASE_DELAY`.

### Running tests

```bash
python3 scripts/acceptance_test.py
```

This runs mocked validator unit tests. Note: the second test function (`test_llm_validation_before_write`) has a pre-existing bug — it catches `ValueError` but `generate_plan` raises `DeepSeekError`, causing an unhandled exception. The first four validator checks (5.1–5.3) pass correctly.

### Gotchas

- `pip install` installs to `~/.local/bin` which may not be on `PATH`. Either use `python3 -m uvicorn` or ensure `~/.local/bin` is on `PATH`.
- The `.env` file must exist at the project root for `python-dotenv` to load `DEEPSEEK_API_KEY` when running locally. If the secret is already an env var (e.g. via Cursor secrets), the app picks it up directly via `os.getenv`.
- Plan generation calls the external DeepSeek API and takes ~15–30 seconds per request.
- No linter is configured in the repo (no flake8/ruff/pylint config). No `pyproject.toml` or linting scripts exist.
