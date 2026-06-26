# Task 5 — Update advisory endpoints for enum-based status filtering

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to work with the new enum-based status column. The list endpoint's status filter query parameter must parse directly to `AdvisoryStatusEnum` values. The get endpoint must return the status from the enum column. The route registration must remove any advisory_status-related sub-routes if they exist.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the status filter query parameter parsing to use `AdvisoryStatusEnum` instead of looking up an ID from the status table; pass the enum value directly to the service layer
- `modules/fundamental/src/advisory/endpoints/get.rs` — ensure the detail response maps the enum status to a string (should flow from model changes in Task 4, but verify the endpoint handler does not reference advisory_status)
- `modules/fundamental/src/advisory/endpoints/mod.rs` — remove any route registrations related to the advisory_status table (e.g., a `/api/v2/advisory-status` listing endpoint if one exists)

## Implementation Notes
The list endpoint in `modules/fundamental/src/advisory/endpoints/list.rs` likely accepts a query parameter for status filtering. Update the deserialization to parse the string directly into `AdvisoryStatusEnum`:

```rust
#[derive(Deserialize)]
pub struct ListQuery {
    pub status: Option<AdvisoryStatusEnum>,
    // ... other fields
}
```

SeaORM's `DeriveActiveEnum` provides `FromStr` / deserialization support, so Axum's query parameter extraction should work directly with the enum type.

Follow the endpoint registration pattern in `modules/fundamental/src/advisory/endpoints/mod.rs` — routes are registered here and mounted by `server/src/main.rs`.

Per CONVENTIONS.md §Error Handling: handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed
- [ ] `GET /api/v2/advisory/{id}` returns the status as a string in the response body
- [ ] No references to `advisory_status` entity remain in the endpoints module
- [ ] API response shape is identical to the pre-migration format

## Test Requirements
- [ ] `cargo build -p fundamental` compiles successfully with endpoint changes
- [ ] Status filter query parameter accepts all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Invalid status values return an appropriate error response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and models to use enum column

[sdlc-workflow] Description digest: sha256-md:e0a4b7c56f9d1382a5c8e3f64d7b2a15c6f9e8d34a0b5c7293f1d4e6b8a0c3d2
