# Step 5 -- Generated Task Description

**Task Summary:** Fix missing pagination headers in date-range filtered advisories endpoint

**Labels:** `ai-generated-jira`

**Jira API call:** `jira.create_issue(project=ACME, summary="Fix missing pagination headers in date-range filtered advisories endpoint", issueType=Task, labels=["ai-generated-jira"], description=<below>)`

---

## Repository
acme-backend

## Target Branch
main

## Description
The `GET /api/v2/advisories` endpoint omits `X-Total-Count` and `Link` pagination headers when the request includes date-range filter parameters (`publishedAfter`, `publishedBefore`). The unfiltered query path correctly invokes the shared pagination utility, but the filtered path bypasses it entirely. This fix integrates the pagination header logic into the date-range filtered query path so that filtered responses include accurate pagination headers. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` -- integrate pagination header generation into the date-range filtered query path

## Implementation Notes
The root cause is a code-path divergence in the advisories endpoint handler. The unfiltered query path invokes the shared pagination utility (likely in `src/api/pagination.rs`) which executes a count query and sets `X-Total-Count` and `Link` response headers. The date-range filtered path skips this utility call.

To fix:
1. Locate the filtered query branch in `src/api/v2/advisories.rs` where `publishedAfter`/`publishedBefore` parameters trigger a different code path.
2. Ensure the filtered path invokes the same pagination utility (e.g., `set_pagination_headers` or equivalent) used by the unfiltered path.
3. Pass the date-range filter predicates to the count query so the total count reflects only the filtered result set, not all advisories.
4. Verify that the `Link` header construction uses the filtered count for `rel="last"` page calculation.

Look for the existing pagination utility in `src/api/pagination.rs` -- reuse its interface rather than duplicating header-setting logic.

## Reuse Candidates
- `src/api/pagination.rs::set_pagination_headers` -- shared pagination utility already used by the unfiltered advisories path; invoke it from the filtered path with the same interface

## Acceptance Criteria
- [ ] Reproducer test: a test sends `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` headers are present and correct (fails before fix, passes after)
- [ ] The date-range filtered query path invokes the shared pagination utility to set `X-Total-Count` and `Link` response headers
- [ ] The count query used for `X-Total-Count` applies the same date-range filter predicates as the data query
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: integration test that calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and asserts: (1) `X-Total-Count` header is present and equals the number of advisories within the date range, (2) `Link` header with `rel="next"` is present when results exceed `limit`, (3) response body contains only advisories within the specified date range
- [ ] Regression test: verify that unfiltered `GET /api/v2/advisories` requests still return correct pagination headers
- [ ] Edge case test: verify pagination headers when the date-range filter returns zero results (expect `X-Total-Count: 0` and no `Link` header)

## Verification Commands
- `cargo test --test advisories` -- run advisories integration tests, expect all pass including new reproducer test
- `curl -s -D- "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | head -20` -- manually verify pagination headers are present in filtered response

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally; call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`; inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtered query path in `src/api/v2/advisories.rs` bypasses the shared pagination utility that sets `X-Total-Count` and `Link` response headers. The unfiltered path invokes this utility correctly.

---

## Post-creation steps

### Step 5b -- Link Task to Bug

```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key=<created-task-key>,
  outward_issue_key=ACME-510
)
```

The Task blocks the Bug -- ACME-510 cannot be resolved until the fix Task is completed.

### Step 5c -- Post Digest Comment

1. Re-fetch the created task: `jira.get_issue(<created-task-key>)`
2. Write description to temp file: `/tmp/desc-<task-key>.txt`
3. Compute tagged digest: `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`
4. Post digest comment on the created task (standalone ADF, no Comment Footnote)

### Step 7 -- Report Result

> Task `<created-task-key>` has been created and linked to ACME-510.
>
> **Root cause:** The date-range filtered query path in the advisories endpoint
> bypasses the shared pagination utility, omitting `X-Total-Count` and `Link`
> response headers.
>
> **Reproducer strategy:** An integration test calls the advisories endpoint with
> `publishedAfter`/`publishedBefore` parameters and asserts pagination headers
> are present and correct.
>
> Run `/implement-task <created-task-key>` to implement the fix.
