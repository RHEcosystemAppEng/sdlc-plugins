# Task Creation Log — TC-9005 (simulated; no Jira calls made)

Project: TC (Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432)
Hierarchy: Feature → Task. No level-1 Epic type was discovered, so step 6a.0 is skipped and no `parent` field is set.

## 6a — Issues created

Placeholder keys (TC-NEW-N) stand in for the keys Jira would assign.

| # | Placeholder key | Issue type | Summary | Description file | Digest file |
|---|---|---|---|---|---|
| 1 | TC-NEW-1 | Task | Create feature branch TC-9005 from main | task-1-create-feature-branch.md | task-1-digest.md |
| 2 | TC-NEW-2 | Task | Add reversible migration converting advisory_status lookup table to advisory_status_enum column | task-2-advisory-status-enum-migration.md | task-2-digest.md |
| 3 | TC-NEW-3 | Task | Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity | task-3-update-advisory-seaorm-entity.md | task-3-digest.md |
| 4 | TC-NEW-4 | Task | Replace advisory_status joins with the advisory.status enum column in all advisory queries | task-4-advisory-queries-use-status-column.md | task-4-digest.md |
| 5 | TC-NEW-5 | Task | Update advisory ingestion pipeline to write AdvisoryStatus enum values directly | task-5-ingestion-write-enum-status.md | task-5-digest.md |
| 6 | TC-NEW-6 | Task | Update internal architecture docs for advisory status enum column | task-6-update-architecture-docs.md | task-6-digest.md |
| 7 | TC-NEW-7 | Task | Merge feature branch TC-9005 to main | task-7-merge-feature-branch.md | task-7-digest.md |

`additional_fields` applied to every task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- Priority: inherited from the Feature (High), so it is propagated.
- fixVersions: inherited from the Feature (RHTPA 2.0.0). It is propagated because `fixVersion scope` is `both`.

Description digests: each digest was computed with `scripts/sha256-digest.py` over the task description body (the `**Summary:**` line is excluded because it is the issue summary, not the description). In a live run, the digest is computed on the description re-fetched from Jira after creation. Each digest comment is posted on its task right after creation, before any links are created.

## Feature label update

```
jira.edit_issue("TC-9005", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

## 6b — Issue links

"Incorporates" links (Feature → Task; no Epics):

| Inward (Feature) | Outward (Task) |
|---|---|
| TC-9005 | TC-NEW-1 |
| TC-9005 | TC-NEW-2 |
| TC-9005 | TC-NEW-3 |
| TC-9005 | TC-NEW-4 |
| TC-9005 | TC-NEW-5 |
| TC-9005 | TC-NEW-6 |
| TC-9005 | TC-NEW-7 |

"Depend" links (inward = dependent, outward = dependency):

| Dependent | Depends on |
|---|---|
| TC-NEW-2 | TC-NEW-1 |
| TC-NEW-3 | TC-NEW-1 |
| TC-NEW-3 | TC-NEW-2 |
| TC-NEW-4 | TC-NEW-1 |
| TC-NEW-4 | TC-NEW-3 |
| TC-NEW-5 | TC-NEW-1 |
| TC-NEW-5 | TC-NEW-3 |
| TC-NEW-6 | TC-NEW-2 |
| TC-NEW-6 | TC-NEW-3 |
| TC-NEW-6 | TC-NEW-4 |
| TC-NEW-6 | TC-NEW-5 |
| TC-NEW-7 | TC-NEW-2 |
| TC-NEW-7 | TC-NEW-3 |
| TC-NEW-7 | TC-NEW-4 |
| TC-NEW-7 | TC-NEW-5 |
| TC-NEW-7 | TC-NEW-6 |

## Comments posted on TC-9005

1. `impact-map.md` — Repository Impact Map, including the workflow mode decision (Step 4)
2. `workflow-mode-comment.md` — workflow mode decision (Step 4.5)
3. `summary-comment.md` — plan summary (Step 6c)
