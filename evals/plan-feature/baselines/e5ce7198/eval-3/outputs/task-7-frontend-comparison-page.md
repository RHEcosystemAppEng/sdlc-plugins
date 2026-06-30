## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Build the SBOM comparison page at `/sbom/compare` following the Figma design mockups. The page features a header toolbar with two PatternFly `Select` dropdowns for choosing SBOMs, a "Compare" button, and vertically stacked `ExpandableSection` components for each diff category (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes). Each section contains a sortable `Table` with a count `Badge`. An `EmptyState` is shown when no comparison has been performed.

### Figma Context
- **SBOM selectors**: PatternFly `Select` (single, typeahead) pre-populated from URL query params `left` and `right`, fetching SBOM list via existing `useSboms` hook
- **Diff sections**: Six `ExpandableSection` components, each with a colored `Badge` count and a composable `Table` inside. Sections default to expanded when item count > 0
- **Count badge colors**: green (Added Packages, Resolved Vulnerabilities), red (Removed Packages, New Vulnerabilities), blue (Version Changes), yellow (License Changes)
- **New Vulnerabilities table**: Rows with severity "Critical" have a highlighted background; uses existing `SeverityBadge` component
- **Empty state**: PatternFly `EmptyState` with `CodeBranchIcon`, title "Select two SBOMs to compare", body text explaining the workflow
- **Loading state**: `Skeleton` placeholders in each diff section while API call is in progress
- **Export dropdown**: PatternFly `Dropdown` with "Export JSON" and "Export CSV" options (disabled until comparison loaded)

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with toolbar, diff sections, empty state, and loading state
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable `ExpandableSection` wrapper with `Badge` count and `Table` content
- `src/pages/SbomComparePage/components/SbomSelector.tsx` — SBOM `Select` dropdown component using `useSboms` hook

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to `SbomComparePage`
- `src/App.tsx` — Add lazy import for `SbomComparePage` if required by routing pattern

## Implementation Notes
Follow the page structure pattern in `src/pages/SbomDetailPage/SbomDetailPage.tsx` — main page component with a `components/` subdirectory for page-specific components.

**SbomComparePage.tsx**:
- Read `left` and `right` from URL search params using React Router's `useSearchParams`
- Use `useSbomComparison(leftId, rightId)` hook from Task 6 to fetch comparison data
- Render `SbomSelector` components for left and right SBOM selection
- On "Compare" click, update URL search params to trigger the comparison query
- Render six `DiffSection` components, one per diff category, passing the appropriate data array and column definitions
- Show `EmptyState` (PatternFly) with `CodeBranchIcon` when no comparison is active
- Show `Skeleton` placeholders when comparison is loading

**DiffSection.tsx**:
- Accept props: `title`, `items`, `columns`, `badgeColor`, `isLoading`
- Render PatternFly `ExpandableSection` with `isExpanded` defaulting to `items.length > 0`
- Render `Badge` with item count and specified color
- Render PatternFly composable `Table` with sortable columns
- For the New Vulnerabilities section, apply highlighted row styling when severity is "Critical"

**SbomSelector.tsx**:
- Use PatternFly `Select` with typeahead and single-select mode
- Fetch SBOM list using existing `useSboms` hook from `src/hooks/useSboms.ts`
- Display SBOM name and version in each option
- Accept `value` and `onChange` props for controlled selection

**Route registration**:
- In `src/routes.tsx`, add `{ path: '/sbom/compare', element: <SbomComparePage /> }` before the `/sbom/:id` route to prevent path conflicts

Per CONVENTIONS.md §Component library: PatternFly 5 — all UI components use PF5 equivalents.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory.
Applies: task creates `src/pages/SbomComparePage/` matching the convention's `src/pages/` directory scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's routing file scope.

Per CONVENTIONS.md §Naming: PascalCase for components.
Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's component naming scope.

## Reuse Candidates
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — reference for page structure with tabs and sub-components
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for PatternFly composable Table usage
- `src/components/SeverityBadge.tsx` — reuse directly for severity indicators in vulnerability diff tables
- `src/components/EmptyStateCard.tsx` — reference for empty state pattern (may use directly or adapt)
- `src/components/LoadingSpinner.tsx` — reference for loading state pattern
- `src/hooks/useSboms.ts` — reuse for SBOM list fetching in selector dropdowns
- `src/components/FilterToolbar.tsx` — reference for PatternFly toolbar layout pattern

## Acceptance Criteria
- [ ] Page renders at `/sbom/compare` route
- [ ] Two SBOM `Select` dropdowns load SBOM list and support typeahead filtering
- [ ] URL query params `left` and `right` are read on page load and pre-populate selectors
- [ ] "Compare" button triggers API call and updates URL search params
- [ ] Six `ExpandableSection` components render with correct titles, badge counts, and badge colors
- [ ] Each section contains a sortable `Table` with the specified columns
- [ ] `EmptyState` with `CodeBranchIcon` displays when no comparison is active
- [ ] `Skeleton` placeholders display while comparison API call is loading
- [ ] Critical severity rows in New Vulnerabilities section have highlighted background
- [ ] Existing `SeverityBadge` component is used for severity display

## Test Requirements
- [ ] Verify page renders empty state when no query params are present
- [ ] Verify SBOM selectors load and display SBOM options
- [ ] Verify comparison results render in the correct sections after API call

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- SbomComparePage` — component tests pass

## Dependencies
- Depends on: Task 1 — create-branch
- Depends on: Task 6 — frontend-api-layer

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:99eb5c9e0a138fe77953b7ee1a550177e6d299bf4538ca9e895db6ac3c029046
