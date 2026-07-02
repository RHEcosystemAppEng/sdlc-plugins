## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the SearchService query execution path in `modules/search/src/service/mod.rs`
to improve search response times. The current full-text search across entities is
reported as slow (see Ambiguity 1 in the impact map — no specific performance targets).
This task focuses on query-level optimizations: reducing unnecessary joins, leveraging
the indexes added in Task 1, and applying the shared query helper patterns from
`common/src/db/query.rs`.

**Assumption (pending clarification):** Without specific performance metrics, this task
focuses on structural query optimizations (eliminating N+1 queries, reducing join
breadth, applying pagination early). The product owner should provide target latency
SLAs so performance can be validated against concrete thresholds.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize full-text search query construction: reduce join scope, apply pagination earlier in the query pipeline, leverage database indexes from Task 1

## Implementation Notes
- Inspect the current SearchService implementation in `modules/search/src/service/mod.rs`
  to understand the existing query patterns before making changes.
- Use the shared query builder helpers in `common/src/db/query.rs` for filtering,
  pagination, and sorting. These helpers already implement efficient pagination patterns
  (see the `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs`).
- Check for N+1 query patterns: if the SearchService fetches entities individually after
  a search query, refactor to use batch fetching or JOIN-based loading.
- Apply pagination at the database level (LIMIT/OFFSET) before entity hydration, not after
  fetching all results.
- Consider using `common/src/db/limiter.rs` connection pool limiter to prevent search
  queries from saturating the connection pool.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the
  error handling convention (see `common/src/error.rs`).
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to files
  listed here; inspect code before modifying.

**Conventions (from Key Conventions):**

Per Key Conventions §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs`.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.

Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; use these instead of implementing custom query logic
- `common/src/db/limiter.rs` — Connection pool limiter to prevent search queries from monopolizing connections
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper for consistent pagination

## Acceptance Criteria
- [ ] SearchService queries use efficient JOIN patterns (no N+1 queries)
- [ ] Pagination is applied at the database level before entity hydration
- [ ] Shared query helpers from `common/src/db/query.rs` are used where applicable
- [ ] Error handling follows `Result<T, AppError>` with `.context()` pattern
- [ ] Existing search API contract (GET /api/v2/search) is preserved — no breaking changes

## Test Requirements
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass
- [ ] Add a test that verifies search returns results within reasonable time for a dataset with multiple entities (verify query completes, not specific latency)

## Verification Commands
- `cargo test --test search` — All search integration tests pass

## Dependencies
- Depends on: Task 1 — Add search performance indexes (indexes should exist for optimized queries to leverage)

## additional_fields
- priority: Normal
- fixVersions: ["RHTPA 1.6.0"]
- labels: ["ai-generated-jira"]
---

[sdlc-workflow] Description digest: sha256-md:3a6aa1435aa7891a0967aee2e400e2a9b79dcfce69a48ec2f151534288c6f92f
