## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. The `advisory` entity must use the enum column instead of the foreign key, and the `advisory_status` entity must be removed entirely.

## Files to Modify
- `entity/src/advisory.rs` -- Replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; define the `AdvisoryStatusEnum` enum with SeaORM's `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` -- Remove the `advisory_status` module re-export; delete `pub mod advisory_status;`

## Implementation Notes
- Define `AdvisoryStatusEnum` in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` macro:
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
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in `advisory.rs`
- Delete `entity/src/advisory_status.rs` entirely (remove the file)
- Update `entity/src/lib.rs` to remove `pub mod advisory_status;`
- See existing entity `entity/src/sbom.rs` for the established SeaORM entity pattern

Per CONVENTIONS.md §Framework: use SeaORM's `DeriveActiveEnum` for enum column mapping.
Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust (.rs) file scope.

## Reuse Candidates
- `entity/src/sbom.rs` -- Existing SeaORM entity demonstrating Model, Relation, and column definition patterns
- `entity/src/advisory.rs` -- Current advisory entity to understand existing Relation and column definitions

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` is defined with values New, Analyzing, Fixed, Rejected using `DeriveActiveEnum`
- [ ] `advisory.rs` Model uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `Relation::AdvisoryStatus` is removed from the advisory entity's Relation enum
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] Entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` passes with the updated entity definitions
- [ ] Verify the `AdvisoryStatusEnum` derives match SeaORM's requirements for enum columns
- [ ] Verify no dangling references to the removed `advisory_status` entity remain in the entity crate

## Verification Commands
- `cargo check -p entity` -- Verify entity crate compiles cleanly

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
