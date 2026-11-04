**Summary**: Invalidate cached advisory summaries on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
TC-9001 requires that the advisory ingestion pipeline invalidate cached advisory summaries when new advisories are linked to an SBOM, so the 5-minute cache introduced in Task 2 does not serve stale severity counts after correlation. When advisory correlation writes `sbom_advisory` rows, evict the cached summary for every affected SBOM ID.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after correlation persists new `sbom_advisory` links, invalidate the advisory-summary cache entry for each affected SBOM ID
- `modules/ingestor/src/service/mod.rs` — wire the cache handle into `IngestorService` so the advisory graph step can reach it (only if not already available)
- `tests/api/advisory.rs` — integration test covering ingestion → invalidation

## Implementation Notes
- Hook point: the correlate step in `modules/ingestor/src/graph/advisory/mod.rs` is the code path that links advisories to SBOMs. Collect the distinct set of SBOM IDs touched by the newly inserted links and call the invalidation entry point added in Task 2 (`invalidate_advisory_summary(sbom_id)`) for each, **after** the DB transaction commits (invalidating before commit allows a concurrent request to re-cache the old value).
- Fail-closed: invalidation failure must not be swallowed silently. If eviction errors, log at warn/error with the SBOM ID and surface it via the ingestion result (`.context(...)`), rather than reporting a clean success while stale data remains cached.
- Only invalidate when links were actually added; if correlation produced zero new links, do nothing.
- Scope note: `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion) is **not** in scope — no evidence it writes `sbom_advisory`. Whether SBOM re-ingestion / advisory severity updates must also invalidate is an open question on the TC-9001 impact map; do not extend scope without confirmation.
- Per repository Key Conventions §Error handling: `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust service/handler scope.
- Per repository Key Conventions §Testing: integration tests in `tests/api/` against the real PostgreSQL test DB. Applies: task modifies `tests/api/advisory.rs` matching the convention's integration-test scope. Example: existing tests in `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to listed files; §5.2 inspect the correlation code first; §5.6 trace the full lifecycle ingestion → `sbom_advisory` write → cache eviction → endpoint read; §2.1–2.3 commit rules; §3.1–3.3 PR rules (`--base main`).

## Reuse Candidates
- Cache invalidation entry point from Task 2 (`modules/fundamental/src/sbom/endpoints/mod.rs` / cache infrastructure) — call it; do not create a second cache
- `modules/ingestor/src/service/mod.rs::IngestorService` — existing dependency wiring pattern

## Acceptance Criteria
- [ ] Ingesting an advisory that is correlated to an SBOM evicts that SBOM's cached advisory summary
- [ ] All SBOMs affected by a single ingestion are invalidated, not just the first
- [ ] Eviction occurs after the correlation transaction commits
- [ ] Ingestion that adds no new SBOM links performs no invalidation
- [ ] An invalidation failure is logged and surfaced (not a silent success)

## Test Requirements
- [ ] Integration test: request summary (cached) → ingest an advisory correlated to the SBOM → request summary again within 5 minutes → counts include the new advisory
- [ ] Integration test: an advisory correlated to two SBOMs invalidates both cached summaries
- [ ] Test: ingestion with no new links leaves the cached summary untouched
- [ ] Test: simulated eviction failure is reported in the ingestion result/logs

## Verification Commands
- `cargo test --test api advisory` — new and existing advisory tests pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
