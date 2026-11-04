# Task Creation Log — TC-9003

Simulated Steps 0–6c. No external services were called. Every Jira mutation the skill would perform is recorded below.

## Step 0 — Project Configuration
- Repository Registry, Jira Configuration (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142) and Code Intelligence are all present, so validation passed.
- Note: the target repos `trustify-backend` and `trustify-ui` are not in the Registry. They were analyzed from the supplied manifests. No Serena instances are configured, so the Glob/Grep/Read fallback was used.

## Step 1 — Feature fetch (from `feature-multi-repo.md`)
- Summary: SBOM comparison view
- Priority: **Critical**. It is set and not "Undefined", so it propagates.
- fixVersions: **[RHTPA 1.5.0]**. The array is not empty.
- Existing labels: `ai-generated-jira`
- Figma link found in the description: https://www.figma.com/design/mock123/SBOMCompare
- Documentation signals: **New Content** (endpoint reference and UI guide; reference material: SBOM detail docs, package/advisory data model docs)

## Step 1.5 — Parent link
- The Feature has no `parent` field. The interactive prompt "Link this Feature to a parent issue?" got no input (non-interactive eval), so the step was skipped and no `edit_issue` call was made.

## Step 2 — Figma
- Taken from `figma-context.md`: the header toolbar, six diff sections, empty and loading states, the component mapping, and the backend response shape. Custom sub-components (colored count badges, critical-row highlight), per-context data scope, and display-vs-API mismatches (`severity` case, `direction` labels) are captured in Tasks 5 and 6.

## Step 2.5 — Issue types
- `jira.get_project_issue_types(2b9e35e3-6bd3-4cec-b838-f4249ee02432, TC)` could not be called (no external services).
- Known types: Feature (ID 10142, from Jira Configuration), Task (level 0), Bug (ID 10016, not used).
- **Epic (level-1) availability is unknown.** CLAUDE.md `## Hierarchy Configuration` sets `Default epic grouping strategy: by-sub-feature`.
  - **If a level-1 "Epic" type is discovered**, create these Epics. The by-sub-feature grouping would be presented to the user for approval first.
    | Epic summary | Tasks |
    |---|---|
    | TC-9003: SBOM comparison diff API | 2, 3 |
    | TC-9003: SBOM comparison UI | 4, 5, 6, 7, 8 |
    | TC-9003: Delivery and documentation | 1, 9, 10 |
    Each Epic gets `parent: TC-9003` and `additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}`. Feature-to-Epic "Incorporates" links replace the Feature-to-Task links, and each task's `parent` is set to its Epic.
  - **If no level-1 type exists** (graceful degradation), the skill logs "No Epic-level type found in project — tasks will be created directly under the Feature." It creates no Epics and adds Feature-to-Task "Incorporates" links (listed below).

## Step 3 — Analysis summary
- CONVENTIONS.md exists in both repos, and its conventions (from the manifests' Key Conventions) were applied with `Applies:` rationales.
- `docs/testing-readiness.md` was not found in either repo, so no testing tasks were generated.
- Shared-artifact analysis: not applicable (read-only diff).
- No `SKILL.md` targets, so eval coverage propagation does not apply.

## Step 4 / 4.5 — Comments on TC-9003
- `jira.add_comment(TC-9003, impact-map.md)`
- `jira.add_comment(TC-9003, workflow-mode-comment.md)`. Mode: **feature-branch**.

## Step 5 — Bookend idempotency guard
- TC-9003 has no existing "Incorporates" links ("Linked Issues: None"), so no existing bookend tasks were found and bookends are generated.

## Step 6a — Task creation

`additional_fields` applied to **every** task:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- priority: inherited from the Feature ("Critical").
- fixVersions: inherited ("RHTPA 1.5.0"), because `fixVersion scope: both` includes tasks.

| # | Placeholder key | Issue type | Summary | Repository | Target Branch | File | Digest |
|---|---|---|---|---|---|---|---|
| 1 | TC-9003-T1 | Task | Create feature branch TC-9003 from main | trustify-ui | main | task-1-create-feature-branch.md | task-1-digest.md |
| 2 | TC-9003-T2 | Task | Backend: SBOM comparison model and diff service | trustify-backend | TC-9003 | task-2-backend-diff-model-service.md | task-2-digest.md |
| 3 | TC-9003-T3 | Task | Backend: GET /api/v2/sbom/compare endpoint and integration tests | trustify-backend | TC-9003 | task-3-backend-compare-endpoint.md | task-3-digest.md |
| 4 | TC-9003-T4 | Task | Frontend: comparison API types, client function, React Query hook and mocks | trustify-ui | TC-9003 | task-4-frontend-api-client-hook.md | task-4-digest.md |
| 5 | TC-9003-T5 | Task | Frontend: comparison diff section components | trustify-ui | TC-9003 | task-5-frontend-diff-sections.md | task-5-digest.md |
| 6 | TC-9003-T6 | Task | Frontend: SBOM comparison page and /sbom/compare route | trustify-ui | TC-9003 | task-6-frontend-compare-page.md | task-6-digest.md |
| 7 | TC-9003-T7 | Task | Frontend: multi-select and "Compare selected" on SBOM list page | trustify-ui | TC-9003 | task-7-frontend-list-compare-selected.md | task-7-digest.md |
| 8 | TC-9003-T8 | Task | Frontend: export comparison as JSON / CSV (non-MVP) | trustify-ui | TC-9003 | task-8-frontend-export.md | task-8-digest.md |
| 9 | TC-9003-T9 | Task | Documentation: SBOM comparison endpoint and UI guide | trustify-backend | TC-9003 | task-9-documentation.md | task-9-digest.md |
| 10 | TC-9003-T10 | Task | Merge feature branch TC-9003 to main | trustify-ui | main | task-10-merge-feature-branch.md | task-10-digest.md |

Description digest: after each task is created, re-fetch it with `jira.get_issue`, run `python3 scripts/sha256-digest.py`, and post a standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` without the footnote. In this eval the digests were computed over the local task files (see `task-N-digest.md`).

Feature label update (after all tasks are created):
```
jira.edit_issue(TC-9003, fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

## Step 6b — Issue links

Feature "Incorporates" links (no-Epic path). On the Epic path, link to the three Epics instead.
- TC-9003 incorporates T1, T2, T3, T4, T5, T6, T7, T8, T9, T10

"Depend" links (inward = dependent, outward = dependency):
| Dependent | Depends on |
|---|---|
| T2 | T1 |
| T3 | T1, T2 |
| T4 | T1, T3 |
| T5 | T1, T4 |
| T6 | T1, T4, T5 |
| T7 | T1, T6 |
| T8 | T1, T6 |
| T9 | T2, T3, T4, T5, T6, T7, T8 |
| T10 | T2, T3, T4, T5, T6, T7, T8, T9 |

## Step 6c — Summary comment
- `jira.add_comment(TC-9003, summary-comment.md)`
