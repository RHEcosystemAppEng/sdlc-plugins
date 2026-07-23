# Task 7: Document remediation dashboard and aggregation endpoints

## Repository
trustify-backend

## Target Branch
main

## Description
Create documentation for the new vulnerability remediation tracking dashboard and its backend aggregation endpoints. The Feature's Documentation Considerations indicate New Content is required: security teams need a user guide for the remediation dashboard, and API consumers need an endpoint reference for the aggregation APIs. This documentation task covers:

- **New Content**: User guide for the remediation dashboard at `/remediation`, explaining summary cards, progress chart, and filterable vulnerability table
- **New Content**: API reference for `GET /api/v2/remediation/summary`, `GET /api/v2/remediation/by-product`, and `GET /api/v2/remediation/export` endpoints
- **User purpose**: Security managers tracking remediation SLAs need a guide for using the dashboard; API consumers need endpoint reference with request/response examples

Reference feature: TC-9006

## Acceptance Criteria
- [ ] API reference documentation exists for all three remediation endpoints (summary, by-product, export) with request parameters and response schemas
- [ ] User guide documentation exists for the remediation dashboard page, covering summary cards, progress chart, and filterable vulnerability table
- [ ] Documentation covers the filtering capabilities (by severity, product, status) with usage examples
- [ ] Documentation covers the CSV export feature for management reporting
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API reference accurately reflects the actual endpoint paths, parameters, and response shapes
- [ ] Verify user guide accurately describes the dashboard UI components and their behavior
- [ ] Verify all documented filter options match the implemented filter capabilities
- [ ] Verify CSV export documentation matches the actual export format and headers

## Dependencies
- Depends on: Task 1 -- Create remediation module with summary aggregation endpoint
- Depends on: Task 2 -- Add per-product remediation breakdown endpoint
- Depends on: Task 3 -- Add CSV export endpoint for remediation report
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard
