# Task Creation Log — TC-9001

Simulated Jira operations (no external services contacted). Placeholder keys TC-9101..TC-9107 stand in for the keys Jira would assign.

## Pre-creation steps

- Step 0: Project Configuration validated (Repository Registry, Jira Configuration, Code Intelligence present).
- Step 1: Feature fetched (from `feature-standard.md`): priority `Major`, fixVersions `[RHTPA 1.5.0]`, doc impact `Updates`.
- Step 1.5: Parent link — Feature has no parent; user prompt skipped (no input) → no parent link set.
- Step 2: No Figma URL → skipped.
- Step 2.5: Issue types — no level-1 (Epic) type available in this run → Feature → Task hierarchy; `by-sub-feature` grouping not applied.
- Step 4: Impact map comment posted on TC-9001 → `impact-map.md`.
- Step 4.5: Workflow mode `direct-to-main` (included in the impact map comment). No `workflow:feature-branch` label; no bookend tasks.

## 6a — Issues created

Every call uses `projectKey=TC`, issue type = Task (level 0), no `parent`, and:

```json
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

| # | Key | Summary | Description file | Digest comment |
|---|---|---|---|---|
| 1 | TC-9101 | Add advisory severity summary model and SBOM aggregation service method | task-1-severity-summary-service.md | task-1-digest.md |
| 2 | TC-9102 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache | task-2-advisory-summary-endpoint.md | task-2-digest.md |
| 3 | TC-9103 | Invalidate cached advisory summaries on advisory ingestion | task-3-cache-invalidation-on-ingestion.md | task-3-digest.md |
| 4 | TC-9104 | Support optional threshold query parameter on advisory-summary (non-MVP) | task-4-threshold-query-param.md | task-4-digest.md |
| 5 | TC-9105 | Document advisory-summary endpoint in REST API reference | task-5-api-reference-docs.md | task-5-digest.md |
| 6 | TC-9106 | Smoke tests for advisory severity aggregation | task-6-smoke-tests.md | task-6-digest.md |
| 7 | TC-9107 | Performance benchmarks for advisory severity aggregation | task-7-performance-benchmarks.md | task-7-digest.md |

Digest note: in a live run the digest is computed with `scripts/sha256-digest.py` over the description re-fetched from Jira (post-normalization). Here it was computed over the submitted markdown body (the file minus its `**Summary**` line), since no Jira round-trip was possible. Digest comments are standalone and carry no footnote.

## 6b — Links

Incorporates (Feature → Task): TC-9001 → TC-9101, TC-9102, TC-9103, TC-9104, TC-9105, TC-9106, TC-9107

Depend (`inward` = dependent, `outward` = dependency):

| Dependent | Depends on |
|---|---|
| TC-9102 (Task 2) | TC-9101 (Task 1) |
| TC-9103 (Task 3) | TC-9102 (Task 2) |
| TC-9104 (Task 4) | TC-9102 (Task 2) |
| TC-9105 (Task 5) | TC-9101, TC-9102, TC-9103, TC-9104 |
| TC-9106 (Task 6) | TC-9101, TC-9102, TC-9103, TC-9104 |
| TC-9107 (Task 7) | TC-9101, TC-9102, TC-9103, TC-9104 |

## 6c — Summary comment

Posted on TC-9001 → `summary-comment.md`.
