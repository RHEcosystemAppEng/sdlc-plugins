## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Replace the `status_id` foreign key field in the advisory entity with a `status` field using the `advisory_status_enum` PostgreSQL enum type. Remove the `advisory_status` entity file since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status` table; update any `impl Related<>` blocks that reference the advisory_status entity
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module declaration and re-export

## Files to Create
None — the `entity/src/advisory_status.rs` file is being removed (deleted), not created.

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::EnumIter` and `sea_orm::DeriveActiveEnum` to map it to the PostgreSQL `advisory_status_enum` type. See SeaORM documentation on enum column mapping.
- The enum definition can be placed directly in `entity/src/advisory.rs` or in a shared types module. Follow the pattern used by existing entities in the `entity/src/` directory.
- Remove all `Relation` variants and `impl Related<>` blocks that reference the `advisory_status` entity, since the join relationship no longer exists.
- Per CONVENTIONS.md §Framework: use SeaORM derive macros (`DeriveEntityModel`, `DeriveActiveEnum`) for entity definitions.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.

## Reuse Candidates
- `entity/src/advisory.rs` — existing advisory entity definition; modify in place to replace FK with enum field
- `entity/src/sbom.rs` — reference for SeaORM entity definition patterns (derive macros, column definitions, relations)

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines an `AdvisoryStatusEnum` enum with variants New, Analyzing, Fixed, Rejected
- [ ] The advisory entity's `Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] The `Relation` to `advisory_status` is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or re-exports the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles: `cargo check -p entity`
- [ ] Verify the enum maps correctly to the PostgreSQL type by running a round-trip test (insert and read back an advisory with each status variant)

## Verification Commands
- `cargo check -p entity` — verify entity crate compiles with new enum definition

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add database migration for advisory status enum conversion
