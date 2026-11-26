**Summary:** Update internal architecture documentation for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the TC-9005 schema change: advisory lifecycle status is now stored in the `advisory.status` column of PostgreSQL enum type `advisory_status_enum` (`New`, `Analyzing`, `Fixed`, `Rejected`), and the `advisory_status` lookup table and `advisory.status_id` foreign key have been removed. Ingestion writes the enum value directly, and advisory queries no longer join a lookup table.

- **Doc impact type:** Updates to existing content (Minor)
- **Scope (from Documentation Considerations):** internal architecture docs only; no external API documentation changes are needed because the API response shape is unchanged (status remains a string).
- **Reference material:** SeaORM enum mapping documentation (`DeriveActiveEnum`).
- **Feature:** TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation describes `advisory.status` as an `advisory_status_enum` column with the four values
- [ ] All references to the `advisory_status` lookup table and `advisory.status_id` are removed or marked historical
- [ ] Documentation notes that ingestion maps feed status strings to the enum and rejects unknown values
- [ ] Documentation states that no external API change occurred (status is still a string)

## Test Requirements
- [ ] Review the updated documentation against the merged implementation (Tasks 2–5) and confirm table/column/type names and enum values match the code
- [ ] Confirm no remaining documentation references to `advisory_status` table or `status_id`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add advisory status enum migration
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
- Depends on: Task 4 — Replace advisory_status joins with advisory.status column in queries and endpoints
- Depends on: Task 5 — Write advisory status enum directly in ingestion pipeline
