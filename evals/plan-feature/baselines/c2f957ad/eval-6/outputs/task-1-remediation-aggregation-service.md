## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` domain module in `modules/fundamental` with the model types and service layer that compute portfolio-wide vulnerability remediation aggregations for TC-9006 (vulnerability remediation tracking dashboard). The service computes (a) counts grouped by severity (Critical/High/Medium/Low) x remediation status (Open/In Progress/Resolved) and (b) a per-product breakdown (total, open, in progress, resolved). Per the Feature's non-functional requirements, no new database tables may be added — all aggregations are computed from the existing advisory and SBOM relationship data (`entity/advisory.rs`, `entity/sbom_advisory.rs`, `entity/sbom.rs`). This task provides the service foundation consumed by the endpoint tasks (Task 2, Task 3, Task 4).

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new `remediation` module

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root exposing `model`, `service`, `endpoints`
- `modules/fundamental/src/remediation/model/mod.rs` — model module root and re-exports
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary`, `SeverityStatusCounts`, `RemediationStatus` and `Severity` enums (serde, `rename_all = "snake_case"`)
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct (`product_id`, `product_name`, `total`, `open`, `in_progress`, `resolved`)
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `summary(product: Option<String>)` and `by_product(paginated)` aggregation methods

## Implementation Notes
- Follow the module pattern used by `modules/fundamental/src/advisory/` and `modules/fundamental/src/sbom/` (`model/ + service/ + endpoints/`). Mirror `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` for service construction and DB connection handling.
- Severity source: `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` already carries a `severity` field — reuse the same severity representation rather than defining a parallel mapping.
- Remediation status source: derive Open/In Progress/Resolved from the SBOM-advisory correlation in `entity/sbom_advisory.rs`. Inspect that entity at implementation time to confirm which column carries correlation/remediation state; if no such column exists, stop and raise it on TC-9006 (the Feature forbids new tables) rather than adding schema.
- "Product" grouping: derive from SBOM identity in `entity/sbom.rs` (the SBOM name/product field). Confirm the field at implementation time.
- Push aggregation into SQL (`GROUP BY severity, status` / `GROUP BY product`) using SeaORM select + `column_as` counts — do not load rows into memory and tally in Rust. This is required to meet the p95 < 500ms summary NFR and the 10,000-vulnerability scale target.
- `by_product` must be paginated (Customer Considerations: portfolios > 50 products) — use `common/src/db/query.rs` pagination helpers and return `PaginatedResults<ProductRemediation>` from `common/src/model/paginated.rs`.
- Return `Result<T, AppError>` (`common/src/error.rs`) with `.context()` wrapping on DB errors.
- Per CONVENTIONS.md §Module pattern: place the new domain under `model/ + service/ + endpoints/` directories exactly as the `advisory` module does.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust domain-module (`modules/*/src/<domain>/`) scope.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` and wrap fallible calls with `.context()`; see `modules/fundamental/src/advisory/service/advisory.rs`.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust (`.rs`) handler/service scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering/pagination helpers in `common/src/db/query.rs` instead of hand-written offset/limit logic.
  Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust (`.rs`) DB query scope.
- Constraints (docs/constraints.md): §5.1 keep changes scoped to the files listed above; §5.2 inspect `entity/sbom_advisory.rs` and `AdvisoryService` before writing code; §5.4 do not duplicate existing severity/pagination logic; §2.1–2.3 commits reference TC-9006 task key, use Conventional Commits, and include an `Assisted-by:` trailer; §3.3 open the PR with `--base main`.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, sorting helpers for the by-product query
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for the paginated product breakdown
- `common/src/error.rs::AppError` — error type for service results
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field/representation to reuse
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — service structure and query patterns to mirror
- `entity/src/sbom_advisory.rs` — SBOM-advisory join entity that is the basis for the aggregation

## Acceptance Criteria
- [ ] `RemediationService::summary` returns counts for every severity (Critical, High, Medium, Low) x status (Open, In Progress, Resolved) combination, including zero-count cells
- [ ] `RemediationService::summary` accepts an optional product filter and restricts counts to vulnerabilities affecting that product
- [ ] `RemediationService::by_product` returns a paginated list where each entry has `total`, `open`, `in_progress`, `resolved` and `total == open + in_progress + resolved`
- [ ] Aggregations are computed in SQL from existing tables; no migration or new table is added
- [ ] Module compiles and is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit/integration test: seeded advisories across all severities and statuses produce the expected count matrix from `summary`
- [ ] Test: `summary` with a product filter returns only counts for SBOMs of that product
- [ ] Test: `by_product` pagination (offset/limit) returns correct pages and `total`
- [ ] Test: empty database returns a zero-filled matrix (not an error and not an empty object)

## Verification Commands
- `cargo build -p trustify-module-fundamental` — builds without errors
- `cargo test -p trustify-module-fundamental remediation` — remediation service tests pass

## Dependencies
- None
