# Task 3 — Add SBOM multi-select and "Compare selected" to SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Modify the existing SBOM list page to support selecting exactly two SBOMs via checkboxes and navigating to the comparison page. This enables the primary user flow where a security analyst selects two SBOM versions from the list and clicks "Compare selected" to initiate a comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column to the SBOM table, add "Compare selected" button to the page toolbar, implement navigation to `/sbom/compare?left={id1}&right={id2}` when two SBOMs are selected
- `src/pages/SbomListPage/SbomListPage.test.tsx` — add tests for the selection and compare navigation behavior

## Implementation Notes
- **Selection UX**: add a checkbox column as the first column in the SBOM table using PatternFly's `Table` select variant. Track selected SBOM IDs in local component state using `useState<string[]>([])`
- **Compare button**: add a PatternFly `Button` with variant="primary" labeled "Compare selected" to the page toolbar (near existing filter controls). The button should be disabled unless exactly 2 SBOMs are selected. On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate()`
- **PatternFly table selection**: use PatternFly 5's composable Table with `isSelected` and `onSelect` props on each `Tr` to implement row selection
- **URL-shareable comparison**: the comparison URL encodes both SBOM IDs as query parameters, enabling direct sharing per UC-2
- **Existing component reuse**: the `FilterToolbar` component in `src/components/FilterToolbar.tsx` is already used on this page — place the Compare button alongside it rather than creating a separate toolbar
- Per docs/constraints.md §2: every commit must reference TC-9003 in the footer, use Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`
- Per docs/constraints.md §5: keep changes scoped to the listed files, inspect code before modifying

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM list page with table rendering; extend rather than rewrite
- `src/components/FilterToolbar.tsx` — reusable toolbar component already used on the SBOM list page; place Compare button alongside it
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list; no changes needed, already provides the data

## Acceptance Criteria
- [ ] Each SBOM row in the list table has a checkbox for selection
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" with 2 SBOMs selected navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is cleared when navigating away and returning to the list page

## Test Requirements
- [ ] Unit test: rendering the SBOM list page shows checkboxes in each row
- [ ] Unit test: selecting exactly 2 SBOMs enables the "Compare selected" button
- [ ] Unit test: selecting fewer than 2 or more than 2 SBOMs disables the "Compare selected" button
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with left and right params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
