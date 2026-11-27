**Summary:** Add remediation domain module with summary and per-product aggregation service
**Parent Epic:** TC-9101 (TC-9006: trustify-backend)
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Major | **fixVersions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` domain module in `modules/fundamental` that computes portfolio-wide vulnerability remediation aggregations from existing data (no new database tables). The service provides two aggregations required by TC-9006:

1. **Summary** — counts of correlated vulnerabilities grouped by severity (Critical/High/Medium/Low) x remediation status (Open/In Progress/Resolved), plus overall totals per status.
2. **By product** — per-product breakdown with `total`, `open`, `in_progress`, and `resolved` counts, paginated to support large portfolios (>50 products).

This task delivers the model and service layers only; HTTP endpoints are added in Task 2.

## Files to Modify
- `modules/fundamental/src/lib.rs` — declare the new `remediation` module

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root exposing `model` and `service`
- `modules/fundamental/src/remediation/model/mod.rs` — model module root, `RemediationStatus` and `Severity` enums (serde `snake_case`)
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` and `SeverityStatusCounts` structs
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct (`product_name`, `total`, `open`, `in_progress`, `resolved`)
- `modules/fundamental/src/remediation/service/mod.rs` — service module root
- `modules/fundamental/src/remediation/service/remediation.rs` — `RemediationService` with `summary()` and `by_product(paginated)` methods

## Implementation Notes
- Follow the existing domain module layout used by `modules/fundamental/src/advisory/` and `modules/fundamental/src/sbom/` (`model/ + service/ + endpoints/`). Model `RemediationService` on `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` (constructor taking the DB connection, async methods returning `Result<T, AppError>`).
- Compute aggregations with SeaORM `GROUP BY` queries joining `entity/src/sbom_advisory.rs` (SBOM-Advisory correlation), `entity/src/advisory.rs` (severity — same field surfaced by `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`), and `entity/src/sbom.rs` (product grouping). Push grouping/counting into SQL — do not load all rows into memory (NFR: p95 < 500ms, up to 10,000 tracked vulnerabilities).
- Remediation status source: verify at implementation time which column on `sbom_advisory` (or related entity) represents remediation status (Open/In Progress/Resolved) and which column on `sbom` identifies the product. If no status column exists, stop and raise with the Feature owner — the NFR forbids new tables.
- Paginate `by_product` using the shared helpers in `common/src/db/query.rs` and return `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs`.
- Serialize enum values as `snake_case` (`critical`, `high`, `medium`, `low`; `open`, `in_progress`, `resolved`) — the frontend maps these to display labels.
- Per CONVENTIONS.md §Module pattern: place the new code under `modules/fundamental/src/remediation/` with `model/` and `service/` subdirectories, mirroring `modules/fundamental/src/advisory/`.
  Applies: task modifies `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust domain module (`modules/*/src/<domain>/`) scope.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` (from `common/src/error.rs`) and wrap DB errors with `.context()`; see `modules/fundamental/src/advisory/service/advisory.rs`.
  Applies: task modifies `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust handler/service `.rs` scope.
- Per CONVENTIONS.md §Response types / §Query helpers: return `PaginatedResults<T>` for the per-product list and use `common/src/db/query.rs` for pagination and sorting.
  Applies: task modifies `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust list-query `.rs` scope.
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, `Implements TC-<task>` footer, `Assisted-by:` trailer); §3 PR rules (`gh pr create --base main`, post PR link to Jira); §5 code change rules (scope to listed files, inspect before modifying, reuse existing helpers, no duplication).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, sorting helpers; use for `by_product` pagination
- `common/src/model/paginated.rs::PaginatedResults` — standard list response wrapper
- `common/src/error.rs::AppError` — error type for service results
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference service structure and advisory querying/severity handling
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field representation; reuse its severity type rather than defining a parallel one if it is an enum

## Acceptance Criteria
- [ ] `RemediationService::summary()` returns counts for every severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) combination, including zero-count combinations
- [ ] `RemediationService::summary()` returns overall totals for Open, In Progress, and Resolved that equal the sum of the per-severity counts
- [ ] `RemediationService::by_product()` returns one entry per product with `total`, `open`, `in_progress`, `resolved`, where `total = open + in_progress + resolved`
- [ ] `by_product()` is paginated and returns `PaginatedResults<ProductRemediation>`
- [ ] No database migration or new entity is introduced
- [ ] Aggregation is performed in SQL (`GROUP BY`), not in-memory iteration over all rows

## Test Requirements
- [ ] Service-level test: seeded SBOMs/advisories with mixed severities and statuses produce the expected summary counts
- [ ] Service-level test: empty database returns all-zero summary (not an error)
- [ ] Service-level test: `by_product` returns correct per-product counts across at least two products, and respects `offset`/`limit`

## Dependencies
- None
