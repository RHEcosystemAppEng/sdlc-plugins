**Summary:** Update SeaORM advisory entity to use AdvisoryStatus enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the schema produced by Task 2: the `advisory` entity gets a `status` field typed as a new `AdvisoryStatus` active enum mapped to the PostgreSQL `advisory_status_enum` type, the `status_id` field and its relation to `advisory_status` are removed, and the `advisory_status` entity is removed from the crate.

Part of TC-9005.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` with `status: AdvisoryStatus`; add the `AdvisoryStatus` enum (`DeriveActiveEnum`); remove the `Relation`/`Related` impls pointing at `advisory_status`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration/re-export if present; re-export `AdvisoryStatus` if the crate's pattern re-exports types

## Implementation Notes
- The Feature references `entity/advisory_status.rs` for removal, but no such file exists in `entity/src/` per repository analysis. Before editing, grep the `entity` crate for `advisory_status` / `AdvisoryStatus` / `status_id` to find where the lookup-table entity or relation is actually defined (likely inline in `entity/src/advisory.rs` or a module declared in `entity/src/lib.rs`). If a separate `advisory_status` entity file is found under a different path, raise it with the reviewer rather than deleting an unlisted file (§5.1).
- Define the enum so the string values match the database and the existing API output exactly:
  ```rust
  #[derive(Debug, Clone, Copy, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)]
  #[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
  pub enum AdvisoryStatus {
      #[sea_orm(string_value = "New")] New,
      #[sea_orm(string_value = "Analyzing")] Analyzing,
      #[sea_orm(string_value = "Fixed")] Fixed,
      #[sea_orm(string_value = "Rejected")] Rejected,
  }
  ```
  Serde serialization must produce `"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"` so the API response shape (status is still a string) is unchanged.
- Provide a fallible conversion from a status string (`impl FromStr` / `TryFrom<&str>`) returning an error for unknown values — Task 5 (ingestion) uses it; it must not fall back to a default variant.
- Follow the existing entity style in `entity/src/sbom.rs` and `entity/src/sbom_advisory.rs` (`DeriveEntityModel`, `Relation` enum, `ActiveModelBehavior`). Keep the `sbom_advisory` relation on `advisory` intact.
- Per CONVENTIONS.md §Framework: entities are SeaORM `DeriveEntityModel` definitions; map the enum with `DeriveActiveEnum` rather than a string column. Applies: task modifies entity/src/advisory.rs matching the convention's SeaORM `.rs` entity scope. Example: `entity/src/sbom.rs`.
- Constraints (docs/constraints.md): §1.4 scoped changes; §2.1–2.3 commit footer with task key, Conventional Commits, `Assisted-by:` trailer; §3.3 PR `--base TC-9005`; §5.1 only listed files; §5.2 inspect before modifying; §5.4 no duplicate status mapping logic; §5.7 ensure the entity's `Model`/`ActiveModel`/`Relation` contracts compile completely.

## Reuse Candidates
- `entity/src/advisory.rs` — existing advisory entity; the `status_id` field and lookup relation are replaced in place
- `entity/src/sbom_advisory.rs` — example of relation definitions in this crate; must remain compatible with the updated advisory entity

## Acceptance Criteria
- [ ] `entity::advisory::Model` has `status: AdvisoryStatus` and no `status_id` field
- [ ] `AdvisoryStatus` maps to the `advisory_status_enum` PostgreSQL type with string values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] No entity, relation, or module referencing `advisory_status` remains in the `entity` crate
- [ ] `AdvisoryStatus` serializes to the same strings previously returned by the API
- [ ] Parsing an unknown status string returns an error (no silent default)
- [ ] `cargo build -p entity` succeeds

## Test Requirements
- [ ] Unit test: each `AdvisoryStatus` variant round-trips through serde as `"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`
- [ ] Unit test: string → `AdvisoryStatus` conversion succeeds for the four valid values and returns an error for an unknown value (e.g., `"Pending"`) and an empty string
- [ ] Integration test: insert and read back an advisory with each status against the migrated test database

## Verification Commands
- `cargo test -p entity` — passes
- `grep -rn "advisory_status\b\|status_id" entity/src` — no matches (other than the `advisory_status_enum` type name)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add advisory status enum migration
