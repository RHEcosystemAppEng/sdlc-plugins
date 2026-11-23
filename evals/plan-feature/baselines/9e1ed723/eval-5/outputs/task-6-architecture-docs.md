**Summary:** Update internal architecture docs for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the internal architecture documentation to reflect the schema change delivered by TC-9005.

**What changed:** the `advisory_status` lookup table and the `advisory.status_id` foreign key are removed. Advisory lifecycle status is now stored directly on `advisory.status`, a PostgreSQL enum column of type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`. The column is mapped in SeaORM as the `AdvisoryStatus` active enum. Advisory queries no longer join a status table. The ingestion pipeline writes the enum value directly and rejects unknown status values. The public API response shape is unchanged: status is still returned as a string.

**Doc impact type:** Updates to existing content.

**Details from Documentation Considerations:**
- Doc impact: Minor. Update internal architecture docs to reflect the schema change.
- User purpose: no external API documentation changes needed.
- Reference material: SeaORM enum mapping documentation (link it for maintainers who add statuses in future).

Note for maintainers: adding a new status now requires a migration (`ALTER TYPE advisory_status_enum ADD VALUE ...`) plus an `AdvisoryStatus` variant. A row insert into a lookup table is no longer enough.

Feature reference: TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture/data-model documentation describes `advisory.status` as an `advisory_status_enum` column and no longer mentions the `advisory_status` table or `status_id`
- [ ] Documentation explains how to add a new advisory status (migration plus `AdvisoryStatus` variant) and links the SeaORM enum mapping reference
- [ ] Documentation states that the public API response for advisory status is unchanged
- [ ] No external/user-facing API documentation is changed

## Test Requirements
- [ ] Review the documentation against the merged implementation (migration, entity, service, ingestion) and confirm the enum name, values and behavior match exactly
- [ ] Confirm that no remaining documentation references `advisory_status` as a table or `status_id` as a column
- [ ] Confirm that the documented procedure for adding a status is consistent with the migration and entity code

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add reversible migration replacing advisory_status table with advisory_status_enum column
- Depends on: Task 3 — Update SeaORM Advisory entity to use status enum column
- Depends on: Task 4 — Remove advisory_status join from advisory and search queries
- Depends on: Task 5 — Write advisory status enum directly in ingestion pipeline
