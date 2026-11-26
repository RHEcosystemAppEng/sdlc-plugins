## Repository
trustify-backend

## Target Branch
main

## Description
Invalidate cached advisory-summary responses whenever new advisories are linked to an SBOM, so `GET /api/v2/sbom/{id}/advisory-summary` never serves stale counts for up to 5 minutes after correlation (TC-9001 NFR: "advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM"). The cached summary is a shared artifact derived from the `sbom_advisory` join table; every ingestion path that writes rows to that table must invalidate the cache entry for the affected SBOM ID(s).

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after advisory correlation persists new `sbom_advisory` links, invalidate the advisory-summary cache entry for each affected SBOM ID
- `modules/ingestor/src/graph/sbom/mod.rs` — if SBOM ingestion/re-ingestion writes `sbom_advisory` links for an existing SBOM ID, invalidate that SBOM's cache entry
- `modules/ingestor/src/service/mod.rs` — give `IngestorService` access to the shared cache handle used for invalidation
- `server/src/main.rs` — construct the cache handle once and share it between the SBOM endpoint router and the ingestor service
- `tests/api/advisory.rs` — integration test: ingesting an advisory that correlates to an SBOM refreshes that SBOM's summary immediately

## Implementation Notes
- Shared-artifact producers (writers of `entity/src/sbom_advisory.rs` rows) identified from the repository structure:
  1. `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion: parse, store, correlate (primary writer named by the Feature)
  2. `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion: parse, store, link packages (verify at implementation time whether it also creates `sbom_advisory` rows; if it does, it must invalidate too)
  Consumer: `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (Task 2). Search the codebase for any other writer of `sbom_advisory` (e.g., `grep -rn "sbom_advisory" modules/`) and include every writer found — the codebase search is authoritative.
- Invalidate only after the database transaction that writes the links commits; invalidating before commit allows a concurrent request to re-cache the old counts.
- Use the cache key helper exposed by Task 2 in `modules/fundamental/src/sbom/endpoints/mod.rs` so the key format is defined in exactly one place. Invalidate all variants for an SBOM ID (with and without the `threshold` query string from Task 4).
- The `tower-http` caching configured in the endpoint route builders must expose a programmatic invalidation handle; wire one shared instance through `server/src/main.rs` (which mounts all modules) into `IngestorService` (`modules/ingestor/src/service/mod.rs`). If the existing cache infrastructure has no invalidation API, stop and raise this with the feature owner rather than silently relying on TTL expiry.
- Fail closed on invalidation errors: an invalidation failure must not be silently swallowed. Log it with SBOM ID context and surface it (return an error from the ingestion step or mark the cache entry stale), so ingestion does not report success while leaving stale summaries.
- Per CONVENTIONS.md §Error handling: propagate invalidation failures as `AppError` with `.context()`. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust (`.rs`) handler/service scope.
- Per CONVENTIONS.md §Endpoint registration: modules are mounted in `server/src/main.rs`; share the cache handle there when building the SBOM router. Applies: task modifies `server/src/main.rs` matching the convention's route mounting scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/advisory.rs` against the real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md): Conventional Commits with Jira ID footer and `Assisted-by:` trailer (§2.1–2.3); PR with `--base main`, link posted on Jira (§3.2, §3.3); scope to listed files, trace the full data flow ingestion → join table → cache invalidation → endpoint before committing (§5.1–5.8).

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing correlation step that writes SBOM-advisory links; hook point for invalidation
- `modules/ingestor/src/service/mod.rs::IngestorService` — existing service composition where shared dependencies are injected
- `modules/fundamental/src/sbom/endpoints/mod.rs` — cache key/config introduced by Task 2
- `tests/api/advisory.rs` — existing advisory ingestion test fixtures

## Acceptance Criteria
- [ ] After an advisory is ingested and correlated to an SBOM, the next `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts (not the cached value), without waiting for the 5-minute TTL
- [ ] Invalidation happens in `modules/ingestor/src/graph/advisory/mod.rs` after the link-writing transaction commits
- [ ] Every other writer of `sbom_advisory` rows found in the codebase (including `modules/ingestor/src/graph/sbom/mod.rs` if applicable) also invalidates the affected SBOM's summary
- [ ] Only cache entries for affected SBOM IDs are invalidated; summaries for unrelated SBOMs remain cached
- [ ] An invalidation failure is logged and surfaced as an error, not silently ignored (fail closed)

## Test Requirements
- [ ] Integration test: fetch summary (cache populated) → ingest a new advisory correlated to the SBOM → fetch summary again → counts reflect the new advisory
- [ ] Integration test: ingesting an advisory for SBOM A does not invalidate the cached summary for SBOM B
- [ ] Integration test (if SBOM ingestion writes `sbom_advisory` rows): re-ingesting an SBOM that gains advisory links refreshes its summary
- [ ] Test: simulated invalidation failure causes the ingestion step to return an error / log, rather than reporting success silently

## Verification Commands
- `cargo test --test api advisory` — new and existing advisory integration tests pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
