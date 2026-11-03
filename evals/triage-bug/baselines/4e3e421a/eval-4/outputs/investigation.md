# Steps 2–3 – Reproduce/Trace and Codebase Investigation for ACME-510

## Step 2 – Reproduce/Trace

### Runnable reproduction
The Steps to Reproduce contain a runnable HTTP call:

```
GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10
```

These would be compared:
1. A control request without date filters: `curl -si "http://localhost:8080/api/v2/advisories?limit=10"`. Expect `X-Total-Count` and `Link` to be present.
2. The bug request: `curl -si "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10"`. Expect both headers to be missing.

**Reproduction outcome: not run (environment-dependent).** The eval forbids external tool calls, and no running acme-backend instance is available. The reporter's Actual Result is the only evidence. That evidence is a useful differential: the same endpoint returns the headers on the unfiltered path and drops them on the date-filtered path.

### Code-path tracing
Entry point: the HTTP handler for `GET /api/v2/advisories` in `acme-backend` (Rust).

The differential points to the fault being **after** query construction and **before** the response is built. The filtered branch returns a correct body, so the filter itself works. What is missing is pagination metadata (total count and the next-page link). So the filtered branch most likely:
- (a) returns a body-only response and skips the shared pagination/response helper used by the unfiltered branch, or
- (b) skips the total-count query, leaving the helper without a total so it emits no headers.

## Step 3 – Codebase Investigation

### Target repository
- Code paths in the description (`/api/v2/advisories`, backend service) map to **acme-backend** in the Repository Registry, at `/home/dev/repos/acme-backend`.
- Component field says `sdlc-workflow`. That does not fit a backend REST endpoint and looks like a mis-set Component. It was not used to narrow the search.

### Tooling
- The Registry lists Serena instance `serena_backend`, but the Code Intelligence section says **no Serena MCP servers are configured**. The investigation therefore falls back to Read/Grep/Glob, as the skill requires.
- This eval forbids external tool calls, so the supplied repository context (`repo-context-mock.md`) is the only view of the codebase.

### Findings from the supplied repository context

**The supplied context does not cover this bug.** `repo-context-mock.md` says it describes code paths "for bug ACME-500". Its contents are:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`: a CONVENTIONS.md heading parser (`line[3:]` does not strip trailing whitespace) and a convention-name lookup that fails because of it.
- `evals/plan-feature/files/conventions-mock.md`: an eval fixture without trailing-whitespace headings.
- A note that there is no CONVENTIONS.md at the repository root.

None of this touches the `/api/v2/advisories` handler, advisory query/filter code, pagination helpers, or `X-Total-Count`/`Link` header code. The whitespace bug in plan-feature is a separate defect (ACME-500). It is **not** part of ACME-510 and must not be folded into this fix.

### Symbols/files that still need discovery (searches to run against acme-backend)
Real file paths could not be confirmed from the supplied context. These are the searches that would be run (`search_for_pattern` / Grep under `/home/dev/repos/acme-backend`):

| Goal | Search |
|---|---|
| Endpoint handler | `advisories` route registration, `"/api/v2/advisories"`, `/v2/advisor` |
| Date filter branch | `publishedAfter`, `published_after`, `publishedBefore`, `published_before`, `filterDateRange` |
| Pagination header emission | `X-Total-Count`, `x-total-count`, `rel=\"next\"`, `Link` header construction |
| Shared pagination helper | `Paginated`, `PaginatedResults`, `paginate`, `total` / `count` query helpers |
| Existing tests | handler/integration tests for advisories, tests asserting `X-Total-Count` |

Which branch skips the pagination wrapper or the count query (hypothesis (a) or (b)) has to be confirmed by these searches before implementation starts.

### Existing tests / patterns
- None for this endpoint appear in the supplied context. The search above should find integration tests for the unfiltered advisories list that assert `X-Total-Count`. Those tests are the pattern the reproducer should copy.

### CONVENTIONS.md
- The supplied context states that the repository has **no CONVENTIONS.md** at its root, so there are no repo conventions to apply.

### Persistence-impact analysis
- The affected output is HTTP response headers (total count and next link). They are computed **per request at query time** from the advisory table and are not written to the database.
- **No persistence boundary. No data migration needed.**

### Decomposition Guard (Step 6) check
- There is a single defect: the date-filtered list path loses its pagination metadata. Even if the fix touches both the handler and a query helper, it is one root cause. **Not a decomposition trigger.**
- The unrelated ACME-500 whitespace issue found in the supplied context is a separate bug that is already tracked. It is not bundled here.
