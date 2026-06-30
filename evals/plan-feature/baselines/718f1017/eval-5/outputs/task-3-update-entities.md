# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema introduced by the migration in Task 2. The `advisory` entity must replace its `status_id` foreign key field with a `status` field using the `advisory_status_enum` PostgreSQL enum type. The `advisory_status` entity file must be removed entirely, and all references to it must be cleaned up from the entity module registration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add the `AdvisoryStatusEnum` enum definition with SeaORM `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module registration and any re-exports

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` derive macro with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
- Enum variants: `New`, `Analyzing`, `Fixed`, `Rejected` — each with `#[sea_orm(string_value = "...")]` matching the PostgreSQL enum values
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum
- Remove the `impl Related<advisory_status::Entity> for Entity` block if present
- Delete `entity/src/advisory_status.rs` entirely
- Follow the existing entity patterns in `entity/src/sbom.rs` for enum field definitions and relation patterns
- Per docs/constraints.md section 5 (Code Change Rules): inspect `entity/src/advisory.rs` and `entity/src/advisory_status.rs` before modifying

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity structure, relation definitions, and field type patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants matching the PostgreSQL enum
- [ ] `advisory` entity `Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `Relation::AdvisoryStatus` is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] `entity` crate compiles without errors

## Test Requirements
- [ ] `cargo build -p entity` compiles successfully
- [ ] No remaining references to `advisory_status` entity in the entity crate

## Verification Commands
- `cargo build -p entity` — entity crate compiles
- `grep -r "advisory_status" entity/src/` — returns no results (confirming all references removed)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

[sdlc-workflow] Description digest: sha256-md:d51ecc86fe64784d58e3660fab6513e48d1e6865bed4900cedcb8203d086c74a
