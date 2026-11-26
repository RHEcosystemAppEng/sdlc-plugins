# Task 2 — Add remediation module and GET /api/v2/remediation/summary endpoint

**Summary:** Add remediation module and GET /api/v2/remediation/summary aggregation endpoint
**Parent Epic:** TC-9006: trustify-backend (Epic group "trustify-backend")

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add a new `remediation` domain module to `modules/fundamental` and implement `GET /api/v2/remediation/summary`. The endpoint returns vulnerability counts across all ingested SBOMs, grouped by severity (Critical/High/Medium/Low) × remediation status (Open/In Progress/Resolved). It feeds the summary cards and the progress chart on the new `/remediation` dashboard (TC-9006, requirement 1, UC-1).

The aggregation must be computed from existing vulnerability and SBOM relationship data (`entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`, `entity/src/sbom.rs`). No new database tables or migrations (NFR).

## Files to Modify
- `modules/fundamental/src/lib.rs` — declare and export the new `remediation` module
- `server/src/main.rs` — mount the remediation routes next to the existing sbom/advisory/package modules

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — module root (`model`, `service`, `endpoints`)
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary`, `SeverityStatusCounts` response structs (serde `Serialize`)
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `summary()` aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` — integration tests for the remediation endpoints

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated counts by severity × status, e.g.
  `{ "totals": { "open": u64, "in_progress": u64, "resolved": u64 }, "by_severity": [ { "severity": "critical"|"high"|"medium"|"low", "open": u64, "in_progress": u64, "resolved": u64 } ] }`

## Implementation Notes
- Follow the existing domain module layout `model/ + service/ + endpoints/` used by `modules/fundamental/src/advisory/` (`advisory/model/summary.rs`, `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`).
- Register routes in `modules/fundamental/src/remediation/endpoints/mod.rs` the same way `modules/fundamental/src/sbom/endpoints/mod.rs` registers `/api/v2/sbom`, then mount the module in `server/src/main.rs`.
- Severity comes from the `severity` field already on `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`) / the advisory entity (`entity/src/advisory.rs`). The SBOM↔vulnerability relationship is `entity/src/sbom_advisory.rs`.
- Remediation status (Open / In Progress / Resolved) is not a documented field in the existing entities. Before you implement, check `entity/src/sbom_advisory.rs` for a status or remediation column. If none exists, stop and ask for clarification on TC-9006: the NFR rules out new tables, so the status source must be agreed first (see the impact map "Open questions").
- Do the aggregation in the database (`GROUP BY severity, status` via SeaORM select with `.group_by()` / `.column_as(count)`), not in Rust memory, to meet the p95 < 500ms target with up to 10,000 tracked vulnerabilities. Reuse the filtering helpers in `common/src/db/query.rs` where they apply.
- All four severities and all three statuses must appear in the response even when the count is 0, so the frontend renders stable cards.
- Handlers return `Result<Json<RemediationSummary>, AppError>` and wrap fallible calls with `.context()` (`common/src/error.rs`).
- If caching is applied, configure it in the route builder like the existing endpoints that use `tower-http` caching middleware. A short TTL is fine; correctness after new ingestion takes priority.
- Per CONVENTIONS.md §Module pattern: build the new module as `model/ + service/ + endpoints/`. Applies: task modifies `modules/fundamental/src/remediation/service/mod.rs` matching the convention's Rust domain-module (`modules/*/src/<domain>/`) scope. Example: `modules/fundamental/src/advisory/`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and use `.context()` wrapping. Applies: task modifies `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs` and mount them in `server/src/main.rs`. Applies: task modifies `server/src/main.rs` matching the convention's route-mounting (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: write integration tests in `tests/api/` against the PostgreSQL test DB and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's integration-test (`tests/api/*.rs`) scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §2.1–2.3 (commit must reference TC Jira ID in footer, Conventional Commits, `Assisted-by:` trailer); §3.3 (`gh pr create --base TC-9006`); §5.1–5.8 (scope to listed files, inspect before modifying, follow referenced patterns, no duplication, trace data flow, sibling parity); §1.4–1.6 (implement-task scope rules).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering/sorting helpers; reuse for any severity filters
- `common/src/error.rs::AppError` — standard handler error type
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory queries and severity access; reuse joins instead of rewriting them
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity representation; reuse its severity enum/type for the response
- `entity/src/sbom_advisory.rs` — SBOM–advisory join entity to aggregate over

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with counts grouped by severity (Critical/High/Medium/Low) × status (Open/In Progress/Resolved)
- [ ] Totals for open, in-progress, and resolved equal the sum of the per-severity counts
- [ ] Every severity/status combination is present in the response, with zero counts where there is no data
- [ ] Aggregation uses existing tables only; no new migration in `migration/`
- [ ] The remediation module follows the `model/ + service/ + endpoints/` structure and is mounted in `server/src/main.rs`
- [ ] p95 response time < 500ms with a dataset of 10,000 tracked vulnerabilities

## Test Requirements
- [ ] Integration test: an empty database returns 200 with all counts = 0 and all severities/statuses present
- [ ] Integration test: seeded SBOMs/advisories across several severities and statuses return the expected per-cell counts and totals
- [ ] Integration test: a vulnerability that affects multiple SBOMs is counted per the agreed counting rule (per vulnerability vs per SBOM–vulnerability pair, see Open questions) and is not silently double-counted
- [ ] Performance check (test or benchmark) with 10,000 seeded vulnerabilities confirms p95 < 500ms

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass
- `curl -s http://localhost:8080/api/v2/remediation/summary | jq .` — returns the severity × status structure

## Documentation Updates
- `README.md` — add `/api/v2/remediation/summary` to the API endpoint overview (Task 8 covers the full documentation)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
