# Repository Impact Map — TC-9003: SBOM comparison view

## Inputs

- Feature: TC-9003 "SBOM comparison view" (Priority: Critical, Fix Versions: RHTPA 1.5.0, Status: New)
- Figma: https://www.figma.com/design/mock123/SBOMCompare (design context from `figma-context.md`)
- Repositories analyzed: trustify-backend (`repo-backend.md`), trustify-ui (`repo-frontend.md`)
- Code intelligence: no Serena instances configured — analysis performed from the provided repository structures (Glob/Grep/Read fallback)

## Step 0 – Project Configuration check

- Repository Registry: present (1+ entries) — PASS
- Jira Configuration: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142 — PASS
- Code Intelligence: present (tool naming convention documented; no instances) — PASS

Note: trustify-backend and trustify-ui are not rows in this project's Repository Registry; they are treated as the target repositories for this eval from the supplied fixtures.

## Step 1 / 1.5 – Feature extraction

- Priority: `Critical` (set, not "Undefined") → propagate
- fixVersions: `[RHTPA 1.5.0]` (non-empty) → propagate (fixVersion scope = `both`)
- Parent link (Step 1.5): no parent on the Feature; prompt skipped in eval mode (no parent linked)
- Documentation signals: **New Content** — document the comparison endpoint and comparison UI; user purpose: API reference + UI workflow guide; reference material: SBOM detail page docs, package/advisory data model docs

## Step 2.5 – Issue types (simulated — Jira not contacted)

```
Type-to-role mapping (assumed; must be confirmed via jira.get_project_issue_types):
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (level: 1)
  Task:    Task    (level: 0)
```

Hierarchy Configuration in CLAUDE.md: `Default epic grouping strategy: by-sub-feature` → applied.

## Step 3 – Repository analysis highlights

**Backend API discovery (contracts for frontend tasks):**
- `GET /api/v2/sbom` — existing; returns `PaginatedResults<SbomSummary>` (`modules/fundamental/src/sbom/endpoints/list.rs`, `common/src/model/paginated.rs`)
- `GET /api/v2/sbom/{id}` — existing; returns `SbomDetails` (`modules/fundamental/src/sbom/endpoints/get.rs`)
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — **does not exist**; to be created (Tasks 2–3) with the response shape from the Figma context (six snake_case arrays)

**Shared-artifact producer/consumer analysis:**
- Artifacts read by the diff: `sbom_package` (`entity/src/sbom_package.rs`), `package_license` (`entity/src/package_license.rs`), `sbom_advisory` (`entity/src/sbom_advisory.rs`)
- Producers: SBOM ingestion `modules/ingestor/src/graph/sbom/mod.rs` (packages, licenses, SBOM–package links); advisory ingestion/correlation `modules/ingestor/src/graph/advisory/mod.rs` (SBOM–advisory links); orchestrated by `modules/ingestor/src/service/mod.rs`
- Consumers (existing): `SbomService`, `PackageService`, `AdvisoryService`; (new) compare service
- Conclusion: the feature is a read-only consumer; no producer changes are required and no acceptance criterion depends on changing how artifacts are populated. Vulnerability diff sections reflect the correlation state at query time (documented in Task 9). No scope conflict.

**Fail-open risk identified:** a missing/unknown SBOM ID or a failed request could render as an empty diff ("nothing changed"). Fail-closed ACs + tests added to Tasks 2, 3, 4, 5, 8.

**CONVENTIONS.md:** present in both repositories (Key Conventions); applicable conventions propagated into each task with `Applies:` rationales.

**Convention discrepancy:** trustify-ui CONVENTIONS.md says kebab-case directories, but existing page directories are PascalCase (`src/pages/SbomListPage/`). Tasks follow the on-disk pattern and flag it.

**Testing readiness template:** `docs/testing-readiness.md` not present in either repository → no testing tasks generated.

**Documentation files:** `README.md`, `CONVENTIONS.md` in both repos.

**Eval infrastructure:** not applicable (no skill `SKILL.md` changes).

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison response model (added/removed packages, version changes, new/resolved vulnerabilities, license changes) in the sbom module
    - Add diff service that computes the comparison on-the-fly from sbom_package, package_license and sbom_advisory data (no new tables), failing with not-found for unknown SBOM IDs
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint registered in the sbom endpoints module, with 400/404 handling
    - Add integration tests for the compare endpoint in tests/api/sbom.rs
    - Add endpoint reference and comparison workflow documentation

trustify-ui:
  changes:
    - Add SbomComparison types, compareSboms() REST function, useSbomComparison hook and MSW mocks/fixtures
    - Add lazy-loaded /sbom/compare page with left/right SBOM selectors, Compare button, URL-encoded left/right state, empty, loading and error states
    - Render six collapsible diff sections with colored count badges, sortable tables, Critical-row highlighting for new vulnerabilities and virtualization above 100 rows
    - Add checkbox selection and "Compare selected" action on the SBOM list page navigating to the comparison URL
    - Add Export dropdown producing JSON and CSV downloads of the diff (non-MVP)
