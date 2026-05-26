# implement-task TC-9202 — Clarification Required

## Step 0 — Project Configuration Validation

The project CLAUDE.md (claude-md-mock.md) contains all required sections:

- `## Repository Registry` — present, includes `trustify-backend` with Serena instance `serena_backend`
- `## Jira Configuration` — present, with project key TC, Cloud ID, and feature issue type ID
- `## Code Intelligence` — present, with tool naming convention documented

Project configuration is valid. Proceeding to Step 1.

---

## Step 1 — Fetch and Parse Jira Task

Parsed the task description for TC-9202. The following required sections are present:

| Section | Status |
|---|---|
| Repository | present — `trustify-backend` |
| Target Branch | present — `main` |
| Description | present |
| Files to Modify | present |
| Files to Create | present |
| API Changes | **missing** |
| Implementation Notes | **missing** |
| Acceptance Criteria | present but vague (see below) |
| Test Requirements | present but vague (see below) |

---

## Gaps Identified

The task description has three significant gaps that prevent safe implementation. Per the skill rules, execution stops here until these are resolved.

### Gap 1 — Missing Implementation Notes section

The task has no **Implementation Notes** section. This section is required to specify:

- Which existing patterns to follow (e.g., how the advisory search endpoint at `modules/fundamental/src/advisory/service/advisory.rs` is structured)
- Whether to reuse the existing `modules/search/` module or add search directly to `PackageService`
- Which query builder helpers from `common/src/db/query.rs` to use for filtering
- How to register the new route in `modules/fundamental/src/package/endpoints/mod.rs`

Without Implementation Notes, the implementation risks diverging from project conventions and duplicating logic that already exists in the `modules/search/` module.

### Gap 2 — Vague Acceptance Criteria

The acceptance criteria are not testable as written:

- "Search results are relevant" — no definition of relevance (full-text match? substring? fuzzy?)
- "Performance is acceptable" — no threshold specified (response time? query plan? result count?)

These criteria cannot be verified in Step 8 without a concrete definition.

### Gap 3 — Vague Test Requirements

"Test that search works correctly" is not actionable. It does not specify:

- Which test scenarios to cover (happy path, empty results, partial match, case sensitivity, pagination)
- Which file to add tests to (the existing `tests/api/` directory follows a per-module pattern; there is no `tests/api/package.rs` listed)
- Whether to test against a real PostgreSQL instance (as sibling tests in `tests/api/` do) or use mocks

---

## Clarifying Questions

Before proceeding with branching or implementation, I need answers to the following:

**Q1 — Which package fields should be searched, and what matching strategy is required?**

The `PackageSummary` struct (in `modules/fundamental/src/package/model/summary.rs`) likely has fields such as name, version, and license. Should the search endpoint:
- Match only on package name?
- Match on name and version?
- Match on name, version, and license?
- Use exact/prefix matching, substring matching, or full-text search (PostgreSQL `tsvector`/`to_tsquery`)?
- Reuse the existing `modules/search/` service (which provides full-text search across entities), or implement a package-specific filter on the existing list endpoint?

**Q2 — What does "search results are relevant" mean concretely?**

Please define the relevance behavior the endpoint must exhibit. For example:
- Results must contain packages whose name includes the query string (case-insensitive substring match)?
- Results must be ranked by match score (full-text relevance ranking)?
- Results that exactly match the query string should appear before partial matches?

This definition will be used to verify Acceptance Criteria in Step 8 and to write meaningful assertions in tests.

**Q3 — What is the performance threshold for "performance is acceptable"?**

Please provide a concrete, measurable criterion, for example:
- The search endpoint must respond within 200 ms for a dataset of 10,000 packages
- The query must use a database index (no sequential scan)
- The endpoint must support pagination using the existing `PaginatedResults<T>` wrapper (from `common/src/model/paginated.rs`) with a default page size

Without a threshold, this criterion cannot be verified in Step 8.

**Q4 — What test scenarios should be covered, and where should the test file live?**

The sibling test files are in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`). Should I create `tests/api/package.rs`? And which scenarios are required — for example:
- `GET /api/v2/package/search?q=<term>` returns 200 with matching packages
- `GET /api/v2/package/search?q=<nonexistent>` returns 200 with an empty result set
- `GET /api/v2/package/search` with no query parameter returns 400 or falls back to listing all packages

---

## Next Steps

Once you provide answers to the questions above, I will:

1. Update the understanding of the implementation scope
2. Proceed to Step 2 (dependency verification — TC-9001 must be Done)
3. Continue through Steps 3–11 as normal

**Execution is paused. No branches have been created and no code has been modified.**
