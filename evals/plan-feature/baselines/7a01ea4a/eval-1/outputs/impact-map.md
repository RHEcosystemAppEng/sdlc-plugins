# Repository Impact Map

**Feature**: TC-9001 — Add advisory severity aggregation endpoint
**Workflow Mode**: direct-to-main (see rationale below)

## trustify-backend

changes:
  - Add `AdvisorySeveritySummary` response model struct for severity count aggregation (`{ critical, high, medium, low, total }`)
  - Add severity aggregation query method to `SbomService` using the existing `sbom_advisory` join table with deduplication by advisory ID
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute `tower-http` cache and 404 response for non-existent SBOMs
  - Add optional `?threshold` query parameter for severity filtering (non-MVP)
  - Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
  - Add integration tests for the new endpoint covering success, 404, caching, and threshold filtering scenarios
  - Update API documentation (REST API reference) to include the new endpoint

## Excluded Requirements

None. All MVP and non-MVP requirements from the Feature description are covered by the changes above.

## Workflow Mode Decision

**Selected mode**: `direct-to-main`

**Rationale**: No atomicity indicators were identified:
1. **Coordinated schema migrations**: No new database tables or schema changes required — the feature uses existing `sbom_advisory` relationship tables.
2. **Breaking API changes**: The new endpoint is purely additive — no existing API contracts are modified.
3. **Cross-cutting refactors**: No structural changes to existing code — all changes add new files or extend existing modules.
4. **Tightly coupled feature components**: This is a backend-only feature in a single repository — no frontend-backend coordination required.

All tasks target `main` as their branch.

## Epic Grouping

**Strategy**: by-sub-feature (per Hierarchy Configuration in CLAUDE.md)

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9001: Severity aggregation API | Task 1 (model + service), Task 2 (endpoint), Task 3 (cache invalidation), Task 5 (integration tests) |
| Epic 2 | TC-9001: Threshold filtering | Task 4 (threshold query parameter) |
| Epic 3 | TC-9001: Documentation and readiness | Task 6 (documentation updates), Task 7 (smoke tests), Task 8 (performance benchmarks) |

## Jira Field Inheritance

The following `additional_fields` are set on every created issue (Epics and Tasks):

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **Priority**: inherited from Feature TC-9001 (Major). Not "Undefined", so propagated.
- **fixVersions**: inherited from Feature TC-9001 (RHTPA 1.5.0). No `fixVersion scope` setting found in Jira Field Defaults, so defaults to `"both"` — propagated to tasks.
