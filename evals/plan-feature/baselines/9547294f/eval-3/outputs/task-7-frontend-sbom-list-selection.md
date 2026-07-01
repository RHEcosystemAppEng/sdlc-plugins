# Task 7 — Add SBOM selection and comparison trigger on list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection for SBOMs on the SBOM list page and a "Compare selected" action button that navigates to the comparison page with the two selected SBOM IDs as query parameters. This provides the primary entry point for users to initiate a comparison from the existing SBOM list workflow (UC-1 in the feature requirements).

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the SBOM table, add "Compare selected" button to the toolbar that navigates to `/sbom/compare?left={id1}&right={id2}`, disable the button until exactly two SBOMs are selected

## Implementation Notes

### Selection behavior

Add a checkbox column to the existing SBOM list table. Track selected SBOM IDs in component state using `useState<string[]>([])`. The "Compare selected" button should:
- Appear in the page toolbar (alongside any existing actions)
- Be disabled until exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left=${selected[0]}&right=${selected[1]}` using React Router's `useNavigate`

### PatternFly table selection

Use PatternFly's composable Table with `select` capabilities. Follow the existing table implementation in `SbomListPage.tsx` and add the `onSelect` row property.

### Reuse candidates

- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page being modified, with its table and toolbar structure
- `src/components/FilterToolbar.tsx` — existing toolbar component for reference on toolbar action placement

Per CONVENTIONS.md: use PatternFly 5 components; mutation-like navigation uses `useNavigate` from React Router v6.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript component file scope.

## Acceptance Criteria
- [ ] SBOM list table has a checkbox selection column
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state clears when navigating away and returning

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0 selections
- [ ] Unit test: "Compare selected" button is disabled with 1 selection
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: "Compare selected" button is disabled with 3+ selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page with diff sections (comparison page must exist for navigation target)

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:a9d3f7b1c6e2805d4a0b3e5c7f9d1a4b6e8c0f2d5a7b9e1c3f6a8d0b2e4c7f9a
