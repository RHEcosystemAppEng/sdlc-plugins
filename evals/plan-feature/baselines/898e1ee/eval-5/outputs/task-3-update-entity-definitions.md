## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new schema after the advisory status migration. Replace the `status_id` foreign key field in the advisory entity with a `status` field of type `advisory_status_enum`. Define the Rust enum mapping for the PostgreSQL enum type. Remove the `advisory_status` entity file since the lookup table no longer exists, and remove its re-export from the entity lib.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the Relation to AdvisoryStatus; add DeriveActiveEnum mapping for the PostgreSQL enum type
- `entity/src/lib.rs` -- remove `pub mod advisory_status;` re-export and any references to the deleted entity

## Files to Create
- None (the enum is defined inline in `entity/src/advisory.rs`)

## Implementation Notes
- In `entity/src/advisory.rs`, define an `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected`, deriving `DeriveActiveEnum` with the `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute.
- Replace the `status_id` column definition (`pub status_id: i32`) with `pub status: AdvisoryStatusEnum`.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its corresponding `RelationTrait` implementation that references `entity::advisory_status`.
- In `entity/src/lib.rs`, remove the `pub mod advisory_status;` line.
- The existing `entity/src/advisory.rs` entity pattern (SeaORM Model derive, Column enum, Relation enum) should be followed for the updated fields.
- Per CONVENTIONS.md §Framework (inferred from Key Conventions): use SeaORM's `DeriveActiveEnum` for enum column mapping. Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` entity file scope.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with DeriveActiveEnum and four variants
- [ ] The `status_id` column is replaced with a `status: AdvisoryStatusEnum` column in the advisory Model
- [ ] The Relation to AdvisoryStatus is removed from the advisory entity
- [ ] `entity/src/lib.rs` no longer exports or references `advisory_status`
- [ ] The `entity` crate compiles without errors

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully with no warnings about missing advisory_status references
- [ ] Verify that the AdvisoryStatusEnum correctly round-trips through SeaORM serialization/deserialization

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:8f672db6b8963a55f33f5708c11f02c0a6cf255155972e65d530fa57ccd9da44
