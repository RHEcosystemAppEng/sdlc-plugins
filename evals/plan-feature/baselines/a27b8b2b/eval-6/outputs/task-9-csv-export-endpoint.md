# Task 9: Add CSV export endpoint for remediation data (non-MVP)

**Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add a `GET /api/v2/remediation/export` endpoint that exports remediation data as a CSV file for management reporting. This is a non-MVP requirement to support security managers who need to generate reports for remediation SLA tracking. The endpoint streams CSV data with columns for product, severity, status, and vulnerability details.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/export.rs` — GET /api/v2/remediation/export handler returning CSV response

## Files to Modify
- `modules/fundamental/src/remediation/endpoints/mod.rs` — register the export route
- `modules/fundamental/src/remediation/service/mod.rs` — add method for fetching flat vulnerability data suitable for CSV export

## API Changes
- `GET /api/v2/remediation/export` — NEW: returns CSV file with Content-Type `text/csv` and Content-Disposition header for download. Columns: product_name, severity, status, vulnerability_id, description

## Implementation Notes
- Implement the CSV export as a streaming response to handle large datasets efficiently. Use Axum's streaming response capabilities rather than buffering the entire CSV in memory.
- Set appropriate response headers: `Content-Type: text/csv` and `Content-Disposition: attachment; filename="remediation-report.csv"`.
- Reuse the aggregation query logic from the RemediationService created in Tasks 2-3, but fetch individual rows rather than aggregated counts.
- Follow the error handling pattern: `Result<T, AppError>` with `.context()`.
- This is a non-MVP feature; it should not block the release of the core remediation dashboard.

## Reuse Candidates
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with existing query patterns; extend for flat data export
- `common/src/db/query.rs` — query builder helpers; reuse for any filtering support on the export endpoint
- `common/src/error.rs` — AppError for error handling

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/export` returns a valid CSV file
- [ ] CSV includes columns: product_name, severity, status, vulnerability_id, description
- [ ] Response includes correct Content-Type and Content-Disposition headers
- [ ] Large datasets (10,000+ vulnerabilities) are handled without memory issues via streaming
- [ ] Error cases return appropriate AppError responses

## Test Requirements
- [ ] Integration test verifying the export endpoint returns valid CSV with correct headers
- [ ] Integration test verifying CSV content matches expected data for a known dataset
- [ ] Integration test verifying streaming works for large datasets without timeout

## Verification Commands
- `cargo test --test api remediation` — run remediation endpoint tests including export
- `cargo clippy --all-targets` — verify no lint warnings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation summary endpoint (module structure and service)
