**Summary:** Update SeaORM Advisory entity to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to match the schema from Task 2. The `Advisory` entity loses its `status_id` foreign key and the relation to the `advisory_status` lookup entity. It gains a `status` column typed as a Rust enum mapped to the PostgreSQL `advisory_status_enum` type. The lookup entity is removed. Every reader and writer of advisory status (Tasks 4 and 5) builds on this change (TC-9005).

## Files to Modify
- `entity/src/advisory.rs` — replace the `status_id` column and its `advisory_status` relation with `status: AdvisoryStatus`. Define the `AdvisoryStatus` enum (`DeriveActiveEnum`, `db_type = "Enum"`, `enum_name = "advisory_status_enum"`) with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration/re-export, and re-export `AdvisoryStatus` if the crate re-exports entity types

## Implementation Notes
- SeaORM enum mapping pattern (see the SeaORM "ActiveEnum" docs referenced in the Feature):
  ```rust
  #[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)]
  #[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
  pub enum AdvisoryStatus {
      #[sea_orm(string_value = "New")] New,
      #[sea_orm(string_value = "Analyzing")] Analyzing,
      #[sea_orm(string_value = "Fixed")] Fixed,
      #[sea_orm(string_value = "Rejected")] Rejected,
  }
  ```
  `string_value`s must match the enum labels created in `migration/src/m0002_advisory_status_enum/mod.rs` exactly.
- Add `Display`/`FromStr` (or `as_str()` / `TryFrom<&str>`) on `AdvisoryStatus`. Task 4 uses them to serialize status as the same string the API returns today, and Task 5 uses them to parse feed status strings. `FromStr` must return an error for unknown values. It must **not** fall back to a default variant.
- Remove the `Relation::AdvisoryStatus` variant and its `Related<advisory_status::Entity>` impl from `entity/src/advisory.rs`.
- **Lookup entity removal:** the Feature names `entity/advisory_status.rs`, but the repository structure analysis did not find `entity/src/advisory_status.rs`. At implementation time, search the entity crate for `advisory_status`. If a standalone file exists, delete it and remove its `mod` line in `entity/src/lib.rs`. If the lookup model is defined inline (e.g., inside `entity/src/advisory.rs`), remove that definition. Record which case applied in the PR description.
- Keep the other relations in `entity/src/advisory.rs` (e.g., to `sbom_advisory`) unchanged.
- Expect compile errors in downstream crates (`modules/fundamental`, `modules/search`, `modules/ingestor`) after this change. Tasks 4 and 5 fix them on `TC-9005`. This task does not need to edit those crates.
- Per CONVENTIONS.md §Framework: entities are SeaORM models. Use `DeriveActiveEnum` for the column type rather than a raw string column.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` SeaORM entity file scope.
- Constraints (docs/constraints.md): §2 commits must use Conventional Commits, include the `Implements TC-<task>` footer and an `Assisted-by:` trailer. §3 the PR must use `--base TC-9005` and the PR link must be posted to the Jira task. §5 changes stay scoped to the listed files (plus the lookup entity file if found), inspect code before modifying it, and must not duplicate existing functionality.

## Reuse Candidates
- `entity/src/advisory.rs` — existing `Advisory` model. Extend it in place; do not create a parallel model
- `entity/src/sbom_advisory.rs` — example of how relations are declared in this crate. Keep the relation style consistent when removing the status relation

## Acceptance Criteria
- [ ] `entity::advisory::Model` has a `status: AdvisoryStatus` field and no `status_id` field
- [ ] `AdvisoryStatus` maps to PostgreSQL enum `advisory_status_enum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] No `advisory_status` entity, module or relation remains in the `entity` crate
- [ ] Parsing an unknown status string into `AdvisoryStatus` returns an error. There is no silent default
- [ ] `cargo build -p entity` succeeds

## Test Requirements
- [ ] Unit test: each `AdvisoryStatus` variant round-trips through its string form (`New`, `Analyzing`, `Fixed`, `Rejected`)
- [ ] Unit test: parsing an unknown string (e.g., `"Closed"`, `""`) returns an error
- [ ] Integration check: with the Task 2 migration applied, inserting and loading an `advisory::ActiveModel` with each status succeeds against PostgreSQL

## Verification Commands
- `cargo build -p entity` — compiles without errors
- `cargo test -p entity` — enum round-trip tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add reversible migration replacing advisory_status table with advisory_status_enum column
