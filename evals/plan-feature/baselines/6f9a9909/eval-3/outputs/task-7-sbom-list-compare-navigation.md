## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add multi-select capability to the SBOM list page so users can select two SBOMs and navigate to the comparison view. This implements the UC-1 workflow where a user selects two SBOMs from the list and clicks "Compare selected" to navigate to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and "Compare selected" toolbar action

## Files to Create
- `src/pages/SbomListPage/SbomListPage.test.tsx` — update or extend existing tests to cover multi-select and compare navigation

## Implementation Notes
**Figma design reference (from SBOMCompare mock123, implied by UC-1 workflow):**

The SBOM list page needs the following additions:
1. **Row checkboxes**: Add PatternFly `Table` row selection (checkbox column) to enable multi-select. Limit selection to exactly 2 SBOMs -- when 2 are selected, disable additional checkboxes.
2. **"Compare selected" toolbar button**: Add a PatternFly `Button` (secondary variant) to the existing toolbar area. The button is disabled when fewer than 2 SBOMs are selected. When clicked, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.
3. **Selection state**: Use React state to track selected SBOM IDs. Clear selection when the user navigates away or when filters change.

Follow the existing `SbomListPage.tsx` component structure. The page already uses a PatternFly table with the `FilterToolbar` component from `src/components/FilterToolbar.tsx`. Add the selection column and toolbar action alongside the existing filter controls.

Per CONVENTIONS.md (Key Conventions) -- Component library: PatternFly 5 -- all UI components use PF5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md (Key Conventions) -- Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` page component scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing list page; extend rather than replace
- `src/components/FilterToolbar.tsx` — existing filter toolbar; the compare button should be placed alongside this component
- `src/hooks/useSboms.ts` — existing SBOM list hook; already used by the list page

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select up to 2 SBOMs; additional checkboxes disabled after 2 selected
- [ ] "Compare selected" button appears in the toolbar area
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is cleared when filters change
- [ ] Existing list page functionality (filtering, sorting, pagination) is not broken

## Test Requirements
- [ ] Unit test: checkbox column renders for each SBOM row
- [ ] Unit test: selecting 2 SBOMs enables the "Compare selected" button
- [ ] Unit test: selecting fewer than 2 SBOMs keeps the button disabled
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with query params
- [ ] Unit test: selecting a third SBOM is prevented when 2 are already selected
- [ ] E2E test: full workflow from SBOM list selection to comparison page navigation

## Verification Commands
- `npx tsc --noEmit` — no TypeScript compilation errors
- `npx vitest run --reporter=verbose -- SbomListPage` — list page tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page (comparison page must exist for navigation target)
