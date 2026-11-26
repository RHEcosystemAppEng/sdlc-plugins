## Repository
trustify-backend

## Target Branch
main

## Description
Add the domain model and service-layer query that aggregate vulnerability advisory severity counts for a single SBOM. This is the data foundation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). The aggregation must count only unique advisories (deduplicated by advisory ID) linked to the SBOM through the existing SBOM-Advisory join table, grouped by severity (Critical, High, Medium, Low), plus a total. No new database tables are introduced.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new `AdvisorySeveritySummary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id)` aggregation method

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }` with `Serialize`/`Deserialize` derives

## Implementation Notes
- Query the join table `entity/src/sbom_advisory.rs` filtered by `sbom_id`, joined to `entity/src/advisory.rs` to read the advisory severity. Use `COUNT(DISTINCT advisory.id)` grouped by severity so the same advisory linked multiple times (e.g., via several packages) is counted once.
- Do the aggregation in a single SQL query (SeaORM `select_only()` + `column_as()` + `group_by()`), not by loading advisories into memory — the NFR is p95 < 200ms for SBOMs with up to 500 advisories.
- The severity value semantics come from `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary` includes a `severity` field). Reuse the same severity representation/mapping rather than redefining string constants; map unknown/unset severities so they are not counted in any bucket but document whether they count toward `total` (recommended: `total` = critical + high + medium + low).
- The method must distinguish "SBOM does not exist" from "SBOM has zero advisories": first check existence of the SBOM (reuse the lookup used by `SbomService` fetch in `modules/fundamental/src/sbom/service/sbom.rs`) and return a not-found `AppError` variant from `common/src/error.rs` when absent; return all-zero counts when the SBOM exists but has no linked advisories.
- Wrap database errors with `.context(...)` and return `Result<AdvisorySeveritySummary, AppError>`.
- Model placement follows the existing `modules/fundamental/src/sbom/model/summary.rs` / `details.rs` layout.
- Per CONVENTIONS.md §Module pattern: place the struct under `sbom/model/` and the query under `sbom/service/`, following the `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain module (`modules/*/src/**/*.rs`) scope. Example: `modules/fundamental/src/sbom/model/summary.rs` + `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap fallible calls with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service (`.rs`) scope. Example: existing fetch methods in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Query helpers: use shared filtering helpers from `common/src/db/query.rs` where applicable instead of hand-rolled filter code. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs`) scope.
- Constraints (docs/constraints.md): commits must follow Conventional Commits, reference the Jira task ID in the footer, and include an `Assisted-by:` trailer (§2.1–2.3); PR must target `--base main` and its link must be posted on the Jira task (§3.2, §3.3); changes scoped to listed files, inspect before modifying, reuse existing utilities, verify sibling parity (§5.1–5.8); implement-task must stay in scope and not guess code structure (§1.4, §1.5).

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join entity; source of the SBOM → advisory relationship (no new tables per NFR)
- `entity/src/advisory.rs` — advisory entity carrying severity
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field/representation to reuse for bucket mapping
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory queries; check for an existing "advisories by SBOM" query to extend rather than duplicate
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch used for the existence check
- `common/src/db/query.rs` — shared query builder helpers
- `common/src/error.rs::AppError` — not-found and database error variants

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields and serializes to `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] `SbomService::advisory_severity_summary` returns correct per-severity counts for an SBOM using the existing `sbom_advisory` relationship
- [ ] Advisories linked to the same SBOM more than once are counted exactly once (deduplicated by advisory ID)
- [ ] Returns a not-found `AppError` when the SBOM ID does not exist
- [ ] Returns all-zero counts (not an error) when the SBOM exists but has no advisories
- [ ] Aggregation is performed in the database in a single query; no new tables or migrations are added

## Test Requirements
- [ ] Service-level test: SBOM with advisories of mixed severities returns correct counts per bucket and correct total
- [ ] Service-level test: same advisory linked twice to an SBOM is counted once
- [ ] Service-level test: non-existent SBOM ID returns the not-found error
- [ ] Service-level test: SBOM with zero advisories returns all zeros

## Verification Commands
- `cargo test -p trustify-module-fundamental advisory_severity_summary` — all new service tests pass
- `cargo clippy --all-targets -- -D warnings` — no new warnings

## Dependencies
- None
