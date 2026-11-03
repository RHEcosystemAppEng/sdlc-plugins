## Repository
trustify-backend

## Target Branch
main

## Description
Invalidate cached advisory severity summaries when the set of advisories linked to an SBOM changes (TC-9001 NFR: "advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM"). Without this, the 5-minute cache added in Task 2 would serve stale counts after new advisories are correlated, which would understate risk on the dashboard and could cause the alerting integration (UC-2) to miss new critical advisories.

The cached summary is a shared artifact derived from the `sbom_advisory` join table. Every code path that writes rows linking advisories to an SBOM must invalidate the affected SBOM's cache entry, not only the primary advisory ingestion path.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after advisory correlation writes `sbom_advisory` rows, invalidate the summary cache for every affected SBOM ID
- `modules/ingestor/src/graph/sbom/mod.rs` — if SBOM ingestion/re-ingestion creates or replaces `sbom_advisory` links (verify during implementation), invalidate that SBOM's summary cache entry
- `modules/ingestor/src/service/mod.rs` — wire the cache invalidation handle into `IngestorService` so the graph modules can call it
- `tests/api/advisory.rs` — add an integration test that ingests a new advisory for an SBOM and asserts the summary reflects it immediately

## Implementation Notes
- Use the invalidation entry point exposed by Task 2 in `modules/fundamental/src/sbom/endpoints/mod.rs` (or wherever Task 2 places it). Do not build a second cache.
- Collect the distinct set of SBOM IDs touched during a correlation run and invalidate each once, after the DB transaction commits (invalidating before commit can let a concurrent request repopulate the cache with pre-commit data).
- Writer enumeration: the known writers of `entity/src/sbom_advisory.rs` rows are advisory correlation in `modules/ingestor/src/graph/advisory/mod.rs` and possibly SBOM ingestion in `modules/ingestor/src/graph/sbom/mod.rs`. Grep for every insert/delete on the `sbom_advisory` entity across the workspace (`modules/`, `server/`) and add invalidation at each site. If a writer is found outside these files, add it to this task and flag it on the Jira task before implementing.
- Fail-closed: if invalidation fails (e.g., cache handle unavailable), log an error and surface it — do not silently swallow the error and leave stale data served for up to 5 minutes without any signal.
- Error handling: `Result<_, AppError>` with `.context(...)` (`common/src/error.rs`).
- Constraints (docs/constraints.md): §2 Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer; §3 PR with `--base main`, link posted to Jira; §5 scope to listed files, inspect before modifying, trace the full data flow (ingest → link → invalidate → next read).

## Reuse Candidates
- `modules/ingestor/src/service/mod.rs::IngestorService` — existing ingestion orchestration; inject the invalidation handle here
- `modules/ingestor/src/graph/advisory/mod.rs` — existing correlate step that writes SBOM-advisory links
- `entity/src/sbom_advisory.rs` — the join entity whose writes trigger invalidation

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the next `GET /api/v2/sbom/{id}/advisory-summary` reflects the new count without waiting for cache expiry
- [ ] Invalidation runs for every SBOM affected by a correlation run, and only after the DB transaction commits
- [ ] Every code path that writes `sbom_advisory` rows (advisory correlation, and SBOM ingestion if it writes links) triggers invalidation
- [ ] Invalidation failures are logged as errors and not silently ignored
- [ ] Unaffected SBOMs keep their cache entries

## Test Requirements
- [ ] Integration test: fetch summary (populates cache), ingest a new critical advisory linked to the SBOM, fetch again — `critical` and `total` increase by 1
- [ ] Integration test: ingesting an advisory for SBOM A does not change the cached summary for SBOM B
- [ ] If SBOM ingestion writes advisory links: integration test that re-ingesting the SBOM refreshes its summary

## Verification Commands
- `cargo test --test api advisory` — advisory integration tests, including the new invalidation test, pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
