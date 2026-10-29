## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. Replace the `status_id` foreign key field in the advisory entity with a `status` field using the `advisory_status_enum` PostgreSQL enum type. Remove the `advisory_status` entity module since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; define the `AdvisoryStatusEnum` Rust enum with SeaORM's `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` -- remove the `advisory_status` module declaration and re-export if present

## Files to Create
(none -- if `entity/src/advisory_status.rs` exists, it should be deleted rather than created)

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` using SeaORM's `DeriveActiveEnum` derive macro to map to the PostgreSQL `advisory_status_enum` type
- Place the enum definition in `entity/src/advisory.rs` alongside the Advisory entity, or in a shared types module if the project convention prefers
- Remove any `Relation::HasOne` or `Relation::BelongsTo` definition that references the advisory_status entity
- Update the `Column` enum in the advisory entity to replace `StatusId` with `Status`
- Per CONVENTIONS.md §Framework: follow SeaORM entity patterns for enum column mapping.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM database scope.
- Reference existing entity definitions (e.g., `entity/src/sbom.rs`) for the established entity structure pattern

## Reuse Candidates
- `entity/src/sbom.rs` -- existing entity demonstrating the project's SeaORM entity definition pattern (column definitions, relations)
- `entity/src/advisory.rs` -- current advisory entity to understand existing field definitions and relations

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines an `AdvisoryStatusEnum` Rust enum with variants: New, Analyzing, Fixed, Rejected
- [ ] `AdvisoryStatusEnum` uses SeaORM's `DeriveActiveEnum` to map to the `advisory_status_enum` PostgreSQL type
- [ ] The advisory entity's `Column` enum has a `Status` variant instead of `StatusId`
- [ ] All relations to `advisory_status` are removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is removed (if it exists)
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] The entity crate compiles successfully after changes

## Test Requirements
- [ ] Entity crate compiles with `cargo check -p entity`
- [ ] Verify `AdvisoryStatusEnum` correctly maps all four enum values to their PostgreSQL counterparts
- [ ] Verify the advisory entity's `Column::Status` maps to the correct database column name

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
