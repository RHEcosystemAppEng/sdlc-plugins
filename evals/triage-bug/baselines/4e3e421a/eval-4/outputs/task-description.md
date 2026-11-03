# Step 5 – Generated Task for ACME-510

**Jira create call (not executed):**
- Project: ACME
- Issue type: Task
- Summary: Fix missing pagination headers on date-filtered GET /api/v2/advisories
- Labels: `ai-generated-jira`
- Link (Step 5b): link type `Blocks`, inward = <created-task-key> (blocker), outward = ACME-510 (blocked)
- Digest (Step 5c): re-fetch the created task description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` leaves out the `X-Total-Count` and `Link` (`rel="next"`) pagination headers when the request filters by date range (`publishedAfter` / `publishedBefore`). The filtered response body is correct, and unfiltered requests return the headers correctly. Clients that rely on pagination headers cannot work out the total count or page through filtered results. This task sends the date-filtered path through the same pagination flow as the unfiltered path, so that both return the same headers.

## Files to Modify
- `/api/v2/advisories` list handler in acme-backend (path to be confirmed). Send the date-filtered branch through the shared pagination response helper so `X-Total-Count` and `Link` are emitted.
- Advisory list/count query function used by the handler (path to be confirmed). Make sure the total-count query applies the same `publishedAfter`/`publishedBefore` predicates as the result query.
- Existing advisories endpoint integration test file (path to be confirmed). Add the reproducer test next to the existing unfiltered pagination tests.

> Note: Triage could not confirm exact file paths. The repository context available during triage did not include the advisories endpoint code. Before editing, locate the files with:
> - `grep -rn "publishedAfter\|published_after" /home/dev/repos/acme-backend`
> - `grep -rni "x-total-count" /home/dev/repos/acme-backend`
> - `grep -rn "/api/v2/advisories\|\"/advisories\"" /home/dev/repos/acme-backend`

## API Changes
- `GET /api/v2/advisories`: MODIFY. When `publishedAfter` and/or `publishedBefore` are supplied, the response now includes `X-Total-Count` (filtered total) and `Link` (with `rel="next"` when more pages exist), matching the unfiltered behavior. The response body does not change.

## Implementation Notes
Fixes ACME-510.

**Reproducer first.** Write the reproducer test before changing any production code and confirm that it fails:
- Trigger: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, with more than 10 advisories seeded inside the range (e.g., 15) and a few outside it (e.g., 3 published in 2024 or after 2025-06-30).
- Behavior before the fix (Actual Result): the body has the correct 10 filtered advisories, but `X-Total-Count` and `Link` are missing.
- Behavior after the fix (Expected Result): `X-Total-Count: 15`, and a `Link` header containing `rel="next"`. The next URL must keep `publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.

**Fix direction.**
- Find the shared pagination helper/wrapper the unfiltered branch uses to set `X-Total-Count` and `Link` (search for `X-Total-Count` / `rel="next"`). Make the date-filtered branch return through that same helper. Do not write header logic again inline.
- Check that the total count comes from a count query with the **same** date predicates as the result query. Using the unfiltered table total would make `X-Total-Count` wrong.
- Check that `Link` URL generation copies the incoming filter query parameters, so that following `rel="next"` keeps the filter.
- Possible causes to check: the filtered branch returns a plain JSON body and skips the paginated response type, or it skips the count query entirely.

**Scope.** Change only the date-filtered pagination path. Do not change filter semantics or response body shape.

**Conventions.** acme-backend has no CONVENTIONS.md. Follow the patterns in the existing advisories handler and its tests.

**Persistence.** None. Pagination headers are computed per request at query time, so no data migration is needed.

## Reuse Candidates
- Shared pagination response helper used by the unfiltered `/api/v2/advisories` branch (symbol to be confirmed via `grep -rni "x-total-count"`). It already emits `X-Total-Count` and `Link`. Reuse it rather than adding a parallel implementation.
- Existing unfiltered-pagination integration test for advisories (to be located). Copy its seeding and header-assertion pattern for the reproducer.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with more in-range advisories than `limit`, and asserts that `X-Total-Count` and `Link` (`rel="next"`) are present. The test fails before the fix and passes after it.
- [ ] Date-filtered requests return `X-Total-Count` equal to the number of advisories matching the date filter, not the unfiltered total.
- [ ] Date-filtered requests return a `Link` header with `rel="next"` when more pages exist, and the next URL keeps the `publishedAfter`/`publishedBefore` parameters.
- [ ] No `rel="next"` link is emitted on the last page of filtered results.
- [ ] Unfiltered `/api/v2/advisories` pagination behavior is unchanged.
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test: seed 15 advisories published between 2025-01-01 and 2025-06-30 and 3 outside that range. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert HTTP 200, 10 items in the body, `X-Total-Count == 15`, and `Link` contains `rel="next"` with a URL that includes `publishedAfter=2025-01-01` and `publishedBefore=2025-06-30`. Must fail on current main (headers missing) and pass after the fix.
- [ ] Last-page test: same filter with an offset/page that reaches the end. Assert `X-Total-Count == 15` and no `rel="next"` in `Link`.
- [ ] Single-bound tests: only `publishedAfter`, and only `publishedBefore`. Assert both headers are present with correct filtered totals.
- [ ] Regression test: an unfiltered request still returns `X-Total-Count` and `Link` as before.

## Verification Commands
- `cargo test advisories` — all advisories tests pass, including the new reproducer
- `curl -si "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE "x-total-count|^link:"` — both headers are printed

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` with the total number of matching advisories, and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body contains the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Non-filtered requests return the headers correctly.
- **Root Cause**: The date-filtered branch of the `/api/v2/advisories` list handler does not go through the shared pagination flow (it skips the pagination response wrapper and/or the filtered total-count query), so pagination headers are never set. Confidence is medium; the exact symbol must be confirmed in acme-backend.
- **Affects Version**: 0.9.0 (Jira: RHTPA 0.9.0, ID 62643, pending user confirmation)
