## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Implement the `GET /api/v2/remediation/export` endpoint that returns a CSV file containing the remediation report for management reporting. The CSV includes vulnerability details with severity, product, and remediation status columns. This is a non-MVP requirement from TC-9006 that supports management reporting on remediation SLAs.

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — add route for the export endpoint
- `modules/fundamental/src/remediation/service/mod.rs` — add export query method to `RemediationService`

## Files to Create
- `modules/fundamental/src/remediation/endpoints/export.rs` — `GET /api/v2/remediation/export` handler returning CSV response

## API Changes
- `GET /api/v2/remediation/export` — NEW: returns a CSV file with Content-Type `text/csv` and Content-Disposition header for file download. Columns: vulnerability_id, severity, product, status, description

## Implementation Notes
- The export handler should return a raw `Response` with `Content-Type: text/csv` and `Content-Disposition: attachment; filename="remediation-report.csv"` headers rather than using the standard JSON response pattern.
- Query all vulnerability records using the existing `RemediationService` methods from Tasks 2 and 3. Stream results if possible to handle large datasets.
- Use the `csv` crate (add to `Cargo.toml`) for CSV serialization, or manually format CSV rows if the crate is not desired.
- Follow error handling conventions: return `Result<Response, AppError>` with `.context()` wrapping.
- Must handle up to 10,000 vulnerabilities without timeout or memory issues.
- Per repo conventions: register the route in `endpoints/mod.rs` following the existing pattern.

## Reuse Candidates
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` methods for querying vulnerability data (created in Tasks 2-3)
- `common/src/error.rs` — `AppError` for error handling

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/export` returns 200 with Content-Type `text/csv`
- [ ] Response includes Content-Disposition header for file download
- [ ] CSV contains columns: vulnerability_id, severity, product, status
- [ ] CSV data matches the remediation data served by the summary and by-product endpoints
- [ ] Export handles 10,000+ vulnerabilities without timeout

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/export` returns 200 with CSV content type
- [ ] Integration test: verify CSV content contains expected headers and data rows
- [ ] Integration test: verify Content-Disposition header is set for file download

## Verification Commands
- `cargo test --test api remediation` — runs all remediation endpoint integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation summary aggregation service and endpoint (reuses RemediationService)
