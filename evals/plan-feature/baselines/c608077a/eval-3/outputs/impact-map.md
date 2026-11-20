# TC-9003 — SBOM comparison view: Planning Record and Repository Impact Map

## Step 0 – Project Configuration validation

CLAUDE.md `# Project Configuration` contains all three required sections:

- **Repository Registry:** present.
- **Jira Configuration:** project key `TC`, Cloud ID `2b9e35e3-…`, Feature issue type ID `10142`.
- **Code Intelligence:** present; no Serena instances are configured.

Validation passed.

**Eval assumption:** the Registry lists only `sdlc-plugins`. This eval supplies two target repositories through fixtures: `trustify-backend` (repo-backend.md) and `trustify-ui` (repo-frontend.md). Both are treated as registered repositories with no Serena instance. Repository analysis used the fixture directory trees and "Key Conventions" sections in place of Glob/Grep/Read on a live checkout. Each repo's `CONVENTIONS.md` exists according to its tree, but its content is not available, so the "Key Conventions" bullet list of each fixture is treated as that repo's CONVENTIONS.md sections.

## Step 1 – Feature data extracted (TC-9003)

| Field | Value |
|---|---|
| Title | SBOM comparison view |
| Priority | Critical (set, not "Undefined") → propagated |
| fixVersions | `RHTPA 1.5.0` (non-empty) → propagated (CLAUDE.md `fixVersion scope: both`) |
| Figma | https://www.figma.com/design/mock123/SBOMCompare (context taken from figma-context.md) |
| Linked issues | None (so there are no existing bookend tasks; the idempotency guard passes) |
| Documentation signals | Doc Impact = **New Content**. Document the comparison endpoint (for API consumers) and the comparison UI (a workflow guide). Reference material: SBOM detail page docs and package/advisory data model docs. |

**Step 1.5 (parent link):** skipped. The feature has no `parent`, and this non-interactive eval assumes the user pressed Enter to skip.

## Step 2 – Figma analysis summary

- **UI structure:**
  - Header toolbar: left and right SBOM `Select`s, a "Compare" button, and an "Export" dropdown.
  - Six `ExpandableSection` diff sections, each with a colored count badge and a composable `Table`.
  - An `EmptyState` before the first comparison, and `Skeleton` placeholders while loading.
- **Backend interactions:**
  - `GET /api/v2/sbom` already exists and is used through the `useSboms` hook.
  - `GET /api/v2/sbom/compare?left&right` is new.
- **Custom sub-components:**
  - Colored count badges (green, red, blue, red, green, yellow). PF5 `Badge` has no color variants, so these map to PF5 `Label` color props or PF tokens.
  - Critical-row highlight in New Vulnerabilities.
  - Details are recorded in Task 6.
- **Data component rendering scope:** each section's table is **per-context**. It renders only its own response array, and its badge counts only that array (Task 6).
- **Display text vs API mismatches:**
  - `severity`: the API returns lowercase `critical`/`high`/…, while `SeverityBadge` and Figma show "Critical". A frontend mapping is needed.
  - `direction`: the API returns `upgrade`/`downgrade`, which the UI shows as "Upgrade"/"Downgrade". A frontend mapping is needed.
  - Null licenses need a placeholder.
  - All three are recorded in Task 6.

## Step 2.5 – Issue type discovery (assumed; Jira not contacted)

```
Type-to-role mapping (assumed for the TC project):
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (ID: <discovered at runtime>, level: 1)
  Task:    Task    (ID: <discovered at runtime>, level: 0)
```

**Assumption:** the TC project has a level-1 "Epic" type. The presence of a `## Hierarchy Configuration` section in CLAUDE.md implies that `/setup` detected one. Grouping strategy from CLAUDE.md: **by-sub-feature**. The suggested groupings below are treated as user-approved, because this eval cannot prompt.

## Step 3 – Repository analysis highlights

