## Repository
trustify-backend

## Target Branch
main

## Description
Implement the remediation service that computes aggregated remediation statistics from existing vulnerability and SBOM relationship data. The service queries existing entity tables (advisory, sbom_advisory, sbom, package) without creating new database tables, and returns RemediationSummary and ProductRemediation results.

## Files to Create
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with methods: `get_summary()` returning RemediationSummary, and `get_by_product()` returning PaginatedResults<ProductRemediation>

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — add `pub mod service;` to expose the service submodule

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) and `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService). The service takes a database connection reference and uses SeaORM queries. Use the shared query helpers from `common/src/db/query.rs` for filtering and pagination support. Aggregate counts from existing entity tables: `entity/src/advisory.rs` (severity field), `entity/src/sbom_advisory.rs` (SBOM-advisory relationship), and `entity/src/sbom.rs` (product association). All handlers should return `Result<T, AppError>` using `.context()` wrapping from `common/src/error.rs`.

Per CONVENTIONS.md §Error handling: return Result<T, AppError> with .context() wrapping.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers
- `common/src/error.rs::AppError` — error type with IntoResponse implementation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for service structure and query patterns
- `entity/src/advisory.rs` — advisory entity with severity field for aggregation
- `entity/src/sbom_advisory.rs` — join table linking SBOMs to advisories

## Acceptance Criteria
- [ ] RemediationService::get_summary() aggregates counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] RemediationService::get_by_product() returns per-product remediation breakdown with total, open, resolved counts
- [ ] No new database tables are created — aggregations computed from existing entity data
- [ ] Summary endpoint target: p95 < 500ms for reasonable data volumes
- [ ] Service uses shared query helpers for filtering and pagination

## Test Requirements
- [ ] Unit test for summary aggregation logic with mock data
- [ ] Unit test for by-product aggregation with multiple products

## Dependencies
- Depends on: Task 1 — Create remediation module with model types
