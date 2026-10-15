## Repository
trustify-backend

## Target Branch
main

## Description
Add the remediation domain module with model types and an aggregation service. This module provides the data layer for the vulnerability remediation tracking dashboard (TC-9006). The service computes aggregated remediation counts by severity and status, and per-product remediation breakdowns, using existing vulnerability and SBOM relationship data without new database tables.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — Remediation module root, re-exports model and service
- `modules/fundamental/src/remediation/model/mod.rs` — Model module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct (severity x status matrix), SeverityStatusCount struct, ProductRemediation struct (product name, total, open, resolved counts)
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with aggregate_summary() and by_product() methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — Register the new remediation module
- `modules/fundamental/Cargo.toml` — Add any needed dependencies for the remediation module (if not already covered by existing deps)

## Implementation Notes
- Per CONVENTIONS.md §Module pattern: follow the established `model/ + service/` structure used by existing domain modules (sbom, advisory, package).
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for error messages.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Query helpers: use the shared query builder helpers from `common/src/db/query.rs` for filtering, pagination, and sorting in the aggregation queries.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` service scope.
- The service must aggregate from existing entity tables (`advisory`, `sbom_advisory`, `package`, `sbom_package`) without creating new database tables — this is a non-functional requirement.
- RemediationSummary should group counts by severity (Critical, High, Medium, Low) crossed with status (Open, In Progress, Resolved).
- ProductRemediation should include: product name, total vulnerability count, open count, in-progress count, resolved count.
- Reference `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) for the pattern of querying across advisory and SBOM relationships.
- Reference `common/src/model/paginated.rs` (PaginatedResults<T>) for response wrapper usage in the by-product method.

## Reuse Candidates
- `common/src/db/query.rs::query helpers` — Shared filtering, pagination, and sorting utilities; use for by-product pagination
- `common/src/model/paginated.rs::PaginatedResults<T>` — Standard paginated response wrapper; use for by-product endpoint response
- `common/src/error.rs::AppError` — Standard error type; use for all service error returns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Pattern reference for querying advisory-related data with SeaORM
- `entity/src/advisory.rs` — Advisory entity definition; use for severity field access
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for correlating vulnerabilities to SBOMs

## Acceptance Criteria
- [ ] RemediationSummary struct contains a severity x status count matrix (4 severities x 3 statuses)
- [ ] ProductRemediation struct contains product name, total, open, in-progress, and resolved counts
- [ ] RemediationService::aggregate_summary() returns a RemediationSummary computed from existing data
- [ ] RemediationService::by_product() returns a paginated list of ProductRemediation records
- [ ] No new database tables or migrations are created
- [ ] Module is registered in modules/fundamental/src/lib.rs

## Test Requirements
- [ ] Unit test for RemediationSummary construction with known input data
- [ ] Unit test for ProductRemediation aggregation logic
- [ ] Verify aggregate_summary returns correct counts when given advisory data with mixed severities and statuses
- [ ] Verify by_product returns correct per-product breakdowns

## Verification Commands
- `cargo build -p trustify-fundamental` — Builds successfully without errors
- `cargo test -p trustify-fundamental -- remediation` — All remediation unit tests pass

## Dependencies
- None (first task in the backend Epic)
