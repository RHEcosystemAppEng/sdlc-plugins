# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new schema: replace the `status_id` foreign key column in the advisory entity with a `status` enum column, define the `AdvisoryStatusEnum` Rust enum with SeaORM derive macros, and remove the `advisory_status` entity module entirely. This ensures the ORM layer matches the migrated database schema.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; add the `AdvisoryStatusEnum` enum definition with `#[derive(EnumIter, DeriveActiveEnum)]`
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` re-export

## Files to Create
None — the enum is defined inline in `entity/src/advisory.rs`.

## Implementation Notes
Define the enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` macro:

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

Replace the `status_id` column definition with `status: AdvisoryStatusEnum` in the `Model` struct. Remove the relation definition that linked `advisory.status_id` to `advisory_status.id`. Also remove the `entity/src/advisory_status.rs` file if it exists (the repo structure in `entity/src/lib.rs` presumably re-exports it).

Update `entity/Cargo.toml` if any dependency was only needed for the lookup table pattern.

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` is defined with four variants: New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` Model struct has `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] Relation to `advisory_status` is removed from advisory entity
- [ ] `advisory_status` entity module is removed from `entity/src/lib.rs`
- [ ] `entity/` crate compiles without errors

## Test Requirements
- [ ] `cargo build -p entity` compiles successfully
- [ ] Verify the `AdvisoryStatusEnum` enum maps correctly to the PostgreSQL `advisory_status_enum` type

## Verification Commands
- `cargo build -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create atomic migration: enum type, backfill, and table drop

[sdlc-workflow] Description digest: sha256-md:c8e2f5a34d7b9160e3a6c1f82b5d0e93a4f7c8d12e6b3a5071d9f2c4e8a1b6d3
