# Task 7: Update internal architecture documentation for schema change

## Repository
trustify-backend

## Target Branch
main

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. Document the removal of the `advisory_status` table, the addition of the `advisory_status_enum` type, and the simplified query pattern that no longer requires a join for status resolution.

## Acceptance Criteria
- [ ] Architecture documentation reflects that `advisory_status` lookup table has been removed
- [ ] Documentation describes the `advisory_status_enum` PostgreSQL type and its values (New, Analyzing, Fixed, Rejected)
- [ ] Documentation notes that advisory queries no longer join a status table
- [ ] Any entity-relationship diagrams or schema references are updated to show the enum column instead of the FK relationship

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema changes

## Dependencies
- None (documentation task, independent of feature branch)
