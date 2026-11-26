# Repository Impact Map — TC-9003: SBOM comparison view

> Would be posted as a Jira comment on TC-9003 (Step 4), then the Workflow Mode decision (Step 4.5) is appended.

## Planning context (non-interactive run — defaults recorded)

| Step | Prompt / decision | Default chosen |
|---|---|---|
| 0 | Project Configuration validation | PASS — Repository Registry, Jira Configuration (Project key TC, Cloud ID, Feature type 10142) and Code Intelligence sections present |
| 1 | Feature fetch | Read from `feature-multi-repo.md` (mock of `jira.get_issue(TC-9003)`). Priority = **Critical**, fixVersions = **[RHTPA 1.5.0]** |
| 1 | Documentation signals | Present — Doc Impact = **New Content** (endpoint reference + comparison UI guide) |
| 1.5 | Link Feature to parent issue? | **Skipped** (no parent field in fixture; default = press Enter / skip) |
| 2 | Figma | URL found in feature description (`https://www.figma.com/design/mock123/SBOMCompare`); design context read from `figma-context.md` |
| 2.5 | Issue type discovery | Jira unavailable in eval. CLAUDE.md `## Hierarchy Configuration` exists, so assumed the TC project exposes a level-1 type named **Epic**. Mapping: Feature (ID 10142, level 2), Epic (level 1, ID resolved at creation time), Task (level 0) |
| 2.5 / 5 | Epic grouping strategy | **by-sub-feature** (from CLAUDE.md `Default epic grouping strategy`); suggested groupings auto-approved |
| 3 | Code intelligence | No Serena instances configured; repository structure taken from `repo-backend.md` and `repo-frontend.md` fixtures (Glob/Read fallback) |
| 3 | CONVENTIONS.md | Present at the root of both repos. Fixture only exposes the "Key Conventions" summary, so those bullets are used as the CONVENTIONS.md sections |
| 3 | Testing readiness template (`docs/testing-readiness.md`) | **Not found** in either repo → no testing tasks generated |
| 3 | Eval infrastructure | Not applicable — no task modifies a `SKILL.md` |
| 3 | Shared-artifact producer/consumer analysis | Not applicable — no acceptance criterion depends on a shared artifact; the diff is computed on the fly, read-only |
| 4 | Approve impact map | **Approved** (default) |
| 4.5 | Workflow mode | **feature-branch** (see below) |
| 5 | Bookend idempotency guard | Feature has no linked issues ("Linked Issues: None") → no existing bookends; bookends generated |
| 6 | Priority / fixVersion prompts (`Prompt for priority: true`, `Prompt for fixVersion: true`) | Accepted inherited values: priority **Critical**, fixVersions **RHTPA 1.5.0** (`fixVersion scope: both` → propagated to Epics and Tasks) |

## Impact map

```
trustify-backend:
  changes:
    - Add an SBOM comparison response model (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add a comparison method to SbomService that computes the diff on the fly from existing sbom_package, package_license and sbom_advisory data (no new tables, no migration)
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint registered in the SBOM module routes
    - Return 404 for unknown SBOM ids and 400 for missing/identical parameters instead of an empty diff
    - Add integration tests for the comparison endpoint
    - Document the comparison endpoint in the backend API reference / README

trustify-ui:
  changes:
    - Add TypeScript types, REST client function and React Query hook for the comparison endpoint (+ MSW handler and fixture)
    - Add the /sbom/compare comparison page: SBOM selectors, Compare button, six collapsible diff sections with count badges, empty and loading states
    - Encode left/right SBOM IDs in the URL query string so comparisons are shareable/bookmarkable
    - Highlight New Vulnerabilities rows with critical severity
    - Virtualize diff tables with >100 rows
    - Add multi-select checkboxes and a "Compare selected" action to the SBOM list page
    - Add client-side "Export JSON" / "Export CSV" of the loaded diff (non-MVP)
    - Document the comparison workflow (user guide) and endpoint (cross-reference)
```

### Discovered backend API contracts (from Step 3)

- `GET /api/v2/sbom` — existing; returns `PaginatedResults<SbomSummary>` (`{ items: SbomSummary[], total: number }`) — `modules/fundamental/src/sbom/endpoints/list.rs`, `modules/fundamental/src/sbom/model/summary.rs`, `common/src/model/paginated.rs`
- `GET /api/v2/sbom/{id}` — existing; returns `SbomDetails` — `modules/fundamental/src/sbom/endpoints/get.rs`, `modules/fundamental/src/sbom/model/details.rs`
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — **NEW** (Task 3). Response shape (from Figma backend interactions):
  ```json
  {
    "added_packages":   [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes":  [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities":      [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes":  [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```

### Excluded requirements

| Requirement | Reason / missing input |
|---|---|
| Add comparison endpoint to the API latency Grafana dashboard (Customer Information/Supportability) | No dashboard/observability repository is in the Repository Registry or the provided repo structures — cannot plan a concrete change. Provide the dashboards repo to plan it. |
| Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM) — alerting | Same: no monitoring/alerting configuration repository available. (Server-side latency is covered by the p95 NFR and tests in Task 3; alert rules are not.) |
| Server-side pagination/filtering of very large diffs (>1000 package changes) (Customer Considerations) | Stated as "may require" — insufficient specification (no API contract or UX for paging a diff). The MVP handles large diffs via frontend virtualization (Task 5). Needs a product decision before planning. |
| Enforce "both SBOMs from the same product/project" | Listed as a customer consideration, not a requirement; no product/project relation is visible in `SbomSummary`/`SbomDetails`. Not enforced by the plan — open question for product owner. |

## Workflow mode decision (Step 4.5)

**Selected mode: `feature-branch`**

Atomicity indicators found:

- **Indicator 4 — Tightly coupled feature components**: the new `/sbom/compare` UI page (Tasks 4–7, trustify-ui) consumes `GET /api/v2/sbom/compare`, which does not yet exist (Tasks 2–3, trustify-backend). Merging the frontend tasks to `main` without the backend endpoint would ship a page whose only data call 404s; the SBOM-list "Compare selected" action (Task 6) navigates to that page.
- Indicators 1–3 not present (no schema migration — diff computed on the fly; no existing API contract is changed; no cross-cutting refactor).

Interdependent tasks: Task 2 → Task 3 (service consumed by endpoint) → Task 4 (client types/hook bound to endpoint contract) → Task 5 (page) → Tasks 6, 7 (entry point and export on the page).

The `workflow:feature-branch` label will be applied to TC-9003 in Step 6a (existing label `ai-generated-jira` preserved).

Bookend tasks are placed in **trustify-ui** (majority of implementation tasks: 4 of 6). Note for implementers: backend tasks (2, 3) also target branch `TC-9003`; implement-task must create/push `TC-9003` in trustify-backend from `main` if it does not exist there, and the backend `TC-9003` branch must be merged to `main` before (or together with) the trustify-ui merge PR (Task 9).

## Epic grouping (by-sub-feature) and Jira field values

| Epic | Summary | Tasks |
|---|---|---|
| Epic A | `TC-9003: SBOM diff API` | Task 2, Task 3 |
| Epic B | `TC-9003: Comparison UI and navigation` | Task 4, Task 5, Task 6 |
| Epic C | `TC-9003: Compliance export and documentation` | Task 7, Task 8 |
| Epic D | `TC-9003: Feature branch lifecycle` | Task 1, Task 9 |

`additional_fields` for every Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

Plus `parent` = the task's Epic key (see `task-creation-log.md`). Feature TC-9003 gets label `workflow:feature-branch` appended.

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
