## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the advisory status migration. Replace the `status_id` foreign key field in `entity/src/advisory.rs` with a `status` field of enum type `AdvisoryStatusEnum`. Remove the `entity/src/advisory_status.rs` entity file entirely since the lookup table no longer exists. Update the entity module re-exports in `entity/src/lib.rs` to remove the `advisory_status` module.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` enum column; remove the `Relation::AdvisoryStatus` relation entry; add SeaORM `DeriveActiveEnum` derive for the new enum type
- `entity/src/lib.rs` — remove `pub mod advisory_status;` re-export

## Files to Create
None (the advisory_status.rs file is deleted, not created)

## Implementation Notes
- Define `AdvisoryStatusEnum` as a Rust enum with `#[derive(DeriveActiveEnum)]` and `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute. Map each variant: `New`, `Analyzing`, `Fixed`, `Rejected`.
- In the `advisory.rs` entity `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its `RelationTrait` implementation.
- Remove `entity/src/advisory_status.rs` since the lookup table no longer exists.
- Update `entity/src/lib.rs` to remove the `advisory_status` module declaration.
- Per repo Key Conventions §Framework: use SeaORM entity patterns consistently.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` entity file scope.
- Per repo Key Conventions §Module pattern: each domain module follows model/ + service/ + endpoints/ structure. The entity layer is the data foundation consumed by these modules.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's entity module scope.
- Reference `entity/src/sbom.rs` for the established SeaORM entity pattern (Model struct, Relation enum, ActiveModel derives).

## Reuse Candidates
- `entity/src/sbom.rs` — existing SeaORM entity demonstrating Model, Relation, and ActiveModel patterns
- `entity/src/package.rs` — another entity example showing column definitions and relation patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` and four variants (New, Analyzing, Fixed, Rejected)
- [ ] `entity/src/advisory.rs` Model struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `Relation::AdvisoryStatus` variant and its `RelationTrait` impl are removed from `advisory.rs`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] `cargo build -p entity` compiles without errors

## Test Requirements
- [ ] Entity crate compiles successfully with the new enum definition
- [ ] SeaORM `DeriveActiveEnum` correctly maps enum variants to PostgreSQL enum values
- [ ] No remaining references to `advisory_status` entity in the entity crate

## Verification Commands
- `cargo build -p entity` — entity crate compiles cleanly
- `cargo test -p entity` — entity crate tests pass (if any)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for enum type and column conversion
