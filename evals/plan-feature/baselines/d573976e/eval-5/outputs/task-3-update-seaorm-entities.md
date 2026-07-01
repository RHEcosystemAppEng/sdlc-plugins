## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: replace the `status_id` integer FK column on the `Advisory` entity with a `status` column mapped to a Rust enum via `DeriveActiveEnum`, and remove the `advisory_status` entity file since the lookup table no longer exists. This provides the type-safe foundation that all service and endpoint code will build on.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; define the `AdvisoryStatusEnum` Rust enum with `DeriveActiveEnum` mapping to the PostgreSQL `advisory_status_enum` type
- `entity/src/lib.rs` — remove `pub mod advisory_status;` re-export; ensure `AdvisoryStatusEnum` is publicly accessible (either re-exported from `advisory.rs` or as a standalone type)
- `entity/Cargo.toml` — verify SeaORM features include enum support (e.g., `with-postgres`); add if missing

## Implementation Notes
- Define the Rust enum in `entity/src/advisory.rs`:
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
- In the `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`
- In the `Relation` enum, remove the variant that references `advisory_status::Entity`
- In the `Related<advisory_status::Entity>` impl, remove it entirely
- Remove the file `entity/src/advisory_status.rs` (the entity for the dropped lookup table)
- Follow the existing entity patterns in `entity/src/sbom.rs` for struct layout and derive macros
- Ensure serde serialization of `AdvisoryStatusEnum` produces the string values ("New", "Analyzing", etc.) for API response compatibility

## Reuse Candidates
- `entity/src/sbom.rs` — reference SeaORM entity pattern: Model struct with derives, Column enum, Relation enum, Related impls
- `entity/src/advisory.rs` — current entity structure to understand existing column definitions, relations, and derive macros before modifying

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` Rust enum exists with four variants: New, Analyzing, Fixed, Rejected
- [ ] `AdvisoryStatusEnum` derives `DeriveActiveEnum` and maps to PostgreSQL `advisory_status_enum`
- [ ] `Advisory` Model struct has `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] No `Relation` or `Related` impl references `advisory_status` entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer re-exports `advisory_status` module
- [ ] `entity/Cargo.toml` has required SeaORM enum features
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Compile the entity crate in isolation: `cargo check -p entity` succeeds
- [ ] Verify that `AdvisoryStatusEnum` serializes to the expected string values via serde

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create enum migration
