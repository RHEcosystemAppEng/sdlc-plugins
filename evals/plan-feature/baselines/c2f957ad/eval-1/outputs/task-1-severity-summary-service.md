## Repository
trustify-backend

## Target Branch
main

## Description
Add the domain model and service-layer aggregation that counts the unique vulnerability advisories affecting an SBOM, bucketed by severity (Critical, High, Medium, Low). This is the core computation behind the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001) and replaces the frontend's multi-page fetch-and-count logic with a single server-side aggregate query over the existing SBOM–advisory relationship.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new `AdvisorySeveritySummary` model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id)` aggregation method

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary { critical: u64, high: u64, medium: u64, low: u64, total: u64 }` with `Serialize`/`Deserialize` (and OpenAPI schema derive if sibling models use one)

## Implementation Notes
- Data source: join `entity/src/sbom_advisory.rs` (SBOM–Advisory join table) with `entity/src/advisory.rs` and group by the advisory severity column. Do NOT add tables or migrations (NFR: use existing advisory-SBOM relationship tables).
- Deduplicate by advisory ID: count `DISTINCT advisory.id` per severity so that an advisory linked to an SBOM multiple times (e.g., via several packages) is counted once.
- Perform the aggregation in a single SQL `GROUP BY` query via SeaORM rather than loading all advisories into memory — required to meet the p95 < 200ms target for SBOMs with up to 500 advisories.
- Severity values: map from the same severity representation used by `AdvisorySummary.severity` in `modules/fundamental/src/advisory/model/summary.rs`. Matching must be case-insensitive. Advisories with a severity outside the four buckets (e.g., none/unknown) are not counted in any bucket; `total` = critical + high + medium + low (decision recorded in the impact map; adjust if product clarifies otherwise).
- Distinguish "SBOM not found" from "SBOM with zero advisories": the method must return a not-found error (`AppError` from `common/src/error.rs`) when the SBOM ID does not exist, rather than returning a summary of all zeros. Reuse the existence check pattern used by `SbomService` fetch for `GET /api/v2/sbom/{id}`.
- Follow the error handling pattern: return `Result<AdvisorySeveritySummary, AppError>` and wrap DB errors with `.context()`.
- Model placement mirrors `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`.
- Per CONVENTIONS.md §Module pattern: place the new struct under `sbom/model/` and the query under `sbom/service/`, keeping the `model/ + service/ + endpoints/` split. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope.
- Per CONVENTIONS.md §Error handling: the service method returns `Result<T, AppError>` with `.context()` wrapping on every fallible DB call. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use shared helpers in `common/src/db/query.rs` where they cover the filter/join being built rather than hand-rolling query fragments. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs`) scope.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task in the footer, and include an `Assisted-by:` trailer; §3 PR branch named after the Jira task ID, `gh pr create --base main`, PR link posted on the Jira task; §5 keep changes scoped to the listed files, inspect code before modifying it, reuse existing helpers, and compare against sibling services for parity in error handling.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field/type; reuse its severity representation for bucketing instead of redefining severity values
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic contains the SBOM existence lookup to reuse for the not-found path
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory queries may already join through `sbom_advisory` (backing `GET /api/v2/sbom/{id}/advisories`); reuse the join rather than duplicating it
- `common/src/db/query.rs` — shared query builder helpers
- `entity/src/sbom_advisory.rs` — SBOM–Advisory join entity

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` serializes to `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] `SbomService::advisory_severity_summary` returns counts of unique advisories (deduplicated by advisory ID) per severity for the given SBOM
- [ ] `total` equals the sum of the four severity counts
- [ ] Non-existent SBOM ID returns a not-found `AppError`, not a zero-count summary
- [ ] An existing SBOM with no linked advisories returns all zeros
- [ ] Aggregation is computed in the database (single grouped query); no new tables or migrations are added

## Test Requirements
- [ ] Service test: SBOM with advisories across all four severities returns correct per-severity counts and total
- [ ] Service test: the same advisory linked to the SBOM more than once is counted once
- [ ] Service test: SBOM with zero advisories returns all-zero summary
- [ ] Service test: unknown SBOM ID returns a not-found error (fail-closed — must not return zeros)
- [ ] Service test: advisories with a severity outside the four buckets are excluded from counts and total

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors (adjust crate name to the one in `modules/fundamental/Cargo.toml`)
- `cargo test -p trustify-module-fundamental advisory_severity_summary` — new tests pass

## Dependencies
- None
