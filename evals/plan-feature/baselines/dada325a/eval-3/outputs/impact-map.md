# TC-9003 — Repository Impact Map and Planning Log

**Feature:** TC-9003 — SBOM comparison view
**Skill:** sdlc-workflow/plan-feature v0.13.10 (eval run: Jira/Figma/Serena were not called; their inputs came from the eval fixture files)

---

## Step 0 — Project Configuration validation
- Repository Registry: present (1 entry)
- Jira Configuration: project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
- Code Intelligence: present. No Serena instances are configured, so repository analysis used the fallback (the repository structure fixtures `repo-backend.md` and `repo-frontend.md`).
- Result: **PASS**

## Step 1 — Feature fields extracted
| Field | Value |
|---|---|
| Title | SBOM comparison view |
| Priority | **Critical** (set; not "Undefined") |
| fixVersions | **RHTPA 1.5.0** |
| Labels | ai-generated-jira |
| Figma link | https://www.figma.com/design/mock123/SBOMCompare |
| Documentation signals | **New Content**: document the comparison endpoint (API reference) and the comparison UI (workflow guide). Reference material: SBOM detail page docs, package/advisory data model docs. |

## Step 1.5 — Parent link
No `parent` on the Feature. The interactive prompt "Link this Feature to a parent issue?" is skipped in this non-interactive eval, so no parent link is created.

## Step 2 — Figma design context (SBOMCompare / Comparison View)
- **UI structure:** header toolbar (left/right typeahead `Select`, primary "Compare" button, secondary "Export" `Dropdown`) above six stacked `ExpandableSection`s, each with a count `Badge` and a composable `Table`. There is an empty state (`CodeBranchIcon` as fallback for `ComparisonIcon`) and a loading state (`Skeleton` per section, toolbar disabled).
- **Components:** existing `SeverityBadge`; existing `useSboms` hook for the selectors.
- **Backend interactions:** `GET /api/v2/sbom` (existing), `GET /api/v2/sbom/compare?left&right` (new).
- **Custom sub-components:** the colored count badge (PF5 `Badge` has no color variants, so use PF `Label` colors or PF tokens) and the critical-row highlight (danger background token). Figma supplied no hex values, so each maps to the nearest PF token. Specs are in Task 6.
- **Data rendering scope:** each table is per-context to its section and renders only `comparison.<section_array>` (Task 6).
- **Display text vs API value:** `severity` is lowercase in the API but title case in `SeverityBadge`/Figma, so a frontend mapping is needed. `direction` is lowercase `upgrade`/`downgrade`, so a frontend mapping to "Upgrade"/"Downgrade" is needed. `advisory_count` matches as is. Mapping tables are in Task 6.

## Step 2.5 — Issue type discovery
`jira.get_project_issue_types` was not called (no external services). Simulated type-to-role mapping, assuming a standard Jira Cloud hierarchy:
```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)    # from CLAUDE.md
  Epic:    Epic    (ID: <discovered at runtime>, level: 1)
  Task:    Task    (ID: <discovered at runtime>, level: 0)
```
Hierarchy Configuration override: `Default epic grouping strategy: by-sub-feature`, applied.
If runtime discovery finds no level-1 type, skip Epic creation and link the tasks directly to the Feature with "Incorporates".

## Step 3 — Repository analysis highlights
- **Repository Registry gap:** the registry in CLAUDE.md lists only `sdlc-plugins`. The feature targets `trustify-backend` and `trustify-ui`, which the eval supplies as structure fixtures. Neither has a Serena instance, so the analysis relied on the fixture directory trees and Key Conventions. Before running implement-task, register both repositories (paths and Serena instances).
- **CONVENTIONS.md:** present at both repo roots. The conventions were taken from each fixture's "Key Conventions" section and propagated into every implementation task with `Applies:` rationales.
- **Documentation files found:** `trustify-backend/README.md`, `trustify-backend/CONVENTIONS.md`, `trustify-ui/README.md`, `trustify-ui/CONVENTIONS.md`.
- **Testing readiness template (`docs/testing-readiness.md`):** not present in either repository, so no testing tasks were generated.
- **Discovered backend API contracts:**
  - `GET /api/v2/sbom` returns `PaginatedResults<SbomSummary>` (`{ items, total }`). See `modules/fundamental/src/sbom/endpoints/list.rs`.
  - `GET /api/v2/sbom/{id}` returns `SbomDetails`. See `modules/fundamental/src/sbom/endpoints/get.rs`.
  - `GET /api/v2/sbom/compare?left&right` is **new**. Its shape comes from the Figma backend-interaction spec (created in Tasks 2–3).
