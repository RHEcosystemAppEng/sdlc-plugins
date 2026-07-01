## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema. Replace the `status_id` integer relation in `entity/src/advisory.rs` with a `status` field of the new enum type, and remove the `entity/src/advisory_status.rs` entity file since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — remove `status_id` column and `advisory_status` relation; add `status` column as `advisory_status_enum` enum type using SeaORM's `DeriveActiveEnum`
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module re-export

## Files to Create
- (none — `entity/src/advisory_status.rs` is deleted, not created)

## Implementation Notes
In `entity/src/advisory.rs`:
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`.
- Replace the `status_id: i32` column with `status: AdvisoryStatusEnum`.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its corresponding `RelationTrait` implementation.

In `entity/src/lib.rs`:
- Remove `pub mod advisory_status;` line to stop exporting the deleted entity.

The `entity/src/advisory_status.rs` file should be deleted entirely.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has a `status` field of type `AdvisoryStatusEnum` instead of `status_id`
- [ ] `AdvisoryStatusEnum` derives `DeriveActiveEnum` with correct variants (New, Analyzing, Fixed, Rejected)
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references `advisory_status` module
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] `cargo build -p entity` succeeds with the updated entity definitions
- [ ] No remaining references to `advisory_status` entity in the entity crate
- [ ] `AdvisoryStatusEnum` can be serialized/deserialized correctly in tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 2 — Create migration for advisory_status_enum
