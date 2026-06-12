# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema where `advisory.status` is a PostgreSQL enum column instead of a foreign key to the `advisory_status` lookup table. This involves modifying the advisory entity to use an enum field and removing references to the now-dropped `advisory_status` entity.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` integer foreign key column with `status` enum column using `advisory_status_enum` type; remove the `Relation` to `advisory_status` table; update the `Model` struct to have a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- `entity/src/lib.rs` — remove the `advisory_status` module re-export if present; ensure only the updated `advisory` entity is exported
- `entity/Cargo.toml` — no changes expected unless a new dependency is needed for enum support

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in Rust with SeaORM's `DeriveActiveEnum` derive macro:
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
- The enum definition can live in `entity/src/advisory.rs` alongside the entity definition, following SeaORM conventions for co-located enum types
- Remove the `Relation::AdvisoryStatus` variant and its `RelationDef` implementation from the advisory entity's `Relation` enum
- Remove any `impl Related<super::advisory_status::Entity>` block
- Follow the existing entity pattern in `entity/src/sbom.rs` for field definitions and relation setup
- Reference SeaORM documentation on `DeriveActiveEnum` for PostgreSQL enum mapping

## Reuse Candidates
- `entity/src/sbom.rs` — existing SeaORM entity pattern showing Model struct, Column enum, Relation enum, and Related implementations
- `entity/src/package.rs` — another entity example for cross-referencing the pattern

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants (New, Analyzing, Fixed, Rejected)
- [ ] `entity/src/advisory.rs` Model struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] All references to `advisory_status` entity are removed from `entity/src/lib.rs`
- [ ] The entity compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Entity module compiles with the updated advisory entity
- [ ] AdvisoryStatusEnum correctly maps to/from string values matching the PostgreSQL enum

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
