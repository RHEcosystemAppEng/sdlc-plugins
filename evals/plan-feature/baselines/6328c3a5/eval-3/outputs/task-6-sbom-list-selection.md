## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add multi-select capability to the SBOM list page so users can select two SBOMs and navigate to the comparison view. This involves adding row selection checkboxes to the SBOM table and a "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}` when exactly two SBOMs are selected.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes to the SBOM table and a "Compare selected" button to the page toolbar

## Implementation Notes
Per CONVENTIONS.md §Component Library: use PatternFly 5 components for table selection and toolbar actions.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

**Selection behavior:**
- Add `select` variant to the existing PatternFly `Table` component to enable row checkboxes
- Track selected SBOM IDs in component state using `useState<string[]>`
- Limit visual selection to maximum 2 SBOMs; disable further checkboxes when 2 are selected (or allow any number but only enable Compare when exactly 2 are selected)

**Compare button:**
- Add a "Compare selected" button in the page toolbar area
- Button is disabled until exactly 2 SBOMs are selected
- On click: use React Router `useNavigate` to navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}`

**User workflow (UC-1):**
1. User views SBOM list page
2. User selects two SBOMs via checkboxes
3. User clicks "Compare selected"
4. Browser navigates to comparison page with both SBOM IDs in URL

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — existing reusable filter toolbar; the "Compare selected" button should be placed in the toolbar area alongside existing filter controls
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component; modify it in-place

## Acceptance Criteria
- [ ] SBOM list page table rows have selection checkboxes
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] "Compare selected" button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state resets when user navigates away and returns

## Test Requirements
- [ ] Unit test: table renders with selection checkboxes
- [ ] Unit test: "Compare selected" button is disabled with 0 selections
- [ ] Unit test: "Compare selected" button is disabled with 1 selection
- [ ] Unit test: "Compare selected" button is enabled with 2 selections
- [ ] Unit test: "Compare selected" button is disabled with 3+ selections
- [ ] Unit test: clicking "Compare selected" navigates to correct URL with both SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Create SBOM comparison page with diff sections (the target route must exist)
