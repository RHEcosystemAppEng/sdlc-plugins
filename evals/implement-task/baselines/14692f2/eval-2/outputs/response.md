# implement-task: TC-9202 — Response

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md (`claude-md-mock.md`) contains the required sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID.
3. **Code Intelligence** — present, includes tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 1 — Fetch and Parse Jira Task

Parsed the task description for TC-9202:

| Section | Status | Value |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **MISSING** | No API Changes section provided |
| Implementation Notes | **MISSING** | No Implementation Notes section provided |
| Acceptance Criteria | Present (but vague) | See analysis below |
| Test Requirements | Present (but vague) | See analysis below |
| Target PR | Not present (optional) | — |
| Review Context | Not present (optional) | — |
| Bookend Type | Not present (optional) | — |
| Dependencies | Not present | — |

### Acceptance Criteria quality analysis

The acceptance criteria are vague and non-verifiable:

- "Users can search for packages" — does not specify the search mechanism (query parameter? full-text? substring match?), the endpoint path, HTTP method, or request/response shape.
- "Search results are relevant" — subjective criterion with no measurable definition. Does not specify ranking algorithm, filtering behavior, or what "relevant" means.
- "Performance is acceptable" — no quantitative target (e.g., latency threshold, result count limit).

### Test Requirements quality analysis

The test requirements are similarly vague:

- "Test that search works correctly" — does not specify what scenarios to test, what assertions to make, what inputs to use, or what "correctly" means.

## Decision: STOP — Missing and Vague Sections

Per the skill's rules in Step 1:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

The task description is **incomplete**. The following gaps must be resolved before implementation can proceed:

### Missing sections

1. **API Changes** — This section is required to know the endpoint path, HTTP method, query parameters, request/response types, and how the search endpoint integrates with the existing `/api/v2/package` route structure. For example:
   - What is the endpoint path? `GET /api/v2/package/search`? Or a query parameter on `GET /api/v2/package?q=...`?
   - What query parameters does it accept (search term, pagination, filters)?
   - What is the response shape — `PaginatedResults<PackageSummary>`?

2. **Implementation Notes** — This section is required to know which existing patterns, services, and utilities to follow. Based on the repository structure, critical questions include:
   - Should the search use the existing `SearchService` from `modules/search/` or implement search directly in `PackageService`?
   - Should it use `common/src/db/query.rs` shared query helpers for filtering and pagination?
   - What search mechanism should be used — SQL `LIKE`/`ILIKE`, PostgreSQL full-text search (`tsvector`/`tsquery`), or integration with the existing `SearchService`?
   - Which existing endpoint (e.g., `sbom/endpoints/list.rs` or `advisory/endpoints/list.rs`) should serve as the pattern to follow?

### Vague sections requiring clarification

3. **Acceptance Criteria** — The criteria need to be specific and verifiable:
   - What fields should be searchable (package name, version, license, purl)?
   - What type of search matching is expected (exact, substring, full-text)?
   - What is the expected response format and pagination behavior?
   - What is the "acceptable" performance target (e.g., < 500ms for 10k packages)?

4. **Test Requirements** — The test requirements need specifics:
   - What test scenarios should be covered (search with results, search with no results, empty query, special characters)?
   - Should there be integration tests in `tests/api/` following the existing `search.rs` test patterns?
   - What assertions are expected (status codes, response body structure, result count, field values)?

### Action required

Please provide the missing **API Changes** and **Implementation Notes** sections, and clarify the vague **Acceptance Criteria** and **Test Requirements** before I proceed with implementation. Alternatively, re-run `/plan-feature` to regenerate this task with a complete structured description.

**No subsequent steps (branching, code inspection, implementation, testing, or Jira updates) will be performed until the missing information is provided.**
