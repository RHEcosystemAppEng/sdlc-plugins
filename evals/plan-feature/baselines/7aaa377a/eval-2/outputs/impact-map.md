# Repository Impact Map — TC-9002: Improve search experience

## trustify-backend

### Changes

- Add database migration to create indexes on frequently searched columns (SBOM name/version, advisory title/severity, package name/license) to improve full-text search query performance
- Optimize SearchService query execution to use indexed columns and improve result ranking by relevance scoring
- Extend the search API endpoint (`GET /api/v2/search`) to accept filter query parameters for entity type, severity, and date range
- Extend shared query builder helpers in `common/src/db/query.rs` to support the new search filter types
- Add and update integration tests in `tests/api/search.rs` covering filtered search, relevance ordering, and query performance characteristics

## Excluded requirements

The following requirements from TC-9002 cannot be decomposed into actionable tasks due to missing inputs:

| Requirement | Reason for Exclusion |
|---|---|
| "Better UI" (non-MVP) | No frontend repository is available in the Repository Registry. The only target repository (`trustify-backend`) is a Rust backend service. UI improvements require a frontend repository to be added to the project configuration. |
| Specific performance targets for "Search should be faster" | The feature description states "currently too slow" but provides no latency benchmarks, target response times, or measurement criteria. The planning proceeds with index and query optimizations, but acceptance testing against specific latency thresholds requires the engineer to define quantified targets (e.g., "p95 search latency < 200ms"). |
| Relevance ranking definition for "Results should be more relevant" | The feature description states "users complain about irrelevant results" but does not define what constitutes a relevant result, ranking criteria, or weighting factors. The planning proceeds with basic relevance scoring improvements (e.g., full-text search rank), but a domain-specific relevance model requires product input. |
| Specific filter fields for "Add filters" | The requirement says "some kind of filtering capability" without specifying which fields should be filterable. The planning assumes entity-type, severity, and date-range filters based on the existing data model. The engineer should confirm the filter set with the product owner. |
| Non-functional requirement "Should be fast enough" | No quantified performance target is provided. This NFR cannot be validated without a concrete threshold. |

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations: the search index migration is additive and does not break existing queries — it can land independently.
- No breaking API changes: the filter parameters are additive query parameters on an existing endpoint — existing callers are unaffected.
- No cross-cutting refactors: changes are contained within the search module, common query helpers, and test files.
- No tightly coupled components: each task (indexing, query optimization, filter support, tests) delivers independent value on `main`.

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration)

| Epic | Tasks | Description |
|---|---|---|
| TC-9002: Search Performance Optimization | Task 1, Task 2 | Database indexing and query execution improvements to reduce search latency |
| TC-9002: Search Filtering | Task 3, Task 4 | Filter parameter support on the search endpoint and integration test coverage |

## Field Inheritance

The following fields will be propagated from TC-9002 to all created tasks and epics:

- **Priority:** Normal (propagated — not "Undefined")
- **Fix Versions:** RHTPA 1.6.0 (propagated — fixVersion scope defaults to "both" since no Jira Field Defaults configured)
- **Labels:** ai-generated-jira (applied to all created issues)

## additional_fields (for all created issues)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```
