## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add the remediation domain module with data models and an aggregation service that computes remediation status from existing vulnerability and SBOM relationship data. This provides the data layer for the remediation tracking dashboard endpoints. No new database tables are introduced -- all aggregations are computed from existing entity tables (advisory, sbom_advisory, sbom, package).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary struct with severity/status breakdown and RemediationSummaryEntry struct
- `modules/fundamental/src/remediation/model/by_product.rs` -- ProductRemediation struct with per-product total/open/resolved counts
- `modules/fundamental/src/remediation/service/mod.rs` -- RemediationService with aggregation query methods: get_summary() and get_by_product()

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` to register the new module
- `modules/fundamental/Cargo.toml` -- add any needed dependencies (if any beyond existing SeaORM)

## Implementation Notes
- Follow the existing module pattern: each domain module has `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/` for the canonical example.
- Per backend conventions: use SeaORM for database queries. Build aggregation queries using the existing query helpers in `common/src/db/query.rs` for filtering, pagination, and sorting.
- Per backend conventions: all service methods should return `Result<T, AppError>` with `.context()` wrapping for error handling. See `common/src/error.rs` for the AppError enum.
- RemediationSummary should group counts by severity (Critical, High, Medium, Low) crossed with status (Open, In Progress, Resolved). Use the existing `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` as reference for severity field handling.
- ProductRemediation should include product name, total vulnerability count, open count, and resolved count. Use the existing SBOM-Advisory join table (`entity/src/sbom_advisory.rs`) and SBOM-Package join table (`entity/src/sbom_package.rs`) for the aggregation queries.
- Per NFR: summary queries should target p95 < 500ms. Use appropriate database indexes on existing columns and avoid N+1 queries.
- Per NFR: no new database tables. All aggregations are computed from existing entity tables: `advisory` (severity), `sbom_advisory` (status/correlation), `sbom` (product association), `package`.
- Constraints: per docs/constraints.md section 2, commit messages must follow Conventional Commits format and reference TC-9006. Per section 5, changes must be scoped to the files listed.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting. Reuse for building remediation aggregation queries.
- `common/src/model/paginated.rs` -- PaginatedResults<T> response wrapper. Use for paginated product remediation results.
- `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct with severity field. Reference for severity enum handling.
- `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService pattern for fetch and list operations. Follow the same service structure.
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity. Core table for aggregation queries.

## Acceptance Criteria
- [ ] RemediationSummary struct contains severity/status breakdown with counts
- [ ] ProductRemediation struct contains product name, total, open, and resolved counts
- [ ] RemediationService.get_summary() returns aggregated counts grouped by severity x status from existing data
- [ ] RemediationService.get_by_product() returns per-product remediation breakdown with total, open, resolved counts
- [ ] No new database migration files are created -- all aggregations use existing tables
- [ ] Module follows the model/ + service/ structure pattern established by other fundamental modules

## Test Requirements
- [ ] Unit test for RemediationService.get_summary() verifying correct grouping by severity and status
- [ ] Unit test for RemediationService.get_by_product() verifying correct per-product breakdown
- [ ] Test that empty data sets return zero counts without errors

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental -- remediation` -- all remediation tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
