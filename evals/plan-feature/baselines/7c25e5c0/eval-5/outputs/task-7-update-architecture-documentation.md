## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation should describe the new enum-based status model, the rationale for the migration (eliminated join overhead, simplified queries), and the four valid status values (New, Analyzing, Fixed, Rejected).

Documentation impact type: Updates to existing content (internal architecture docs).

Reference: Feature TC-9005 — Drop status table and migrate to enum column.

## Acceptance Criteria
- [ ] Architecture documentation accurately reflects the `advisory_status_enum` column on the `advisory` table
- [ ] Documentation describes the four valid status values: New, Analyzing, Fixed, Rejected
- [ ] Documentation mentions the rationale for the migration (eliminated join, performance improvement)
- [ ] No references to the `advisory_status` lookup table remain in architecture docs (or are explicitly noted as removed)

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema
- [ ] Documentation correctly describes the SeaORM enum mapping pattern used

## Dependencies
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests
