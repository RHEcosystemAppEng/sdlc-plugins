## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema. Replace the `status_id` foreign key field in the advisory entity with a `status` enum field of type `advisory_status_enum`. Remove the `advisory_status` entity entirely since the lookup table no longer exists. Define a Rust enum that maps to the PostgreSQL `advisory_status_enum` type using SeaORM's `DeriveActiveEnum` derive macro.

## Files to Modify
- `entity/src/advisory.rs` -- replace the `status_id: i32` foreign key column with a `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; add the `AdvisoryStatusEnum` Rust enum with SeaORM `DeriveActiveEnum` derive
- `entity/src/lib.rs` -- remove the `pub mod advisory_status;` module registration

## Files to Create
None (the enum type is defined inline in `entity/src/advisory.rs`)

## Implementation Notes
- Define the `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected`. Use SeaORM's `DeriveActiveEnum` macro to map it to the PostgreSQL `advisory_status_enum` type.
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
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum and its `RelationDef` implementation.
- Remove the `advisory_status.rs` file from disk (the entity for the dropped lookup table). Update `entity/src/lib.rs` to remove its `pub mod advisory_status;` declaration.
- The `sbom_advisory.rs` join table entity references `advisory` but should not reference `advisory_status` -- verify and clean up if needed.
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `entity/src/sbom.rs` -- reference for SeaORM entity definition patterns (Column enum, Relation enum, derive macros)

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants mapped to `advisory_status_enum`
- [ ] `entity/src/advisory.rs` has `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles cleanly with the new enum field
- [ ] Verify no remaining references to `advisory_status` entity in the codebase (except migration history)

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors
- `grep -r "advisory_status" entity/src/` -- no remaining references to the old entity (except the enum type name itself)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create migration for advisory_status_enum
