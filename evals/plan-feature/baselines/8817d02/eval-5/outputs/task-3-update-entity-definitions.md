# Task 3 — Update SeaORM entity definitions for advisory status enum

## Summary

Update advisory entity to use enum column and remove advisory_status entity

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the SeaORM entity definitions to reflect the new database schema. The `advisory` entity must use the `advisory_status_enum` PostgreSQL enum for its `status` field instead of a `status_id` foreign key. The `advisory_status` entity module must be removed since the lookup table no longer exists.

## Files to Modify

- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add SeaORM `DeriveActiveEnum` mapping for `AdvisoryStatusEnum`
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` re-export

## Files to Create

None — the enum type definition is added directly to `entity/src/advisory.rs`

## Implementation Notes

- Define `AdvisoryStatusEnum` as a Rust enum with `#[derive(DeriveActiveEnum)]` and `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`. Map variants: `New`, `Analyzing`, `Fixed`, `Rejected`.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `RelationDef` implementation.
- Remove any `impl Related<advisory_status::Entity> for Entity` block.
- See SeaORM documentation for `DeriveActiveEnum` usage with PostgreSQL enums.
- Follow the existing entity pattern in `entity/src/sbom.rs` for struct layout and derives.

## Reuse Candidates

- `entity/src/sbom.rs` — reference for SeaORM entity struct layout, derives, and relation definitions
- `entity/src/advisory.rs` — existing file to modify; inspect current `Relation` enum and `Related` impls

## Acceptance Criteria

- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The advisory `Model` struct has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] No reference to `advisory_status` entity remains in the entity crate
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements

- [ ] `cargo check -p entity` compiles successfully
- [ ] Verify the `AdvisoryStatusEnum` derives `DeriveActiveEnum` with correct PostgreSQL enum mapping

## Verification Commands

- `cargo check -p entity` — entity crate compiles without errors

## Dependencies

- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add database migration for advisory status enum column

sha256-md:4d6715e18e6c9e3334da8961eb601a24253a9dc93dd1e8a1b38b8efc3edcb168
