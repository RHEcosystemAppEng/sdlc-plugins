# Task 1 — Add advisory severity summary model and SBOM service aggregation

**Summary:** TC-9001: Add advisory severity summary model and SbomService aggregation query
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add the server-side aggregation that counts unique vulnerability advisories affecting an SBOM, grouped by severity (Critical, High, Medium, Low). This is the data layer behind the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (Task 2). Today the frontend pages through `GET /api/v2/sbom/{id}/advisories` and counts severities client-side, which takes about 2s for large SBOMs. Doing the counting in the backend lets the endpoint answer in under 200ms (p95) for SBOMs with up to 500 advisories.

The aggregation must count each advisory only once (deduplicate by advisory ID), even when one advisory is linked to the SBOM through more than one row. It must use the existing SBOM–advisory relationship table and must not add new database tables.

Part of feature TC-9001.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `advisory_summary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id)` that runs the aggregation query and returns `Option<AdvisorySeveritySummary>` (`None` when the SBOM does not exist)

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` response struct `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }` deriving `Serialize`, `Deserialize`, `utoipa::ToSchema` (or whichever schema derive sibling models use)

## Implementation Notes
- Follow the module pattern `model/ + service/ + endpoints/`. Put the struct next to `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `details.rs` (`SbomDetails`), and copy their derive and serde attributes.
- Query: join `entity/src/sbom_advisory.rs` (SBOM–advisory join table) to `entity/src/advisory.rs`, filter by `sbom_id`, and group by the advisory severity column using `COUNT(DISTINCT advisory.id)`. Do the aggregation in SQL with SeaORM `select_only()` / `column_as()` / `group_by()`. Do NOT load advisories into memory to count them, because that would break the p95 < 200ms budget. One query should return one row per severity.
- Severity source: `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` already has a `severity` field. Reuse the same severity enum or column mapping so labels match `GET /api/v2/advisory`. Don't create a second severity type.
- Severity normalisation: match severity values case-insensitively to the four buckets. `total` = number of unique advisories linked to the SBOM. If advisories without a severity (or with a severity outside the four buckets) exist, they count toward `total` but not toward any bucket. Document this in a doc comment on the struct.
- Existence check: check that the SBOM exists first, reusing the lookup `SbomService` already uses for `GET /api/v2/sbom/{id}` (`modules/fundamental/src/sbom/endpoints/get.rs` calls into `service/sbom.rs`). Return `Ok(None)` for an unknown ID so the endpoint can turn it into a 404. An SBOM that exists but has no correlated advisories returns all zeros, not `None`.
- The feature says `GET /api/v2/sbom/{id}/advisories` already exists, but it isn't listed in `modules/fundamental/src/sbom/endpoints/`. Before writing a new join, search (`grep -rn "advisories" modules/fundamental/src`) for the query that backs it and reuse its join or filter logic if you find it.
- Error handling: return `Result<_, AppError>` (`common/src/error.rs`) and wrap DB errors with `.context(...)`, as sibling service methods do.
- Per CONVENTIONS.md §Module pattern: add the new model under `sbom/model/` and the query method under `sbom/service/`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain-module (`model/ + service/ + endpoints/`) `.rs` scope.
- Per CONVENTIONS.md §Error handling: the new service method returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service `.rs` scope.
- Constraints (docs/constraints.md): §5.1 keep changes to the files listed here. §5.2 inspect `sbom.rs`, `sbom_advisory.rs`, and `advisory.rs` before editing. §5.4 reuse the existing severity type and SBOM lookup instead of duplicating them. §5.6 trace the data flow (DB → service → struct). §2.1–2.3 commits reference TC-9001's task key, use Conventional Commits, and include an `Assisted-by:` trailer. §3.1–3.3 branch is named after the task key, and the PR uses `--base main` and is linked back in Jira. §1.4–1.5 (implement-task) stay in scope and inspect code before modifying it.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — already has the advisory `severity` field. Reuse its severity type and value mapping for the buckets.
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch-by-ID logic, used for the SBOM existence check.
- `entity/src/sbom_advisory.rs` — existing SBOM–advisory join entity. Join on it so no new table is needed.
- `common/src/db/query.rs` — shared query builder helpers. Reuse any filtering helpers that fit, instead of writing raw filter code.
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has list/search queries over advisories. Check whether its SBOM-scoped filtering can be reused.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` exists with `critical`, `high`, `medium`, `low`, `total` fields that serialize to exactly those JSON keys
- [ ] `SbomService::advisory_severity_summary` returns correct per-severity counts for an SBOM with advisories at all four severities
- [ ] An advisory linked to the SBOM more than once is counted exactly once (deduplicated by advisory ID)
- [ ] Returns `None` for a non-existent SBOM ID
- [ ] Returns all-zero counts (not `None`) for an existing SBOM with no linked advisories
- [ ] Aggregation runs as a single grouped SQL query, with no per-advisory row loading
- [ ] No new database tables or migrations are added

## Test Requirements
- [ ] Service-level test: SBOM with advisories at each severity returns matching counts and `total` equal to the number of unique advisories
- [ ] Service-level test: duplicate SBOM–advisory links for the same advisory produce a count of 1
- [ ] Service-level test: unknown SBOM ID returns `None`
- [ ] Service-level test: existing SBOM with zero advisories returns `{0,0,0,0,0}`
- [ ] Service-level test: advisory with a missing or unrecognised severity counts toward `total` only

## Verification Commands
- `cargo build -p trustify-module-fundamental` (or the crate name in `modules/fundamental/Cargo.toml`) — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_severity_summary` — all new tests pass

## Dependencies
- None
