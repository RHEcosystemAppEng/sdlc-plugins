# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison model types (`SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
  - Add SBOM comparison service logic to compute structured diff between two SBOMs using existing package, advisory, and license data — no new database tables
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
  - Register the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs`
  - Add integration tests for the comparison endpoint in `tests/api/sbom.rs`

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types in `src/api/models.ts`
  - Add API client function `compareSboms(leftId, rightId)` in `src/api/rest.ts`
  - Add React Query hook `useSbomCompare` in `src/hooks/`
  - Add `SbomComparePage` component at `src/pages/SbomComparePage/` with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Register `/sbom/compare` route in `src/routes.tsx`
  - Add checkbox selection and "Compare selected" button to `src/pages/SbomListPage/SbomListPage.tsx`
  - Add MSW mock handler and fixture data for the comparison endpoint in `tests/mocks/`
  - Add unit tests for `SbomComparePage` and E2E tests for the comparison workflow

## Excluded requirements

None. All requirements (MVP and non-MVP) from the Feature description can be decomposed into actionable tasks with the available repositories and design context.

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** — Not applicable. The feature computes diffs on-the-fly from existing package and advisory data; no new database tables or schema changes are required.
2. **Breaking API changes** — Not applicable. The comparison endpoint is a new addition (`GET /api/v2/sbom/compare`); no existing endpoints are modified.
3. **Cross-cutting refactors** — Not applicable. No shared types, module reorganizations, or structural changes span multiple tasks in a way that would leave the codebase inconsistent.
4. **Tightly coupled feature components** — Not applicable. The backend comparison endpoint can be merged to `main` independently without breaking any existing functionality. The frontend comparison page depends on the backend endpoint, but this is a sequential dependency satisfied by task ordering, not an all-or-nothing delivery requirement.

All tasks target branch `main` with sequential dependencies ensuring correct merge order (backend before frontend).

---

## Epic Grouping (by-sub-feature)

| Epic | Label | Tasks |
|---|---|---|
| Epic 1 | TC-9003: Backend comparison API | Task 1, Task 2 |
| Epic 2 | TC-9003: Frontend comparison UI | Task 3, Task 4, Task 5, Task 6 |
| Epic 3 | TC-9003: Documentation | Task 7 |

---

## Task Creation — additional_fields

All created issues (Epics and Tasks) will include:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: inherited from Feature TC-9003 (Critical). Not "Undefined", so it is propagated.
- **fixVersions**: inherited from Feature TC-9003 (RHTPA 1.5.0). The `fixVersion scope` setting is absent from Jira Field Defaults (no `### Jira Field Defaults` section in CLAUDE.md), so the default `"both"` applies — fixVersions are propagated to tasks.

---

## Documentation Signals

- **Doc impact type**: New Content
- **Details**: Document the comparison endpoint and comparison UI
- **User purpose**: API consumers need endpoint reference; UI users need a guide for the comparison workflow
- **Reference material**: Existing SBOM detail page documentation, package/advisory data model docs
