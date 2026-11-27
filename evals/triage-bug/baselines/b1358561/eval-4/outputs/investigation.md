# Steps 2–3 — Reproduction/Trace and Codebase Investigation (ACME-510)

## Step 2 — Reproduce/Trace

### Runnable reproduction

The Steps to Reproduce are runnable (start backend, then
`curl -i "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10"`).
In this eval no external services or processes may be run, so reproduction was **not attempted**.
Outcome: **not executed (eval constraint)**. The reproduction a human or implement-task would run:

| Request | Expected headers | Reported behavior |
|---|---|---|
| `GET /api/v2/advisories?limit=10` | `X-Total-Count`, `Link; rel="next"` | Present (correct) |
| `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` | `X-Total-Count`, `Link; rel="next"` | **Absent**; body correct |

### Code-path trace (from bug evidence)

- Entry point: HTTP handler for `GET /api/v2/advisories` in `acme-backend`.
- Key differential: the **same endpoint** returns pagination headers without date filters and drops them when `publishedAfter`/`publishedBefore` are supplied, while the body is still correctly filtered and limited.
- This means the divergence happens inside the advisories list path at the point where the date-range parameters are handled. Filtering itself works. What gets lost is the pagination metadata (total count and next-page link) or the step that writes it into response headers.
- Terminology inconsistency to note: the Issue Description says `filterDateRange` parameters, but the Steps to Reproduce use `publishedAfter`/`publishedBefore`. The investigation treats `publishedAfter`/`publishedBefore` as authoritative (they are the concrete reproducer). `filterDateRange` is probably the internal name of the filter (a struct or function).

## Step 3 — Codebase Investigation

### Target repository

- The Component field is `sdlc-workflow`, which matches no entry in the Repository Registry.
- The bug describes a REST API (`/api/v2/advisories`) in a "backend service", and the only registered repository is **`acme-backend`** (Rust backend service, path `/home/dev/repos/acme-backend`, Serena instance `serena_backend`).
- Target: **acme-backend**.

### Code intelligence

The Code Intelligence section says no Serena MCP servers are configured, so the Read/Grep/Glob fallback applies against `/home/dev/repos/acme-backend`.

### Findings from the provided repository context

The provided repository context (`repo-context-mock.md`) **does not cover this bug**:

- Its header says it simulates code paths for **ACME-500**, not ACME-510.
- It contains only excerpts from `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` about a CONVENTIONS.md heading-whitespace defect (`line[3:]` not stripping trailing whitespace) and the eval fixture `evals/plan-feature/files/conventions-mock.md`.
- It has no advisories endpoint, pagination helper, date-filter logic, or Rust source files.

**These excerpts were deliberately not used as evidence for ACME-510.** They are unrelated to pagination headers, and using them would produce a made-up root cause.

The only relevant fact from the context: **the repository has no CONVENTIONS.md at its root**, so no conventions feed into Implementation Notes.

### Affected files and symbols

No concrete file paths or symbol names could be confirmed from the available material. The searches below are what Step 3 would run against `acme-backend` to pin them down. Implement-task must run them, since the Task cannot list verified paths.

| Goal | Search (Grep/Glob fallback) |
|---|---|
| Locate the advisories list handler | Grep `"/advisories"`, `"/api/v2/advisories"`, `fn list_advisories`, `fn get_advisories` in `**/*.rs` |
| Locate date-range filter handling | Grep `publishedAfter`, `published_after`, `publishedBefore`, `published_before`, `filterDateRange`, `filter_date_range`, `DateRange` |
| Locate pagination header emission | Grep `X-Total-Count`, `x-total-count`, `rel=\"next\"`, `header::LINK`, `Paginated`, `PaginatedResults`, `total` |
| Locate count query | Grep `.count(`, `count_query`, `fetch_page`, `paginate(` |
| Existing tests for the endpoint | Glob `**/tests/**/*advisor*.rs`, `**/*advisor*test*.rs`; Grep `X-Total-Count` in tests |

### Expected shape of the defect (to be confirmed by the searches above)

The body is filtered correctly while the headers disappear only with date filters. That points to one of these:

1. **Separate code branch**: the handler (or service) has an `if let Some(date_range)` branch that runs a filtered query and returns a plain list (`Vec<Advisory>`) or JSON body directly. That branch skips the shared paginated-response wrapper or header helper that the unfiltered branch uses.
2. **Count failure swallowed**: the total-count query is built without the date predicates, or fails with them (for example a type/bind mismatch on the date columns), and the error path silently omits the headers instead of failing.
3. **Header builder conditional**: the helper that writes `X-Total-Count`/`Link` gets a `None` total when filters are present. It also builds the `Link` URL from a query struct that does not carry the date parameters.

Option 1 fits the symptom best: body correct, headers entirely absent (not wrong), unfiltered path fine. Option 2 also fits if errors are swallowed. All three share one root cause (date-filtered list path does not produce pagination metadata), so the **Decomposition Guard (Step 6) is not triggered**.

### Reuse candidates (to confirm)

- Whatever pagination helper or wrapper the **unfiltered** advisories path already uses to emit `X-Total-Count` and `Link`. The fix should route the date-filtered path through the same helper and not duplicate header logic.
- The existing `Link` URL builder must keep `publishedAfter`/`publishedBefore` in the `rel="next"` URL, so page 2 is still filtered.

### Persistence-impact analysis

- The affected output is HTTP response headers derived from a count query on each request.
- No value is written to a database. Pagination metadata is computed **at query time**.
- **No persistence boundary**, so no data migration is needed.

### Test patterns

No existing test files for the advisories endpoint could be confirmed from the provided context. Implement-task should look for existing integration tests that assert response headers on list endpoints (Grep `X-Total-Count` under `tests/`) and copy their setup (test server / seeded DB) and assertion style.
