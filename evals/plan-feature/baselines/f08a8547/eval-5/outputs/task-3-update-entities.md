## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new schema after the advisory status migration. Replace the `status_id` foreign key column in the advisory entity with a `status` column of type `AdvisoryStatusEnum`, and remove the `advisory_status` entity since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column definition with `status: AdvisoryStatusEnum` column; define `AdvisoryStatusEnum` enum type with SeaORM derive macros; remove `Relation::AdvisoryStatus` variant from the entity's `Relation` enum
- `entity/src/lib.rs` -- remove `pub mod advisory_status` re-export since the entity file is no longer needed

## Implementation Notes
- Define `AdvisoryStatusEnum` in `entity/src/advisory.rs` using:
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
- Replace the `status_id` column in the `Model` struct with `status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant and its `RelationDef` implementation
- Remove or update any `Related<advisory_status::Entity>` implementation on the advisory entity
- The file `entity/src/advisory_status.rs` should be deleted (removal of its module reference in `lib.rs` effectively removes it from compilation)
- Per CONVENTIONS.md §Framework: use SeaORM's `DeriveActiveEnum` macro for enum-to-column mapping.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.
- Constraint §5.2: inspect existing entity code before modifying
- Constraint §5.4: reuse SeaORM derive patterns established in existing entities

## Reuse Candidates
- `entity/src/advisory.rs` -- existing entity definition to modify in-place; contains current column definitions, relations, and derive macros
- `entity/src/sbom.rs` -- reference for SeaORM entity structure patterns (column definitions, relations, derive macros)
- `entity/src/package.rs` -- reference for entity patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants: New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` Model struct has `status: AdvisoryStatusEnum` column replacing `status_id: i32`
- [ ] Relation to `advisory_status` table is removed from the advisory entity
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] `cargo build -p entity` compiles successfully
- [ ] No references to `advisory_status` entity or `status_id` column remain in the entity crate

## Test Requirements
- [ ] Verify the entity crate compiles with the new enum column type
- [ ] Verify no references to `advisory_status` entity remain in the entity crate
- [ ] Verify the `AdvisoryStatusEnum` enum has exactly four variants matching the PostgreSQL enum type

## Verification Commands
- `cargo build -p entity` -- compilation succeeds

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum
