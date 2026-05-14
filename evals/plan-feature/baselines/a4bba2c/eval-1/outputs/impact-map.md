# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### Workflow Mode: `direct-to-main`

**Rationale:** No atomicity indicators identified. All changes are within a single repository (trustify-backend). The new endpoint is additive and does not break existing APIs. No coordinated schema migrations are required (uses existing `sbom_advisory` join table). No cross-cutting refactors or tightly coupled cross-repo components. Each task can be merged independently without leaving `main` in a broken state.

---

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct for the aggregation response shape
    - Add service method on SbomService to query and aggregate advisory severity counts from the sbom_advisory join table, deduplicating by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and 404 handling for missing SBOMs
    - Add optional ?threshold query parameter support for severity filtering (non-MVP)
    - Add cache invalidation in the advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
    - Update API documentation to include the new endpoint
```
