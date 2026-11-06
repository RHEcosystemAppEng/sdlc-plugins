**Summary:** Update advisory ingestion pipeline to write AdvisoryStatus enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
The advisory ingestion pipeline currently writes or looks up a row in the `advisory_status` table and then stores its id in `advisory.status_id`. After this task, the pipeline maps the feed's status string to `AdvisoryStatus` (from Task 3) and stores it directly in `advisory.status`, with no lookup-table insert or select.

Use case UC-2: parse the advisory, map the status string to an `advisory_status_enum` value, and insert the advisory row with that status.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion (parse, store, correlate): remove the `advisory_status` lookup/insert, map the parsed status string to `AdvisoryStatus`, and set `advisory::ActiveModel.status`
- `modules/ingestor/src/service/mod.rs` — `IngestorService`: update it only if it passes status ids or creates `advisory_status` rows on behalf of the graph layer. Otherwise leave it unchanged

## Implementation Notes
- Before you start, run `grep -rn "advisory_status\|status_id" modules/ingestor/` to find every ingestion write site. This includes alternate paths that populate `advisory`, such as re-ingest or update of an existing advisory, and any bulk or backfill entry point in `IngestorService`. Every path that writes an advisory row must set `status` through the same mapping function. If a path is found that this task does not list, include it.
- Put the mapping in one function, e.g. `fn map_status(raw: &str) -> Result<AdvisoryStatus, AppError>`, that calls `AdvisoryStatus::from_str` from Task 3. Every write path calls it.
- **Fail closed on unknown status:** if the feed carries a status string that is not one of `New`, `Analyzing`, `Fixed`, `Rejected`, reject that advisory with an error, using `AppError` and `.context()`, e.g. "unknown advisory status '<raw>' for advisory <id>". Do not default to `New`, do not store `NULL`, and do not skip the advisory while reporting success. The old lookup table could absorb new names; the enum cannot, so an unknown status must be visible. Decide with the team whether matching is case-sensitive and document the choice. The default is an exact match against the enum labels.
- On re-ingest of an existing advisory, update `status` to the new value. Keep the existing identifier and upsert behavior of the ingestion code; only the status field's storage changes.
- Follow the error-handling convention: return `Result<T, AppError>` with `.context()` wrapping, as in the existing `modules/ingestor/src/graph/advisory/mod.rs` and `modules/ingestor/src/graph/sbom/mod.rs`.
- Constraints (docs/constraints.md):
  - §2.1–2.3: Conventional Commit, task-key footer, `Assisted-by:` trailer.
  - §3.3: `gh pr create --base TC-9005`.
  - §5.1–5.4: scoped files, inspect first, reuse `AdvisoryStatus::from_str`.
  - §5.6: trace UC-2 from feed parse to the persisted row.
  - §5.8: keep parity with the error handling in `modules/ingestor/src/graph/sbom/mod.rs`.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` (from Task 3) — enum and `FromStr`. Reuse it rather than writing a second string-to-status map
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion module, as the pattern for error context and ActiveModel insertion
- `common/src/error.rs::AppError` — error type for rejecting unknown statuses

## Acceptance Criteria
- [ ] Ingesting an advisory with status `New`, `Analyzing`, `Fixed` or `Rejected` stores that value in `advisory.status`
- [ ] No ingestion code path reads from or writes to `advisory_status`, or sets `status_id`
- [ ] Every ingestion path that writes an advisory row, including initial insert and re-ingest/update, uses the single status mapping function
- [ ] Re-ingesting an existing advisory with a changed status updates `advisory.status` and keeps the advisory's identifier
- [ ] Ingestion fails closed: an advisory whose feed status is not a valid enum label is rejected with an error naming the advisory and the raw value. It is not stored with a default or `NULL` status and is not silently skipped while reporting success

## Test Requirements
- [ ] Ingest test: one advisory per status value, then assert the persisted `advisory.status` matches
- [ ] Re-ingest test: ingest an advisory as `New`, re-ingest it as `Fixed`, then assert the same advisory row now has `status = Fixed`
- [ ] Fail-closed test: ingest an advisory with status `"Bogus"` (and an empty string). Assert ingestion returns an error and that no advisory row with a default status was written
- [ ] Assert no `advisory_status` table access happens during ingestion. The table no longer exists after Task 2, so any access fails at runtime in the integration test DB

## Verification Commands
- `cargo test -p ingestor` — ingestion tests pass
- `grep -rn "advisory_status\b\|status_id" modules/ingestor/` — no output

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity
