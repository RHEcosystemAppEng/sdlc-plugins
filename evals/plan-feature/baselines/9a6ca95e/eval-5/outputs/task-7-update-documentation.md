## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the advisory_status lookup table to the advisory_status_enum column on the advisory table. The documentation should describe the new enum-based status model, the removal of the join, and the simplified query patterns. No external API documentation changes are needed since the response shape is unchanged.

## Files to Modify
- `README.md` — update any schema diagrams or data model descriptions that reference the advisory_status table or status_id foreign key

## Implementation Notes
- Document the new advisory_status_enum PostgreSQL type and its values (New, Analyzing, Fixed, Rejected)
- Remove references to the advisory_status lookup table from architecture descriptions
- Note that advisory queries no longer require a join for status filtering
- Reference SeaORM enum mapping documentation for developers who need to understand the DeriveActiveEnum pattern

## Acceptance Criteria
- [ ] Architecture documentation reflects the enum column instead of the lookup table
- [ ] No stale references to advisory_status table in documentation
- [ ] Schema descriptions show the direct status enum column on the advisory table

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema changes

## Dependencies
- Depends on: Task 2 — Database migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests
