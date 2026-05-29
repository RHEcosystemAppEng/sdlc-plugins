## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: replace the `status_id` foreign key field in the advisory entity with a `status` field mapped to the `advisory_status_enum` PostgreSQL enum type, and remove the `advisory_status` entity module entirely.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column definition with `status: AdvisoryStatusEnum` using SeaORM's `DeriveActiveEnum` macro; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module export

## Files to Create
- (none — the advisory_status.rs file is deleted, not created)

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` derive macro with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`. Each variant needs `#[sea_orm(string_value = "New")]` etc.
- Follow the pattern used by other entity files in `entity/src/` (e.g., `sbom.rs`, `package.rs`) for column definitions and relation declarations.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum and its corresponding `RelationTrait` implementation.
- Remove the `impl Related<super::advisory_status::Entity> for Entity` block.
- The `entity/src/advisory_status.rs` file should be deleted (listed as a file to remove, not modify).

## Reuse Candidates
- `entity/src/sbom.rs` — demonstrates SeaORM entity definition pattern with column types, relations, and model struct
- `entity/src/package.rs` — demonstrates entity definition with enum-like fields

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The advisory `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The `Relation::AdvisoryStatus` variant and its trait implementations are removed
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] The project compiles with the updated entity definitions (may require other tasks to land first)

## Test Requirements
- [ ] Verify entity compiles with the new enum field definition
- [ ] Verify SeaORM can deserialize a row with the enum column into the `Model` struct

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:4b968e8cacbb7aa4f3bf5dd3e8bd761b1e92b82e99ebdfb79660cc8c41dff1cc
