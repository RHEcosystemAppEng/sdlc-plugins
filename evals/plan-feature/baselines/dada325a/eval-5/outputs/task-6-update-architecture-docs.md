**Summary:** Update internal architecture docs for advisory status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the internal architecture documentation to describe the schema change from TC-9005 (Drop status table and migrate to enum column).

**What changed:** the `advisory_status` lookup table and the `advisory.status_id` foreign key are gone. Advisory lifecycle status is now stored directly in `advisory.status`, a column of the PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed` and `Rejected`. In SeaORM it maps to the `AdvisoryStatus` active enum in the `entity` crate.

- Advisory queries no longer join a lookup table.
- The ingestion pipeline writes enum values directly and rejects unknown status strings.
- The public API response shape is unchanged: `status` is still a string.

**Doc impact type:** Updates to existing content (Minor). Update the internal architecture docs to reflect the schema change.

**Details from Documentation Considerations:**
- User purpose: no external API documentation changes are needed. This is an internal, developer-facing update.
- Reference material: SeaORM enum mapping documentation (`DeriveActiveEnum`).

Feature reference: TC-9005.

## Acceptance Criteria
- [ ] Internal architecture docs describe advisory status as the `advisory.status` enum column (`advisory_status_enum`) and no longer mention the `advisory_status` lookup table or `status_id` FK
- [ ] The docs list the four enum values and state that adding a status needs a new migration (`ALTER TYPE … ADD VALUE`) plus an update to the `AdvisoryStatus` Rust enum
- [ ] The docs note that ingestion rejects unknown status strings instead of defaulting
- [ ] The docs reference the SeaORM enum mapping approach used
- [ ] No external API documentation is changed

## Test Requirements
- [ ] Review the updated docs against the merged implementation (migration, entity, service and ingestion code) to confirm table, column, type and enum names match exactly
- [ ] Confirm no remaining references to `advisory_status` (the table) or `status_id` exist in internal docs

## Dependencies
- Depends on: Task 2 — Add reversible migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity
- Depends on: Task 4 — Replace advisory_status joins with the advisory.status enum column in all advisory queries
- Depends on: Task 5 — Update advisory ingestion pipeline to write AdvisoryStatus enum values directly