**trustify-backend (Rust, Axum, SeaORM):**
- **SBOM module:** `modules/fundamental/src/sbom/` follows the `model/` + `service/` + `endpoints/` structure. `endpoints/mod.rs` registers `/api/v2/sbom`; `get.rs` serves `/{id}`.
- **Data sources for the diff (no new tables):**
  - `entity/src/sbom_package.rs` and `entity/src/package.rs`
  - `entity/src/package_license.rs`
  - `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs`
  - `AdvisorySummary.severity` (`advisory/model/summary.rs`)
  - `PackageSummary.license` (`package/model/summary.rs`)
- **Shared helpers:**
  - `common/src/db/query.rs` (query builders)
  - `common/src/error.rs::AppError`
  - `common/src/model/paginated.rs` (not used for the diff, which is a single object)
- **Tests:** `tests/api/sbom.rs`, which runs integration tests against PostgreSQL.
- **Docs:** `README.md`, `CONVENTIONS.md`.

**Shared-artifact producer/consumer analysis.** The diff only reads the SBOM↔package, package↔license, and SBOM↔advisory link data.

- **Producers:**
  - `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion: parse, store, link packages)
  - `modules/ingestor/src/graph/advisory/mod.rs` (advisory correlation)
- **Existing consumers:**
  - `sbom/service/sbom.rs`
  - `package/service/mod.rs`
  - `advisory/service/advisory.rs`
  - `search/service/mod.rs`

No acceptance criterion requires changing a producer. The feature adds a read-only consumer, so no producer path is excluded and there is no coverage gap. Correlation timing does matter: an advisory correlated after ingestion appears in new or resolved vulnerabilities at request time, which is the expected live-diff behaviour.

**trustify-ui (React 18, PF5, React Query, React Router v6):**
- **API layer:**
  - `src/api/client.ts` (Axios)
  - `src/api/models.ts`
  - `src/api/rest.ts`
  - Hooks in `src/hooks/` (`useSboms`, `useSbomById`)
- **Pages:**
  - `src/pages/SbomListPage/` (entry point for "Compare selected")
  - `src/pages/SbomDetailPage/components/{PackageTable,AdvisoryList}.tsx` (patterns to reuse)
- **Shared components and utilities:**
  - `src/components/SeverityBadge.tsx`
  - `src/components/FilterToolbar.tsx`
  - `src/components/EmptyStateCard.tsx`
  - `src/utils/severityUtils.ts`
  - `src/utils/formatDate.ts`
- **Routing:** `src/routes.tsx`.
- **Tests:**
  - `tests/mocks/handlers.ts` and `tests/mocks/fixtures/`
  - `tests/e2e/sbom-list.spec.ts`
- **Docs:** `README.md`, `CONVENTIONS.md`.
- **Convention conflict found:** CONVENTIONS.md asks for kebab-case directories, but existing page directories are PascalCase. The tasks follow the existing sibling pattern and flag the conflict.
- **No virtualization library** appears in the repo, so one must be added (Task 6).

**Testing readiness template:** neither repo tree contains `docs/testing-readiness.md`, so no testing tasks are generated.

**Eval infrastructure:** no task modifies a skill `SKILL.md`, so eval coverage propagation does not apply.

## Step 4 – Repository Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison response model (six diff categories) under modules/fundamental/src/sbom/model/
    - Add on-the-fly diff computation (packages, versions, licenses, advisories) to SbomService — no new tables/migrations
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint with 400/404 handling, registered in sbom endpoints/mod.rs
    - Add integration tests for the compare endpoint in tests/api/sbom.rs (incl. p95 < 1s for 2000-package SBOMs)
    - Document the compare endpoint in README.md API reference

trustify-ui:
  changes:
    - Add SbomComparison TypeScript types, fetchSbomComparison() REST function, useSbomComparison hook, MSW mock + fixture
    - Add lazy-loaded /sbom/compare page with left/right SBOM selectors, Compare button, URL-encoded (shareable) state, empty/loading/error states
    - Add six collapsible diff sections with colored count badges, sortable tables, SeverityBadge, critical-vulnerability row highlight, virtualization >100 rows
    - Add row selection + "Compare selected" action on SBOM list page navigating to /sbom/compare; E2E test for the full flow
    - Add Export JSON/CSV dropdown (non-MVP, client-side)
    - Add user/API documentation for the comparison feature (New Content)
```

