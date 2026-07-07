# Task 6 -- SBOM comparison page component

## Repository
trustify-ui

## Target Branch
main

## Description
Implement the SBOM comparison page at /sbom/compare per the Figma design. The page includes a header toolbar with two SBOM selector dropdowns (PatternFly Select with typeahead), a Compare button, and an Export dropdown. Below the toolbar, six collapsible diff sections display the comparison results using PatternFly ExpandableSection with composable Tables inside. The page supports URL-shareable comparisons via left and right query parameters and includes loading skeleton states and an empty state with CodeBranchIcon.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.tsx` -- Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff section rendering
- `src/pages/SbomComparePage/components/DiffSection.tsx` -- Reusable collapsible diff section component using PatternFly ExpandableSection with count Badge and data Table
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` -- Table for added packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` -- Table for removed packages (columns: Package Name, Version, License, Advisories count)
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` -- Table for version changes (columns: Package Name, Left Version, Right Version, Direction)
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` -- Table for new vulnerabilities (columns: Advisory ID, Severity via SeverityBadge, Title, Affected Package); rows with Critical severity get highlighted background
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` -- Table for resolved vulnerabilities (columns: Advisory ID, Severity, Title, Previously Affected Package)
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` -- Table for license changes (columns: Package Name, Left License, Right License)

## Files to Modify
- `src/routes.tsx` -- Add route definition for /sbom/compare pointing to SbomComparePage (lazy-loaded)

## Implementation Notes
- **PatternFly components (per Figma design)**: Use `Select` (single, typeahead) for SBOM selector dropdowns, `ExpandableSection` for each diff section, `Badge` (color-coded: green for added/resolved, red for removed/new-vuln, blue for version changes, yellow for license changes) for item counts, `Table` (composable, sortable) for data tables inside each section, `EmptyState` with `CodeBranchIcon` for the initial empty state ("Select two SBOMs to compare"), `Skeleton` for loading states, `Dropdown` for the Export button.
- **SeverityBadge**: Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for vulnerability severity display in NewVulnerabilitiesTable and ResolvedVulnerabilitiesTable.
- **SBOM selectors**: Use the existing `useSboms` hook from `src/hooks/useSboms.ts` to populate the selector dropdowns. Display SBOM name and version.
- **URL-shareable state**: Read left and right from URL search params on mount using React Router's useSearchParams. When the user clicks Compare, update URL search params. Pre-populate selectors from URL params.
- **Section expand behavior**: Sections with >0 items default to expanded; sections with 0 items default to collapsed.
- **Critical vulnerability highlighting**: In NewVulnerabilitiesTable, rows where severity is "critical" should have a highlighted/warning background row style.
- **Loading state (per Figma)**: While comparison API call is in progress, show Skeleton placeholders in each diff section area and disable the header toolbar controls.
- **Empty state (per Figma)**: When no comparison has been performed (no query params, page first load), show PatternFly EmptyState with CodeBranchIcon, title "Select two SBOMs to compare", body "Choose an SBOM for each side and click Compare to see what changed."
- **Export dropdown**: Secondary button with "Export JSON" and "Export CSV" options. Disabled until comparison result is loaded.
- Follow the existing page structure pattern in `src/pages/` for component organization.
- Follow React Router v6 lazy-loading pattern in `src/routes.tsx` matching existing route definitions.
- Per CONVENTIONS.md Component naming: use PascalCase for all component files. Applies: task creates `src/pages/SbomComparePage/SbomComparePage.tsx` matching the convention's `.tsx` scope.

## Acceptance Criteria
- [ ] Page renders at /sbom/compare with two SBOM selector dropdowns and Compare button
- [ ] Both SBOM selectors are populated from the SBOM list API via useSboms hook
- [ ] Compare button is disabled until both selectors have values
- [ ] Clicking Compare calls the comparison API via useSbomComparison and renders six diff sections
- [ ] URL is updated with left and right query params when Compare is clicked
- [ ] Page loads comparison directly when URL contains left and right params (URL-shareable)
- [ ] Each diff section shows correct count Badge with appropriate color
- [ ] Sections with >0 items are expanded by default; empty sections are collapsed
- [ ] Critical vulnerabilities are visually highlighted in the New Vulnerabilities section
- [ ] Empty state with CodeBranchIcon is shown when no comparison has been performed
- [ ] Skeleton loading state is shown while the comparison API call is in progress
- [ ] Export dropdown is present but disabled when no comparison is loaded
- [ ] Route is registered in src/routes.tsx with lazy loading

## Test Requirements
- [ ] Unit test: page renders empty state when no query params are present
- [ ] Unit test: selectors populate with SBOM list data
- [ ] Unit test: Compare button enables when both selectors have values
- [ ] Unit test: clicking Compare triggers API call and renders diff sections
- [ ] Unit test: URL params pre-populate selectors and trigger comparison on mount
- [ ] Unit test: critical vulnerability rows are highlighted
- [ ] Unit test: sections with zero items are collapsed by default

## Dependencies
- Depends on: Task 5 -- Frontend API types and client for SBOM comparison
