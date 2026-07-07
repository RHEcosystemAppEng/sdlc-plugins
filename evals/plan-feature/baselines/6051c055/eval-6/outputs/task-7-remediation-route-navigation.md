## Repository
trustify-ui

## Target Branch
main

## Description
Register the `/remediation` route in the application router and add a navigation entry so users can access the remediation dashboard from the main navigation. This connects the RemediationDashboardPage component (TC-9006) to the application's routing and navigation system.

## Files to Modify
- `src/routes.tsx` — add `/remediation` route definition with lazy-loaded RemediationDashboardPage component
- `src/App.tsx` — add navigation entry for the remediation dashboard in the main navigation menu

## Implementation Notes
- Add a lazy-loaded route for `/remediation` in `src/routes.tsx`, following the pattern of existing route definitions. Use `React.lazy()` for code-splitting, consistent with how other pages are loaded.
- Add a navigation link in `src/App.tsx` to the main navigation menu. Place it alongside existing navigation items (SBOMs, Advisories, Search).
- The navigation label should be "Remediation" or "Remediation Dashboard" — consistent with PatternFly's navigation component patterns.

Per CONVENTIONS.md Section "Routing": React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing file scope.

Per CONVENTIONS.md Section "Component library": all UI components use PatternFly 5 equivalents.
Applies: task modifies `src/App.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions to follow for pattern consistency (lazy loading, path format)
- `src/App.tsx` — existing navigation structure to follow for adding a new entry

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the RemediationDashboardPage
- [ ] A navigation entry for the remediation dashboard appears in the main navigation menu
- [ ] The route uses lazy loading for the page component (code-splitting)
- [ ] The navigation link highlights correctly when on the `/remediation` page

## Test Requirements
- [ ] Verify navigating to `/remediation` renders the RemediationDashboardPage component
- [ ] Verify the navigation entry is present in the rendered navigation menu
- [ ] Verify lazy loading works correctly (component loads on navigation)

## Dependencies
- Depends on: Task 5 — Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 6 — Add filterable vulnerability table to remediation dashboard
