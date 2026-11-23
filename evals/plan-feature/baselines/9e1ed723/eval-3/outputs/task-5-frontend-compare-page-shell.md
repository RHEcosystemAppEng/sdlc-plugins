# Task 5 — Add SBOM comparison page with selectors, URL state, empty and loading states

**Summary:** Add /sbom/compare page shell with SBOM selectors and URL-shareable state
**Epic:** TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create the comparison page at `/sbom/compare` (TC-9003) with the header toolbar from the Figma design (left/right SBOM selectors and Compare button), URL-encoded state so comparisons are bookmarkable and shareable (UC-2), the empty state, the loading state, and the error state. The diff sections themselves are implemented in Task 6 and the Export dropdown in Task 8; this task renders a placeholder container that Task 6 fills.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded route `/sbom/compare` → `SbomComparePage`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — page component: reads `left`/`right` from the URL, renders toolbar, empty/loading/error states, and the diff container
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — page tests
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — header toolbar with the two selectors and the Compare button (leaves a slot for the Export dropdown added in Task 8)
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — PatternFly single typeahead `Select` listing SBOMs as "<name> v<version>"

## Implementation Notes
**Figma UI structure (header toolbar):**
- Left and right SBOM selectors: PatternFly `Select` (single, typeahead), options populated with the existing `useSboms` hook (`src/hooks/useSboms.ts`, backed by `GET /api/v2/sbom`). Option label format: SBOM name + version (e.g., "my-product-sbom v2.3.1"); fields come from `SbomSummary` in `src/api/models.ts`.
- Pre-populate the left selector from query param `left` and the right selector from `right`.
- "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. Clicking it writes `?left=<id1>&right=<id2>` to the URL via React Router `useSearchParams` (`setSearchParams`), which in turn drives `useSbomComparison` (Task 4). The URL is the single source of truth — do not keep a separate copy of the IDs in component state once Compare is clicked.
- Opening a URL with both params already set must load the comparison immediately without clicking Compare (UC-2).
- During loading, the whole toolbar is disabled (selectors + buttons).

**Empty state** (page load without query params): PatternFly `EmptyState` with icon `CodeBranchIcon` (Figma names `ComparisonIcon`, which is not in PatternFly — use the specified fallback), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Reuse/extend `src/components/EmptyStateCard.tsx` if its props allow a custom icon/title/body; otherwise compose PF `EmptyState` directly.

**Loading state:** while `useSbomComparison` is fetching, render a PatternFly `Skeleton` placeholder for each of the six diff sections (in Figma order: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes).

**Error state (fail-closed):** when the comparison request fails (e.g., `404` for an unknown/deleted SBOM in a shared URL), show an error alert/empty state naming the problem. Never render the diff sections with zero counts on error — that would tell a compliance user "nothing changed". The guard belongs in `SbomComparePage.tsx` where the hook's `isError` is checked before rendering the diff container.

**Same-SBOM selection:** if `left === right`, keep Compare enabled but the result is an all-empty diff; optionally show an info hint. Same-product validation is an open question in the impact map — do not block in this task.

**Directory naming:** CONVENTIONS.md says kebab-case directories, but all existing page directories are PascalCase (`src/pages/SbomListPage/`, `src/pages/SbomDetailPage/`). Follow the existing on-disk pattern (`src/pages/SbomComparePage/`) for consistency and mention the discrepancy in the PR description.

**Conventions:**
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route-definition scope. Example: existing lazy routes for `SbomListPage` / `SbomDetailPage` in `src/routes.tsx`.
- Per CONVENTIONS.md §Page structure: each page has its own directory under `src/pages/` with a main component, a test file, and a `components/` subdirectory. Applies: task modifies `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `src/pages/` scope. Example: `src/pages/SbomDetailPage/` with `components/`.
- Per CONVENTIONS.md §Component library: use PatternFly 5 components (`Select`, `Button`, `EmptyState`, `Skeleton`, `Toolbar`). Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Naming: PascalCase for components. Applies: task modifies `src/pages/SbomComparePage/components/SbomSelector.tsx` matching the convention's component naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW. Applies: task modifies `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's unit test scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx` and render helpers in `tests/setup.ts`.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: scope to listed files; reuse `useSboms`, `EmptyStateCard`, `LoadingSpinner` where they fit; doc comments on every test function; given-when-then comments for non-trivial tests.

## Reuse Candidates
- `src/hooks/useSboms.ts` — SBOM list for the selectors (Figma explicitly calls for this hook)
- `src/hooks/useSbomComparison.ts` — comparison query hook (Task 4)
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder
- `src/components/FilterToolbar.tsx` — existing PatternFly toolbar composition to mirror for layout
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout pattern (page section, title, toolbar)
- `tests/setup.ts` — render helpers with router + QueryClient providers

## Acceptance Criteria
- [ ] Navigating to `/sbom/compare` renders the comparison page (lazy-loaded route)
- [ ] Without query params, the empty state shows `CodeBranchIcon`, "Select two SBOMs to compare", and the specified body text
- [ ] Both selectors list SBOMs from `GET /api/v2/sbom` as "<name> v<version>" with typeahead filtering
- [ ] Compare is disabled until both selectors have values
- [ ] Clicking Compare updates the URL to `?left=<id1>&right=<id2>` and triggers the comparison request
- [ ] Loading `/sbom/compare?left=<id1>&right=<id2>` directly pre-populates both selectors and loads the comparison without user action
- [ ] While loading, six `Skeleton` section placeholders render and the toolbar is disabled
- [ ] Fail-closed: when the comparison request fails, an error state is shown and no zero-count diff sections are rendered

## Test Requirements
- [ ] Test: empty state renders when no query params are present
- [ ] Test: Compare button disabled with zero or one selection, enabled with two
- [ ] Test: clicking Compare sets `left`/`right` search params
- [ ] Test: rendering with `?left=a&right=b` pre-selects both SBOMs and calls the compare endpoint (MSW)
- [ ] Test: skeletons render and toolbar controls are disabled while the request is pending
- [ ] Fail-closed test: MSW returns `404` → error state is shown and diff section headings with "0" badges are not rendered

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/pages/SbomComparePage` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
