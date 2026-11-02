## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add a RemediationService that computes aggregated remediation statistics from existing vulnerability and SBOM relationship data. The service provides two methods: `summary()` returns severity × status counts across all vulnerabilities, and `by_product()` returns per-product remediation breakdowns. No new database tables are needed — aggregations are computed from existing entity relationships.

## Files to Create
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with summary() and by_product() methods

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod service;` declaration

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService). Key patterns:

- Service methods take `&self` with a database connection pool reference
- Use SeaORM queries against existing entities: `entity/src/advisory.rs` (Advisory), `entity/src/sbom_advisory.rs` (SBOM-Advisory join), `entity/src/sbom.rs` (SBOM)
- `summary()`: join advisory → sbom_advisory → sbom, group by advisory severity and status, count distinct advisory IDs
- `by_product()`: join advisory → sbom_advisory → sbom → sbom_package → package, group by product (SBOM name), aggregate open/in-progress/resolved counts
- Return `Result<RemediationSummary, AppError>` and `Result<RemediationByProduct, AppError>` using `common/src/error.rs` (AppError)
- Use `.context()` wrapping for error handling per the established pattern in `modules/fundamental/src/sbom/service/sbom.rs`
- Use query helpers from `common/src/db/query.rs` for any filtering or pagination needs

Per docs/constraints.md §5 (Code Change Rules): no new database tables — use existing entity relationships only.

## Acceptance Criteria
- [ ] RemediationService::summary() returns aggregated counts grouped by severity and status
- [ ] RemediationService::by_product() returns per-product remediation breakdowns with total/open/resolved
- [ ] Both methods use existing entity relationships — no new database migrations
- [ ] Error handling uses AppError with .context() wrapping
- [ ] p95 response time consideration: queries use appropriate joins and aggregations, not N+1 patterns

## Test Requirements
- [ ] Unit test for summary() with known test data verifying correct grouping by severity × status
- [ ] Unit test for by_product() with known test data verifying correct per-product aggregation
- [ ] Test that empty dataset returns zero counts (not errors)
- [ ] Test that duplicate advisory-SBOM relationships are handled correctly (no double-counting)

## Dependencies
- Depends on: Task 1 — Remediation models
