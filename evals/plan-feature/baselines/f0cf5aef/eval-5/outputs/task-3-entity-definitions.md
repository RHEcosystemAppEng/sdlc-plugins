## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Replace the `status_id` foreign key relation in the `advisory` entity with a direct `status` enum column mapped to the `advisory_status_enum` PostgreSQL type. Remove the `advisory_status` entity file since the lookup table no longer exists. Update the entity module exports accordingly.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; remove the `Relation::AdvisoryStatus` variant and related `Related<advisory_status::Entity>` impl; add `#[derive(EnumIter, DeriveActiveEnum)]` enum definition for `AdvisoryStatusEnum` mapping to the PostgreSQL `advisory_status_enum` type
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module export

## Files to Create
None — the advisory_status entity is removed, not replaced.

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
- Remove the `advisory_status.rs` file entirely (or `git rm entity/src/advisory_status.rs`).
- Update any `Relation` enum variants in `advisory.rs` that reference `AdvisoryStatus` — remove the variant and its `RelationDef` implementation.
- Remove any `Related<super::advisory_status::Entity>` impl block from `advisory.rs`.
- Verify that no other entity files reference `advisory_status` (check `sbom_advisory.rs` and other files).
- Per CONVENTIONS.md §Framework: use SeaORM entity conventions for enum column mapping.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `entity/src/advisory.rs` — existing entity definition shows the established pattern for column definitions, relations, and `ActiveModel` derivation
- `entity/src/sbom.rs` — reference for SeaORM entity structure if the advisory entity needs structural guidance

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `entity/src/advisory.rs` `Column` enum includes `Status` variant mapped to the `advisory_status_enum` type
- [ ] `entity/src/advisory.rs` no longer has `StatusId` column or `AdvisoryStatus` relation
- [ ] `entity/src/advisory_status.rs` is removed
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Verify that the advisory entity compiles with the new enum column definition
- [ ] Verify that no dangling references to `advisory_status` entity remain in the entity crate

## Verification Commands
- `cargo check -p entity` — compiles without errors
- `grep -r "advisory_status" entity/src/` — returns no matches (all references removed)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion
