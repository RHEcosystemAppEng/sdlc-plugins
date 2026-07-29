## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory schema. Replace the `status_id` integer foreign key on the `Advisory` entity with a `status` field mapped to the `advisory_status_enum` PostgreSQL enum type. Remove the `advisory_status` entity file entirely since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` — replace the `status_id: i32` column definition with a `status: AdvisoryStatusEnum` column using SeaORM's `DeriveActiveEnum` macro; remove the `Relation` to `advisory_status` entity; update any `Related<>` trait implementations that reference the advisory_status entity
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module declaration and any re-exports

## Files to Create
- None (the enum type definition can be co-located in `entity/src/advisory.rs` or in a shared types module, depending on project convention)

## Implementation Notes
- Define the `AdvisoryStatusEnum` using SeaORM's `DeriveActiveEnum` derive macro with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`. Map each variant: `New`, `Analyzing`, `Fixed`, `Rejected` with corresponding `#[sea_orm(string_value = "...")]` attributes.
- In the `Advisory` model, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`. Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its corresponding `RelationDef` implementation.
- Remove or update any `impl Related<advisory_status::Entity> for Entity` blocks.
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for enum field mappings and relation definitions.
- Per the project's Key Conventions: SeaORM is used for entity definitions. Follow the existing entity structure in sibling entity files.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — existing entity pattern showing column definitions, relations, and `Related<>` implementations
- `entity/src/package.rs` — existing entity with related field mappings

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants matching the PostgreSQL enum values
- [ ] The `Advisory` model's `status` field uses `AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] No `Relation` or `Related<>` references to `advisory_status` remain in the entity module
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles cleanly with `cargo check -p entity`
- [ ] Verify that no references to `advisory_status` remain in the entity crate (grep for `advisory_status` in `entity/src/`)

## Verification Commands
- `cargo check -p entity` — compiles without errors
- `grep -r "advisory_status" entity/src/` — returns no results

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory_status_enum
