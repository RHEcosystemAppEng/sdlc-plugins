## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status schema. The `advisory` entity must replace the `status_id` foreign key column with a `status` column of the `AdvisoryStatusEnum` type. The `advisory_status` entity must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation::AdvisoryStatus` relation definition; define `AdvisoryStatusEnum` as a `DeriveActiveEnum`
- `entity/src/lib.rs` -- remove the `advisory_status` module re-export

## Implementation Notes
- Define the `AdvisoryStatusEnum` as a SeaORM `DeriveActiveEnum` with variants: `New`, `Analyzing`, `Fixed`, `Rejected`. Use the `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` attribute.
- In `entity/src/advisory.rs`, replace the `status_id` column definition with a `status` column using the enum type.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `RelationDef` implementation and any `Related<advisory_status::Entity>` impl.
- Update `entity/src/lib.rs` to remove the `pub mod advisory_status;` line.
- If `entity/src/advisory_status.rs` exists as a separate file, delete it.

Per CONVENTIONS.md §Module Pattern: follow the SeaORM entity pattern established in sibling entities like `entity/src/sbom.rs`.
Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `entity/src/sbom.rs` -- sibling SeaORM entity showing the project's entity definition patterns
- `entity/src/package.rs` -- another entity example for consistent structure

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants (New, Analyzing, Fixed, Rejected)
- [ ] `entity/src/advisory.rs` uses `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] The `Relation::AdvisoryStatus` relation is removed from the advisory entity
- [ ] `entity/src/lib.rs` no longer re-exports an `advisory_status` module
- [ ] The crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Entity compiles and derives all required SeaORM traits
- [ ] `AdvisoryStatusEnum` correctly maps to the PostgreSQL `advisory_status_enum` type
- [ ] No references to the old `advisory_status` entity remain in the entity crate

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
