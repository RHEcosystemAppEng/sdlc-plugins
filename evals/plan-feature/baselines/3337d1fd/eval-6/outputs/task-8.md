## Repository
trustify-ui

## Target Branch
main

## Description
Integrate the remediation dashboard into the application routing and navigation. Add the /remediation route to the router configuration and add a navigation entry so users can access the dashboard from the application menu.

## Files to Modify
- `src/routes.tsx` — add route definition for /remediation pointing to RemediationDashboardPage (lazy-loaded)
- `src/App.tsx` — add navigation menu entry for the remediation dashboard

## Implementation Notes
Follow the routing pattern in `src/routes.tsx` where existing routes map paths to page components. Use React Router v6 lazy loading as used for other pages. Add the VulnerabilityTable component from Task 7 into the RemediationDashboardPage layout below the summary cards and progress chart. Add a navigation link in `src/App.tsx` following the existing menu structure pattern.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions for pattern reference
- `src/App.tsx` — existing navigation menu entries

## Acceptance Criteria
- [ ] /remediation route renders the RemediationDashboardPage
- [ ] Navigation menu includes a "Remediation" entry
- [ ] Page is lazy-loaded consistent with other routes
- [ ] Dashboard page includes summary cards, progress chart, and vulnerability table

## Test Requirements
- [ ] Unit test verifying /remediation route renders the dashboard page
- [ ] Test that navigation link is present and navigates correctly

## Dependencies
- Depends on: Task 6 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 — Create filterable vulnerability table component
