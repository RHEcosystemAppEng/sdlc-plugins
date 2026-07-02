## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Modify `entity/src/advisory.rs` to replace the `status_id` integer FK column with a `status` column using the `advisory_status_enum` PostgreSQL enum type. Remove the `entity/src/advisory_status.rs` entity file since the `advisory_status` lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module declaration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status` entity; update `Related` implementations
- `entity/src/lib.rs` — remove `pub mod advisory_status;` module declaration

## Files to Create
None — this task only modifies and removes existing files.

## Implementation Notes
- In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` from SeaORM to map it to the PostgreSQL `advisory_status_enum` type. Use the `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute.
- Remove the `status_id` column from the `Model` struct and add `status: AdvisoryStatusEnum`.
- Remove any `Relation::AdvisoryStatus` variant from the `Relation` enum and its `RelationDef` implementation.
- Remove `impl Related<super::advisory_status::Entity> for Entity` if present.
- Delete `entity/src/advisory_status.rs` entirely.
- In `entity/src/lib.rs`, remove `pub mod advisory_status;` and any re-exports.
- Follow the existing entity pattern in `entity/src/sbom.rs` for SeaORM `DeriveEntityModel` structure.
- Per repo Key Conventions: framework is SeaORM for database; follow the existing entity patterns in `entity/src/`.

## Reuse Candidates
- `entity/src/sbom.rs` — existing SeaORM entity demonstrating the `DeriveEntityModel`, `Relation` enum, and `Related` implementation patterns
- `entity/src/advisory.rs` — the current advisory entity file (pre-modification) showing the existing column and relation structure to preserve during refactor

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `advisory_status` relation is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or re-exports `advisory_status` module
- [ ] `cargo build` compiles the entity crate without errors

## Test Requirements
- [ ] Verify `cargo build -p entity` compiles successfully with the updated entity definitions
- [ ] Verify no remaining references to `advisory_status` entity in the entity crate
- [ ] Verify `AdvisoryStatusEnum` correctly maps to PostgreSQL `advisory_status_enum` type

## Verification Commands
- `cargo build -p entity` — verify entity crate compiles
- `cargo check --workspace` — verify no workspace-wide compilation errors from entity changes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:621ee8b4e001d3c218f315bc5b95fb223acdef82633b3df06a32e3741e1bef45
