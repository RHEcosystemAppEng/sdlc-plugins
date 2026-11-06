**Summary:** Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to match the new schema from Task 2. The `advisory` entity gets a `status` field typed as a Rust enum mapped to the PostgreSQL `advisory_status_enum`. The `status_id` field and the relation to the `advisory_status` entity are removed. The `advisory_status` entity is deleted.

This task introduces the shared `AdvisoryStatus` Rust type. Task 4 (query and service layer) and Task 5 (ingestion pipeline) use it.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` with `pub status: AdvisoryStatus`. Add the `AdvisoryStatus` enum (`DeriveActiveEnum`, `rs_type = "String"`, `db_type = "Enum"`, `enum_name = "advisory_status_enum"`) with variants `New`, `Analyzing`, `Fixed`, `Rejected`. Remove the `Relation` and `Related` impls that point at `advisory_status`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export, if present

## Implementation Notes
- **Repository discrepancy:** the Feature says to "remove `entity/advisory_status.rs`". The repository listing for `entity/src/` has `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs` and `package_license.rs`, but no `advisory_status.rs`. Before you change anything, check whether the lookup entity exists:
  - as `entity/src/advisory_status.rs`: delete it and its `mod` line in `entity/src/lib.rs`;
  - or inline inside `entity/src/advisory.rs`: remove it there.
  Record which case applied in the PR description. If the file does not exist, do not create it.
- Define the enum with SeaORM's `DeriveActiveEnum` and `EnumIter`. Use `#[sea_orm(string_value = "New")]` and so on, so the values match the PostgreSQL enum labels created in Task 2 exactly, including case.
- Derive `Serialize`/`Deserialize` on `AdvisoryStatus` with the variant names as the serialized string. The API response must not change ("status is still a string", see Customer Considerations). Add `Display` and `FromStr`, or an equivalent `TryFrom<&str>`, so that:
  - Task 4 can parse the status query filter;
  - Task 5 can map feed strings.
  `FromStr` must return an error for unknown strings. Do not fall back to a default variant (fail closed, see Task 5).
- Follow the existing entity conventions in `entity/src/advisory.rs` and `entity/src/sbom_advisory.rs`: `DeriveEntityModel`, `Relation` enum, and `ActiveModelBehavior`. Keep the remaining relations, such as `sbom_advisory`, unchanged.
- This change alters the `advisory::Model` shape, so code that reads `status_id` or joins `advisory_status` will stop compiling. Task 4 and Task 5 fix those call sites. On the feature branch, the PR for this task may be stacked with Task 4 and Task 5, or must at least build the `entity` crate on its own.
- Constraints (docs/constraints.md):
  - §2.1–2.3: Conventional Commit with the task-key footer and an `Assisted-by:` trailer.
  - §3.3: `gh pr create --base TC-9005`.
  - §5.1–5.4: scoped files, inspect before modifying, follow existing entity patterns.
  - §5.7: the `ActiveEnum` trait implementation must be complete.

## Reuse Candidates
- `entity/src/advisory.rs` — existing `advisory` entity definition to modify (`Model`, `Relation`, `ActiveModelBehavior`)
- `entity/src/sbom_advisory.rs` — sibling entity showing the crate's relation and `Related` impl conventions, to keep consistent after removing the `advisory_status` relation

## Acceptance Criteria
- [ ] `advisory::Model` has a `status: AdvisoryStatus` field and no `status_id` field
- [ ] `AdvisoryStatus` maps to PostgreSQL enum `advisory_status_enum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The `advisory` entity has no relation to `advisory_status`
- [ ] The `advisory_status` entity no longer exists in the `entity` crate, and `entity/src/lib.rs` does not declare it
- [ ] `AdvisoryStatus` serializes to and deserializes from the exact strings `"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`
- [ ] Parsing an unknown status string into `AdvisoryStatus` returns an error and never a default variant
- [ ] The `entity` crate compiles

## Test Requirements
- [ ] Unit test: round-trip each `AdvisoryStatus` variant through serde JSON and assert the string value matches the enum label
- [ ] Unit test: `FromStr`/`TryFrom` for each valid label succeeds. An unknown label (e.g., `"Unknown"`, `""`, `"fixed"`) returns `Err`
- [ ] Integration test (against the migrated test DB from Task 2): insert and read an `advisory::ActiveModel` with each status and assert the value persists

## Verification Commands
- `cargo build -p entity` — builds without errors
- `cargo test -p entity` — enum mapping tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add reversible migration converting advisory_status lookup table to advisory_status_enum column
