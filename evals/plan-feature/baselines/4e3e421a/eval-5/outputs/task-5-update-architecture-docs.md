# Task 5 — Update internal architecture docs for advisory status enum schema change

**Summary:** Update internal architecture docs for advisory status enum schema change
**Labels:** ai-generated-jira
**Priority:** High (inherited from TC-9005)
**Fix Versions:** RHTPA 2.0.0 (inherited from TC-9005, fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the internal architecture documentation for the TC-9005 schema change. The `advisory_status` lookup table and the `advisory.status_id` foreign key have been replaced by an `advisory.status` column of the PostgreSQL enum type `advisory_status_enum`, with the values `New`, `Analyzing`, `Fixed`, and `Rejected`. Advisory queries no longer join a lookup table, and the ingestion pipeline writes enum values directly.

- **Doc impact type:** Updates to existing content (Feature: "Doc Impact: Minor — update internal architecture docs to reflect schema change")
- **User purpose:** internal only. No external API documentation changes are needed because the API response shape is unchanged and `status` is still a string.
- **Reference material:** SeaORM enum mapping documentation (`DeriveActiveEnum`), which describes how the Rust `AdvisoryStatus` enum maps to the PostgreSQL enum
- **Feature:** TC-9005 — Drop status table and migrate to enum column

## Acceptance Criteria
- [ ] The internal architecture and data-model documentation no longer describes the `advisory_status` table or the `advisory.status_id` foreign key
- [ ] The documentation describes `advisory.status` as an `advisory_status_enum` column with its four values
- [ ] The documentation states that adding a new status value requires a migration (`ALTER TYPE advisory_status_enum ADD VALUE ...`) plus an update to the `AdvisoryStatus` Rust enum
- [ ] No external or user-facing API documentation is changed

## Test Requirements
- [ ] Review the updated docs against the merged migration, entity, and ingestion code on `TC-9005`, and confirm the table, column, type, and value names match the implementation exactly
- [ ] Confirm that `grep -rn "advisory_status" ` across the repository's docs returns only references to `advisory_status_enum`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
- Depends on: Task 3 — Update SeaORM advisory entity and advisory queries to use the status enum column
- Depends on: Task 4 — Update advisory ingestion pipeline to write status enum values directly