- **Reuse candidates:** `SbomService`, `PackageService` / `PackageSummary` (license), `AdvisoryService` / `AdvisorySummary` (severity), `common/src/db/query.rs`, `AppError`, `SeverityBadge`, `severityUtils`, `useSboms`, `useSbomById` pattern, `EmptyStateCard`, `PackageTable`, `AdvisoryList`, `FilterToolbar`, `formatDate`.
- **Shared-artifact analysis:** not applicable. The diff is computed read-only from existing data, and the feature introduces no new shared artifact. Existing ingestion (`modules/ingestor/src/graph/sbom`, `.../advisory`) populates the source data unchanged.
- **Eval infrastructure:** not applicable (no `SKILL.md` is modified).

---

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison response model (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add on-the-fly SBOM diff computation in the SBOM service, using existing sbom_package, package, package_license, and sbom_advisory data (no new tables)
    - Return not-found (404) for unknown SBOM IDs instead of an empty diff
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint and register it in the SBOM route builder
    - Add integration tests for the compare endpoint (diff correctness, 400/404, route precedence, 2000-package performance)
    - Document the compare endpoint in README / API reference (endpoint reference and comparison workflow docs)

trustify-ui:
  changes:
    - Add SbomComparison TypeScript types, compareSboms() REST function, and useSbomComparison React Query hook, with MSW mocks
    - Add /sbom/compare page with left/right SBOM selectors, Compare button, and URL-encoded left/right state (shareable)
    - Add empty, loading (Skeleton), and error states to the comparison page
    - Render six collapsible diff sections with colored count badges and sortable tables
    - Highlight new critical vulnerabilities and virtualize tables with more than 100 rows
    - Add checkbox selection and a "Compare selected" action to the SBOM list page, plus an E2E test
    - Add JSON/CSV export of the comparison result (non-MVP)
```

### Excluded requirements
| Requirement | Source | Missing input that prevents planning |
|---|---|---|
| Add comparison endpoint to the API latency Grafana dashboard | Customer Information/Supportability | **No target repository**: no monitoring/dashboard repository (Grafana dashboards-as-code) is in the Repository Registry. Task 3 gives the handler a stable route name/tracing span so the dashboard can be added once the repository is identified. |
| Monitor for timeouts on large SBOM comparisons (more than 2000 packages per SBOM) | Customer Information/Supportability | **No target repository** for alerting rules, and **insufficient specification** (no timeout threshold or alert channel defined). The p95 < 1s performance test is covered in Task 3. |
| Pagination or filtering for very large diffs (more than 1000 package changes) | Customer Considerations ("may require") | **Insufficient specification**: the Figma contract defines an unpaginated response, and the requirement is conditional ("may"). Frontend virtualization (Task 6) covers rendering; no server-side pagination was planned. Needs a product decision on whether pagination is in scope. |

Non-MVP requirement "Export diff as JSON or CSV" is **planned** (Task 8). Figma specifies it fully, so nothing is missing, but it is marked non-MVP and can be deferred.

### Open questions / scope conflicts
1. **Package-to-advisory correlation:** the visible entity layer has `sbom_advisory` (SBOM level) but no package-advisory join. That join is needed for `affected_package`, `previously_affected_package`, and `advisory_count`. Task 2 must verify the correlation in `modules/ingestor/src/graph/advisory/mod.rs` before implementing, and escalate on TC-9003 if only SBOM-level links exist.
2. **Feature branch in two repositories:** feature-branch mode needs `TC-9003` in both `trustify-backend` and `trustify-ui`. The bookend template allows a single repository, so the bookends are assigned to `trustify-ui`, which has most of the tasks (5 of 8 intermediate). The engineer running Task 1 must also create `TC-9003` in `trustify-backend`. Task 10's merge must be coordinated with the backend `TC-9003` → `main` merge. Confirm, or approve separate per-repo bookends.
3. **Same-product constraint:** the backend contract does not enforce it. The UI shows a non-blocking warning (Task 5). Confirm that the backend should not reject cross-product comparisons.

---

## Step 4.5 — Workflow mode decision
**Mode: `feature-branch`**

Atomicity indicators evaluated:
1. Coordinated schema migrations: **not present** (no new tables, per the NFR).
2. Breaking API changes: **not present** (the endpoint is additive).
3. Cross-cutting refactors: **not present**.
4. Tightly coupled feature components: **PRESENT**. The new `/sbom/compare` UI page (Tasks 4–8) calls `GET /api/v2/sbom/compare`, which does not exist yet (Tasks 2–3). The "Compare selected" entry point (Task 7) would route users to a page whose API is missing if the frontend landed on `main` alone.

Interdependent tasks: Task 4 (API client) → Tasks 5, 6, 7, 8 (UI) depend on Task 3 (endpoint) → Task 2 (diff service).
The `workflow:feature-branch` label is added to TC-9003 in Step 6a, preserving the existing `ai-generated-jira` label.

---

## Step 5 — Epic grouping (by-sub-feature, from Hierarchy Configuration)
Suggested groupings (in an interactive run, these are shown to the user for approval before tasks are finalized):

| Epic | Summary | Tasks |
|---|---|---|
| A | TC-9003: SBOM diff API | Task 2, Task 3 |
| B | TC-9003: SBOM comparison UI | Task 4, Task 5, Task 6, Task 7, Task 8 |
| C | TC-9003: Delivery and documentation | Task 1, Task 9, Task 10 |

Epic descriptions (plain text):
- **A — TC-9003: SBOM diff API:** Backend work in trustify-backend: the SbomComparison model, on-the-fly diff computation from existing package, license, and advisory data, and the new GET /api/v2/sbom/compare endpoint with integration and performance tests.
- **B — TC-9003: SBOM comparison UI:** Frontend work in trustify-ui: comparison API client and hook, the /sbom/compare page with selectors and URL-shareable state, six collapsible diff sections with critical highlighting and virtualization, the "Compare selected" entry point on the SBOM list, and JSON/CSV export (non-MVP).
- **C — TC-9003: Delivery and documentation:** Feature-branch bookends (create and merge TC-9003) and the documentation task for the compare endpoint and comparison UI workflow.

## Task list
| # | File | Summary | Repository | Target Branch | Epic | Depends on |
|---|---|---|---|---|---|---|
| 1 | task-1-create-feature-branch.md | Create feature branch TC-9003 from main | trustify-ui | main | C | — |
| 2 | task-2-sbom-diff-model-and-service.md | Add SBOM comparison response model and on-the-fly diff computation in SbomService | trustify-backend | TC-9003 | A | 1 |
| 3 | task-3-sbom-compare-endpoint.md | Add GET /api/v2/sbom/compare endpoint with integration tests | trustify-backend | TC-9003 | A | 1, 2 |
| 4 | task-4-frontend-compare-api-client.md | Add SbomComparison types, compareSboms() client, and useSbomComparison hook | trustify-ui | TC-9003 | B | 1, 3 |
| 5 | task-5-sbom-compare-page-shell.md | Add /sbom/compare page with header toolbar, URL-shareable state, empty and loading states | trustify-ui | TC-9003 | B | 1, 4 |
| 6 | task-6-sbom-diff-sections.md | Add collapsible diff sections with count badges, virtualized tables, and critical highlighting | trustify-ui | TC-9003 | B | 1, 4, 5 |
| 7 | task-7-sbom-list-compare-selection.md | Add checkbox selection and "Compare selected" action to SbomListPage | trustify-ui | TC-9003 | B | 1, 5, 6 |
| 8 | task-8-export-comparison.md | Implement "Export JSON" / "Export CSV" in the comparison toolbar (non-MVP) | trustify-ui | TC-9003 | B | 1, 4, 5 |
| 9 | task-9-documentation.md | Document the SBOM comparison API endpoint and comparison UI workflow | trustify-backend | TC-9003 | C | 3, 5, 6, 7, 8 |
| 10 | task-10-merge-feature-branch.md | Merge feature branch TC-9003 to main | trustify-ui | main | C | 2–9 |

Bookend idempotency guard: TC-9003 has no linked issues ("Linked Issues: None"), so no existing "Create/Merge feature branch" tasks exist and bookends were generated.

---

## Step 6 — Task creation log (simulated; no Jira calls made)

### 6a.0 — Epics
Each Epic is created as `issueTypeName=Epic`, `parent=TC-9003`, with:
```json
additional_fields = {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

### 6a — Tasks
Every task (1–10) is created as `issueTypeName=Task` in project `TC`, with `parent` set to its Epic key (A, B, or C above) and:
```json
additional_fields = {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- `priority`: **propagated**. The Feature priority is "Critical" (not "Undefined").
- `fixVersions`: **propagated**. The Feature has "RHTPA 1.5.0" and `fixVersion scope: both` includes tasks.
- "Prompt for priority" and "Prompt for fixVersion" are `true` in Jira Field Defaults. In an interactive run, the user would confirm the inherited Critical / RHTPA 1.5.0 values before creation. This non-interactive run uses the inherited values.

Feature label update (after all tasks are created):
```
jira.edit_issue("TC-9003", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

Description digest comments: one per task, posted right after creation. See `task-N-digest.md`. The digests were computed with `scripts/sha256-digest.py` over the local markdown description. A live run would compute them over the description re-fetched from Jira after normalization, so the values would differ.

### 6b — Links
- Incorporates: TC-9003 → Epic A, TC-9003 → Epic B, TC-9003 → Epic C (Epics available, so Feature-to-Task Incorporates links are not created)
- Depend links (`inward` = dependent, `outward` = dependency):
  - T2 → T1; T3 → T1, T2; T4 → T1, T3; T5 → T1, T4; T6 → T1, T4, T5; T7 → T1, T5, T6; T8 → T1, T4, T5; T9 → T3, T5, T6, T7, T8; T10 → T2, T3, T4, T5, T6, T7, T8, T9

### 6c — Summary comment
See `summary-comment.md`.
