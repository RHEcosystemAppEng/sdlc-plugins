[sdlc-workflow] Planning complete for TC-9001: Add advisory severity aggregation endpoint

## Tasks Created

| # | Title | Type | Repository |
|---|-------|------|------------|
| 1 | Add advisory severity summary model | Implementation | trustify-backend |
| 2 | Implement advisory severity aggregation service | Implementation | trustify-backend |
| 3 | Add advisory-summary endpoint with caching | Implementation | trustify-backend |
| 4 | Add cache invalidation on advisory ingestion | Implementation | trustify-backend |
| 5 | Add integration tests for advisory-summary endpoint | Implementation | trustify-backend |
| 6 | Update REST API reference documentation | Documentation | trustify-backend |
| 7 | Smoke tests | Testing | trustify-backend |
| 8 | Performance benchmarks | Testing | trustify-backend |

**Total**: 8 tasks (5 implementation, 1 documentation, 2 testing)

## Repositories Affected
- **trustify-backend** (sole repository) — 3 new files, 4 modified files

## Architecture Summary
The implementation adds a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint following the existing module pattern (model + service + endpoint). A new `AdvisorySeveritySummary` model struct holds severity counts. The `SbomService` gains an aggregation method that queries the existing `sbom_advisory` join table, grouping by severity and deduplicating by advisory ID. The endpoint handler is registered under the SBOM route namespace with 5-minute response caching via `tower-http`. Cache invalidation is added to the advisory ingestion pipeline to ensure freshness when new advisories are correlated.

## Field Propagation
The following field values were inherited from feature TC-9001 and propagated to all 8 created tasks:
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## additional_fields on Created Issues
```json
{
  "priority": { "name": "Major" },
  "fixVersions": [{ "name": "RHTPA 1.5.0" }]
}
```
