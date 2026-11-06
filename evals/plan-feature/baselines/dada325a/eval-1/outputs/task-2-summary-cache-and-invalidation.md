## Repository
trustify-backend

## Target Branch
main

## Description
Cache `GET /api/v2/sbom/{id}/advisory-summary` responses for 5 minutes using the existing cache infrastructure, and invalidate an SBOM's cached summary whenever the advisory ingestion pipeline links new advisories to that SBOM (TC-9001 MVP requirement "Response is cached for 5 minutes" and NFR "Cache invalidation"). Caching and invalidation ship together in this task so `main` never serves a summary that is stale for up to 5 minutes after new advisories are correlated.

The cached summary is a shared artifact. It has one consumer (the advisory-summary endpoint) and one or more producers (every code path that adds or replaces `sbom_advisory` rows). Invalidation must cover every producer path, not just the primary advisory ingestion path.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — apply the existing cache configuration to the advisory-summary route with a 5-minute TTL, keyed per SBOM ID
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — read through the cache before calling `SbomService`, and populate the cache on a miss (file created in Task 1)
- `modules/fundamental/src/sbom/service/sbom.rs` — expose a per-SBOM invalidation entry point (e.g., `invalidate_advisory_summary(sbom_id)`) on the shared cache handle
- `modules/ingestor/src/graph/advisory/mod.rs` — after correlating an advisory and writing `sbom_advisory` rows, invalidate the cached summary for **every** SBOM ID that gained a link (primary producer)
- `modules/ingestor/src/graph/sbom/mod.rs` — producer to verify: if SBOM ingestion or re-ingestion creates, replaces, or deletes `sbom_advisory` rows for an SBOM ID, invalidate that SBOM's summary here as well
- `modules/ingestor/src/service/mod.rs` — `IngestorService` entry points (scheduled and on-demand/API ingestion). Pass the shared cache handle down so every ingestion path reaches the invalidation call.
- `server/src/main.rs` — create a single shared cache instance and pass it to both the fundamental (SBOM endpoints) module and the ingestor module
- `tests/api/sbom.rs` — integration tests for caching and invalidation

## Implementation Notes
- **Check the existing cache infrastructure first**: the repository uses `tower-http` caching middleware configured in endpoint route builders. Inspect the existing route builders in `modules/fundamental/src/*/endpoints/mod.rs` to see what that middleware actually provides:
  - If it is an **in-process response cache with keyed eviction**, reuse it. Set a 300s TTL on the advisory-summary route and evict by request path `/api/v2/sbom/{id}/advisory-summary`.
  - If it only emits **HTTP `Cache-Control` headers** (client/proxy caching), the server cannot invalidate copies held by clients or proxies after ingestion, so the invalidation NFR cannot be met with headers alone. In that case, keep a server-side TTL cache of `AdvisorySeveritySummary` keyed by SBOM ID inside `SbomService` (reusing an existing cache crate already in `Cargo.lock` if there is one). Do not set long-lived `Cache-Control: max-age` on this route. **Get user confirmation before adding a new crate dependency.**
- **Shared handle placement**: `modules/ingestor` must not depend on `modules/fundamental`. Put the invalidation handle in a crate both modules already depend on (`common`), or reuse an existing shared-state type if `server/src/main.rs` already passes one to both modules. Wire the handle through `server/src/main.rs`.
- **Producer coverage (shared-artifact trace)**:
  - Primary: `modules/ingestor/src/graph/advisory/mod.rs` (advisory parse/store/correlate). Invalidate for each SBOM ID touched by correlation, after the database write commits. Invalidating before the commit lets a concurrent request repopulate the cache with pre-commit data.
  - Verify: `modules/ingestor/src/graph/sbom/mod.rs` (SBOM parse/store/link packages). The analyzed structure says this path links packages, not advisories. Confirm whether it ever writes or deletes `sbom_advisory` rows (for example, correlating a newly ingested SBOM against already-known advisories, or replacing an existing SBOM). If it does, add invalidation there. If it does not, record that in the PR description.
  - Entry points: `modules/ingestor/src/service/mod.rs` (`IngestorService`). Make sure scheduled/background and on-demand/API-triggered ingestion all go through the graph functions that invalidate. No path may write `sbom_advisory` while bypassing invalidation.
