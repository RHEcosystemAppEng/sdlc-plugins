# Repository Impact Map

**Feature:** TC-9001 — Add advisory severity aggregation endpoint
**Priority:** Major (inherited from feature — will be propagated to all tasks)
**Fix Version:** RHTPA 1.5.0 (inherited from feature — will be propagated to all tasks per default fixVersion scope "both")

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This feature is entirely backend within a single repository (trustify-backend). It involves no breaking API changes to existing endpoints, no coordinated schema migrations, no cross-cutting refactors, and no cross-repo dependencies. All tasks produce additive changes that can be merged independently to main without leaving the codebase in a broken state. No tightly coupled feature components exist — each task adds functionality that is self-contained even without subsequent tasks.

## Impact

```yaml
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields critical, high, medium, low, total in modules/fundamental/src/sbom/model/
    - Add advisory_summary aggregation method to SbomService that queries sbom_advisory join table, deduplicates by advisory ID, groups by severity, and returns counts
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute tower-http cache configuration in modules/fundamental/src/sbom/endpoints/
    - Add cache invalidation in advisory ingestion pipeline (modules/ingestor/src/graph/advisory/mod.rs) when new advisory-SBOM links are created
    - Add integration tests for the advisory-summary endpoint covering happy path, 404, deduplication, and cache behavior in tests/api/
    - (Non-MVP) Add optional ?threshold=critical query parameter to filter severity counts above a specified threshold
```

## Jira Operations (simulated — external services not available)

### Task Creation (Step 6a)

Each task would be created with `additional_fields`:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Priority "Major" is propagated because the feature has a set priority (not "Undefined").
fixVersions ["RHTPA 1.5.0"] is propagated because the feature has a non-empty fixVersions array and no Jira Field Defaults section exists in CLAUDE.md, so fixVersion scope defaults to "both" (propagate to tasks).

### Description Digest (Step 6a)

After creating each task, the description would be re-fetched from the Jira API, written to a temp file, and the digest computed using `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`. The resulting format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`) would be posted as a standalone ADF comment:

```
[sdlc-workflow] Description digest: sha256-md:<64-char-hex>
```

### Issue Links (Step 6b)

- Feature TC-9001 "incorporates" each created task
- Dependency links created per the Dependencies sections in each task

### Summary Comment (Step 6c)

A summary comment would be posted on TC-9001 including:
- 6 tasks created in trustify-backend
- Repository affected: trustify-backend
- Architecture: new endpoint under existing SBOM module following model/ + service/ + endpoints/ pattern, with cache invalidation in the ingestion pipeline
- Priority "Major" propagated to all tasks (inherited from feature)
- fixVersion "RHTPA 1.5.0" propagated to all tasks (inherited from feature; fixVersion scope defaults to "both")
