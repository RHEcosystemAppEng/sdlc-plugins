**Summary**: Support optional threshold query parameter on advisory-summary (non-MVP)

## Repository
trustify-backend

## Target Branch
main

## Description
Non-MVP requirement of TC-9001 (UC-2 alerting integration): support `GET /api/v2/sbom/{id}/advisory-summary?threshold=<severity>` so external systems can poll only for severities at or above a threshold. For `threshold=critical`, only the critical count is returned. Without the parameter, behaviour is unchanged from Task 2.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — parse and validate optional `threshold` query parameter and apply it to the response
- `tests/api/sbom.rs` — integration tests for threshold handling

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — MODIFY: accepts optional `threshold` query param (`critical` | `high` | `medium` | `low`); severities below the threshold are excluded and `total` reflects only included severities. Invalid value → 400.

## Implementation Notes
- Use an Axum `Query<AdvisorySummaryParams { threshold: Option<Severity> }>` extractor in `advisory_summary.rs`; reuse the severity type from `modules/fundamental/src/advisory/model/summary.rs` for deserialization so valid values match the rest of the API.
- Semantics (planned, confirm on TC-9001): inclusive "at or above" — `threshold=high` returns critical + high. Below-threshold fields are omitted from the JSON (`#[serde(skip_serializing_if = "Option::is_none")]`) so UC-2's "only critical count is returned" holds; `total` = sum of included fields.
- Fail-closed: an unrecognised threshold value must return 400 via `AppError`, not silently fall back to the unfiltered summary (an alerting integration would otherwise act on wrong data).
- Cache key must include the threshold value (or apply filtering after the cached full summary is read) so filtered and unfiltered responses never collide. Preferred: cache the full summary per SBOM and filter in the handler, so Task 3's invalidation remains a single per-SBOM eviction.
- Per repository Key Conventions §Error handling: `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust service/handler scope.
- Per repository Key Conventions §Testing: integration tests in `tests/api/` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration-test scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to listed files; §5.2 inspect before modifying; §5.9 prefer parameterized tests for the per-threshold cases if sibling tests use them (§5.10); §2.1–2.3 commit rules; §3.1–3.3 PR rules (`--base main`).

## Reuse Candidates
- `common/src/db/query.rs` — existing query-parameter filtering helpers/patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity type for parsing

## Acceptance Criteria
- [ ] Without `threshold`, the response is identical to Task 2's
- [ ] `threshold=critical` returns only `critical` (and `total` equal to it)
- [ ] `threshold=high|medium|low` return severities at or above the threshold
- [ ] Invalid `threshold` returns 400, not an unfiltered summary
- [ ] Filtered and unfiltered responses never serve each other's cached values
- [ ] Unknown SBOM ID still returns 404 when `threshold` is supplied

## Test Requirements
- [ ] Integration test per threshold value verifying included/excluded fields and `total`
- [ ] Integration test: invalid threshold → 400
- [ ] Integration test: unfiltered then filtered request on the same SBOM returns correct distinct bodies (cache key check)
- [ ] Integration test: unknown SBOM with threshold → 404

## Verification Commands
- `curl -s 'localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical'` — body contains only `critical` and `total`

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
