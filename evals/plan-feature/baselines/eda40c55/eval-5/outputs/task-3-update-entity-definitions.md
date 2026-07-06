## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the advisory status enum migration. The `advisory` entity must replace the `status_id` foreign key integer column with a `status` column mapped to the `advisory_status_enum` PostgreSQL enum type. Any entity module for the `advisory_status` lookup table must be removed since the table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column using SeaORM's `EnumIter` derive macro; remove the relation to `advisory_status`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration if present; add the new `AdvisoryStatusEnum` type export

## Implementation Notes
- Define `AdvisoryStatusEnum` as a Rust enum with `#[derive(EnumIter, DeriveActiveEnum)]` and map each variant to the PostgreSQL enum values: `New`, `Analyzing`, `Fixed`, `Rejected`.
- Use SeaORM's `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute on the enum.
- In `entity/src/advisory.rs`, update the `Model` struct to replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its corresponding `RelationTrait` implementation.
- Remove the `impl Related<super::advisory_status::Entity> for Entity` block if present.
- Per CONVENTIONS.md §Framework: use SeaORM entity conventions for enum mapping as documented in SeaORM's enum column support.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `entity/src/advisory.rs` — existing entity structure, relation definitions, and column mappings to follow as reference
- `entity/src/sbom.rs` — reference for SeaORM entity patterns (Model struct, Relation enum, RelationTrait impl)

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `advisory::Model` struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] No relation to `advisory_status` entity remains in the advisory entity
- [ ] `entity/src/lib.rs` no longer exports or declares an `advisory_status` module
- [ ] Entity compiles without errors against the migrated database schema

## Test Requirements
- [ ] Compile the entity crate with `cargo build -p entity` — no errors
- [ ] Verify that `AdvisoryStatusEnum` correctly maps to/from the PostgreSQL enum values
- [ ] Verify that queries using `advisory::Entity::find()` work with the new schema

## Verification Commands
- `cargo build -p entity` — compiles without error
- `cargo test -p entity` — all entity tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration for advisory status enum conversion
