## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema. Add a `status` field using the `advisory_status_enum` type to the `advisory` entity, remove the `status_id` foreign key field, and delete the `advisory_status` entity module that is no longer needed. This task bridges the database schema change (Task 2) and the service layer updates (Tasks 4, 5) by providing the ORM types that all downstream code depends on.

## Files to Modify
- `entity/src/advisory.rs` -- Add `status` field as `AdvisoryStatusEnum` (SeaORM enum mapping), remove `status_id` foreign key field and its relation definition
- `entity/src/lib.rs` -- Remove the `advisory_status` module declaration and re-export
- `entity/src/advisory_status.rs` -- Delete this file (entity for the dropped lookup table is no longer needed)

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` from SeaORM to map it to the PostgreSQL `advisory_status_enum` type
- In `advisory.rs`, replace the `status_id: i32` column with `status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `RelationDef` implementation
- Remove any `Related<advisory_status::Entity>` implementation from the advisory entity
- Per CONVENTIONS.md §Framework: use SeaORM entity derive macros and `DeriveActiveEnum` for the enum mapping.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust file scope.
- See `entity/src/advisory.rs` for the existing entity definition pattern and `entity/src/sbom.rs` for a reference entity implementation

## Reuse Candidates
- `entity/src/advisory.rs::Model` -- existing Advisory entity model struct to modify (not rewrite from scratch)
- `entity/src/sbom.rs` -- reference entity implementation showing the SeaORM derive pattern used in this project

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants (New, Analyzing, Fixed, Rejected) using `DeriveActiveEnum`
- [ ] `entity/src/advisory.rs` `Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles cleanly with the updated advisory entity
- [ ] Verify that `AdvisoryStatusEnum` serializes and deserializes correctly for all four variants
- [ ] Verify that removing `advisory_status` entity does not leave dangling references in other entity modules

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Database migration to create enum type and add status column
