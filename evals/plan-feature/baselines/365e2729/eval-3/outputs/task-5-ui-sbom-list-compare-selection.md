## Repository
trustify-ui

## Target Branch
main

## Description
Add the comparison entry point to the SBOM list page (TC-9003, UC-1 steps 1–3): users select exactly two SBOMs using row checkboxes and click "Compare selected", which navigates to `/sbom/compare?left={id1}&right={id2}`. The first selected SBOM becomes `left`, the second `right`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — tests for selection and navigation
- `tests/e2e/sbom-list.spec.ts` — E2E flow: select two SBOMs → Compare selected → comparison page loads

## Implementation Notes
- **Figma / PatternFly:** use PF5 composable `Table` row selection (`<Td select={{ rowIndex, onSelect, isSelected }} />`) on the existing table in `SbomListPage.tsx`; add a PF `Button variant="secondary"` labelled "Compare selected" in the existing toolbar (the page's toolbar is built on `src/components/FilterToolbar.tsx` — add the button as a `ToolbarItem` alongside the filters rather than forking the toolbar).
- Button is enabled only when exactly two rows are selected; with more than two selected, keep it disabled and show a PF `Tooltip` "Select exactly two SBOMs to compare".
- Navigate with React Router `useNavigate()` to `/sbom/compare?left=${first.id}&right=${second.id}` (build with `URLSearchParams`), preserving selection order.
- Selection state is local component state (`useState<string[]>`); it is not server state, so no React Query involvement.
- Customer consideration: both SBOMs should be from the same product. If the SBOM list rows expose a product/name field, show a PF inline `Alert variant="warning"` (non-blocking) when the two selected SBOMs have different product names.
- **Per CONVENTIONS.md §Component library:** use PF5 table selection and `Button`/`Tooltip`, consistent with the existing PF5 table in `src/pages/SbomListPage/SbomListPage.tsx`.
  Applies: task modifies src/pages/SbomListPage/SbomListPage.tsx matching the convention's React `.tsx` UI component scope.
- **Per CONVENTIONS.md §Routing:** use React Router v6 `useNavigate` for the transition to the lazy-loaded `/sbom/compare` route defined in `src/routes.tsx` (Task 4).
  Applies: task modifies src/pages/SbomListPage/SbomListPage.tsx matching the convention's React Router navigation scope.
- **Per CONVENTIONS.md §Testing:** unit tests with Vitest + RTL + MSW (`tests/mocks/fixtures/sboms.json`) and Playwright for the E2E flow, extending `tests/e2e/sbom-list.spec.ts`.
  Applies: task modifies tests/e2e/sbom-list.spec.ts matching the convention's Playwright E2E `.ts` scope.
- **Constraints (docs/constraints.md):** §2 commits (Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer); §3 PRs (`--base main`, PR link on Jira task); §5 code changes (scoped files, inspect `SbomListPage.tsx` first, reuse `FilterToolbar`, no duplicated table); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — existing PF toolbar; add the Compare button as an extra item
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM table; extend in place with selection
- `tests/mocks/fixtures/sboms.json` — mock SBOM rows for selection tests

## Acceptance Criteria
- [ ] Each SBOM row has a selection checkbox
- [ ] "Compare selected" is disabled with 0, 1 or >2 selections and enabled with exactly 2
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={firstSelectedId}&right={secondSelectedId}`
- [ ] Existing filtering, sorting and deletion on the SBOM list page continue to work
- [ ] A non-blocking warning is shown when the two selected SBOMs belong to different products (if product info is available in the list data)

## Test Requirements
- [ ] Unit test: button disabled/enabled states for 0, 1, 2, 3 selections
- [ ] Unit test: clicking the button navigates to the correct URL with selection order preserved
- [ ] E2E test: select two SBOMs on the list page, click "Compare selected", assert the comparison page renders with both selectors pre-populated

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — list page tests pass
- `npx playwright test tests/e2e/sbom-list.spec.ts` — E2E flow passes

## Dependencies
- Depends on: Task 4 — Build SBOM comparison page at /sbom/compare (navigation target)