```

## Excluded requirements

- **"Add comparison endpoint to the API latency Grafana dashboard"** (Customer Information/Supportability) — no repository containing Grafana dashboard definitions is available in the Repository Registry or the provided inputs. Missing input: the dashboards/monitoring repository and its dashboard definition paths. Task 3 adds request instrumentation so the endpoint emits latency metrics, but the dashboard panel itself is not planned.
- **"Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM)"** — alerting configuration repository not provided. Missing input: monitoring/alerting repository and alert rule conventions.

## Open questions (do not block planning)

- **Same-product constraint:** "Both SBOMs must be from the same product/project for a meaningful comparison" — should the backend reject (e.g., 400) or the UI warn on cross-product comparisons? Currently planned as no enforcement; confirm with product owner.
- **Very large diffs (>1000 package changes):** Customer Considerations mention pagination/filtering; the NFR and Figma specify virtualization with no pagination. Planned as virtualization only (Task 6).
- **Left/right ordering from the list page:** planned as first-selected = left, preferring older = left when an ingestion date is available (Task 7).

## Step 4.5 – Workflow mode

**Selected mode: `feature-branch`**

Atomicity indicators found:
- **Tightly coupled feature components (indicator 4):** the new `/sbom/compare` UI (Tasks 4–8) requires `GET /api/v2/sbom/compare`, which does not yet exist (Tasks 2–3). Merging the UI alone breaks the page; merging the UI data layer before the endpoint makes every comparison request fail.
- Within trustify-backend, Task 3 (endpoint) depends on the model/service types introduced in Task 2.

Not found: coordinated schema migrations (no new tables per NFR), breaking changes to existing API contracts, cross-cutting refactors.

Interdependent tasks: Task 2 → Task 3 → Task 4 → Tasks 5/6/7/8. The `workflow:feature-branch` label will be applied to TC-9003 in Step 6a.

Bookend repository: trustify-ui (5 of 8 intermediate tasks). The trustify-backend intermediate tasks also target a `TC-9003` branch in trustify-backend (see Task 1 description).

## Epic grouping (by-sub-feature, from Hierarchy Configuration)

| Epic summary | Tasks |
|---|---|
| TC-9003: SBOM diff API | Task 2, Task 3 |
| TC-9003: SBOM comparison UI | Task 4, Task 5, Task 6, Task 7, Task 8 |
| TC-9003: Delivery and documentation | Task 1, Task 9, Task 10 |

(by-sub-feature groupings require user approval; treated as approved in eval mode.)

## Task list

| # | Summary | Repository | Target Branch | Epic | Depends on |
|---|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-ui | main | Delivery and documentation | — |
| 2 | Add SBOM comparison response model and on-the-fly diff service | trustify-backend | TC-9003 | SBOM diff API | 1 |
| 3 | Add GET /api/v2/sbom/compare endpoint with integration tests | trustify-backend | TC-9003 | SBOM diff API | 1, 2 |
| 4 | Add SBOM comparison API client and useSbomComparison hook | trustify-ui | TC-9003 | SBOM comparison UI | 1, 3 |
| 5 | Add /sbom/compare page shell with SBOM selectors and URL-shareable state | trustify-ui | TC-9003 | SBOM comparison UI | 1, 4 |
| 6 | Render the six SBOM diff sections with count badges, sortable tables, and critical highlighting | trustify-ui | TC-9003 | SBOM comparison UI | 1, 5 |
| 7 | Add two-SBOM checkbox selection and "Compare selected" on the SBOM list page | trustify-ui | TC-9003 | SBOM comparison UI | 1, 5 |
| 8 | Add Export dropdown to download the SBOM diff as JSON or CSV (non-MVP) | trustify-ui | TC-9003 | SBOM comparison UI | 1, 5, 6 |
| 9 | Document the SBOM comparison API endpoint and comparison UI workflow | trustify-backend | TC-9003 | Delivery and documentation | 1–8 |
| 10 | Merge feature branch TC-9003 to main | trustify-ui | main | Delivery and documentation | 2–9 |

## Requirement coverage

| Requirement | MVP | Covered by |
|---|---|---|
| `GET /api/v2/sbom/compare` structured diff | Yes | Tasks 2, 3 |
| Frontend comparison page at `/sbom/compare` | Yes | Tasks 4, 5, 6 |
| URL-shareable comparison | Yes | Task 5 (URL state), Task 7 (list entry point) |
| Export diff as JSON or CSV | No | Task 8 |
| Highlight packages with new critical vulnerabilities | Yes | Task 6 |
| NFR: p95 < 1s for 2000 packages | — | Tasks 2, 3 |
| NFR: virtualized lists > 100 rows | — | Task 6 |
| NFR: no new database tables | — | Task 2 |
| UC-1 select two SBOMs on list page | — | Task 7 |
| Documentation (New Content) | — | Task 9 |
| Grafana dashboard / timeout monitoring | — | Excluded (see above) |

## Jira field values (`additional_fields`)

Applied to every created Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- priority: `Critical` — propagated (Feature priority set, not "Undefined")
- fixVersions: `RHTPA 1.5.0` — propagated (Feature has fixVersions; `fixVersion scope: both`)
- Task `parent`: the Epic key for its group (see Epic grouping)
- Epic `parent`: TC-9003
- Feature TC-9003 labels after Step 6a: `["ai-generated-jira", "workflow:feature-branch"]` (existing labels preserved)
