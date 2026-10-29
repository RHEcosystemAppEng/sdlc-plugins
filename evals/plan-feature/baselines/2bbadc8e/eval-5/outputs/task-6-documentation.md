## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation should describe the new schema structure, the rationale for the change (eliminating join overhead, simplifying queries), and the enum values (New, Analyzing, Fixed, Rejected).

Doc impact type: Updates to existing content
Details: Update internal architecture docs to reflect schema change. No external API documentation changes needed since the response shape remains identical.

Reference: Feature TC-9005

## Acceptance Criteria
- [ ] Internal architecture documentation accurately describes the `advisory.status` enum column replacing the `advisory_status` lookup table
- [ ] Documentation lists the enum values: New, Analyzing, Fixed, Rejected
- [ ] Documentation notes that the public API response shape is unchanged (status remains a string)
- [ ] Documentation references SeaORM enum mapping for the `AdvisoryStatusEnum` type

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented schema change
- [ ] Verify documentation is consistent with the actual database schema and entity definitions

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum conversion
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service layer and endpoints to use enum status
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
