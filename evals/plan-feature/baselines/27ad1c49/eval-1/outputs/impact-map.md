# Repository Impact Map — TC-9001

## Feature

**TC-9001**: Add advisory severity aggregation endpoint

## Inherited Field Values

- **Priority**: Major — propagated to all created tasks (inherited from TC-9001)
- **Fix Versions**: RHTPA 1.5.0 — propagated to all created tasks (fixVersion scope defaults to "both")

## Repository: trustify-backend

### Changes Required

#### Model Layer
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — **CREATE**: AdvisorySeveritySummary struct with critical, high, medium, low, total fields
- `modules/fundamental/src/sbom/model/mod.rs` — **MODIFY**: add module declaration and re-export for advisory_summary

#### Service Layer
- `modules/fundamental/src/sbom/service/sbom.rs` — **MODIFY**: add get_advisory_summary method that aggregates severity counts from sbom_advisory join table

#### Endpoint Layer
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — **CREATE**: GET /api/v2/sbom/{id}/advisory-summary handler with 5-minute cache
- `modules/fundamental/src/sbom/endpoints/mod.rs` — **MODIFY**: register advisory-summary route

#### Cache Invalidation
- `modules/ingestor/src/graph/advisory/mod.rs` — **MODIFY**: invalidate advisory-summary cache for affected SBOMs when new advisories are linked

#### Testing
- `tests/api/sbom.rs` — **MODIFY**: add integration tests for the advisory-summary endpoint

## Task Summary

| # | Title | Type | Dependencies |
|---|---|---|---|
| 1 | Add advisory severity summary model and service layer | Implementation | None |
| 2 | Add advisory-summary endpoint with response caching | Implementation | Task 1 |
| 3 | Invalidate advisory-summary cache on advisory ingestion | Implementation | Task 2 |
| 4 | Document advisory-summary endpoint in REST API reference | Documentation | Tasks 1, 2, 3 |
| 5 | Smoke tests for advisory severity summary feature | Testing | Tasks 1, 2, 3 |
| 6 | Performance benchmarks for advisory severity summary | Testing | Tasks 1, 2, 3 |
