## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the enum migration. Replace the `status_id` foreign key field in the advisory entity with a `status` field of the new enum type, and remove the `advisory_status` entity definition if present.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; update the `Relation` enum to remove the relation to `advisory_status`; add `#[derive(EnumIter, DeriveActiveEnum)]` enum definition for `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- `entity/src/lib.rs` — remove `pub mod advisory_status;` re-export if present; ensure advisory module is still exported

## Implementation Notes
- Follow the SeaORM `DeriveActiveEnum` pattern for PostgreSQL enum mapping. Define the enum with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` and annotate each variant with `#[sea_orm(string_value = "New")]` etc.
- Reference the existing entity pattern in `entity/src/sbom.rs` for the `Model`, `Entity`, `ActiveModel`, `Relation`, and `Column` derivations
- Remove any `RelationDef` that references `advisory_status::Entity` from the `Relation` enum in `advisory.rs`
- If `entity/src/advisory_status.rs` exists, remove the file entirely (the lookup table no longer exists after migration)
- Per CONVENTIONS.md §Framework: use SeaORM derive macros for entity definitions.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM entity scope.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` and four variants
- [ ] Advisory entity `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] No relation to `advisory_status` entity remains in the advisory entity
- [ ] `entity/src/advisory_status.rs` is removed (if it existed)
- [ ] `entity/src/lib.rs` no longer re-exports `advisory_status`
- [ ] Project compiles with the updated entity definitions

## Test Requirements
- [ ] Entity definitions compile and derive correctly
- [ ] `AdvisoryStatusEnum` can be converted to and from database values
- [ ] Advisory model can be constructed with each of the four enum variants

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Database migration (enum type must exist before entities reference it)
