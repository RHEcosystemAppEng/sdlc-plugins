# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Run context and non-interactive decisions

| Step | Decision | Rationale |
|---|---|---|
| Step 0 — Project Configuration | PASS | CLAUDE.md has Repository Registry, Jira Configuration (Project key TC, Cloud ID, Feature type ID 10142), and Code Intelligence. |
| Step 0.5 — Jira access | Offline (eval) | No external calls; all Jira writes are emitted as files in this directory. |
| Step 1 — Feature fetch | From `feature-standard.md` | Priority = `Major` (set, propagate). fixVersions = `RHTPA 1.5.0` (non-empty, propagate). |
| Step 1 — Documentation signals | Present | Doc impact type = **Updates** ("add endpoint to REST API reference"). Documentation task generated. |
| Step 1.5 — Parent link | Skipped (default = press Enter) | Feature has no parent; non-interactive run chooses to skip the optional link. |
| Step 2 — Figma | Skipped | No Figma URL in arguments or description. Backend-only feature. |
| Step 2.5 — Issue types | No level-1 type confirmed → Feature → Task hierarchy | Project issue types cannot be fetched offline, so no Epic-level type could be discovered. Per constraint 1.64/1.80 the skill falls back to Feature → Task without error. `Hierarchy Configuration: by-sub-feature` is recorded but not applied because Epic creation is skipped. |
| Step 3 — Code intelligence | No Serena instance → fallback analysis of `repo-backend.md` structure | Registry has no Serena instance; target repo structure supplied as fixture. |
| Step 3 — CONVENTIONS.md | Present at repo root (`trustify-backend/CONVENTIONS.md`) | Contents summarized in the fixture's "Key Conventions"; those conventions are used for enrichment. |
| Step 3 — Testing readiness template | Found at `docs/testing-readiness.md` | Categories: **Smoke Tests**, **Performance Benchmarks** → 2 testing tasks. |
| Step 4 — Impact map approval | Auto-approved (non-interactive) | |
| Step 4.5 — Workflow mode | **direct-to-main** | See "Workflow Mode Decision" below. |
| Step 5 — Epic grouping prompt | Not shown | No Epic type available. |
| Priority prompt (Jira Field Defaults: Prompt for priority = true) | Inherit Feature priority `Major` | Default choice in non-interactive mode. |
| fixVersion prompt (Prompt for fixVersion = true) | Inherit Feature fixVersion `RHTPA 1.5.0` | `fixVersion scope: both` → propagate to tasks. |

## Repository analysis summary (trustify-backend)

