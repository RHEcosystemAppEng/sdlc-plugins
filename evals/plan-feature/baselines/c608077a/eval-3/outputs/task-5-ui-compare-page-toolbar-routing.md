# Task 5 — Add SBOM comparison page shell with selectors, URL state, and route

**Summary:** Add /sbom/compare page with SBOM selectors, Compare button, URL-shareable state, empty and loading states
**Epic:** TC-9003: Comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the `/sbom/compare` page described in TC-9003 and the Figma "Comparison View" frame. This task covers the page shell:

- a header toolbar with left and right SBOM selectors and a "Compare" button
- comparison state encoded in the URL (`?left={id1}&right={id2}`), so the URL can be bookmarked and shared (UC-2)
- the empty state shown before any comparison
- the loading state while the diff is fetched
- an error state

Task 6 builds the six diff sections, which this page renders inside its results area. Task 8 adds the Export dropdown.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded route `/sbom/compare` → `SbomComparePage`. It must be matched before any `/sbom/:id` route.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — page component: reads and writes `left`/`right` URL search params, renders the toolbar, empty, loading, error, and results areas
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — page tests (Vitest + React Testing Library + MSW)
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with two typeahead `Select`s and the "Compare" button

## Implementation Notes
- **Figma → PatternFly mapping (figma-context.md, "Component Mapping").**
  - SBOM selector → PF5 `Select` (single, typeahead), populated from the existing `useSboms` hook (`src/hooks/useSboms.ts`). Option label format: `"<sbom name> v<version>"`, e.g., "my-product-sbom v2.3.1".
  - "Compare" button → PF5 `Button variant="primary"`. Disabled until both selectors have a value. While a comparison is loading, the whole toolbar is disabled.
  - Empty state → PF5 `EmptyState`:
    - Icon: `CodeBranchIcon` from `@patternfly/react-icons` (fallback for the Figma "ComparisonIcon", which has no PF equivalent)
    - Title: "Select two SBOMs to compare"
    - Body: "Choose an SBOM for each side and click Compare to see what changed."
    - Check whether `src/components/EmptyStateCard.tsx` can be reused with this icon and text before building a new one.
  - Loading state → render the six section placeholders as PF5 `Skeleton`, one per diff section (Figma "Loading State"). Do not use `src/components/LoadingSpinner.tsx` here; the design specifies skeletons.
- **URL as the source of truth (UC-2).**
  - Use React Router v6 `useSearchParams`.
  - On mount, pre-populate both selectors from `left` and `right`. If both are present, run the comparison immediately with no click required, so a shared URL loads the comparison directly.
  - Clicking "Compare" writes `?left=…&right=…` with `setSearchParams`. The fetch is driven by `useSbomComparison(left, right)` from Task 4, reading from the URL params rather than local selector state.
  - With no params, show the empty state.
- **Error state.** If `useSbomComparison` returns an error (e.g., a 404 for an unknown or stale SBOM ID in a shared URL), show a PF5 inline `Alert variant="danger"` that names the failing ID. Never render the diff sections with empty data on error.
- **Selector data volume.** `useSboms` returns paginated results. Use the typeahead filter to query by name rather than loading all SBOMs. Check whether `useSboms` already accepts a filter or search param.
- **Same-product guard.** The feature notes that both SBOMs "must be from the same product", but no product field has been confirmed on `SbomSummary`. Do not block the comparison. This is tracked as an open question on TC-9003 (see the impact map, "Excluded requirements").
- **Data component rendering scope.** This page only hosts the sections. Each section's table is scoped per section (see Task 6).
- **Directory naming conflict.** CONVENTIONS.md "Naming" specifies kebab-case for directories, but all existing page directories use PascalCase (`src/pages/SbomListPage/`, `src/pages/SbomDetailPage/`). Follow the existing sibling pattern (`src/pages/SbomComparePage/`) for consistency, and mention the discrepancy in the PR description.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, a test file, and a `components/` subdirectory for page-specific components. See `src/pages/SbomDetailPage/` (with `components/PackageTable.tsx`) for the established pattern.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `src/pages/` page-structure scope.
- Per CONVENTIONS.md §Routing: register the page as a lazy-loaded component in `src/routes.tsx` (React Router v6). See the existing `SbomDetailPage` route entry.
  Applies: task modifies `src/routes.tsx` matching the convention's route-definition scope.
- Per CONVENTIONS.md §Component library: use PatternFly 5 equivalents for all UI elements (`Select`, `Button`, `EmptyState`, `Skeleton`, `Alert`).
  Applies: task creates `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW handlers from `tests/mocks/handlers.ts`. See `src/pages/SbomDetailPage/SbomDetailPage.test.tsx`.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's unit-test scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: use `--base TC-9003` and post the PR link on the Jira task.
  - §5 Code change rules: stay within the listed files; inspect before modifying; reuse existing components and hooks.
  - §1.4/§1.5: no unrelated refactoring.

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing SBOM list hook for populating both selectors (Figma explicitly specifies reusing it)
- `src/hooks/useSbomComparison.ts` — added in Task 4; drives the comparison fetch
- `src/components/EmptyStateCard.tsx` — existing empty-state placeholder; reuse it if it accepts a custom icon, title, and body
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page layout, the loading and error pattern, and reading route or search params
- `src/components/FilterToolbar.tsx` — existing PatternFly toolbar composition; follow its `Toolbar`/`ToolbarItem` layout for `CompareToolbar`

## Acceptance Criteria
- [ ] Navigating to `/sbom/compare` with no params shows the empty state with the title "Select two SBOMs to compare" and the specified body text
- [ ] Both selectors list SBOMs as "name vVersion" using `useSboms`, with typeahead filtering
- [ ] "Compare" is disabled until both selectors have values
- [ ] Clicking "Compare" updates the URL to `/sbom/compare?left={id1}&right={id2}` and triggers the comparison request
- [ ] Opening `/sbom/compare?left={id1}&right={id2}` directly pre-populates both selectors and loads the comparison without user interaction (UC-2)
- [ ] While loading, each diff section area shows a `Skeleton` and the toolbar is disabled
- [ ] A failed comparison (e.g., 404) shows an error alert, not an empty diff
- [ ] `/sbom/compare` does not get captured by an `/sbom/:id` route

## Test Requirements
- [ ] Test: render with no search params → the empty state text is visible and no compare request is sent
- [ ] Test: select both SBOMs and click Compare → the URL contains `left` and `right`, and the MSW compare handler is called
- [ ] Test: render with `?left=a&right=b` → selectors show the matching SBOMs and the results area renders without a click
- [ ] Test: Compare button is disabled with only one selection
- [ ] Test: MSW returns 404 → the error alert is shown and no diff sections render
- [ ] Test: during a pending request, skeletons are rendered and the toolbar controls are disabled

## Verification Commands
- `npx vitest run src/pages/SbomComparePage` — all tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SbomComparison types, fetchSbomComparison() and useSbomComparison hook with MSW mocks
