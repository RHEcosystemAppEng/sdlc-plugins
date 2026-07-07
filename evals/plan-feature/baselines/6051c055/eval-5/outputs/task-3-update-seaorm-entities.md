# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. The `advisory` entity must replace the `status_id` foreign key field with a `status` field mapped to the `advisory_status_enum` PostgreSQL enum type. The `advisory_status` entity file must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the relation to `advisory_status`; add the `AdvisoryStatusEnum` Rust enum with SeaORM `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` — Remove the `advisory_status` module declaration and re-export

## Files to Create
None

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` from SeaORM to map it to the PostgreSQL `advisory_status_enum` type
- Use the `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute on the enum
- Each variant needs a `#[sea_orm(string_value = "New")]` (etc.) attribute to map to the database enum values
- Update the `advisory::Column` enum to replace `StatusId` with `Status`
- Remove any `Relation` variants and `Related` implementations that referenced the `advisory_status` entity
- Per CONVENTIONS.md §Framework: follow SeaORM entity patterns consistent with existing entities like `entity/src/sbom.rs`.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — Reference for SeaORM entity structure, column definitions, and relation patterns
- `entity/src/package.rs` — Reference for entity with enum-like fields

## Acceptance Criteria
- [ ] `advisory::Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `AdvisoryStatusEnum` Rust enum is defined with four variants mapping to the PostgreSQL enum
- [ ] `advisory_status` entity file is removed from the codebase
- [ ] `entity/src/lib.rs` no longer declares or re-exports the `advisory_status` module
- [ ] The entity compiles without errors

## Test Requirements
- [ ] Verify `advisory::Model` can be deserialized from a database row with an enum `status` column
- [ ] Verify that the `AdvisoryStatusEnum` correctly maps all four values to and from the database
- [ ] Verify that removing `advisory_status.rs` does not cause compilation errors in dependent crates

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
