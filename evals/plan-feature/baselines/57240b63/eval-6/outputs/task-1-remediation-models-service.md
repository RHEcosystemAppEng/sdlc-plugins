## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the remediation domain module with data models and an aggregation service that computes remediation status counts from existing vulnerability and SBOM relationship data. This is the data layer for the remediation tracking dashboard -- it provides the aggregation logic that the API endpoints (Task 2) will expose. No new database tables are introduced; all counts are computed by querying and joining existing entity tables (advisory, sbom_advisory, sbom, package).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` -- model submodule root, re-exports types
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary, SeverityStatusCount, RemediationTotals structs with Serialize derives
- `modules/fundamental/src/remediation/model/product.rs` -- ProductRemediation struct with Serialize derive for per-product breakdown
- `modules/fundamental/src/remediation/service/mod.rs` -- service submodule root
- `modules/fundamental/src/remediation/service/remediation.rs` -- RemediationService with methods: get_summary() and get_by_product()

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` to register the new submodule
- `modules/fundamental/Cargo.toml` -- add any needed dependencies (if not already present)

## Implementation Notes
- Follow the established module pattern: each domain module under `modules/fundamental/src/` uses `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/` for the reference implementation.
  - Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's module structure scope.
- All service methods must return `Result<T, AppError>` using `.context()` wrapping for error propagation, consistent with `modules/fundamental/src/sbom/service/sbom.rs`.
  - Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's error handling scope.
- Use SeaORM query builder to join existing entity tables. Key entities to query:
  - `entity/src/advisory.rs` -- Advisory entity (has severity field per AdvisorySummary in `modules/fundamental/src/advisory/model/summary.rs`)
  - `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table for correlating vulnerabilities to SBOMs
  - `entity/src/sbom.rs` -- SBOM entity for product association
- Use shared query helpers from `common/src/db/query.rs` for filtering and pagination support in the by-product query.
- For `get_by_product()`, return `PaginatedResults<ProductRemediation>` using the wrapper from `common/src/model/paginated.rs` to support pagination for large portfolios (>50 products per the feature requirements).
- RemediationSummary struct should group counts by severity (Critical/High/Medium/Low) cross status (Open/In Progress/Resolved) with totals.
- Performance target: p95 < 500ms for summary endpoint. Consider using aggregate SQL queries (GROUP BY) rather than fetching all records and counting in Rust.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared filtering, pagination, and sorting helpers; reuse for by-product query pagination
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard paginated response wrapper; use for ProductRemediation list
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- reference for severity field structure
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference implementation for service pattern with SeaORM queries

## Acceptance Criteria
- [ ] RemediationSummary struct contains by_severity (Vec<SeverityStatusCount>) and totals (RemediationTotals) fields
- [ ] SeverityStatusCount contains severity (String), open (i64), in_progress (i64), resolved (i64) fields
- [ ] ProductRemediation struct contains product_id, product_name, total, open, in_progress, resolved fields
- [ ] RemediationService::get_summary() returns aggregated counts from existing data
- [ ] RemediationService::get_by_product() returns PaginatedResults<ProductRemediation>
- [ ] No new database tables or migrations are introduced
- [ ] Module compiles and is exported from modules/fundamental/src/lib.rs

## Test Requirements
- [ ] Unit test for RemediationService::get_summary() verifying correct severity x status grouping
- [ ] Unit test for RemediationService::get_by_product() verifying per-product aggregation
- [ ] Verify that PaginatedResults wrapper is correctly applied to by-product results

## Dependencies
- None (first task in the backend epic)

---
Description digest: sha256-md:21c1635947f5e4fe0d68fd4138757e81c4faca2b951a1c8c194a238709a7b47c
