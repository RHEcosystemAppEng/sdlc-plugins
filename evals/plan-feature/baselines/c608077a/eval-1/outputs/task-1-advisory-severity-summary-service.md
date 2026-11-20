## Repository
trustify-backend

## Target Branch
main

## Description
Add a server-side aggregation that computes unique advisory severity counts (critical, high, medium, low, total) for a given SBOM. This is the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). Today the frontend paginates through `GET /api/v2/sbom/{id}/advisories` and counts severities client-side; moving the count into a single grouped database query is what makes the p95 < 200ms target (SBOMs with up to 500 advisories) achievable. Counts must deduplicate by advisory ID and must use the existing SBOM-advisory relationship table — no new tables or migrations.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — register and re-export the new `advisory_summary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id)` returning the aggregated counts, or `None`/not-found when the SBOM does not exist

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }` with `Serialize`/`Deserialize` (and the OpenAPI schema derive used by sibling models)

## Implementation Notes
- Follow the existing `model/ + service/ + endpoints/` module layout of `modules/fundamental/src/sbom/`. Model the new struct on `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for derives and serde attributes.
- Implement the query in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) alongside the existing fetch/list methods. Join `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) to `entity/src/advisory.rs` (Advisory entity), filter by SBOM ID, and `COUNT(DISTINCT advisory.id)` grouped by severity. Do the counting in SQL (SeaORM `select_only().column_as(...).group_by(...)`), not by loading rows into memory.
- The severity field and its value set are defined on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`; map those severity values to the four buckets. Document (in a code comment) how any severity outside Critical/High/Medium/Low is handled — it counts toward `total` only. `total` is the count of distinct advisory IDs, not the sum of buckets if extra severities exist.
- Check SBOM existence first (reuse the existing lookup used by `GET /api/v2/sbom/{id}` in `modules/fundamental/src/sbom/endpoints/get.rs` / `SbomService` fetch) so the endpoint task can return 404 for an unknown ID rather than all-zero counts. An SBOM that exists with no advisories returns all zeros.
- Return `Result<_, AppError>` and wrap DB errors with `.context()` per `common/src/error.rs`.
- Per CONVENTIONS.md §Module pattern: place the model under `sbom/model/` and the query under `sbom/service/`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain module (`modules/*/src/<domain>/{model,service,endpoints}`) scope. Example: `modules/fundamental/src/advisory/service/advisory.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared helpers in `common/src/db/query.rs` for filtering rather than hand-rolled query fragments. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs` service) scope.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task ID in the footer, and include an `Assisted-by:` trailer; §3 branch is named after the task ID and the PR is opened with `--base main` with its link posted to Jira; §5 keep changes to the listed files, inspect code before modifying, reuse existing helpers rather than duplicating logic.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory fetch/list/search queries; reuse its severity column handling and any SBOM-scoped advisory query rather than writing a parallel one
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — defines the `severity` field and its value set
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join entity (the required relationship table; no new tables)
- `common/src/db/query.rs` — shared filtering helpers
- `common/src/error.rs::AppError` — standard error type

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` serializes to `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Counts deduplicate by advisory ID — an advisory linked to the SBOM more than once is counted once
- [ ] Aggregation is a single grouped SQL query over `sbom_advisory` + `advisory`; no new tables or migrations are added
- [ ] Unknown SBOM ID is reported as not-found (distinguishable from an SBOM with zero advisories)
- [ ] An SBOM with no advisories returns all-zero counts

## Test Requirements
- [ ] Service-level test: SBOM with advisories across all four severities returns correct per-bucket counts and total
- [ ] Service-level test: the same advisory linked twice to one SBOM is counted once
- [ ] Service-level test: SBOM with no linked advisories returns all zeros
- [ ] Service-level test: non-existent SBOM ID returns not-found

## Verification Commands
- `cargo test -p trustify-module-fundamental` — new and existing tests pass

## Dependencies
- None
