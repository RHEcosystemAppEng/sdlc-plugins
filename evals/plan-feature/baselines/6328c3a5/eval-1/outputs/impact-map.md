# Repository Impact Map

## trustify-backend

### Changes

- Add `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total`
- Add severity aggregation service method to `SbomService` that queries advisory-SBOM relationships, deduplicates by advisory ID, and counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler returning severity counts
- Register the new endpoint route in the SBOM endpoints module (`modules/fundamental/src/sbom/endpoints/mod.rs`)
- Configure 5-minute response cache on the new endpoint using `tower-http` caching middleware
- Add cache invalidation in the advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to clear cached summaries when new advisories are linked to an SBOM
- Add integration tests in `tests/api/` for the new endpoint covering: valid SBOM, nonexistent SBOM (404), advisory deduplication, and cache behavior
- Add optional `?threshold` query parameter to filter severity counts above a given severity level (Non-MVP)

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified:
- No coordinated schema migrations — uses existing advisory-SBOM relationship tables, no new database tables
- No breaking API changes — this is an additive new endpoint that does not modify existing endpoints
- No cross-cutting refactors — changes are contained within the SBOM and advisory/ingestor modules
- No tightly coupled cross-repository components — this is a single-repository backend feature

All tasks can be merged to main independently without leaving the codebase in a broken state.

## Hierarchy

No Epic-level (level-1) issue type available in the project. Tasks are created directly under the Feature (Feature -> Task hierarchy). The `Default epic grouping strategy: by-sub-feature` setting in CLAUDE.md Hierarchy Configuration is noted but not applied since no level-1 type exists.

## Field Propagation

- **Priority:** Major (from Feature TC-9001) — will be propagated to all created tasks
- **Fix Versions:** RHTPA 1.5.0 (from Feature TC-9001) — will be propagated to all created tasks (`fixVersion scope: both` in Jira Field Defaults includes task-level propagation)
