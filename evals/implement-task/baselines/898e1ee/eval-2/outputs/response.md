# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md verified:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, with tool naming convention `mcp__<serena-instance>__<tool>`

Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the expected template sections:

| Section              | Status      | Notes |
|----------------------|-------------|-------|
| Repository           | Present     | `trustify-backend` |
| Target Branch        | Present     | `main` |
| Description          | Present     | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify      | Present     | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create      | Present     | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes          | **Missing** | No API Changes section found |
| Implementation Notes | **Missing** | No Implementation Notes section found |
| Acceptance Criteria  | Present     | But criteria are vague (see below) |
| Test Requirements    | Present     | But requirements are vague (see below) |
| Dependencies         | Not present | (optional -- acceptable) |

### Missing Sections

1. **Implementation Notes** -- This section is entirely absent. The Implementation Notes section is critical because it specifies which existing code patterns to follow, which utilities and helpers to reuse, and which concrete code references to model the implementation after. Without it, there is no guidance on how to integrate the search endpoint with the existing codebase (e.g., whether to use the existing `SearchService` in `modules/search/`, or the query helpers in `common/src/db/query.rs`, or a new approach entirely).

2. **API Changes** -- This section is missing. There is no specification for the search endpoint's HTTP method, URL path, query parameters, request/response shape, or pagination behavior.

### Vague Acceptance Criteria

The Acceptance Criteria section contains three items, two of which are too vague to verify:

- "Users can search for packages" -- Minimally actionable, but does not specify **which fields** are searchable (package name? version? license? description? PURL?).
- **"Search results are relevant"** -- This is not a verifiable acceptance criterion. "Relevant" is undefined. Does this mean exact match? Substring match? Full-text search with ranking? TF-IDF scoring? What constitutes a relevant result vs. an irrelevant one?
- **"Performance is acceptable"** -- This is not a verifiable acceptance criterion. "Acceptable" is undefined. What is the maximum acceptable response time? Under what data volume (10 packages? 10,000? 1,000,000?)? Is there a specific latency SLA (e.g., p95 < 200ms)?

### Vague Test Requirements

The Test Requirements section contains a single item:

- **"Test that search works correctly"** -- This is not actionable. It does not specify what scenarios to test, what inputs to use, what outputs to expect, or what edge cases to cover (e.g., empty query, no results, special characters, pagination, case sensitivity).

## Execution Halted

Per the SKILL.md instructions:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

> "If the structured description is incomplete, ask the user for clarification and stop execution. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

The task description is incomplete. I am stopping execution and requesting clarification before proceeding with any implementation work.

## Clarifying Questions

Please provide the following information so the task description can be completed:

1. **Which fields should be searchable?** The package entity (in `entity/src/package.rs`) likely has fields such as name, version, license, namespace/PURL, and description. Which of these fields should the search endpoint query against? Should the search match against a single field (e.g., name only) or multiple fields simultaneously?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by relevance (e.g., using PostgreSQL full-text search with `ts_rank`), or is a simple `ILIKE`/substring filter sufficient? If ranked, what determines relevance -- exact match > prefix match > substring match? Should the existing `SearchService` in `modules/search/` be reused, or is this a module-specific search with different behavior?

3. **What is the concrete performance threshold?** "Performance is acceptable" needs a measurable target. What is the maximum acceptable response time (e.g., p95 < 500ms)? Under what data volume should this hold (e.g., 100K packages)? Should the implementation include database indexing (e.g., GIN index for full-text search)?

4. **What is the API contract for the search endpoint?** What HTTP method and path should be used (e.g., `GET /api/v2/package/search?q=...` vs. adding a query parameter to the existing `GET /api/v2/package` list endpoint)? Should results use the existing `PaginatedResults<PackageSummary>` response wrapper? What query parameters should be supported (q, limit, offset, sort)?

5. **What specific test scenarios are required?** For example: search with matching results, search with no results, search with empty query string, search with special characters, pagination of search results, case-insensitive matching? Should tests follow the existing integration test pattern in `tests/api/` against a real PostgreSQL test database?

6. **What Implementation Notes / patterns should be followed?** Should the implementation follow the pattern used by the existing `advisory` module (which already has a `search` capability in `AdvisoryService`)? Should it reuse `common/src/db/query.rs` query helpers? Are there specific Rust crates or PostgreSQL features to use (e.g., `tsvector`, `ILIKE`, `similarity()`)?

Please update the task description with the missing sections and clarified criteria, then re-run `/implement-task TC-9202`.
