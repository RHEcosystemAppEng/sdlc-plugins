# Root Cause Analysis – ACME-510 (Step 4)

## Root Cause

**What is broken:** The `GET /api/v2/advisories` endpoint does not attach `X-Total-Count`
and `Link` pagination headers when date range filter parameters (`publishedAfter`,
`publishedBefore`) are supplied. Non-filtered requests return these headers correctly.

**Why it is broken:** The route handler for `/api/v2/advisories` contains two code paths:
a base (non-filtered) path and a filtered path. The pagination header attachment logic —
which computes the total matching count and builds the `Link` header value — is called
in the base path but is absent from (or not reached in) the filtered path. When the
handler detects date range parameters and branches into the filtered code path, it
executes the database query and serializes the response body, but returns before the
header attachment function is invoked.

**Where it is broken:**

- **Primary location:** The advisory route handler (inferred: `src/api/advisories.rs`)
  in the filtered branch — specifically the point where filtered results are assembled
  into the HTTP response but pagination headers are not set.
- **Secondary location (if applicable):** Any shared pagination utility
  (`src/middleware/pagination.rs` or `src/api/common.rs`) that exposes
  `set_pagination_headers()` — this function exists and works correctly for non-filtered
  responses, but is not called in the filtered code path.

**How to verify the fix:**

A reproducer test should:
1. Seed the database (or mock layer) with a known set of advisories that span a date range.
2. Issue `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
   against the test service.
3. Assert that the response includes `X-Total-Count` with the correct count of matching
   advisories and `Link` with a `rel="next"` value when the result set exceeds the limit.
4. Confirm the test **fails** before the fix (headers absent) and **passes** after
   (headers present with correct values).

---

## Affected Files

| File                            | Nature of Defect                                          |
|---------------------------------|-----------------------------------------------------------|
| `src/api/advisories.rs`         | Filtered branch returns response without calling header attachment logic |
| `src/middleware/pagination.rs` (or `src/api/common.rs`) | Header utility exists but is not invoked for filtered requests |

---

## Suggested Approach

1. Locate the filtered query branch in the advisory route handler.
2. Identify the call site where the base (non-filtered) path sets `X-Total-Count` and
   `Link` headers.
3. Ensure the same header-attachment logic (or the shared utility function) is called
   after computing the filtered result count — parallel to how it is called in the
   non-filtered branch.
4. The filtered count query must be issued alongside the filtered data query so that
   the total is available before header construction.
5. Write a reproducer integration test that exercises the filtered path and asserts
   both headers are present with correct values.

---

## Reproducer Strategy

| Test phase   | What to assert                                                  |
|--------------|-----------------------------------------------------------------|
| Before fix   | `X-Total-Count` header absent, `Link` header absent             |
| After fix    | `X-Total-Count: N` present (N = count of advisories in range), `Link: <url>; rel="next"` present when N > limit |

Test type: integration test against the advisory route handler (or a full HTTP round-trip
test using the test harness already in use for non-filtered advisory tests).

---

## Decomposition Guard

This bug has a **single root cause**: the filtered branch of one route handler fails to
call header attachment logic. Although the fix may touch the route handler and possibly
a shared pagination utility, both changes address the same defect. A single Task is
appropriate — no decomposition is needed.

---

## Persistence-Impact Assessment

The bug affects response header generation only. Headers are computed at query time from
current database state and are never persisted. **No data migration is required.**

---

## Comment to Post on ACME-510

The following would be posted as an ADF comment on the Bug issue (with Comment Footnote appended):

---

**Root Cause**

The `GET /api/v2/advisories` route handler branches on the presence of date range filter
parameters. The non-filtered branch correctly calls the pagination header attachment
function (`set_pagination_headers` or equivalent), but the filtered branch returns the
HTTP response without invoking it. As a result, `X-Total-Count` and `Link` headers are
never set for filtered queries.

**Affected Files**

- `src/api/advisories.rs` — filtered code path in the advisory route handler
- `src/middleware/pagination.rs` (or `src/api/common.rs`) — header utility not called
  from the filtered path

**Suggested Approach**

Locate the point where the non-filtered path attaches pagination headers and replicate
the same call (or refactor into a shared helper) in the filtered branch. The total
count of filtered results must be available before header construction.

**Reproducer Strategy**

Integration test: seed advisories spanning a known date range, call the filtered
endpoint with a `limit` smaller than the total count, and assert `X-Total-Count` equals
the total count and `Link` contains `rel="next"`. The test must fail before the fix and
pass after.
