# performance-setup evals

Evaluates the performance setup skill's ability to detect project architecture, configure analysis scope, handle Serena discovery, and produce a valid performance config.

## Test cases

| ID | Name | Tests |
|---|---|---|
| 1 | Frontend-only greenfield | Architecture 3, no Serena, CONVENTIONS.md missing warning, frontend-only scope |
| 2 | Full-stack monorepo + Serena | Architecture 1, actix-web detection, Serena onboarded, hybrid metrics |
| 3 | Separate repos, no Serena | Architecture 2, manual express entry, cross-repo paths, grep-based fallback |
| 4 | Backend-only | Architecture 4, backend-only scope, no frontend repository |
| 5 | Serena skip | Serena discovered but not onboarded, user skips, serena_status='skipped' |

## Fixtures

- `files/mock-frontend-next/` — Minimal Next.js project (package.json, next.config.js, page.tsx)
- `files/mock-backend-rust/` — Rust/actix-web backend with sea-orm (strong detection indicators)
- `files/mock-backend-node/` — Express backend (low-confidence detection, tests manual entry)
- `files/mock-backend-only/` — Standalone Rust backend for backend-only architecture
- `files/mcp-tools-no-serena.md` — MCP tool listing without Serena
- `files/mcp-tools-with-serena.md` — MCP tool listing with onboarded Serena instance
- `files/mcp-tools-serena-not-onboarded.md` — Serena present but not onboarded

## Running

```
/sdlc-workflow:run-evals performance-setup
```

## Notes

- Evals cover Steps 0–8 of the setup skill (no workflow selection or baseline capture)
- Every config-producing eval requires `perf-config.py validate` output in `config-validation.txt`
- No live MCP calls, server startup, or dependency installation — all fixture-based
- Assertions focus on skill-owned contract (scope, framework, Serena status, repo paths), not `perf-config.py` defaults
