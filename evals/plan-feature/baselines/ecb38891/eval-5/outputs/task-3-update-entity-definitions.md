## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the migration. The `advisory` entity must replace its `status_id` integer FK column with a `status` column mapped to the `advisory_status_enum` PostgreSQL enum type. The `advisory_status` entity file must be removed since the lookup table no longer exists. The entity library's module registry must be updated to remove the `advisory_status` module export.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; add the `AdvisoryStatusEnum` enum definition with SeaORM's `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` -- remove the `pub mod advisory_status;` module declaration

## Files to Create
None -- the enum type is defined inline in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum`.

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` derive macro:
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
- In the `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its `RelationDef` implementation
- Remove any `impl Related<super::advisory_status::Entity> for Entity` block
- Reference the existing entity pattern in `entity/src/sbom.rs` for the standard SeaORM entity structure

## Reuse Candidates
- `entity/src/advisory.rs` -- existing advisory entity to be modified (current `status_id` FK pattern)
- `entity/src/sbom.rs` -- reference for standard SeaORM entity structure and derive macros

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants: New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` `Model` struct has `status: AdvisoryStatusEnum` column (not `status_id: i32`)
- [ ] `entity/src/advisory.rs` has no `Relation` to `advisory_status`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Verify `cargo check -p entity` succeeds with the updated entity definitions
- [ ] Verify the `AdvisoryStatusEnum` correctly maps to the PostgreSQL `advisory_status_enum` type

## Verification Commands
- `cargo check -p entity` -- compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create atomic database migration (entities must match the new schema)
