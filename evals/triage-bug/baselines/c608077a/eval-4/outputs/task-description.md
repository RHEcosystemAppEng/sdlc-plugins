# Step 5 — Generated Task (ACME-510)

**Create call (not executed in this eval):**
```
jira.create_issue(
  cloudId: "mock-cloud-id-for-eval",
  projectKey: "ACME",
  issueTypeName: "Task",
  summary: "Fix missing pagination headers on /api/v2/advisories when filtering by date range",
  description: <below>,
  additional_fields: { "labels": ["ai-generated-jira"] }
)
```

**Step 5b — Link (not executed):**
```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key=<created-task-key>,   # Task blocks...
  outward_issue_key="ACME-510"           # ...the Bug
)
```

**Step 5c — Digest (not executed):** re-fetch the created task, write its description to
`/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`,
then post a standalone comment `[sdlc-workflow] Description digest: <tagged-digest>`, with no
footnote.

---

## Task Description

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` omits the `X-Total-Count` and `Link` pagination headers
when the request includes date-range filters (`publishedAfter` / `publishedBefore`). The filtered
body is correct, but clients cannot work out the total count or the number of pages. Unfiltered
requests return the headers correctly. This task makes date-filtered responses emit the same
pagination headers as unfiltered ones. Work starts with a reproducer test that fails before the
fix.

## Files to Modify
The investigation could not confirm exact paths: the code context available during triage did
not include this endpoint. Locate them in `acme-backend` first:
- Advisories list endpoint handler/service (find it with
  `grep -rn "publishedAfter\|published_after" /home/dev/repos/acme-backend/`): the date-range
  branch must return the paginated result (items, total count, next page) and must not skip the
  pagination metadata
- Pagination header emission code (find it with
  `grep -rn "X-Total-Count\|x-total-count" /home/dev/repos/acme-backend/`): make sure headers are
  attached for filtered results and that the `Link` URL keeps the date filter query parameters
- The existing advisories endpoint integration test file (find it with
  `grep -rln "advisories" /home/dev/repos/acme-backend/**/tests/`): add the reproducer test

## Implementation Notes
- **Traceability:** Fixes ACME-510 (https://mock-jira.example.com/browse/ACME-510). Affects
  Version: RHTPA 0.9.0.
- **Reproducer scenario (write first):**
  - Input: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
    against a dataset with more than 10 advisories published inside 2025-01-01..2025-06-30
    (e.g. 15) and a few outside the window.
  - Current (buggy) behavior, from the Actual Result: the body holds the correct filtered
    advisories, but the `X-Total-Count` and `Link` headers are missing.
  - Correct behavior, from the Expected Result: `X-Total-Count: 15` is present, and
    `Link: <url>; rel="next"` is present because more pages exist.
  - Control: the same dataset without the date params already returns both headers. Keep that as
    a regression assertion.
- **Suspected defect (confirm in code):** the date-range filter path in the advisories listing
  builds its response without the pagination metadata that the header logic needs. It either
  returns a plain list instead of the paginated result type, or skips the total-count query. The
  unfiltered path does carry this metadata.
- **Fix direction:** do not add new header code. Send the date-filtered query through the same
  paginated listing and header-emission code that the unfiltered `/api/v2/advisories` path uses
  today. Apply the date predicate to both the item query and the total-count query, so
  `X-Total-Count` reflects the filtered total and not the global total.
- **Link header:** the `rel="next"` URL must keep `publishedAfter` and `publishedBefore` (plus
  `limit`) and advance only the offset/page. Otherwise following the link would drop the filter.
- **Persistence:** none. Headers and counts are computed per request, so no data migration is
  needed.
- **Conventions:** there is no CONVENTIONS.md at the repository root. Follow the existing
  patterns in the advisories endpoint module and its tests.

## Reuse Candidates
- The existing pagination result type and helper used by the unfiltered `/api/v2/advisories`
  listing (locate with `grep -rn "Paginated\|X-Total-Count" /home/dev/repos/acme-backend/`). It
  already produces correct headers and should be reused for the filtered path.
- The existing `Link` header builder used by the unfiltered path. Reuse it, making sure it
  carries the extra query parameters.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` against seeded data with more in-window advisories than `limit`, and asserts that `X-Total-Count` and `Link` (`rel="next"`) are present. It fails before the fix and passes after.
- [ ] Date-filtered requests to `/api/v2/advisories` return `X-Total-Count` equal to the total number of advisories matching the date filter (not the unfiltered total)
- [ ] Date-filtered requests return a `Link` header with `rel="next"` when more pages exist, and its URL keeps the `publishedAfter`/`publishedBefore` parameters
- [ ] No `rel="next"` link is emitted on the last page of a date-filtered result
- [ ] Filtering with only one of `publishedAfter` or `publishedBefore` also returns the pagination headers
- [ ] Unfiltered `/api/v2/advisories` requests keep returning the same pagination headers (no regression)
- [ ] All existing tests pass

## Test Requirements
- [ ] Reproducer test (first): seed about 15 advisories published between 2025-01-01 and 2025-06-30 and about 5 outside that window. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert status 200, a body with 10 in-window advisories, `X-Total-Count == "15"`, and a `Link` header containing `rel="next"` whose URL includes `publishedAfter=2025-01-01` and `publishedBefore=2025-06-30`. Before the fix, the header assertions fail because the headers are absent, per ACME-510's Actual Result.
- [ ] Last-page test: request the second page of the same filtered query. Assert `X-Total-Count == "15"`, 5 items, and no `rel="next"` in `Link`.
- [ ] Single-bound test: `publishedAfter` only, and `publishedBefore` only, each return a correct `X-Total-Count`.
- [ ] Regression test: unfiltered `GET /api/v2/advisories?limit=10` still returns `X-Total-Count` (the full total) and `Link` `rel="next"`.

## Verification Commands
- `cargo test advisories`: all advisories tests pass, including the new reproducer
- `curl -si "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE "^(x-total-count|link):"`: both headers are printed

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` (total matching advisories) and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body contains the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Non-filtered requests return the headers correctly.
- **Root Cause**: The date-range filter path of the advisories listing builds its response without the pagination metadata (total count and next page) that the header logic needs, so neither pagination header is emitted. The unfiltered path carries this metadata. Exact file and symbol to be confirmed in `acme-backend`.
