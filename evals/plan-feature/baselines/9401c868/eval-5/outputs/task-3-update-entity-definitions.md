## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Replace the `status_id` foreign key column in the advisory entity with a `status` column using the `AdvisoryStatusEnum` type. Remove the `advisory_status` entity file since the lookup table no longer exists after the migration.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation::AdvisoryStatus` variant from the Relation enum; update any `Related<advisory_status::Entity>` impl
- `entity/src/lib.rs` -- remove the `pub mod advisory_status;` module declaration

## Implementation Notes
- Define `AdvisoryStatusEnum` using SeaORM's `DeriveActiveEnum` derive macro, mapping to the PostgreSQL `advisory_status_enum` type created by the migration:
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
- In the `Model` struct within `entity/src/advisory.rs`, replace the `status_id` field with:
  ```rust
  pub status: AdvisoryStatusEnum,
  ```
- Remove the `Relation::AdvisoryStatus` variant and its `RelationDef` impl from the advisory entity's `Relation` enum
- Remove the `impl Related<super::advisory_status::Entity>` block from `advisory.rs`
- Delete `entity/src/advisory_status.rs` -- the entity is no longer needed since the lookup table was dropped
- Remove the `advisory_status` module reference from `entity/src/lib.rs`
- Check if `entity/src/sbom_advisory.rs` or other join entities reference `advisory_status` and update if needed

Per CONVENTIONS.md section "Framework": use SeaORM for database entity definitions.
Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `entity/src/advisory.rs` -- existing advisory entity definition showing current column, relation, and `DeriveEntityModel` patterns
- `entity/src/package.rs` -- example of an entity with enum-like fields for reference on SeaORM enum mapping patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` Model struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] Foreign key relation to `advisory_status` table is removed from advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares the `advisory_status` module
- [ ] Entity crate compiles successfully

## Test Requirements
- [ ] SeaORM entity compiles and maps correctly to the new database schema
- [ ] Enum variants serialize to the correct PostgreSQL enum values (New, Analyzing, Fixed, Rejected)
- [ ] Enum variants deserialize correctly from database query results

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum
