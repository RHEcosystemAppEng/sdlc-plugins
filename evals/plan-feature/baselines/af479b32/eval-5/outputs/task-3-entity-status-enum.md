# Task 3: Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema. The `advisory` entity must replace its `status_id` integer foreign key field with a `status` field of type `AdvisoryStatusEnum`. Define the Rust enum using SeaORM's `DeriveActiveEnum` macro to map to the PostgreSQL `advisory_status_enum` type. Remove the `advisory_status` entity module since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` field with `status: AdvisoryStatusEnum` field; add the `AdvisoryStatusEnum` enum definition with `DeriveActiveEnum` derive; remove the `Relation` entry for `advisory_status`
- `entity/src/lib.rs` -- remove the `advisory_status` module declaration and its re-export

## Files to Create
None

## Implementation Notes
- Define the enum in `entity/src/advisory.rs` (or a sub-module) using SeaORM's `DeriveActiveEnum`:
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
- Remove the `status_id` column definition from the `Model` struct and replace with `status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant and its `RelationTrait` implementation
- Remove the `Related<advisory_status::Entity>` implementation
- Per CONVENTIONS.md: use SeaORM for database entity definitions.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM entity scope.
- Follow the pattern of existing entity files (e.g., `entity/src/sbom.rs`) for struct layout, derive macros, and relation definitions

## Reuse Candidates
- `entity/src/sbom.rs` -- existing SeaORM entity demonstrating the project's entity struct pattern, derive macros, column definitions, and relation implementations
- `entity/src/advisory.rs` -- current advisory entity showing the existing structure that must be modified

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` enum is defined with variants: New, Analyzing, Fixed, Rejected
- [ ] `AdvisoryStatusEnum` uses `DeriveActiveEnum` and maps to the PostgreSQL `advisory_status_enum` type
- [ ] `advisory::Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] No `Relation::AdvisoryStatus` variant exists in the advisory entity
- [ ] `advisory_status` module is removed from `entity/src/lib.rs`
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles with `cargo check -p entity`
- [ ] Verify the `AdvisoryStatusEnum` can be serialized to and deserialized from the database enum values
- [ ] Verify no compilation errors in downstream crates that depend on the entity crate

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors
- `cargo check --workspace` -- no downstream compilation errors from entity changes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
