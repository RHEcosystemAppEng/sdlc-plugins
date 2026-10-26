# Plan Summary — TC-9003: SBOM Comparison View

## Tasks Created

| # | Summary | Repository | Type |
|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-backend | Bookend (create-branch) |
| 2 | Add SBOM comparison model types | trustify-backend | Implementation |
| 3 | Add SBOM comparison service and REST endpoint | trustify-backend | Implementation |
| 4 | Add SBOM comparison endpoint integration tests | trustify-backend | Implementation |
| 5 | Add SBOM comparison API client and React Query hook | trustify-ui | Implementation |
| 6 | Build SBOM comparison page UI with diff sections | trustify-ui | Implementation |
| 7 | Add comparison route and SBOM list selection | trustify-ui | Implementation |
| 8 | Add SBOM comparison export (JSON/CSV) | trustify-ui | Implementation (non-MVP) |
| 9 | Update documentation for SBOM comparison feature | trustify-backend | Documentation |
| 10 | Merge feature branch TC-9003 to main | trustify-backend | Bookend (merge-branch) |

## Repositories Affected

- **trustify-backend** — new comparison model types, service logic, REST endpoint, and integration tests
- **trustify-ui** — new comparison page UI, API client/hook, route registration, SBOM list page selection, and export functionality

## Architecture Summary

The feature adds a side-by-side SBOM comparison capability spanning two repositories:

**Backend (trustify-backend):** A new `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint computes a structured diff between two SBOMs on-the-fly (no new database tables). The diff service compares linked packages, advisories, and licenses to produce six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The implementation reuses existing `SbomService`, `PackageService`, and `AdvisoryService` for data retrieval.

**Frontend (trustify-ui):** A new comparison page at `/sbom/compare` renders the diff result using PatternFly 5 components (ExpandableSection, Table, Select, Badge, EmptyState). The SBOM list page is extended with checkbox selection and a "Compare selected" button. URLs are shareable via query parameters. The data layer follows the existing pattern: TypeScript interfaces in `models.ts`, REST client function in `rest.ts`, React Query hook in `hooks/`.

**Workflow mode:** Feature-branch (`TC-9003`) — the frontend comparison page requires the backend endpoint; neither side functions independently.

## Inherited Field Values

- **Priority:** `Critical` — inherited from Feature TC-9003 and propagated to all created tasks via `additional_fields.priority`.
- **fixVersions:** `RHTPA 1.5.0` — inherited from Feature TC-9003 and propagated to all created tasks via `additional_fields.fixVersions`. No `fixVersion scope` configuration exists in CLAUDE.md's Jira Configuration, so the default scope `"both"` applies (propagate to tasks).

## additional_fields applied to all created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
