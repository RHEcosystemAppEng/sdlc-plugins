## Repository
trustify-backend

## Target Branch
main

## Description
Establish a measurable performance baseline for the search endpoint before any optimization work. TC-9002 states that "search is slow" and that it "should be fast enough", but provides no latency figures, no target, and no description of which queries are slow. This task adds tracing instrumentation and a repeatable timing harness for `GET /api/v2/search`, so the optimization work in Task 2 can be measured against real numbers, and so the Product Owner can set a concrete latency target (an open question on TC-9002).

**Assumption (needs confirmation):** "slow" means end-to-end latency of `GET /api/v2/search` as experienced through the REST API. No other slow surface (for example, the SBOM/advisory list endpoints or ingestion) is named in the Feature.

## Files to Modify
- `modules/search/src/service/mod.rs` — add `tracing` spans around `SearchService` query building, database execution, and result mapping so each phase's latency is visible
- `modules/search/src/endpoints/mod.rs` — add a request-level span on the `GET /api/v2/search` handler that records query string length, result count, and elapsed time
- `tests/api/search.rs` — add a seeded-dataset timing test that runs a fixed set of representative queries and records their latency

## Implementation Notes
- `SearchService` in `modules/search/src/service/mod.rs` runs full-text search across entities. Instrument it in its existing location and do not restructure it in this task.
- Put spans on the separate phases (query build, DB execute, mapping to response) so Task 2 can see where the time goes.
- The timing test in `tests/api/search.rs` must follow the existing integration-test pattern (a real PostgreSQL test database, `assert_eq!(resp.status(), StatusCode::OK)`). Seed enough SBOM, advisory, and package rows (through the existing ingestion paths in `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs`, or through direct entity inserts using `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`) for timings to mean something.
- Representative query set (assumed, because the Feature does not list the slow queries): exact identifier match (e.g. a CVE ID), partial name match, a common term that matches many rows, and a term that matches nothing.
- The timing test records and prints the baseline. It must not assert an absolute latency threshold, because TC-9002 defines no target yet. Once the Product Owner sets a target, Task 2 turns it into an assertion.
- Per CONVENTIONS.md §Error Handling: any new code paths in handlers must keep returning `Result<T, AppError>` and wrap fallible calls with `.context()`. See `common/src/error.rs` for `AppError`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests run against the real PostgreSQL test database and assert status with `assert_eq!(resp.status(), StatusCode::OK)`. See `tests/api/sbom.rs` for the established pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §2.1–2.3 (commit footer references the Jira task, Conventional Commits, `Assisted-by:` trailer); §3.1–3.3 (branch named after the Jira task, PR link posted to Jira, `gh pr create --base main`); §5.1–5.4 (stay within the listed files, inspect before modifying, follow the referenced patterns, no duplicated functionality).

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests. Extend this file rather than creating a new test module.
- `tests/api/sbom.rs`, `tests/api/advisory.rs` — existing data-seeding and request patterns to copy for the timing dataset.

## Acceptance Criteria
- [ ] `GET /api/v2/search` emits a request-level tracing span that records elapsed time and result count
- [ ] `SearchService` emits separate spans for query building, database execution, and result mapping
- [ ] A repeatable timing test exists in `tests/api/search.rs` that runs the representative query set against a seeded dataset and reports per-query latency
- [ ] Baseline latency numbers for the representative query set are recorded in the PR description so they can be used to set the TC-9002 latency target
- [ ] Existing search behaviour (response shape, status codes, result set) is unchanged

## Test Requirements
- [ ] Existing tests in `tests/api/search.rs` still pass unchanged
- [ ] The new timing test runs each representative query (exact match, partial match, broad term, no-match) and asserts `StatusCode::OK` for each
- [ ] The new timing test asserts that the no-match query returns an empty result set with a 200 status (not an error)

## Verification Commands
- `cargo test --test api search` — all search integration tests pass, and the timing test prints per-query latency

## Dependencies
- None
