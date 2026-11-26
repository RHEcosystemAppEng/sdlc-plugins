## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the advisory status directly as an `advisory_status_enum` value on the `advisory` row, instead of first inserting/looking up a row in the `advisory_status` lookup table and storing its `status_id`. This implements UC-2 of TC-9005: the pipeline parses the advisory, maps the feed's status string to `AdvisoryStatus`, and inserts the advisory with the enum status in a single write.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove the lookup-table insert/lookup of `advisory_status`; map the parsed feed status string to `AdvisoryStatus` and set `advisory::ActiveModel.status` directly
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it passes or resolves `status_id` when delegating advisory ingestion (remove any lookup-table plumbing)

## Implementation Notes
- Use the canonical string parser on `AdvisoryStatus` from Task 3 (`entity/src/advisory.rs`) — do not write a second mapping table in the ingestor.
- **Fail-closed on unknown statuses:** today an unknown status would be inserted into (or fail to match) the lookup table. With an enum column, a feed status that does not map to `New`/`Analyzing`/`Fixed`/`Rejected` must cause ingestion of that advisory to return an error (`AppError` with `.context("unknown advisory status ...")`), not silently default to `New` or skip the status. The guard belongs in the status-mapping step of the advisory ingestion function in `modules/ingestor/src/graph/advisory/mod.rs`.
- Keep the insert as a single `advisory::ActiveModel` write with `status: Set(status)`; there must be no remaining read/write of `advisory_status` in the ingestion path.
- Follow the existing SBOM ingestion flow in `modules/ingestor/src/graph/sbom/mod.rs` for how parsed values are mapped to `ActiveModel`s and persisted within the ingestion transaction.
- Propagate errors with `?` and `.context(...)` into `AppError` (`common/src/error.rs`), consistent with the existing ingestion code in `modules/ingestor/src/graph/sbom/mod.rs`.
- Commit rules (docs/constraints.md §2): Conventional Commits (e.g., `refactor(ingestor): write advisory status enum directly`), footer `Implements <task-key>`, `Assisted-by:` trailer.
- PR rules (docs/constraints.md §3): `gh pr create --base TC-9005`; post the PR link on this Jira task.
- Code change rules (docs/constraints.md §5): change only the listed files; compare against the SBOM ingestion path for parity in error handling and logging.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` — enum and string parser introduced by Task 3
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion implementation showing the parse/store pattern
- `common/src/error.rs::AppError` — error type for unknown-status failures

## Acceptance Criteria
- [ ] Advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` writes `advisory.status` as an `advisory_status_enum` value and performs no insert/select on `advisory_status`
- [ ] `IngestorService` (`modules/ingestor/src/service/mod.rs`) contains no `status_id` / `advisory_status` plumbing
- [ ] Each of the feed status strings `New`, `Analyzing`, `Fixed`, `Rejected` is stored as the matching enum value
- [ ] Ingesting an advisory whose feed status is not one of the four values returns an error and does not insert the advisory with a defaulted status (fail-closed)

## Test Requirements
- [ ] Test: ingest an advisory feed document for each of the four statuses and assert the stored `advisory.status` matches
- [ ] Fail-closed test: ingest an advisory with status `"Pending"` (or empty), assert ingestion returns an error and no advisory row is created with a defaulted status
- [ ] Integration test in `tests/api/advisory.rs`: after ingestion, `GET /api/v2/advisory/{id}` returns the ingested status string

## Verification Commands
- `grep -rn "advisory_status\|status_id" modules/ingestor/` — no matches
- `cargo test -p ingestor` — ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
