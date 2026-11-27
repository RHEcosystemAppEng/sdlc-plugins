**Summary:** Update internal architecture docs for advisory status enum
**Epic:** TC-9005: Feature branch delivery and documentation

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the TC-9005 schema change (Feature TC-9005 — Drop status table and migrate to enum column).

- **What changed:** the `advisory_status` lookup table and `advisory.status_id` FK were replaced by a PostgreSQL enum type `advisory_status_enum` (New, Analyzing, Fixed, Rejected) and an `advisory.status` column. Advisory queries (service, endpoints, search) no longer join a lookup table, and ingestion writes the enum value directly. The SeaORM `AdvisoryStatus` active enum in the `entity` crate is the single mapping.
- **Doc impact type:** Updates to existing content (Minor — internal architecture docs).
- **User purpose:** internal only; no external API documentation changes are needed (API response shape unchanged).
- **Reference material:** SeaORM enum mapping documentation (`DeriveActiveEnum`).

## Acceptance Criteria
- [ ] Internal architecture docs describe `advisory.status` as an `advisory_status_enum` column and no longer mention the `advisory_status` table or `status_id`
- [ ] Docs note how new status values would be added (new migration altering the enum + `AdvisoryStatus` variant)
- [ ] No external API documentation is changed

## Test Requirements
- [ ] Review the docs against the merged code on `TC-9005` (migration, entity, service, ingestion) and confirm they are accurate and complete
- [ ] Confirm no remaining doc references to the `advisory_status` table

## Dependencies
- Depends on: Task 2 — Add migration replacing advisory_status table with advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity for status enum column
- Depends on: Task 4 — Use advisory.status column in AdvisoryService and advisory endpoints
- Depends on: Task 5 — Use advisory.status column in SearchService
- Depends on: Task 6 — Write advisory status enum directly in ingestion pipeline
