# Task 5 — Add SBOM comparison page with selectors, URL state, and empty/loading states

**Summary:** Add /sbom/compare page with header toolbar, URL-shareable state, empty and loading states
**Epic:** TC-9003: SBOM comparison UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the `/sbom/compare` page from the Figma design: a header toolbar with left and right SBOM selectors and a "Compare" button, the comparison state encoded in the URL so it can be bookmarked and shared (UC-2), an empty state shown before any comparison, a loading state while the diff loads, and an error state. The six diff sections render inside this page; Task 6 builds them. This task leaves a placeholder region for them.

## Files to Modify
- `src/routes.tsx` — register the lazy-loaded `/sbom/compare` route

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — page component: reads and writes `left`/`right` URL params, calls `useSbomComparison`, renders the toolbar plus the empty, loading, error, or result region
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for page states and URL behavior
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with two typeahead `Select` SBOM selectors, the "Compare" button, and an "Export" dropdown slot (Task 8 enables it)

## Implementation Notes
**Figma layout (SBOMCompare / Comparison View):**
- **Left/right SBOM selector:** PatternFly `Select` (single, typeahead). Each option label is `"<name> v<version>"` (e.g., "my-product-sbom v2.3.1"). Populate the options from the existing `useSboms` hook (`src/hooks/useSboms.ts`, backed by `GET /api/v2/sbom`). Pre-fill from the `left` and `right` URL query params.
- **"Compare" button:** primary variant. Disabled until both selectors have a value. Clicking it writes `?left={id1}&right={id2}` to the URL, and the URL change triggers the fetch.
- **"Export" dropdown:** secondary `Dropdown`, disabled until a comparison has loaded. Task 8 adds the menu items and behavior; this task renders it disabled.
- **Empty state** (no `left`/`right` params): PatternFly `EmptyState` with `CodeBranchIcon` (the fallback, since `ComparisonIcon` is not in PF5), title "Select two SBOMs to compare", and body "Choose an SBOM for each side and click Compare to see what changed." Use the existing `src/components/EmptyStateCard.tsx` if it accepts an icon, title, and body. Otherwise compose PF `EmptyState` directly.
- **Loading state:** while `useSbomComparison` is loading, show a PF `Skeleton` placeholder for each of the six diff sections and disable the whole toolbar (both selectors, Compare, and Export).
- **Error state:** on a 404 or 400 from the compare call, show an error alert or empty state such as "One or both SBOMs could not be found". Do not render empty diff sections. This is fail-closed: an error must not look like "no changes".

**URL-shareable state (UC-2):** use React Router v6 `useSearchParams` as the single source of truth for `left` and `right`. Opening `/sbom/compare?left=A&right=B` directly must pre-fill both selectors and run the comparison automatically, with no extra click. Selector changes alone must not trigger a fetch; only "Compare" commits the params.

**Same-product guard (Customer Considerations):** the Feature says both SBOMs should come from the same product. The backend contract does not enforce this. If `SbomSummary` exposes a product or name field, show a non-blocking PF `Alert` (warning) when the two selected SBOMs differ in it. Do not block the comparison.

**Display text vs API value:** selector labels are composed from the SBOM list fields (`name` + `version`). Check the actual `SbomSummary` field names in `src/api/models.ts`. No enum mapping is needed in this task.

**Conventions:**
- Per CONVENTIONS.md §Page structure: create `src/pages/SbomComparePage/` with the main component, a test file, and a `components/` subdirectory for page-specific components. Mirror `src/pages/SbomDetailPage/`.
  Applies: task modifies `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's page directory (`src/pages/<Page>/`) scope.
- Per CONVENTIONS.md §Routing: register the route in `src/routes.tsx` with a lazy-loaded page component, like the existing pages.
  Applies: task modifies `src/routes.tsx` matching the convention's React Router route definition scope.
- Per CONVENTIONS.md §Component library: use PF5 `Select`, `Button`, `Dropdown`, `EmptyState`, `Skeleton`, and `Toolbar`. Do not use custom HTML controls.
  Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Naming: PascalCase component files (`SbomComparePage.tsx`, `CompareToolbar.tsx`).
  Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's component naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW for API mocking (handler added in Task 4).
  Applies: task modifies `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's unit test (`*.test.tsx`) scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits, `Implements TC-XXXX` footer, `Assisted-by:` trailer.
- §3: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5: Change only the listed files; reuse `useSboms`, `EmptyStateCard`, and `LoadingSpinner` patterns.

## Reuse Candidates
- `src/hooks/useSboms.ts` — SBOM list for the selectors (Figma explicitly calls for it).
- `src/hooks/useSbomComparison.ts` — added in Task 4.
- `src/components/EmptyStateCard.tsx` — existing empty-state placeholder.
- `src/components/LoadingSpinner.tsx` — existing loading indicator. Prefer PF `Skeleton` per Figma, but follow its conventions.
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page layout, URL param usage, and loading/error handling.

## Acceptance Criteria
- [ ] Navigating to `/sbom/compare` with no params shows the empty state with the Figma icon, title, and body
- [ ] Both selectors list SBOMs as "name vVersion" using `useSboms` and support typeahead filtering
- [ ] "Compare" is disabled until both selectors have values
- [ ] Clicking "Compare" updates the URL to `?left={id1}&right={id2}` and triggers the comparison request
- [ ] Opening `/sbom/compare?left=A&right=B` directly pre-fills both selectors and loads the comparison without user interaction (URL-shareable)
- [ ] While loading, each diff section shows a `Skeleton` and the toolbar is disabled
- [ ] When the compare request fails (404/400), an error state appears instead of empty diff sections (fail-closed)
- [ ] The "Export" dropdown renders and stays disabled until a comparison result has loaded

## Test Requirements
- [ ] Test: renders the empty state when there are no URL params
- [ ] Test: the Compare button is disabled with zero or one selection and enabled with two
- [ ] Test: rendering with `?left=…&right=…` pre-fills the selectors and calls the compare endpoint (MSW)
- [ ] Test: Skeleton placeholders render and the toolbar controls are disabled while the request is pending
- [ ] Test: when MSW returns 404 for compare, an error message renders and no diff sections render (fail-closed path)
- [ ] Test: the Export dropdown is disabled before results arrive and enabled after

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/pages/SbomComparePage` — all page tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
