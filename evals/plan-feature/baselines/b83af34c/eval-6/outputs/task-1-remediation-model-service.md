## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Priority
Major (inherited from Feature TC-9006)

## Fix Versions
RHTPA 1.5.0 (inherited from Feature TC-9006)

## Target Branch
main

## Description
Create the remediation domain module with model types and an aggregation service that computes remediation status summaries from existing vulnerability and SBOM relationship data. The service provides two aggregation methods: summary by severity and status, and breakdown by product. No new database tables are created; all computations use existing entity relationships (advisory, sbom_advisory, sbom, package).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — Remediation module root, re-exports model and service submodules
- `modules/fundamental/src/remediation/model/mod.rs` — Model submodule root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary, RemediationByProduct, and SeverityStatusCount structs
- `modules/fundamental/src/remediation/service/mod.rs` — Service submodule root
- `modules/fundamental/src/remediation/service/remediation.rs` — RemediationService with aggregation query methods

## Files to Modify
- `modules/fundamental/src/lib.rs` — Add `pub mod remediation;` to register the new domain module

## Implementation Notes
Follow the existing domain module pattern established by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`. Each domain module uses the `model/ + service/ + endpoints/` structure.

The RemediationService should query existing entities: `entity/src/advisory.rs` (severity field on AdvisorySummary), `entity/src/sbom_advisory.rs` (SBOM-Advisory join for correlation), and `entity/src/sbom.rs` (product association). Use `common/src/db/query.rs` query builder helpers for filtering and pagination. All service methods return `Result<T, AppError>` using the error type from `common/src/error.rs` with `.context()` wrapping.

The summary aggregation groups vulnerabilities by severity (Critical/High/Medium/Low) crossed with status (Open/In Progress/Resolved). The by-product aggregation returns per-product totals including open and resolved counts.

Per CONVENTIONS.md §Module pattern: structure remediation module with model/, service/, and endpoints/ subdirectories. Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] RemediationSummary struct contains severity-by-status aggregation counts
- [ ] RemediationByProduct struct contains per-product total, open, and resolved counts
- [ ] RemediationService queries existing advisory and SBOM relationship entities without new database tables
- [ ] Service methods return Result<T, AppError> following the project error handling pattern
- [ ] Module is registered in modules/fundamental/src/lib.rs

## Test Requirements
- [ ] Unit tests for RemediationService aggregation logic with mock data
- [ ] Verify severity grouping produces correct counts for Critical/High/Medium/Low
- [ ] Verify by-product breakdown correctly totals open and resolved per product

## Dependencies
- None
