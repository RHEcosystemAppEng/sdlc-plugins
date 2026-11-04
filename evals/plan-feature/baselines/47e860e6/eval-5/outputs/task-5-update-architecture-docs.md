## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the internal architecture documentation to reflect the schema change delivered by TC-9005 (Drop status table and migrate to enum column).

**What changed:** the `advisory_status` lookup table and the `advisory.status_id` foreign key have been removed. Advisory lifecycle status (`New`, `Analyzing`, `Fixed`, `Rejected`) is now stored directly on the `advisory` table in a `status` column of the PostgreSQL enum type `advisory_status_enum`, mapped to the SeaORM `AdvisoryStatus` active enum. Advisory queries (list with status filter, get, search) no longer join a lookup table. The ingestion pipeline writes the enum value directly and rejects unknown status strings.

**Doc impact type:** Updates to existing content (Minor). This means updating the internal architecture docs that describe the advisory data model. Per the Feature's Documentation Considerations, no external or API documentation changes are needed, because the API response shape is unchanged.

**Reference material:** SeaORM enum mapping documentation (`DeriveActiveEnum`).

**Feature reference:** TC-9005.

## Acceptance Criteria
- [ ] Internal architecture documentation describes `advisory.status` as an `advisory_status_enum` column with the values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] All references to the `advisory_status` lookup table and `advisory.status_id` are removed from, or marked as historical in, the internal docs
- [ ] The docs mention the SeaORM `AdvisoryStatus` enum mapping and link to the SeaORM enum mapping documentation
- [ ] No external or API documentation is changed, because the response shape is unchanged

## Test Requirements
- [ ] Review the updated docs against the merged code on `TC-9005` (the migration, `entity/src/advisory.rs`, and the advisory service) and confirm the described schema and enum values match exactly
- [ ] Confirm that no remaining doc text describes the join-based status lookup

## Dependencies
- Depends on: Task 2 — Add advisory_status_enum migration
- Depends on: Task 3 — Update SeaORM entities and advisory query layer to use the status enum column
- Depends on: Task 4 — Write advisory status enum directly in the ingestion pipeline
