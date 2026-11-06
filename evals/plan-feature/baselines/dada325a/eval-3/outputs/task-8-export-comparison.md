# Task 8 — Export comparison as JSON or CSV (non-MVP)

**Summary:** Implement "Export JSON" / "Export CSV" in the comparison toolbar
**Epic:** TC-9003: SBOM comparison UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the "Export" dropdown from the Figma header toolbar. It offers "Export JSON" and "Export CSV", so compliance officers can download the diff as a document (Feature goal: "Provide exportable diff report for compliance documentation"). The Feature marks this requirement **non-MVP**: schedule it after the MVP tasks, and it may be deferred without blocking the rest of TC-9003. Export runs client-side on the already-loaded `SbomComparison`, so no backend change is needed.

## Files to Modify
- `src/pages/SbomComparePage/components/CompareToolbar.tsx` — wire the "Export" `Dropdown` items to the export functions; enabled only when comparison data is loaded

## Files to Create
- `src/utils/exportComparison.ts` — `toComparisonJson(comparison)`, `toComparisonCsv(comparison)`, and `downloadFile(content, filename, mime)` helpers
- `src/utils/exportComparison.test.ts` — unit tests for the serializers

## Implementation Notes
- JSON export: pretty-print the `SbomComparison` exactly as the API returned it (`JSON.stringify(data, null, 2)`). Add a small header object with the `left` and `right` SBOM IDs and an export timestamp, formatted with `src/utils/formatDate.ts`.
- CSV export: one flat CSV with a `category` column (`added_package`, `removed_package`, `version_change`, `new_vulnerability`, `resolved_vulnerability`, `license_change`) and the union of fields. Escape commas, quotes, and newlines per RFC 4180. Keep severity and direction as the raw API values in CSV for machine readability, and document that choice.
- Filename: `sbom-compare-{left}-{right}.{json|csv}`. Trigger the download through a Blob URL and revoke it afterwards.
- The Figma Export dropdown must stay disabled until a result has loaded. Task 5 already renders it disabled; this task supplies the enabled behavior.

**Conventions:**
- Per CONVENTIONS.md §Naming: camelCase utility module (`exportComparison.ts`) in `src/utils/`, next to `formatDate.ts`.
  Applies: task modifies `src/utils/exportComparison.ts` matching the convention's utilities naming (`src/utils/*.ts`) scope.
- Per CONVENTIONS.md §Component library: use PF5 `Dropdown` / `DropdownItem` for the Export menu.
  Applies: task modifies `src/pages/SbomComparePage/components/CompareToolbar.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Testing: Vitest unit tests for the serializers.
  Applies: task modifies `src/utils/exportComparison.test.ts` matching the convention's Vitest unit test scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits, `Implements TC-XXXX` footer, `Assisted-by:` trailer.
- §3: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5: Change only the listed files; reuse `formatDate`.

## Reuse Candidates
- `src/utils/formatDate.ts` — timestamp formatting for the export header.
- `src/api/models.ts::SbomComparison` — added in Task 4; the export input type.

## Acceptance Criteria
- [ ] The "Export" dropdown has exactly two items: "Export JSON" and "Export CSV"
- [ ] The dropdown is disabled until a comparison result has loaded
- [ ] "Export JSON" downloads a file containing the full comparison and the left/right SBOM IDs
- [ ] "Export CSV" downloads a valid RFC 4180 CSV with one row per diff entry and a `category` column
- [ ] Downloaded filenames include both SBOM IDs

## Test Requirements
- [ ] Unit test: the JSON serializer round-trips the fixture comparison
- [ ] Unit test: the CSV serializer produces the expected header and row count, and escapes values containing commas or quotes
- [ ] Component test: clicking "Export CSV" calls the download helper with a `text/csv` Blob

## Verification Commands
- `npx vitest run src/utils/exportComparison.test.ts` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, and empty/loading states
