## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. The `advisory.rs` entity must replace the `status_id` integer foreign key column with a `status` column that maps to the `advisory_status_enum` PostgreSQL enum type. The `advisory_status.rs` entity file (for the now-dropped lookup table) must be removed, and all references to it in `entity/src/lib.rs` must be deleted.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column using SeaORM's `DeriveActiveEnum` mapping
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export

## Files to Create
None — the `AdvisoryStatusEnum` Rust enum can be defined in `entity/src/advisory.rs` alongside the entity, following SeaORM conventions for inline enum definitions.

## Implementation Notes
- Define an `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` using SeaORM's `#[derive(DeriveActiveEnum)]` macro with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute
- Map each variant to its database value using `#[sea_orm(string_value = "New")]` etc.
- In `entity/src/advisory.rs`, replace the `status_id` column definition with a `status` column of type `AdvisoryStatusEnum`
- Remove the `Relation` to `advisory_status` from the advisory entity's `RelationDef`
- Remove `entity/src/advisory_status.rs` (the entity for the dropped lookup table)
- Remove the `mod advisory_status` and `pub use advisory_status::*` lines from `entity/src/lib.rs`
- Follow the existing entity pattern in `entity/src/sbom.rs` for struct layout and attribute usage

Per CONVENTIONS.md Key Conventions: use SeaORM for database entity definitions. Applies: task modifies `entity/src/advisory.rs` matching the convention's entity definition scope.

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct layout, column definitions, and relation definitions

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` uses `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] Relation to `advisory_status` table is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] `cargo check` passes in the entity crate

## Test Requirements
- [ ] Verify `cargo check` passes with the updated entity definitions
- [ ] Verify that removing advisory_status references does not cause compilation errors in dependent crates

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add database migration for advisory status enum conversion
