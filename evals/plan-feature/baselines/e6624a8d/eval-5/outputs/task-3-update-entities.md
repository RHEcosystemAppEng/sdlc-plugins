## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new advisory status enum schema. Modify the `advisory` entity to replace the `status_id` foreign key column with a `status` enum column mapped to the `advisory_status_enum` PostgreSQL type. Remove the `advisory_status` entity definition and its registration, as the lookup table no longer exists after the migration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; add SeaORM enum mapping for `advisory_status_enum`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export; remove any references to the advisory_status entity

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::EnumIter` and `sea_orm::DeriveActiveEnum`
- Use the `#[sea_orm(db_type = "Enum", enum_name = "advisory_status_enum")]` attribute on the enum
- Map each variant to its database string value using `#[sea_orm(string_value = "New")]` etc.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum
- Remove any `Related<advisory_status::Entity>` implementation

Per CONVENTIONS.md §Framework: use SeaORM entity patterns for defining the enum type mapping and entity column definitions.
Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM database framework scope.

## Reuse Candidates
- `entity/src/advisory.rs` — existing entity definition pattern to follow for column definitions and relation declarations
- `entity/src/sbom.rs` — reference for SeaORM entity structure and relation patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants mapped to the PostgreSQL enum
- [ ] `advisory` entity `Model` struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `advisory_status` entity is removed from `entity/src/lib.rs`
- [ ] No compilation errors in the entity crate
- [ ] No remaining references to `advisory_status` entity or `status_id` column in entity code

## Test Requirements
- [ ] Verify the entity crate compiles without errors (`cargo check -p entity`)
- [ ] Verify `AdvisoryStatusEnum` correctly maps to the PostgreSQL enum type
- [ ] Verify no orphaned imports or references to the removed advisory_status entity

## Verification Commands
- `cargo check -p entity` — verify entity crate compiles
- `cargo build` — verify full project builds with updated entities

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
