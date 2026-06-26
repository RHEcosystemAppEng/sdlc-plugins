# Task 7 — Update integration tests for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. Tests must verify that the advisory list endpoint correctly filters by enum status values, that the detail endpoint returns the status as a string, and that the search endpoint includes status in its results. Remove any test setup code that seeds the `advisory_status` lookup table.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to insert advisories with `AdvisoryStatusEnum` values instead of `status_id` foreign keys; update assertions for status filtering to use enum values; remove any `advisory_status` table seeding; add test cases for each of the four status values
- `tests/api/search.rs` — update any search tests that reference advisory status to use the new enum column; ensure search results include the status field correctly

## Implementation Notes
The existing tests in `tests/api/advisory.rs` likely seed test data by inserting rows into both `advisory` and `advisory_status` tables. Update the seeding to insert advisories with the `status` enum column directly:

```rust
let advisory = advisory::ActiveModel {
    status: Set(AdvisoryStatusEnum::Fixed),
    // ... other fields
};
```

Follow the existing test pattern using `assert_eq!(resp.status(), StatusCode::OK)` from `tests/api/advisory.rs`.

Use the `PaginatedResults<AdvisorySummary>` response type from `common/src/model/paginated.rs` for deserializing list endpoint responses in assertions.

Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test data seeding uses `AdvisoryStatusEnum` values directly (no lookup table seeding)
- [ ] Status filter tests cover all four enum values: New, Analyzing, Fixed, Rejected
- [ ] No references to `advisory_status` entity remain in test code
- [ ] Search tests continue to pass with advisory status in results

## Test Requirements
- [ ] `cargo test --test api` passes all advisory and search tests
- [ ] Each of the four status filter values is tested explicitly
- [ ] Edge case: filtering by a status with no matching advisories returns an empty list

## Verification Commands
- `cargo test --test api -- advisory` — all advisory tests pass
- `cargo test --test api -- search` — all search tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory endpoints for enum-based status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum values directly

[sdlc-workflow] Description digest: sha256-md:a2c6d9e78b1f3504c7e0a5b86f9d4c37e8b1a0f56c2d7e9415b3f6a8d0c2e5f4
