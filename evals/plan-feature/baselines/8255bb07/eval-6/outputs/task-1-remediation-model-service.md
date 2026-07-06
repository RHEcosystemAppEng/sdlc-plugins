## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Description
Add the remediation module with model structs and an aggregation service layer to support the vulnerability remediation tracking dashboard. This module provides the data layer for two new API endpoints: a summary endpoint that aggregates remediation counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved), and a per-product breakdown endpoint that returns total, open, and resolved counts for each product. All aggregations are computed from existing vulnerability and SBOM relationship data without introducing new database tables.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — Remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` — Model submodule root, re-exports summary and by-product structs
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with severity-by-status aggregation fields
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product total, open, and resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with aggregation query methods (get_summary, get_by_product)

## Files to Modify
- `modules/fundamental/src/lib.rs` — Register the remediation submodule
- `modules/fundamental/Cargo.toml` — Add any required dependencies for aggregation queries

## Implementation Notes
Follow the established domain module pattern used by existing modules such as `sbom`, `advisory`, and `package` under `modules/fundamental/src/`. Each module follows the `model/ + service/ + endpoints/` directory structure.

Per CONVENTIONS.md §Module pattern: structure the remediation module as `model/ + service/ + endpoints/` matching sibling modules (sbom, advisory, package).
Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's Rust module structure scope.

Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response types: list/aggregation responses should use or mirror the `PaginatedResults<T>` pattern from `common/src/model/paginated.rs` for consistency.
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` for the aggregation queries.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.

The aggregation queries should join across existing entity tables (`advisory`, `sbom_advisory`, `package`, `sbom_package`) to compute remediation status counts. Use SeaORM query builder for the aggregation SQL. Reference `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for the severity field structure.

Non-functional: the summary aggregation query must target p95 < 500ms response time and handle up to 10,000 tracked vulnerabilities. Consider query optimization (appropriate GROUP BY, avoiding N+1 patterns).

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — Shared query builder helpers for filtering, pagination, and sorting; reuse for aggregation query construction
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper pattern to reference when designing aggregation response structs
- `common/src/error.rs::AppError` — Error type for all service method return types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field structure and serialization patterns
- `entity/src/advisory.rs` — Advisory entity definition; source table for vulnerability status data
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table; needed for correlating vulnerabilities to SBOMs/products

## Acceptance Criteria
- [ ] RemediationSummary struct represents a 4x3 matrix of severity (Critical/High/Medium/Low) by status (Open/In Progress/Resolved) with integer counts
- [ ] ProductRemediation struct includes product identifier, total count, open count, and resolved count fields
- [ ] RemediationService.get_summary() returns aggregated counts from existing advisory and SBOM data
- [ ] RemediationService.get_by_product() returns per-product breakdown with correct counts
- [ ] All service methods return Result<T, AppError> following the error handling convention
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test for RemediationSummary serialization and field structure
- [ ] Unit test for ProductRemediation serialization and field structure
- [ ] Service method tests with mock data verifying correct aggregation counts by severity and status
- [ ] Service method tests verifying per-product breakdown returns correct total, open, and resolved counts
- [ ] Test that aggregation handles zero-count categories correctly (e.g., no Critical vulnerabilities)

## Dependencies
None
