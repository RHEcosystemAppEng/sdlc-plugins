**Summary:** Update SeaORM advisory entity for status enum column
**Epic:** TC-9005: Advisory status schema migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to match the schema produced by Task 2: the `advisory` entity gains a `status` column backed by a Rust `AdvisoryStatus` enum mapped to PostgreSQL `advisory_status_enum`, and the `status_id` column, the relation to `advisory_status`, and the `advisory_status` entity are removed. The `AdvisoryStatus` enum becomes the single source of truth used by the service, search, and ingestion tasks.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` field and `advisory_status` relation with `status: AdvisoryStatus`; define the `AdvisoryStatus` enum
- `entity/src/lib.rs` — remove the `advisory_status` module declaration/re-export (if present); export `AdvisoryStatus`
- `entity/src/advisory_status.rs` — DELETE if present (path named by the Feature as `entity/advisory_status.rs`; not shown in the analyzed tree — confirm at implementation time)

## Implementation Notes
- Define the enum with SeaORM's active-enum derive:
  `#[derive(Debug, Clone, Copy, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)]`
  `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
  with variants `#[sea_orm(string_value = "New")] New`, `Analyzing`, `Fixed`, `Rejected` — string values must exactly match the Postgres enum labels created in Task 2.
- Add `Display`/`as_str` and a fallible `FromStr`/`TryFrom<&str>` on `AdvisoryStatus` so downstream code (Task 4 response mapping, Task 6 ingestion parsing) reuses one mapping instead of re-implementing string tables. `FromStr` must return an error for unknown values — never default.
- Follow existing entity patterns in `entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`, and `entity/src/package_license.rs` (`DeriveEntityModel`, `Relation` enum, `ActiveModelBehavior`). Remove the `Relation::AdvisoryStatus` variant and its `Related<advisory_status::Entity>` impl.
- If no `entity/src/advisory_status.rs` exists, the lookup model may be defined inline in `entity/src/advisory.rs`; remove it there instead.
- After this task the `modules/fundamental`, `modules/search`, and `modules/ingestor` crates will not compile until Tasks 4–6 land — expected on the `TC-9005` feature branch.
- Per CONVENTIONS.md §Framework: model the column with SeaORM (`DeriveActiveEnum`) rather than raw SQL strings. Applies: task modifies entity/src/advisory.rs matching the convention's Rust (`.rs`) SeaORM scope. Example: `entity/src/sbom.rs`.
- Constraints (docs/constraints.md): §2 commit rules (Jira ID footer, Conventional Commits, `Assisted-by:` trailer); §3 PR `--base TC-9005`, PR link posted to Jira; §5 scope limited to listed files, inspect before modifying, no duplicated functionality.

## Reuse Candidates
- `entity/src/advisory.rs::Model` — existing advisory entity to modify in place
- `entity/src/sbom_advisory.rs` — reference for relation definitions to keep intact

## Acceptance Criteria
- [ ] `entity::advisory::Model` has `status: AdvisoryStatus` and no `status_id` field
- [ ] `AdvisoryStatus` maps to Postgres enum `advisory_status_enum` with variants New, Analyzing, Fixed, Rejected
- [ ] `AdvisoryStatus` parsing from an unknown string returns an error
- [ ] No `advisory_status` entity, module, or relation remains in the `entity` crate
- [ ] `cargo build -p entity` succeeds

## Test Requirements
- [ ] Unit test: `AdvisoryStatus` round-trips each variant to/from its string value
- [ ] Unit test: parsing an unknown status string (e.g., `"Closed"`) returns an error
- [ ] Integration (with Task 2 schema): insert and read back an `advisory` row via the entity for each status value

## Verification Commands
- `cargo build -p entity` — compiles
- `cargo test -p entity` — tests pass
- `grep -rn "advisory_status::" entity/src` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add migration replacing advisory_status table with advisory_status_enum column
