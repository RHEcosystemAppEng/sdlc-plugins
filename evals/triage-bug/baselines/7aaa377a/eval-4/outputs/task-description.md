# Task Description – Fix Missing Pagination Headers for Filtered Advisory Queries

> This is the task description that would be created in Jira via `jira.create_issue`.
> The created task would be linked to ACME-510 with link type "Blocks"
> (Task blocks Bug), and labeled `ai-generated-jira`.

---

## Repository
acme-backend

## Target Branch
main

## Description

Fix the `GET /api/v2/advisories` endpoint so that `X-Total-Count` and `Link` pagination
headers are included in responses when date range filter parameters (`publishedAfter`,
`publishedBefore`) are present. Currently, the filtered query branch of the route
handler returns the HTTP response without attaching these headers, while the
non-filtered branch correctly sets them. Clients that rely on pagination headers to
determine total pages and navigate multi-page results cannot function correctly when
filtering by date range.

Fixes ACME-510.

## Files to Modify

- `src/api/advisories.rs` — extend the filtered query branch to call the pagination header
  attachment logic after computing the filtered result count, mirroring the non-filtered branch
- `src/middleware/pagination.rs` (or `src/api/common.rs`) — if the header utility is not
  already shared, refactor it so both branches call a single function rather than duplicating
  the logic

## Implementation Notes

**Root cause recap (from ACME-510 investigation):**
The advisory route handler forks on the presence of `publishedAfter`/`publishedBefore`
query parameters. The base (non-filtered) branch invokes the pagination header attachment
function and returns correct headers. The filtered branch executes the filtered database
query and serializes the response body but returns before the header attachment function
is reached.

**Fix approach:**
1. Locate the divergence point in `src/api/advisories.rs` where the filtered branch
   assembles the HTTP response.
2. Find the call to `set_pagination_headers()` (or equivalent) in the non-filtered branch.
3. Ensure the filtered branch issues a `count` query for the filtered result set (matching
   the same `publishedAfter`/`publishedBefore` predicates) to determine the total count.
4. Call the same header attachment function — passing the filtered total count and the
   pagination parameters — before returning the filtered response.
5. If the header logic is duplicated between branches rather than shared, extract it into
   a single utility function and call it from both branches.

**Reproducer test guidance:**
- Trigger: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- Before fix — assert: `X-Total-Count` header absent, `Link` header absent
- After fix — assert:
  - `X-Total-Count: N` present, where N equals the number of advisories whose published
    date falls in `[2025-01-01, 2025-06-30]`
  - `Link: <url>; rel="next"` present when N exceeds the `limit` value

**Existing test patterns to reference:**
- Locate existing integration tests for `GET /api/v2/advisories` (non-filtered) that
  assert pagination headers — follow the same test setup, seeding, and assertion style.
- Existing tests do NOT cover the filtered + pagination headers combination; this is the
  gap that must be filled.

No CONVENTIONS.md was found at the repository root.

## Acceptance Criteria

- [ ] **Reproducer test**: an integration test for `GET /api/v2/advisories` with
  `publishedAfter` and `publishedBefore` parameters asserts that `X-Total-Count` and
  `Link` headers are present and correct — this test must fail before the fix is applied
  and pass after.
- [ ] The `GET /api/v2/advisories` endpoint returns `X-Total-Count: N` when date range
  filters are supplied, where N equals the count of advisories matching those filters.
- [ ] The `GET /api/v2/advisories` endpoint returns `Link: <url>; rel="next"` when
  date range filters are supplied and the result set exceeds the page `limit`.
- [ ] Non-filtered requests to `GET /api/v2/advisories` continue to return correct
  pagination headers (no regression).
- [ ] All existing tests pass.

## Test Requirements

- [ ] **Reproducer test** (add first): integration test that seeds advisories spanning a
  known date range, calls `GET /api/v2/advisories?publishedAfter=<start>&publishedBefore=<end>&limit=<n>`
  with a limit smaller than the total count, and asserts:
  (a) `X-Total-Count` equals the count of advisories within the date range, and
  (b) `Link` header contains `rel="next"` with the correct next-page URL.
  The test must fail before the fix and pass after.
- [ ] Regression test: call `GET /api/v2/advisories` without date range parameters and
  assert `X-Total-Count` and `Link` headers remain correct (guards against regressions
  from refactoring the header attachment logic).
- [ ] Edge case: call with date range that matches zero advisories — assert `X-Total-Count: 0`
  and no `Link` header.

## Verification Commands

- `cargo test --test advisories_pagination` — all pagination header tests pass, including the new reproducer

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**:
  1. Start the backend service locally.
  2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
  3. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` and `Link: <url>; rel="next"` (when more pages exist).
- **Actual Result**: Response body contains the correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return headers correctly.
- **Root Cause**: The advisory route handler branches on date range filter parameters. The filtered branch returns the HTTP response without calling the pagination header attachment function that the non-filtered branch correctly invokes. The filtered total count is not computed before the response is returned, so headers are never set.
