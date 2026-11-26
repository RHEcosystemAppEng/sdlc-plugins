## Repository
trustify-backend

## Target Branch
main

## Description
Invalidate the cached advisory severity summary for an SBOM whenever the set of advisories linked to that SBOM changes, so `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001) never serves stale counts after new advisories are correlated. The NFR requires the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM. Because the cached summary is a shared artifact derived from the `sbom_advisory` link set, every ingestion path that writes those links must invalidate — not only the primary advisory correlation path.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after advisory correlation links advisories to SBOMs, invalidate the summary cache for each affected SBOM ID
- `modules/ingestor/src/graph/sbom/mod.rs` — on SBOM (re-)ingestion, invalidate the summary cache for the SBOM if this path creates or replaces `sbom_advisory` links
- `modules/ingestor/src/service/mod.rs` — wire the cache invalidation handle into `IngestorService` so both graph paths can reach it
- `tests/api/advisory.rs` — integration test: ingesting a new advisory for an SBOM updates the summary returned by the endpoint

## Implementation Notes
- Call the keyed invalidation entry point added in Task 2 (next to the advisory-summary cache configuration in `modules/fundamental/src/sbom/endpoints/`). Do not create a second cache or duplicate the cache-key format.
- In `modules/ingestor/src/graph/advisory/mod.rs`, collect the distinct SBOM IDs whose `sbom_advisory` rows were inserted during correlation and invalidate each once after the DB transaction commits (invalidating before commit allows a concurrent request to re-cache stale data).
- In `modules/ingestor/src/graph/sbom/mod.rs`, first confirm whether SBOM ingestion writes `entity/src/sbom_advisory.rs` rows (e.g., correlating against already-known advisories). If it does, invalidate the SBOM's summary after commit; if it provably does not, record that finding in the PR description and leave the file unchanged.
- Fail-closed: an invalidation failure must not be silently swallowed. Log it at error level and propagate it via `AppError`/`.context()` per sibling ingestion error handling. Ingestion must not report success while leaving a stale summary cached, unless the implementer documents that the 5-minute TTL is the accepted bound.
- Per CONVENTIONS.md §Error handling: propagate invalidation errors as `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust (`.rs`) handler/service scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/` scope.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task in the footer, and include an `Assisted-by:` trailer; §3 PR branch named after the Jira task ID, `gh pr create --base main`, PR link posted on the Jira task; §5 keep changes scoped to the listed files, inspect code before modifying it, trace the full data flow (ingest → link → invalidate → endpoint recompute), and keep error handling consistent between the advisory and SBOM ingestion paths.

## Reuse Candidates
- Advisory-summary cache invalidation function — added in Task 2; the only invalidation mechanism to use
- `modules/ingestor/src/service/mod.rs::IngestorService` — existing orchestration point for dependency injection into the graph ingestors
- `entity/src/sbom_advisory.rs` — join entity; its inserted rows identify which SBOM IDs to invalidate

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the next `GET /api/v2/sbom/{id}/advisory-summary` reflects the new count without waiting for the 5-minute TTL
- [ ] Each affected SBOM is invalidated once per ingestion, after the transaction commits
- [ ] SBOM re-ingestion that changes `sbom_advisory` links invalidates that SBOM's summary (or the PR documents that this path never writes those links)
- [ ] Ingestion that links nothing to an SBOM does not invalidate that SBOM's cache
- [ ] Invalidation failures are logged and propagated; they are never silently ignored

## Test Requirements
- [ ] Integration test: request the summary (populating the cache), ingest an advisory correlated to the SBOM, then request again and assert the updated count
- [ ] Integration test: ingest an advisory affecting SBOM A only; SBOM B's cached summary is not invalidated
- [ ] Integration test (if the SBOM path writes links): re-ingest an SBOM that gains an advisory link; the summary updates
- [ ] Test: an invalidation error surfaces as an ingestion error, not a silent success

## Verification Commands
- `cargo test --test api advisory` — advisory integration tests, including invalidation tests, pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
