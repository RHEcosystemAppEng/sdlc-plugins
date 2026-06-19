# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the advisory_status table is dropped and replaced with an enum column. Define a Rust enum `AdvisoryStatusEnum` that maps to the PostgreSQL `advisory_status_enum` type. Update the advisory entity to use the new `status` enum field instead of `status_id`. Remove the advisory_status entity file since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` foreign key field with `status` field of type `AdvisoryStatusEnum`; remove the relation to `advisory_status`
- `entity/src/lib.rs` — remove the `advisory_status` module re-export; add the new `AdvisoryStatusEnum` enum (or its module)

## Files to Create
- `entity/src/advisory_status_enum.rs` — define `AdvisoryStatusEnum` Rust enum with SeaORM `DeriveActiveEnum` derive macro, mapping variants (New, Analyzing, Fixed, Rejected) to the PostgreSQL `advisory_status_enum` type

## Implementation Notes
Use SeaORM's `DeriveActiveEnum` derive macro to map the Rust enum to the PostgreSQL enum type. The enum definition should use `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` with appropriate variant attributes. Follow the existing entity patterns in `entity/src/advisory.rs` and `entity/src/sbom.rs` for struct layout and derive macros.

Remove the file `entity/src/advisory_status.rs` (the entity for the dropped lookup table) if it exists, and remove its reference from `entity/src/lib.rs`.

Per CONVENTIONS.md §Framework: use SeaORM for database entity definitions. Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM scope.

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` Rust enum exists with variants New, Analyzing, Fixed, Rejected
- [ ] `AdvisoryStatusEnum` uses SeaORM `DeriveActiveEnum` to map to PostgreSQL `advisory_status_enum`
- [ ] `entity/src/advisory.rs` uses `status: AdvisoryStatusEnum` instead of `status_id` FK
- [ ] Relation to `advisory_status` table removed from advisory entity
- [ ] `entity/src/advisory_status.rs` removed (or no longer referenced)
- [ ] `entity/src/lib.rs` updated to export new enum and remove old module

## Test Requirements
- [ ] Entity compiles without errors
- [ ] `AdvisoryStatusEnum` correctly serializes/deserializes all four status values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
