## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Description
Add a CSV export endpoint for the remediation report to support management reporting use cases. This endpoint allows security managers to download remediation data as a CSV file for offline analysis and reporting on remediation SLAs. This is a non-MVP requirement that extends the remediation module with an export capability.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/export.rs` — GET /api/v2/remediation/export/csv handler that serializes remediation data to CSV format

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Register the export route alongside existing remediation routes
- `tests/api/remediation.rs` — Add integration test for CSV export endpoint

## API Changes
- `GET /api/v2/remediation/export/csv` — NEW: Returns remediation data as a downloadable CSV file with Content-Type: text/csv header

## Implementation Notes
Per CONVENTIONS.md §Endpoint registration: add the export route in `endpoints/mod.rs` alongside the summary and by-product routes.
Applies: task modifies `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: the export handler must return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/export.rs` matching the convention's `.rs` file scope.

The CSV export handler should reuse the `RemediationService` from Task 1 to fetch the data, then serialize it to CSV format. Set the response Content-Type to `text/csv` and Content-Disposition to `attachment; filename="remediation-report.csv"`. Each row should include: vulnerability ID, severity, status, product, and any relevant timestamps.

Reference `modules/fundamental/src/sbom/endpoints/list.rs` for the handler pattern. For CSV serialization, consider using the `csv` crate or manual string formatting with comma-separated values.

## Reuse Candidates
- `modules/fundamental/src/remediation/service/mod.rs::RemediationService` — Reuse existing aggregation service to fetch data for CSV export
- `modules/fundamental/src/remediation/endpoints/summary.rs` — Reference handler pattern for consistent error handling and response construction

## Acceptance Criteria
- [ ] GET /api/v2/remediation/export/csv returns a valid CSV file with Content-Type: text/csv
- [ ] CSV includes headers: vulnerability ID, severity, status, product
- [ ] CSV data matches the remediation data returned by the summary and by-product endpoints
- [ ] Response includes Content-Disposition header for file download

## Test Requirements
- [ ] Integration test: GET /api/v2/remediation/export/csv returns 200 with Content-Type text/csv
- [ ] Integration test: CSV response body contains expected headers and data rows
- [ ] Integration test: CSV export handles empty dataset gracefully (returns headers only)

## Verification Commands
- `cargo test --test api remediation` — Run remediation integration tests including CSV export, expect all tests to pass
- `curl -v http://localhost:8080/api/v2/remediation/export/csv` — Verify CSV export returns text/csv content type

## Dependencies
- Depends on: Task 2 — Add remediation API endpoints with integration tests
