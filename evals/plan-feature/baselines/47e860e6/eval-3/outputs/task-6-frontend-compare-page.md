# Task 6 — Frontend: SBOM comparison page and /sbom/compare route

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the SBOM comparison page at `/sbom/compare` (TC-9003). The header toolbar has left and right SBOM selectors and a Compare button, and an Export dropdown placeholder is wired in Task 8. The page encodes both SBOM IDs in the URL (`?left=..&right=..`) so comparisons are shareable (UC-2), shows an empty state before a comparison and a loading state during one, and renders the diff sections from Task 5.

## Files to Modify
- `src/routes.tsx`: register a lazy-loaded `/sbom/compare` route pointing to `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx`: page component that reads and writes URL params, calls `useSbomComparison`, and renders the toolbar, empty state, loading state, error state and diff sections
- `src/pages/SbomComparePage/components/CompareToolbar.tsx`: header toolbar with two PF5 typeahead `Select` SBOM selectors, the "Compare" primary button and the "Export" dropdown (disabled until a result is loaded; Task 8 adds its actions)
- `src/pages/SbomComparePage/SbomComparePage.test.tsx`: page tests

## Implementation Notes
- **Header toolbar** (Figma):
  - Left and right SBOM selectors: PF5 `Select` (single, typeahead). Each option shows the SBOM name and version, e.g., "my-product-sbom v2.3.1". Options come from the existing `useSboms` hook (`GET /api/v2/sbom`). Each selector is pre-populated from the URL query param (`left` or `right`).
  - "Compare" button: primary, disabled until both selectors have values. Clicking it writes `?left=<id>&right=<id>` to the URL with `useSearchParams` (React Router v6), and that URL change triggers the query.
  - "Export" dropdown: secondary, items "Export JSON" and "Export CSV", disabled until a comparison result is loaded. This task renders it disabled, and Task 8 implements the actions.
  - The whole toolbar is disabled while the comparison is loading.
- **URL as source of truth:** derive `left`/`right` from `useSearchParams()` and pass them to `useSbomComparison(left, right)`. When the page loads with both params, the comparison runs immediately without another click, which satisfies UC-2. This resolves the Figma note "Compare triggers the call" for a shared URL.
- **Empty state** (no params): PF5 `EmptyState` with icon `CodeBranchIcon` (fallback for `ComparisonIcon`), title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state:** pass `isLoading` to each `DiffSection` (Task 5) so it renders `Skeleton`.
- **Error state** (fail-closed): when the query errors (e.g., `404` unknown SBOM ID from a stale shared URL), show an error alert or empty state naming the failure. Never render six empty sections as if the SBOMs were identical.
- **Backend API contracts:**
  - `GET /api/v2/sbom` returns `{ items: SbomSummary[], total: number }` (`modules/fundamental/src/sbom/endpoints/list.rs`). It is consumed via the existing `useSboms`.
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `SbomComparison`. Errors are `400` and `404` (`modules/fundamental/src/sbom/endpoints/compare.rs`, Task 3). It is consumed via `useSbomComparison` (Task 4).
  - Verify these contracts against the `trustify-backend` repo during implementation using the implement-task cross-repo API verification step.
- **Display text vs API value:** selector labels combine `SbomSummary` name and version fields into "name vVERSION". Confirm the field names in `src/api/models.ts`.
- Per CONVENTIONS.md §Routing: add a lazy-loaded route in `src/routes.tsx` (React Router v6 `lazy`), following the existing `SbomDetailPage` route entry.
  Applies: task modifies `src/routes.tsx` matching the convention's route definition (`src/routes.tsx`) scope.
- Per CONVENTIONS.md §Page structure: the page lives in `src/pages/SbomComparePage/` with the main component, a test file and a `components/` subdirectory. See `src/pages/SbomDetailPage/`.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page (`src/pages/<Page>/*.tsx`) scope.
- Per CONVENTIONS.md §Component library: use PF5 `Select` (typeahead), `Button`, `Dropdown`, `EmptyState`, `Toolbar`, and `CodeBranchIcon` from `@patternfly/react-icons`.
  Applies: task creates `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Shared components: reuse `src/components/EmptyStateCard.tsx` for the empty state if its API supports a custom icon, title and body; otherwise compose PF5 `EmptyState` directly.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's component (`.tsx`) scope.
- Per CONVENTIONS.md §Testing: use Vitest, React Testing Library and MSW handlers from `tests/mocks/handlers.ts`, following `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's unit test (`.test.tsx`) scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to the listed files; §5.2 inspect `routes.tsx`, `useSboms.ts` and `SbomDetailPage.tsx` before changing; §5.4 reuse `useSboms` and do not add a new SBOM list fetch; §5.6 trace URL params to the hook, the API, and the rendered sections; §5.11–5.13 test comments; §2.1–2.3 commit format; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `src/hooks/useSboms.ts::useSboms`: SBOM list for both selectors (required by the Figma component mapping)
- `src/hooks/useSbomComparison.ts::useSbomComparison` (Task 4): comparison data
- `src/components/EmptyStateCard.tsx`: existing empty state placeholder
- `src/components/FilterToolbar.tsx`: existing PF5 toolbar composition pattern for the header toolbar layout
- `src/pages/SbomDetailPage/SbomDetailPage.tsx`: page layout and URL-param handling pattern

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and lazy-loaded
- [ ] Without query params, the page shows the empty state with the Figma title and body text
- [ ] The Compare button is disabled until both selectors have values; clicking it updates the URL to `?left=<id>&right=<id>`
- [ ] Opening `/sbom/compare?left=<id1>&right=<id2>` directly pre-populates both selectors and loads the comparison without extra clicks (UC-2)
- [ ] While loading, the toolbar is disabled and each section shows a skeleton
- [ ] On a backend error (e.g., `404`), the page shows an error state, not empty diff sections (fail-closed)
- [ ] The Export dropdown is rendered and stays disabled until a comparison result is loaded

## Test Requirements
- [ ] Test: render without params and assert the empty state title "Select two SBOMs to compare"
- [ ] Test: render with `?left=a&right=b` and assert selectors show the matching SBOMs and the diff sections render fixture data
- [ ] Test: Compare is disabled with one selector empty and enabled with both set; clicking it updates the URL search params
- [ ] Test: during loading, skeletons render and the toolbar controls are disabled
- [ ] Test (fail-closed): when the MSW compare handler returns `404`, an error message renders and no diff section shows "0"

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Frontend: comparison API types, client function, React Query hook and mocks
- Depends on: Task 5 — Frontend: comparison diff section components
