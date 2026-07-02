# implement-task TC-9202 — Execution Halted: Incomplete Task Description

## Step 0 — Validate Project Configuration

Project Configuration validated successfully:
- Repository Registry: contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key (TC), Cloud ID, Feature issue type ID all present
- Code Intelligence: configured with `serena_backend` instance using rust-analyzer

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the expected template.

### Gaps Identified

The task description for TC-9202 is **incomplete** and does not follow the required template. The following gaps prevent implementation from proceeding:

---

**1. Missing section: Implementation Notes**

The task description has no **Implementation Notes** section. This section is required by the template and must provide:
- Patterns and code references to follow when implementing the changes
- Guidance on which existing utilities, services, or modules to reuse (e.g., does the search module under `modules/search/` already provide reusable search infrastructure? Should `PackageService` be extended, or should a new service method be added?)
- References to specific code patterns in sibling modules (e.g., how `AdvisoryService` implements its `search` method in `modules/fundamental/src/advisory/service/advisory.rs`)
- Whether to use the existing `SearchService` in `modules/search/` or build package-specific search logic

Without Implementation Notes, there is no specification for *how* to implement the search — only *what* to implement. The skill cannot proceed without this guidance.

---

**2. Vague Acceptance Criteria**

The following acceptance criteria are not specific enough to be verifiable:

- **"Search results are relevant"** — This criterion is not actionable. "Relevant" is undefined. It does not specify:
  - Which fields should be searched (package name only? version? description? license? pURL?)
  - Whether partial/substring matching is required or only exact matches
  - Whether any relevance ranking or scoring algorithm should be applied
  - Whether typo tolerance or fuzzy matching is expected

- **"Performance is acceptable"** — This criterion has no measurable threshold. It does not specify:
  - A maximum response time (e.g., "responds within 200ms for datasets under 10,000 packages")
  - Whether database indexing is required
  - Whether pagination is expected for large result sets
  - Any concurrency or load requirements

The criterion "Users can search for packages" is directional but still lacks specificity about the search interface (query parameter name, supported operators, response shape).

---

**3. Vague Test Requirements**

- **"Test that search works correctly"** — This requirement does not define what "correctly" means. It does not specify:
  - Which search scenarios to test (exact match, partial match, no results, special characters, empty query)
  - What assertions to make on the response (status code, result count, field presence, result ordering)
  - Whether error cases should be tested (invalid query parameters, overly long queries)
  - Whether performance-related test assertions are needed

---

**4. Missing section: API Changes**

The task involves adding a search endpoint but does not include an **API Changes** section. This section should specify:
- The endpoint path (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`)
- Request parameters (query string format, supported filters)
- Response shape (does it return `PaginatedResults<PackageSummary>` like the existing list endpoint?)

---

## Clarifying Questions

Before proceeding with implementation, please provide answers to the following:

1. **Which fields should the search cover?** Should the search query match against the package name only, or also against other fields such as version, pURL, description, or license? Should it support partial/substring matching, or only exact matches?

2. **What does "relevant" mean for search results, and is ranking required?** Should results be ranked by relevance score (e.g., exact name match ranked higher than partial match), or is unranked filtering sufficient? Is fuzzy matching or typo tolerance expected?

3. **What is the performance threshold for "acceptable" performance?** Is there a maximum response time target (e.g., under 200ms)? Should the endpoint support pagination via `PaginatedResults<T>`? Are database indexes required?

4. **What is the API contract for the search endpoint?** Should this be a new endpoint (e.g., `GET /api/v2/package/search?q=...`) or a query parameter added to the existing list endpoint (`GET /api/v2/package?q=...`)? What should the response shape look like?

5. **What test scenarios define "works correctly"?** Specifically, which of the following should be covered: exact match, partial/substring match, case-insensitive match, no results found, empty query string, special characters in query, pagination of search results?

6. **Should this reuse the existing search module?** The repository has a `modules/search/` module with `SearchService` providing full-text search across entities. Should the package search integrate with this existing infrastructure, or should it be a standalone query within the package module?

---

## Execution Status

**Stopped.** Implementation cannot proceed until the gaps above are resolved. Per the skill protocol: the structured description is incomplete, so no branching, implementation planning, or code changes will be attempted.

Please update the task description with the missing Implementation Notes section, specific acceptance criteria, and detailed test requirements, then re-run `/implement-task TC-9202`.
