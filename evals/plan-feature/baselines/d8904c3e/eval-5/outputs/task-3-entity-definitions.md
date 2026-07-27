## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new database schema where `advisory.status` is an enum column instead of a foreign key to the `advisory_status` lookup table. Remove the now-obsolete `advisory_status` entity file and update all module exports.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; add SeaORM enum derivation for `AdvisoryStatusEnum`
- `entity/src/lib.rs` — remove the `advisory_status` module re-export

## Implementation Notes
- Define `AdvisoryStatusEnum` as a Rust enum with `#[derive(EnumIter, DeriveActiveEnum)]` and `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attributes
- Map each variant with `#[sea_orm(string_value = "New")]`, `#[sea_orm(string_value = "Analyzing")]`, `#[sea_orm(string_value = "Fixed")]`, `#[sea_orm(string_value = "Rejected")]`
- Follow the existing entity pattern in `entity/src/sbom.rs` for field definitions and derive macros
- Remove `entity/src/advisory_status.rs` entirely — this entity is no longer needed after the migration drops the table
- Update any `Related<advisory_status::Entity>` implementations in `advisory.rs` — remove the relation definition
- Check `entity/src/sbom_advisory.rs` for any references to `advisory_status` and update if needed

## Reuse Candidates
- `entity/src/sbom.rs` — reference entity implementation demonstrating the standard SeaORM entity pattern with derive macros and relations

## Acceptance Criteria
- [ ] `advisory.rs` entity uses `AdvisoryStatusEnum` type for the `status` column
- [ ] `AdvisoryStatusEnum` is correctly derived with SeaORM active enum attributes
- [ ] `entity/src/advisory_status.rs` entity file is removed
- [ ] `lib.rs` no longer exports the `advisory_status` module
- [ ] All entity definitions compile without errors

## Test Requirements
- [ ] Entity module compiles successfully (`cargo check -p entity`)
- [ ] SeaORM enum mapping matches the PostgreSQL enum type values exactly (New, Analyzing, Fixed, Rejected)

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Database migration (schema must exist before entity can reference the enum type)
