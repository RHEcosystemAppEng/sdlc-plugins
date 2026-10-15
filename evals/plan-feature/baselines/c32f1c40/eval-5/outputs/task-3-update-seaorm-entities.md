## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status schema. The `advisory` entity must replace the `status_id` foreign key field with a `status` field of the new `advisory_status_enum` type. The `advisory_status` entity module must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add SeaORM `DeriveActiveEnum` mapping for the `advisory_status_enum` PostgreSQL type
- `entity/src/lib.rs` -- remove the `advisory_status` module registration and re-export; update any `use` statements that reference advisory_status

## Implementation Notes
- Define an `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` using SeaORM's `DeriveActiveEnum` derive macro
- Map the Rust enum to the PostgreSQL `advisory_status_enum` type using `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
- Each variant needs `#[sea_orm(string_value = "New")]` (etc.) attributes to map to the PostgreSQL enum values
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum
- Remove the `Related<advisory_status::Entity>` implementation from the advisory entity
- The `advisory_status.rs` file should be deleted (it is no longer needed since the lookup table has been dropped)
- Per CONVENTIONS.md §Framework: follow SeaORM entity definition patterns with `DeriveEntityModel`, `DeriveActiveEnum`.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM database scope.
- Reference `entity/src/package_license.rs` for an example of entity-to-entity relation patterns and how relations are defined in the project

## Reuse Candidates
- `entity/src/advisory.rs` -- existing advisory entity definition showing current field layout, relations, and SeaORM derive macros
- `entity/src/package_license.rs` -- example of SeaORM entity with relations that can serve as a pattern reference

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines an `AdvisoryStatusEnum` Rust enum with variants matching the PostgreSQL enum values
- [ ] The `advisory` entity model uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] No `Relation::AdvisoryStatus` variant exists in the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Verify the entity compiles with `cargo check -p entity`
- [ ] Verify the enum serialization/deserialization roundtrips correctly (enum value to database and back)

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create advisory status enum migration
