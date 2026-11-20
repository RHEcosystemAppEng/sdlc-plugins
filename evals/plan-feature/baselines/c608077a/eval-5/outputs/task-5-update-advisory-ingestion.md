# Task 5 — Write advisory status enum directly in advisory ingestion pipeline

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline so that it maps the feed's status string to an `AdvisoryStatus` enum value and inserts/updates the advisory row with that value directly, instead of first writing to (or looking up in) the `advisory_status` lookup table and storing `status_id`. Covers UC-2 (advisory ingestion writes the enum value directly without a lookup table insert).

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove the `advisory_status` lookup/insert step; map the parsed feed status to `AdvisoryStatus` and set `advisory::ActiveModel.status` directly on insert and update
- `modules/ingestor/src/service/mod.rs` — propagate the new unknown-status ingestion error from the advisory graph through `IngestorService` (only if the service currently maps advisory graph errors explicitly)

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs` (advisory ingestion: parse, store, correlate), locate the step that resolves or inserts the status row in `advisory_status` and sets `status_id`; replace it with a conversion of the parsed status string using the fallible `AdvisoryStatus` conversion added in `entity/src/advisory.rs` (Task 3), then set `status: Set(advisory_status)` on the `advisory::ActiveModel`.
- Fail-closed mapping: if the feed contains a status string that does not map to one of `New`, `Analyzing`, `Fixed`, `Rejected`, the ingestion of that advisory must return an error (with `.context()` naming the advisory identifier and the offending value) — it must not silently default to `New`, skip the status, or insert the row with a null status. Previously the lookup-table path could have accepted arbitrary values; with the enum, unknown values must be surfaced explicitly.
- If the feed format uses different casing or synonyms (e.g., `fixed`, `FIXED`), normalize case before conversion and document the accepted mapping in a code comment; do not broaden the mapping beyond the four statuses.
- Re-ingestion/update path: ensure the same enum write is applied when an existing advisory is updated by a re-ingested feed, not only on first insert (both paths previously wrote `status_id`).
- Keep the correlation logic with SBOMs (via `entity/src/sbom_advisory.rs`) unchanged.
- Follow the error-propagation pattern of the sibling SBOM ingestion in `modules/ingestor/src/graph/sbom/mod.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>`-compatible errors and wrap fallible calls with `.context()`. Applies: task modifies modules/ingestor/src/graph/advisory/mod.rs matching the convention's Rust `.rs` error-handling scope. See `modules/ingestor/src/graph/sbom/mod.rs` for the established pattern.
- Per CONVENTIONS.md §Framework: write rows through SeaORM `ActiveModel`s. Applies: task modifies modules/ingestor/src/graph/advisory/mod.rs matching the convention's SeaORM database `.rs` scope. See `modules/ingestor/src/graph/sbom/mod.rs` for the established pattern.
- Constraints (docs/constraints.md): commits must reference the Jira task ID in the footer (§2.1), follow Conventional Commits (§2.2), and include an `Assisted-by:` trailer (§2.3); the PR must be opened with `--base TC-9005` (§3.3) and its link posted to the Jira task (§3.2); changes scoped to the listed files (§5.1), inspected before modification (§5.2), reuse the entity's `AdvisoryStatus` conversion rather than writing a second string mapping (§5.4); trace the full ingest data flow feed → parse → enum → DB row → API read (§5.6).

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` (from Task 3) — typed enum with fallible string conversion; reuse instead of a new mapping table in the ingestor
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion module showing parse/store/error-propagation structure
- `common/src/error.rs::AppError` — error type for surfacing unknown status values

## Acceptance Criteria
- [ ] Advisory ingestion performs no read or write against `advisory_status` and does not set `status_id`
- [ ] Ingesting an advisory with each of the four feed statuses stores the matching `advisory_status_enum` value in `advisory.status`
- [ ] Re-ingesting an existing advisory with a changed status updates `advisory.status`
- [ ] Ingesting an advisory with an unknown status string fails with an error identifying the advisory and value, and no advisory row is written with a defaulted or null status
- [ ] SBOM–advisory correlation behaviour is unchanged

## Test Requirements
- [ ] Test: ingest a feed containing advisories with `New`, `Analyzing`, `Fixed`, `Rejected`; assert `advisory.status` holds the corresponding enum values and that no `advisory_status` table access occurs (table no longer exists after Task 2)
- [ ] Test: re-ingest an advisory with a changed status; assert the stored status is updated
- [ ] Test: ingest an advisory with an unknown status (e.g., `"Pending"`); assert ingestion returns an error and the advisory is not persisted with a default status
- [ ] Test: end-to-end — ingest an advisory, then `GET /api/v2/advisory/{id}` (via `tests/api/advisory.rs` helpers) returns the ingested status string

## Verification Commands
- `cargo test -p ingestor` — ingestor tests pass
- `grep -rn "advisory_status::\|status_id" modules/ingestor` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column
