# Task Creation Log — TC-9001 (simulated; no Jira calls made)

## Type-to-role mapping (Step 2.5)

```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)   # from CLAUDE.md Jira Configuration
  Epic:    — not discovered (offline run; project issue types could not be fetched)
  Task:    Task (level 0)
```
No Epic-level type was found, so tasks are created directly under the Feature. Step 6a.0 is skipped. `Default epic grouping strategy: by-sub-feature` from CLAUDE.md is not applied.

## Step 1.5 parent link
Skipped. The Feature has no parent, and the non-interactive default is to skip the optional link.

## Bookend idempotency guard
Not applicable: the mode is `direct-to-main`, so no bookend tasks are generated.

## Issues to create (project TC, issue type Task, no parent)

`additional_fields` (identical for every task):
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- `priority` is propagated because the Feature priority is `Major`, not "Undefined".
- `fixVersions` is propagated because the Feature has `RHTPA 1.5.0` and `fixVersion scope` is `both`.

| # | Placeholder key | Summary | Description file | Digest comment file |
|---|---|---|---|---|
| 1 | TASK-1 | Add advisory severity summary model and service aggregation | task-1-severity-summary-service.md | task-1-digest.md |
| 2 | TASK-2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | task-2-advisory-summary-endpoint.md | task-2-digest.md |
| 3 | TASK-3 | Invalidate cached advisory summaries on advisory/SBOM ingestion | task-3-cache-invalidation-on-ingestion.md | task-3-digest.md |
| 4 | TASK-4 | Support ?threshold query parameter on advisory-summary endpoint (non-MVP) | task-4-threshold-query-param.md | task-4-digest.md |
| 5 | TASK-5 | Document advisory-summary endpoint in REST API reference | task-5-docs-rest-api-reference.md | task-5-digest.md |
| 6 | TASK-6 | Smoke Tests for advisory severity aggregation | task-6-smoke-tests.md | task-6-digest.md |
| 7 | TASK-7 | Performance Benchmarks for advisory severity aggregation | task-7-performance-benchmarks.md | task-7-digest.md |

Digest note: in a live run, each digest is computed with `scripts/sha256-digest.py` on the description re-fetched from Jira after creation. In this offline run, it is computed on the description file as written. Each digest comment is standalone and has no footnote.

## Feature label
`workflow:feature-branch` is not added because the mode is `direct-to-main`.

## Links (Step 6b)

Incorporates (inward TC-9001 → outward task): TASK-1, TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7

Depend (inward = dependent, outward = dependency):
| Dependent | Depends on |
|---|---|
| TASK-2 | TASK-1 |
| TASK-3 | TASK-2 |
| TASK-4 | TASK-2 |
| TASK-5 | TASK-1, TASK-2, TASK-3, TASK-4 |
| TASK-6 | TASK-1, TASK-2, TASK-3, TASK-4 |
| TASK-7 | TASK-1, TASK-2, TASK-3, TASK-4 |
