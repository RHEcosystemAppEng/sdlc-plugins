## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory API endpoints to use the new enum-based status from the updated service layer. The response shape (status as a string) remains unchanged for API consumers, so this is an internal implementation update with no external API contract changes.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update list handler to pass status filter as enum value; remove any join-related query logic for status
- `modules/fundamental/src/advisory/endpoints/get.rs` — update get handler to use status from enum column via the updated service layer
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any status-related query parameter types change (e.g., status filter parameter type)

## Implementation Notes
- Per CONVENTIONS.md §Error Handling: all endpoint handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's response type scope.
- Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes; verify route registration is consistent after any parameter type changes.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/mod.rs` matching the convention's endpoint registration scope.
- See `modules/fundamental/src/sbom/endpoints/list.rs` for the standard list endpoint pattern using `PaginatedResults`
- The API response shape must remain identical (status is returned as a string) — the enum's `Serialize` implementation handles the conversion transparently
- Remove any `use entity::advisory_status` imports from endpoint files

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint implementation following the standard pattern with PaginatedResults
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper used by all list endpoints

## Acceptance Criteria
- [ ] Advisory list endpoint returns status as a string (same format as before the migration)
- [ ] Advisory get endpoint returns status as a string (same format as before the migration)
- [ ] Status filter query parameter works correctly with enum values
- [ ] No references to `advisory_status` entity remain in endpoint code
- [ ] API response shape is unchanged (backward compatible for consumers)

## Test Requirements
- [ ] Endpoint handlers compile without errors
- [ ] List endpoint returns advisories with correct status strings
- [ ] Status filter query parameter correctly filters by enum value

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model layer (endpoints depend on updated service)
