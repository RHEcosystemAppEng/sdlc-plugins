# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

> This file is the content of the impact map comment the skill would post on TC-9001 (Step 4), followed by the workflow mode decision (Step 4.5) and the task creation log (Step 6).

## Feature inputs (Step 1)

| Field | Value |
|---|---|
| Key | TC-9001 |
| Summary | Add advisory severity aggregation endpoint |
| Priority | Major (set — will be inherited) |
| Fix Versions | RHTPA 1.5.0 (non-empty — will be inherited) |
| Figma | None (backend-only feature; Step 2 skipped) |
| Parent link (Step 1.5) | None set; skipped (non-interactive eval run) |
| Documentation signals | Doc impact: **Updates** — add endpoint to REST API reference; user purpose: API consumers need path, parameters, response shape; reference: existing SBOM advisory endpoints docs |
| Testing readiness template | Found at `docs/testing-readiness.md` — categories: **Smoke Tests**, **Performance Benchmarks** |
| CONVENTIONS.md | Present at repo root (`trustify-backend/CONVENTIONS.md`); conventions applied: Module pattern, Error handling, Endpoint registration, Query helpers, Testing, Caching |

## Impact map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model { critical, high, medium, low, total } in modules/fundamental/src/sbom/model/advisory_summary.rs and export it from sbom/model/mod.rs
    - Add SbomService::advisory_severity_summary in modules/fundamental/src/sbom/service/sbom.rs: single GROUP BY severity query over entity sbom_advisory ⨝ advisory with COUNT(DISTINCT advisory.id); not-found error for unknown SBOM; zeros for SBOM without advisories
    - Add handler modules/fundamental/src/sbom/endpoints/advisory_summary.rs and register GET /api/v2/sbom/{id}/advisory-summary in sbom/endpoints/mod.rs with 404 for unknown SBOM
    - Configure 5-minute (300 s) tower-http response caching for the new route, keyed per SBOM ID + query string, 404s not cached
    - Invalidate the SBOM's cached summary from the advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs) after new sbom_advisory links commit; share the cache handle via server/src/main.rs into IngestorService (modules/ingestor/src/service/mod.rs)
    - Invalidate from SBOM ingestion (modules/ingestor/src/graph/sbom/mod.rs) if it also writes sbom_advisory links for an existing SBOM
    - Add optional ?threshold={critical|high|medium|low} query parameter returning only severities at or above the threshold; 400 on invalid values (non-MVP)
    - Add integration tests in tests/api/sbom.rs (endpoint, dedup, 404, caching, threshold) and tests/api/advisory.rs (ingestion invalidation)
    - Update the REST API reference with the new endpoint
    - Run Smoke Tests and Performance Benchmarks per docs/testing-readiness.md
```

## Shared-artifact producer/consumer analysis (Step 3)

The cached advisory summary is derived from the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).

| Role | Path | Coverage |
|---|---|---|
| Producer (primary) | `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion/correlation | Task 3 (invalidation + `tests/api/advisory.rs`) |
| Producer (to verify) | `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion; invalidate if it writes `sbom_advisory` rows for an existing SBOM | Task 3 (conditional AC + test) |
| Consumer | `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (new) via `SbomService` | Tasks 1, 2, 4 (`tests/api/sbom.rs`) |

No scope exclusions conflict with the acceptance criteria.

## Clarifications recorded

- **Threshold response shape**: Requirements say "filter counts above a severity" while UC-2 says "only critical count is returned" for `threshold=critical`. Planned interpretation: include severities **at or above** the threshold, omit lower keys, `total` = sum of included. Confirm with the feature owner before Task 4 is implemented.
- **Unknown severities**: advisories without a recognized severity are not counted in any bucket; `total` = critical + high + medium + low. Confirm with feature owner.

## Excluded requirements

| Requirement | Reason excluded (missing input) |
|---|---|
| Add the new endpoint to the API latency Grafana dashboard (Customer Information/Supportability) | No repository for Grafana dashboards / monitoring configuration exists in the Repository Registry; dashboard definitions are not in `trustify-backend`. Provide the observability repo (and add it to the registry) to plan this. |
| Alert if p95 exceeds 500ms (Customer Information/Supportability) | Same as above — no target repository for alerting rules (e.g., Prometheus/Grafana alert config). |
| UC-1 frontend dashboard widget rendering the severity bar chart / removing client-side counting | No frontend repository in the Repository Registry and no Figma design provided; this feature is scoped to the backend endpoint. Frontend adoption must be planned separately. |

---

