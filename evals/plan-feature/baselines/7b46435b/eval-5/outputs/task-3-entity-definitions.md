# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. Replace the `status_id` integer foreign key field in the advisory entity with a `status` field using SeaORM's enum column support. Remove the `advisory_status` entity file and its registration since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status` and the `impl Related<super::advisory_status::Entity>` block
- `entity/src/lib.rs` — remove `advisory_status` module declaration and re-export

## Implementation Notes
- Define an `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` (or a shared location) with variants: `New`, `Analyzing`, `Fixed`, `Rejected`
- Use SeaORM's `#[derive(EnumIter, DeriveActiveEnum)]` macro on the enum with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
- Map each variant to its database value with `#[sea_orm(string_value = "New")]`, `#[sea_orm(string_value = "Analyzing")]`, etc.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum
- Remove the `impl Related<super::advisory_status::Entity>` block from `advisory.rs`
- Delete the `entity/src/advisory_status.rs` file (the lookup table entity is no longer needed)
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct definition, derives, and relation patterns

## Reuse Candidates
- `entity/src/advisory.rs` — current advisory entity structure to modify in place
- `entity/src/sbom.rs` — reference entity for SeaORM patterns (derives, relations, column definitions)

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants mapping to database enum values
- [ ] Advisory entity's `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] All `Relation` and `Related` references to `advisory_status` are removed from `advisory.rs`
- [ ] `advisory_status` entity file is deleted and no longer registered in `entity/src/lib.rs`
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] Verify the entity crate compiles: `cargo check -p entity`
- [ ] Verify the advisory entity correctly maps to the database schema with the enum column
- [ ] Verify no references to `advisory_status` entity remain in the entity crate

## Verification Commands
- `cargo check -p entity` — entity crate compiles
- `grep -r "advisory_status" entity/src/` — no references remain (should return empty)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion
