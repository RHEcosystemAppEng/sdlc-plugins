Summary: Invalidate cached advisory summaries on advisory and SBOM ingestion
Epic: TC-9001: Advisory summary cache invalidation
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Per the TC-9001 NFR, the advisory ingestion pipeline must invalidate cached advisory severity
summaries when new advisories are linked to an SBOM. The cached summary (Task 2) is a shared
artifact derived from the `sbom_advisory` relationship, and repository analysis shows two
ingestion paths write that relationship: advisory ingestion/correlation and SBOM
(re-)ingestion. Both — including API-triggered (on-demand) ingestion routed through
`IngestorService` — must invalidate the affected SBOM's cache entry so consumers never see
stale counts for up to 5 minutes after new correlations.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after correlation inserts `sbom_advisory` links, invalidate the advisory-summary cache entry for every affected SBOM ID
- `modules/ingestor/src/graph/sbom/mod.rs` — after SBOM (re-)ingestion links that change the SBOM's advisory set, invalidate that SBOM's advisory-summary cache entry
- `modules/ingestor/src/service/mod.rs` — give `IngestorService` access to the advisory-summary cache handle and pass it to both graph ingestion paths
- `tests/api/sbom.rs` — integration tests that ingestion invalidates the cached summary

## Implementation Notes
- Reuse the cache key function exposed by Task 2 (in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` or wherever Task 2 placed it) — do not reconstruct the key format independently, or invalidation will silently miss.
- Advisory path: in `modules/ingestor/src/graph/advisory/mod.rs`, collect the set of SBOM IDs touched by the correlation step and invalidate each **after** the DB transaction commits (invalidating before commit lets a concurrent request repopulate the cache with pre-commit data).
- SBOM path: in `modules/ingestor/src/graph/sbom/mod.rs`, invalidate the ingested SBOM's entry after commit (re-ingesting an SBOM can change which advisories correlate to it).
- Wiring: inject the cache handle through `IngestorService` (`modules/ingestor/src/service/mod.rs`) so both paths, including API-triggered uploads that go through the service, share the same handle as the endpoint. Verify the ingestor and fundamental modules share the same cache instance at runtime (wired in `server/src/main.rs` if necessary — if so, add it to the PR and note the scope addition on the Jira task).
- Fail-closed: if the cache invalidation call returns an error, log it at error level and propagate/surface it rather than silently ignoring it; an ingestion that "succeeds" while leaving stale summaries is a silent no-op success. At minimum the ingestion must not swallow the error without logging.
- Per CONVENTIONS.md §Error handling: invalidation failures are returned as `AppError` with `.context("invalidating advisory summary cache for sbom ...")`. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust (`.rs`) handler/service scope.
- Per CONVENTIONS.md §Caching: use the same `tower-http`-based cache infrastructure configured for the endpoint rather than introducing a second cache. Applies: task modifies `modules/ingestor/src/service/mod.rs` matching the convention's cache configuration scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hitting the real PostgreSQL test DB. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/*.rs`) scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md):
  - §1.4/§5.1 — scope limited to the files listed above.
  - §1.5/§5.2 — inspect both ingestion paths and `IngestorService` before modifying.
  - §5.6 — trace ingest → link insert → commit → invalidate → next GET returns fresh data.
  - §5.8 — both ingestion paths must have parity in invalidation and error handling.
  - §5.11–5.13 — doc comments on new tests; given-when-then for non-trivial tests.
  - §2.1–2.3 — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
  - §3.1–3.3 — branch named after the task key; `gh pr create --base main`; post PR link to Jira.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — cache key function from Task 2
- `modules/ingestor/src/service/mod.rs::IngestorService` — common entry point for both ingestion paths
- `entity/src/sbom_advisory.rs` — join table whose writes trigger invalidation

## Acceptance Criteria
- [ ] Advisory ingestion that links a new advisory to an SBOM invalidates that SBOM's cached summary
- [ ] Advisory ingestion affecting multiple SBOMs invalidates every affected SBOM's entry
- [ ] SBOM re-ingestion that changes its advisory links invalidates that SBOM's cached summary
- [ ] API-triggered (on-demand) ingestion via `IngestorService` triggers the same invalidation
- [ ] Invalidation happens after the ingestion transaction commits
- [ ] Invalidation failure is logged and surfaced, not silently ignored (fail-closed)
- [ ] Cached summaries for unaffected SBOMs remain cached

## Test Requirements
- [ ] Integration test: GET summary (populates cache) → ingest advisory correlated to the SBOM → GET summary returns updated counts immediately (within the 5-minute TTL)
- [ ] Integration test: ingest advisory affecting two SBOMs → both summaries reflect the new advisory
- [ ] Integration test: GET summary → re-ingest the SBOM with changed packages → GET summary reflects the new advisory set
- [ ] Integration test: ingest advisory for SBOM A does not evict the cached summary for SBOM B
- [ ] Test: simulated invalidation failure is logged/surfaced (not swallowed)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
