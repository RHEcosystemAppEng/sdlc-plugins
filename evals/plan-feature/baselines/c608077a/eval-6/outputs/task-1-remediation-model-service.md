## Repository
trustify-backend

## Target Branch
main

## Description
Introduce a new `remediation` domain module in `modules/fundamental` that provides the model types and the service-layer aggregation logic backing the TC-9006 vulnerability remediation tracking dashboard. The service computes remediation aggregations (counts by severity x status, per-product breakdown, filterable outstanding-vulnerability listing, and a 30-day trend) entirely from existing vulnerability/advisory and SBOM relationship data — no new database tables are introduced (TC-9006 NFR). This task contains no HTTP endpoints; those are added in Task 2 and Task 3.

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new `remediation` module (`pub mod remediation;`)

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root re-exporting `model` and `service`
- `modules/fundamental/src/remediation/model/mod.rs` — model module root; defines `RemediationStatus` enum (`Open`, `InProgress`, `Resolved`) and re-exports submodules
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct: counts per severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) plus overall totals per status
- `modules/fundamental/src/remediation/model/by_product.rs` — `ProductRemediation` struct: product identifier/name, `total`, `open`, `in_progress`, `resolved` counts
- `modules/fundamental/src/remediation/model/vulnerability.rs` — `RemediationVulnerability` struct (advisory id, identifier, title, severity, product, status, affected SBOM count) and `RemediationTrendPoint` struct (date, open, in_progress, resolved)
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `summary()`, `by_product(paginated)`, `list_vulnerabilities(filters, paginated)`, and `trend(days)` methods

## Implementation Notes
- Follow the existing domain module layout `model/ + service/ + endpoints/` used by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`. Mirror `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` for the service struct shape (constructor taking the DB connection, async methods returning `Result<_, AppError>`).
- Aggregations must be computed in SQL (SeaORM `select` with `group_by` / `count`) over the existing entities — `entity/src/advisory.rs` (severity source), `entity/src/sbom_advisory.rs` (SBOM-to-advisory correlation), `entity/src/sbom.rs` (product grouping). Do not load all rows into memory and aggregate in Rust: the dashboard must support up to 10,000 tracked vulnerabilities and the summary endpoint has a p95 < 500ms target.
- Severity values must match those already exposed by `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` (severity field) so the frontend `SeverityBadge` / `severityUtils.ts` mappings keep working.
- Remediation status derivation: there is no dedicated status column in the documented entities. Derive `RemediationStatus` from the existing `sbom_advisory` relationship data (e.g., a status/remediation attribute on the join row, or presence of a fixed/patched indicator). Before implementing, inspect `entity/src/sbom_advisory.rs` to confirm which column carries the status; if none exists, stop and raise this with the feature owner rather than adding a table (NFR forbids new tables). This is recorded as an open question in the impact map.
- Trend: compute daily status counts for the last N days (default 30) from timestamps already present on the relationship/advisory rows. Same open question applies if no suitable timestamp exists.
- Product grouping: group by the SBOM's product/name attribute from `entity/src/sbom.rs`. Large portfolios (>50 products) must be paginated — use the shared pagination helpers.
- Use `common/src/db/query.rs` helpers for filtering (severity, product, status), pagination and sorting in `list_vulnerabilities` and `by_product` rather than hand-rolling query clauses.
- Wrap all DB errors with `.context(...)` and return `AppError` from `common/src/error.rs`.
- Per CONVENTIONS.md §Module pattern: create the new domain module with `model/`, `service/` subdirectories (endpoints added in Task 2). Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope. Example: `modules/fundamental/src/advisory/`.
- Per CONVENTIONS.md §Error handling: service methods return `Result<T, AppError>` with `.context()` wrapping on every fallible DB call. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust handler/service `.rs` scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination and sorting helpers. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust query code scope. Example: `common/src/db/query.rs`.
- Per CONVENTIONS.md §Response types: paginated listings (`by_product`, `list_vulnerabilities`) return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/remediation/model/by_product.rs` matching the convention's list response `.rs` scope. Example: `common/src/model/paginated.rs`.
- Constraints (docs/constraints.md): §5.1 keep changes scoped to the files listed above; §5.2 inspect entity/service code before modifying; §5.4 reuse existing query helpers and models instead of duplicating; §2.1–2.3 commits reference the Jira task ID, use Conventional Commits, and include an `Assisted-by:` trailer; §3.1–3.3 branch named after the Jira task ID, PR link posted on the task, `gh pr create --base main`.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination and sorting helpers for the filterable list and per-product breakdown
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for paginated aggregates
- `common/src/error.rs::AppError` — standard error type
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field and value set to reuse for severity grouping
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference pattern for service construction and advisory queries
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join entity; source of correlation data for all aggregations

## Acceptance Criteria
- [ ] `RemediationService::summary()` returns counts for every severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) combination, including zero counts for empty combinations
- [ ] `RemediationService::by_product()` returns per-product `total`, `open`, `in_progress`, `resolved` counts, paginated via `PaginatedResults`
- [ ] `RemediationService::list_vulnerabilities()` supports filtering by severity, product and status, plus pagination and sorting by severity
- [ ] `RemediationService::trend(30)` returns one data point per day for the last 30 days
- [ ] All aggregations are computed via SQL grouping over existing entities; no migration or new table is added under `migration/`
- [ ] An empty database yields zeroed summary counts and empty lists (not errors)

## Test Requirements
- [ ] Unit/integration test: seed SBOMs and correlated advisories across multiple severities and statuses and assert `summary()` counts match exactly per severity x status cell
- [ ] Test: `by_product()` with two products returns correct per-product counts and respects pagination limits
- [ ] Test: `list_vulnerabilities()` with each filter (severity, product, status) individually and combined returns only matching rows
- [ ] Test: empty dataset returns zero counts for all summary cells and empty paginated results
- [ ] Test: `trend(30)` returns 30 daily points with counts consistent with seeded timestamps

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental remediation` — all remediation service tests pass

## Dependencies
- None
