## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory schema after the enum migration. Modify `entity/src/advisory.rs` to replace the `status_id` integer FK field with a `status` field of the `AdvisoryStatusEnum` type. Remove the `entity/src/advisory_status.rs` entity module since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module export. Define the `AdvisoryStatusEnum` derive enum in the advisory entity module to match the PostgreSQL `advisory_status_enum` type.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` field; add `#[derive(EnumIter, DeriveActiveEnum)]` enum definition for `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected; remove the `Relation` to `advisory_status` table
- `entity/src/lib.rs` — remove `pub mod advisory_status;` export

## Implementation Notes
Define the SeaORM active enum in `entity/src/advisory.rs`:

```rust
#[derive(Clone, Debug, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
pub enum AdvisoryStatusEnum {
    #[sea_orm(string_value = "New")]
    New,
    #[sea_orm(string_value = "Analyzing")]
    Analyzing,
    #[sea_orm(string_value = "Fixed")]
    Fixed,
    #[sea_orm(string_value = "Rejected")]
    Rejected,
}
```

Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its `RelationDef` implementation. The `advisory_status.rs` entity file should be deleted entirely since the table no longer exists.

Per CONVENTIONS.md §Framework: use SeaORM derive macros for entity definitions.
Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM database scope.

## Reuse Candidates
- `entity/src/advisory.rs::Model` — existing advisory entity struct to extend with the enum field
- `entity/src/sbom.rs` — reference for SeaORM entity definition patterns used in this project

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `entity/src/advisory.rs` `Relation` enum no longer includes `AdvisoryStatus` variant
- [ ] `entity/src/advisory_status.rs` is removed
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] Entity compiles successfully with `cargo check -p entity`

## Test Requirements
- [ ] Verify the entity module compiles without errors
- [ ] Verify that downstream crates (`modules/fundamental`, `modules/ingestor`) can reference the updated `AdvisoryStatusEnum` type

## Verification Commands
- `cargo check -p entity` — entity crate compiles successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion
