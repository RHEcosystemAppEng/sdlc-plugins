# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. The `advisory.rs` entity must replace the `status_id` foreign key field with a `status` enum field backed by the `advisory_status_enum` PostgreSQL type. The `advisory_status.rs` entity file must be removed since the lookup table no longer exists. The entity module exports in `lib.rs` must be updated accordingly.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add SeaORM enum derivation for `AdvisoryStatusEnum`
- `entity/src/lib.rs` — Remove the `pub mod advisory_status` export and add the `AdvisoryStatusEnum` re-export if needed

## Files to Create
None — this task only modifies existing entity files.

## Implementation Notes
- Define the `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` using SeaORM's `DeriveActiveEnum` derive macro. Map each variant to its PostgreSQL enum string value.
- In `entity/src/advisory.rs`, replace the `status_id` column definition with a `status` column of type `AdvisoryStatusEnum`. Remove the `Relation::AdvisoryStatus` variant and its `RelationTrait` implementation.
- Follow the existing entity pattern established in `entity/src/sbom.rs` and `entity/src/package.rs` for struct layout and derive macros (`DeriveEntityModel`, `DeriveRelation`, etc.).
- Remove or delete `entity/src/advisory_status.rs` entirely — the lookup table entity is no longer needed.
- Update `entity/src/lib.rs` to remove the `advisory_status` module declaration.
- Per CONVENTIONS.md §Framework: use SeaORM entity conventions consistent with existing entities in the codebase.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust entity file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — Reference for SeaORM entity structure, derive macros, and relation definitions
- `entity/src/package.rs` — Reference for entity pattern with enum-like fields (license field pattern)

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines an `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The `Model` struct in `advisory.rs` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] The `Relation::AdvisoryStatus` variant is removed from the entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles cleanly: `cargo check -p entity`
- [ ] Verify that the `AdvisoryStatusEnum` correctly maps to PostgreSQL enum values using SeaORM's `DeriveActiveEnum`

## Verification Commands
- `cargo check -p entity` — expected: compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion

---

[sdlc-workflow] Description digest: sha256-md:b9411fd6dfe624cecc2cf40db306cc86bf824c7fdd121a459c3193ec8d475cdf
