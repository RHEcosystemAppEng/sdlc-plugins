## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` module under `modules/fundamental/src/` with model structs and a service layer for aggregating vulnerability remediation data. The service computes remediation statistics by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved) from existing advisory and SBOM relationship data without introducing new database tables.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary, SeverityBreakdown, StatusBreakdown structs
- `modules/fundamental/src/remediation/model/by_product.rs` — ProductRemediation struct with per-product counts
- `modules/fundamental/src/remediation/service/mod.rs` — service module root
- `modules/fundamental/src/remediation/service/remediation.rs` — RemediationService with aggregation query methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new module
- `modules/fundamental/Cargo.toml` — add any additional dependencies if needed

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/`: each domain has `model/` + `service/` + `endpoints/` subdirectories. Reference `modules/fundamental/src/sbom/` as the canonical example of this structure.
- The `RemediationSummary` struct should mirror the pattern used by `SbomSummary` (in `modules/fundamental/src/sbom/model/summary.rs`) for consistent serialization and field naming.
- Use `common/src/db/query.rs` for filtering and pagination helpers in aggregation queries.
- Aggregation queries should join existing entities: `advisory` (for severity), `sbom_advisory` (for SBOM-advisory relationships), and derive remediation status from advisory state fields. Reference `entity/src/advisory.rs` and `entity/src/sbom_advisory.rs` for the entity schemas.
- Per the non-functional requirement, the summary endpoint response time must be p95 < 500ms. Consider query optimization with indexed joins. Do not create new database tables.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure for the new remediation module. Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all service methods. Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; use for aggregation queries
- `common/src/model/paginated.rs::PaginatedResults<T>` — standard response wrapper for list endpoints; reuse for by-product endpoint pagination
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — example service implementation pattern; follow the same struct and method conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field representation and serialization

## Acceptance Criteria
- [ ] `RemediationSummary` struct represents aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] `ProductRemediation` struct represents per-product remediation breakdown with total, open, in_progress, and resolved counts
- [ ] `RemediationService` computes aggregation from existing advisory and SBOM relationship data
- [ ] No new database tables or migrations are introduced
- [ ] Service methods return `Result<T, AppError>` following the established error handling pattern

## Test Requirements
- [ ] Unit tests for `RemediationService` aggregation logic with mock data
- [ ] Verify correct grouping by severity levels (Critical, High, Medium, Low)
- [ ] Verify correct grouping by status (Open, In Progress, Resolved)
- [ ] Verify per-product breakdown returns correct counts

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental` — all tests pass

## Dependencies
- None (this is the foundation task)
