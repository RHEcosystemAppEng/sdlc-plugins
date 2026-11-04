## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` domain module in `modules/fundamental` and implement the
`GET /api/v2/remediation/summary` endpoint. The endpoint returns portfolio-wide
remediation counts grouped by severity (Critical/High/Medium/Low) × status
(Open/In Progress/Resolved), computed on the fly from existing vulnerability/advisory
and SBOM relationship data (no new database tables). This is the data source for the
summary cards and progress chart on the `/remediation` dashboard (TC-9006, UC-1).

Parent Epic: TC-9006: trustify-backend

## Files to Modify
- `modules/fundamental/src/lib.rs` — declare and export the new `remediation` module
- `server/src/main.rs` — mount the remediation routes alongside the existing modules

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root (re-exports model/service/endpoints)
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` response struct (per-severity × per-status counts plus totals)
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `summary()` aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` — integration tests for remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `{ total: { open, in_progress, resolved }, by_severity: [{ severity: "critical"|"high"|"medium"|"low", open, in_progress, resolved }] }`

## Implementation Notes
- Follow the existing domain module layout used by `modules/fundamental/src/advisory/` (`model/` + `service/` + `endpoints/`). Mirror `advisory/endpoints/mod.rs` for route registration and `advisory/service/advisory.rs` for the service struct shape.
- Compute aggregations with a single grouped SQL query (SeaORM `select_only()` + `column_as(..count..)` + `group_by(severity, status)`) joining `entity/src/sbom_advisory.rs` (SBOM–Advisory join) with `entity/src/advisory.rs`. Severity is available on advisories (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`). Do not load rows into memory and count in Rust — the NFR requires p95 < 500ms at 10,000 tracked vulnerabilities.
- Verify at implementation time where remediation status (Open/In Progress/Resolved) is persisted — expected on the `sbom_advisory` join entity. If no status column exists, stop and raise it on TC-9006: the feature forbids new tables, so a schema change needs explicit approval.
- Always return all four severities and all three statuses (zero-filled) so the frontend never has to handle missing keys.
- Return `Result<Json<RemediationSummary>, AppError>` using `AppError` from `common/src/error.rs` with `.context()` wrapping on DB errors.
- Per CONVENTIONS.md §Module pattern: create the remediation domain as `model/ + service/ + endpoints/` under `modules/fundamental/src/remediation/`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope. Example: `modules/fundamental/src/advisory/`.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register routes in `remediation/endpoints/mod.rs` and mount them in `server/src/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's endpoint registration scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching in the remediation route builder (short TTL, e.g. 60s) to help meet the p95 target. Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint route builder scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test DB using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/` scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task in the footer, and include `--trailer="Assisted-by: Claude Code"`; §3 PR `--base main`, link PR on the Jira task; §5 keep changes scoped to listed files, inspect code before modifying, reuse existing helpers, compare against sibling modules for parity.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field/enum; reuse the severity type instead of defining a new one
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — pattern for DB-backed service struct and query construction
- `common/src/db/query.rs` — shared filtering helpers; reuse for any query filters
- `common/src/error.rs::AppError` — standard handler error type
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity, the source of per-SBOM vulnerability correlation

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with counts for every severity (Critical/High/Medium/Low) × status (Open/In Progress/Resolved) combination, zero-filled when there is no data
- [ ] Totals equal the sum of the per-severity counts
- [ ] Aggregation is computed from existing tables; no new migrations or tables are added
- [ ] The aggregation runs as a grouped SQL query (no in-memory counting of all rows)
- [ ] Routes are mounted in `server/src/main.rs` and reachable under `/api/v2/remediation`
- [ ] When the database query fails, the endpoint returns an error response via `AppError` instead of an empty or all-zero summary

## Test Requirements
- [ ] Integration test: seeded SBOMs/advisories across several severities and statuses produce the expected count matrix
- [ ] Integration test: empty database returns 200 with all counts zero and all severity/status keys present
- [ ] Integration test: the same advisory correlated with two SBOMs is counted per the documented counting rule (per SBOM–advisory pair) consistently
- [ ] Integration test: a DB failure path yields a non-2xx error response rather than a 200 with zeros

## Verification Commands
- `cargo test -p tests remediation` — all remediation integration tests pass
- `curl -s localhost:8080/api/v2/remediation/summary | jq .` — returns the severity × status matrix

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/summary` to the API endpoint list

## Dependencies
- None
