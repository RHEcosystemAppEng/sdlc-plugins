# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: modify `entity/src/advisory.rs` to replace the `status_id` foreign key column with a `status` enum column of type `advisory_status_enum`, and remove the `entity/src/advisory_status.rs` entity file since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module export.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; add SeaORM enum derive for `AdvisoryStatusEnum`
- `entity/src/lib.rs` — remove `pub mod advisory_status;` export

## Implementation Notes
- Follow the SeaORM enum mapping pattern: define `#[derive(EnumIter, DeriveActiveEnum)]` for `AdvisoryStatusEnum` with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
- Each variant needs `#[sea_orm(string_value = "New")]` etc. for the four values: New, Analyzing, Fixed, Rejected
- The `advisory.rs` entity currently has a `Relation::HasOne` or `Relation::BelongsTo` to `advisory_status` — this relation must be removed entirely
- Remove any `impl Related<advisory_status::Entity>` block from `advisory.rs`
- The entity pattern is established in sibling files like `entity/src/sbom.rs` — follow the same struct and derive conventions
- Delete the file `entity/src/advisory_status.rs` entirely since the backing table is dropped

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct pattern and derive macros
- `entity/src/advisory.rs` — existing entity to modify, shows current relation pattern

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with SeaORM enum derives
- [ ] `advisory` entity uses `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] Relation to `advisory_status` entity is removed from `advisory.rs`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] All entity crate code compiles without errors

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully
- [ ] Verify the `AdvisoryStatusEnum` enum correctly maps to PostgreSQL enum values

## Verification Commands
- `cargo check -p entity` — entity crate compiles
- `cargo build -p entity` — entity crate builds without warnings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to add advisory status enum and drop lookup table

---
Description Digest: sha256-md:fab1d22dfaff6c58e03211a7e13d51e3bfc1560d41dd356d0351448222b2b6e3
Priority: High
Fix Versions: RHTPA 2.0.0
