# Implementation Plan — TC-9201

## Pre-implementation Analysis

Before making any changes, inspect the following files to understand existing patterns, conventions, and integration points:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Study the existing GET endpoint handler pattern: how `Path<Id>` is extracted, how the `AdvisoryService` is obtained from Axum state, how the service method is called with a `Transactional` context, how responses are returned via `Json`, and how errors are propagated using `AppError` and `.context()`.
2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Understand the `AdvisoryService` struct, its existing methods (`fetch`, `list`, `search`), how SeaORM queries are constructed, how entity joins are performed, and what imports/traits are used. This informs the signature and implementation of the new `severity_summary` method.
3. **`modules/fundamental/src/advisory/model/summary.rs`** — Examine the `AdvisorySummary` struct to understand the `severity` field type, derive macros used (`Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema`), and field naming conventions. This guides the design of the new `SeveritySummary` struct.
4. **`common/src/error.rs`** — Review the `AppError` enum and its variants (especially `NotFound`), the `IntoResponse` implementation, and the `.context()` extension pattern for proper error handling in the new code.
5. **`entity/src/sbom_advisory.rs`** — Understand the `sbom_advisory` join table entity, its columns, and relations to build the correct SeaORM query for aggregating advisory severity counts by SBOM ID.
6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — See how existing routes are registered to follow the same pattern when adding the new route.
7. **`tests/api/advisory.rs`** — Review existing integration test structure, test harness usage, and assertion patterns for the test file.

## Branch

```bash
git checkout -b TC-9201
```

## Files to Create

| # | Path | Purpose |
|---|------|---------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Define the `SeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total` |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` — extracts SBOM ID, calls service, returns JSON |
| 3 | `tests/api/advisory_summary.rs` | Integration tests verifying correct severity counts, 404 for missing SBOM, zero counts for no advisories |

## Files to Modify

| # | Path | Change |
|---|------|--------|
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table and aggregates severity counts |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` GET route pointing to the new handler |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to expose the new model module |

## Implementation Order

1. **Model first** — Create `SeveritySummary` struct (file 1) and register the module (file 6)
2. **Service method** — Add `severity_summary` to `AdvisoryService` (file 4)
3. **Endpoint handler** — Create the GET handler (file 2) and register the route (file 5)
4. **Tests** — Create integration tests (file 3)

## Commit

```bash
git add \
  modules/fundamental/src/advisory/model/severity_summary.rs \
  modules/fundamental/src/advisory/endpoints/severity_summary.rs \
  tests/api/advisory_summary.rs \
  modules/fundamental/src/advisory/service/advisory.rs \
  modules/fundamental/src/advisory/endpoints/mod.rs \
  modules/fundamental/src/advisory/model/mod.rs

git commit -m "$(cat <<'EOF'
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService::severity_summary method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
per-severity counts (critical, high, medium, low, total) for a given
SBOM. Includes integration tests covering valid SBOM, missing SBOM
(404), and empty advisory scenarios.

Implements TC-9201
EOF
)" --trailer='Assisted-by: Claude Code'
```
