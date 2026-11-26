# Task Creation Log — TC-9005 (simulated; no Jira calls made)

Jira keys below are placeholders (`<EPIC-n>`, `<TASK-n>`) that would be replaced by the keys returned by `jira.create_issue`.

## Common `additional_fields` (Epics and Tasks)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

## 6a.0 — Epics (issue type: level-1 "Epic", parent: TC-9005)

| Placeholder | Summary | Description (plain text) |
|---|---|---|
| EPIC-A | TC-9005: Advisory status schema migration | Migration to advisory_status_enum and SeaORM entity update (Tasks 2, 3). |
| EPIC-B | TC-9005: Advisory query and ingestion updates | Advisory queries/endpoints/consumers and ingestion pipeline use the enum column (Tasks 4, 5). |
| EPIC-C | TC-9005: Feature branch delivery and documentation | Create/merge feature branch TC-9005 and update internal architecture docs (Tasks 1, 6, 7). |

## 6a — Tasks (issue type: level-0 "Task")

| # | Placeholder | Summary | parent | Description file | Digest comment |
|---|---|---|---|---|---|
| 1 | TASK-1 | Create feature branch TC-9005 from main | EPIC-C | task-1-create-feature-branch.md | task-1-digest.md |
| 2 | TASK-2 | Add advisory status enum migration (create type, backfill, drop FK column and lookup table) | EPIC-A | task-2-advisory-status-enum-migration.md | task-2-digest.md |
| 3 | TASK-3 | Update SeaORM advisory entity to use AdvisoryStatus enum | EPIC-A | task-3-advisory-entity-enum.md | task-3-digest.md |
| 4 | TASK-4 | Replace advisory_status joins with advisory.status column in queries and endpoints | EPIC-B | task-4-advisory-queries-use-status-column.md | task-4-digest.md |
| 5 | TASK-5 | Write advisory status enum directly in ingestion pipeline | EPIC-B | task-5-ingestion-write-enum.md | task-5-digest.md |
| 6 | TASK-6 | Update internal architecture documentation for advisory status enum | EPIC-C | task-6-architecture-docs.md | task-6-digest.md |
| 7 | TASK-7 | Merge feature branch TC-9005 to main | EPIC-C | task-7-merge-feature-branch.md | task-7-digest.md |

Digest note: in eval mode the digests were computed with `scripts/sha256-digest.py` over the local description markdown (everything after the Summary line). In a live run each digest is computed over the description re-fetched from Jira after creation, and posted as a standalone comment with no footnote, before any links or other comments.

## Feature label update

`jira.edit_issue(TC-9005, fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})` — existing label preserved.

## 6b — Links

Incorporates (Feature → Epic):
- TC-9005 → EPIC-A
- TC-9005 → EPIC-B
- TC-9005 → EPIC-C

Depend (inward = dependent, outward = dependency):
- TASK-2 → TASK-1
- TASK-3 → TASK-1, TASK-2
- TASK-4 → TASK-1, TASK-3
- TASK-5 → TASK-1, TASK-3
- TASK-6 → TASK-1, TASK-2, TASK-3, TASK-4, TASK-5
- TASK-7 → TASK-1, TASK-2, TASK-3, TASK-4, TASK-5, TASK-6

## Comments on TC-9005

1. `impact-map-comment.md` — Impact map + workflow mode decision (Steps 4 and 4.5)
2. `summary-comment.md` — Plan summary (Step 6c)

## Skipped / simulated steps

- Step 1.5 (parent link): no parent on Feature; interactive prompt not answerable in eval — skipped.
- Step 2 (Figma): no Figma link — skipped.
- Step 2.5 (issue-type discovery): not executable without Jira; Epic level-1 type assumed (Hierarchy Configuration sets by-sub-feature). Epic grouping would be shown to the user for approval.
- Bookend idempotency guard: Feature has no linked issues, so bookends are generated.
