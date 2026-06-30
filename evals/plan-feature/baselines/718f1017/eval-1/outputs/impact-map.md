# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### Workflow Mode: `direct-to-main`

**Rationale:** No atomicity indicators identified. All changes are within a single repository (trustify-backend) and can be merged independently without leaving `main` in a broken state. The new endpoint, model, service, cache invalidation, and tests are additive — each task extends the codebase without breaking existing functionality.

### Field Propagation

- **Priority:** Major — will be propagated to all created tasks
- **fixVersions:** RHTPA 1.5.0 — will be propagated to all created tasks (no `fixVersion scope` restriction found in Jira Configuration; defaulting to `"both"`)

---

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model for severity count aggregation
    - Add advisory summary service method to SbomService that queries sbom_advisory join table and groups by severity
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional threshold query parameter
    - Add cache invalidation hook in advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory summary endpoint covering happy path, 404, caching, and threshold filtering
    - Update API documentation to include the new endpoint
