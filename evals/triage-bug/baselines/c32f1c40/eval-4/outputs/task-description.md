# Step 5 -- Generated Task Description: ACME-510

## Task Summary

Fix missing pagination headers when filtering advisories by date range

## Task Labels

`ai-generated-jira`

## Full Task Description

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination
headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are used.
Currently, the filtered query path bypasses pagination header generation, causing clients
that rely on these headers to fail when paginating filtered results. Fixes ACME-510.

## Files to Modify
- `src/api/advisories/handler.rs` -- Add pagination header generation to the filtered query path
- `src/api/advisories/query.rs` -- Ensure total count is computed for filtered queries

## Implementation Notes
The unfiltered query path for `/api/v2/advisories` correctly generates pagination headers
(`X-Total-Count` and `Link`). The filtered path (activated when `publishedAfter` and/or
`publishedBefore` query parameters are present) bypasses this logic.

The fix should:
1. Identify where the unfiltered path invokes pagination header generation (likely a
   shared utility or middleware function that computes total count and constructs headers).
2. Ensure the filtered path calls the same pagination header generation, passing the
   filtered query's total count rather than skipping it.
3. The total count query must apply the same date range filters as the data query, so
   `X-Total-Count` reflects the filtered result set size, not the unfiltered total.
4. The `Link` header's `rel="next"` URL must include the original filter parameters
   so that following pagination links preserves the filter context.

Reference the existing pagination header generation logic used by the unfiltered path
as the pattern to follow. Do not duplicate the logic -- reuse the existing function/method.

Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` headers are present and correct (test fails before fix, passes after)
- [ ] The `/api/v2/advisories` endpoint returns `X-Total-Count` header with the correct total count of matching advisories when date range filters are applied
- [ ] The `/api/v2/advisories` endpoint returns `Link` header with `rel="next"` when more pages exist in filtered results
- [ ] The `X-Total-Count` value reflects the filtered result count, not the unfiltered total
- [ ] Pagination links in the `Link` header preserve the `publishedAfter` and `publishedBefore` query parameters
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with a dataset containing more than 10 matching advisories. Assert `X-Total-Count` header equals the total number of matching advisories. Assert `Link` header contains `rel="next"` with correct URL including filter parameters. This test must fail before the fix and pass after.
- [ ] Test that `X-Total-Count` reflects the filtered count (not the unfiltered total) by verifying against a known dataset where filtered count differs from total count
- [ ] Test that pagination links preserve filter parameters by following the `Link: rel="next"` URL and verifying it returns the next page of filtered results
- [ ] Regression test: verify that unfiltered requests (`GET /api/v2/advisories?limit=10`) continue to return `X-Total-Count` and `Link` headers correctly

## Verification Commands
- `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` -- Response should include `X-Total-Count` and `Link` headers
- `GET /api/v2/advisories?limit=10` -- Response should continue to include pagination headers (regression check)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start backend service locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The filtered query path for `/api/v2/advisories` bypasses the pagination header generation logic. The unfiltered path correctly produces these headers, confirming the pagination logic works but is not invoked in the filtered branch.

## Jira Operations (would be performed)

### Step 5 -- Create Task

```
jira.create_issue(
  project: "ACME",
  summary: "Fix missing pagination headers when filtering advisories by date range",
  description: <task description above>,
  issue_type: "Task",
  additional_fields: { "labels": ["ai-generated-jira"] }
)
```

### Step 5b -- Link Task to Bug

```
jira.create_issue_link(
  link_type: "Blocks",
  inward_issue_key: <created-task-key>,
  outward_issue_key: "ACME-510"
)
```

### Step 5c -- Post Digest Comment

Would re-fetch the created task, compute SHA-256 digest of the persisted description
using `python3 scripts/sha256-digest.py`, and post a standalone digest comment:

```
[sdlc-workflow] Description digest: sha256-md:<computed-digest>
```
