## Summary
Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. The `advisory` entity must replace the `status_id` integer foreign key column with a `status` column mapped to the `advisory_status_enum` PostgreSQL enum type. The `advisory_status` entity file must be removed since the lookup table no longer exists. The entity module root (`entity/src/lib.rs`) must be updated to remove the `advisory_status` module re-export.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; add SeaORM enum derive for `AdvisoryStatusEnum`; remove the `Relation` to `advisory_status` table
- `entity/src/lib.rs` -- remove `pub mod advisory_status` re-export and any references to the advisory_status entity

## Files to Create
None -- only modifying existing files and removing `entity/src/advisory_status.rs`

## Implementation Notes
Define the `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` using SeaORM's `DeriveActiveEnum` derive macro mapped to the PostgreSQL `advisory_status_enum` type. The enum should implement `Display` and `FromStr` for serialization. Follow the existing entity patterns in `entity/src/sbom.rs` for struct layout and derive macros. Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `RelationDef` implementation. The file `entity/src/advisory_status.rs` should be deleted entirely.

## Reuse Candidates
- `entity/src/sbom.rs` -- reference for SeaORM entity struct layout, derive macros, and relation definitions

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` mapping to PostgreSQL `advisory_status_enum`
- [ ] `entity/src/advisory.rs` `Model` struct has `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] `entity/src/advisory.rs` no longer defines a relation to `advisory_status`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer re-exports `advisory_status`
- [ ] `cargo build -p entity` compiles successfully

## Test Requirements
- [ ] Verify `cargo build -p entity` compiles with the updated entity definitions
- [ ] Verify no remaining references to `advisory_status` entity in `entity/src/`

## Verification Commands
- `cargo build -p entity` -- entity crate compiles successfully
- `grep -r "advisory_status" entity/src/` -- returns no matches (all references removed)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:74e66ba059b583c9e75db928d7b57c38f74d46b5a8859938e64a882a7d64c05d
