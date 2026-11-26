# Task 5 — Validate remediation aggregation performance (p95 < 500ms at 10k vulnerabilities)

**Parent Epic:** TC-9006: trustify-backend (<EPIC-BE>)
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major
**fixVersions:** RHTPA 1.5.0

---

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Confirm that the remediation endpoints meet TC-9006's non-functional requirements: summary endpoint p95 < 500ms, and correct handling of up to 10,000 tracked vulnerabilities. Add a seeded large-dataset integration test. If query plans show sequential scans on the aggregation path, optimize the queries in `RemediationService`. The NFR forbids new tables, so any fix must stay within query changes and indexes on existing columns.

## Files to Modify
- `modules/fundamental/src/remediation/service/mod.rs` — query optimizations, if profiling shows they are needed
- `tests/api/remediation.rs` — add the large-dataset (10,000 vulnerability) tests

## Implementation Notes
- Seed 10,000 `sbom_advisory` rows across at least 50 products and all severity/status combinations. Reuse the seeding helpers added in Tasks 2–4 in `tests/api/remediation.rs`.
- Measure `/api/v2/remediation/summary` latency over repeated calls (for example 100 requests) and assert p95 < 500ms. Also assert that `/by-product` and `/vulnerabilities` return correct totals at this scale.
- Use `EXPLAIN ANALYZE` on the aggregation queries. If an index is needed on an existing column (for example on the `sbom_advisory` status/advisory FK columns), raise it on TC-9006 first, because this would add a migration file outside the current scope.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration test scope. Example: `tests/api/search.rs`.
- Per CONVENTIONS.md §Query helpers: keep the optimized queries on the shared `common/src/db/query.rs` helpers. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's query scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Constraints (docs/constraints.md):
  - §2: commit rules.
  - §3: the PR is created with `--base TC-9006`.
  - §5: changes stay limited to the listed files, and code is inspected before it is changed.

## Reuse Candidates
- `common/src/db/limiter.rs` — connection pool limiter. Check that concurrent dashboard calls do not exhaust the pool
- `tests/api/remediation.rs` (Tasks 2–4) — existing seed fixtures

## Acceptance Criteria
- [ ] With 10,000 seeded tracked vulnerabilities, `/api/v2/remediation/summary` p95 latency is < 500ms in the test environment
- [ ] With 10,000 vulnerabilities, `/by-product` and `/vulnerabilities` return correct totals and paginate without errors
- [ ] No new database tables are introduced

## Test Requirements
- [ ] Large-dataset integration test that asserts summary p95 < 500ms across 100 requests
- [ ] Large-dataset integration test that asserts the summary totals equal the seeded counts
- [ ] Large-dataset integration test that asserts the `/vulnerabilities` filtered `total` is correct at scale

## Verification Commands
- `cargo test -p tests remediation -- --include-ignored` — the large-dataset tests pass (mark them `#[ignore]` if they are slow and run them in CI)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product
- Depends on: Task 4 — Add GET /api/v2/remediation/vulnerabilities
