## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection support to the SBOM list page so users can select two SBOMs and click a "Compare selected" button to navigate to the comparison page. This implements the UC-1 workflow where users discover and select SBOMs from the list page, then are navigated to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row checkbox selection (PatternFly Table selection), a "Compare selected" toolbar action button, and navigation logic to `/sbom/compare?left={id}&right={id}`

## Implementation Notes
- Use PatternFly `Table` built-in row selection (checkbox variant) — the existing `SbomListPage.tsx` already uses a PatternFly table, so add the `select` prop configuration.
- Add a "Compare selected" `Button` to the toolbar area (next to existing filters). The button should be:
  - Disabled when fewer than 2 SBOMs are selected
  - Disabled when more than 2 SBOMs are selected (show tooltip: "Select exactly 2 SBOMs to compare")
  - Enabled when exactly 2 SBOMs are selected
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate()`.
- Maintain selection state using React `useState` with an array of selected SBOM IDs.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's TypeScript/React component scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component being modified; review its current Table configuration to understand how to add selection
- `src/components/FilterToolbar.tsx` — reference for toolbar action placement patterns

## Acceptance Criteria
- [ ] SBOM list page shows checkboxes for each row
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than 2 SBOMs are selected
- [ ] Clicking "Compare selected" with 2 SBOMs navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection state is managed correctly across page interactions

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with query params
- [ ] Update existing `SbomListPage.test.tsx` to account for the new selection UI

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Frontend comparison page (navigation target must exist)

<!-- [sdlc-workflow] Description digest: sha256-md:b999ea67e9aa25deeda8a84739e2c7039bd8c666d4ce39492e6ff34f3af0a224 -->
