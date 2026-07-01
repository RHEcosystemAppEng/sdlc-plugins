# Task 3 — Update SeaORM entity definitions for advisory status enum

**Priority:** High
**Fix Versions:** RHTPA 2.0.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: modify `entity/advisory.rs` to replace the `status_id` foreign key relation with a `status` field using the `advisory_status_enum` PostgreSQL enum, and remove the `advisory_status` entity since the lookup table no longer exists. Define a Rust enum `AdvisoryStatusEnum` with `DeriveActiveEnum` to map to the PostgreSQL enum type.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation::AdvisoryStatus` variant from the `Relation` enum; remove the `Related<advisory_status::Entity>` impl
- `entity/src/lib.rs` — remove the `pub mod advisory_status` re-export

## Files to Create
- `entity/src/advisory_status_enum.rs` — define `AdvisoryStatusEnum` Rust enum with `DeriveActiveEnum` derive macro, mapping variants (New, Analyzing, Fixed, Rejected) to the PostgreSQL `advisory_status_enum` type

## Implementation Notes
- Use SeaORM's `DeriveActiveEnum` derive macro to map the Rust enum to the PostgreSQL enum type. The enum variants should be: `New`, `Analyzing`, `Fixed`, `Rejected`
- The `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute configures the mapping
- Each variant needs `#[sea_orm(string_value = "New")]` etc. to map to the PostgreSQL enum values
- In `entity/src/advisory.rs`, the `Model` struct's `status_id: i32` field becomes `status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant and the corresponding `impl Related<super::advisory_status::Entity>` block
- Per CONVENTIONS.md Key Conventions: follow the existing entity pattern established by other entities like `entity/src/sbom.rs` for struct layout, derives, and relation definitions.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's entity file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct layout, `DeriveEntityModel`, `DeriveRelation`, and `Related` implementations
- `entity/src/package.rs` — reference for entity with enum-like fields

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `AdvisoryStatusEnum` is defined with `DeriveActiveEnum` and four variants (New, Analyzing, Fixed, Rejected)
- [ ] The `Relation::AdvisoryStatus` variant is removed from the advisory entity
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] Verify the entity crate compiles (`cargo check -p entity`)
- [ ] Verify `AdvisoryStatusEnum` correctly serializes/deserializes each variant

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4
