## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the internal architecture documentation to reflect the schema change delivered by feature TC-9005 (Drop status table and migrate to enum column).

What changed: the `advisory_status` lookup table has been dropped and replaced by a PostgreSQL enum type `advisory_status_enum` (values `New`, `Analyzing`, `Fixed`, `Rejected`) stored directly in the new `advisory.status` column; `advisory.status_id` has been removed; advisory queries no longer join a lookup table; the ingestion pipeline writes the enum value directly; and the SeaORM `advisory` entity exposes an `AdvisoryStatus` enum.

Doc impact type: **Updates to existing content** (Minor) — update internal architecture docs to reflect the schema change. No external API documentation changes are needed (the API response shape is unchanged; status is still a string). Reference material: SeaORM enum mapping documentation (`DeriveActiveEnum`).

Feature reference: TC-9005.

## Acceptance Criteria
- [ ] Internal architecture docs describe `advisory.status` as an `advisory_status_enum` column with the four values and no longer mention the `advisory_status` table or `advisory.status_id`
- [ ] Docs explain how the SeaORM `AdvisoryStatus` enum maps to the PostgreSQL enum, referencing SeaORM enum mapping
- [ ] Docs note that adding a new status now requires a migration altering `advisory_status_enum`
- [ ] No external/user-facing API documentation is changed

## Test Requirements
- [ ] Review the updated docs against the merged migration, entity, service, and ingestion changes on the `TC-9005` branch and confirm every described table/column/enum name matches the implementation
- [ ] Confirm no remaining documentation references `advisory_status` as a table or `status_id` as a column

## Dependencies
- Depends on: Task 2 — Add atomic migration replacing advisory_status table with advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
- Depends on: Task 4 — Update advisory queries to use status enum column instead of join
- Depends on: Task 5 — Update advisory ingestion to write status enum directly
