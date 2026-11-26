# Task 2 — Add remediation module and GET /api/v2/remediation/summary

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
Create a new `remediation` domain module in `modules/fundamental` and expose `GET /api/v2/remediation/summary`. The endpoint returns vulnerability counts for the whole portfolio, grouped by severity (Critical/High/Medium/Low) and by remediation status (Open/In Progress/Resolved). The counts are computed from existing SBOM–advisory relationship data. No new database tables may be added. This endpoint provides the dashboard summary cards and progress chart for TC-9006 (UC-1).

## Files to Modify
- `modules/fundamental/src/lib.rs` — declare the new `remediation` module
- `server/src/main.rs` — mount the remediation routes next to the sbom and advisory modules

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root (re-export model, service, endpoints)
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` and `SeverityStatusCount` response structs
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `summary()` aggregation
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` — integration tests for the remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW. Response shape:
  ```json
  {
    "total": 0,
    "by_status": { "open": 0, "in_progress": 0, "resolved": 0 },
    "by_severity": [
      { "severity": "critical", "open": 0, "in_progress": 0, "resolved": 0, "total": 0 }
    ]
  }
  ```
  `by_severity` always contains all four severities (critical, high, medium, low), even when a count is zero.

## Implementation Notes
- Follow the existing domain module layout `model/ + service/ + endpoints/`, using `modules/fundamental/src/advisory/` as the reference: `advisory/endpoints/mod.rs` for route registration and `advisory/service/advisory.rs::AdvisoryService` for the service structure.
- Compute the aggregation in the database with a single `GROUP BY severity, status` query over `entity/src/sbom_advisory.rs` joined to `entity/src/advisory.rs`. Do not load rows into memory. This keeps the p95 < 500ms NFR achievable at 10,000 tracked vulnerabilities.
- Read severity from the advisory. `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` already exposes a `severity` field, so reuse the same severity source and mapping instead of re-deriving it.
- **Open question (blocking):** confirm which existing column holds remediation status (Open/In Progress/Resolved) on `sbom_advisory` or a related existing entity. Do not add a migration or table (NFR: no new database tables). If no such column exists, stop and raise this on TC-9006 before implementing.
- Count a vulnerability as an `(sbom, advisory)` pair from `sbom_advisory`, so the same advisory affecting two SBOMs counts twice. Document this choice in the struct's doc comment so the UI and docs describe it the same way.
- Return `Result<Json<RemediationSummary>, AppError>` and wrap database errors with `.context(...)` (`common/src/error.rs::AppError`). A database or query failure must produce an error response. It must never fall back to a zero-filled summary.
- Per CONVENTIONS.md §Module pattern: build the new domain as `model/ + service/ + endpoints/`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's domain module scope. Example: `modules/fundamental/src/advisory/`.
- Per CONVENTIONS.md §Error handling: every handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's endpoint handler scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register routes in the module's `endpoints/mod.rs` and mount them in `server/src/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's route registration scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration test scope. Example: `tests/api/advisory.rs`.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder with the `tower-http` middleware. Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's route builder scope. Use a short TTL so the dashboard stays close to current correlation state.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, a Jira ID footer (`Implements <task-key>`), and an `Assisted-by:` trailer.
  - §3: the PR targets `TC-9006` (`gh pr create --base TC-9006`), and the PR link is posted to Jira.
  - §5: changes stay limited to the listed files, existing code is inspected before it is modified, and existing helpers are reused instead of duplicated.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — service structure and DB connection handling to mirror
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field and representation
- `common/src/db/query.rs` — shared query builder helpers for filters
- `common/src/error.rs::AppError` — error type for handlers
- `entity/src/sbom_advisory.rs` — SBOM–Advisory join entity, the source of truth for affected vulnerabilities

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with `total`, `by_status`, and `by_severity` as specified
- [ ] `by_severity` contains exactly the four severities Critical/High/Medium/Low, and each has open/in_progress/resolved/total counts
- [ ] The counts match the underlying `sbom_advisory` data (sum of `by_severity[*].total` == `total` == sum of `by_status`)
- [ ] The aggregation is a database-side GROUP BY query. No new tables or migrations are added
- [ ] Fail-closed behavior: a database or query failure returns an error status (5xx via `AppError`). It does not return a 200 with zero counts
- [ ] The route is mounted in `server/src/main.rs` and registered in `remediation/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test: seed SBOMs and advisories with mixed severities and statuses through the existing ingestion path, call `/api/v2/remediation/summary`, and assert the exact counts for every severity × status cell
- [ ] Integration test: with an empty database, return 200 with all counts zero and all four severities present
- [ ] Integration test: assert the totals are consistent (sum of severity totals == `total` == sum of `by_status`)
- [ ] Integration or unit test: when the service's query fails, the handler returns an error response, not a zero-filled 200

## Verification Commands
- `cargo test -p tests remediation` — all remediation tests pass
- `curl -s localhost:8080/api/v2/remediation/summary | jq .by_severity | jq length` — outputs `4`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
