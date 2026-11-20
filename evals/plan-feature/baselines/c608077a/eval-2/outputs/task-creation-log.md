# Task Creation Log — TC-9002 (simulated; no Jira calls made)

Jira keys below are placeholders (`<EPIC-n>`, `<TASK-n>`), because no issues were created in this eval.

## 6a.0 — Epics (issue type: Epic, level 1 — assumed; see impact-map.md)

| Placeholder | Summary | Parent | additional_fields |
|---|---|---|---|
| `<EPIC-1>` | TC-9002: Search performance | TC-9002 | `{"labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}]}` |
| `<EPIC-2>` | TC-9002: Search relevance | TC-9002 | same as above |
| `<EPIC-3>` | TC-9002: Search filtering | TC-9002 | same as above |

Epic descriptions (plain text):
- EPIC-1: "Measure and improve GET /api/v2/search latency: baseline instrumentation (Task 1) and index, pagination, and caching optimizations (Task 2)."
- EPIC-2: "Rank search results by relevance using a deterministic model pending PO confirmation (Task 3)."
- EPIC-3: "Add type/severity/license filters to GET /api/v2/search, filter set pending PO confirmation (Task 4)."

## 6a — Tasks (issue type: Task, level 0)

All tasks use `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

| # | Placeholder | Summary | Parent (Epic) | Description file | Digest comment |
|---|---|---|---|---|---|
| 1 | `<TASK-1>` | Add search performance baseline instrumentation | `<EPIC-1>` | task-1-search-performance-baseline.md | task-1-digest.md |
| 2 | `<TASK-2>` | Optimize search query performance (indexes, pagination, caching) | `<EPIC-1>` | task-2-search-query-performance.md | task-2-digest.md |
| 3 | `<TASK-3>` | Improve search result relevance ranking | `<EPIC-2>` | task-3-search-relevance-ranking.md | task-3-digest.md |
| 4 | `<TASK-4>` | Add type, severity, and license filters to search | `<EPIC-3>` | task-4-search-filters.md | task-4-digest.md |

Digest note: the protocol requires hashing the description as re-fetched from Jira. That was not possible here, so each digest in `task-N-digest.md` is computed with `scripts/sha256-digest.py` over the local markdown description. In a live run, recompute it from the description returned by `jira.get_issue` after creation. Digest comments are standalone and carry no footnote.

No bookend tasks (direct-to-main mode). No documentation task (no Documentation Considerations section). No testing tasks (no `docs/testing-readiness.md`).

## 6b — Links

Incorporates (Feature → Epic):
- TC-9002 incorporates `<EPIC-1>`
- TC-9002 incorporates `<EPIC-2>`
- TC-9002 incorporates `<EPIC-3>`

Depend (dependent → dependency):
- `<TASK-2>` depends on `<TASK-1>`
- `<TASK-3>` depends on `<TASK-2>`
- `<TASK-4>` depends on `<TASK-2>`
- `<TASK-4>` depends on `<TASK-3>`

## Feature label changes

None. `workflow:feature-branch` is not applied (direct-to-main).
