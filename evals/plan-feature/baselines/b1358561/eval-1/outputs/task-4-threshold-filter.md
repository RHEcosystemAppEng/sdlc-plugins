Summary: Support optional ?threshold query parameter on advisory-summary
Epic: TC-9001: Advisory severity summary endpoint
Labels: ai-generated-jira | Priority: Major | Fix Version: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Non-MVP requirement of TC-9001 for alerting integrations (UC-2): support an optional
`?threshold=<severity>` query parameter on `GET /api/v2/sbom/{id}/advisory-summary` that
limits counts to severities at or above the given level. For example,
`?threshold=critical` returns only the critical count. To keep the response shape stable for
clients, severities below the threshold are returned as `0` and `total` is the sum of the
included severities. Without the parameter, behavior is unchanged.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — accept and validate the optional `threshold` query parameter
- `modules/fundamental/src/sbom/service/sbom.rs` — apply the threshold to `advisory_severity_summary`
- `tests/api/sbom.rs` — integration tests for threshold filtering

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — MODIFY: add optional query param `threshold` (`critical` | `high` | `medium` | `low`, case-insensitive); counts below threshold are `0`, `total` sums included severities; invalid value returns 400

## Implementation Notes
- Parse with an Axum `Query<...>` struct holding `threshold: Option<Severity>` (serde enum, lowercase), following query extraction in `modules/fundamental/src/sbom/endpoints/list.rs`.
- Order: critical > high > medium > low. Implement threshold inclusion once on the severity enum (e.g., `fn at_or_above(&self, threshold)`), reusing the severity mapping introduced in Task 1.
- Invalid threshold value must return 400 (`AppError` bad request in `common/src/error.rs`) — never fall back to unfiltered counts, which would make an alerting integration silently receive the wrong numbers.
- Caching: the cache key must include the threshold (or cache only the unfiltered summary and apply the threshold after cache lookup — preferred, since it keeps Task 3 invalidation per-SBOM). Ensure invalidation from Task 3 still covers thresholded responses.
- Per CONVENTIONS.md §Query helpers: reuse filtering helpers in `common/src/db/query.rs` if the threshold is applied at query level. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs`) scope.
- Per CONVENTIONS.md §Error handling: invalid parameters are returned as `AppError` from a `Result`-returning handler. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: tests in `tests/api/sbom.rs` with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md):
  - §1.4/§5.1 — scope limited to the files listed above.
  - §1.5/§5.2 — inspect Task 1/Task 2 code before modifying.
  - §5.9/§5.10 — parameterize per-threshold tests only if sibling tests use parameterization.
  - §5.11–5.13 — doc comments on new tests; given-when-then for non-trivial tests.
  - §2.1–2.3 — Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
  - §3.1–3.3 — branch named after the task key; `gh pr create --base main`; post PR link to Jira.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing query parameter extraction pattern
- `common/src/db/query.rs` — shared filtering helpers
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — summary model from Task 1

## Acceptance Criteria
- [ ] Without `threshold`, response is identical to Task 2 behavior
- [ ] `?threshold=critical` returns only the critical count (others `0`, `total` = critical)
- [ ] `?threshold=high` includes critical and high; `?threshold=medium` includes critical, high, medium; `?threshold=low` includes all
- [ ] Invalid `threshold` value returns 400, not unfiltered counts (fail-closed)
- [ ] Unknown SBOM ID still returns 404 when `threshold` is supplied
- [ ] Cached responses never return the wrong filter's counts

## Test Requirements
- [ ] Integration test for each threshold value against a mixed-severity SBOM
- [ ] Integration test: invalid threshold (e.g., `?threshold=urgent`) returns 400
- [ ] Integration test: unfiltered and `?threshold=critical` requests in sequence each return correct counts (cache isolation)
- [ ] Integration test: unknown SBOM with threshold returns 404

## Verification Commands
- `curl -s 'http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical'` — only `critical` non-zero, `total` equals `critical`

## Documentation Updates
- REST API reference — document the `threshold` parameter (covered by Task 5)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
