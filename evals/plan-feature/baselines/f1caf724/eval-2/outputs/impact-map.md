# Repository Impact Map -- TC-9002: Improve search experience

## Workflow Mode: direct-to-main

**Rationale:** No atomicity indicators identified. Each task (performance indexes, relevance ranking, filter parameters) modifies the search module independently and can land on `main` without breaking other tasks. No coordinated schema migrations between tasks (the index migration is consumed but not co-dependent), no breaking API changes between tasks, and no cross-cutting refactors that require simultaneous delivery.

## Field Inheritance

- **Priority:** Normal (inherited from TC-9002; will be propagated to all created tasks)
- **fixVersions:** RHTPA 1.6.0 (inherited from TC-9002; will be propagated to all created tasks -- no `fixVersion scope` restriction found in Jira Field Defaults section, defaulting to "both")

## Hierarchy

No Epic-level issue type information available from project metadata. Tasks will be created directly under the Feature (Feature -> Task hierarchy).

Default epic grouping strategy in CLAUDE.md is `by-sub-feature`, but this applies only when a level-1 issue type is discovered. Without issue type discovery data, Epic grouping is skipped.

## trustify-backend

### Changes
- Add database migration with GIN indexes on text-searchable columns (sbom name/description, advisory title/description, package name) to improve search query performance
- Implement PostgreSQL full-text search ranking (tsvector/tsquery with ts_rank) in SearchService to improve result relevance, with configurable field weighting
- Add filter query parameters (entity_type, created_after, created_before) to the search endpoint for narrowing results by category and date range

## Ambiguities Identified

The following ambiguities were identified in the TC-9002 feature description. These must be clarified with the product owner before or during implementation:

### Ambiguity 1: "Search should be faster" -- no performance target

The feature states search is "currently too slow" but provides no baseline metrics (current p50/p95 latency), no target metrics (acceptable response time), and no indication of which search operations are slow (simple queries, complex queries, large result sets). The non-functional requirement "should be fast enough" similarly lacks any quantifiable target.

**Assumption pending clarification:** We will add GIN indexes and optimize queries; performance improvement will be validated by comparing query execution plans (EXPLAIN output) before and after. Without a specific SLA, we cannot guarantee the improvement meets unstated expectations.

### Ambiguity 2: "Results should be more relevant" -- no relevance criteria defined

The feature does not specify what constitutes a "relevant" result, which fields should be weighted more heavily in ranking, whether relevance is relative to the search query alone or considers user context, or what ranking algorithm to use. "Users complain about irrelevant results" does not identify the specific failure mode (wrong results, poor ordering, missing results).

**Assumption pending clarification:** We will implement PostgreSQL full-text search with `ts_rank`, weighting title/name fields (weight A) higher than description/body fields (weight D). Results will be sorted by relevance score by default when a text query is provided.

### Ambiguity 3: "Add filters" -- no filter specification

The feature says "some kind of filtering capability" without specifying which attributes should be filterable, how filters combine (AND vs OR logic), what the filter UI should look like, or whether filters apply uniformly across entity types or are type-specific (e.g., severity only for advisories).

**Assumption pending clarification:** We will add filters for entity type (SBOM, advisory, package) and date range (created_after, created_before). Filters will combine with AND logic. Additional filters (severity, license, etc.) can be added in follow-up work once requirements are clarified.

### Ambiguity 4: "Should be fast enough" -- no quantitative NFR

The non-functional requirement provides no specific performance SLA, percentile target, or maximum acceptable latency. There is no indication of expected data scale (number of SBOMs, advisories, packages) or concurrent user load.

**Assumption pending clarification:** We will ensure query response times are reasonable for typical workloads and document actual performance characteristics for product owner review.

### Ambiguity 5: "Don't break existing functionality" -- no regression criteria

No specific regression test suite, backward-compatibility constraints, or API versioning strategy is specified. It is unclear whether "existing functionality" refers to the search API contract, search result quality, or the broader platform.

**Assumption pending clarification:** We will maintain backward compatibility on the search API endpoint -- existing query parameters continue to work unchanged, and new parameters (sort, filters) are optional additions. The existing integration tests in `tests/api/search.rs` serve as the regression baseline.

## Excluded Requirements

### "Better UI" (Non-MVP)

**Requirement:** "Make it look nicer" (marked as non-MVP in the feature requirements table).

**Reason for exclusion:** This requirement cannot be planned for the following reasons:
1. **No design mockups or Figma link provided.** The feature description contains no Figma URL and no visual specification for what "better" means.
2. **No frontend repository in scope.** The Repository Registry in CLAUDE.md contains only `sdlc-plugins` (this plugin repo). The `trustify-backend` repository from the fixture is a Rust backend service with no frontend code. UI improvements require a frontend repository to target.
3. **Insufficient specification.** "Make it look nicer" provides no actionable design direction -- no wireframes, no component specifications, no user research findings.

This requirement should be revisited when design mockups are available and a frontend repository is added to the Repository Registry.

---

*This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.8.*
