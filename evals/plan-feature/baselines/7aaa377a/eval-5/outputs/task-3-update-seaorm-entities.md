## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Modify `entity/src/advisory.rs` to replace the `status_id` integer foreign key field with a `status` field of the new enum type. Remove the `advisory_status` entity module (referenced in the feature as `entity/advisory_status.rs`). Update `entity/src/lib.rs` to remove the `advisory_status` module declaration and add the enum type definition.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status` table; update any derive macros for enum support
- `entity/src/lib.rs` — remove `advisory_status` module declaration; add `AdvisoryStatusEnum` enum definition with SeaORM `DeriveActiveEnum` derive macro
- `entity/Cargo.toml` — ensure SeaORM enum feature flags are enabled if not already

## Files to Create
None — the enum type definition belongs in the existing entity module.

## Implementation Notes
- Define `AdvisoryStatusEnum` using SeaORM's `DeriveActiveEnum` derive macro with variants: `New`, `Analyzing`, `Fixed`, `Rejected`. Map each variant to the PostgreSQL enum value string.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `RelationTrait` implementation.
- Remove any `Related<advisory_status::Entity>` implementation from the advisory entity.
- The `advisory_status` entity file (`entity/src/advisory_status.rs`) should be deleted if it exists — the feature requirements explicitly call for its removal. Verify its location before deletion.
- Per CONVENTIONS.md §Framework: use SeaORM patterns for entity definitions including `DeriveEntityModel`, `DeriveActiveEnum`, and relation macros.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust/SeaORM entity file scope.

## Reuse Candidates
- `entity/src/advisory.rs` — existing advisory entity with current FK-based status field; pattern for SeaORM entity definitions
- `entity/src/package_license.rs` — if it contains enum mappings, reference it as a pattern for `DeriveActiveEnum`

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` uses an `AdvisoryStatusEnum` field instead of `status_id` FK
- [ ] `AdvisoryStatusEnum` is defined with `DeriveActiveEnum` and maps to `advisory_status_enum` PostgreSQL type
- [ ] The `advisory_status` entity module is removed
- [ ] `entity/src/lib.rs` no longer declares the `advisory_status` module
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] Entity crate compiles successfully (`cargo build -p entity`)
- [ ] SeaORM enum serialization/deserialization works for all four variants (New, Analyzing, Fixed, Rejected)
- [ ] No references to `advisory_status` entity remain in the entity crate

## Verification Commands
- `cargo build -p entity` — compiles without errors
- `cargo test -p entity` — all entity tests pass (if any exist)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
