# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Feature metadata (Step 1)
- Priority: Major (set → inherited by all created tasks)
- Fix Versions: RHTPA 1.5.0 (non-empty; CLAUDE.md `fixVersion scope: both` → inherited by all created tasks)
- Documentation signals: Doc impact = **Updates** (add endpoint to REST API reference). Details: API consumers need the path, parameters, and response shape. Reference: existing SBOM advisory endpoints docs.
- Figma: none (backend-only feature; Step 2 skipped)
- Parent link (Step 1.5): skipped. The Feature has no parent, and the eval doesn't allow prompting.

## Repository analysis inputs (Step 3)
- Target repo: trustify-backend (structure from repo-backend.md; no Serena instance → manifest/Glob-style analysis)
- CONVENTIONS.md: present at the repo root. Conventions used: Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching. Each task applies only the conventions whose file scope matches its files.
- Testing readiness template: `docs/testing-readiness.md` found with 2 categories (Smoke Tests, Performance Benchmarks) → 2 testing tasks
- Documentation files: `README.md`, `CONVENTIONS.md`
- Eval infrastructure: N/A (no SKILL.md changes)
- Reuse candidates: `AdvisoryService` (advisory/service/advisory.rs), `AdvisorySummary.severity` (advisory/model/summary.rs), `entity/src/sbom_advisory.rs`, `common/src/db/query.rs`, `common/src/error.rs::AppError`, the `sbom/endpoints/get.rs` 404 pattern

### Shared-artifact producer/consumer map (cached advisory summary)
| Role | Path | Coverage |
|---|---|---|
| Source data | `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) | Task 1 |
| Producer (writes links) | `modules/ingestor/src/graph/advisory/mod.rs` (advisory correlation) | Task 3 (invalidation + test) |
| Possible producer | `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion; the manifest shows only package linking) | Task 3 (verify; invalidate and test if it writes `sbom_advisory`) |
| Cache owner | `modules/fundamental/src/sbom/endpoints/mod.rs` route builder | Task 2 |
| Consumer | `GET /api/v2/sbom/{id}/advisory-summary` (`sbom/endpoints/advisory_summary.rs`) | Tasks 2, 4 |

## Impact map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model {critical, high, medium, low, total} in modules/fundamental/src/sbom/model/advisory_summary.rs
    - Add SbomService::advisory_severity_summary: a grouped COUNT(DISTINCT advisory.id) by severity over sbom_advisory + advisory, with not-found for an unknown SBOM
    - Add GET /api/v2/sbom/{id}/advisory-summary handler (sbom/endpoints/advisory_summary.rs) and register it in sbom/endpoints/mod.rs, returning 404 for an unknown SBOM
    - Configure a 5-minute per-SBOM cache on the advisory-summary route with an invalidation hook
    - Invalidate the cached summary for affected SBOMs in advisory ingestion correlation (ingestor/src/graph/advisory/mod.rs), wired through IngestorService and server/src/main.rs
    - Add optional ?threshold=<severity> query param to the advisory-summary endpoint (non-MVP)
    - Add integration tests in tests/api/sbom.rs for counts, dedup, 404, caching, invalidation, and threshold
    - Update the REST API reference with the new endpoint
    - Run cross-cutting Smoke Tests and Performance Benchmarks per docs/testing-readiness.md
```

## Excluded requirements
- **Add the endpoint to the API latency Grafana dashboard / alert if p95 > 500ms** (Customer Information/Supportability). Missing input: no monitoring or dashboard-config repository is in the Repository Registry, and repo-backend.md has no Grafana or alerting configuration. Provide the monitoring repo (or confirm where dashboards live) to plan this work.

## Workflow mode (Step 4.5)
- **Mode: direct-to-main**
- Rationale: no atomicity indicators.
  - No schema migrations: the feature explicitly forbids new tables and uses the existing `sbom_advisory` table.
  - No breaking API changes: the new endpoint is additive and the threshold param is optional.
  - No cross-cutting refactors.
  - No tightly coupled frontend/backend pair in scope: this is backend only, and the dashboard can adopt the endpoint later.
- Each task can merge to main in order (1 → 2 → 3/4) without breaking main.

## Hierarchy (Step 2.5)
- Issue types could not be discovered (no Jira access in the eval). Assumption: no level-1 (Epic) type is available → graceful degradation to Feature → Task. CLAUDE.md sets `Default epic grouping strategy: by-sub-feature`. If an Epic type exists, the suggested grouping would be: "TC-9001: Advisory summary endpoint" (Tasks 1, 2, 4), "TC-9001: Cache invalidation" (Task 3), and "TC-9001: Docs & validation" (Tasks 5–7).

## Task list and dependencies (DAG)
| # | Task | Depends on |
|---|---|---|
| 1 | Add advisory severity aggregation model and service method | — |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | 1 |
| 3 | Invalidate cached advisory summaries on advisory ingestion | 2 |
| 4 | Add optional threshold query parameter to advisory-summary endpoint | 2 |
| 5 | Document advisory-summary endpoint in REST API reference | 2, 3, 4 |
| 6 | Smoke Tests | 1, 2, 3, 4 |
| 7 | Performance Benchmarks | 1, 2, 3, 4 |

All tasks: Repository = trustify-backend, Target Branch = main.
