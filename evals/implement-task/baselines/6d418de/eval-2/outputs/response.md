# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Checked the project's CLAUDE.md for required sections under `# Project Configuration`:

1. **Repository Registry** — Present. Contains `trustify-backend` mapped to Serena instance `serena_backend`.
2. **Jira Configuration** — Present. Project key `TC`, Cloud ID, Feature issue type ID, and custom fields are all configured.
3. **Code Intelligence** — Present. Tool naming convention documented; `serena_backend` instance configured with `rust-analyzer`.

Project Configuration is valid. Proceeding to Step 1.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP call `jira.get_issue("TC-9202")` to fetch the task. (Skipped per eval instructions — using provided task description file instead.)

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Validating all required sections against the template:

| Section | Status | Assessment |
|---|---|---|
| Repository | Present | `trustify-backend` — valid |
| Target Branch | Present | `main` — valid |
| Description | Present | Vague — "Add search capabilities to the package module so users can find packages more easily." No specifics on what kind of search (full-text, filtered listing, fuzzy match), what fields are searchable, or how it integrates with the existing `modules/search/` module. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — valid |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — valid |
| **API Changes** | **MISSING** | No API Changes section. A search endpoint requires specifying: HTTP method, path (e.g., `GET /api/v2/package/search`), query parameters (search term, filters, pagination), and response shape. |
| **Implementation Notes** | **MISSING** | No Implementation Notes section. Critical gaps: no guidance on which patterns to follow (e.g., does this reuse `SearchService` from `modules/search/`, or implement search directly in `PackageService`?), no code references to existing search implementations (e.g., `AdvisoryService::search`), no indication of whether full-text search or SQL LIKE/ILIKE filtering is expected, no mention of which query helpers from `common/src/db/query.rs` to use. |
| Acceptance Criteria | Present | **Too vague to be actionable.** All three criteria are subjective and unmeasurable: "Users can search for packages" (by what field? what input?), "Search results are relevant" (what defines relevance?), "Performance is acceptable" (what threshold? what dataset size?). Acceptance criteria must be specific and verifiable. |
| Test Requirements | Present | **Too vague to be actionable.** Single item "Test that search works correctly" provides no guidance on: which scenarios to test (empty query, no results, partial match, pagination), expected assertions, error cases (invalid input, 400/404 responses), or whether integration tests in `tests/api/` are expected. |
| Target PR | Not present | Optional — OK |
| Bookend Type | Not present | Optional — OK |
| Dependencies | Not present | Optional — OK |

### Gaps Identified

The task description is **incomplete** and cannot be implemented as-is. The following gaps must be resolved before proceeding:

**Missing required sections:**

1. **API Changes**: The search endpoint's HTTP method, URL path, query parameters, and response shape are not specified. For example:
   - What is the endpoint path? (`GET /api/v2/package/search` vs `GET /api/v2/package?q=...`)
   - What query parameters does it accept? (search term, filters like license/namespace, pagination params)
   - What is the response shape? (`PaginatedResults<PackageSummary>` or a different type?)

2. **Implementation Notes**: No patterns or code references are provided. Key questions:
   - Should this reuse the existing `SearchService` from `modules/search/` or implement search logic directly in `PackageService`?
   - What search mechanism is expected — full-text PostgreSQL search (`tsvector`/`tsquery`), SQL `ILIKE` filtering, or integration with an external search index?
   - Should the implementation follow the pattern in `AdvisoryService` which already has a `search` method, or use a different approach?
   - Which fields on `PackageSummary` should be searchable (name, namespace, license, all)?

**Present but insufficiently specified sections:**

3. **Acceptance Criteria**: All three criteria are subjective. They need to be rewritten with measurable, verifiable conditions. For example:
   - "Users can search packages by name using a `q` query parameter" (instead of "Users can search for packages")
   - "Search for 'openssl' returns packages whose name contains 'openssl'" (instead of "Search results are relevant")
   - "Search endpoint responds within 500ms for queries against 10k packages" (instead of "Performance is acceptable")

4. **Test Requirements**: The single test item is too vague to guide implementation. It should specify:
   - Which test scenarios are required (successful search, empty results, pagination, invalid input)
   - Where tests should be written (e.g., `tests/api/package.rs` or a new `tests/api/package_search.rs`)
   - What assertions to make (status codes, response body structure, result counts)

## Execution Stopped — Clarification Required

Per the implement-task skill rules, I am stopping execution immediately. The task description has missing required sections (API Changes, Implementation Notes) and vague required sections (Acceptance Criteria, Test Requirements) that prevent deterministic implementation.

**I will not proceed with branching, code inspection, implementation planning, or code changes until these gaps are resolved.**

Please update the TC-9202 task description in Jira with:
1. An **API Changes** section specifying the endpoint contract (method, path, parameters, response type)
2. An **Implementation Notes** section with patterns to follow and architectural decisions (e.g., SearchService reuse vs. direct SQL, search mechanism)
3. Revised **Acceptance Criteria** with specific, measurable, and verifiable conditions
4. Revised **Test Requirements** with concrete test scenarios, file locations, and expected assertions

Once the description is updated, re-run `/implement-task TC-9202` to continue.
