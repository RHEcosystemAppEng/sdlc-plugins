## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the advisory status enum migration. Replace the `status_id` foreign key field in the advisory entity with a `status` field using the `AdvisoryStatusEnum` type, and remove the `advisory_status` entity entirely since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; add the `AdvisoryStatusEnum` enum definition using SeaORM's `DeriveActiveEnum` macro; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` — remove the `pub mod advisory_status` module export

## Files to Create
None — only modifications needed

## Implementation Notes
- In `entity/src/advisory.rs`, define the enum using SeaORM's `DeriveActiveEnum` derive macro:
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
- Update the `Model` struct in `entity/src/advisory.rs` to replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- Remove any `Relation` variant pointing to `advisory_status` in the advisory entity's `RelationDef`.
- The file `entity/src/advisory_status.rs` should be deleted since the lookup table entity is obsolete. Remove its module declaration from `entity/src/lib.rs`.
- Per CONVENTIONS.md §Key Conventions: use SeaORM for database entities. Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants: New, Analyzing, Fixed, Rejected
- [ ] Advisory `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `entity/src/advisory_status.rs` is removed
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] All entity crate compilation succeeds with `cargo check -p entity`

## Test Requirements
- [ ] Entity crate compiles without errors
- [ ] `AdvisoryStatusEnum` serializes and deserializes correctly to/from the PostgreSQL enum type
- [ ] No remaining references to `advisory_status` entity in the codebase

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create advisory status enum migration

[sdlc-workflow] Description digest: sha256-md:d1d18465a1ca8f17da1f29b9981dd21e7b21b700b9384b7c973439ca71d08908
