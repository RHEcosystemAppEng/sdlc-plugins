# Task 4 — Update advisory service and model to use enum status column

**Priority:** High
**Fix Versions:** RHTPA 2.0.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, simplifying the query logic and reducing p95 latency on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` to source status from the enum column instead of joined table; remove any `advisory_status` join logic in the `From` or construction impl
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update any status-related type re-exports or helper functions
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from `fetch`, `list`, and `search` query methods; update status filtering to use `WHERE advisory.status = ?` instead of join-based filtering

## Implementation Notes
- In `AdvisoryService` query methods, replace patterns like:
  ```rust
  .join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())
  .filter(advisory_status::Column::Name.eq(status_filter))
  ```
  with direct enum column filtering:
  ```rust
  .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- The `AdvisorySummary` and `AdvisoryDetails` structs should expose status as a string (matching the current API response shape) by converting the enum to a string during serialization. The response shape must remain identical to avoid breaking API consumers.
- Use `common/src/db/query.rs` for shared query builder helpers — the existing filtering and pagination patterns should work with the enum column without modification
- Per CONVENTIONS.md Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping (Error handling convention). Follow the query helper patterns in `common/src/db/query.rs` for filtering and pagination.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for enum-column filtering
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service method patterns (`fetch`, `list`) without join-based status lookups
- `modules/fundamental/src/sbom/model/summary.rs` — reference for model struct patterns without join-dependent fields

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] Status filtering works directly on the `advisory.status` enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` expose status as a string in serialized output (API response shape unchanged)
- [ ] The advisory module compiles without errors

## Test Requirements
- [ ] Verify the fundamental module compiles (`cargo check -p fundamental`)
- [ ] Verify advisory list query returns correct results with status filter using enum column
- [ ] Verify advisory detail query returns correct status string in response

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5
