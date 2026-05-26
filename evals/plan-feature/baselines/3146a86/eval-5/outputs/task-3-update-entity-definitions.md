# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new database schema. Replace the `status_id` foreign key field in the advisory entity with a `status` field mapped to the `advisory_status_enum` PostgreSQL enum type. Remove the `advisory_status` entity file entirely since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; add SeaORM `DeriveActiveEnum` mapping for the enum type; remove the `Relation` to `AdvisoryStatus` from the entity's `RelationTrait` impl
- `entity/src/lib.rs` — Remove the `pub mod advisory_status` module re-export and any references to the advisory_status entity

## Files to Create
None — the enum definition should live within `entity/src/advisory.rs` as a `DeriveActiveEnum` derive on a Rust enum, not in a separate file.

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` with `db_type = "Enum"` and `enum_name = "advisory_status_enum"`. Each variant needs `#[sea_orm(string_value = "New")]` etc.
- Follow the SeaORM active enum pattern: `#[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]`
- In the `Model` struct, change the `status_id` field to `pub status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant and its definition from `RelationTrait` impl
- Remove `impl Related<super::advisory_status::Entity> for Entity` if present
- Delete `entity/src/advisory_status.rs` entirely (the file is removed, not just emptied)
- Update `entity/src/lib.rs` to remove the `advisory_status` module declaration
- Per constraints doc section 5 (Code Change Rules): inspect the existing entity files before modifying to understand the current patterns (relation definitions, column mappings).
- Per constraints doc section 2 (Commit Rules): commit message must reference TC-9005 and follow Conventional Commits format.

## Reuse Candidates
- `entity/src/advisory.rs` — Current advisory entity definition showing existing column mappings and relation patterns to follow
- `entity/src/sbom.rs` — Sibling entity demonstrating the project's SeaORM entity conventions (for cross-cutting concern parity per constraint 5.8)

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` and four variants
- [ ] Advisory entity `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `advisory_status` relation is removed from advisory entity's `RelationTrait`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references `advisory_status`
- [ ] `cargo check -p entity` succeeds (no compile errors in the entity crate)

## Test Requirements
- [ ] Entity crate compiles without errors or warnings
- [ ] `AdvisoryStatusEnum` correctly maps to/from PostgreSQL enum values (New, Analyzing, Fixed, Rejected)

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
