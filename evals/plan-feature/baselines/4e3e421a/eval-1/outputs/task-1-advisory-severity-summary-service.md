## Repository
trustify-backend

## Target Branch
main

## Description
Add the domain model and service-layer logic that aggregates vulnerability advisory severity counts for a single SBOM. This is the foundation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). The service must count only unique advisories linked to the SBOM (deduplicated by advisory ID) and bucket them into Critical, High, Medium, and Low, plus a total. The aggregation must be performed in the database (a single grouped query over the existing SBOM-advisory join table) rather than by loading every advisory into memory, so that the endpoint can meet the p95 < 200ms target for SBOMs with up to 500 advisories. No new database tables may be introduced.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new `AdvisorySeveritySummary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::advisory_severity_summary(sbom_id)` method that runs the aggregation query and returns `Option<AdvisorySeveritySummary>` (None when the SBOM does not exist)

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` (all `u64`), deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, and `utoipa::ToSchema` if the sibling models use it

## Implementation Notes
- Query against the existing join entity `entity/src/sbom_advisory.rs` joined to `entity/src/advisory.rs`; filter by `sbom_id`, then `COUNT(DISTINCT advisory.id)` grouped by the advisory severity column. Do not add migrations under `migration/` — the feature NFR forbids new tables.
- The severity field already exists on the advisory side: see the `severity` field in `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`). Reuse the same severity type/enum when mapping the grouped rows into the struct so that the string-to-bucket mapping is defined in one place.
- Deduplication requirement: an advisory linked to the same SBOM through multiple rows (e.g., via multiple packages) must be counted once. Use `COUNT(DISTINCT ...)` (or `SELECT DISTINCT advisory_id` subquery) rather than counting join rows.
- `total` must equal the number of unique advisories linked to the SBOM. Decide explicitly how advisories with a null or unrecognized severity are handled: they must still be counted in `total` (so `total` is never silently smaller than the true count) and must not be silently folded into another bucket. Document the decision in a doc comment on the struct.
- SBOM existence: first check the SBOM via the existing fetch logic in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) and return `Ok(None)` when it is missing, so the endpoint can map it to 404. An existing SBOM with zero advisories must return `Some` with all counts `0` — never conflate "SBOM missing" with "no advisories".
- Error handling: return `Result<_, AppError>` (`common/src/error.rs`) and wrap DB errors with `.context(...)`, following the existing service methods.
- Follow the module pattern `model/ + service/ + endpoints/` used throughout `modules/fundamental/src/`.
- Constraints (docs/constraints.md): §2 commits must use Conventional Commits, reference the Jira task in the footer, and carry the `Assisted-by: Claude Code` trailer; §3 PR targets `main` via `gh pr create --base main` and the PR link is posted to the Jira task; §5 keep changes to the listed files, inspect code before changing it, reuse existing helpers instead of duplicating, and compare against sibling services for parity in error handling.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — already carries the advisory `severity` field; reuse its severity type for bucketing
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic for SBOM existence check; add the new method here rather than creating a new service
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory query logic (list/search); check for an existing "advisories by SBOM" query to reuse its join instead of re-writing it
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join entity to aggregate over
- `common/src/db/query.rs` — shared query builder helpers; reuse filtering helpers where applicable

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary { critical, high, medium, low, total }` exists in the SBOM model module and is serializable to JSON with exactly those field names
- [ ] `SbomService::advisory_severity_summary` returns `None` when the SBOM ID does not exist
- [ ] Returns all-zero counts (not `None`, not an error) for an existing SBOM with no linked advisories
- [ ] Advisories linked multiple times to the same SBOM are counted once (deduplicated by advisory ID)
- [ ] `total` equals the number of unique linked advisories, including any with null/unrecognized severity
- [ ] Aggregation is done in a single database query (no per-advisory loading into memory)
- [ ] No new migration or table is added

## Test Requirements
- [ ] Service test: SBOM with advisories across all four severities returns correct per-bucket counts and total
- [ ] Service test: the same advisory linked twice to the SBOM is counted once
- [ ] Service test: existing SBOM with zero advisories returns `Some` with all zeros
- [ ] Service test: non-existent SBOM ID returns `None`
- [ ] Service test: advisory with null/unrecognized severity is included in `total` and not counted in any of the four named buckets

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_severity_summary` — new tests pass

## Dependencies
- None
