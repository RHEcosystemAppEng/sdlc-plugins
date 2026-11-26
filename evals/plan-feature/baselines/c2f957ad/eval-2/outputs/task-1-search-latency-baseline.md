# Task 1 — Instrument search and establish a latency baseline

**Jira:** Task, parent EPIC-1 ("TC-9002: Search performance"), labels `ai-generated-jira`, priority `Normal`, fixVersions `RHTPA 1.6.0`

## Repository
trustify-backend

## Target Branch
main

## Description
TC-9002 says search is "too slow", but it gives no baseline and no target. This task adds timing instrumentation to the search request path and a repeatable way to measure `GET /api/v2/search` latency. With these in place, the optimizations in Task 2 and Task 3 can be measured, and the Feature owner can set a target based on real numbers.

**Assumptions (pending clarification on TC-9002, open questions 1 and 6):**
- No latency target exists yet. This task records a baseline and does not enforce a threshold.
- Instrumentation must not change endpoint behavior or the response shape.

## Files to Modify
- `modules/search/src/service/mod.rs` — add tracing spans with timing around `SearchService` query execution, per entity type (sbom, advisory, package)
- `modules/search/src/endpoints/mod.rs` — add a request-level tracing span for `GET /api/v2/search` that records the query, the number of results and the elapsed time
- `tests/api/search.rs` — add a baseline latency test that seeds a representative dataset and records search timings

## Implementation Notes
- `SearchService` in `modules/search/src/service/mod.rs` runs full-text search across entities. Put one span around each per-entity query so the slowest entity type shows up in the data.
- Keep handler signatures `Result<T, AppError>` (see `common/src/error.rs`). Instrumentation must not add new error paths.
- Do not log full result payloads. Log counts and durations only.
- The baseline test must **record** timings, for example by printing them or writing them as test output. It must not assert a hard latency threshold, because no target exists and timing assertions are flaky in CI. Write the measured baseline into the PR description so Task 2 can compare against it.
- Seed data through the same ingestion entry points used in production (`modules/ingestor/src/service/mod.rs` `IngestorService`). Direct table inserts would leave out the data shapes that ingestion produces (see the shared-artifact analysis in the impact map).
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping, so any new fallible call in the handler must use `.context()`. Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's Rust handler (`.rs`) scope. Example pattern: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/search.rs matching the convention's integration test (`tests/api/*.rs`) scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §1.4 and §5.1 keep changes to the listed files. §5.2 inspect code before modifying it. §5.4 do not duplicate existing helpers. §2.1–2.3 commits use Conventional Commits, reference the Jira key in the footer and include an `Assisted-by:` trailer. §3.1–3.3 branch named after the task key, PR with `--base main`, PR link posted on the Jira task. §5.11–5.12 test doc comments and given-when-then comments.

## Reuse Candidates
- `modules/ingestor/src/service/mod.rs::IngestorService` — use it to seed realistic search test data
- `tests/api/search.rs` — existing search integration tests and fixtures; extend them instead of creating a new test file

## Acceptance Criteria
- [ ] Every `GET /api/v2/search` request emits a tracing span with the total elapsed time and the number of results
- [ ] `SearchService` emits a separate timing span for each entity type queried (sbom, advisory, package)
- [ ] A baseline latency test exists in `tests/api/search.rs` and reports timings for a seeded dataset
- [ ] The measured baseline (dataset size, median and p95 per entity type) is recorded in the PR description
- [ ] Search response status, path, parameters and `PaginatedResults<T>` response shape are unchanged

## Test Requirements
- [ ] Existing tests in `tests/api/search.rs` pass unchanged (regression check for "don't break existing functionality")
- [ ] New baseline test seeds SBOM and advisory data through the ingestion path, runs a set of representative queries and reports timings without asserting a threshold
- [ ] Test confirms that a search request still returns `StatusCode::OK` with the same response body shape after instrumentation is added

## Verification Commands
- `cargo test --test api search` — all search integration tests pass and the baseline timings are printed

## Dependencies
- None
