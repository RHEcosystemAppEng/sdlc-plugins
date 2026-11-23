# Task 3 — Invalidate cached advisory summaries when advisories are linked to an SBOM

**Summary:** TC-9001: Invalidate cached SBOM advisory summaries from the ingestion pipeline
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
The feature requires that the advisory ingestion pipeline invalidate cached advisory summaries when new advisories are linked to an SBOM. Without this, `GET /api/v2/sbom/{id}/advisory-summary` can serve stale counts for up to 5 minutes after correlation.

The cached summary is a shared artifact. It is derived from the `sbom_advisory` join table, so **every** ingestion path that inserts `sbom_advisory` rows must invalidate the affected SBOM's cache entry, not only the primary advisory-correlation path. This task covers all of those writers.

Part of feature TC-9001.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after advisory correlation commits new `sbom_advisory` links, invalidate the advisory-summary cache for each affected SBOM ID
- `modules/ingestor/src/graph/sbom/mod.rs` — if SBOM ingestion also correlates the new SBOM against existing advisories (writes `sbom_advisory` rows), invalidate that SBOM's cache entry after commit
- `modules/ingestor/src/service/mod.rs` — pass the cache invalidation handle into the graph ingestion code (`IngestorService` wiring)
- `modules/ingestor/Cargo.toml` — add a dependency on the crate that exposes the invalidation function, if `ingestor` does not already depend on `fundamental`

## Implementation Notes
- Use the per-SBOM invalidation function added by Task 2 next to the cache configuration in `modules/fundamental/src/sbom/endpoints/mod.rs`. Do not reach into cache internals directly.
- Producer and consumer map for the cached summary (from the Step 3 shared-artifact analysis):
  - **Consumer / cache populator:** `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (Task 2)
  - **Writer – advisory ingestion (primary):** `modules/ingestor/src/graph/advisory/mod.rs` — "parse, store, correlate" inserts `sbom_advisory` rows
  - **Writer – SBOM ingestion:** `modules/ingestor/src/graph/sbom/mod.rs` — "parse, store, link packages". Check whether it also correlates against already-ingested advisories. If it does, it is a second writer and must invalidate.
  - **Orchestration / on-demand path:** `modules/ingestor/src/service/mod.rs` (`IngestorService`) — any re-ingest, re-correlate, or API-triggered ingest path must go through the invalidating code.
  - Before implementing, run `grep -rn "sbom_advisory" modules/ entity/` to confirm this list. Any additional writer you find (for example a deletion or unlink path) must also invalidate. Add it to this task and note it on the Jira issue.
- Ordering: invalidate **after** the DB transaction commits. If you invalidate before commit, a concurrent request can re-cache the old counts.
- **Fail-closed requirement:** an invalidation failure must not be swallowed silently. If invalidation returns an error, log it at `error` level with the SBOM ID, and either propagate it as an `AppError` or record it so the stale entry is forced to expire. Ingestion must never report success while leaving a known-stale summary cached with no signal. The guard belongs at the post-commit correlation site in `modules/ingestor/src/graph/advisory/mod.rs` (and the matching site in `graph/sbom/mod.rs`).
- Collect the distinct set of affected SBOM IDs per ingestion batch and invalidate each one once, so a large advisory batch doesn't trigger thousands of redundant invalidations.
- Per CONVENTIONS.md §Error handling: invalidation errors use `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust `.rs` handler/service scope.
- Constraints (docs/constraints.md): §5.1 scope is limited to the files above, plus any additional `sbom_advisory` writer found by the grep, which must be reported. §5.2 inspect the ingestion code before editing. §5.6 trace ingest → commit → invalidate → next GET recomputes. §5.8 keep parity between the advisory and SBOM ingestion paths. §2.1–2.3 and §3.1–3.3 apply to commits and PRs.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — per-SBOM cache invalidation function introduced by Task 2
- `modules/ingestor/src/service/mod.rs::IngestorService` — existing place to inject shared dependencies into graph ingestion
- `entity/src/sbom_advisory.rs` — join entity whose inserts define when invalidation is needed

## Acceptance Criteria
- [ ] Ingesting an advisory that correlates to an SBOM invalidates that SBOM's cached advisory summary, and the next GET returns updated counts within the same request cycle (no 5-minute wait)
- [ ] Ingesting an SBOM that correlates to existing advisories (if that path writes `sbom_advisory`) invalidates that SBOM's cached summary
- [ ] Every code path that inserts `sbom_advisory` rows (confirmed by grep) calls invalidation after commit
- [ ] Invalidation runs after the DB transaction commits
- [ ] An invalidation failure is logged at error level and is not silently ignored (fail-closed). Ingestion does not report clean success while a known-stale entry remains
- [ ] SBOMs not affected by an ingestion batch keep their cache entries

## Test Requirements
- [ ] Integration test: GET summary (cache warm), ingest a new advisory linked to the SBOM, GET again, and assert counts include the new advisory
- [ ] Integration test: same flow through the SBOM ingestion path, if it writes `sbom_advisory`
- [ ] Integration test: ingest an advisory linked to SBOM A only and assert SBOM B's cached summary is untouched
- [ ] Test: simulate an invalidation failure (inject a failing invalidator) and assert the error is surfaced or logged, not swallowed (fail-closed path)

## Verification Commands
- `cargo test -p trustify-module-ingestor` — all tests pass
- `cargo test --test api sbom::advisory_summary_invalidation` — new invalidation integration tests pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching
