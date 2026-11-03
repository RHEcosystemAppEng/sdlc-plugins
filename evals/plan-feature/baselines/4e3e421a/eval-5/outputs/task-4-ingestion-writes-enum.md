# Task 4 — Update advisory ingestion pipeline to write status enum values directly

**Summary:** Update advisory ingestion pipeline to write status enum values directly
**Labels:** ai-generated-jira
**Priority:** High (inherited from TC-9005)
**Fix Versions:** RHTPA 2.0.0 (inherited from TC-9005, fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Change the advisory ingestion pipeline so it writes the advisory status directly as an `AdvisoryStatus` enum value on the `advisory` row. Today it first inserts or looks up a row in the `advisory_status` lookup table and stores that row's id in `status_id`. This covers the TC-9005 requirement "Update advisory ingestion pipeline to write enum values directly" and implements UC-2: parse the advisory, map the status string to `advisory_status_enum`, and insert the advisory row with the enum status, with no lookup-table insert.

The ingestion pipeline is the only runtime writer of `advisory.status`. The Task 2 migration backfill is the one-time writer. With this task, every producer of the column moves to the enum.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove the `advisory_status` lookup or insert step. Add a mapping from the feed status string to `entity::advisory::AdvisoryStatus` and set `status` on the advisory `ActiveModel` before insert or update.
- `modules/ingestor/src/service/mod.rs` — `IngestorService`: remove any `advisory_status` seeding or caching, and pass ingestion errors from an unmappable status up to the caller
- `tests/api/advisory.rs` — add ingestion-driven tests that ingest advisories and assert the stored status

## Implementation Notes
**Status mapping (fail-closed):** add a `TryFrom<&str>` (or `FromStr`) implementation for `AdvisoryStatus`, in `entity/src/advisory.rs` from Task 3 or locally in the ingestor, that maps the feed's status strings to the four variants. If the feed uses different spellings, such as lowercase `fixed`, normalize them explicitly in the mapping. An unrecognized or missing status string must return an error that the ingestion call reports. It must not silently default to `New`, and the advisory must not be stored with a guessed status. With the lookup table gone, unknown values can no longer be stored as new lookup rows, so a silent default would make ingestion report success while recording the wrong data.

**Gate site:** the status mapping call in `modules/ingestor/src/graph/advisory/mod.rs`, where the advisory `ActiveModel` is built. Return `Err(...)` with `.context("unrecognized advisory status: {value}")`.

**Cross-cutting call sites:** run `grep -rn "advisory_status\|StatusId" modules/ingestor/` and update every hit. After this task, `cargo check --workspace` must pass with zero references to the removed lookup entity anywhere in the workspace.

**Patterns to follow:**
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for the unmappable-status error. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's error-returning code scope. Reference example: the existing parse and store error handling in `modules/ingestor/src/graph/sbom/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against a real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.

**Constraints (docs/constraints.md):** §2.1–2.3 (Jira key footer, Conventional Commits, `Assisted-by: Claude Code` trailer). §3.3 (`gh pr create --base TC-9005`). §5.1–5.8 (stay within the files listed above, inspect before modifying, follow existing ingestion patterns, check parity with the SBOM ingestion path for error handling and logging).

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` (added in Task 3) — the enum to write. Put the string-to-enum conversion next to it so it is defined in one place.
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion path showing the parse, store, and link structure and its error handling

## Acceptance Criteria
- [ ] Advisory ingestion no longer reads, inserts, or references the `advisory_status` table or entity
- [ ] Each ingested advisory is stored with `advisory.status` set to the enum value that corresponds to the feed's status (`New`, `Analyzing`, `Fixed`, `Rejected`)
- [ ] Re-ingesting an existing advisory with a changed status updates `advisory.status` in place, following the existing update semantics
- [ ] Fail-closed: a feed advisory with an unrecognized or missing status string makes ingestion of that advisory return an error naming the offending value. It is not stored with a default status, and the ingestion result is not reported as successful.
- [ ] `cargo check --workspace` passes, and `grep -rn "advisory_status" --include=*.rs .` matches only the `enum_name = "advisory_status_enum"` attribute and the migration files

## Test Requirements
- [ ] Integration test: ingest one advisory per status value and assert that each persisted row's `status` equals the expected enum value, and that the advisory list endpoint returns the matching status strings
- [ ] Integration test: ingest an advisory, re-ingest it with a different status, and assert the stored `status` is updated
- [ ] Fail-closed test: ingest an advisory whose status is `"Bogus"` (and one with no status field) and assert ingestion returns an error and no advisory row is created for it
- [ ] Unit test: the status mapping covers all four valid strings plus any normalized spellings, and returns `Err` for unknown input

## Verification Commands
- `cargo test --workspace` — all tests pass, including the ingestion and advisory integration suites
- `cargo check --workspace` — the build succeeds with no references to the removed lookup entity

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity and advisory queries to use the status enum column
