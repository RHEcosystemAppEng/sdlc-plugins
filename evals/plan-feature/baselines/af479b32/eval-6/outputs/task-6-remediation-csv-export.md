## Repository
trustify-backend

## Target Branch
main

## Description
Add a CSV export endpoint for the remediation report to support management reporting on remediation SLAs. This is a non-MVP requirement. The endpoint returns the remediation data (by-product breakdown with severity and status details) as a downloadable CSV file. This allows security managers to export the current remediation status for offline reporting and stakeholder communication.

## Files to Create
- `modules/remediation/src/endpoints/export.rs` — GET /api/v2/remediation/export handler returning CSV response

## Files to Modify
- `modules/remediation/src/endpoints/mod.rs` — Register the export route
- `tests/api/remediation.rs` — Add integration tests for the CSV export endpoint

## API Changes
- `GET /api/v2/remediation/export` — NEW: Returns remediation report as CSV (Content-Type: text/csv) with columns for product, severity, status, and count

## Implementation Notes
- Follow the endpoint handler pattern in `modules/remediation/src/endpoints/summary.rs` (created in Task 1) for handler structure and error handling.
- The CSV response should set the `Content-Type: text/csv` header and include a `Content-Disposition: attachment; filename="remediation-report.csv"` header for browser download support.
- Reuse the RemediationService aggregation queries from Task 1 to generate the export data — do not duplicate the aggregation logic.
- Use the existing error handling pattern with `Result<T, AppError>` and `.context()` wrapping.
- Consider using the `csv` crate for CSV serialization, or manually format the output if adding a dependency is undesirable.
- The export should include all products and all severity/status combinations, not just a summary — this provides the detailed view needed for management reporting.

## Reuse Candidates
- `modules/remediation/src/service/mod.rs::RemediationService` — Reuse the existing aggregation queries for generating export data; do not duplicate query logic
- `modules/remediation/src/model/product.rs::ProductRemediation` — Reuse the product remediation model for CSV row data
- `common/src/error.rs::AppError` — Standard error type for endpoint handlers

## Acceptance Criteria
- [ ] GET /api/v2/remediation/export returns a CSV response with Content-Type: text/csv
- [ ] The response includes a Content-Disposition header for download
- [ ] The CSV includes columns for product name, severity, status, and count
- [ ] The CSV includes data for all products with remediation entries
- [ ] The endpoint returns an empty CSV (headers only) when no data exists
- [ ] The endpoint uses existing aggregation logic from RemediationService (no duplicated queries)

## Test Requirements
- [ ] Integration test: GET /api/v2/remediation/export returns 200 with text/csv content type
- [ ] Integration test: Export CSV contains correct headers and data rows
- [ ] Integration test: Export returns headers-only CSV when no data exists
- [ ] Follow the integration test pattern in `tests/api/remediation.rs`

## Verification Commands
- `cargo test --test api remediation` — All remediation integration tests pass including export tests

## Dependencies
- Depends on: Task 1 — Create remediation module with summary endpoint
