## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination headers when date-range filter parameters (`publishedAfter`, `publishedBefore`) are used. Currently, the filtered query code path bypasses the pagination header logic, causing clients to lose pagination metadata when filtering advisories by date range. Fixes ACME-510.

## Files to Modify
- `src/api/advisories.rs` (or equivalent endpoint handler) -- add pagination header logic to the date-range-filtered query path, reusing the existing pagination utility already used by the unfiltered path
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace from extracted heading names in the convention parsing logic (related fix for the same normalization pattern)

## Implementation Notes
- The unfiltered query path for `GET /api/v2/advisories` already correctly computes and sets `X-Total-Count` and `Link` pagination headers. Identify the pagination utility or function it calls and ensure the filtered query path (when `publishedAfter`/`publishedBefore` are present) invokes the same logic.
- The total count query must be executed against the filtered result set, not the unfiltered set, so that `X-Total-Count` reflects the number of advisories matching the date range.
- The `Link` header should include `rel="next"` pointing to the next page of filtered results when more pages exist beyond the requested `limit`.
- For the heading extraction fix in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, change `line[3:]` to `line[3:].strip()` so that trailing whitespace on `## ` headings is removed before convention name matching.
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. A new test case should be added to cover this edge case.
- No CONVENTIONS.md exists in the repository root. No additional conventions apply.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: sends a `GET /api/v2/advisories` request with `publishedAfter` and `publishedBefore` query parameters and a `limit`, and asserts that the response includes `X-Total-Count` and `Link` headers. This test must fail before the fix and pass after.
- [ ] The `/api/v2/advisories` endpoint returns `X-Total-Count` header with the correct total count of matching advisories when date-range filters are applied.
- [ ] The `/api/v2/advisories` endpoint returns a `Link` header with `rel="next"` when more filtered results exist beyond the requested limit.
- [ ] Non-filtered requests to `/api/v2/advisories` continue to return pagination headers correctly (no regression).
- [ ] Heading extraction in convention parsing strips trailing whitespace so that convention name matching works regardless of whitespace in source headings.
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test: call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and assert that the response headers include `X-Total-Count` with a numeric value and `Link` with `rel="next"` when total results exceed the limit. Before the fix, these headers should be absent; after the fix, they should be present.
- [ ] Test that unfiltered `GET /api/v2/advisories?limit=10` still returns `X-Total-Count` and `Link` headers (regression guard).
- [ ] Test with date-range filters that return zero results -- `X-Total-Count` should be `0` and `Link` header should be absent (no next page).
- [ ] Test with date-range filters where results fit within a single page -- `X-Total-Count` should match result count and `Link` header should be absent.
- [ ] Test that convention heading extraction correctly strips trailing whitespace (e.g., `## Migration Patterns  ` is extracted as `"Migration Patterns"`).

## Verification Commands
- `cargo test` -- all existing tests pass without regression
- `curl -s -D - "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -E "X-Total-Count|Link"` -- both headers present in response

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filter code path in the `/api/v2/advisories` endpoint handler bypasses the pagination header utility. The unfiltered path invokes this utility correctly, but the filtered branch was implemented without wiring up the same pagination header logic.
