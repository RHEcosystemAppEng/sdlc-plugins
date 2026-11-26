**Summary:** Write advisory status enum directly in ingestion pipeline

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline so it maps the feed's status string to `AdvisoryStatus` and inserts the advisory row with the enum value directly, removing the current step that writes to / looks up the `advisory_status` lookup table first.

Part of TC-9005 (UC-2: pipeline parses advisory, maps status string to `advisory_status_enum`, inserts advisory with enum status directly).

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove lookup-table insert/lookup; map feed status to `AdvisoryStatus`; set `advisory::ActiveModel.status`
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` advisory ingest path if it resolves or caches `advisory_status` IDs
- `tests/api/advisory.rs` — add ingestion-to-API tests for status values

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, replace the "find-or-insert `advisory_status` row, then set `status_id`" sequence with `status: Set(AdvisoryStatus::try_from(feed_status)?)` using the fallible conversion defined in `entity/src/advisory.rs` (Task 3). Do not duplicate the mapping table in the ingestor.
- Fail-closed: an unknown or missing status string in the feed must cause that advisory's ingestion to return an error (wrapped with `.context()` naming the advisory identifier and offending value). It must not default to `New` or skip the status silently.
- Check `IngestorService` in `modules/ingestor/src/service/mod.rs` for any cached map of status name → `status_id` or pre-seeding of the lookup table and remove it; this is the entrypoint for on-demand ingestion, so both the scheduled/feed and on-demand paths go through the updated graph code.
- Follow the SBOM ingestion structure in `modules/ingestor/src/graph/sbom/mod.rs` for how entities are built with `ActiveModel` and inserted.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap fallible calls with `.context()`. Applies: task modifies modules/ingestor/src/graph/advisory/mod.rs matching the convention's Rust `.rs` handler/service scope. Example: `modules/ingestor/src/graph/sbom/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests run against the real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies tests/api/advisory.rs matching the convention's `tests/api/*.rs` scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §1.4 scoped changes; §2.1–2.3 commit rules; §3.3 PR `--base TC-9005`; §5.1 only listed files; §5.4 reuse `AdvisoryStatus` conversion; §5.6 trace feed status → enum → DB → API response.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` — enum and string conversion from Task 3
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion implementation showing entity insert patterns

## Acceptance Criteria
- [ ] Ingesting an advisory writes `advisory.status` directly; no read or write against `advisory_status` occurs
- [ ] Each feed status (`New`, `Analyzing`, `Fixed`, `Rejected`) is stored as the corresponding enum value
- [ ] An advisory with an unknown or missing status fails ingestion with a descriptive error and is not inserted with a default status
- [ ] `IngestorService` contains no `advisory_status` lookups or caches
- [ ] Ingested advisories are returned by `GET /api/v2/advisory/{id}` with the correct status string

## Test Requirements
- [ ] Test: ingest advisories with each of the four statuses and assert the stored `advisory.status` and the API response status
- [ ] Test (fail-closed): ingest an advisory with an unknown status (e.g., `"Pending"`) and with no status field; assert ingestion returns an error and no advisory row is created
- [ ] Test: re-ingesting an existing advisory with a changed status updates `advisory.status`

## Verification Commands
- `cargo test -p ingestor` — passes
- `grep -rn "advisory_status::\|status_id" modules/ingestor` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
