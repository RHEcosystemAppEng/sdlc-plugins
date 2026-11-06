<!-- Jira creation metadata (simulated; not part of the description body) -->
<!-- Summary: Add remediation module with summary aggregation endpoint | Simulated key: TC-9103 | Issue type: Task | Parent Epic: TC-9101 (TC-9006: trustify-backend) | Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0 -->

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` domain module in `modules/fundamental` and expose `GET /api/v2/remediation/summary`, which returns portfolio-wide counts of vulnerabilities grouped by severity (Critical/High/Medium/Low) × remediation status (Open/In Progress/Resolved), plus a daily trend series for the dashboard progress chart (default window: 30 days). The summary feeds the dashboard summary cards and progress chart (TC-9006, UC-1). Per the feature's non-functional requirements, aggregations MUST be computed from existing vulnerability/advisory and SBOM relationship data — no new database tables — and the endpoint must meet p95 < 500ms.

This task establishes the module skeleton (`model/` + `service/` + `endpoints/`) that Tasks 2 and 3 extend.

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new `remediation` module
- `server/src/main.rs` — mount the remediation routes alongside the existing sbom/advisory/package routes

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root (declares `model`, `service`, `endpoints`)
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary`, `SeverityStatusCount`, `RemediationTrendPoint` structs (serde `Serialize`)
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `summary(trend_days)` aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` — integration tests for remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns
  `{ totals: { open: u64, in_progress: u64, resolved: u64 }, by_severity: [{ severity: "critical"|"high"|"medium"|"low", open: u64, in_progress: u64, resolved: u64 }], trend: [{ date: "YYYY-MM-DD", open: u64, in_progress: u64, resolved: u64 }] }`.
  Optional query parameter `trend_days` (integer, default 30, max 365).

## Implementation Notes
- Follow the existing domain module layout used by `modules/fundamental/src/advisory/` (`model/summary.rs`, `service/advisory.rs`, `endpoints/mod.rs` + per-route handler files). Mirror `modules/fundamental/src/advisory/endpoints/mod.rs` for route registration and `modules/fundamental/src/advisory/endpoints/get.rs` for the handler shape.
- Data sources (existing entities only — no migration):
  - `entity/src/sbom_advisory.rs` — SBOM↔Advisory join; one row = one vulnerability occurrence in an SBOM. Remediation status must be derived from this relationship.
  - `entity/src/advisory.rs` — advisory entity; severity is surfaced on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` (reuse the same severity mapping, do not redefine severity levels).
  - `entity/src/sbom.rs` — SBOM entity.
- **Verify before implementing:** confirm which column on `sbom_advisory` (or related entity) carries the remediation status (Open/In Progress/Resolved) and which timestamp column(s) allow a per-day trend to be reconstructed. If no status or timestamp data exists in current entities, stop and raise with the feature owner — the NFR forbids new tables, so the trend/status source must be agreed before coding (recorded as an open question in the TC-9006 impact map).
- Compute aggregations in SQL (`GROUP BY severity, status` via SeaORM `select_only()` / `column_as()` / `group_by()`), not by loading rows into memory — required to hit p95 < 500ms at 10,000 tracked vulnerabilities. Generate the trend with a single grouped query over the date window, not one query per day.
- Error handling: handlers return `Result<Json<RemediationSummary>, AppError>` using `AppError` from `common/src/error.rs`, wrapping DB errors with `.context()`.
- Validate `trend_days` (reject `0` or `> 365` with a 400 via `AppError`).
- Empty result must be distinguishable from failure: when no correlated vulnerabilities exist return HTTP 200 with zero counts and an empty-but-dated trend; any DB/query error must surface as an error response — never fall back to a zero-filled 200 on error.
- Caching: configure `tower-http` caching on the route builder the same way existing endpoints do (see `modules/fundamental/src/advisory/endpoints/mod.rs`); keep max-age short since data changes with ingestion.
- Per CONVENTIONS.md §Module pattern: create the remediation module as `model/ + service/ + endpoints/` under `modules/fundamental/src/remediation/`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust domain module scope. Example: `modules/fundamental/src/sbom/`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from every handler and wrap fallible calls with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register routes in `modules/fundamental/src/remediation/endpoints/mod.rs` and mount them in `server/src/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's endpoint registration scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching in the remediation route builder. Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's route builder scope. Example: `modules/fundamental/src/advisory/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` against the PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration test scope. Example: `tests/api/advisory.rs`.
- Commit rules (docs/constraints.md §2): Conventional Commits format, `Implements <task-key>` footer, `Assisted-by:` trailer.
- PR rules (docs/constraints.md §3): `gh pr create --base main`; post the PR link on the Jira task.
- Code change rules (docs/constraints.md §5): stay within the files listed above; inspect code before modifying; reuse existing helpers; compare against sibling modules (advisory/sbom) for parity on error handling and caching.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — already carries the advisory severity field; reuse its severity type/mapping for the `by_severity` grouping
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory query patterns (joins, filters) to follow for the aggregation query
- `common/src/db/query.rs` — shared filtering helpers; reuse for any filter parsing rather than hand-rolling
- `common/src/error.rs::AppError` — error type for handlers
- `entity/src/sbom_advisory.rs` — existing SBOM↔Advisory relationship used as the aggregation base

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns HTTP 200 with `totals`, `by_severity` (one entry per Critical/High/Medium/Low), and `trend` fields as specified in API Changes
- [ ] Counts are grouped by severity × status (Open/In Progress/Resolved) and `totals` equals the sum across severities
- [ ] `trend` contains one entry per day for the requested `trend_days` window (default 30)
- [ ] Invalid `trend_days` (0, negative, > 365, non-integer) returns HTTP 400
- [ ] No new database tables or migrations are introduced
- [ ] Aggregation is executed as grouped SQL queries (no full-row loading into memory)
- [ ] With no correlated vulnerabilities, the endpoint returns 200 with zero counts; a database error returns an error response, not a zero-filled 200
- [ ] Remediation routes are registered in `modules/fundamental/src/remediation/endpoints/mod.rs` and mounted in `server/src/main.rs`

## Test Requirements
- [ ] Integration test: seed SBOMs/advisories with known severity/status mix and assert exact `by_severity` and `totals` counts
- [ ] Integration test: empty database returns 200 with all-zero counts and a 30-entry trend
- [ ] Integration test: `trend_days=7` returns exactly 7 trend entries
- [ ] Integration test: `trend_days=0` and `trend_days=1000` return 400
- [ ] Integration test: a forced query failure path (e.g., service error) surfaces as an error status, not a 200 with zero counts
- [ ] Performance check: summary over a seeded dataset of 10,000 vulnerability occurrences completes within the p95 < 500ms budget

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass
- `curl -s localhost:8080/api/v2/remediation/summary | jq '.totals'` — returns open/in_progress/resolved counts

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/summary` to the API endpoint overview (path, parameters, response shape)

## Dependencies
- None
