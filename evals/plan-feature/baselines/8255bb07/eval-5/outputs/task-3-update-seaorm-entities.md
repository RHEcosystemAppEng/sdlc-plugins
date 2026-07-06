## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status migration. The `advisory` entity must use the new `advisory_status_enum` column instead of the `status_id` foreign key, and the `advisory_status` entity must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- Replace `status_id: i32` column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` -- Remove the `advisory_status` module registration

## Implementation Notes
- Define an `AdvisoryStatusEnum` Rust enum with `#[derive(EnumIter, DeriveActiveEnum)]` and map it to the PostgreSQL `advisory_status_enum` type using SeaORM's `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute
- Each variant should be annotated with `#[sea_orm(string_value = "New")]` etc. to match the PostgreSQL enum values exactly
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum
- Remove or update any `Related<advisory_status::Entity>` impl on the advisory entity
- Delete `entity/src/advisory_status.rs` -- the module reference in `entity/src/lib.rs` must also be removed
- Reference the existing entity pattern in `entity/src/sbom.rs` for SeaORM entity structure conventions

Per CONVENTIONS.md §Framework: use SeaORM `DeriveActiveEnum` for enum column mapping.
Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.

## Reuse Candidates
- `entity/src/sbom.rs` -- Existing SeaORM entity demonstrating the project's entity structure and derive macros

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] The advisory entity's `Column` enum has a `Status` variant instead of `StatusId`
- [ ] The `advisory_status` entity file is removed and no longer registered in `entity/src/lib.rs`
- [ ] The advisory entity compiles without errors after the changes
- [ ] No remaining references to `advisory_status` in the entity crate

## Test Requirements
- [ ] Verify the advisory entity compiles with `cargo check -p entity`
- [ ] Verify the `AdvisoryStatusEnum` correctly maps to the PostgreSQL enum type
- [ ] Verify no orphaned imports or references to the removed `advisory_status` entity

## Verification Commands
- `cargo check -p entity` -- entity crate compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
