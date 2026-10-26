# Repository Impact Map — TC-9001

## trustify-backend

**changes:**
- Add `AdvisorySeveritySummary` response model struct to the SBOM model module (`modules/fundamental/src/sbom/model/`)
- Add severity aggregation service method to `SbomService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, and counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with route registration and 5-minute cache via `tower-http` caching middleware
- Add optional `?threshold` query parameter support for severity filtering (non-MVP)
- Add cache invalidation logic in the advisory ingestion pipeline to clear cached advisory summaries when new advisories are linked to an SBOM
- Add integration tests for the advisory summary endpoint covering success, 404, caching, and threshold filtering scenarios

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were found:
1. No coordinated schema migrations — the feature uses existing database tables (`sbom_advisory` join table) with no new migrations required.
2. No breaking API changes — the feature adds a new endpoint without modifying existing endpoints.
3. No cross-cutting refactors — changes are additive within the existing module structure.
4. No tightly coupled cross-repo components — all changes are within the `trustify-backend` repository.

Each task PR can be merged independently to `main` without leaving the codebase in a broken state.

## Excluded Requirements

None — all requirements (MVP and non-MVP) from the feature description can be planned with the available `trustify-backend` repository structure.

## Inherited Field Values

- **Priority:** Major — propagated to all created tasks
- **fixVersions:** RHTPA 1.5.0 — propagated to all created tasks (no `fixVersion scope` setting in CLAUDE.md Jira Field Defaults; defaults to "both")