- SBOM module: `modules/fundamental/src/sbom/` — `endpoints/mod.rs` registers `/api/v2/sbom`; `endpoints/get.rs` serves `GET /api/v2/sbom/{id}` (existing 404 pattern); `service/sbom.rs` (`SbomService`: fetch, list, ingest); `model/summary.rs`, `model/details.rs`.
- Advisory module: `modules/fundamental/src/advisory/` — `model/summary.rs` (`AdvisorySummary`, includes `severity` field); `service/advisory.rs` (`AdvisoryService`).
- Entities: `entity/src/sbom_advisory.rs` (SBOM–Advisory join table — the data source; no new tables per NFR), `entity/src/advisory.rs`, `entity/src/sbom.rs`.
- Shared helpers: `common/src/db/query.rs` (query builder helpers), `common/src/error.rs` (`AppError`, `IntoResponse`).
- Caching: `tower-http` caching middleware configured in endpoint route builders.
- Ingestion: `modules/ingestor/src/graph/advisory/mod.rs` (advisory parse/store/**correlate** → writes SBOM–advisory links), `modules/ingestor/src/graph/sbom/mod.rs` (SBOM parse/store/link), `modules/ingestor/src/service/mod.rs` (`IngestorService`).
- Server: `server/src/main.rs` mounts module routes.
- Tests: `tests/api/sbom.rs`, `tests/api/advisory.rs` (integration tests against real PostgreSQL).
- Docs: `README.md`, `CONVENTIONS.md`, `docs/testing-readiness.md`. No dedicated REST API reference file found in the tree — the documentation task leaves file selection to the implementer.

### Shared-artifact producer/consumer analysis — cached advisory summary

The cached per-SBOM severity summary is a shared artifact whose correctness depends on the `sbom_advisory` link set.

| Role | Path | Coverage |
|---|---|---|
| Producer (populates cache) | `modules/fundamental/src/sbom/endpoints/` (new `advisory_summary.rs`) via `SbomService` | Task 2 |
| Writer of underlying data — primary | `modules/ingestor/src/graph/advisory/mod.rs` (advisory correlation links advisories to SBOMs) | Task 3 (invalidate) |
| Writer of underlying data — SBOM (re-)ingestion | `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingest/link; re-ingesting an SBOM can change its advisory links) | Task 3 (invalidate — implementer must confirm whether this path writes `sbom_advisory`; if it does, invalidate) |
| Orchestration (on-demand/API-triggered ingestion) | `modules/ingestor/src/service/mod.rs` (`IngestorService`) | Task 3 |
| Consumer | `GET /api/v2/sbom/{id}/advisory-summary` | Tasks 2, 4 |

Open risk recorded: the repo uses `tower-http` caching middleware. If this provides only HTTP `Cache-Control` headers (no server-side store), server-side invalidation from the ingestion pipeline is not possible for client/proxy caches. Task 2/3 instruct the implementer to verify the existing cache infrastructure supports keyed server-side invalidation; if it does not, they must stop and raise this rather than shipping a header-only cache that silently serves stale counts.

## Impact Map

```
trustify-backend:
  changes:
    - Add a severity-summary response model (critical, high, medium, low, total) for an SBOM's advisories
    - Add an SbomService method that counts unique advisories per severity for an SBOM using the existing sbom_advisory join table (no new tables)
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint, returning 404 for unknown SBOM IDs, cached for 5 minutes via existing cache infrastructure
    - Invalidate the cached summary for an SBOM whenever advisory ingestion (and any SBOM re-ingestion path) changes that SBOM's advisory links
    - (Non-MVP) Support optional ?threshold=<severity> query parameter on the advisory-summary endpoint
    - Update REST API reference documentation with the new endpoint
    - Run Smoke Tests and Performance Benchmarks per docs/testing-readiness.md
```

## Excluded requirements

| Requirement | Missing input preventing planning |
|---|---|
| Add the new endpoint to the API latency Grafana dashboard (Customer Information/Supportability) | No repository in the Repository Registry or fixture owns Grafana dashboard definitions / observability config. Provide the dashboards repository (or confirm it is managed outside code) to plan this. |
| Alert if p95 exceeds 500ms (Customer Information/Supportability) | Same — no alerting/monitoring-rules repository is available to the plan. |

## Planned tasks

| # | Title | Type | Depends on |
|---|---|---|---|
| 1 | Add advisory severity summary model and service aggregation | Implementation | — |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | Implementation | 1 |
| 3 | Invalidate cached advisory summaries on advisory/SBOM ingestion | Implementation | 2 |
| 4 | Support ?threshold query parameter on advisory-summary endpoint (non-MVP) | Implementation | 2 |
| 5 | Document advisory-summary endpoint in REST API reference | Documentation | 1, 2, 3, 4 |
| 6 | Smoke Tests for advisory severity aggregation | Testing | 1, 2, 3, 4 |
| 7 | Performance Benchmarks for advisory severity aggregation | Testing | 1, 2, 3, 4 |

## Workflow Mode Decision

**Mode: `direct-to-main`**

Atomicity indicators evaluated:
1. Coordinated schema migrations — **none** (NFR: no new tables; no migration).
2. Breaking API changes — **none**. The endpoint is new and additive; no existing contract changes.
3. Cross-cutting refactors — **none**.
4. Tightly coupled feature components — **none**. Single backend repository; each task merges independently: Task 1 adds an unused service method (compiles, no behavior change), Task 2 exposes it, Task 3 adds invalidation, Task 4 adds an optional parameter.

All tasks use Target Branch `main`. No bookend tasks; `workflow:feature-branch` label is not applied.

## Jira `additional_fields` for created issues

Applied to all 7 tasks (no Epics created):

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- Issue type: Task (level 0), project `TC`, no `parent` (no Epic type available).
- Links: Feature TC-9001 "Incorporates" each task; "Depend" links per the table above.
- Full per-task log: see `task-creation-log.md`.
