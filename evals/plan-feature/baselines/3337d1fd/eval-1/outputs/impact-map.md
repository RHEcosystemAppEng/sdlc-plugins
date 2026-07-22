# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

## Feature Summary
Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets and alerting integrations to retrieve severity breakdowns in a single call.

## Inherited Field Values
All tasks inherit the following fields from feature TC-9001:
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Tasks Overview

| Task | Title | Repository | Type | Dependencies |
|------|-------|------------|------|-------------|
| Task 1 | Add advisory severity summary model | trustify-backend | Implementation | None |
| Task 2 | Implement advisory severity aggregation service | trustify-backend | Implementation | Task 1 |
| Task 3 | Add advisory-summary endpoint with caching | trustify-backend | Implementation | Task 2 |
| Task 4 | Add cache invalidation on advisory ingestion | trustify-backend | Implementation | Task 3 |
| Task 5 | Add integration tests for advisory-summary endpoint | trustify-backend | Implementation | Task 3 |
| Task 6 | Update REST API reference documentation | trustify-backend | Documentation | Task 3 |
| Task 7 | Smoke tests | trustify-backend | Testing | Tasks 1-5 |
| Task 8 | Performance benchmarks | trustify-backend | Testing | Tasks 1-5 |

## Dependency Graph

```
Task 1 (model)
  └── Task 2 (service)
        └── Task 3 (endpoint)
              ├── Task 4 (cache invalidation)
              ├── Task 5 (integration tests)
              └── Task 6 (documentation)

Tasks 1-5 (all implementation)
  ├── Task 7 (smoke tests)
  └── Task 8 (performance benchmarks)
```

## Repository Impact: trustify-backend

### New Files
| File | Task | Purpose |
|------|------|---------|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | Task 1 | AdvisorySeveritySummary response struct |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Task 3 | Endpoint handler for advisory-summary |
| `tests/api/sbom_advisory_summary.rs` | Task 5 | Integration tests |

### Modified Files
| File | Task | Change |
|------|------|--------|
| `modules/fundamental/src/sbom/model/mod.rs` | Task 1 | Add module declaration and re-export |
| `modules/fundamental/src/sbom/service/sbom.rs` | Task 2 | Add advisory_summary method to SbomService |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 3 | Register advisory-summary route |
| `modules/ingestor/src/graph/advisory/mod.rs` | Task 4 | Add cache invalidation after advisory correlation |

### API Changes
| Endpoint | Method | Task | Description |
|----------|--------|------|-------------|
| `/api/v2/sbom/{id}/advisory-summary` | GET | Task 3 | NEW: Returns aggregated severity counts (critical, high, medium, low, total) |

## Modules Affected
- `modules/fundamental` — New model, service method, and endpoint
- `modules/ingestor` — Cache invalidation on advisory ingestion
- `entity` — Referenced but not modified (uses existing sbom_advisory join table)
- `common` — Referenced but not modified (uses existing AppError and query helpers)
- `tests` — New integration test file

## Risk Assessment
- **Low risk**: No database schema changes; uses existing entity relationships
- **Medium risk**: Cache invalidation in ingestion pipeline must not degrade ingestion throughput
- **Mitigation**: Integration tests (Task 5) and performance benchmarks (Task 8) validate correctness and performance