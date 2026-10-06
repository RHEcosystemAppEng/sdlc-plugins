# Task 3 — Update SeaORM entity definitions for advisory status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. Replace the `status_id` foreign key field in the `advisory` entity with a `status` enum field, define the `AdvisoryStatusEnum` Rust enum with SeaORM's `DeriveActiveEnum` derive macro, and remove the `advisory_status` entity that is no longer needed.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column definition with `status: AdvisoryStatusEnum` enum column; add `AdvisoryStatusEnum` enum definition with `DeriveActiveEnum` derive; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` — remove `pub mod advisory_status;` module registration; ensure `advisory` module exports the new enum type
- `entity/Cargo.toml` — verify SeaORM features include enum support (if not already present)

## Implementation Notes
- Define `AdvisoryStatusEnum` as a Rust enum deriving `DeriveActiveEnum`, `EnumIter`, `Debug`, `Clone`, `PartialEq`, `Eq`:
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
- In the `Model` struct within `advisory.rs`, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`
- Remove the `Relation::HasOne` (or `BelongsTo`) relationship to `advisory_status` from the `Relation` enum
- Remove `entity/src/advisory_status.rs` (the file for the lookup table entity that is no longer needed)
- Per CONVENTIONS.md §Framework: use SeaORM entity conventions (`DeriveEntityModel`, `DeriveActiveEnum`) for the entity definition.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM entity file scope.

### Constraints (from docs/constraints.md)
- §2.1: Every commit MUST reference Jira issue ID in the footer
- §2.2: Commit messages MUST follow Conventional Commits (`refactor(entity): ...`)
- §2.3: Every commit MUST include `--trailer="Assisted-by: Claude Code"`
- §5.1: Changes MUST be scoped to the files listed in Files to Modify
- §5.7: Modified code implementing a type contract MUST have all required methods, properties, and type signatures verified as complete

## Reuse Candidates
- `entity/src/sbom.rs` — example SeaORM entity definition showing the project's entity pattern (Model struct, Relation enum, ActiveModelBehavior)
- `entity/src/advisory.rs` — current advisory entity to understand the existing structure before modification

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` enum is defined in `entity/src/advisory.rs` with four variants: `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory` entity `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] Relation to `advisory_status` is removed from the `advisory` entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer registers the `advisory_status` module
- [ ] `cargo check` on the entity crate compiles without errors

## Test Requirements
- [ ] Verify the `AdvisoryStatusEnum` derives `DeriveActiveEnum` and maps to the correct PostgreSQL enum type name
- [ ] Verify the `advisory` entity compiles with the new `status` field
- [ ] Verify no remaining references to `advisory_status` entity in the entity crate

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
