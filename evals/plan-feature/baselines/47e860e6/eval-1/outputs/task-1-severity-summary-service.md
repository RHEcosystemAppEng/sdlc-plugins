**Summary**: Add advisory severity summary model and SBOM aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add the server-side aggregation that powers TC-9001: given an SBOM ID, count the unique vulnerability advisories (deduplicated by advisory ID) linked to that SBOM, grouped by severity (Critical, High, Medium, Low), and return them in a new `AdvisorySeveritySummary` model `{ critical, high, medium, low, total }`. The count must be computed in the database from the existing SBOM–advisory relationship — no new tables. This replaces the frontend's multi-page fetch-and-count of `GET /api/v2/sbom/{id}/advisories` and is the basis for the endpoint in Task 2.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `advisory_summary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id)` aggregation method

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct (`critical`, `high`, `medium`, `low`, `total`; serde `Serialize` + OpenAPI schema derive, matching sibling models)

## Implementation Notes
- Data source: join `entity/src/sbom_advisory.rs` (SBOM–Advisory join table) to `entity/src/advisory.rs` and filter by the SBOM ID; group by the advisory severity column and count `DISTINCT advisory.id` so an advisory linked multiple times (e.g. via several packages) is counted once. Do the aggregation in SQL via SeaORM (`select_only().column_as(...count_distinct...)` + `group_by`) rather than loading rows and counting in Rust — required to meet the p95 < 200ms NFR for 500 advisories.
- Severity values: use the same severity representation exposed by `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`. Map Critical/High/Medium/Low into the four fields case-insensitively; map any other/null severity explicitly (do not silently drop into a bucket). Default plan: `total = critical + high + medium + low`; unknown-severity advisories are excluded from all fields — document this in the struct doc comment (open question on TC-9001 impact map).
- SBOM existence: before aggregating, check the SBOM exists (same lookup used by `SbomService` fetch for `GET /api/v2/sbom/{id}` in `modules/fundamental/src/sbom/endpoints/get.rs`). Return `Option<AdvisorySeveritySummary>` (or an `AppError::NotFound` via `common/src/error.rs`) so a non-existent SBOM can never be reported as an all-zero summary. An existing SBOM with no linked advisories returns all zeros.
- Error handling: return `Result<_, AppError>` and wrap DB errors with `.context(...)` as in the existing `SbomService` methods.
- Per repository Key Conventions §Module pattern: place the model under `sbom/model/` and the query under `sbom/service/`, following `model/ + service/ + endpoints/`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain-module scope. Example: `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`).
- Per repository Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service/handler scope. Example: existing fetch in `modules/fundamental/src/sbom/service/sbom.rs`.
- Constraints (docs/constraints.md): §1.4/§5.1 keep changes to the listed files; §5.2 inspect `SbomService`, `AdvisoryService`, and the entities before editing; §5.4 reuse existing join/query logic rather than duplicating it; §2.1–2.3 commits use Conventional Commits, reference the Jira task in the footer, and include `--trailer="Assisted-by: Claude Code"`; §3.1–3.3 branch named after the task ID, PR `--base main`, PR link posted to Jira.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory list/search queries likely already join `sbom_advisory` (backing `GET /api/v2/sbom/{id}/advisories`); reuse its join/filter construction instead of writing a new one
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — defines the `severity` field type; reuse the same severity type/enum for mapping
- `entity/src/sbom_advisory.rs` — SeaORM relation definitions for the join
- `common/src/db/query.rs` — shared query builder helpers (filtering)
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` (fetch) — SBOM existence lookup

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary { critical, high, medium, low, total }` exists and serializes to JSON with exactly those field names
- [ ] `SbomService::advisory_severity_summary` returns correct per-severity counts for an SBOM using only existing tables (no migration added)
- [ ] Advisories linked to the same SBOM more than once are counted once (deduplicated by advisory ID)
- [ ] A non-existent SBOM ID yields a not-found result, never an all-zero summary
- [ ] An existing SBOM with no linked advisories yields all-zero counts
- [ ] Handling of advisories with missing/unknown severity is explicit, documented, and consistent with `total`
- [ ] Aggregation is executed as a single grouped DB query (no per-advisory loading)

## Test Requirements
- [ ] Test: SBOM with advisories at each severity returns the expected counts and `total`
- [ ] Test: the same advisory linked to an SBOM via multiple relationships is counted once
- [ ] Test: unknown SBOM ID returns not-found (fail-closed — not zeros)
- [ ] Test: SBOM with zero advisories returns all zeros
- [ ] Test: advisory with null/unrecognised severity is handled per the documented rule

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test` — all tests pass

## Dependencies
- None
