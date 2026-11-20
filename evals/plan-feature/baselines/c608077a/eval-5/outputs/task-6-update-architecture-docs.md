# Task 6 — Update internal architecture documentation for advisory status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the internal architecture documentation to reflect the schema change delivered by feature TC-9005 (Drop status table and migrate to enum column).

What changed: the `advisory_status` lookup table and the `advisory.status_id` foreign key have been replaced by a PostgreSQL enum type `advisory_status_enum` (values `New`, `Analyzing`, `Fixed`, `Rejected`) stored directly in the `advisory.status` column. Advisory queries no longer join a lookup table, the SeaORM `advisory` entity exposes a typed `AdvisoryStatus` enum, and the ingestion pipeline writes enum values directly and rejects unknown statuses.

Doc impact type: **Updates to existing content** (Feature "Documentation Considerations": Doc Impact: Minor — update internal architecture docs to reflect schema change).

Details from Documentation Considerations:
- User purpose: no external API documentation changes are needed — the advisory API response shape is unchanged (status remains a string).
- Reference material: SeaORM enum mapping documentation (`DeriveActiveEnum`).

Reference: Feature TC-9005.

## Acceptance Criteria
- [ ] Internal architecture documentation describes advisory status as the `advisory.status` column of PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] All references to the `advisory_status` lookup table and `advisory.status_id` foreign key are removed or marked as historical (dropped by the TC-9005 migration)
- [ ] The documentation notes that new status values require a new migration (`ALTER TYPE ... ADD VALUE`) plus an `AdvisoryStatus` enum variant, and links to the SeaORM enum mapping documentation
- [ ] No external/user-facing API documentation is changed

## Test Requirements
- [ ] Review the updated documentation against the merged migration, `entity/src/advisory.rs`, and the advisory service to confirm it accurately reflects the implemented schema and behaviour
- [ ] Confirm no remaining documentation references describe the dropped `advisory_status` table as current

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column
- Depends on: Task 4 — Replace advisory_status joins with advisory.status column in advisory and search queries
- Depends on: Task 5 — Write advisory status enum directly in advisory ingestion pipeline
