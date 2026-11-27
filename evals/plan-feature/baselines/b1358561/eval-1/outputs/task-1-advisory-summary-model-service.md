Summary: Add advisory severity aggregation model and service method
Epic: TC-9001: Advisory severity summary endpoint
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Add the domain model and service-layer aggregation that powers the new advisory severity
summary for TC-9001. Given an SBOM ID, the service returns the number of **unique** advisories
(deduplicated by advisory ID) affecting that SBOM at each severity level (Critical, High,
Medium, Low) plus a total. The query must use the existing SBOM–advisory relationship tables
(no new tables, per the Feature's NFR) and must report "not found" for an unknown SBOM ID so
the endpoint (Task 2) can return 404 rather than a zero-count summary.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `advisory_summary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id, ...)` aggregation method

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary { critical: u64, high: u64, medium: u64, low: u64, total: u64 }` (serde `Serialize`/`Deserialize`, OpenAPI schema derive matching sibling models)

## Implementation Notes
- Model: mirror the struct/derive style of `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`. Field names must serialize exactly as `critical`, `high`, `medium`, `low`, `total`.
- Query: a single aggregate query over `entity/src/sbom_advisory.rs` (join table) joined to `entity/src/advisory.rs`, filtered by SBOM ID, grouped by the advisory severity column, using `COUNT(DISTINCT advisory.id)` to satisfy the deduplication requirement. Do not load advisory rows into memory and count in Rust — the p95 < 200ms target for 500 advisories requires DB-side aggregation.
- `total` must equal the count of distinct advisories across the four buckets. Decide and document how advisories with a missing/unknown severity are handled (recommended: excluded from buckets and from `total`, with a code comment) — this must be consistent with how `AdvisorySummary.severity` (`modules/fundamental/src/advisory/model/summary.rs`) is represented.
- Severity mapping: map the stored severity representation used by `AdvisorySummary` to the four buckets in one place (a `match` on the severity type), not via string comparisons scattered through the code.
- Not-found (fail-closed): first verify the SBOM exists (reuse the lookup used by `SbomService` fetch for `GET /api/v2/sbom/{id}` in `modules/fundamental/src/sbom/endpoints/get.rs`). If it does not exist, return `AppError` not-found (`common/src/error.rs`) — never return an all-zero summary for a nonexistent SBOM, since that would be a silent "green" result indistinguishable from a clean SBOM.
- The Feature mentions an existing `GET /api/v2/sbom/{id}/advisories` endpoint; its handler is not visible in the SBOM endpoints tree. Locate it and reuse its SBOM→advisory join condition so the summary counts the same advisory set that endpoint lists.
- Per CONVENTIONS.md §Module pattern: place the model in `sbom/model/` and the logic in `sbom/service/`, keeping the `model/ + service/ + endpoints/` split. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain module (`.rs` under `modules/*/src/<domain>/`) scope. Example: `modules/fundamental/src/advisory/` layout.
- Per CONVENTIONS.md §Error handling: return `Result<AdvisorySeveritySummary, AppError>` and wrap DB errors with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service (`.rs`) scope. Example: existing methods in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Query helpers: use shared filtering helpers from `common/src/db/query.rs` where they apply instead of hand-built filter code. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs`) scope.
- Constraints (docs/constraints.md):
  - §1.4/§5.1 — keep changes scoped to the files listed above; no unrelated refactoring.
  - §1.5/§5.2 — inspect `SbomService`, `AdvisorySummary` and the `sbom_advisory` entity before modifying.
  - §5.4 — reuse existing join/query logic; do not duplicate it.
  - §5.11–5.13 — doc comment on every new test; given-when-then comments for non-trivial tests.
  - §2.1–2.3 — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
  - §3.1–3.3 — branch named after the task key; `gh pr create --base main`; post PR link to the Jira task.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic for SBOM existence check
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — source of the `severity` field type/representation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory list/search queries; reuse the SBOM-advisory join condition
- `entity/src/sbom_advisory.rs` — SBOM–Advisory join table entity (satisfies "no new tables")
- `common/src/db/query.rs` — shared filtering helpers
- `common/src/error.rs::AppError` — not-found error variant

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` serializes to `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] `SbomService::advisory_severity_summary` returns correct per-severity counts for an existing SBOM
- [ ] Advisories linked to the SBOM more than once are counted once (dedup by advisory ID)
- [ ] `total` equals the number of distinct counted advisories
- [ ] Unknown SBOM ID returns an `AppError` not-found, not an all-zero summary (fail-closed)
- [ ] An existing SBOM with no advisories returns all zeros (distinguishable from not-found)
- [ ] No new database tables or migrations are introduced
- [ ] Aggregation is performed in a single DB query (no client-side counting)

## Test Requirements
- [ ] Service test: SBOM with advisories of mixed severities returns correct bucket counts and total
- [ ] Service test: the same advisory linked twice to an SBOM (duplicate relationship rows / multiple packages) is counted once
- [ ] Service test: nonexistent SBOM ID yields not-found error (asserts error, not zero counts)
- [ ] Service test: existing SBOM with zero advisories yields `{0,0,0,0,0}`
- [ ] Service test: advisory with missing/unknown severity is handled per the documented rule

## Dependencies
- None
