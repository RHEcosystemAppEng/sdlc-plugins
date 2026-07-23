# Task 3: Add CSV export endpoint for remediation report

## Repository
trustify-backend

## Target Branch
main

## Description
Add a CSV export endpoint to the remediation module that allows security managers to download the current remediation status as a CSV file for management reporting. This is a non-MVP requirement for TC-9006 -- it extends the remediation module established in Task 1 with an export capability. The endpoint returns the full remediation dataset (all vulnerabilities with their severity, status, product, and remediation details) formatted as CSV with appropriate headers.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/export.rs` -- `GET /api/v2/remediation/export` handler returning CSV response

## Files to Modify
- `modules/fundamental/src/remediation/service/remediation.rs` -- add `get_export_data()` method to `RemediationService` that returns the flat vulnerability list for export
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- register the export route
- `tests/api/remediation.rs` -- add integration tests for the CSV export endpoint

## API Changes
- `GET /api/v2/remediation/export` -- NEW: returns remediation data as CSV. Response Content-Type: `text/csv`. Includes headers: severity, status, product, vulnerability_id, description, created_date, resolved_date

## Implementation Notes
- Set the response `Content-Type` header to `text/csv` and include a `Content-Disposition: attachment; filename="remediation-report.csv"` header for browser download support.
  - Applies: task creates `modules/fundamental/src/remediation/endpoints/export.rs` matching the Rust endpoint file scope.
- Follow the error handling pattern: `Result<T, AppError>` with `.context()` wrapping.
  - Applies: task modifies `modules/fundamental/src/remediation/service/remediation.rs` matching the Rust service file scope.
- For CSV generation, consider using the `csv` crate or building CSV output manually with proper escaping. Check if a CSV dependency already exists in `Cargo.toml` before adding a new one.
- Reuse the aggregation query logic from `RemediationService` (established in Tasks 1 and 2) but return individual rows rather than aggregated counts.
- NFR: must handle up to 10,000 vulnerabilities in a single export without timeout.
- This is a non-MVP feature -- it can be deferred if higher-priority tasks require attention.

## Reuse Candidates
- `modules/fundamental/src/remediation/service/remediation.rs` -- `RemediationService` established in Task 1; extend with export data method
- `common/src/error.rs` -- `AppError` enum for error handling

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/export` returns HTTP 200 with Content-Type `text/csv`
- [ ] Response includes a `Content-Disposition` header for file download
- [ ] CSV output includes headers: severity, status, product, vulnerability_id, description, created_date, resolved_date
- [ ] CSV data correctly reflects the current remediation status from existing entity data
- [ ] Export handles up to 10,000 vulnerabilities without timeout

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/export` returns 200 with Content-Type `text/csv`
- [ ] Integration test: CSV output contains expected headers and data rows
- [ ] Integration test: empty dataset produces CSV with headers only
- [ ] Integration test: CSV values are properly escaped (commas, quotes in descriptions)

## Verification Commands
- `cargo test --test api remediation` -- expected: all remediation integration tests pass

## Dependencies
- Depends on: Task 1 -- Create remediation module with summary aggregation endpoint
