# Task 3 — Add remediation aggregation service

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Implement the remediation aggregation service that computes remediation status summaries from existing vulnerability and SBOM relationship data. The service provides two aggregation methods: one for overall severity-by-status breakdown and one for per-product remediation counts. All aggregation is computed on-the-fly from existing data without introducing new database tables, using SeaORM queries against the advisory, sbom_advisory, sbom, and package entities.

## Files to Create
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with methods `get_summary(&self, db: &DatabaseConnection) -> Result<RemediationSummary, AppError>` and `get_by_product(&self, db: &DatabaseConnection) -> Result<Vec<ProductRemediation>, AppError>`

## Files to Modify
- `modules/fundamental/src/remediation/mod.rs` — Add `pub mod service;` to expose the service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) and `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) for method signatures and error handling.
- Use SeaORM queries against existing entities: `entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`, `entity/src/sbom.rs`, `entity/src/package.rs` to compute aggregations.
- For `get_summary`: query advisories grouped by severity and status, counting occurrences in each severity x status bucket (Critical/High/Medium/Low x Open/In Progress/Resolved). Use `group_by` and `count` in SeaORM.
- For `get_by_product`: join sbom with sbom_advisory and advisory to compute per-product (SBOM name) counts of open, in_progress, and resolved vulnerabilities.
- Use the shared query helpers from `common/src/db/query.rs` for any filtering or pagination needs.
- Wrap all database errors with `.context()` per the error handling convention.
- Performance requirement: p95 response time < 500ms for the summary endpoint. Consider using efficient aggregate queries rather than loading all records into memory.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Query helpers): use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Example service pattern with database queries and error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Example of querying advisory entities with filtering
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, sorting
- `entity/src/sbom_advisory.rs` — Join table entity needed for SBOM-to-advisory aggregation queries

## Acceptance Criteria
- [ ] `RemediationService::get_summary` returns aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] `RemediationService::get_by_product` returns per-product remediation breakdown with total, open, in_progress, resolved counts
- [ ] Aggregation queries do not introduce new database tables — all data is derived from existing entities
- [ ] All database errors are wrapped with `.context()` and return `AppError`

## Test Requirements
- [ ] Unit test: `get_summary` returns correct aggregation when test data has mixed severity/status combinations
- [ ] Unit test: `get_by_product` returns correct per-product counts with multiple products
- [ ] Unit test: `get_summary` returns zero counts when no advisory data exists
- [ ] Unit test: verify p95 performance target is achievable with 10,000 vulnerability records (benchmark test)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation aggregation model structs

## Parent Epic
TC-9006: trustify-backend