### Excluded requirements

| Requirement | Source in TC-9003 | Why it cannot be planned / missing input |
|---|---|---|
| Add the comparison endpoint to the API latency Grafana dashboard | Customer Information/Supportability | No observability or dashboard repository is in the Repository Registry, and the dashboard definition location is unknown. **Missing input:** the repository or path holding the Grafana dashboard JSON. (Task 3 keeps the route compatible with existing per-route metrics.) |
| Monitor for timeouts on large comparisons (>2000 packages per SBOM) | Customer Information/Supportability | Alerting configuration lives outside the registered repos. **Missing input:** the alerting/monitoring repository and the timeout threshold. |
| Enforce "both SBOMs must be from the same product/project" | Customer Considerations | Neither the fixture `SbomSummary`/`SbomDetails` nor the `sbom` entity exposes a product/project relationship, so there is no field to validate against. The expected behaviour is also unspecified (block, or warn). **Missing input:** the product linkage field and the desired UX. Until resolved, comparisons are not blocked. |
| Pagination or filtering for very large diffs (>1000 package changes) | Customer Considerations | Phrased as "may require". The Figma design specifies no pagination, with virtualization above 100 rows, which Task 6 implements. Server-side pagination of the diff is **not planned**. **Missing input:** a decision on whether virtualization is sufficient, or a design for paginated or filtered diff sections. |

Non-MVP "Export diff as JSON or CSV" **is** planned (Task 8), because the Figma design specifies it and it is client-side only.

## Step 4.5 – Workflow mode decision

**Selected mode: `feature-branch`.**

Atomicity indicators:
1. Coordinated schema migrations: **not present** (no new tables).
2. Breaking API changes: **not present** (the endpoint is additive).
3. Cross-cutting refactors: **not present**.
4. Tightly coupled feature components: **present.** The new `/sbom/compare` page (Tasks 4–7) requires `GET /api/v2/sbom/compare` (Tasks 2–3), which does not yet exist. Merging the UI alone would ship a page whose core call returns 404. The backend endpoint alone has no user-facing entry point.

Interdependent tasks:
- Task 4 consumes the Task 3 contract.
- Tasks 5, 6, and 8 consume the Task 4 hook.
- Task 7 navigates to the Task 5 page.

The `workflow:feature-branch` label will be applied to TC-9003 in Step 6a.

**Cross-repository note.** The bookends (Task 1 and Task 10) are in `trustify-ui`, which holds 7 of the 9 non-bookend tasks counting documentation. The two `trustify-backend` tasks also target a `TC-9003` branch. Task 3's Implementation Notes tell the implementer to create that branch from `main` if it is missing. Task 10 requires the backend `TC-9003` → `main` PR to be merged first, or together with the UI merge.

## Step 5 – Epics (by-sub-feature) and task assignment

| Epic summary | Description (plain text) | Tasks |
|---|---|---|
| TC-9003: SBOM diff API | Backend diffing model, service, and GET /api/v2/sbom/compare endpoint with integration tests in trustify-backend. | Task 2, Task 3 |
| TC-9003: Comparison UI | Frontend data layer, /sbom/compare page, diff sections, SBOM list entry point, export, and feature-branch bookends in trustify-ui. | Task 1, Task 4, Task 5, Task 6, Task 7, Task 8, Task 10 |
| TC-9003: Documentation | API reference and user guide for the SBOM comparison feature. | Task 9 |

## Task list

