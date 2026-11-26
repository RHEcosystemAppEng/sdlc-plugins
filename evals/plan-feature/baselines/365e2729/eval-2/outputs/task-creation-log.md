# Task Creation Log — TC-9002 (simulated; no Jira calls made)

## Issue type mapping (Step 2.5)
Issue types could not be discovered in eval mode. CLAUDE.md lists Feature issue type ID 10142.
- If the project has a level-1 type (Epic): use the `by-sub-feature` strategy from Hierarchy Configuration.
  - Epic "TC-9002: Search performance": Task 1, Task 2
  - Epic "TC-9002: Search relevance and filtering": Task 3, Task 4
  - Each Epic: parent = TC-9002, with the same `additional_fields` as the tasks (below). The Feature gets an "Incorporates" link to each Epic.
- If no level-1 type exists, the plan falls back to Feature → Task. The Feature gets an "Incorporates" link to each Task.

## Tasks to create

All tasks use issue type Task, project TC, and these fields:

```json
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

| # | Summary | Description file | Epic (if available) | Digest comment |
|---|---|---|---|---|
| 1 | Add full-text search indexes (migration) | task-1-search-indexes-migration.md | Search performance | task-1-digest.md |
| 2 | Optimize search queries and add response caching | task-2-search-query-caching.md | Search performance | task-2-digest.md |
| 3 | Rank search results by relevance | task-3-search-relevance-ranking.md | Search relevance and filtering | task-3-digest.md |
| 4 | Add filters to the search endpoint | task-4-search-filters.md | Search relevance and filtering | task-4-digest.md |

Each digest was computed with `scripts/sha256-digest.py` over the task description markdown (the `sha256-md` path). In a live run it is computed over the description re-fetched from Jira.

## Links (Step 6b)
- Task 2 Depends on Task 1
- Task 3 Depends on Task 1
- Task 3 Depends on Task 2
- Task 4 Depends on Task 2
- Feature TC-9002 Incorporates each Epic (or each Task when no Epic type exists)

## Feature label
Workflow mode is `direct-to-main`, so the `workflow:feature-branch` label is **not** added.
