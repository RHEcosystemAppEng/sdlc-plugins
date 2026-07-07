# Plan Summary: TC-9001 "Add advisory severity aggregation endpoint"

## Repository
trustify-backend

## Tasks Created

### Implementation Tasks
| # | Task | Description |
|---|---|---|
| 1 | Advisory severity summary model | Create `AdvisorySeveritySummary` struct with critical, high, medium, low, and total fields |
| 2 | Advisory summary service | Add `get_severity_summary_for_sbom` method to `AdvisoryService` with deduplication and severity aggregation |
| 3 | Advisory summary endpoint | Register GET /api/v2/sbom/{id}/advisory-summary with 5-minute caching and 404 handling |
| 4 | Cache invalidation | Hook into advisory ingestion pipeline to invalidate cached summaries on new SBOM-advisory links |
| 5 | Integration tests | Comprehensive integration tests for the advisory-summary endpoint against real PostgreSQL |
| 6 | Threshold query parameter | Optional `?threshold=critical` filter for severity level cutoff (non-MVP) |

### Documentation Task
| # | Task | Description |
|---|---|---|
| 7 | Documentation | Update REST API reference with the new advisory-summary endpoint, parameters, and response schema |

Documentation task generated due to Documentation Considerations section in the feature description (Doc Impact: Updates -- add endpoint to REST API reference).

### Testing Tasks
| # | Task | Description |
|---|---|---|
| 8 | Smoke Tests | Validate new endpoint returns successful responses, backward compat maintained, E2E workflow completes |
| 9 | Performance Benchmarks | Validate p95 < 200ms for 500 advisories, no memory leaks, no DB query regression |

2 testing tasks generated from testing readiness template (`docs/testing-readiness.md`): Smoke Tests, Performance Benchmarks.

## Inherited Fields

- **Priority:** Major -- propagated to all tasks
- **Fix Versions:** RHTPA 1.5.0 -- propagated to all tasks (fixVersion scope: both)

## Dependency Chain

```
Task 1 (model)
  -> Task 2 (service)
       -> Task 3 (endpoint)
             -> Task 4 (cache invalidation)
                   -> Task 5 (integration tests)
                         -> Task 6 (threshold query param)

Tasks 7, 8, 9 depend on all implementation tasks (1-6)
```

## Workflow Mode
Direct-to-main -- all tasks target `main` branch.
