## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new advisory status enum schema. The `advisory` entity must replace the `status_id` integer foreign key column with a `status` enum column using SeaORM's `DeriveActiveEnum` macro. The `advisory_status` entity file must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace the `status_id: i32` column with a `status: AdvisoryStatusEnum` column using SeaORM's `DeriveActiveEnum` derive macro; remove the `Relation::AdvisoryStatus` variant and its foreign key definition from the `impl RelationTrait` block
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module declaration and re-export

## Files to Create
None — the advisory_status entity file is being removed, not created.

## Implementation Notes
Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` (or a shared location) using SeaORM's enum support:

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

Follow the existing entity pattern in `entity/src/sbom.rs` for the `Model` struct field definition and `DeriveEntityModel` usage. The `Column::Status` variant replaces `Column::StatusId`.

Remove the `advisory_status` relation from the `Relation` enum and the `impl Related<super::advisory_status::Entity>` block (if present). Any other entity that previously related to `advisory_status` (e.g., via `Related` impl) must also be updated.

Delete the file `entity/src/advisory_status.rs` entirely — this entity no longer has a backing table.

Per CONVENTIONS.md: follow the established SeaORM entity pattern with `DeriveEntityModel`.
Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` entity file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — demonstrates the standard SeaORM entity definition pattern with `DeriveEntityModel`, `DeriveRelation`, and column definitions that this task should follow

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` macro and four variants (New, Analyzing, Fixed, Rejected)
- [ ] The `advisory` Model struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The `Relation::AdvisoryStatus` variant is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or re-exports the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles cleanly with `cargo check -p entity`
- [ ] Verify that no references to `advisory_status` remain in the entity crate (grep for `advisory_status` in `entity/src/`)
- [ ] Verify the `AdvisoryStatusEnum` serialization matches the PostgreSQL enum values

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors
- `grep -r "advisory_status" entity/src/` — returns no matches (all references removed)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
