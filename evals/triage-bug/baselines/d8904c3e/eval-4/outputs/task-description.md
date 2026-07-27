# Step 5 -- Generated Task Description: ACME-510

**Task Summary:** Fix missing pagination headers on date-range-filtered advisory queries

**Labels:** ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to return `X-Total-Count` and `Link` pagination headers when date-range filter parameters (`publishedAfter`, `publishedBefore`) are used. Currently, filtered requests return the correct response body but omit pagination headers, while unfiltered requests return headers correctly. This breaks clients that rely on pagination headers to navigate result pages. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` (or equivalent route handler) -- ensure the date-range filtered query path invokes pagination header generation with the filtered count
- Pagination utility/middleware file -- if conditional logic excludes filtered paths from header generation, remove or fix the condition

## Implementation Notes
The root cause is that the date-range filtered query path in the advisory listing endpoint bypasses the pagination header generation logic. The unfiltered path correctly computes the total count and generates `X-Total-Count` and `Link` headers, but the filtered path does not.

To fix:
1. Locate the advisory endpoint handler that processes `publishedAfter` and `publishedBefore` query parameters.
2. Ensure the count query used for pagination includes the same date-range filter criteria as the main query.
3. Ensure the pagination header generation logic (`X-Total-Count` and `Link`) runs for filtered query results, not just unfiltered ones.
4. Follow the same pagination pattern already used by the unfiltered path -- reuse the existing pagination utility/helper rather than reimplementing.

The advisory endpoint likely has a query builder pattern where the date-range filters are applied. The fix should apply the same filters to the count query and pass the total count to the existing header generation function.

Reference the existing unfiltered pagination implementation as the pattern to follow. No CONVENTIONS.md was found in the repository root.

Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=<date>&publishedBefore=<date>&limit=<n>` (where matching results exceed `limit`) and asserts that `X-Total-Count` and `Link` headers are present with correct values. This test must fail before the fix and pass after.
- [ ] The `X-Total-Count` header returns the total number of advisories matching the date-range filter, not the total unfiltered count.
- [ ] The `Link` header includes `rel="next"` when more pages exist for the filtered result set.
- [ ] Unfiltered requests (`GET /api/v2/advisories?limit=<n>`) continue to return pagination headers correctly (no regression).
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test: Seed test data with 15+ advisories spanning multiple dates. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` where more than 10 advisories match the filter. Assert: (1) `X-Total-Count` header is present and equals the total filtered count, (2) `Link` header is present with `rel="next"`. This test should fail before the code fix and pass after.
- [ ] Pagination correctness test: Verify that the `X-Total-Count` value matches the actual number of advisories within the date range, not the total unfiltered count.
- [ ] Boundary test: Call with a date range that returns fewer results than `limit` and verify `X-Total-Count` equals the result count and `Link` header with `rel="next"` is absent.
- [ ] Regression test: Verify that unfiltered advisory listing requests still include correct pagination headers.

## Verification Commands
- `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` -- response must include `X-Total-Count` and `Link` headers
- `GET /api/v2/advisories?limit=10` -- response must still include `X-Total-Count` and `Link` headers (regression check)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start backend service locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtered query path in the advisory endpoint bypasses the pagination header generation logic. The filtered path either skips the count query or fails to pass filter criteria to it, resulting in omitted headers.

---

## Jira Operations (Step 5, 5b, 5c)

### Step 5 -- Task Creation

```
jira.create_issue(
  project: "ACME",
  summary: "Fix missing pagination headers on date-range-filtered advisory queries",
  description: <task description above>,
  issue_type: "Task",
  labels: ["ai-generated-jira"]
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

The Task (inward/blocker) blocks the Bug (outward/blocked): the Bug cannot be resolved until the Task is done.

### Step 5c -- Post Digest Comment

After task creation, the description would be re-fetched from Jira, hashed via `python3 scripts/sha256-digest.py`, and the tagged digest posted as a standalone comment on the created task (no Comment Footnote on digest comments).

### Step 6 -- Decomposition Guard

This bug has a single root cause (date-range filtered path bypassing pagination header logic). No decomposition is needed -- a single Task is appropriate.

### Step 7 -- Report Result

Task created and linked to ACME-510. The root cause is that date-range filtered advisory queries bypass pagination header generation. The fix ensures the filtered path invokes the same pagination logic as the unfiltered path. The reproducer test calls the filtered endpoint and asserts both `X-Total-Count` and `Link` headers are present.

Next step: Run `/implement-task <task-key>` to implement the fix.
