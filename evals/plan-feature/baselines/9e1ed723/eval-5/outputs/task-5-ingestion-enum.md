**Summary:** Write advisory status enum directly in ingestion pipeline

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline (UC-2) to map the status string from an advisory feed to `AdvisoryStatus` (the `advisory_status_enum` value) and write it directly to `advisory.status`. Today the pipeline writes to, or looks up, the `advisory_status` table first and stores `status_id`. That table no longer exists after Task 2 (TC-9005).

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion (parse, store, correlate): remove the lookup-table insert/lookup, parse the feed status into `AdvisoryStatus`, and set `advisory::ActiveModel.status`
- `modules/ingestor/src/service/mod.rs` — `IngestorService`: remove any `advisory_status` seeding/caching or status-id plumbing passed into advisory ingestion, and propagate status parse errors as ingestion failures
- `tests/api/advisory.rs` — add ingestion-path tests that ingest advisories and assert the stored status through the API

## Implementation Notes
- **Shared-artifact producers.** `advisory.status` is written by the Task 2 backfill and by this ingestion path. Repository analysis found no other writer (no status-update endpoint and no scheduled job). Before opening the PR, run `grep -rn "advisory_status\|status_id" modules/ingestor/` and a repo-wide search for `advisory::ActiveModel` to confirm this. Any additional writer found (re-ingest/update path, fallback path) must be updated in this task and covered by a test.
- Mapping: use `AdvisoryStatus::from_str` / `TryFrom<&str>` from `entity/src/advisory.rs` (Task 3). Do not add a second mapping table in the ingestor. If feed values differ in case or spelling from the enum labels (e.g., `"fixed"`, `"FIXED"`), normalize them in one place before parsing, and document the accepted forms.
- **Fail-closed on unknown status.** An unrecognized or missing feed status must fail ingestion of that advisory with a descriptive error (wrapped with `.context()`). It must not default silently to `New`, which would store a wrong lifecycle state and still report success. Put the guard at the point in `modules/ingestor/src/graph/advisory/mod.rs` where the parsed advisory is converted into `advisory::ActiveModel`.
- Updates to existing advisories (re-ingestion of the same advisory ID) must update `status` with the same mapping. Identifiers and the existing upsert semantics must stay the same.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` (or the ingestor's existing error type) and wrap failures with `.context()`.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` Rust source scope.
- Per CONVENTIONS.md §Framework: write the status through the SeaORM `ActiveModel` (`Set(AdvisoryStatus::...)`), not raw SQL.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` SeaORM data-access file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` run against a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/*.rs` integration test scope.
- Constraints (docs/constraints.md): §2 commits must use Conventional Commits, include the `Implements TC-<task>` footer and an `Assisted-by:` trailer. §3 the PR must use `--base TC-9005` and the PR link must be posted to the Jira task. §5 changes stay scoped to the listed files, inspect code before modifying it, do not duplicate the enum mapping, and trace the data flow (feed → parse → `advisory.status` → API).

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` — enum and `FromStr` from Task 3. This is the single source of the status mapping
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion module. Follow its parse → store → link structure and error-handling style
- `common/src/error.rs::AppError` — existing error type for ingestion failures

## Acceptance Criteria
- [ ] Advisory ingestion no longer reads or writes the `advisory_status` table or `status_id`
- [ ] A feed advisory with status `New`, `Analyzing`, `Fixed` or `Rejected` is stored with the matching `advisory.status` enum value in a single insert, with no lookup-table insert
- [ ] Re-ingesting an existing advisory with a changed status updates `advisory.status` and keeps the advisory's identifier
- [ ] A feed advisory with an unknown or missing status fails ingestion with a descriptive error and stores no row. It is not defaulted silently
- [ ] `IngestorService` contains no `advisory_status` seeding or status-id plumbing
- [ ] `cargo build -p ingestor` succeeds

## Test Requirements
- [ ] Ingest advisories carrying each of the four statuses, then `GET /api/v2/advisory/{id}` returns the same status string for each
- [ ] Ingest an advisory, then re-ingest it with a different status. Assert the status is updated and the advisory ID is unchanged
- [ ] Ingest an advisory with an unknown status (e.g., `"Closed"`). Assert ingestion returns an error and no advisory row is created
- [ ] Ingest an advisory with no status field. Assert ingestion returns an error (no silent default to `New`)

## Verification Commands
- `cargo test -p tests --test api advisory` — ingestion and advisory tests pass
- `grep -rn "advisory_status\|status_id" modules/ingestor/` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM Advisory entity to use status enum column
