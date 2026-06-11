# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema. Replace the `status_id` foreign key field in the `Advisory` entity with a `status` field of type `AdvisoryStatusEnum`. Remove the `advisory_status` entity module entirely since the lookup table no longer exists. Define the `AdvisoryStatusEnum` Rust enum with SeaORM derive macros for database mapping.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add the `AdvisoryStatusEnum` enum definition with SeaORM `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module export
- `entity/Cargo.toml` — no changes expected unless new dependencies are needed for enum support

## Files to Delete
- `entity/src/advisory_status.rs` — the lookup table entity is no longer needed

## Implementation Notes
- Define `AdvisoryStatusEnum` as a Rust enum with variants: `New`, `Analyzing`, `Fixed`, `Rejected`
- Use SeaORM's `DeriveActiveEnum` derive macro to map the Rust enum to the PostgreSQL `advisory_status_enum` type
- Example pattern for SeaORM enum mapping:
  ```rust
  #[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
  #[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
  pub enum AdvisoryStatusEnum {
      #[sea_orm(string_value = "New")]
      New,
      #[sea_orm(string_value = "Analyzing")]
      Analyzing,
      #[sea_orm(string_value = "Fixed")]
      Fixed,
      #[sea_orm(string_value = "Rejected")]
      Rejected,
  }
  ```
- Remove the `RelationDef` that linked `Advisory` to `AdvisoryStatus` via `status_id`
- Inspect `entity/src/advisory.rs` to understand the current entity structure before modifying
- Inspect `entity/src/advisory_status.rs` to confirm it can be safely removed (check for other references)
- Follow the pattern of other entity files (e.g., `entity/src/sbom.rs`) for consistency
- Per docs/constraints.md §5.2: inspect code before modifying
- Per docs/constraints.md §5.4: do not duplicate existing enum patterns — check if SeaORM enum mappings exist elsewhere in the entity crate

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity structure and derive macro usage
- `entity/src/advisory.rs` — existing entity to modify (inspect current field definitions and relations)

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` enum is defined with variants New, Analyzing, Fixed, Rejected
- [ ] `Advisory` entity has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `Relation` to `advisory_status` is removed from the `Advisory` entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] Entity crate compiles successfully (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` passes with no errors
- [ ] No remaining references to `advisory_status` entity in the entity crate

## Verification Commands
- `cargo check -p entity` — entity crate compiles successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
