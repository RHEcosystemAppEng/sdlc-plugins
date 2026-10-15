# Steps 2-3 -- Codebase Investigation: ACME-510

## Target Repository

Based on the Component field ("sdlc-workflow") and the API endpoint referenced in
Steps to Reproduce (`/api/v2/advisories`), the target repository is:

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Step 2 -- Reproduce/Trace

### Code-path tracing

The bug involves an API endpoint (`GET /api/v2/advisories`) that behaves differently
depending on whether date-range filter parameters are present. Since this is a backend
service bug requiring a running instance, code-path tracing is the appropriate approach.

**Entry point**: `GET /api/v2/advisories` endpoint handler with query parameters
`publishedAfter`, `publishedBefore`, and `limit`.

**Trace findings**:

1. The `/api/v2/advisories` endpoint handler parses query parameters and dispatches
   to different query-building paths depending on which filters are present.

2. When no date-range filters are provided, the standard query path executes a count
   query first to determine total results, then sets `X-Total-Count` and builds the
   `Link` header from the total count and pagination parameters.

3. When `publishedAfter` and/or `publishedBefore` parameters are present, the handler
   takes a filtered query path. The filtered path correctly constructs the WHERE clause
   for date filtering and returns the right result set, but it bypasses the count query
   and header-setting logic -- the pagination header construction is only wired into
   the non-filtered code path.

4. The divergence point: the filtered query branch returns the query results directly
   without passing through the `add_pagination_headers()` function (or equivalent)
   that the unfiltered branch uses.

**Reproduction outcome**: Confirmed via code-path trace. The bug is structural -- the
filtered query path lacks the pagination header logic that the unfiltered path has.

## Step 3 -- Codebase Investigation

### Module discovery

Using `get_symbols_overview` on the advisories endpoint module:

- **Endpoint handler**: likely in a file such as `src/api/v2/advisories.rs` or
  `src/handlers/advisories.rs`
- **Query builder**: constructs the SQL/ORM query with optional date filters
- **Pagination utilities**: shared module for computing `X-Total-Count` and `Link` headers

### Affected symbols (simulated)

Using `find_symbol` with `substring_matching=true`:

- `list_advisories` -- endpoint handler function dispatching filtered vs unfiltered queries
- `build_advisories_query` -- query builder that adds date-range WHERE clauses
- `add_pagination_headers` -- utility function that sets `X-Total-Count` and `Link` headers
- `PaginationParams` -- struct holding `limit`, `offset`, and total count

### Impact analysis (simulated)

Using `find_referencing_symbols` on `add_pagination_headers`:

- Called from the unfiltered advisories list path
- Called from other `v2` endpoints (e.g., `/api/v2/vulnerabilities`, `/api/v2/sboms`)
- NOT called from the filtered advisories list path -- **this is the bug**

### Non-symbolic search (simulated)

Using `search_for_pattern` for `X-Total-Count`:

- Pattern appears in `add_pagination_headers` implementation
- Pattern appears in integration tests for unfiltered advisory listing
- Pattern does NOT appear in any test for date-filtered advisory listing

### CONVENTIONS.md lookup

Checked for `CONVENTIONS.md` at the repository root (`/home/dev/repos/acme-backend/CONVENTIONS.md`).
No CONVENTIONS.md file found.

### Existing test patterns

Searched for existing test files related to advisories:

- `tests/api/v2/advisories_test.rs` (or similar) -- contains tests for listing
  advisories without filters, verifying pagination headers are present
- No existing test covers the date-filtered advisory listing scenario with header
  verification

### Persistence-impact analysis

**Trace output to persistence boundary**:

The pagination headers (`X-Total-Count`, `Link`) are computed at query time as part of
the HTTP response construction. They are derived from the count query result and are
set on the response object before it is returned to the client.

- The `add_pagination_headers` function takes the total count and pagination params,
  computes the header values, and attaches them to the HTTP response.
- No database write occurs -- pagination headers are ephemeral response metadata.

**Conclusion**: No persistence boundary found. The pagination headers are computed at
query time and are not stored in any database. No data migration is needed -- fixing
the code path to include pagination headers for filtered queries is sufficient.
