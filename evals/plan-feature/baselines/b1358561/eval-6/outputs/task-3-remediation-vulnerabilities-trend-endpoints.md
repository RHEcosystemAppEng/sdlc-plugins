**Summary:** Add filterable remediation vulnerability list and 30-day trend endpoints
**Parent Epic:** TC-9101 (TC-9006: trustify-backend)
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Major | **fixVersions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
The TC-9006 dashboard needs (a) a filterable, sortable table of vulnerabilities with remediation status and (b) a progress chart showing the remediation trend over the past 30 days. Neither is served by the summary/by-product endpoints. Add two endpoints under `/api/v2/remediation`, computed from existing vulnerability/SBOM relationship data (no new tables):

- `GET /api/v2/remediation/vulnerabilities` — paginated list filterable by severity, product, and status, sortable by severity.
- `GET /api/v2/remediation/trend?days=30` — daily counts of Open / In Progress / Resolved for the requested window.

## Files to Modify
- `modules/fundamental/src/remediation/model/mod.rs` — export new model types
- `modules/fundamental/src/remediation/service/remediation.rs` — add `list_vulnerabilities(filters, paginated)` and `trend(days)` methods
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the two new routes
- `tests/api/remediation.rs` — add integration tests for the new endpoints

## Files to Create
- `modules/fundamental/src/remediation/model/vulnerability.rs` — `RemediationVulnerability` struct (`advisory_id`, `identifier`, `title`, `severity`, `status`, `product_name`, `sbom_id`)
- `modules/fundamental/src/remediation/model/trend.rs` — `RemediationTrend` / `TrendPoint` (`date`, `open`, `in_progress`, `resolved`)
- `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` — list handler
- `modules/fundamental/src/remediation/endpoints/trend.rs` — trend handler

## API Changes
- `GET /api/v2/remediation/vulnerabilities?severity=&product=&status=&sort=&offset=&limit=` — NEW: returns `PaginatedResults<RemediationVulnerability>`
- `GET /api/v2/remediation/trend?days=30` — NEW: returns `{ points: [{ date, open, in_progress, resolved }] }` (one point per day, `days` defaults to 30, capped at 90)

## Implementation Notes
- Implement filtering, sorting and pagination with the shared helpers in `common/src/db/query.rs` (the same helpers used by `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`). Severity sort must use severity rank order (Critical > High > Medium > Low), not alphabetical.
- Query joins: `entity/src/sbom_advisory.rs` -> `entity/src/advisory.rs` (severity) and `entity/src/sbom.rs` (product). Reuse the join/status logic introduced in Task 1's `RemediationService` rather than duplicating it.
- Trend computation: derive daily status counts from existing timestamps on the correlation/advisory data. Verify at implementation time that a status-change or resolution timestamp exists; if historical status cannot be reconstructed without a new table, stop and raise with the Feature owner (NFR forbids new tables) — do not fabricate data.
- Validate query params: unknown `severity`/`status` values return 400 via `AppError` rather than silently returning an empty list.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` for filter, sort and pagination parameters.
  Applies: task modifies `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust list-query `.rs` scope.
- Per CONVENTIONS.md §Response types: the vulnerability list returns `PaginatedResults<RemediationVulnerability>`.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` matching the convention's Rust list endpoint `.rs` scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()`.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/trend.rs` matching the convention's Rust handler `.rs` scope.
- Per CONVENTIONS.md §Testing: extend `tests/api/remediation.rs` with `assert_eq!(resp.status(), StatusCode::OK)` style tests; follow `tests/api/sbom.rs`.
  Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules (§5.14: filter at the query level, not in memory).

## Reuse Candidates
- `common/src/db/query.rs` — filtering, pagination, sorting helpers
- `modules/fundamental/src/advisory/endpoints/list.rs` — filterable list endpoint pattern
- `modules/fundamental/src/remediation/service/remediation.rs::RemediationService` (Task 1) — shared join and status logic

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/vulnerabilities` returns `PaginatedResults<RemediationVulnerability>` and supports `severity`, `product`, `status` filters individually and combined
- [ ] Sorting by severity orders Critical > High > Medium > Low
- [ ] Invalid filter values return 400, not an empty 200
- [ ] `GET /api/v2/remediation/trend` returns one point per day for the last 30 days by default, with Open/In Progress/Resolved counts
- [ ] Both routes are registered in `modules/fundamental/src/remediation/endpoints/mod.rs`
- [ ] No database migration or new entity is introduced

## Test Requirements
- [ ] Integration test: each filter (severity, product, status) narrows results correctly; combined filters intersect
- [ ] Integration test: severity sort order is rank-based
- [ ] Integration test: invalid `status` value returns 400
- [ ] Integration test: trend returns 30 points by default with correct counts for seeded data, and `days` parameter is honored and capped

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass

## Documentation Updates
- `README.md` — add the vulnerability list and trend endpoints to the API overview (if endpoints are enumerated)

## Dependencies
- Depends on: Task 1 — Add remediation domain module with summary and per-product aggregation service
- Depends on: Task 2 — Add GET /api/v2/remediation/summary and /api/v2/remediation/by-product endpoints
