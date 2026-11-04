## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory.status` enum value directly (UC-2). Today the pipeline inserts or looks up a row in the `advisory_status` lookup table and then writes `advisory.status_id`. After this task it maps the feed's status string to `AdvisoryStatus` (defined in Task 3) and inserts the advisory row with `status` set, with no lookup-table write.

An unknown or missing status string in the feed must cause an explicit ingestion error for that advisory. It must not be silently coerced to a default value.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove the `advisory_status` lookup and insert; map the parsed status string to `entity::advisory::AdvisoryStatus`; set `advisory::ActiveModel.status` directly
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` to propagate the new status-mapping error from advisory ingestion as an ingestion failure, if it handles advisory results or errors
- `tests/api/advisory.rs` — add ingestion-to-API tests that cover each status value and the unknown-status failure path

## Implementation Notes
- **Status mapping:** add a single mapping function in `modules/ingestor/src/graph/advisory/mod.rs`, for example `fn parse_status(raw: &str) -> Result<AdvisoryStatus, ...>`. It accepts exactly the four enum values. If feeds use different casing, normalize case explicitly and document the accepted inputs. Do not duplicate the mapping. If Task 3 added `FromStr` / `TryFrom<&str>` on `AdvisoryStatus` in `entity/src/advisory.rs`, reuse it.
- **Fail-closed ingestion (fail-open risk):** a mapping that falls back to `AdvisoryStatus::New` on an unknown string would let ingestion succeed while recording the wrong lifecycle status. The guard belongs in the status-mapping step of `modules/ingestor/src/graph/advisory/mod.rs`. Return an error for an unknown or missing status so the advisory is not inserted, and surface that error through `IngestorService` in `modules/ingestor/src/service/mod.rs`.
- Remove all reads and writes of `advisory_status::Entity` and `advisory::Column::StatusId` from the ingestor. Afterwards, `grep -rn "advisory_status::\|StatusId\|status_id" --include=*.rs modules/ingestor` must return nothing.
- Keep the advisory insert and its correlation steps (SBOM-advisory linking via `entity/src/sbom_advisory.rs`) inside the transaction they already use. This task only changes how `status` is set.
- Shared-artifact coverage: the ingestor is the only runtime writer of `advisory.status`. Task 2's backfill is the only other writer. Readers are handled in Task 3. If the codebase grep in Task 3 finds another advisory writer (for example a re-ingest or update path in `modules/ingestor/src/graph/advisory/mod.rs`), that path must also set `status` directly and must be covered by a test here.
- Per CONVENTIONS.md §Framework: write the enum through the SeaORM `ActiveModel` (`status: Set(AdvisoryStatus::Fixed)`) rather than raw SQL.
  Applies: task modifies modules/ingestor/src/graph/advisory/mod.rs matching the convention's SeaORM `.rs` database code scope.
- Per CONVENTIONS.md §Testing: add the ingestion-to-API tests to `tests/api/advisory.rs` against the real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies tests/api/advisory.rs matching the convention's tests/api integration test scope.
- Constraints (docs/constraints.md): Conventional Commits with a TC-9005 footer and the `Assisted-by: Claude Code` trailer (§2.1–2.3). Open the PR with `--base TC-9005` (§3.3). Keep changes scoped to the listed files (§5.1). Inspect before modifying (§5.2). Reuse the `AdvisoryStatus` type and any parser from Task 3 rather than duplicating them (§5.4).

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` — enum added in Task 3. Reuse it, and any `FromStr` / `TryFrom` impl on it, for mapping.
- `modules/ingestor/src/graph/sbom/mod.rs` — sibling ingestion module. Follow its parse-and-store error handling for parity (§5.8).
- `common/src/error.rs::AppError` — existing error type for surfacing ingestion failures

## Acceptance Criteria
- [ ] Advisory ingestion inserts the advisory row with `status` set from the feed and never reads or writes `advisory_status`
- [ ] Each of `New`, `Analyzing`, `Fixed`, `Rejected` in the feed is stored as the matching `advisory_status_enum` value
- [ ] An unknown or missing status in the feed makes ingestion of that advisory fail with an explicit error. No row is inserted and no default status is applied.
- [ ] `IngestorService` reports the status-mapping failure as an ingestion error and does not report success
- [ ] No `advisory_status` / `status_id` references remain under `modules/ingestor`
- [ ] The full workspace (`cargo build`) compiles on `TC-9005` once Tasks 2 to 4 have merged

## Test Requirements
- [ ] Ingest an advisory for each of the four statuses, then call `GET /api/v2/advisory/{id}` and assert that the `status` string matches the feed
- [ ] Ingest an advisory with status `Fixed`, call `GET /api/v2/advisory?status=Fixed`, and assert that it appears in the results
- [ ] Fail-closed test: ingest an advisory whose feed status is unknown (e.g., `"Withdrawn"`) or missing. Assert that ingestion returns an error and that the advisory does not exist afterwards (not stored as `New`).
- [ ] Existing advisory ingestion and correlation tests still pass

## Verification Commands
- `grep -rn "advisory_status::\|StatusId\|status_id" --include=*.rs modules/ingestor` — no matches
- `cargo build` — the whole workspace compiles
- `cargo test --manifest-path tests/Cargo.toml` — all API tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add advisory_status_enum migration
- Depends on: Task 3 — Update SeaORM entities and advisory query layer to use the status enum column
