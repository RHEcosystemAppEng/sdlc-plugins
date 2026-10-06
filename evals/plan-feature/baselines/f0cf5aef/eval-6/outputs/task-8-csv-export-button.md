## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add a CSV export button to the remediation dashboard page that triggers a file download of the remediation report from the backend export endpoint. This is a non-MVP requirement from TC-9006 that supports management reporting on remediation SLAs.

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — add the CSV export button to the page toolbar or action area

## Files to Create
- `src/pages/RemediationDashboardPage/components/ExportButton.tsx` — CSV export button component that calls `fetchRemediationExport()` and triggers browser file download
- `src/pages/RemediationDashboardPage/components/ExportButton.test.tsx` — unit tests for the export button

## Implementation Notes
- The export button should call `fetchRemediationExport()` from `src/api/rest.ts` (created in Task 5), which returns a Blob response.
- Trigger a browser file download by creating an object URL from the Blob and programmatically clicking an anchor element: `URL.createObjectURL(blob)` -> `<a download="remediation-report.csv" href={url}>`.
- Use a PatternFly 5 `Button` component with a download icon for the export trigger.
- Show a loading state on the button while the export is in progress (disable the button and show a spinner).
- Handle errors gracefully: show a PatternFly toast notification if the export fails.
- Per frontend conventions: do NOT use `window.location.reload()`. Use React Query mutation pattern with `onSuccess` for success handling if wrapping in a mutation, though a simple async function is acceptable here since this is a download, not a cache-modifying operation.

**Backend API contracts:**
- `GET /api/v2/remediation/export` — response: CSV file with Content-Type `text/csv` and Content-Disposition attachment header (see `modules/fundamental/src/remediation/endpoints/export.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchRemediationExport()` — API client function for CSV export (created in Task 5)
- `src/components/LoadingSpinner.tsx` — loading indicator pattern for button loading state

## Acceptance Criteria
- [ ] Export button is visible on the remediation dashboard page
- [ ] Clicking the export button triggers a CSV file download
- [ ] Downloaded file has the correct CSV content matching remediation data
- [ ] Button shows loading state while export is in progress
- [ ] Error state shows toast notification if export fails

## Test Requirements
- [ ] Unit test: `ExportButton` renders and is clickable
- [ ] Unit test: clicking the button calls `fetchRemediationExport()`
- [ ] Unit test: successful export triggers file download via object URL
- [ ] Unit test: failed export shows error notification

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 4 — Add CSV export endpoint for remediation report (backend endpoint)
- Depends on: Task 5 — Add API client functions, types, and React Query hooks for remediation endpoints
- Depends on: Task 6 — Add remediation dashboard page with summary cards and progress chart (button is placed on this page)
