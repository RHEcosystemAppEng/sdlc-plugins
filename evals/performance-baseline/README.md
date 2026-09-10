# performance-baseline evals

Evaluates the performance-baseline skill's ability to discover workflows from source code, auto-populate configuration (scenarios, modules, workflow), and trace frontend-to-backend API calls.

**Scope limitation:** Baseline capture steps (8-10) require a running application and Playwright browser automation. These cannot be fixture-tested and are out of scope. These evals cover only workflow discovery (Steps 2-4.8) and config writing.

See [IMPROVEMENT-PLAN.md](IMPROVEMENT-PLAN.md) for the hardening roadmap and convention alignment notes.

## Test cases

| ID | Name | Steps | Tests |
|---|---|---|---|
| 1 | Frontend route discovery + config write | 2–4.7 | Route extraction from App.tsx router, workflow grouping, user selection, scenario/module auto-population, config write + validation |
| 2 | Full-stack API tracing | 2–4.8 | Frontend discovery + API call tracing from component files, backend endpoint verification via grep, scenario type tagging, traced_api_endpoints metadata, POST exclusion from scenarios |
| 3 | Missing config stop path | 2 halt | Skill detects missing config, halts with performance-setup remediation, no config written |
| 4 | Backend-only discovery | 2–3.6, 4.7 | Grep-based endpoint discovery from products.rs, workflow selection, GET scenarios only, POST excluded |
| 5 | Skip backend at 4.8.6 | 2–4.8 | Full-stack tracing then user skips backend; analysis_scope downgraded to frontend-only |
| 6 | Corrupt workflow_selected | 2.0 halt | workflow_selected=true with null workflow fields; skill halts with re-discover prompt |

## Fixtures

- `files/mock-frontend/` — React SPA with 4 routes (Home, Packages, PackageDetail, Settings), react-router-dom, @tanstack/react-query
- `files/mock-backend/` — Rust/actix-web API with 3 endpoints (list, get, scan vulnerabilities)
- `files/mock-frontend/performance/config-pre-discovery.json` — Frontend-only config with `workflow_selected: false`
- `files/mock-frontend/performance/config-pre-discovery-fullstack.json` — Full-stack config with `backend_available: true`
- `files/mock-backend/performance/config-pre-discovery-backend-only.json` — Backend-only config for eval 4
- `files/mock-frontend/performance/config-workflow-selected-incomplete.json` — Corrupt workflow seed for eval 6

## Output layout

Eval prompts specify the full output path (`outputs/mock-repo/performance-config.json`) for sandbox isolation:

```
outputs/
├── mock-repo/
│   └── performance-config.json       # evals 1, 2, 3, 5, 6
├── mock-backend/
│   └── performance-config.json       # eval 4
├── config-validation.txt             # config-producing evals
└── response.md                       # stop-path evals 3, 6
```

## Running

```
/sdlc-workflow:run-evals performance-baseline
```

## Notes

- Evals use grep-based discovery (no Serena) — `serena_status: "not-configured"`
- No live app, Playwright, Jira, or server startup — all fixture-based
- Eval 1 tests Steps 2-4.7 (frontend-only discovery and config write)
- Eval 2 tests Steps 2-4.8 (full-stack discovery with API tracing from frontend components to backend handlers)
- The POST `/api/v2/packages/:id/vulnerabilities` endpoint is intentionally included as a trace-only endpoint (appears in `traced_api_endpoints` but NOT in `scenarios`) per Step 4.8.4 rules
- Settings route (`/settings`) is present in the router but excluded from workflow `key_screens` in eval 1
