# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the migration. The `advisory.rs` entity must replace the `status_id` foreign key field with a `status` field of type `advisory_status_enum`. The `advisory_status.rs` entity file must be removed since the lookup table no longer exists. The entity module's `lib.rs` must be updated to remove the `advisory_status` module export.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add SeaORM `DeriveActiveEnum` mapping for the PostgreSQL enum type
- `entity/src/lib.rs` — Remove `pub mod advisory_status;` module declaration and re-export

## Files to Create
- None (file removal only: `entity/src/advisory_status.rs` is deleted)

## Implementation Notes
- In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::DeriveActiveEnum` to map to the PostgreSQL `advisory_status_enum` type. Use `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in `advisory.rs` and the corresponding `impl Related<advisory_status::Entity>` block.
- Replace the `status_id` column definition (`ColumnType::Integer`) with `status` column definition (`ColumnType::Enum`).
- Update `entity/src/lib.rs` to remove the `advisory_status` module. Check for any other files that re-export or reference `advisory_status` entities (e.g., `sbom_advisory.rs` if it has relations).
- Follow the existing entity pattern seen in `entity/src/sbom.rs` and `entity/src/package.rs` for struct and relation definitions.

## Reuse Candidates
- `entity/src/sbom.rs` — Example SeaORM entity showing the established pattern for Model struct, Column enum, Relation enum, and ActiveModelBehavior implementation
- `entity/src/package.rs` — Another entity example for reference on column type definitions

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` mapping to `advisory_status_enum`
- [ ] The `Model` struct in `advisory.rs` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] The `Relation` enum no longer includes `AdvisoryStatus`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status`
- [ ] The project compiles after these entity changes (with expected downstream compilation errors in service/endpoint code that will be resolved in Task 4)

## Test Requirements
- [ ] Verify the entity module compiles with `cargo check -p entity`
- [ ] Verify `AdvisoryStatusEnum` correctly serializes/deserializes the four enum values
- [ ] Verify no dangling references to `advisory_status` entity remain in the entity crate

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
