## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Register the /remediation route in the application router and add a navigation entry so users can access the remediation dashboard from the main application navigation. This makes the dashboard discoverable and accessible.

## Files to Modify
- `src/routes.tsx` -- add /remediation route definition pointing to RemediationDashboardPage with lazy loading
- `src/App.tsx` -- add navigation entry for the remediation dashboard in the router setup

## Implementation Notes
- Add the route in `src/routes.tsx` following the existing pattern for route definitions (path to page component mapping). Use React Router v6 lazy-loaded page components consistent with the existing routes.
- Add a navigation entry in `src/App.tsx` following the existing navigation structure. The remediation dashboard should be accessible alongside existing pages (SBOMs, Advisories, Search).
- Use lazy loading (`React.lazy`) for the RemediationDashboardPage import to maintain the code-splitting pattern used by other pages.

## Reuse Candidates
- `src/routes.tsx` -- existing route definitions to follow as a pattern
- `src/App.tsx` -- existing navigation structure and router setup

## Acceptance Criteria
- [ ] /remediation route is registered and navigates to RemediationDashboardPage
- [ ] Navigation entry for remediation dashboard is visible in the application nav
- [ ] Route uses lazy loading consistent with other page routes
- [ ] Navigating to /remediation renders the dashboard page correctly

## Test Requirements
- [ ] Test that /remediation route renders the RemediationDashboardPage component
- [ ] Test that navigation entry is present in the rendered navigation
- [ ] E2E test navigating to /remediation and verifying page loads

## Dependencies
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
