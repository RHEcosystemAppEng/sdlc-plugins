## Repository
trustify-backend

## Target Branch
main

## Description
Make sure cached advisory-summary responses (5-minute TTL, Task 2) don't go stale when new advisories are linked to an SBOM. Per the TC-9001 non-functional requirements, the advisory ingestion pipeline must invalidate the cached summary for every SBOM that gains a new advisory link. The cached summary is a shared artifact derived from the `sbom_advisory` join table, so every path that writes to `sbom_advisory` must invalidate it.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after advisory correlation links advisories to SBOMs, invalidate the cached summary for each affected SBOM ID
- `modules/ingestor/src/service/mod.rs` — thread the advisory-summary cache handle into `IngestorService` so the graph ingestion code can reach it
- `modules/ingestor/src/graph/sbom/mod.rs` — if SBOM ingestion or re-ingestion creates or removes `sbom_advisory` rows, invalidate that SBOM's cached summary (confirm during implementation; see Implementation Notes)
- `server/src/main.rs` — share a single cache instance between the SBOM endpoint route builder and the ingestor service
- `tests/api/sbom.rs` — integration test that ingestion invalidates the cached summary

## Implementation Notes
- Shared-artifact producer/consumer map (cached advisory summary, derived from `entity/src/sbom_advisory.rs`):
  - Producer: advisory ingestion/correlation in `modules/ingestor/src/graph/advisory/mod.rs` ("parse, store, correlate"). This is the primary writer of new SBOM-advisory links.
  - Possible producer: SBOM ingestion in `modules/ingestor/src/graph/sbom/mod.rs` ("parse, store, link packages"). The manifest doesn't show it writing `sbom_advisory`. Grep it for `sbom_advisory` inserts/deletes at implementation time and add invalidation if it writes there.
  - Consumer: `GET /api/v2/sbom/{id}/advisory-summary` (`modules/fundamental/src/sbom/endpoints/advisory_summary.rs`, Task 2).
- Collect the distinct affected SBOM IDs during correlation and invalidate once per SBOM after the DB transaction commits. Invalidating before commit lets a concurrent request re-cache stale data.
- Use the invalidation hook created in Task 2. Don't add a second cache implementation.
- Per CONVENTIONS.md §Error handling: invalidation helpers return `Result<T, AppError>` with `.context()` wrapping, and a failed invalidation is logged and surfaced rather than silently swallowed. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust (`.rs`) handler/service scope.
- Per CONVENTIONS.md §Testing: integration test in `tests/api/` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task ID in the footer, and include an `Assisted-by:` trailer; §3 branch is named after the task ID and the PR is opened with `--base main` with its link posted to Jira; §5 keep changes to the listed files, inspect code before modifying, reuse existing helpers rather than duplicating logic.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing correlation step where SBOM-advisory links are created (the invalidation call site)
- `modules/ingestor/src/service/mod.rs::IngestorService` — existing service wiring for dependencies
- `entity/src/sbom_advisory.rs` — join entity whose writes trigger invalidation

## Acceptance Criteria
- [ ] Ingesting an advisory that correlates to SBOM X invalidates SBOM X's cached summary, and the next request returns updated counts within the TTL window
- [ ] Only the SBOMs affected by the ingestion are invalidated; other SBOMs' cache entries are left alone
- [ ] Every code path that writes `sbom_advisory` rows (advisory correlation, plus SBOM ingestion if it writes the table) invalidates the affected SBOM's summary
- [ ] Invalidation runs after the ingestion transaction commits
- [ ] A failed invalidation is logged and surfaced as an error, not silently ignored

## Test Requirements
- [ ] Integration test: request the summary (cached), ingest a new advisory linked to the same SBOM, request again → counts include the new advisory
- [ ] Integration test: ingesting an advisory for SBOM A does not invalidate SBOM B's cached entry
- [ ] If SBOM ingestion writes `sbom_advisory`, an integration test covering re-ingestion invalidation

## Verification Commands
- `cargo test --test api sbom` — integration tests pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
