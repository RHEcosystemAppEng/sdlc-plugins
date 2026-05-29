# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: replace the `status_id` foreign key field in the advisory entity with a `status` enum field, remove the `advisory_status` entity module entirely, and update all entity re-exports. This task provides the Rust type system foundation that all subsequent service and endpoint changes depend on.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; add a `#[derive(EnumIter, DeriveActiveEnum)]` enum definition for `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` mapped to the PostgreSQL `advisory_status_enum` type
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` re-export since the entity module is being deleted

## Files to Create
None — the advisory_status entity file is being deleted, not created.

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` macro:
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
- In the `Relation` enum, remove the variant that relates to `advisory_status` (e.g., `AdvisoryStatus`)
- Remove the `impl Related<super::advisory_status::Entity>` block
- Delete the file `entity/src/advisory_status.rs` entirely
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct layout and derive macros

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct layout, derive macros, and relation definitions
- `entity/src/package.rs` — reference for entity pattern with enum-like fields

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants: New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` `Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] The `Relation` to `advisory_status` is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer re-exports `advisory_status`
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully
- [ ] Verify that no references to `advisory_status` entity remain in the entity crate

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create atomic migration to replace advisory_status table with enum column
