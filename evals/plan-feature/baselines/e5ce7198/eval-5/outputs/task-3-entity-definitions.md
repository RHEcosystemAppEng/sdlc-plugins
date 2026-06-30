## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: add a `status` enum field to the advisory entity mapped to the `advisory_status_enum` PostgreSQL type, remove the `status_id` foreign key field, and delete the `advisory_status` entity file since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id` integer field with `status` enum field using SeaORM enum mapping
- `entity/src/lib.rs` -- remove the `advisory_status` module re-export

## Implementation Notes
In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `EnumIter` and `DeriveActiveEnum` from SeaORM to map it to the PostgreSQL `advisory_status_enum` type. Replace the existing `status_id: i32` column definition with `status: AdvisoryStatusEnum`. Remove the `Relation` entry for the `advisory_status` table if one exists.

In `entity/src/lib.rs`, remove the `pub mod advisory_status;` line (or equivalent re-export). Any other entities that reference `advisory_status` via relations should have those relation definitions removed.

Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct and column definition style.

## Reuse Candidates
- `entity/src/sbom.rs` -- reference for SeaORM entity struct and column definition patterns
- `entity/src/advisory.rs` -- existing advisory entity to be modified; inspect current relation definitions

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` Rust enum is defined with variants matching the PostgreSQL enum values
- [ ] `entity/src/advisory.rs` uses the new `status: AdvisoryStatusEnum` field instead of `status_id`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] All relation definitions referencing `advisory_status` are removed
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify `cargo check` passes with the updated entity definitions
- [ ] Verify the `AdvisoryStatusEnum` correctly maps to/from the PostgreSQL enum type

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Database migration (schema must exist before entity definitions are validated)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}

[sdlc-workflow] Description digest: sha256-md:f4d7d57ed48f2026c8dd2ad8fe246400bc92b1a799409c26ea830e6d73793ddb
