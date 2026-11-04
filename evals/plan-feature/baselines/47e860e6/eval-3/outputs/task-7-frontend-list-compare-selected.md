# Task 7 — Frontend: multi-select and "Compare selected" on SBOM list page

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Enable UC-1 of TC-9003. On the SBOM list page, users select two SBOMs with row checkboxes and click "Compare selected", which navigates to `/sbom/compare?left={id1}&right={id2}` (Task 6).

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx`: add row selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx`: add tests for selection and navigation
- `tests/e2e/sbom-list.spec.ts`: add an E2E scenario: select two SBOMs, click Compare selected, and land on the comparison page

## Implementation Notes
- Use PF5 composable `Table` row selection (`Td select={{ rowIndex, onSelect, isSelected }}`) and track selected IDs in component state.
- "Compare selected" is enabled only when **exactly two** SBOMs are selected. With fewer or more, it is disabled with a tooltip ("Select exactly two SBOMs to compare").
- On click, `navigate(\`/sbom/compare?left=${leftId}&right=${rightId}\`)` (React Router `useNavigate`). Left/right assignment: put the older SBOM (earlier ingestion or creation date from `SbomSummary`) on the left and the newer on the right, so "Added" and "New Vulnerabilities" read as changes introduced by the newer version. Confirm the date field name in `src/api/models.ts`. If no date field exists, use selection order.
- Place the button in the existing list toolbar next to the filters.
- Per CONVENTIONS.md §Component library: use PF5 table selection and `Button`/`Tooltip`.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Routing: navigate with React Router v6 `useNavigate`, never `window.location`.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React Router page (`.tsx`) scope.
- Per CONVENTIONS.md §Testing: unit tests use Vitest and React Testing Library with MSW, and E2E uses Playwright in `tests/e2e/`. Follow the existing `src/pages/SbomListPage/SbomListPage.test.tsx` and `tests/e2e/sbom-list.spec.ts`.
  Applies: task modifies `tests/e2e/sbom-list.spec.ts` matching the convention's Playwright E2E (`tests/e2e/*.spec.ts`) scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to the listed files; §5.2 inspect `SbomListPage.tsx` and `FilterToolbar.tsx` before changing; §5.8 keep the existing filter, sort and delete behavior intact; §5.11–5.13 test comments; §2.1–2.3 commit format; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `src/components/FilterToolbar.tsx`: existing list toolbar where the Compare selected action fits
- `src/hooks/useSboms.ts`: already supplies list rows, including IDs and dates

## Acceptance Criteria
- [ ] SBOM list rows have selection checkboxes
- [ ] "Compare selected" is disabled unless exactly two SBOMs are selected
- [ ] Clicking it navigates to `/sbom/compare?left=<older-id>&right=<newer-id>`
- [ ] Existing list behavior (filters, sorting, delete) is unchanged

## Test Requirements
- [ ] Unit test: selecting 0, 1 or 3 rows keeps the button disabled, and selecting 2 enables it
- [ ] Unit test: clicking the button navigates to the compare URL with both IDs in the correct left/right order
- [ ] E2E test: select two SBOMs, click Compare selected, and assert the URL contains `left` and `right` and the comparison sections render

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 6 — Frontend: SBOM comparison page and /sbom/compare route
