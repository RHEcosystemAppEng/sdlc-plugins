# Task 7 — Add multi-select and "Compare selected" to SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Let users start a comparison from the SBOM list page (TC-9003, UC-1 steps 1–3). The user ticks checkboxes on two SBOM rows and clicks a "Compare selected" button, which goes to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row-selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — tests for selection and navigation
- `tests/e2e/sbom-list.spec.ts` — E2E flow: select two SBOMs, click Compare, and land on the comparison view

## Implementation Notes
- Use PF5 composable `Table` row selection (`Td select={{ rowIndex, onSelect, isSelected }}`) in the existing SBOM list table.
- Keep the selected IDs in local component state. They are UI state, not server state, so React Query is not needed.
- Add the "Compare selected" `Button` (variant secondary) to the existing toolbar, next to the `FilterToolbar` controls.
  - Enable it only when **exactly two** SBOMs are selected.
  - With more than two selected, keep it disabled and show a tooltip: "Select exactly two SBOMs to compare".
- Order: the first-selected SBOM is `left` and the second is `right`. Alternatively, order by ingestion date (older = left) if `SbomSummary` exposes it. Pick one rule and document it in a code comment.
- Navigate with React Router `useNavigate()` to `/sbom/compare?left=${encodeURIComponent(id1)}&right=${encodeURIComponent(id2)}`. Do not use `window.location`.
- Selection must survive filter changes only for rows that are still visible, or be cleared when filters change. Choose clearing (simpler) unless the existing table already keeps selection across filters.
- Per CONVENTIONS.md §Component library: use PF5 table selection and `Button`/`Tooltip`. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React UI component scope. Example: the existing table and `FilterToolbar` usage in `src/pages/SbomListPage/SbomListPage.tsx`.
- Per CONVENTIONS.md §Testing: Vitest + RTL for unit tests, and Playwright for E2E. Applies: task modifies `tests/e2e/sbom-list.spec.ts` matching the convention's Playwright E2E scope. Example: the existing scenarios in `tests/e2e/sbom-list.spec.ts`.
- Constraints (docs/constraints.md):
  - §2: commit format, Jira footer, `Assisted-by` trailer
  - §3: `gh pr create --base TC-9003`, and post the PR link to Jira
  - §5: change only the listed files

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and toolbar to extend
- `src/components/FilterToolbar.tsx` — toolbar where the action button goes
- `tests/mocks/fixtures/sboms.json` — has multiple SBOMs for selection tests

## Acceptance Criteria
- [ ] Each SBOM row in the list has a selection checkbox
- [ ] "Compare selected" is disabled with 0, 1, or more than 2 rows selected, and enabled with exactly 2
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the selected IDs URL-encoded
- [ ] Existing list behavior (filtering, sorting, deletion) is unchanged

## Test Requirements
- [ ] Unit test: button enable/disable states for 0, 1, 2, and 3 selections
- [ ] Unit test: clicking the button navigates to the expected URL
- [ ] E2E test: select two SBOMs, click "Compare selected", and the comparison view renders its section headers

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — tests pass
- `npx playwright test tests/e2e/sbom-list.spec.ts` — E2E passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Add SBOM comparison page at /sbom/compare
