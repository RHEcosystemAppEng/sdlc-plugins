# Task Creation Log — TC-9005 (simulated; no Jira calls made)

## Type-to-role mapping (Step 2.5)
- Feature: Feature (ID 10142, level 2), from CLAUDE.md
- Epic: not discovered. Jira was unavailable in this eval, so the plan uses graceful degradation (Feature → Task) and skips sub-step 6a.0
- Task: Task (level 0)

## 6a — Issues created

All issues use `projectKey=TC`, `issueTypeName=Task`, no `parent`, and:

```json
additional_fields = {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

| # | Summary | Target Branch | Placeholder key | Digest comment |
|---|---|---|---|---|
| 1 | Create feature branch TC-9005 from main | main | TC-9005-T1 | task-1-digest.md |
| 2 | Add migration converting advisory_status lookup table to advisory_status_enum column | TC-9005 | TC-9005-T2 | task-2-digest.md |
| 3 | Update SeaORM advisory entity and advisory queries to use the status enum column | TC-9005 | TC-9005-T3 | task-3-digest.md |
| 4 | Update advisory ingestion pipeline to write status enum values directly | TC-9005 | TC-9005-T4 | task-4-digest.md |
| 5 | Update internal architecture docs for advisory status enum schema change | TC-9005 | TC-9005-T5 | task-5-digest.md |
| 6 | Merge feature branch TC-9005 to main | main | TC-9005-T6 | task-6-digest.md |

Digest note: in a live run each digest is computed with `scripts/sha256-digest.py` on the description re-fetched from Jira. Here it was computed on the local task markdown file, so the format tag is `sha256-md`. Each digest is a standalone comment with no footnote.

## Feature label update
```
jira.edit_issue("TC-9005", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

## 6b — Issue links

**Incorporates** (Feature → Task, because there are no Epics):
- TC-9005 → T1, T2, T3, T4, T5, T6

**Depend** (inward = dependent, outward = dependency):
- T2 → T1
- T3 → T1, T2
- T4 → T1, T2, T3
- T5 → T1, T2, T3, T4
- T6 → T2, T3, T4, T5

## Comments posted on TC-9005
1. Impact map + workflow mode decision → `impact-map.md`
2. Plan summary → `summary-comment.md`
