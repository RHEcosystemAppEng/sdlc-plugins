# Step 5 — Generated Task: ACME-510

## Task creation parameters

```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix missing pagination headers on /api/v2/advisories when filtering by date range",
  description: <markdown below>,
  additional_fields: { "labels": ["ai-generated-jira"] }
)
```

After creation:

- **Step 5b link:** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-510")`. The Task blocks the Bug.
- **Step 5c digest:** re-fetch `<new-task-key>`, write the description to `/tmp/desc-<new-task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<new-task-key>.txt`, then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` with no footnote.

---

## Task description

```markdown
## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` leaves out the `X-Total-Count` and `Link` pagination headers when the request includes the date-range filters `publishedAfter` / `publishedBefore`. The filtered response body is correct, and unfiltered requests return both headers. Clients that rely on pagination headers cannot work out the total number of pages for date-filtered queries. This task restores pagination headers on the date-range filtered path, so filtered and unfiltered requests behave the same way.

## Files to Modify
- Advisories list handler for `GET /api/v2/advisories` (date-range filter branch). Exact path not determined during triage. Locate it with `grep -rn "publishedAfter\|published_after" src/`. Send the filtered query through the paginated query/response path.
- Advisory list query/service function used for date-range filtering (if separate from the handler). Exact path not determined during triage. Make sure it returns the total count with the date-range predicate applied.
- Existing integration tests for the advisories endpoint. Exact path not determined during triage. Locate them with `grep -rn "api/v2/advisories" tests/`. Add the reproducer test.

## Implementation Notes
Fixes ACME-510.

**Note on discovery:** triage could not inspect the advisories handler source. The repository context available during triage did not include it. The file paths and symbols above must be confirmed first. Search the repo for:
- `publishedAfter|published_after|publishedBefore|published_before|filterDateRange` to find the date-range branch
- `X-Total-Count|x-total-count` and `rel="next"` / `LINK` to find the existing pagination header logic used by the unfiltered path
- The paginated result type (for example `Paginated*` / a `total` field) returned by the unfiltered advisory list query

**Root cause (hypothesis):** the date-range filtered request takes a code path that does not produce or forward pagination metadata. It either skips the total-count query or returns a body-only response instead of the paginated response wrapper. As a result, the shared header logic has nothing to emit. Both missing headers come from this single gap.

**Fix direction:**
- Reuse the same pagination mechanism that the unfiltered path already uses. Do not write separate header-setting code for the filtered branch.
- Compute the total count **with the date-range predicate applied**. `X-Total-Count` must reflect the filtered total, not the unfiltered total and not the page size.
- Build `Link` (`rel="next"`, plus any other rels the unfiltered path emits) with the original `publishedAfter` / `publishedBefore` query parameters kept in the generated URLs, so following `next` stays within the filtered result set.

**Reproducer test guidance (write this first, before the fix):**
- Scenario: seed more than 10 advisories with publish dates between 2025-01-01 and 2025-06-30, plus some outside that range.
- Request: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- Current (buggy) behavior from the Actual Result: the body has the correct filtered advisories, but `X-Total-Count` and `Link` headers are **absent**. The test must fail on this before the fix.
- Correct behavior from the Expected Result: `X-Total-Count: <n>`, where n is the count of seeded in-range advisories, and `Link: <url>; rel="next"`, because more than one page exists.
- Follow the assertion style of the existing advisories endpoint integration tests (locate them as described above).

**Persistence impact:** none. Pagination headers are computed per request. No data migration is required.

**Conventions:** the repository has no `CONVENTIONS.md`. Follow the patterns in the surrounding handler and test code.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` (`rel="next"`) are present and correct. It fails before the fix and passes after.
- [ ] Date-range filtered requests to `/api/v2/advisories` return `X-Total-Count` equal to the total number of advisories matching the date range.
- [ ] Date-range filtered requests return a `Link` header with `rel="next"` when more pages exist, and its URLs keep the `publishedAfter`/`publishedBefore` parameters.
- [ ] The filtered path reuses the existing pagination mechanism used by unfiltered requests. No duplicated header logic.
- [ ] Unfiltered requests to `/api/v2/advisories` still return correct pagination headers.
- [ ] No regressions in the existing test suite.

## Test Requirements
- [ ] Reproducer test: seed more than 10 advisories inside 2025-01-01..2025-06-30 and some outside. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert the response contains `X-Total-Count` equal to the in-range count, and that `Link` contains `rel="next"`. Before the fix, it fails because both headers are absent.
- [ ] Test that the last page of a date-filtered result has no `rel="next"` in `Link`, and that `X-Total-Count` stays the filtered total.
- [ ] Test that a date-filtered request returning fewer results than `limit` still includes `X-Total-Count`.
- [ ] Regression test: an unfiltered `GET /api/v2/advisories?limit=10` still returns `X-Total-Count` and `Link`.

## Verification Commands
- `cargo test` — all tests pass, including the new reproducer test
- `curl -s -D - -o /dev/null "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10"` — response headers include `X-Total-Count` and `Link: <...>; rel="next"` (when more pages exist)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` with the total number of matching advisories, and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body contains the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtered path (`publishedAfter`/`publishedBefore`) in the advisories list handler does not produce or forward pagination metadata (the filtered total count), so the shared pagination header logic is never applied. This is a hypothesis: the exact code location needs confirmation because the handler source was not available during triage.
- **Affects Version**: RHTPA 0.9.0 (ID 62643), pending user confirmation in Step 4.5.
```

---

## Step 7 — Report (what the user would see)

- Task created: `<new-task-key>`, linked as blocking ACME-510
- Root cause: the date-range filtered path on `/api/v2/advisories` skips pagination metadata, so `X-Total-Count` and `Link` are omitted. Confidence is limited because the handler source was not in the provided repository context.
- Reproducer: a filtered request with `limit=10` over a seeded dataset of more than 10 in-range advisories, asserting both headers.
- Next step: "Run `/implement-task <new-task-key>` to implement the fix."
