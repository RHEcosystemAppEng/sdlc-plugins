**Summary:** Write advisory status enum directly in ingestion pipeline
**Epic:** TC-9005: Advisory status query and ingestion updates

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
The advisory ingestion pipeline currently writes the status to the `advisory_status` lookup table first and stores the resulting `status_id`. Update it to map the feed's status string to `AdvisoryStatus` and insert the `advisory` row with the enum value directly (UC-2), with no lookup-table insert or lookup.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove lookup-table insert/lookup; parse feed status into `AdvisoryStatus`; set `advisory::ActiveModel.status`
- `modules/ingestor/src/service/mod.rs` — `IngestorService` entry points (scheduled feed and on-demand/API ingestion) — propagate parse errors; remove any `advisory_status` references
- `tests/api/advisory.rs` — ingestion-to-API tests for status values and invalid status

## Implementation Notes
- Use `AdvisoryStatus::from_str` / `TryFrom<&str>` from `entity/src/advisory.rs` (Task 3) — do not add a second mapping table in the ingestor. If the feed uses different casing (e.g., `fixed`), normalize in one place in `modules/ingestor/src/graph/advisory/mod.rs` before parsing.
- **Fail-closed parsing:** an unknown or missing status in the feed must fail ingestion of that advisory with a contextual error (`.context("unknown advisory status ...")`), not silently default to `New` and not skip-and-succeed. The guard belongs in the status-mapping step in `modules/ingestor/src/graph/advisory/mod.rs`, and `IngestorService` in `modules/ingestor/src/service/mod.rs` must surface the error (non-success result), not swallow it.
- Both producer paths that populate `advisory.status` must be covered: the graph ingestion (`graph/advisory/mod.rs`) and every `IngestorService` entry point that routes advisories into it (scheduled feed and on-demand/API upload).
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies modules/ingestor/src/graph/advisory/mod.rs matching the convention's Rust (`.rs`) scope. Example: `modules/ingestor/src/graph/sbom/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against real PostgreSQL using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/advisory.rs matching the convention's Rust (`.rs`) integration test scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR `--base TC-9005`, PR link posted to Jira; §5 scope limited to listed files, inspect before modifying, no duplicated functionality.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` — parsing/mapping (Task 3)
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion pattern (parse, store) for error handling parity

## Acceptance Criteria
- [ ] Advisory ingestion writes `advisory.status` directly with the enum value; no insert into or read from `advisory_status`
- [ ] Each of New, Analyzing, Fixed, Rejected in a feed is stored as the matching enum value
- [ ] A feed advisory with an unknown or missing status fails ingestion with an error (not defaulted, not silently skipped with success)
- [ ] `IngestorService` scheduled and on-demand/API ingestion paths both use the new write path
- [ ] `modules/ingestor` contains no reference to `advisory_status` or `status_id`

## Test Requirements
- [ ] Integration test: ingest an advisory feed containing all four statuses, then `GET /api/v2/advisory/{id}` returns the correct `status` for each
- [ ] Fail-closed test: ingest an advisory with status `"Closed"` (unknown) and one with no status; assert ingestion returns an error and no advisory row is created
- [ ] Test the on-demand/API ingestion entry point in `IngestorService` stores the enum status

## Verification Commands
- `grep -rn "advisory_status\|status_id" modules/ingestor/src` — no matches
- `cargo test --workspace` — all tests pass on the TC-9005 branch

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity for status enum column
