# Repository Impact Map

**Feature:** TC-9001 — Add advisory severity aggregation endpoint
**Priority:** Major (inherited from Feature)
**Fix Versions:** RHTPA 1.5.0 (inherited from Feature)

## trustify-backend

### Changes

- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in the sbom model layer
- Add severity aggregation query method to `SbomService` that joins `sbom_advisory` with `advisory` entities, deduplicates by advisory ID, and counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache via tower-http caching middleware
- Return 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints
- Add optional `?threshold=critical` query parameter to filter severity counts above a threshold (non-MVP)
- Add cache invalidation logic to the advisory ingestion pipeline so cached summaries are invalidated when new advisories are linked to an SBOM
- Add integration tests for the advisory-summary endpoint covering: valid SBOM, nonexistent SBOM (404), deduplication, threshold filtering, and caching behavior

### Excluded Requirements

None. All requirements (MVP and non-MVP) can be planned against the trustify-backend repository.

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:
- No coordinated schema migrations (no new database tables required)
- No breaking API changes (this is a new additive endpoint)
- No cross-cutting refactors (changes are scoped to the sbom module and ingestion pipeline)
- No tightly coupled cross-repo components (single repository, backend only)

All tasks can be merged independently into `main` without leaving the codebase in a broken state.

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration)

- **Epic 1: TC-9001: Severity aggregation API** — Tasks 1, 2, 4 (model, endpoint, threshold parameter)
- **Epic 2: TC-9001: Cache management** — Task 3 (cache invalidation in ingestion pipeline)
- **Epic 3: TC-9001: Validation and documentation** — Tasks 5, 6, 7, 8 (integration tests, documentation, smoke tests, performance benchmarks)

## Task Field Inheritance

Every created task (and Epic) will include the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **Priority:** "Major" inherited from Feature TC-9001 (not "Undefined", so propagated)
- **fixVersions:** "RHTPA 1.5.0" inherited from Feature TC-9001. No `fixVersion scope` setting found in Jira Field Defaults — defaulting to "both" (propagate to tasks).
