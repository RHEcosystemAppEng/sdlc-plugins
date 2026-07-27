# Task 8: Register remediation route and navigation

**Epic:** TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Register the `/remediation` route in React Router to render the RemediationDashboardPage and add a navigation entry so users can access the dashboard from the application navigation. This completes the frontend routing setup for the remediation tracking feature.

## Files to Modify
- `src/routes.tsx` — add route definition mapping `/remediation` to the RemediationDashboardPage component with lazy loading
- `src/App.tsx` — add navigation link for the remediation dashboard in the application navigation structure

## Implementation Notes
- Add the route definition in `src/routes.tsx` following the existing pattern for other pages (SbomListPage, AdvisoryListPage, SearchPage). Use React Router v6 lazy-loaded page components per the project convention.
- Add a navigation entry in `src/App.tsx` following the existing navigation structure. The label should be "Remediation" and the path should be `/remediation`.
- Use React.lazy() for the RemediationDashboardPage import to maintain the lazy-loading convention used by other pages.
- Use PascalCase for the component import and camelCase for any utility functions per project naming conventions.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions; follow the same pattern for adding the remediation route
- `src/App.tsx` — existing navigation structure; follow the same pattern for adding the navigation entry

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the RemediationDashboardPage
- [ ] A navigation link labeled "Remediation" is visible in the application navigation
- [ ] The RemediationDashboardPage is lazy-loaded following the existing route pattern
- [ ] No existing routes or navigation entries are affected

## Test Requirements
- [ ] Unit test verifying the /remediation route resolves to RemediationDashboardPage
- [ ] E2E test verifying a user can navigate to the remediation dashboard from the navigation menu

## Verification Commands
- `npx vitest run src/routes` — run route tests
- `npx tsc --noEmit` — verify TypeScript compilation

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 6 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Add filterable vulnerability table to remediation dashboard
