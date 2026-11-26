## Repository
trustify-backend

## Target Branch
main

## Description
Add `GET /api/v2/remediation/trend` returning daily Open / In Progress / Resolved counts over a time window (default 30 days) to back the dashboard progress chart for TC-9006 (Requirement: "chart shows trend over time"; UC-1 step 3: "Progress chart shows remediation trend over the past 30 days"). The Feature forbids new database tables, so the trend must be derived from timestamps already present on existing advisory / SBOM-advisory data.

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the trend route
- `modules/fundamental/src/remediation/service/mod.rs` — add `RemediationService::trend(days)`
- `modules/fundamental/src/remediation/model/mod.rs` — re-export trend model
- `tests/api/remediation.rs` — add trend integration tests
- `README.md` — document the trend endpoint

## Files to Create
- `modules/fundamental/src/remediation/model/trend.rs` — `RemediationTrend { points: Vec<TrendPoint> }`, `TrendPoint { date, open, in_progress, resolved }`
- `modules/fundamental/src/remediation/endpoints/trend.rs` — trend handler

## API Changes
- `GET /api/v2/remediation/trend` — NEW: query params `days` (optional, default 30, max 365), `product` (optional). Response `RemediationTrend`: `{ points: [{ date: "YYYY-MM-DD", open: number, in_progress: number, resolved: number }] }` — one point per day, oldest first, no gaps.

## Implementation Notes
- Inspect `entity/sbom_advisory.rs` and `entity/advisory.rs` at implementation time for creation / status-change timestamps. Use `generate_series` over the date window and count vulnerabilities whose state on each day was open / in progress / resolved.
- If the existing entities do not carry the timestamps needed to reconstruct historical status, do not add a table (forbidden by the Feature NFRs). Stop and raise the gap on TC-9006 so the product owner can decide (for example, a trend based only on first-seen / resolved dates).
- The endpoint must not "succeed" with a flat or empty series when the history can't be computed: return an explicit error (`AppError`) instead of an all-zero series that hides missing data.
- Reuse the product filter derivation from Task 1's `RemediationService`.
- Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()`.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/trend.rs` matching the convention's Rust (`.rs`) handler scope.
- Per CONVENTIONS.md §Endpoint registration: register in `modules/fundamental/src/remediation/endpoints/mod.rs`.
  Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's Rust endpoint-registration scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` with `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/*.rs` integration-test scope.
- Constraints (docs/constraints.md): §5.1, §5.2, §5.4, §2.1–2.3, §3.3 PR `--base main`.

## Reuse Candidates
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` — status/product derivation from Task 1
- `common/src/error.rs::AppError` — error responses

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/trend` returns 200 with exactly `days` points (default 30), ordered oldest first
- [ ] Counts on each day reflect the status of vulnerabilities on that day
- [ ] `product` filter restricts the series to that product
- [ ] `days` outside 1–365 returns 400
- [ ] No new tables or migrations are introduced

## Test Requirements
- [ ] Integration test: seeded data with status changes on known dates produces the expected per-day counts
- [ ] Integration test: default window returns 30 points with no gaps
- [ ] Integration test: invalid `days` returns 400
- [ ] Integration test: product filter

## Verification Commands
- `cargo test --test api remediation` — trend tests pass

## Documentation Updates
- `README.md` — add `GET /api/v2/remediation/trend`

## Dependencies
- Depends on: Task 1 — Remediation aggregation model and service
- Depends on: Task 2 — Remediation summary and by-product endpoints (creates `endpoints/mod.rs` and `tests/api/remediation.rs`)
