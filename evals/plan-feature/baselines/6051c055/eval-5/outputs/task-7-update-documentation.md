# Task 7 — Update internal architecture documentation for advisory status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The Feature's Documentation Considerations indicate a minor doc impact: internal architecture docs need updating, but no external API documentation changes are needed since the API response shape is unchanged.

Documentation updates should cover:
- The removal of the `advisory_status` lookup table from the database schema
- The addition of the `advisory_status_enum` PostgreSQL enum type
- The new `status` column on the `advisory` table
- Updated entity relationship diagrams or data model descriptions
- Reference to SeaORM enum mapping for the `AdvisoryStatusEnum` Rust type

Doc impact type: Updates to existing content.

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new schema (enum column replacing lookup table)
- [ ] Data model descriptions show the `advisory` table with a `status` enum column instead of `status_id` FK
- [ ] The removed `advisory_status` table is no longer referenced in any architecture docs
- [ ] Documentation covers the `AdvisoryStatusEnum` type and its mapping to PostgreSQL

## Test Requirements
- [ ] Verify documentation accurately describes the current schema after migration
- [ ] Verify no stale references to the `advisory_status` lookup table remain in documentation
- [ ] Verify documentation is consistent with the implemented feature behavior

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for status enum migration
