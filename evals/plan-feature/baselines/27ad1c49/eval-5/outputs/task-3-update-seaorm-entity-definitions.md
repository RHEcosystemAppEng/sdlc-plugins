## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. The `advisory` entity must replace its `status_id` foreign key field with a `status` field mapped to the `advisory_status_enum` PostgreSQL enum type. The `advisory_status` entity file must be removed since the lookup table no longer exists. The entity module registration in `lib.rs` must be updated accordingly.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field. Add SeaORM enum derivation for `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected. Remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` — Remove the `advisory_status` module declaration and re-export

## Files to Create
None — the `advisory_status.rs` entity file is being removed, not created.

## Implementation Notes
Follow the SeaORM enum mapping pattern for PostgreSQL enums. Define the enum in `entity/src/advisory.rs`:

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

The `Model` struct in `advisory.rs` should replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.

Remove the `RelationDef` that previously linked `advisory` to `advisory_status` via the foreign key.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `advisory::Model` has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] Relation from `advisory` to `advisory_status` is removed
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or re-exports the `advisory_status` module
- [ ] `cargo build -p entity` compiles without errors

## Test Requirements
- [ ] Entity crate compiles successfully with the new enum field
- [ ] SeaORM enum mapping correctly maps between Rust variants and PostgreSQL enum values

## Verification Commands
- `cargo build -p entity` — entity crate compiles
- `cargo test -p entity` — entity tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
