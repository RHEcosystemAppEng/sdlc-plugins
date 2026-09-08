## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column on the `advisory` table. This is a documentation-only task -- no code changes are involved.

The feature TC-9005 replaces the `advisory_status` lookup table (joined via `status_id` FK) with a direct `advisory_status_enum` column on the `advisory` table. Documentation should reflect:
- The new schema design with the enum column
- Removal of the `advisory_status` lookup table from the data model
- The rationale for the change (eliminating join overhead, simplifying queries)
- Updated entity relationship descriptions

Doc impact type: Updates to existing content
Reference material: SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Architecture documentation reflects the new enum-based advisory status column
- [ ] Documentation accurately describes the data model without referencing the dropped `advisory_status` table
- [ ] Schema diagrams or entity relationship descriptions are updated if present
- [ ] No documentation references to the `advisory_status` lookup table or `status_id` FK column remain

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented schema changes
- [ ] Verify no references to the dropped `advisory_status` table remain in documentation
- [ ] Verify the described data model matches the actual schema after migration

## Dependencies
- Depends on: Task 4 -- Update advisory service and endpoints to use enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update advisory integration tests
