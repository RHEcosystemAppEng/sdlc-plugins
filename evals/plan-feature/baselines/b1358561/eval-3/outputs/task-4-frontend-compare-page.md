# Task 4 — Add SBOM comparison page with selectors, URL state and route

**Summary:** TC-9003: Add /sbom/compare page with SBOM selectors and URL-shareable state
**Issue type:** Task
**Parent (Epic):** Epic 2 — TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Description
Create the SBOM comparison page at `/sbom/compare` (TC-9003) per the Figma "Comparison View"
design: a header toolbar with left/right SBOM selectors and a "Compare" button, an empty state
when no comparison has been run, a loading state, and an error state. The selected SBOM IDs are
encoded in the URL (`/sbom/compare?left={id1}&right={id2}`) so a comparison can be bookmarked
and shared (UC-2): opening such a URL loads the comparison directly without re-selecting SBOMs.

This task renders the page shell and wires data loading; the six diff sections are rendered by
the `ComparisonResults` component delivered in Task 5 (this task renders a placeholder container
that Task 5 fills). The Export dropdown is Task 7.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded route `/sbom/compare` → `SbomComparePage` (register before any `/sbom/:id` route so `compare` is not treated as an ID)

## Files to Create
- `src/pages/sbom-compare-page/SbomComparePage.tsx` — page component: toolbar, URL state, empty/loading/error states
- `src/pages/sbom-compare-page/components/SbomSelector.tsx` — single typeahead PatternFly `Select` showing "name version", fed by `useSboms`
- `src/pages/sbom-compare-page/SbomComparePage.test.tsx` — page tests

## Implementation Notes
- **Figma header toolbar:**
  - Left / right SBOM selector: PatternFly `Select` (single, typeahead) showing SBOM name + version (e.g. "my-product-sbom v2.3.1"); options loaded via the existing `src/hooks/useSboms.ts` hook (backed by `GET /api/v2/sbom`). Pre-populated from URL query params `left` / `right`.
  - "Compare" button: PatternFly primary `Button`, disabled until both selectors have values. Clicking it writes `left`/`right` into the URL with React Router `useSearchParams`; the comparison query is driven by the URL params (single source of truth), so a shared URL and a button click follow the same code path.
  - Toolbar (selectors + button) is disabled while the comparison request is loading.
- **Empty state** (no `left`/`right` in URL): PatternFly `EmptyState` with icon `CodeBranchIcon` (Figma `ComparisonIcon` is not in PatternFly — use the documented fallback), title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed." Reuse/extend `src/components/EmptyStateCard.tsx` if it accepts icon/title/body props.
- **Loading state:** while `useSbomComparison` (Task 3) is loading, render PatternFly `Skeleton` placeholders for each of the six diff sections (pass `isLoading` to `ComparisonResults` from Task 5, or render six skeleton blocks here). `src/components/LoadingSpinner.tsx` is not the Figma-specified pattern for this page.
- **Error state:** on 404 (unknown SBOM) or 400, show a PatternFly danger `Alert`/`EmptyState` naming the problem — do not render an empty comparison, which would falsely read as "no changes".
- **Backend API contracts:**
  - `GET /api/v2/sbom` — `{ items: SbomSummary[], total: number }` (trustify-backend `modules/fundamental/src/sbom/endpoints/list.rs`) — consumed via existing `useSboms`.
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — `SbomComparison` (trustify-backend `modules/fundamental/src/sbom/endpoints/compare.rs`, Task 2) — consumed via `useSbomComparison` (Task 3).
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- If `useSboms` is paginated, ensure the typeahead searches server-side (or loads enough items) so SBOMs beyond the first page are selectable; and when the URL contains an ID not in the loaded page, resolve its label via `useSbomById`.
- Same-product guidance (Customer Considerations): not enforced in MVP; if both selected SBOMs have different product names, show an inline PatternFly `Alert` variant="warning" ("These SBOMs appear to belong to different products") but still allow comparison.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file and a `components/` subdirectory; see `src/pages/SbomDetailPage/` (`SbomDetailPage.tsx`, `components/PackageTable.tsx`).
  Applies: task creates `src/pages/sbom-compare-page/SbomComparePage.tsx` matching the convention's `src/pages/<page>/` `.tsx` scope.
- Per CONVENTIONS.md §Naming: PascalCase for components, kebab-case for directories (`sbom-compare-page/`, `SbomComparePage.tsx`, `SbomSelector.tsx`). Note: existing page directories (`SbomListPage/`) are PascalCase, contradicting the documented kebab-case rule — follow the documented convention unless the reviewer prefers consistency with siblings; flag in the PR description.
  Applies: task creates `src/pages/sbom-compare-page/components/SbomSelector.tsx` matching the convention's component/directory naming `.tsx` scope.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components; follow existing entries in `src/routes.tsx`.
  Applies: task modifies `src/routes.tsx` matching the convention's route-definition `.tsx` scope.
- Per CONVENTIONS.md §Component library: all UI uses PatternFly 5 components (`Select`, `Button`, `EmptyState`, `Skeleton`, `Alert`).
  Applies: task creates `src/pages/sbom-compare-page/SbomComparePage.tsx` matching the convention's React `.tsx` component scope.
- Constraints (docs/constraints.md): §5.1 scope; §5.4 reuse `useSboms`, `EmptyStateCard`; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `src/hooks/useSboms.ts` — SBOM list for selector options
- `src/hooks/useSbomById.ts` — resolve a selector label for an ID provided via URL
- `src/components/EmptyStateCard.tsx` — existing empty state placeholder
- `src/components/FilterToolbar.tsx` — existing PatternFly toolbar layout pattern
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page structure and data-loading pattern
- `src/routes.tsx` — lazy-route registration pattern

## Acceptance Criteria
- [ ] Navigating to `/sbom/compare` with no params shows the empty state with title "Select two SBOMs to compare" and the specified body text
- [ ] Both selectors list SBOMs as "name version" from `GET /api/v2/sbom` and support typeahead
- [ ] "Compare" is disabled until both selectors have values
- [ ] Clicking "Compare" updates the URL to `/sbom/compare?left={id1}&right={id2}` and triggers the comparison request
- [ ] Opening `/sbom/compare?left={id1}&right={id2}` directly pre-populates both selectors and loads the comparison without user interaction (URL-shareable)
- [ ] While loading, skeletons are shown for the diff sections and the toolbar is disabled
- [ ] A 404/400 response shows an error state, not an empty comparison
- [ ] `/sbom/compare` does not resolve to the SBOM detail route

## Test Requirements
- [ ] Render test: no URL params → empty state text and `CodeBranchIcon` rendered, Compare disabled
- [ ] Interaction test: select both SBOMs, click Compare → URL search params updated and MSW compare handler called
- [ ] Deep-link test: render at `/sbom/compare?left=a&right=b` → selectors pre-populated and results requested
- [ ] Loading test: skeletons visible and toolbar disabled while request pending
- [ ] Error test: MSW returns 404 → error message rendered, no diff sections

## Verification Commands
- `npm run test -- SbomComparePage` — page tests pass
- `npm run build` — type-check and build succeed

## Dependencies
- Depends on: Task 3 — Add SBOM comparison API client and useSbomComparison hook
