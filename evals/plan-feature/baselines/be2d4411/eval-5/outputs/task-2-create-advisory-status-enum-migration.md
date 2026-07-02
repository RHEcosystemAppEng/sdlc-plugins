## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the new `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = s.name FROM advisory_status s WHERE advisory.status_id = s.id`); (4) set the `status` column to NOT NULL after backfill; (5) drop the `status_id` foreign key constraint and column from `advisory`; (6) drop the `advisory_status` table. The migration must be atomic and reversible.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration module structure (SeaORM `MigrationTrait` implementation with `up` and `down` methods).
- The `up` method must execute the following steps in order: (1) create enum type, (2) add nullable column, (3) backfill, (4) alter to NOT NULL, (5) drop FK constraint, (6) drop `status_id` column, (7) drop `advisory_status` table.
- The `down` method must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for PostgreSQL-specific enum type creation (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`).
- The migration must be safe to run while the application is serving traffic (zero downtime requirement from NFRs).
- Per repo Key Conventions: framework is SeaORM for database operations; follow the existing migration pattern in `migration/src/`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration that demonstrates the `MigrationTrait` pattern including table creation, column definitions, and foreign key setup

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from `advisory_status` join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` FK constraint and column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible (`down` method restores previous schema)
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run migration against a test database with existing advisory data and verify all steps complete
- [ ] Verify `status` column is populated correctly by querying `advisory` table after migration
- [ ] Verify `advisory_status` table no longer exists after migration
- [ ] Run `down` migration and verify the schema is restored to original state
- [ ] Verify migration handles edge case of advisories with NULL `status_id` (if any)

## Verification Commands
- `cargo test --test migration` — verify migration runs and reverses successfully against test database

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:31ebb165060625142c1c2011805ecd956462bc65d560f4a95a10880d49845a79
