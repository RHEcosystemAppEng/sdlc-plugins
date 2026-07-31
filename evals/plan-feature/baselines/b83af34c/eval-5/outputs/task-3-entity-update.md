## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory schema. Modify the `advisory` entity to replace the `status_id` foreign key field with a `status` enum field using the new `advisory_status_enum` type. Remove the `advisory_status` entity module since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id` integer column with `status` enum column mapped to `advisory_status_enum`; remove the relation to the advisory_status table
- `entity/src/lib.rs` — Remove the `advisory_status` module re-export and add the new enum type definition if needed

## Implementation Notes
Follow the existing SeaORM entity pattern in `entity/src/advisory.rs`. Use SeaORM's `DeriveActiveEnum` macro to define a Rust enum that maps to the PostgreSQL `advisory_status_enum` type. The enum variants should be: `New`, `Analyzing`, `Fixed`, `Rejected`.

Example pattern from the existing codebase:
```rust
#[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
pub enum AdvisoryStatus {
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

The `advisory` entity's `Model` struct should replace `pub status_id: i32` with `pub status: AdvisoryStatus`. Remove the `Relation::BelongsTo` for advisory_status from the `Relation` enum.

Per CONVENTIONS.md §Framework: use SeaORM entity conventions for enum mapping. Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] `AdvisoryStatus` enum is defined with variants: New, Analyzing, Fixed, Rejected
- [ ] `advisory` entity uses `status: AdvisoryStatus` column instead of `status_id: i32`
- [ ] Relation to advisory_status table is removed from the advisory entity
- [ ] The advisory_status entity module is removed from `entity/src/lib.rs`
- [ ] Code compiles with `cargo check` (within the entity crate)

## Test Requirements
- [ ] Verify the `AdvisoryStatus` enum serializes and deserializes correctly for all four values
- [ ] Verify the advisory entity compiles and maps correctly to the updated database schema

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
