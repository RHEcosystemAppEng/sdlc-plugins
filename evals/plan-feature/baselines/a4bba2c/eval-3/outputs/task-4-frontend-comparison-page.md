# Task 4 — Add SBOM comparison page with diff sections

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the SBOM comparison page at `/sbom/compare` with a header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections as specified in the Figma design. The page reads `left` and `right` query parameters from the URL, fetches the comparison data from the backend, and renders the structured diff with appropriate visual indicators for each category of change.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison API response types
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string)` API client function
- `src/routes.tsx` — add route definition for `/sbom/compare` pointing to the new SbomComparePage component

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call with `left` and `right` parameters
- `src/pages/SbomComparePage/SbomComparePage.tsx` — main comparison page component with header toolbar and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — reusable collapsible diff section component (ExpandableSection + Badge + Table)
- `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` — header toolbar with SBOM selectors, Compare button, and Export dropdown

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — CONSUME: frontend calls this new backend endpoint

## Implementation Notes
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
    ```json
    {
      "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": "number" }],
      "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": "number" }],
      "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
      "new_vulnerabilities": [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
      "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
      "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
    }
    ```
  - See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend (created in Task 2)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step

- **Page structure (from Figma):**
  1. **ComparisonToolbar** — contains left/right SBOM Select dropdowns (PatternFly `Select`, single, typeahead), "Compare" primary button, and "Export" secondary Dropdown button
  2. **DiffSection** components for each of the 6 categories, rendered in order: Added Packages (green badge), Removed Packages (red badge), Version Changes (blue badge), New Vulnerabilities (red badge), Resolved Vulnerabilities (green badge), License Changes (yellow badge)

- **SBOM selectors**: use PatternFly `Select` with typeahead, populated via the existing `useSboms` hook. Pre-populate from URL query params `left` and `right` on initial load using `useSearchParams()` from React Router
- **Compare button**: disabled until both selectors have values. On click, update URL query params and trigger the comparison API call
- **Export dropdown**: PatternFly `Dropdown` with two items: "Export JSON" and "Export CSV". Disabled until comparison result is loaded. Export is a non-MVP feature but include the UI shell with a placeholder implementation
- **Empty state**: when no query params are present, show PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Loading state**: while API call is in progress, show PatternFly `Skeleton` placeholders in each diff section. Disable the toolbar during loading
- **DiffSection component**: each section is a PatternFly `ExpandableSection` with a title, `Badge` (count + color), and a composable `Table` inside. Default expanded when item count > 0. Sortable columns
- **Virtualized lists**: per NFR, use virtualized rendering for sections with >100 items to prevent browser freezing. Consider `react-window` or PatternFly's built-in virtualization support
- **New Vulnerabilities highlighting**: rows with severity "Critical" in the New Vulnerabilities section should have a highlighted/warning background using PatternFly's `Tr` `isHoverable` or custom CSS with `--pf-v5-global--danger-color--100`
- **URL-shareable**: the page reads `left` and `right` from URL search params and auto-triggers comparison on load if both are present
- **React Query hook**: `useSbomComparison` should accept `leftId` and `rightId`, use `useQuery` with `enabled: !!leftId && !!rightId` to conditionally fetch, and use a query key like `['sbom-comparison', leftId, rightId]`
- **Route registration**: add the route in `src/routes.tsx` following the same lazy-loading pattern as other pages
- Per docs/constraints.md §2: every commit must reference TC-9003 in the footer, use Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`
- Per docs/constraints.md §5: keep changes scoped to the listed files, inspect code before modifying

## Reuse Candidates
- `src/hooks/useSboms.ts` — existing React Query hook for SBOM list; reuse to populate the SBOM selectors in the toolbar
- `src/hooks/useSbomById.ts` — reference for React Query hook patterns (query key structure, enabled flag)
- `src/components/SeverityBadge.tsx` — existing shared component for rendering severity levels; use in the New Vulnerabilities and Resolved Vulnerabilities diff sections
- `src/components/EmptyStateCard.tsx` — existing empty state component; adapt for the comparison page's initial empty state
- `src/components/LoadingSpinner.tsx` — existing loading indicator; consider using alongside Skeleton placeholders
- `src/components/FilterToolbar.tsx` — reference for toolbar layout patterns with PatternFly
- `src/api/rest.ts` — existing API client functions (e.g., `fetchSboms`) as pattern for the new `fetchSbomComparison` function
- `src/api/models.ts` — existing TypeScript interfaces as pattern for comparison response types
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; reuse for vulnerability severity display and for determining critical row highlighting
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — existing package table component; reference for table column definitions and rendering patterns
- `src/pages/SbomDetailPage/components/AdvisoryList.tsx` — existing advisory list component; reference for advisory display patterns

## Acceptance Criteria
- [ ] The page is accessible at `/sbom/compare`
- [ ] SBOM selectors allow selecting SBOMs via typeahead search
- [ ] URL query params `left` and `right` pre-populate the selectors on page load
- [ ] Clicking "Compare" fetches the diff and renders all six sections
- [ ] Added Packages section shows packages with name, version, license, and advisory count columns with green count badge
- [ ] Removed Packages section shows packages with name, version, license, and advisory count columns with red count badge
- [ ] Version Changes section shows package name, left version, right version, and direction columns with blue count badge
- [ ] New Vulnerabilities section shows advisory ID, severity badge, title, and affected package columns with red count badge
- [ ] Resolved Vulnerabilities section shows advisory ID, severity, title, and previously affected package columns with green count badge
- [ ] License Changes section shows package name, left license, and right license columns with yellow count badge
- [ ] Sections with 0 items are collapsed by default; sections with >0 items are expanded
- [ ] Rows with Critical severity in New Vulnerabilities have highlighted background
- [ ] Empty state displays when no comparison has been performed
- [ ] Loading skeleton placeholders appear during API call
- [ ] The comparison URL is shareable — opening a URL with left and right params auto-triggers comparison
- [ ] Export dropdown is present (JSON and CSV options) and disabled until results are loaded

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: page renders SBOM selectors pre-populated from URL query params
- [ ] Unit test: Compare button is disabled when only one SBOM is selected
- [ ] Unit test: successful comparison renders all six diff sections with correct data
- [ ] Unit test: diff sections with 0 items are collapsed
- [ ] Unit test: critical severity rows in New Vulnerabilities have highlighted styling
- [ ] Unit test: loading state shows skeleton placeholders
- [ ] MSW mock handler for `GET /api/v2/sbom/compare` returns fixture data
- [ ] Tests follow the Vitest + React Testing Library patterns in `tests/setup.ts`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff endpoint (backend API must exist for integration testing)