- **Fail-closed invalidation**: invalidation must never be a silent no-op. Do not wrap it in `let _ =` or `.ok()`, and do not skip it when the cache handle is not configured. If invalidation cannot run (handle missing, or eviction returns an error), the ingestion function in `modules/ingestor/src/graph/advisory/mod.rs` must return an error through the existing `AppError`/`.context()` chain, or at minimum log at `error!` level and fail the ingestion result. A successful ingestion must never leave a stale cached summary behind.
- **Cache key correctness**: the key must include the SBOM ID. Task 3 adds a `threshold` query parameter and will extend the key with it. Design the key so that invalidating one SBOM evicts all of that SBOM's variants (for example, a key prefix per SBOM, or invalidating the whole per-SBOM entry).
- **404 responses must not be cached**: caching a 404 would keep returning 404 for an SBOM that has since been ingested.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder for the advisory-summary route. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder (`endpoints/mod.rs`) scope. Example: the existing cache configuration in the route builders under `modules/fundamental/src/*/endpoints/mod.rs`.
- Per CONVENTIONS.md §Error handling: invalidation failures propagate as `AppError` with `.context()` instead of being swallowed. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust (`.rs`) scope. Example: the `.context()` usage in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` against the PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` scope. Example: the existing tests in `tests/api/sbom.rs`.
- **Constraints (docs/constraints.md)**:
  - §1.4/§1.5/§1.6: keep changes to this task's scope, inspect code before changing it, and ask for clarification when this description is incomplete (for example, when the cache infrastructure turns out to be header-only).
  - §2.1–§2.3: Conventional Commits message, a Jira ID footer, and an `Assisted-by:` trailer.
  - §3.1–§3.3: branch named after the task's Jira ID, PR link posted on the Jira task, and `gh pr create --base main`.
  - §5.1–§5.14: change only the listed files, reuse the existing cache infrastructure, trace the full lifecycle (ingest → link → invalidate → next GET recomputes), and match sibling modules on error handling and logging.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder where `tower-http` cache configuration lives
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — host for the summary computation added in Task 1, and for the invalidation entry point
- `modules/ingestor/src/graph/advisory/mod.rs` — existing correlate step that writes `sbom_advisory`. Hook invalidation in here rather than adding a separate listener.
- `common/src/error.rs::AppError` — error propagation for invalidation failures

## Acceptance Criteria
- [ ] A second `GET /api/v2/sbom/{id}/advisory-summary` within 5 minutes is served from cache, with no aggregation query executed
- [ ] Cached entries expire after 5 minutes (300s TTL)
- [ ] After advisory ingestion (`modules/ingestor/src/graph/advisory/mod.rs`) links a new advisory to an SBOM, the next summary request for that SBOM returns updated counts immediately, without waiting for the TTL
- [ ] Every SBOM that gains a link in one correlation run is invalidated, not only the first one
- [ ] If SBOM ingestion (`modules/ingestor/src/graph/sbom/mod.rs`) writes or deletes `sbom_advisory` rows, it also invalidates that SBOM's summary. The PR records whether this path writes those rows.
- [ ] Scheduled and on-demand/API ingestion entry points in `modules/ingestor/src/service/mod.rs` both trigger invalidation
- [ ] Invalidating one SBOM does not evict other SBOMs' cached summaries
- [ ] Fail-closed: if invalidation cannot be performed, ingestion reports an error. It does not report success while leaving a stale cached summary.
- [ ] 404 responses for unknown SBOM IDs are not cached

## Test Requirements
- [ ] Integration test: two consecutive summary requests return identical results, and the second is a cache hit (assert through a query counter, a cache-hit metric, or cache inspection)
- [ ] Integration test: request the summary (populating the cache), ingest a new advisory correlated to the SBOM through the advisory ingestion path, request again, and assert the counts increased
- [ ] Integration test: an advisory correlated to two SBOMs invalidates both cached summaries
- [ ] Integration test: ingestion triggered through the on-demand/API `IngestorService` path also invalidates the summary
- [ ] Integration test (conditional): if SBOM re-ingestion modifies `sbom_advisory`, re-ingesting an SBOM refreshes its summary
- [ ] Integration test (fail-closed): with the cache handle missing or invalidation forced to fail, advisory ingestion returns an error instead of succeeding silently
- [ ] Integration test: a 404 for an unknown ID is not cached. After the SBOM is ingested, the endpoint returns 200.
- [ ] Unit or integration test: the TTL is 300 seconds (assert the configured value, or use a controllable clock)

## Verification Commands
- `cargo test --test api sbom` — all SBOM integration tests pass, including the caching and invalidation tests
- `cargo build --workspace` — the workspace compiles with the shared cache handle wired through `server/src/main.rs`

## Dependencies
- Depends on: Task 1 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
