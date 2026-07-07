## Repository
trustify-backend

## Target Branch
main

## Description
Create the `LicensePolicy` entity and configuration model that defines how licenses are classified for compliance purposes. Each license identifier (SPDX expression) maps to a policy classification: `Allowed`, `Denied`, or `ReviewRequired`. This model underpins the compliance checking logic in the license report service.

## Files to Modify
- `entity/src/lib.rs` -- add `pub mod license_policy;` to expose the new entity module

## Files to Create
- `entity/src/license_policy.rs` -- SeaORM entity defining the `license_policy` table with columns: `id` (UUID primary key), `license_spdx` (String, the SPDX license identifier), `classification` (Enum: Allowed/Denied/ReviewRequired), `reason` (optional String), `created_at`, `updated_at`

## Implementation Notes
- Follow the existing SeaORM entity patterns in `entity/src/sbom_package.rs` and `entity/src/package_license.rs` for derive macros and column definitions
- Use `sea_orm::entity::prelude::*` imports consistent with other entity files
- Define a `Classification` enum with `#[derive(EnumIter, DeriveActiveEnum)]` for the three states
- The `license_spdx` field should use the SPDX license expression format (e.g., "Apache-2.0", "MIT", "GPL-3.0-only")
- Add a database migration file under `migration/` to create the `license_policy` table
- Per CONVENTIONS.md Key Conventions (Framework): use SeaORM derive macros and entity patterns consistent with existing entities in `entity/src/`.
  Applies: task creates `entity/src/license_policy.rs` matching the convention's Rust entity file scope.
- Per CONVENTIONS.md Key Conventions (Module pattern): follow the established entity module registration pattern by adding the module to `entity/src/lib.rs`.
  Applies: task modifies `entity/src/lib.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `entity/src/package_license.rs` -- reference for SeaORM entity pattern with license-related fields
- `entity/src/sbom_package.rs` -- reference for join table entity derive macros

## Acceptance Criteria
- [ ] `LicensePolicy` entity compiles and is accessible from `entity::license_policy`
- [ ] `Classification` enum supports `Allowed`, `Denied`, and `ReviewRequired` variants
- [ ] Migration creates the `license_policy` table with all required columns
- [ ] Entity follows existing patterns (derives, column types) from other entity files

## Test Requirements
- [ ] Unit test verifying `Classification` enum serialization/deserialization
- [ ] Migration runs successfully against a test database

## Dependencies
- None (foundational task)
