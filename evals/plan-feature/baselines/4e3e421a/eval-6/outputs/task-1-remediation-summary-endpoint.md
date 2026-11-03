## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` domain module in `modules/fundamental` and implement the `GET /api/v2/remediation/summary` endpoint, which returns portfolio-wide remediation counts grouped by severity (Critical/High/Medium/Low) and by remediation status (Open/In Progress/Resolved). This is the backend foundation for the TC-9006 remediation tracking dashboard (UC-1: View remediation summary). Aggregations must be computed from existing vulnerability/advisory and SBOM relationship data; no new database tables may be introduced.

## Files to Modify
- `modules/fundamental/src/lib.rs` — declare and export the new `remediation` module
- `server/src/main.rs` — mount the remediation module's routes alongside the existing sbom/advisory/package modules

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root wiring `model`, `service`, `endpoints`
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` and `SeverityStatusCounts` response structs (serde `Serialize`)
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with a `summary()` aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` — integration tests for the remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated counts by severity × status. Response shape:
  `{ "total": number, "by_status": { "open": number, "in_progress": number, "resolved": number }, "by_severity": [ { "severity": "critical" | "high" | "medium" | "low", "open": number, "in_progress": number, "resolved": number, "total": number } ] }`

## Implementation Notes
- Follow the established domain module layout (`model/ + service/ + endpoints/`) used by `modules/fundamental/src/advisory/` — mirror `advisory/mod.rs`, `advisory/service/advisory.rs` (`AdvisoryService`) and `advisory/endpoints/mod.rs` for route registration.
- Compute aggregations with a single grouped SQL query (SeaORM `select_only()` + `group_by` / `column_as` with `COUNT`) joining `entity/src/sbom_advisory.rs` (SBOM–Advisory join) with `entity/src/advisory.rs` (severity source). Avoid loading rows into memory and counting in Rust — the NFR requires p95 < 500ms with up to 10,000 tracked vulnerabilities.
- Severity comes from the advisory's severity field (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`). Always emit all four severity buckets (zero-filled) so the frontend gets a stable shape.
- Remediation status (Open / In Progress / Resolved) is not an explicit column in the listed entities. Derive it from existing `sbom_advisory` correlation data and confirm the derivation rule with the feature owner before implementing (see impact map "Open questions"). Encapsulate the derivation in one function in `RemediationService` so tasks 2 and 3 reuse it.
- No migration: the NFR forbids new tables, so do not add files under `migration/`.
- Handlers return `Result<Json<RemediationSummary>, AppError>` using `.context()` wrapping per `common/src/error.rs` (`AppError`).
- Register the route in `remediation/endpoints/mod.rs` and mount it in `server/src/main.rs` the same way the advisory module is mounted. Consider configuring `tower-http` caching on the summary route builder (short TTL) to help meet the p95 target.
- Per CONVENTIONS.md §Module pattern: create the new domain under `model/`, `service/`, `endpoints/` subdirectories. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope. Example: `modules/fundamental/src/advisory/`.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register routes in the module's `endpoints/mod.rs` and mount the module in `server/src/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's endpoint registration scope. Example: `modules/fundamental/src/advisory/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` against the PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/` scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): commits follow Conventional Commits, reference the Jira task in the footer, and include `--trailer="Assisted-by: Claude Code"` (§2.1–2.3); open the PR with `--base main` and post the PR link on the Jira task (§3.2–3.3); keep changes scoped to listed files, inspect code before modifying, reuse existing helpers (§5.1–5.4).

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory query service; reuse its severity access and query patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — holds the `severity` field used for grouping
- `entity/src/sbom_advisory.rs` — SBOM–Advisory join entity; the source relation for aggregation
- `common/src/db/query.rs` — shared query builder helpers (filtering) to reuse instead of hand-rolled SQL fragments
- `common/src/error.rs::AppError` — standard error type for handlers

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns HTTP 200 with the documented JSON shape
- [ ] Response always contains four severity buckets (critical, high, medium, low), zero-filled where no data exists
- [ ] `by_status` totals equal the sum of the corresponding per-severity counts, and `total` equals open + in_progress + resolved
- [ ] With an empty database the endpoint returns 200 with all counts equal to 0 (not an error, not a missing field)
- [ ] Aggregation is executed in the database (grouped query); no new tables or migrations are added
- [ ] Route is mounted in `server/src/main.rs` and reachable from the running server

## Test Requirements
- [ ] Integration test in `tests/api/remediation.rs`: seed SBOMs, advisories of mixed severities, and SBOM–advisory links; assert per-severity and per-status counts match the seeded data
- [ ] Integration test: empty database returns 200 with zero-filled buckets
- [ ] Integration test: totals are consistent (`total` = sum of `by_status`, sum of `by_severity[*].total` = `total`)
- [ ] Unit test for the status-derivation function in `RemediationService` covering each status value

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass
- `curl -s http://localhost:8080/api/v2/remediation/summary | jq .` — returns the summary JSON with four severity buckets

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/summary` to the API endpoint overview
