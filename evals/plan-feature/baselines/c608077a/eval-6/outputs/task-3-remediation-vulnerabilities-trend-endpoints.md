## Repository
trustify-backend

## Target Branch
main

## Description
Add the supporting endpoints the TC-9006 dashboard needs beyond the two aggregation endpoints: a filterable, paginated list of tracked vulnerabilities with their remediation status (backs the "Filterable vulnerability table" MVP requirement, filters: severity, product, status) and a 30-day remediation trend series (backs the "progress chart shows trend over time" MVP requirement). Both are served from `RemediationService` (Task 1) and registered in the remediation router created in Task 2.

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the `vulnerabilities` and `trend` routes
- `tests/api/remediation.rs` — add integration tests for the new routes

## Files to Create
- `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` — `GET /api/v2/remediation/vulnerabilities` handler
- `modules/fundamental/src/remediation/endpoints/trend.rs` — `GET /api/v2/remediation/trend` handler

## API Changes
- `GET /api/v2/remediation/vulnerabilities?severity={s}&product={p}&status={st}&sort={field}&offset={n}&limit={n}` — NEW: returns `PaginatedResults<RemediationVulnerability>` (advisory id, identifier, title, severity, product, status, affected SBOM count)
- `GET /api/v2/remediation/trend?days={n}` — NEW: returns `RemediationTrendPoint[]` (date, open, in_progress, resolved); `days` defaults to 30, capped at a sane maximum (e.g. 365)

## Implementation Notes
- Use `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` as the handler pattern for query-parameter parsing, filtering, and paginated responses.
- Parse filters with the shared helpers in `common/src/db/query.rs`; reject unknown `severity` / `status` values with a 400 via `AppError` rather than silently returning an unfiltered list.
- Validate `days` (positive integer, upper bound) and return 400 on invalid input.
- Status semantics depend on the open question recorded in Task 1 / impact map (source column for remediation status and timestamps). Do not invent a new table.
- Per CONVENTIONS.md §Response types: the vulnerabilities list endpoint returns `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` matching the convention's list endpoint scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination and sorting. Applies: task modifies `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs` matching the convention's Rust query code scope. Example: `common/src/db/query.rs`.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/trend.rs` matching the convention's Rust handler `.rs` scope. Example: `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: add the routes in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint registration scope. Example: `modules/fundamental/src/advisory/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/remediation.rs` matching the convention's `tests/api/*.rs` scope. Example: `tests/api/search.rs`.
- Constraints (docs/constraints.md): §5.1 scope; §5.2 inspect before modifying; §5.4 no duplicated filtering logic; §5.8 sibling parity; §2.1–2.3 commit rules; §3.1–3.3 PR rules (`--base main`).

## Reuse Candidates
- `modules/fundamental/src/advisory/endpoints/list.rs` — filtered/paginated list handler for advisories (closest existing analogue to the vulnerability table)
- `common/src/db/query.rs` — filter/sort/pagination helpers
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/vulnerabilities` returns 200 with a paginated list; each item includes severity, product and status
- [ ] Filtering by `severity`, `product`, and `status` (individually and combined) returns only matching items
- [ ] Sorting by severity orders Critical > High > Medium > Low
- [ ] Invalid `severity`/`status` filter values return 400 instead of an unfiltered list
- [ ] `GET /api/v2/remediation/trend` returns 30 daily points by default; `days` parameter is validated

## Test Requirements
- [ ] Integration test: each filter individually and a combined filter return only matching rows
- [ ] Integration test: invalid `status=foo` returns 400
- [ ] Integration test: severity sort order is Critical, High, Medium, Low
- [ ] Integration test: `GET /api/v2/remediation/trend` returns 30 points; `days=7` returns 7; `days=0` returns 400

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass

## Documentation Updates
- `README.md` — list the `/api/v2/remediation/vulnerabilities` and `/api/v2/remediation/trend` endpoints

## Dependencies
- Depends on: Task 1 — Add remediation model and aggregation service
- Depends on: Task 2 — Add remediation summary and by-product endpoints