# Workflow Mode Decision (Step 4.5)

**Selected mode: `direct-to-main`**

Atomicity indicators evaluated:

1. Coordinated schema migrations — **not present** (NFR: no new tables; no migrations).
2. Breaking API changes — **not present** (new endpoint is purely additive; Task 4 adds an optional parameter; existing endpoints unchanged).
3. Cross-cutting refactors — **not present**.
4. Tightly coupled feature components — **not present** (backend-only; each task merges independently: Task 1 adds an unused service method, Task 2 exposes it, Task 3 adds invalidation, Task 4 adds the optional filter — `main` stays functional after each merge; before Task 3 lands, summaries can be at most 5 minutes stale, which is not a broken state).

All tasks target `main`. No bookend tasks. No `workflow:feature-branch` label.

---

# Hierarchy (Step 2.5 / Step 5 Epic grouping)

- Issue type discovery (`jira.get_project_issue_types(2b9e35e3-6bd3-4cec-b838-f4249ee02432, TC)`) could not be executed (no Jira access in this eval run). Planned behavior: if a level-1 type exists, create Epics; otherwise fall back to Feature → Task with Incorporates links to tasks.
- Hierarchy Configuration in CLAUDE.md: `Default epic grouping strategy: by-sub-feature` — applied without prompting.
- Proposed Epic groups (created only if a level-1 type is discovered):

| Epic summary | Tasks |
|---|---|
| TC-9001: Advisory summary API | Task 1, Task 2, Task 4, Task 5 |
| TC-9001: Ingestion cache invalidation | Task 3 |
| TC-9001: Feature validation | Task 6, Task 7 |

---

# Task Creation Log (Step 6)

## additional_fields applied to every created issue (Epics and Tasks)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: Feature priority is `Major` (not "Undefined") → propagated.
- **fixVersions**: Feature has `RHTPA 1.5.0`, and CLAUDE.md `fixVersion scope: both` → propagated to tasks.

## Tasks

| # | File | Summary | Issue type | Target Branch | Depends on | Epic (if available) | Description digest |
|---|---|---|---|---|---|---|---|
| 1 | task-1-severity-aggregation-service.md | Add advisory severity aggregation model and service method | Task | main | — | Advisory summary API | `sha256-md:cfdc993f8035fc4441e0a4ded37f14a4bb8ef67c7cf7024188e5db77e5c221f5` |
| 2 | task-2-advisory-summary-endpoint.md | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | Task | main | 1 | Advisory summary API | `sha256-md:64090e511d0308d71011280548658352768548361a8eb36bd02acc10df35ecb9` |
| 3 | task-3-cache-invalidation-on-ingestion.md | Invalidate advisory-summary cache on advisory ingestion | Task | main | 2 | Ingestion cache invalidation | `sha256-md:9bf19993457b5f7de5e4b13b8382b2cc8136e3d058f6df9f4a4e3de76e67499c` |
| 4 | task-4-severity-threshold-filter.md | Add optional severity threshold filter to advisory-summary endpoint | Task | main | 2 | Advisory summary API | `sha256-md:7aec08e844bbca571ede823c169e47736dcd853966105b96e440b29139289efe` |
| 5 | task-5-api-reference-docs.md | Document advisory-summary endpoint in REST API reference | Task | main | 1, 2, 3, 4 | Advisory summary API | `sha256-md:eea052ab87caa203741ad17c07edce8f1cef33bd1cb4fb511a0df65c3ccb7ba6` |
| 6 | task-6-smoke-tests.md | Smoke tests for advisory severity aggregation | Task | main | 1, 2, 3, 4 | Feature validation | `sha256-md:bd1688d561a77d9a840c3494592b56d0b7a3301fe213f55d9611c4df49610571` |
| 7 | task-7-performance-benchmarks.md | Performance benchmarks for advisory severity aggregation | Task | main | 1, 2, 3, 4 | Feature validation | `sha256-md:6684008d1beea6a328f96edcf55ec6cb52cb316cd7e61d8cc5bc3e6ac22b7882` |

Digests were computed with `scripts/sha256-digest.py` over each task description (markdown). In a live run the description is re-fetched from Jira after creation and hashed as persisted. Digest comments: `task-N-digest.md`.

## Links (Step 6b)

- Incorporates: TC-9001 → each Epic (or → each Task if no level-1 type exists)
- Depend: Task 2 → Task 1; Task 3 → Task 2; Task 4 → Task 2; Tasks 5, 6, 7 → Tasks 1, 2, 3, 4 (DAG, no cycles)

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
