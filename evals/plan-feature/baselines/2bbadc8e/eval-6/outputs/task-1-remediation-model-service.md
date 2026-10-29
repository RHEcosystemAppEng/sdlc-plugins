## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model and service layer for vulnerability remediation aggregation. This task creates the RemediationService that computes aggregated remediation statistics from existing vulnerability, advisory, and SBOM relationship data without introducing new database tables. The service provides two aggregation functions: one that groups remediation counts by severity and status, and one that groups by product.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with fields for severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) counts
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with product name, total, open, and resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with aggregation query methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new remediation module
- `modules/fundamental/Cargo.toml` — add any needed dependencies

## Implementation Notes
Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure used by existing domain modules (sbom, advisory, package).
Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` module structure scope.

Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for error context propagation.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response Types: aggregation query results that return lists should use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the by-product endpoint.
Applies: task creates `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query Helpers: use the shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` for building aggregation queries.
Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.

The aggregation queries must operate on existing entity tables (advisory, sbom_advisory, package, sbom_package) without creating new database tables, per the non-functional requirement.

The summary aggregation must group by severity (Critical, High, Medium, Low) crossed with status (Open, In Progress, Resolved), producing a matrix of counts.

The by-product aggregation must return per-product entries with total, open, and resolved counts.

Summary endpoint must achieve p95 < 500ms response time. Consider using efficient SQL aggregation (GROUP BY with COUNT) rather than loading all records into memory.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared query builder helpers for filtering, pagination, and sorting; reuse for building aggregation queries
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for paginated list results; use for the by-product breakdown which may need pagination for large portfolios
- `common/src/error.rs::AppError` — error enum that implements IntoResponse; use for service error handling
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for struct design pattern including severity field
- `entity/src/advisory.rs` — Advisory entity with severity data needed for aggregation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for correlating vulnerabilities to SBOMs

## Acceptance Criteria
- [ ] RemediationSummary struct contains fields for severity x status count matrix (4 severity levels x 3 statuses)
- [ ] ProductRemediation struct contains product name, total count, open count, and resolved count
- [ ] RemediationService aggregates data from existing advisory, sbom_advisory, and related entity tables
- [ ] No new database tables or migrations are introduced
- [ ] Service methods return Result<T, AppError> with proper error context
- [ ] Aggregation queries handle the case where no vulnerability data exists (returns zero counts, not errors)

## Test Requirements
- [ ] Unit test for RemediationSummary serialization
- [ ] Unit test for ProductRemediation serialization
- [ ] Service test verifying correct aggregation counts with known test data
- [ ] Service test verifying empty result set returns zero counts rather than errors
- [ ] Service test verifying aggregation handles up to 10,000 tracked vulnerabilities
