# Task 3: Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. Modify the `advisory` entity to replace the `status_id` foreign key integer column with a `status` column mapped to the `advisory_status_enum` PostgreSQL type. Remove the `advisory_status` entity module since the lookup table no longer exists. Update the entity library root to remove the `advisory_status` module re-export.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; add a `#[derive(EnumIter, DeriveActiveEnum)]` Rust enum mapping for `AdvisoryStatusEnum`
- `entity/src/lib.rs` — remove `pub mod advisory_status` re-export

## Files to Create
None — the `advisory_status.rs` entity file is removed, not replaced.

## Implementation Notes
- In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::EnumIter` and `sea_orm::DeriveActiveEnum` with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`.
- Replace the `status_id` column definition with `status: AdvisoryStatusEnum` in the `Model` struct.
- Remove the `Relation::AdvisoryStatus` variant and its `RelationTrait` implementation.
- Remove `entity/src/advisory_status.rs` entirely.
- In `entity/src/lib.rs`, remove the `pub mod advisory_status;` line and any re-exports of `advisory_status::Entity`.
- Follow the existing entity patterns in `entity/src/sbom.rs` for SeaORM derive macro usage and column definitions.
- Per CONVENTIONS.md §Framework: use SeaORM for entity definitions and enum mapping. Applies: convention has no file-type restriction (broadly applicable).

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with SeaORM active enum derives
- [ ] `advisory::Model` has `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] `advisory::Relation::AdvisoryStatus` variant is removed
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Entity compiles with new enum column definition
- [ ] SeaORM can serialize and deserialize `AdvisoryStatusEnum` values correctly

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Write database migration for advisory status enum
