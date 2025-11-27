# Production Readiness Review

This document captures a quick audit of the current state of the repository with respect to production deployment, security, and operational resilience.

## Backend
- **Authentication enforcement is optional by default.** The FastAPI middleware that validates JWTs is intentionally commented out, leaving rate limiting as the only protection on all routes. Production should enable authentication and align the configuration with the expected identity provider before exposing the API. 【F:backend/api/main.py†L200-L207】
- **Secrets and credentials ship with demo defaults.** The settings layer includes a placeholder secret key and a demo API key, and it falls back to a local SQLite database URL. Move these values to required environment variables and validate them at startup to avoid running with non-production credentials. 【F:backend/config/settings.py†L21-L39】
- **Entrypoint has a hard-coded sys.path.** The server runner inserts an absolute path for module resolution, which will break in most deployment layouts and makes reproducible container builds harder. Replace this with relative imports or package installation. 【F:backend/run_server.py†L1-L15】

## Frontend
- **No build, lint, or test automation is defined.** The root `frontend/package.json` only defines a failing placeholder test script, offering no guidance for building or validating the UI. Add scripts for linting, type checks, testing, and production builds to keep the frontend shippable. 【F:frontend/package.json†L1-L13】

## Operations & Infrastructure
- **Containerization lacks secret management and hardening.** The docker-compose stack uses plaintext defaults for database and Redis, mounts the working tree into the backend container, and exposes nginx TLS paths without documented certificate handling. Introduce secrets management, hardened credentials, and immutable images for production deploys. 【F:docker-compose.yml†L6-L89】

## Recommended Next Steps
1. **Enable JWT/security middleware via environment flags and validate end-to-end.**
   - Add an environment variable (for example, `ENABLE_AUTH_MIDDLEWARE=true`) that gates the FastAPI JWT middleware.
   - Default the flag to `true` in production-like environments and `false` only for local development and automated UI testing.
   - Document required identity provider settings (issuer/audience, JWKS URL, algorithms) and add a startup check that fails fast when required values are missing.
   - Create integration tests that start the API with the flag enabled and confirm protected routes reject unauthenticated calls while accepting valid tokens.

2. **Fail-fast on secrets and connection strings.**
   - Replace placeholder values for `SECRET_KEY`, API keys, and database URLs with required environment variables; refuse startup when defaults are detected.
   - Add a `settings.validate()` hook in application startup that logs missing/weak values and exits with a non-zero status.
   - Provide `.env.example` and deployment docs that list required variables without embedding secrets.
   - Include a CI check that loads the app with a minimal `.env` to ensure validation logic executes.

3. **Refactor server entrypoints and containerize with tests.**
   - Convert the backend to an installable package (or fix relative imports) so `sys.path` hacking is unnecessary.
   - Add a Dockerfile build that installs the package, runs unit tests, and executes a smoke test (`/health` or similar) against the built image.
   - Update the compose file (or a separate production compose/k8s manifest) to run the image instead of mounting the source tree.
   - Gate merges on CI jobs that build and test the image to catch packaging regressions early.

4. **Expand frontend tooling and CI coverage.**
   - Add `lint`, `typecheck`, `test`, and `build` scripts to `frontend/package.json` using the project’s chosen stack (e.g., ESLint, TypeScript, Vitest/Jest, Vite/Next build).
   - Introduce a baseline lint config and type definitions; fail CI on lint or type errors.
   - Add minimal component/unit tests and a headless browser smoke test for critical flows (auth, core navigation).
   - Publish build artifacts (or a static bundle) as CI outputs to verify production readiness.

5. **Harden container and secrets handling.**
   - Replace plaintext credentials in `docker-compose.yml` with secrets mounted from a provider (e.g., Docker secrets, KMS, Vault) and disable bind-mounting source in production services.
   - Use non-root, read-only filesystem layers for app containers; drop Linux capabilities and enable seccomp/apparmor profiles where supported.
   - Rotate database/Redis credentials per environment and enforce TLS for inter-service traffic where possible.
   - Add runtime probes (health/readiness) and resource limits to support orchestration platforms and operational SLOs.
