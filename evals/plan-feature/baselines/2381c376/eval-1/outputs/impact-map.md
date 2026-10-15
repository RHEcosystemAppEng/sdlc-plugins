# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators were found. All changes are additive (new endpoint, new model, new service method) within a single repository. No coordinated schema migrations, no breaking API changes, no cross-cutting refactors, and no tightly coupled frontend/backend dependencies. Each task's PR can land on `main` independently without breaking the codebase.

## trustify-backend

### Changes

- Add `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total`
- Add aggregation service method on `SbomService` that queries the `sbom_advisory` join table, groups advisories by severity, deduplicates by advisory ID, and returns severity counts
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache via `tower-http` caching middleware
- Add optional `?threshold` query parameter to filter severity counts above a given level
- Return 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints
- Add cache invalidation logic in the advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached advisory summaries when new advisories are linked to an SBOM
- Add integration tests in `tests/api/` covering: happy path severity counts, 404 for missing SBOM, threshold filtering, advisory deduplication
- Update REST API reference documentation to include the new endpoint

### Excluded Requirements

None. All MVP and non-MVP requirements from the feature description can be decomposed into actionable tasks within the trustify-backend repository.

## Task Creation Log — Field Inheritance

All created tasks receive the following `additional_fields`:

```
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **Priority**: "Major" — inherited from Feature TC-9001 (not "Undefined", so propagated)
- **fixVersions**: ["RHTPA 1.5.0"] — inherited from Feature TC-9001. No `Jira Field Defaults` section in CLAUDE.md, so default `fixVersion scope` of "both" applies; versions propagated to all tasks.
