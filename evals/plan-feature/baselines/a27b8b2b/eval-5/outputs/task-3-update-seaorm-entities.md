## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Modify the `advisory` entity to replace the `status_id` integer FK field with a `status` field using a Rust enum that maps to the `advisory_status_enum` PostgreSQL type. Remove the `advisory_status` entity module entirely since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module export.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column definition with `status: AdvisoryStatusEnum` column using SeaORM's `DeriveActiveEnum` macro; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` — remove `pub mod advisory_status;` export

## Files to Create
- None (the enum can be defined within `entity/src/advisory.rs` or in a shared types file if the project uses one)

## Implementation Notes
- Define the `AdvisoryStatusEnum` Rust enum using SeaORM's `DeriveActiveEnum` derive macro with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`.
- Map each variant: `#[sea_orm(string_value = "New")]`, `#[sea_orm(string_value = "Analyzing")]`, `#[sea_orm(string_value = "Fixed")]`, `#[sea_orm(string_value = "Rejected")]`.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `RelationDef` enum and the corresponding `Related<super::advisory_status::Entity>` implementation.
- Reference the existing entity pattern in `entity/src/advisory.rs` for column and relation definition style.
- The `advisory_status.rs` entity file should be deleted (Files to Create lists none; the file is being removed).

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` has a `status` column of type `AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The `Relation` to `advisory_status` is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] Verify the entity crate compiles: `cargo check -p entity`
- [ ] Verify the `AdvisoryStatusEnum` correctly maps to/from PostgreSQL `advisory_status_enum` type values
- [ ] Verify no remaining references to `advisory_status` entity in the codebase

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors
- `grep -r "advisory_status" entity/src/` — no remaining references to the old entity

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration for advisory status enum
