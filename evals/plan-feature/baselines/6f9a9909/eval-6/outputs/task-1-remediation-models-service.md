## Repository
trustify-backend

## Target Branch
main

## Description
Add a new remediation module under `modules/fundamental/` with data models and an aggregation service for vulnerability remediation tracking. The service computes remediation status by querying existing vulnerability and SBOM relationship data -- no new database tables are created. This module provides the domain logic consumed by the remediation REST endpoints (Tasks 2 and 3).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` -- model submodule root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary struct with counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `modules/fundamental/src/remediation/model/by_product.rs` -- ProductRemediation struct with per-product total, open, and resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` -- service submodule root
- `modules/fundamental/src/remediation/service/remediation.rs` -- RemediationService with methods to compute summary and by-product aggregations

## Files to Modify
- `modules/fundamental/src/lib.rs` -- register the remediation submodule
- `modules/fundamental/Cargo.toml` -- add any needed dependencies for aggregation queries

## Implementation Notes
Per CONVENTIONS.md "Module pattern": follow the `model/ + service/ + endpoints/` structure used by existing domain modules. See `modules/fundamental/src/sbom/` for the established pattern.
Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md "Error handling": all service methods must return `Result<T, AppError>` with `.context()` wrapping for error propagation. See `common/src/error.rs` for the AppError enum.
Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md "Query helpers": use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` for database queries.
Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` file scope.

The service must compute aggregations from existing entity tables (`advisory`, `sbom_advisory`, `package`, `sbom_package`) without creating new database tables (per non-functional requirements). Use SeaORM query builder for GROUP BY aggregations.

Relevant constraints from `docs/constraints.md`:
- Per SS5.2: Code must not be modified without first inspecting it.
- Per SS5.4: Code must not duplicate existing functionality -- reuse existing query helpers and entity definitions.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults` -- paginated response wrapper for list results
- `common/src/error.rs::AppError` -- error enum implementing IntoResponse for consistent error handling
- `entity/src/advisory.rs` -- Advisory entity with severity field, used for severity-based aggregation
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table for correlating vulnerabilities with SBOMs
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference implementation for service layer patterns

## Acceptance Criteria
- [ ] RemediationSummary struct models a 4x3 matrix of counts: severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- [ ] ProductRemediation struct models per-product breakdown with product identifier, total count, open count, and resolved count
- [ ] RemediationService::get_summary() returns aggregated counts from existing entity data
- [ ] RemediationService::get_by_product() returns per-product breakdown from existing entity data
- [ ] No new database migration files are created
- [ ] Module compiles and integrates into the fundamental crate without errors

## Test Requirements
- [ ] Unit tests for RemediationService::get_summary() verifying correct grouping by severity and status with mock data
- [ ] Unit tests for RemediationService::get_by_product() verifying correct per-product aggregation with mock data
- [ ] Test edge case: no vulnerabilities returns zero counts for all severity/status combinations
- [ ] Test edge case: single product with mixed statuses returns correct breakdown

## Dependencies
- None (this is the foundational task)

## Parent Epic
TC-9007
