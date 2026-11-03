# Task 6 — Add SBOM comparison page at /sbom/compare

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` for TC-9003. It has a header toolbar (left/right SBOM selectors, a Compare button, and an Export placeholder slot), the six diff sections from Task 5, and the empty, loading, and error states. Both SBOM IDs live in the URL (`?left=&right=`), so a comparison URL can be shared and opened directly without re-selecting SBOMs (UC-2, MVP).

## Files to Modify
- `src/routes.tsx` — register a lazy-loaded `/sbom/compare` route that renders `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — page component: toolbar, URL state, data fetching through `useSbomComparison`, and the empty/loading/error/result states
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — two typeahead SBOM `Select`s and a Compare button
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — page tests

## Implementation Notes
- **Header toolbar (Figma):**
  - The left and right selectors are PF5 `Select` (single, typeahead). Each option shows "<SBOM name> v<version>" (e.g., "my-product-sbom v2.3.1").
  - Options come from the existing `useSboms` hook (`src/hooks/useSboms.ts`, `GET /api/v2/sbom`).
  - The selectors are pre-filled from the `left` / `right` URL params.
  - The **Compare** button is primary and disabled until both selectors have values. Clicking it writes `?left={id1}&right={id2}` to the URL with React Router `useSearchParams`, which triggers the query.
  - Leave a slot to the right of Compare for the Export dropdown (added in Task 8).
  - Disable the whole toolbar while the comparison is loading.
- **URL as source of truth (UC-2)**:
  - Read `left`/`right` with `useSearchParams` and pass them to `useSbomComparison(left, right)` from Task 4.
  - Loading the page with both params fetches immediately, without a Compare click.
  - Do not store the selection only in component state.
- **States:**
  - **Empty** (no params): PF `EmptyState` with icon `CodeBranchIcon` (the Figma `ComparisonIcon` is not available in PF, so use the fallback). Title "Select two SBOMs to compare". Body "Choose an SBOM for each side and click Compare to see what changed." Reuse `src/components/EmptyStateCard.tsx` if its props support icon, title, and body.
  - **Loading**: each `DiffSection` gets `isLoading` and shows a `Skeleton`. The toolbar is disabled.
  - **Error (fail-closed)**: if the hook returns 404/400, show a PF `Alert` (danger) such as "One or both SBOMs could not be found". **Do not** render six empty sections, because that would falsely suggest "no changes".
  - **Result**: render the six sections from Task 5 in order, each passed its own array from the response (per-context scope; see Task 5).
- **Display text vs API value**: selector options display `name` + `version` from `SbomSummary` (`GET /api/v2/sbom`), and the URL stores the SBOM `id`. Map `id` back to its label for pre-filled selectors. If a URL `id` is not in the loaded list, still run the comparison, show the raw id in the selector, and rely on the 404 error state if it is invalid.
- **Backend API contracts:**
  - `GET /api/v2/sbom`: response `{ items: SbomSummary[], total: number }` (see `modules/fundamental/src/sbom/endpoints/list.rs`, `modules/fundamental/src/sbom/model/summary.rs`)
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}`: response `SbomComparison` (see Task 4 for the full shape; `modules/fundamental/src/sbom/endpoints/compare.rs`). 400 if a param is missing, 404 if an SBOM is unknown.
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- **Routing**: follow the existing lazy-loaded route entries in `src/routes.tsx`, e.g. the `SbomDetailPage` route. Make sure `/sbom/compare` is declared so that it is not captured by an `/sbom/:id` detail route. Static segments rank higher in React Router v6, but test it.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. Example: the existing `SbomDetailPage` lazy route in `src/routes.tsx`.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with the main component, a test file, and a `components/` folder. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §State management: server state lives only in React Query, with no Redux and no copies of fetched data in local state. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's server-state consumer scope. Example: `src/pages/SbomDetailPage/SbomDetailPage.tsx` using `useSbomById`.
- Per CONVENTIONS.md §Testing: Vitest + RTL with MSW. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's unit test scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md):
  - §2: commit format, Jira footer, `Assisted-by` trailer
  - §3: `gh pr create --base TC-9003`, and post the PR link to Jira
  - §5: scoped changes, reuse the existing hooks/components, trace the data flow (URL -> hook -> sections)

## Reuse Candidates
- `src/hooks/useSboms.ts` — SBOM list for the selectors (Figma explicitly calls for it)
- `src/hooks/useSbomComparison.ts` (Task 4) — comparison data
- `src/pages/SbomComparePage/components/DiffSection.tsx` and the table components (Task 5)
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/components/FilterToolbar.tsx` — PF toolbar layout pattern for the header
- `src/routes.tsx` — existing lazy route pattern

## Acceptance Criteria
- [ ] Navigating to `/sbom/compare` with no params shows the empty state with the Figma title and body text
- [ ] The Compare button is disabled until both selectors have a value
- [ ] Clicking Compare updates the URL to `?left={id1}&right={id2}` and loads the comparison
- [ ] Opening `/sbom/compare?left={id1}&right={id2}` directly pre-fills both selectors and renders the comparison without further interaction (UC-2)
- [ ] During loading, each section shows a `Skeleton` and the toolbar is disabled
- [ ] A 404/400 from the compare endpoint shows an error alert, never empty diff sections
- [ ] The six diff sections render with their respective data once loaded
- [ ] The `/sbom/compare` route is lazy-loaded and does not conflict with SBOM detail routes

## Test Requirements
- [ ] Test: renders the empty state when there are no query params
- [ ] Test: Compare is disabled with one selection and enabled with two
- [ ] Test: rendering with `?left=a&right=b` calls the compare endpoint (MSW) and shows section titles with the fixture counts
- [ ] Test: shows skeletons while the request is pending
- [ ] Test: a 404 from MSW renders the error alert and no diff sections (fail-closed)
- [ ] Test: clicking Compare updates the URL search params

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — page tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add comparison API client, types, and React Query hook
- Depends on: Task 5 — Add comparison diff section components