| # | File | Summary | Repo | Target Branch | Depends on |
|---|---|---|---|---|---|
| 1 | task-1-create-feature-branch.md | Create feature branch TC-9003 from main | trustify-ui | main | — |
| 2 | task-2-backend-sbom-diff-model-service.md | Add SBOM comparison response model and on-the-fly diff computation in SbomService | trustify-backend | TC-9003 | 1 |
| 3 | task-3-backend-compare-endpoint.md | Add GET /api/v2/sbom/compare endpoint with integration tests | trustify-backend | TC-9003 | 1, 2 |
| 4 | task-4-ui-compare-api-client-hook.md | Add SbomComparison types, fetchSbomComparison() and useSbomComparison hook with MSW mocks | trustify-ui | TC-9003 | 1, 3 |
| 5 | task-5-ui-compare-page-toolbar-routing.md | Add /sbom/compare page with SBOM selectors, Compare button, URL-shareable state, empty and loading states | trustify-ui | TC-9003 | 1, 4 |
| 6 | task-6-ui-diff-sections.md | Add six collapsible diff sections (tables, count badges, critical highlight, virtualized rows) | trustify-ui | TC-9003 | 1, 4, 5 |
| 7 | task-7-ui-sbom-list-compare-selection.md | Add row checkboxes and "Compare selected" action on SBOM list page | trustify-ui | TC-9003 | 1, 5, 6 |
| 8 | task-8-ui-export-diff.md | Add Export dropdown (JSON, CSV) to the SBOM comparison toolbar (non-MVP) | trustify-ui | TC-9003 | 1, 5 |
| 9 | task-9-documentation.md | Document SBOM comparison API endpoint and comparison UI workflow | trustify-ui | TC-9003 | 3, 6, 7, 8 |
| 10 | task-10-merge-feature-branch.md | Merge feature branch TC-9003 to main | trustify-ui | main | 2–9 |

## Step 6 – Issue creation log (simulated; no Jira calls made)

### additional_fields applied to every created issue (Epics and Tasks)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- `priority` is included because the Feature priority is "Critical", which is set and not "Undefined".
- `fixVersions` is included because the Feature has `RHTPA 1.5.0` and `fixVersion scope` is `both`.

### 6a.0 Epics

| Epic | issueTypeName | parent | Placeholder key |
|---|---|---|---|
| TC-9003: SBOM diff API | Epic | TC-9003 | EPIC-A |
| TC-9003: Comparison UI | Epic | TC-9003 | EPIC-B |
| TC-9003: Documentation | Epic | TC-9003 | EPIC-C |

### 6a Tasks

Each task is created with `issueTypeName=Task`, `parent=<Epic key>`, and the `additional_fields` above. A description digest comment is posted immediately after each task is created (see the `task-N-digest.md` files).

| Task | parent | Placeholder key |
|---|---|---|
| 1 | EPIC-B | TASK-1 |
| 2 | EPIC-A | TASK-2 |
| 3 | EPIC-A | TASK-3 |
| 4 | EPIC-B | TASK-4 |
| 5 | EPIC-B | TASK-5 |
| 6 | EPIC-B | TASK-6 |
| 7 | EPIC-B | TASK-7 |
| 8 | EPIC-B | TASK-8 |
| 9 | EPIC-C | TASK-9 |
| 10 | EPIC-B | TASK-10 |

**Feature label update:** `jira.edit_issue(TC-9003, labels=["ai-generated-jira", "workflow:feature-branch"])`. The existing label is preserved and the new one appended.

### 6b Links

- **Incorporates** (Feature → Epics): TC-9003 → EPIC-A, TC-9003 → EPIC-B, TC-9003 → EPIC-C
- **Depend** (dependent → dependency):

| Dependent | Depends on |
|---|---|
| TASK-2 | TASK-1 |
| TASK-3 | TASK-1, TASK-2 |
| TASK-4 | TASK-1, TASK-3 |
| TASK-5 | TASK-1, TASK-4 |
| TASK-6 | TASK-1, TASK-4, TASK-5 |
| TASK-7 | TASK-1, TASK-5, TASK-6 |
| TASK-8 | TASK-1, TASK-5 |
| TASK-9 | TASK-3, TASK-6, TASK-7, TASK-8 |
| TASK-10 | TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7, TASK-8, TASK-9 |

### Comments posted to TC-9003

1. `impact-map-comment.md`: the impact map, posted after approval (approval assumed).
2. `workflow-mode-comment.md`: the workflow mode decision.
3. `summary-comment.md`: the final plan summary.
