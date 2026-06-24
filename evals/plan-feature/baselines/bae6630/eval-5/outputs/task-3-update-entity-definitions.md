## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status schema. The `advisory` entity must replace the `status_id` foreign key integer column with a `status` enum column mapped to the `advisory_status_enum` PostgreSQL type. All references to the removed `advisory_status` entity must be cleaned up from the entity module registry.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; add SeaORM `DeriveActiveEnum` mapping for the enum type
- `entity/src/lib.rs` — Remove the `advisory_status` module re-export if present

## Implementation Notes
In `entity/src/advisory.rs`, define a Rust enum for the advisory status using SeaORM's `DeriveActiveEnum` derive macro:

```rust
#[derive(Debug, Clone, PartialEq, Eq, DeriveActiveEnum)]
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

Replace the `status_id` column definition with a `status: AdvisoryStatusEnum` column. Remove the `Relation::HasOne` or `Relation::BelongsTo` relationship pointing to the advisory_status entity.

Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for column definitions and relation declarations.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with DeriveActiveEnum mapping to `advisory_status_enum` PostgreSQL type
- [ ] `advisory` entity Model has `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] Relation to `advisory_status` entity is removed from advisory entity
- [ ] `entity/src/lib.rs` no longer exports an `advisory_status` module
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] Entity crate compiles with `cargo check -p entity`
- [ ] Enum variant serialization matches PostgreSQL enum values (New, Analyzing, Fixed, Rejected)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

## Digest
[sdlc-workflow] Description digest: sha256-md:9a5b7fe5bec42b63428b30bf3f264738f111ef9a7fba6382730377e0cc778e07
