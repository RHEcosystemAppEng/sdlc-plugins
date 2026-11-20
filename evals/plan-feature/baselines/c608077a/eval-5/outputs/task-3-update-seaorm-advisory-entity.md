# Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema created in Task 2: the `advisory` entity gets a `status` field backed by a Rust enum mapped to the PostgreSQL `advisory_status_enum` type, and the `status_id` field plus the relation to the `advisory_status` entity are removed. The `advisory_status` entity is deleted. This gives the service layer (Task 4) and ingestion pipeline (Task 5) a typed enum to read and write directly, with no join.

## Files to Modify
- `entity/src/advisory.rs` — replace the `status_id` column and its `advisory_status` relation with a `status: AdvisoryStatus` column; add the `AdvisoryStatus` enum deriving `DeriveActiveEnum` mapped to `advisory_status_enum`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration/re-export (if present) and export the new `AdvisoryStatus` enum as needed by consumers

## Implementation Notes
- Define the enum in `entity/src/advisory.rs` (or alongside it) using SeaORM's active enum support:
  `#[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)]`
  `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
  with variants `#[sea_orm(string_value = "New")] New`, `Analyzing`, `Fixed`, `Rejected`. The `string_value`s must match the enum labels created by the Task 2 migration exactly.
- Serialization must keep the API response shape unchanged (Customer Considerations: status is still a string). Ensure `serde` serializes the variants to the same strings the API currently returns (`"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`); add `#[serde(rename = ...)]` if the current API strings differ in case.
- Provide a fallible conversion from string (e.g., `impl FromStr for AdvisoryStatus` / `TryFrom<&str>`) returning an error for unknown values; Task 5 uses it to map feed status strings. Do not provide a lossy default variant.
- The Feature names `entity/advisory_status.rs` for removal. This file does not appear in the repository structure manifest (`entity/src/` lists `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs`, `package_license.rs`). At implementation time, verify whether `entity/src/advisory_status.rs` exists: if it does, delete it and remove its `mod` declaration from `entity/src/lib.rs`; if the lookup entity is instead defined inline in `entity/src/advisory.rs`, remove it there.
- Remove the `Relation::AdvisoryStatus` variant and the `Related<advisory_status::Entity>` impl from `entity/src/advisory.rs`; keep existing relations such as the one to `entity/src/sbom_advisory.rs` intact.
- Follow the existing entity style used in `entity/src/sbom.rs` and `entity/src/package.rs` (`DeriveEntityModel`, `Relation` enum, `ActiveModelBehavior`).
- Per CONVENTIONS.md §Framework: model database tables with SeaORM entities (`DeriveEntityModel`, `DeriveActiveEnum`). Applies: task modifies entity/src/advisory.rs matching the convention's SeaORM database `.rs` scope. See `entity/src/sbom.rs` for the established entity pattern.
- Constraints (docs/constraints.md): commits must reference the Jira task ID in the footer (§2.1), follow Conventional Commits (§2.2), and include an `Assisted-by:` trailer (§2.3); the PR must be opened with `--base TC-9005` (§3.3) and its link posted to the Jira task (§3.2); changes scoped to the listed files (§5.1), inspected before modification (§5.2), no duplicated functionality (§5.4), and the entity must fully implement the SeaORM traits it derives (§5.7).

## Reuse Candidates
- `entity/src/advisory.rs` — existing Advisory entity; modify in place rather than creating a new entity
- `entity/src/sbom.rs` — sibling SeaORM entity demonstrating the project's entity derive and relation conventions

## Acceptance Criteria
- [ ] `entity::advisory::Model` has a `status: AdvisoryStatus` field mapped to the `status` column of type `advisory_status_enum`
- [ ] `AdvisoryStatus` has exactly four variants (`New`, `Analyzing`, `Fixed`, `Rejected`) whose DB string values match the Task 2 enum labels
- [ ] `status_id` field and the relation to `advisory_status` are removed from the advisory entity
- [ ] The `advisory_status` entity no longer exists in the `entity` crate and is not referenced from `entity/src/lib.rs`
- [ ] Converting an unknown string to `AdvisoryStatus` returns an error (no silent default)
- [ ] `AdvisoryStatus` serializes to the same status strings the API currently returns

## Test Requirements
- [ ] Unit test: each `AdvisoryStatus` variant round-trips through its DB string value and serde JSON string
- [ ] Unit test: parsing an unknown status string (e.g., `"Unknown"`, empty string) returns an error
- [ ] Integration test (via `tests/api/advisory.rs` in Task 4): an advisory inserted with each enum value can be read back through the entity with the same status

## Verification Commands
- `cargo test -p entity` — entity unit tests pass
- `cargo build -p entity` — entity crate compiles with no reference to `advisory_status`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
