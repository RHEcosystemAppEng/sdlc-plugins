## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema introduced by the TC-9005 migration: the `advisory` entity gains a `status` field backed by a Rust enum mapped to the PostgreSQL `advisory_status_enum` type, the `status_id` field and the relation to the `advisory_status` entity are removed, and the `advisory_status` entity is removed from the entity crate. This gives the service and ingestion layers a typed `AdvisoryStatus` value to use instead of joining the lookup table.

## Files to Modify
- `entity/src/advisory.rs` — add `AdvisoryStatus` enum (`DeriveActiveEnum`, `rs_type = "String"`, `db_type = "Enum"`, `enum_name = "advisory_status_enum"`) with variants `New`, `Analyzing`, `Fixed`, `Rejected`; replace the `status_id` column with `status: AdvisoryStatus`; remove the `advisory_status` relation and its `Related` impl
- `entity/src/lib.rs` — remove the `advisory_status` module declaration/re-export (if present)

## Implementation Notes
- The feature description names `entity/advisory_status.rs` as the lookup-table entity to remove, but that file does not appear in the analyzed repository structure (`entity/src/` lists `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs`, `package_license.rs`). At implementation time, check whether `entity/src/advisory_status.rs` exists: if it does, delete it and remove its `pub mod` line from `entity/src/lib.rs`; if the lookup entity is instead defined inline in `entity/src/advisory.rs`, remove it there. Record which case applied in the PR description.
- Map the enum string values exactly to the PostgreSQL labels created by Task 2 (`#[sea_orm(string_value = "New")]`, etc.), so the DB value and the serialized API value stay identical (the feature requires no user-facing response-shape change — status is still a string).
- Derive `Serialize`/`Deserialize` (and `utoipa::ToSchema` if the other entity enums/models in `entity/src/` do) on `AdvisoryStatus` so model structs in `modules/fundamental/src/advisory/model/` can expose it as a string without a manual mapping layer.
- Provide a single canonical string-to-enum conversion on `AdvisoryStatus` (e.g., `impl FromStr for AdvisoryStatus` returning an error for unknown values) — Task 5 (ingestion) and Task 4 (status filter parsing) reuse it rather than each writing their own match.
- Follow the existing entity style in `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs` (`DeriveEntityModel`, `Relation` enum, `ActiveModelBehavior`).
- This crate will not compile cleanly against downstream crates until Tasks 4 and 5 land on the `TC-9005` branch; that is expected in feature-branch mode. Keep this task scoped to the entity crate.
- Commit rules (docs/constraints.md §2): Conventional Commits (e.g., `refactor(entity): replace advisory status_id relation with AdvisoryStatus enum`), footer `Implements <task-key>`, `Assisted-by:` trailer.
- PR rules (docs/constraints.md §3): `gh pr create --base TC-9005`; post the PR link on this Jira task.
- Code change rules (docs/constraints.md §5): change only the files listed; verify the `ActiveEnum` implementation is complete (all four variants) before committing.

## Reuse Candidates
- `entity/src/advisory.rs` — existing Advisory entity to extend; keep column naming consistent
- `entity/src/sbom_advisory.rs` — example of relation definitions in this crate; use it to confirm the advisory relations that remain after removing the status relation

## Acceptance Criteria
- [ ] `entity::advisory::Model` has a `status: AdvisoryStatus` field and no `status_id` field
- [ ] `AdvisoryStatus` maps to the PostgreSQL enum `advisory_status_enum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` whose string values match the DB labels exactly
- [ ] No `advisory_status` entity, relation, or `Related<advisory_status::Entity>` impl remains in the `entity` crate
- [ ] `AdvisoryStatus` exposes a single string parse function that returns an error (not a default variant) for unknown values
- [ ] `AdvisoryStatus` serializes to the same string values the API returns today (`"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`)

## Test Requirements
- [ ] Unit test: round-trip each `AdvisoryStatus` variant through its string value and serde serialization, asserting the strings `"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`
- [ ] Unit test: parsing an unknown status string (e.g., `"Pending"`, `""`) returns an error
- [ ] Integration test (with Task 2 migration applied): insert and read back an advisory with each status via the SeaORM entity against the PostgreSQL test database

## Verification Commands
- `cargo build -p entity` — compiles without errors
- `cargo test -p entity` — enum tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add atomic migration replacing advisory_status table with advisory_status_enum column
