# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add SBOM comparison diff model types (SbomComparisonResult with six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- Implement comparison diff logic in SbomService (fetch packages, advisories, and licenses for two SBOMs, compute set differences on-the-fly from existing data)
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint with query parameter validation and error handling
- Add integration tests for the comparison endpoint covering success, missing params, invalid IDs, and not-found scenarios
- Add documentation for the comparison API endpoint and UI workflow (New Content per Documentation Considerations)

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison response (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- Add `compareSboms(leftId, rightId)` client function in `src/api/rest.ts`
- Add `useSbomComparison` React Query hook in `src/hooks/`
- Implement SBOM comparison page at `/sbom/compare` with header toolbar (SBOM selectors via PatternFly Select typeahead, Compare button, Export dropdown)
- Implement six collapsible diff sections (PatternFly ExpandableSection) with data tables and count badges
- Implement empty state (PatternFly EmptyState with CodeBranchIcon) and loading state (PatternFly Skeleton)
- Highlight rows for packages with new critical vulnerabilities
- Implement virtualized rendering for tables with >100 rows
- Implement export as JSON and CSV for compliance documentation
- Register `/sbom/compare` route in React Router with lazy loading
- Add checkbox selection and "Compare selected" button to SBOM list page
- Encode both SBOM IDs in URL query parameters for shareable comparison links

## Workflow Mode

- **Selected mode:** `direct-to-main`
- **Rationale:** No atomicity indicators found:
  1. No coordinated schema migrations — the feature explicitly states "no new database tables; compute diff on-the-fly from existing data."
  2. No breaking API changes — only a new additive endpoint is created; no existing endpoints are modified.
  3. No cross-cutting refactors — changes are confined to new files in both repositories with minimal modifications to existing files (route registration, module re-exports).
  4. Tightly coupled feature components — partially applicable (the frontend comparison page requires the backend endpoint), but the backend side functions independently as a purely additive endpoint. With dependency ordering (backend tasks completed before frontend tasks), each merge to main is safe independently. The criterion requires "neither side functions independently," which is not met since the backend is independently deployable.
- **Cross-repo dependency ordering:** Backend tasks (1-2) must complete before frontend tasks (3-5) that depend on the comparison endpoint.

## Epic Grouping (by-sub-feature)

Per Hierarchy Configuration in CLAUDE.md, tasks are grouped by logical sub-features:

- **Epic: TC-9003: Backend comparison service** — Tasks 1, 2
- **Epic: TC-9003: Frontend comparison UI** — Tasks 3, 4, 5
- **Epic: TC-9003: Documentation** — Task 6

## Task Summary

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | Implement SBOM comparison diff service and model types | trustify-backend | None |
| 2 | Add SBOM comparison REST endpoint with integration tests | trustify-backend | Task 1 |
| 3 | Add SBOM comparison API types, client function, and React Query hook | trustify-ui | Task 2 |
| 4 | Implement SBOM comparison page with diff sections and export | trustify-ui | Task 3 |
| 5 | Add comparison route and SBOM list page integration | trustify-ui | Task 4 |
| 6 | Document SBOM comparison endpoint and UI workflow | trustify-backend | Tasks 1-5 |

## Inherited Field Propagation

- **Priority:** Critical (inherited from Feature TC-9003; propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from Feature TC-9003; propagated to all tasks — fixVersion scope defaults to "both" since no Jira Field Defaults override is configured)
- **Labels:** ai-generated-jira (applied to all created issues)

## Additional Fields (per task)

All tasks are created with:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
