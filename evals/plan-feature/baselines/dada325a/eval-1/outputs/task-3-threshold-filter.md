## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `threshold` query parameter to `GET /api/v2/sbom/{id}/advisory-summary` so alerting integrations can ask only for severities at or above a given level (TC-9001 requirement "Support optional `?threshold=critical` query param", non-MVP; use case UC-2). For example, `?threshold=critical` returns only the critical count, and the integration alerts when `critical > 0`. Without the parameter, the endpoint behaves exactly as delivered in Task 1.

This requirement is **non-MVP**. It can be scheduled after the MVP tasks or deferred without affecting them.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — accept and validate an optional `threshold` query parameter (`critical` | `high` | `medium` | `low`), and return 400 for any other value
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — let severity fields below the threshold be omitted from the serialized response (e.g., `Option<u64>` with `#[serde(skip_serializing_if = "Option::is_none")]`)
- `modules/fundamental/src/sbom/service/sbom.rs` — apply the threshold to the computed counts and compute `total` over the included levels
- `modules/fundamental/src/sbom/endpoints/mod.rs` — include `threshold` in the cache key for the advisory-summary route
- `tests/api/sbom.rs` — integration tests for threshold filtering

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={critical|high|medium|low}` — MODIFY: new optional query parameter. When present, the response contains only the severity levels at or above the threshold, and `total` is their sum. An invalid value returns 400. Without the parameter, the response is unchanged.

## Implementation Notes
- **Semantics** (flagged in the impact map for confirmation): "filter counts above a severity" is read as *at or above*, because UC-2 expects `?threshold=critical` to return the critical count. Ordering is critical > high > medium > low. So `threshold=high` returns `critical`, `high`, and `total = critical + high`.
- **Parsing**: use Axum's `Query<T>` extractor with a `#[serde(rename_all = "lowercase")]` enum for the severity levels. If `modules/fundamental/src/advisory/model/summary.rs` already defines a severity type, reuse it instead of creating a new enum. Return `AppError`'s bad-request variant (`common/src/error.rs`) for unknown values. Unknown values must **not** be ignored. Silently ignoring an invalid threshold would return unfiltered counts, and an alerting integration with a typo would then alert on the wrong data.
- **Cache key**: Task 2 keys the cache per SBOM. Extend the key with the normalized threshold value so filtered and unfiltered responses never collide. Per-SBOM invalidation from Task 2 must still evict every threshold variant for that SBOM.
- **Backward compatibility**: when `threshold` is absent, the JSON must stay byte-for-byte compatible with Task 1's response: all four fields, plus `total` over all distinct advisories.
- Per CONVENTIONS.md §Error handling: return `Result<_, AppError>` and map invalid query values to a client error through `AppError`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Query helpers: if `common/src/db/query.rs` already parses filter query parameters, reuse it instead of hand-rolling parsing. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust query/service (`.rs`) scope. Example: the query parameter handling in `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Caching: the cache configuration in the route builder must vary by the `threshold` query parameter. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder (`endpoints/mod.rs`) scope. Example: the cache configuration added to `modules/fundamental/src/sbom/endpoints/mod.rs` in Task 2.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` scope. Example: the existing tests in `tests/api/sbom.rs`.
- **Constraints (docs/constraints.md)**:
  - §1.4/§1.5/§1.6: keep changes to this task's scope, inspect code before changing it, and ask for clarification when this description is incomplete.
  - §2.1–§2.3: Conventional Commits message, a Jira ID footer, and an `Assisted-by:` trailer.
  - §3.1–§3.3: branch named after the task's Jira ID, PR link posted on the Jira task, and `gh pr create --base main`.
  - §5.1–§5.14: change only the listed files, reuse the existing severity type and query helpers, and use parameterized tests for the threshold matrix if sibling tests already use that pattern.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing severity field and type. Reuse it for threshold parsing and ordering.
- `common/src/db/query.rs` — shared filtering helpers for query parameters
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing example of query parameter extraction in the SBOM module

## Acceptance Criteria
- [ ] `?threshold=critical` returns only `critical` and `total` (equal to the critical count)
- [ ] `?threshold=high` returns `critical`, `high`, and `total = critical + high`; `medium` and `low` work the same way
- [ ] Threshold values are case-insensitive or documented as lowercase-only, consistently with existing query parameters
- [ ] An invalid `threshold` value (e.g., `?threshold=urgent`) returns 400. It does not return unfiltered counts.
- [ ] Without `threshold`, the response is identical to Task 1's response
- [ ] Filtered and unfiltered responses are cached under different keys, and per-SBOM invalidation evicts all variants
- [ ] An unknown SBOM ID with a valid threshold still returns 404

## Test Requirements
- [ ] Integration test: for each threshold value, the returned fields and `total` match the expected subset
- [ ] Integration test (fail-closed): an invalid threshold returns 400, and the test asserts the body is not a summary
- [ ] Integration test: request `?threshold=critical`, then the unfiltered endpoint, and assert the second response is not served from the first's cache entry
- [ ] Integration test: after ingesting a new critical advisory, `?threshold=critical` reflects the new count (invalidation covers threshold variants)
- [ ] Integration test: no `threshold` returns all five fields, unchanged from Task 1

## Verification Commands
- `cargo test --test api sbom` — all SBOM integration tests pass, including the threshold tests
- `curl -s 'http://localhost:8080/api/v2/sbom/<existing-id>/advisory-summary?threshold=critical'` — returns only `critical` and `total`

## Dependencies
- Depends on: Task 1 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 2 — Cache advisory summary for 5 minutes with ingestion-driven invalidation
