## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new schema: replace the `status_id` foreign key column with a `status` enum column in the advisory entity, and remove all references to the `advisory_status` entity since the lookup table is being dropped.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK column with `status: AdvisoryStatusEnum` enum column; add SeaORM `DeriveActiveEnum` mapping for the PostgreSQL enum type
- `entity/src/lib.rs` — remove `advisory_status` module registration and re-export; remove any `Relation` definitions that reference the advisory_status entity

## Implementation Notes
In `entity/src/advisory.rs`, define an enum type using SeaORM's `DeriveActiveEnum` derive macro to map the Rust enum to the PostgreSQL `advisory_status_enum` type. Example pattern from SeaORM:

```rust
#[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
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

Replace the `status_id` column in the `Model` struct with `status: AdvisoryStatusEnum`. Remove the `Relation` to `advisory_status` from the `impl RelationTrait` block.

In `entity/src/lib.rs`, remove the `pub mod advisory_status;` line and any re-exports of the advisory_status entity types.

Per CONVENTIONS.md §Framework: use SeaORM derive macros for entity and enum definitions.
Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust/SeaORM scope.

Per CONVENTIONS.md §Module pattern: maintain the entity registration pattern in `lib.rs`.
Applies: task modifies `entity/src/lib.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `entity/src/advisory.rs` has no `Relation` to `advisory_status`
- [ ] `entity/src/lib.rs` has no references to `advisory_status` module
- [ ] All entity code compiles without errors

## Test Requirements
- [ ] Entity compiles and the enum mapping is correct
- [ ] SeaORM generates correct SQL for queries using the enum column
- [ ] No compilation errors from removing advisory_status references

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Database migration for enum column (schema must exist before entity can reference it)
